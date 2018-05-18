#coding:utf-8
__doc__ = '''config file '''


URL = "http://test.com"

def reqData(kwargs):
  DATA = {
    "username": "test",
    "indexKey": kwargs['indexkey'],
    "datas": '''[
      {"INDEX_TIME": %s, 
      "INDEX_VALUE": %s
    ]''' % (kwargs['indextime'],kwargs['indexvalue'])
  }
  return DATA

KeyMap = {
  "core_num": "LS000030",
  "core_rate": "LS000033",
  "full_num": "DD000002",
  "full_rate": "LS000032"
}

DB = {
  'host': 'test',
  'port': 7302,
  'user': 'test',
  'passwd': 'test',
  'db': 'dispatch',
  'charset': 'utf8',
  'connect_timeout': 5
}


FULL_DELAY_SQL = '''
  SELECT count(*) 
  FROM `t_dispatch_job` as job join t_dispatch_job_logs as log 
  on job.id=log.job_id 
  WHERE 
  log.day_key={0} 
  and log.late_finish_time is not null 
  and (FROM_UNIXTIME(log.end_time/1000,'%Y-%m-%d %H:%i:%S')> log.late_finish_time or log.end_time is null)
'''
CORE_DELAY_SQL = '''
  SELECT count(*) 
  FROM `t_dispatch_job` as job join t_dispatch_job_logs as log 
  on job.id=log.job_id 
  WHERE 
  log.day_key={0} 
  and log.late_finish_time is not null 
  and  (FROM_UNIXTIME(log.end_time/1000,'%Y-%m-%d %H:%i:%S')> log.late_finish_time or log.end_time is null) 
  and job.id in(101,201,344,72,73,74,75,106,315,353,370,453,454,455,457,341,117,80,58,224,225,226,227,163,132,115,140,145,146,147,248,249,279,82,76,265,178,158,144,200,142,306)
'''
FULL_DELAY_RATE_SQL = '''
  SELECT 
  (SELECT count(*) 
    FROM `t_dispatch_job` as job join t_dispatch_job_logs as log 
    on job.id=log.job_id 
    WHERE log.day_key={0} and log.late_finish_time is not null
    and  (FROM_UNIXTIME(log.end_time/1000,'%Y-%m-%d %H:%i:%S')> log.late_finish_time or log.end_time is null))
    /(select count(*) from t_dispatch_job_logs where late_finish_time is not null 
  and day_key={0})
'''
CORE_DELAY_RATE_SQL = '''
SELECT 
  (SELECT count(*) FROM `t_dispatch_job` as job join t_dispatch_job_logs as log on job.id=log.job_id 
  WHERE log.day_key={0}
  AND log.late_finish_time is not null
  AND  (FROM_UNIXTIME(log.end_time/1000,'%Y-%m-%d %H:%i:%S')> log.late_finish_time or log.end_time is null) 
  AND job.id in(101,201,344,72,73,74,75,106,315,353,370,453,454,455,457,341,117,80,58,224,225,226,227,163,132,115,140,145,146,147,248,249,279,82,76,265,178,158,144,200,142,306))
/(SELECT 
  count(*) from t_dispatch_job_logs 
  WHERE late_finish_time is not null 
  AND day_key={0}
  AND job_id in(101,201,344,72,73,74,75,106,315,353,370,453,454,455,457,341,117,80,58,224,225,226,227,163,132,115,140,145,146,147,248,249,279,82,76,265,178,158,144,200,142,306))
'''
CORE_DELAY_NAME_SQL = '''
SELECT job.job_name 
FROM `t_dispatch_job` as job join t_dispatch_job_logs as log 
on job.id=log.job_id 
WHERE log.day_key={0} 
AND log.late_finish_time is not null 
AND  (FROM_UNIXTIME(log.end_time/1000,'%Y-%m-%d %H:%i:%S')> log.late_finish_time or log.end_time is null) 
AND job.id in(101,201,344,72,73,74,75,106,315,353,370,453,454,455,457,341,117,80,58,224,225,226,227,163,132,115,140,145,146,147,248,249,279,82,76,265,178,158,144,200,142,306)
'''
