CREATE TABLE `word_filter` (
  `filter_id` int(5) NOT NULL AUTO_INCREMENT COMMENT '敏感词ID',
  `content` varchar(1024) DEFAULT NULL COMMENT '内容',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `create_user` varchar(10) NOT NULL COMMENT '创建工号',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `update_user` varchar(10) NOT NULL COMMENT '更新工号',
  PRIMARY KEY (`filter_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='仅供测试';

drop table word_filter

CREATE TABLE `item_today`(
`ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'ID',
`ITEM_NAME` varchar(1024) DEFAULT NULL COMMENT '拍品名称',
`ITEM_DESC` varchar(1024) DEFAULT NULL COMMENT '拍品描述',
`ITEM_LINK` varchar(1024) DEFAULT NULL COMMENT '拍品链接',
`CREATE_TIME` datetime DEFAULT NULL COMMENT '创建时间',
PRIMARY KEY (`ID`)
)  ENGINE=MyISAM AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8 COMMENT='今日拍品表'

CREATE TABLE `item_tommorrow`(
`ID` int(6) NOT NULL AUTO_INCREMENT COMMENT 'ID',
`ITEM_NAME` varchar(1024) DEFAULT NULL COMMENT '拍品名称',
`ITEM_DESC` varchar(1024) DEFAULT NULL COMMENT '拍品描述',
`ITEM_LINK` varchar(1024) DEFAULT NULL COMMENT '拍品链接',
`CREATE_TIME` datetime DEFAULT NULL COMMENT '创建时间',
PRIMARY KEY (`ID`)
)  ENGINE=MyISAM AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8 COMMENT='明日拍品表'

insert into item_today (ITEM_NAME,ITEM_DESC,ITEM_LINK) values('你好','buhao','http://baidu.com')
select * from item_today
select * from item_tommorrow

