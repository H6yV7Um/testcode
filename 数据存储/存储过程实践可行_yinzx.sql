drop procedure if exists pr_stu -- 删除存储过程
drop table stu_info

CREATE TABLE `stu_info` (     -- 创建表，反引号用来区别mysql中的关键字，以防重复，报错
  `sid` int(10) NOT NULL AUTO_INCREMENT COMMENT '学生编号',
  `class` varchar(50) DEFAULT NULL COMMENT '班级',
  `age` int(11) NOT NULL COMMENT '年龄',
  `sex` varchar(10) NOT NULL COMMENT '性别',
  `hometown` varchar(50) DEFAULT NULL COMMENT '家乡',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `content` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`sid`),
  UNIQUE KEY `unique_sid` (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=1000000101 DEFAULT CHARSET=utf8;

DELIMITER $$ -- 重新定义执行分隔符，针对命令行模式中执行时有用,sql脚本中不定义也可以
CREATE PROCEDURE pr_stu() -- 创建存储过程
  BEGIN
    DECLARE _sid int(12);
    DECLARE _class varchar(50);
    DECLARE _age int(11);
    DECLARE _sex varchar(10);
    DECLARE _hometown varchar(50);
    DECLARE _create_time datetime;
    DECLARE _update_time datetime;
    DECLARE _content varchar(255);
    DECLARE total int;
    DECLARE num int;
  
    set total=100;  -- 定义插入数据总数
    set num=1;  -- 计数器初始值
    set _sid=1000000100;
  
    while num<=total do
      set _sid=_sid+1;
      set _class='大三';
      set _age=floor(rand()*100);
      set _sex='男';
      set _hometown=concat(round(rand()*1000),'河北省张家口市崇礼县');
      set _create_time=current_date();
      set _update_time=current_date();
      set _content=round(rand()*100000);
    
      insert into stu_info (`sid`,`class`,`age`,`sex`,`hometown`,`create_time`,`update_time`,`content`) 
      values 
      (_sid,_class,_age,_sex,_hometown,_create_time,_update_time,_content);
    
      set num=num+1;
    END while;
  END $$
DELIMITER;

grant execute on test.* to yunwei@'%';flush privileges;  -- 调用存储过程提示权限问题时执行该两条语句解决

call pr_stu;  -- 调用存储过程

truncate stu_info;
select * from stu_info

rollback()



