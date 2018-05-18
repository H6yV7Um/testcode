#coding:utf-8
from telnetlib import Telnet
import logging

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash

from .models import CommonConfig, SvcLoadClient, SvcLoadClientForm, LoadTestRecord, AutoTestRecord
from utils import slice_seq, only_support_post
from dataprocess import response_msg, make_struct, JenkinsJob, InvalidJobError
from data_runner import data_runners
from data_runner.data_runners import MasterRunner, global_runner
from deploy.main import main
from deploy.deploy_settings import LOCUST_MASTER


logger = logging.getLogger('svc_web')

@login_required(login_url='admin/login')
def test(req):
    return HttpResponse('Hello World!')

def index(req):
    if req.user.is_authenticated:
        return render_to_response('index.html')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))

def get_user_profile(req):
    user = req.user
    if user.is_authenticated:
        group = user.groups.get_queryset()
        user_profile = {
            'name': user.get_username(), 
            'group': group.first().name if group.count() else None,
            'is_super': user.is_superuser
            }
        return response_msg(user_profile)
    return response_msg(3)

def user_logout(req):
    logout(req)
    return response_msg('%s?next=%s' % (settings.LOGIN_URL, '/'))

@only_support_post
def change_password(req):
    user = req.user
    new_password = req.POST.get('password1', None)
    if user.is_authenticated:
        user.set_password(new_password)
        user.save()
        login(req, user)
        # update_session_auth_hash(req, user)
        return response_msg(1)
    else:
        return response_msg(3)

def client_list(req):
    data_list = list(SvcLoadClient.objects.values('id', 'client_ip', 'role', 'slave_count', 'status'))
    return response_msg(data_list)

def master_exists(req):
    master = SvcLoadClient.objects.filter(role='1', status=1)
    if req.POST.get('role', None) == '1' and master.count() != 0:
        if int(req.POST.get('id', -1)) != master.first().id:
            return True
    return False

@only_support_post
def add_client(req):
    if master_exists(req):
        return response_msg("Master exists!")
    new_client = SvcLoadClientForm(req.POST)
    if new_client.is_valid():
        new_client.save()
        msg = 1
    else:
        msg = new_client.error_message
    return response_msg(msg)

@login_required
@only_support_post
def update_client(req):
    if master_exists(req):
        return response_msg("Master exists!")
    pk_id = req.POST.get('id', None)
    client = SvcLoadClient.objects.get(pk=pk_id)
    new_client = SvcLoadClientForm(req.POST, instance=client)
    if not new_client.is_valid():
        return response_msg(new_client.error_message)
    new_client.save()
    return response_msg(1)

@login_required(login_url='admin/login')
@only_support_post
def del_client(req):
    pk_id = req.POST.get('id', None)
    is_deleted = SvcLoadClient.objects.filter(pk=pk_id).delete()
    if not is_deleted:
        return response_msg('delete fail')
    return response_msg(1)

# @login_required
@only_support_post
def deploy(req):
    try:
        params = req.POST.dict()
        cmd_code = int(params['opcode'])
        path = params.get('path', None)
        main(cmd_code, path)
        return response_msg(1)
    except KeyError as e:
        return response_msg("Param opcode can not be null")
    except ValueError as e:
        return response_msg(e.args)

global_runner = MasterRunner()
@only_support_post
def start_hatch_data(req):
    try:
        if global_runner.state != 'connected':
            return response_msg("请先重置数据!")
        struct = make_struct(req)
        if struct["data_struct"]['total'] < len(global_runner.clients.connected):
            return response_msg('数据量必须大于等于slave数量')
        if global_runner.start_hatch(struct):
            return response_msg(1)
        else:
            return response_msg("Make data failed!")   
    except Exception as e:
        logger.error('Hatch data error', exc_info=True)
        return response_msg(e.args)

def req_stats(req):
    data = [value for value in data_runners.global_stats.values()]
    return response_msg(data)

def reset(req):
    if global_runner:
        global_runner.reset()
        return response_msg(1)
    else:
        return response_msg("data runner stopped!")

def get_locust_master(req):
    locust_master_ip = LOCUST_MASTER
    try:
        t = Telnet(locust_master_ip, 8089, timeout=5)
        t.close()
        return response_msg({'locust_master': locust_master_ip})
    except:
        return response_msg("locust master-%s do not start!" % locust_master_ip)
    
def get_load_test_record(req):
    record_list = list(LoadTestRecord.objects.values(
        "id", "start_time", "end_time", "user_count", "hatch_rate",
        "total_rps", "fail_ratio", "status"
    ))
    return response_msg(record_list)

def get_load_test_stats(req):
    param = req.GET or req.POST
    pk_id = param.get("record_id", None)
    if pk_id:
        record = LoadTestRecord.objects.get(pk=pk_id)
        return response_msg(record.stats)
    return response_msg("record_id can not be null")

def get_load_test_exceptions(req):
    param = req.GET or req.POST
    pk_id = param.get("record_id", None)
    if pk_id:
        record = LoadTestRecord.objects.get(pk=pk_id)
        return response_msg(record.exceptions)
    return response_msg("record_id can not be null")

def start_build(req):
    try:
        param = req.GET or req.POST
        job_name = param.get('job_name', None)
        mail_switch = param.get('mail_switch', 'true')
        job = JenkinsJob(job_name)
        if not job.start_build(mail_switch):
            return response_msg('Job is running...')
        return response_msg(1)
    except InvalidJobError as e:
        return response_msg(e.args)
    except Exception as e:
        logger.error('Build Error:', exc_info=True)
        return response_msg(e.args)

def stop_build(req):
    try:
        param = req.GET or req.POST
        job_name = param.get('job_name', None)
        bn = int(param.get('build_no', None))
        JenkinsJob(job_name).stop_build(bn)
        pk_id = param.get('id', None)
        record = AutoTestRecord.objects.get(pk=pk_id)
        record.status = 3
        record.save()
        return response_msg(1)
    except (TypeError, ValueError):
        return response_msg('build_no needed and must be int!')
    except KeyError as e:
        return response_msg(e.args)
    except Exception as e:
        logger.error("Stop Jenkins Build Error:", exc_info=True)
        return response_msg(e.args)

def get_func_test_record(req):
    record_list = list(AutoTestRecord.objects.values(
        "id","job_name","build_no","success_count","error_count",
        "failure_count","status","start_time","end_time","report_url"
    ))
    return response_msg(record_list)

def get_func_test_error_msg(req):
    param = req.GET or req.POST
    info_type = param.get("info_type")
    pk_id = param.get("pk_id")
    record = AutoTestRecord.objects.get(pk=pk_id)
    if info_type == 'error':
        msg = record.error_info
    elif info_type == 'fail':
        msg = record.fail_info
    else:
        msg = "wrong type"
    return response_msg(msg)

def get_build_console(req):
    try:
        param = req.GET or req.POST
        job_name = param.get('job_name', None)
        bn = int(param.get('build_no', None))
        build_log = JenkinsJob(job_name).get_console(bn)
        return response_msg(build_log)
    except (TypeError, ValueError):
        return response_msg('build_no needed and must be int!')
    except KeyError as e:
        return response_msg(e.args)
    except Exception as e:
        logger.error("Get Console Error:", exc_info=True)
        return response_msg(e.args)

def get_push_uid(req):
    uids = data_runners.push_uid_list or []
    uidset = set(uids)
    return response_msg({"uid_sample": uids[0:10], "uid_total": len(uidset)})

def start_push(req):
    try:
        from acinter import interface
        from random import shuffle
        ac = interface.acsim()
        LBS_IP = CommonConfig.objects.get(pk=3).value
        LBS_PORT = int(CommonConfig.objects.get(pk=4).value)
        ac.connect_italk(lbs_ip=LBS_IP, lbs_port=LBS_PORT)
        ac.login(Account=4444)
        ac.login_complete()
        msg_id = int(req.GET.get('msg_id', None))
        offline_num = int(req.GET.get('offline', 0))
        step = int(req.GET.get('step', 1000))
        target_uid = data_runners.push_uid_list or []
        random_uid = list(range(1, offline_num))
        target_uid_num = len(target_uid)
        total_uid_list = target_uid + random_uid
        shuffle(total_uid_list)
        message = {'MsgId': msg_id, 'online': target_uid_num, 'offline': offline_num, 'batch_step': step}
        for batch_seq in slice_seq(total_uid_list, step):
            result = ac.push_message(MsgID=msg_id, TargetUIDNum=step, TargetUIDs=batch_seq, timeout=600)
            if result.get('RspCode', -1) == 0:
                message['pushed_num'] = message.setdefault('pushed_num', 0) + step
            else:
                return response_msg(result)
        return response_msg(message)
    except ValueError as e:
        return response_msg("Invalid param: %s" % str(e.args).split(':')[1])
    except TypeError:
        return response_msg('msg_id is required!')
    except Exception as e:
        logger.error('Push Error', exc_info=True)
        return response_msg(e.args)
    finally:
        ac.disconnect_italk()
        # data_runners.push_uid_list = None

