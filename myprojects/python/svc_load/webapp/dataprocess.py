#coding: utf-8
import sys
import json
import xml.etree.ElementTree as ET

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

from django.conf import settings
from django.db import connections
from django.http import HttpResponse
from utils import DictObj, CJsonEncoder, curtime


class FormatRequest(object):
    """处理request，格式化为插库时需要的格式"""
    def __init__(self):
        super(FormatRequest, self).__init__()

    # @classmethod
    def check_data(self, req):
        '''func doc'''
        data = DictObj(**req.POST.dict())
        if data.id:
            data.modify_time = curtime()
        else:
            data.create_time = curtime()
        # data.operate_ip = req.META['HTTP_X_REAL_IP']
        return data

    @classmethod
    def format_for_query(cls, req):
        '''func doc'''
        pass

    @classmethod
    def format_for_delete(cls, req):
        data = DictObj(**req.POST.dict())
        ids_list = [int(client_id) for client_id in data.id.split(',')]
        return ids_list

    @classmethod
    def format_for_insert(cls, req):
        '''将请求数据转化为{"tkey":[],"tvalue":"","tstr":""}形式'''
        res_dict = DictObj()
        req_post = cls().check_data(req)
        if isinstance(req_post, dict):
            tkey = []
            tvalue = ""
            nlist = []
            for key, value in req_post.items():
                key_str = '`%s`' % key
                value_str = '"%s",' % value
                tkey.append(key_str)
                tvalue += value_str
                if key != 'id':
                    equal_str = '`%s`="%s" ' % (key, value)
                    nlist.append(equal_str)
            tstr = ",".join(nlist)
            tkey_str = ",".join(tkey)
            tvalue = tvalue[:-1]
            res_dict.tkey = '(' + tkey_str + ')'
            res_dict.tvalue = '(' + tvalue + ')'
            res_dict.tstring = tstr
            return res_dict
        else:
            raise TypeError("param is not a dict!")


class DBConnection(object):
    """django db api """
    def __init__(self, db='test'):
        super(DBConnection, self).__init__()
        self.cursor = connections[db].cursor()

    def query(self, sql, *args):
        '''通用查询，可选关键字参数用于格式化sql'''
        #sql = sql.format(kwargs) if kwargs else sql
        self.cursor.execute(sql, args)
        db_data = DataTransform.dictfetchall(self.cursor)
        return db_data

    def insert(self, sql, **kwargs):
        """content涉及中文，占位符要加且必须双引号，否则报数据库错误"""
        sql = sql.format(kwargs)
        num = self.cursor.execute(sql)
        return num > 0

    def delete(self, sql, *args):
        '''func doc'''
        effected_num = 0
        for client_id in args:
            num = self.cursor.execute(sql, [client_id])
            effected_num += num
        return effected_num == len(args)


class DataTransform(object):
    """定义了处理cursor返回数据的处理方式"""
    def __init__(self):
        super(DataTranform, self).__init__()

    @classmethod
    def dictfetchall(cls,cursor):
        '''将cursor查询到的每行数据作为dict元素包含在list中返回'''
        columns = [col[0] for col in cursor.description]
        data = [DictObj(columns, row) for row in cursor.fetchall()]
        return data

    @classmethod
    def namedtuplefetchall(cls,cursor):
        '''将cursor查询到的所有数据作为namedtuple返回'''
        desc = cursor.description   #返回sql中查询的列信息的list
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]


def handle_upload_file(req):
    """return the file path on server"""
    import uuid
    import os
    filepath = ""
    if req.FILES:
        f = req.FILES['file']
        filename = '{0}.jpg'.format(uuid.uuid4())
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        filepath = os.path.abspath(filename)
    return filepath


def response_msg(data):
    """返回状态信息1：成功，0：失败，dict：返回json"""
    if data == 1:
        ret_dict = {"status": 1, "msg":"success!"}
    elif data == 0:
        ret_dict = {"status": 0, "msg":"fail,please try it later!"}
    elif data == 2:
        ret_dict = {"status": 2, "msg": "Internal Error!Please contact the administrator!"}
    elif data == 3:
        ret_dict = {"status": 3, "msg": "user not login"}
    elif isinstance(data, (dict, list)):
        ret_dict = {"status":1, "data": data}
    else:
        ret_dict = {"status": 0,"msg": data}
    ret_data = json.dumps(ret_dict, cls=CJsonEncoder)
    response = HttpResponse(ret_data)
    response['Access-Control-Allow-Origin'] = '*'
    return response


class InvalidParam(Exception):
    pass

def make_struct(req):
    struct = {"test_scene": {}, "data_struct": {'total': 0, 'detail': {}}}
    class_type = req.POST.getlist('class_type')
    class_count = req.POST.getlist('class_count')
    user_count = req.POST.getlist('user_count')
    teacher_scene = [int(i) for i in req.POST.getlist('teacher_scene')]
    student_scene = [int(i) for i in req.POST.getlist('student_scene')]
    include_static_stu = req.POST.get("include_static_stu", False)
    is_random = req.POST.get("is_random", False)
    is_push = req.POST.get('is_push', False)
    if not all([class_type, class_count, user_count, teacher_scene, student_scene]):
        raise InvalidParam("Invalid params!")
    if is_push:
        teacher_scene.append(18)
        student_scene.append(18)
    struct["test_scene"]["teacher_scene"] = teacher_scene
    struct["test_scene"]["student_scene"] = student_scene
    struct["include_static_stu"] = include_static_stu
    struct["is_random"] = is_random
    total = sum(map(lambda t: int(t[0])*int(t[1]), zip(class_count, user_count)))
    struct["data_struct"]['total'] = total
    for i in range(len(class_type)):
        temp = {int(class_type[i]): (int(class_count[i]), int(user_count[i]))}
        struct["data_struct"]['detail'].update(temp)
    return struct

class InvalidJobError(Exception):
    pass

class JenkinsJob:
    '''class doc'''
    def __init__(self, job_name):
        self.info = settings.JENKINS_INFO
        self.cr = CrumbRequester(**self.info)
        self.jclient = Jenkins(requester=self.cr, **self.info)
        if not self.jclient.has_job(job_name):
            raise InvalidJobError('No job named {}'.format(job_name))
        self.job =self.jclient.get_job(job_name)

    def start_build(self, ms):
        if self.job.is_running():
            return False
        self.update_mail_switch(ms)
        self.job.invoke()
        return True

    def stop_build(self, build_no):
        build =self. job.get_build(build_no)
        if build.is_running():
            build.stop()

    def get_console(self, build_no):
        build =self. job.get_build(build_no)
        return build.get_console()

    def update_mail_switch(self, ms):
        '''turn on/off mail switch
          @param: switch should be true or false
        '''
        job_config = self.job._get_config_element_tree()
        for email_publisher in job_config.iter('hudson.plugins.emailext.ExtendedEmailPublisher'):
            switch = email_publisher.find('disabled')
            if switch.text == ms:
                return
            switch.text = ms
        #升级到python3后tostring返回的是bytes需要转换为string
        new_config_str = ET.tostring(job_config).decode()
        self.job.update_config(new_config_str)