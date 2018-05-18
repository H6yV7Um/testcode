/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.1.73 : Database - superman
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`superman` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `superman`;

/*Table structure for table `QRTZ_BLOB_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_BLOB_TRIGGERS`;

CREATE TABLE `QRTZ_BLOB_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `BLOB_DATA` blob,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  KEY `SCHED_NAME` (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  CONSTRAINT `QRTZ_BLOB_TRIGGERS_ibfk_1` FOREIGN KEY (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`) REFERENCES `QRTZ_TRIGGERS` (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_BLOB_TRIGGERS` */

/*Table structure for table `QRTZ_CALENDARS` */

DROP TABLE IF EXISTS `QRTZ_CALENDARS`;

CREATE TABLE `QRTZ_CALENDARS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `CALENDAR_NAME` varchar(200) NOT NULL,
  `CALENDAR` blob NOT NULL,
  PRIMARY KEY (`SCHED_NAME`,`CALENDAR_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_CALENDARS` */

/*Table structure for table `QRTZ_CRON_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_CRON_TRIGGERS`;

CREATE TABLE `QRTZ_CRON_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `CRON_EXPRESSION` varchar(120) NOT NULL,
  `TIME_ZONE_ID` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  CONSTRAINT `QRTZ_CRON_TRIGGERS_ibfk_1` FOREIGN KEY (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`) REFERENCES `QRTZ_TRIGGERS` (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_CRON_TRIGGERS` */

insert  into `QRTZ_CRON_TRIGGERS`(`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`,`CRON_EXPRESSION`,`TIME_ZONE_ID`) values ('RenrenScheduler','TASK_1','DEFAULT','0 0/30 * * * ?','Asia/Shanghai'),('RenrenScheduler','TASK_2','DEFAULT','0 0/30 * * * ?','Asia/Shanghai');

/*Table structure for table `QRTZ_FIRED_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_FIRED_TRIGGERS`;

CREATE TABLE `QRTZ_FIRED_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `ENTRY_ID` varchar(95) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `INSTANCE_NAME` varchar(200) NOT NULL,
  `FIRED_TIME` bigint(13) NOT NULL,
  `SCHED_TIME` bigint(13) NOT NULL,
  `PRIORITY` int(11) NOT NULL,
  `STATE` varchar(16) NOT NULL,
  `JOB_NAME` varchar(200) DEFAULT NULL,
  `JOB_GROUP` varchar(200) DEFAULT NULL,
  `IS_NONCONCURRENT` varchar(1) DEFAULT NULL,
  `REQUESTS_RECOVERY` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`SCHED_NAME`,`ENTRY_ID`),
  KEY `IDX_QRTZ_FT_TRIG_INST_NAME` (`SCHED_NAME`,`INSTANCE_NAME`),
  KEY `IDX_QRTZ_FT_INST_JOB_REQ_RCVRY` (`SCHED_NAME`,`INSTANCE_NAME`,`REQUESTS_RECOVERY`),
  KEY `IDX_QRTZ_FT_J_G` (`SCHED_NAME`,`JOB_NAME`,`JOB_GROUP`),
  KEY `IDX_QRTZ_FT_JG` (`SCHED_NAME`,`JOB_GROUP`),
  KEY `IDX_QRTZ_FT_T_G` (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  KEY `IDX_QRTZ_FT_TG` (`SCHED_NAME`,`TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_FIRED_TRIGGERS` */

/*Table structure for table `QRTZ_JOB_DETAILS` */

DROP TABLE IF EXISTS `QRTZ_JOB_DETAILS`;

CREATE TABLE `QRTZ_JOB_DETAILS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `JOB_NAME` varchar(200) NOT NULL,
  `JOB_GROUP` varchar(200) NOT NULL,
  `DESCRIPTION` varchar(250) DEFAULT NULL,
  `JOB_CLASS_NAME` varchar(250) NOT NULL,
  `IS_DURABLE` varchar(1) NOT NULL,
  `IS_NONCONCURRENT` varchar(1) NOT NULL,
  `IS_UPDATE_DATA` varchar(1) NOT NULL,
  `REQUESTS_RECOVERY` varchar(1) NOT NULL,
  `JOB_DATA` blob,
  PRIMARY KEY (`SCHED_NAME`,`JOB_NAME`,`JOB_GROUP`),
  KEY `IDX_QRTZ_J_REQ_RECOVERY` (`SCHED_NAME`,`REQUESTS_RECOVERY`),
  KEY `IDX_QRTZ_J_GRP` (`SCHED_NAME`,`JOB_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_JOB_DETAILS` */

insert  into `QRTZ_JOB_DETAILS`(`SCHED_NAME`,`JOB_NAME`,`JOB_GROUP`,`DESCRIPTION`,`JOB_CLASS_NAME`,`IS_DURABLE`,`IS_NONCONCURRENT`,`IS_UPDATE_DATA`,`REQUESTS_RECOVERY`,`JOB_DATA`) values ('RenrenScheduler','TASK_1','DEFAULT',NULL,'com.vdcoding.modules.job.utils.ScheduleJob','0','0','0','0','��\0sr\0org.quartz.JobDataMap���迩��\0\0xr\0&org.quartz.utils.StringKeyDirtyFlagMap�����](\0Z\0allowsTransientDataxr\0org.quartz.utils.DirtyFlagMap�.�(v\n�\0Z\0dirtyL\0mapt\0Ljava/util/Map;xpsr\0java.util.HashMap���`�\0F\0\nloadFactorI\0	thresholdxp?@\0\0\0\0\0w\0\0\0\0\0\0t\0\rJOB_PARAM_KEYt\0�{\"jobId\":1,\"beanName\":\"testTask\",\"methodName\":\"test\",\"params\":\"renren\",\"cronExpression\":\"0 0/30 * * * ?\",\"status\":0,\"remark\":\"有参数测试\",\"createTime\":\"Dec 1, 2016 11:16:46 PM\"}x\0'),('RenrenScheduler','TASK_2','DEFAULT',NULL,'com.vdcoding.modules.job.utils.ScheduleJob','0','0','0','0','��\0sr\0org.quartz.JobDataMap���迩��\0\0xr\0&org.quartz.utils.StringKeyDirtyFlagMap�����](\0Z\0allowsTransientDataxr\0org.quartz.utils.DirtyFlagMap�.�(v\n�\0Z\0dirtyL\0mapt\0Ljava/util/Map;xpsr\0java.util.HashMap���`�\0F\0\nloadFactorI\0	thresholdxp?@\0\0\0\0\0w\0\0\0\0\0\0t\0\rJOB_PARAM_KEYt\0�{\"jobId\":2,\"beanName\":\"testTask\",\"methodName\":\"test2\",\"cronExpression\":\"0 0/30 * * * ?\",\"status\":1,\"remark\":\"无参数测试\",\"createTime\":\"Dec 3, 2016 2:55:56 PM\"}x\0');

/*Table structure for table `QRTZ_LOCKS` */

DROP TABLE IF EXISTS `QRTZ_LOCKS`;

CREATE TABLE `QRTZ_LOCKS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `LOCK_NAME` varchar(40) NOT NULL,
  PRIMARY KEY (`SCHED_NAME`,`LOCK_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_LOCKS` */

insert  into `QRTZ_LOCKS`(`SCHED_NAME`,`LOCK_NAME`) values ('RenrenScheduler','STATE_ACCESS'),('RenrenScheduler','TRIGGER_ACCESS');

/*Table structure for table `QRTZ_PAUSED_TRIGGER_GRPS` */

DROP TABLE IF EXISTS `QRTZ_PAUSED_TRIGGER_GRPS`;

CREATE TABLE `QRTZ_PAUSED_TRIGGER_GRPS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_PAUSED_TRIGGER_GRPS` */

/*Table structure for table `QRTZ_SCHEDULER_STATE` */

DROP TABLE IF EXISTS `QRTZ_SCHEDULER_STATE`;

CREATE TABLE `QRTZ_SCHEDULER_STATE` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `INSTANCE_NAME` varchar(200) NOT NULL,
  `LAST_CHECKIN_TIME` bigint(13) NOT NULL,
  `CHECKIN_INTERVAL` bigint(13) NOT NULL,
  PRIMARY KEY (`SCHED_NAME`,`INSTANCE_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_SCHEDULER_STATE` */

insert  into `QRTZ_SCHEDULER_STATE`(`SCHED_NAME`,`INSTANCE_NAME`,`LAST_CHECKIN_TIME`,`CHECKIN_INTERVAL`) values ('RenrenScheduler','HelloWorld1526482331377',1526482725113,15000);

/*Table structure for table `QRTZ_SIMPLE_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_SIMPLE_TRIGGERS`;

CREATE TABLE `QRTZ_SIMPLE_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `REPEAT_COUNT` bigint(7) NOT NULL,
  `REPEAT_INTERVAL` bigint(12) NOT NULL,
  `TIMES_TRIGGERED` bigint(10) NOT NULL,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  CONSTRAINT `QRTZ_SIMPLE_TRIGGERS_ibfk_1` FOREIGN KEY (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`) REFERENCES `QRTZ_TRIGGERS` (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_SIMPLE_TRIGGERS` */

/*Table structure for table `QRTZ_SIMPROP_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_SIMPROP_TRIGGERS`;

CREATE TABLE `QRTZ_SIMPROP_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `STR_PROP_1` varchar(512) DEFAULT NULL,
  `STR_PROP_2` varchar(512) DEFAULT NULL,
  `STR_PROP_3` varchar(512) DEFAULT NULL,
  `INT_PROP_1` int(11) DEFAULT NULL,
  `INT_PROP_2` int(11) DEFAULT NULL,
  `LONG_PROP_1` bigint(20) DEFAULT NULL,
  `LONG_PROP_2` bigint(20) DEFAULT NULL,
  `DEC_PROP_1` decimal(13,4) DEFAULT NULL,
  `DEC_PROP_2` decimal(13,4) DEFAULT NULL,
  `BOOL_PROP_1` varchar(1) DEFAULT NULL,
  `BOOL_PROP_2` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  CONSTRAINT `QRTZ_SIMPROP_TRIGGERS_ibfk_1` FOREIGN KEY (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`) REFERENCES `QRTZ_TRIGGERS` (`SCHED_NAME`, `TRIGGER_NAME`, `TRIGGER_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_SIMPROP_TRIGGERS` */

/*Table structure for table `QRTZ_TRIGGERS` */

DROP TABLE IF EXISTS `QRTZ_TRIGGERS`;

CREATE TABLE `QRTZ_TRIGGERS` (
  `SCHED_NAME` varchar(120) NOT NULL,
  `TRIGGER_NAME` varchar(200) NOT NULL,
  `TRIGGER_GROUP` varchar(200) NOT NULL,
  `JOB_NAME` varchar(200) NOT NULL,
  `JOB_GROUP` varchar(200) NOT NULL,
  `DESCRIPTION` varchar(250) DEFAULT NULL,
  `NEXT_FIRE_TIME` bigint(13) DEFAULT NULL,
  `PREV_FIRE_TIME` bigint(13) DEFAULT NULL,
  `PRIORITY` int(11) DEFAULT NULL,
  `TRIGGER_STATE` varchar(16) NOT NULL,
  `TRIGGER_TYPE` varchar(8) NOT NULL,
  `START_TIME` bigint(13) NOT NULL,
  `END_TIME` bigint(13) DEFAULT NULL,
  `CALENDAR_NAME` varchar(200) DEFAULT NULL,
  `MISFIRE_INSTR` smallint(2) DEFAULT NULL,
  `JOB_DATA` blob,
  PRIMARY KEY (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`),
  KEY `IDX_QRTZ_T_J` (`SCHED_NAME`,`JOB_NAME`,`JOB_GROUP`),
  KEY `IDX_QRTZ_T_JG` (`SCHED_NAME`,`JOB_GROUP`),
  KEY `IDX_QRTZ_T_C` (`SCHED_NAME`,`CALENDAR_NAME`),
  KEY `IDX_QRTZ_T_G` (`SCHED_NAME`,`TRIGGER_GROUP`),
  KEY `IDX_QRTZ_T_STATE` (`SCHED_NAME`,`TRIGGER_STATE`),
  KEY `IDX_QRTZ_T_N_STATE` (`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`,`TRIGGER_STATE`),
  KEY `IDX_QRTZ_T_N_G_STATE` (`SCHED_NAME`,`TRIGGER_GROUP`,`TRIGGER_STATE`),
  KEY `IDX_QRTZ_T_NEXT_FIRE_TIME` (`SCHED_NAME`,`NEXT_FIRE_TIME`),
  KEY `IDX_QRTZ_T_NFT_ST` (`SCHED_NAME`,`TRIGGER_STATE`,`NEXT_FIRE_TIME`),
  KEY `IDX_QRTZ_T_NFT_MISFIRE` (`SCHED_NAME`,`MISFIRE_INSTR`,`NEXT_FIRE_TIME`),
  KEY `IDX_QRTZ_T_NFT_ST_MISFIRE` (`SCHED_NAME`,`MISFIRE_INSTR`,`NEXT_FIRE_TIME`,`TRIGGER_STATE`),
  KEY `IDX_QRTZ_T_NFT_ST_MISFIRE_GRP` (`SCHED_NAME`,`MISFIRE_INSTR`,`NEXT_FIRE_TIME`,`TRIGGER_GROUP`,`TRIGGER_STATE`),
  CONSTRAINT `QRTZ_TRIGGERS_ibfk_1` FOREIGN KEY (`SCHED_NAME`, `JOB_NAME`, `JOB_GROUP`) REFERENCES `QRTZ_JOB_DETAILS` (`SCHED_NAME`, `JOB_NAME`, `JOB_GROUP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `QRTZ_TRIGGERS` */

insert  into `QRTZ_TRIGGERS`(`SCHED_NAME`,`TRIGGER_NAME`,`TRIGGER_GROUP`,`JOB_NAME`,`JOB_GROUP`,`DESCRIPTION`,`NEXT_FIRE_TIME`,`PREV_FIRE_TIME`,`PRIORITY`,`TRIGGER_STATE`,`TRIGGER_TYPE`,`START_TIME`,`END_TIME`,`CALENDAR_NAME`,`MISFIRE_INSTR`,`JOB_DATA`) values ('RenrenScheduler','TASK_1','DEFAULT','TASK_1','DEFAULT',NULL,1526482800000,-1,5,'WAITING','CRON',1525416366000,0,NULL,2,'��\0sr\0org.quartz.JobDataMap���迩��\0\0xr\0&org.quartz.utils.StringKeyDirtyFlagMap�����](\0Z\0allowsTransientDataxr\0org.quartz.utils.DirtyFlagMap�.�(v\n�\0Z\0dirtyL\0mapt\0Ljava/util/Map;xpsr\0java.util.HashMap���`�\0F\0\nloadFactorI\0	thresholdxp?@\0\0\0\0\0w\0\0\0\0\0\0t\0\rJOB_PARAM_KEYt\0�{\"jobId\":1,\"beanName\":\"testTask\",\"methodName\":\"test\",\"params\":\"renren\",\"cronExpression\":\"0 0/30 * * * ?\",\"status\":0,\"remark\":\"有参数测试\",\"createTime\":\"Dec 1, 2016 11:16:46 PM\"}x\0'),('RenrenScheduler','TASK_2','DEFAULT','TASK_2','DEFAULT',NULL,1525417200000,-1,5,'PAUSED','CRON',1525416366000,0,NULL,2,'��\0sr\0org.quartz.JobDataMap���迩��\0\0xr\0&org.quartz.utils.StringKeyDirtyFlagMap�����](\0Z\0allowsTransientDataxr\0org.quartz.utils.DirtyFlagMap�.�(v\n�\0Z\0dirtyL\0mapt\0Ljava/util/Map;xpsr\0java.util.HashMap���`�\0F\0\nloadFactorI\0	thresholdxp?@\0\0\0\0\0w\0\0\0\0\0\0t\0\rJOB_PARAM_KEYt\0�{\"jobId\":2,\"beanName\":\"testTask\",\"methodName\":\"test2\",\"cronExpression\":\"0 0/30 * * * ?\",\"status\":1,\"remark\":\"无参数测试\",\"createTime\":\"Dec 3, 2016 2:55:56 PM\"}x\0');

/*Table structure for table `app_category` */

DROP TABLE IF EXISTS `app_category`;

CREATE TABLE `app_category` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `shop_id` int(4) NOT NULL,
  `seq` int(2) NOT NULL,
  `type` enum('RECOMMEND','CUSTOM') COLLATE utf8_unicode_ci NOT NULL,
  `is_show` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_category` */

insert  into `app_category`(`id`,`name`,`shop_id`,`seq`,`type`,`is_show`) values (1,'推荐',3,1,'RECOMMEND',1),(2,'白酒',3,2,'CUSTOM',1),(3,'啤酒',3,3,'CUSTOM',1),(4,'葡萄酒',3,4,'CUSTOM',1),(5,'洋酒',3,5,'CUSTOM',1);

/*Table structure for table `app_comment` */

DROP TABLE IF EXISTS `app_comment`;

CREATE TABLE `app_comment` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `order_id` int(32) NOT NULL,
  `customer_id` int(32) NOT NULL,
  `shop_id` int(8) NOT NULL DEFAULT '0',
  `goods_id` int(32) NOT NULL,
  `star` tinyint(2) NOT NULL,
  `comment` text COLLATE utf8_unicode_ci,
  `images` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_comment` */

insert  into `app_comment`(`id`,`order_id`,`customer_id`,`shop_id`,`goods_id`,`star`,`comment`,`images`,`create_time`,`update_time`) values (1,10000001,1000000,0,1,5,'HelloWorld绝对好',NULL,'2018-04-23 11:02:42','2018-04-23 11:14:42'),(2,10000001,1000001,0,1,3,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-05-10 11:16:42'),(3,10000001,1000002,0,1,4,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-05-10 11:16:45'),(4,10000001,1000003,0,1,2,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-05-10 11:16:48'),(5,10000001,1000004,0,1,1,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-05-10 11:16:50'),(6,10000001,1000004,0,100000,3,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-05-10 20:54:08');

/*Table structure for table `app_component_data` */

DROP TABLE IF EXISTS `app_component_data`;

CREATE TABLE `app_component_data` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `component_id` int(4) DEFAULT NULL,
  `target_id` int(4) DEFAULT NULL,
  `seq` int(2) NOT NULL,
  `title` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `action` enum('FAVORITE','ADDRESS','COUPON_OWN','COUPON_PICK','MEMBER_BONUS','MEMBER_DETAIL','MEMBER_CODE','MEMBER_SIGN','GOODS_ALL','CONTACT','PHONE','SHARE','SHOP_INFO','COMMENT_LIST','GOODS_SEARCH','MEMBER_REGIST','CATEGORY','NONE') COLLATE utf8_unicode_ci DEFAULT 'NONE',
  `url` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `icon_class` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `icon_color` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `icon_size` varchar(16) COLLATE utf8_unicode_ci DEFAULT '24px',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_component_data` */

insert  into `app_component_data`(`id`,`component_id`,`target_id`,`seq`,`title`,`action`,`url`,`icon_class`,`icon_color`,`icon_size`) values (1,2,1,1,NULL,'GOODS_SEARCH','http://img.zcool.cn/community/0190e259eeb56ca801216a4bcec4bf.jpg@640w_1l_2o_100sh.jpg',NULL,NULL,NULL),(2,2,2,2,NULL,'GOODS_SEARCH','http://img.zcool.cn/community/01bbc65a1fd1aea8012171329beb05.jpg@640w_1l_2o_100sh.webp',NULL,NULL,NULL),(3,2,3,3,NULL,'GOODS_SEARCH','http://img.zcool.cn/community/013a6a5a1fd1aca80120908de888db.jpg@640w_1l_2o_100sh.webp',NULL,NULL,NULL),(4,4,NULL,1,'分类购买','GOODS_ALL','http://img.leshare.shop/shop/3/btn1.png',NULL,NULL,NULL),(5,4,NULL,2,'注册会员','MEMBER_REGIST','http://img.leshare.shop/shop/3/btn2.png',NULL,NULL,NULL),(6,4,NULL,4,'好友分享','SHARE','http://img.leshare.shop/shop/3/btn4.png',NULL,NULL,NULL),(7,4,NULL,3,'联系我们','PHONE','http://img.leshare.shop/shop/3/btn3.png',NULL,NULL,NULL),(8,6,NULL,1,NULL,'NONE','http://pic.58pic.com/58pic/15/03/41/39X58PICDgC_1024.jpg',NULL,NULL,NULL),(9,7,NULL,1,'白酒','CATEGORY','http://img13.360buyimg.com/focus/jfs/t12829/319/1332490773/11660/b2ed197/5a1eb2eeN1b625ed6.jpg',NULL,NULL,NULL),(10,7,NULL,2,'啤酒','CATEGORY','http://img12.360buyimg.com/focus/jfs/t14650/46/248971120/11222/8bec926c/5a27c364N1bb537d9.jpg',NULL,NULL,NULL),(11,7,NULL,3,'葡萄酒','CATEGORY','http://img30.360buyimg.com/focus/jfs/t15253/106/252084226/4063/4adcc3fb/5a27c37bNa669ff29.jpg',NULL,NULL,NULL),(12,7,NULL,4,'黄酒/养生酒','CATEGORY','http://img14.360buyimg.com/focus/jfs/t13132/236/1734048263/12205/f167c0ea/5a27c36eN6549ac45.jpg',NULL,NULL,NULL),(13,7,NULL,5,'洋酒','CATEGORY','http://img20.360buyimg.com/focus/jfs/t13339/271/1323514062/3093/29ede56/5a1eb2eaN1fcbec0f.jpg',NULL,NULL,NULL),(14,15,NULL,1,'我的收藏','FAVORITE','','like','#f85','24px'),(15,15,NULL,2,'常用地址','ADDRESS','','address','#1296DB','24px'),(16,15,NULL,3,'我的优惠券','COUPON_OWN','','coupon','#e33','24px'),(17,15,NULL,4,'领取优惠券','COUPON_PICK','','receive-coupons','#008000','24px'),(18,15,NULL,5,'积分中心','MEMBER_BONUS','','bouns','#1296DB','24px'),(19,15,NULL,6,'店铺信息','SHOP_INFO','','address','#1296DB','24px'),(20,15,NULL,7,'电话咨询','PHONE','','call','#e33','24px'),(21,15,NULL,8,'我的评论','COMMENT_LIST','','chat','#e33','24px'),(22,2,1,4,NULL,'GOODS_SEARCH','http://img.sccnn.com/bimg/339/18050.jpg',NULL,NULL,'24px');

/*Table structure for table `app_component_target` */

DROP TABLE IF EXISTS `app_component_target`;

CREATE TABLE `app_component_target` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `content` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `category_id` int(4) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_component_target` */

insert  into `app_component_target`(`id`,`content`,`category_id`,`create_time`) values (1,'波斯猫',NULL,'2018-05-07 13:55:53'),(2,'啤酒',NULL,'2018-05-07 13:55:54'),(3,'hello',NULL,'2018-05-07 13:55:57');

/*Table structure for table `app_coupon` */

DROP TABLE IF EXISTS `app_coupon`;

CREATE TABLE `app_coupon` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(8) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'CASH',
  `price` float DEFAULT NULL,
  `limit_price` float DEFAULT NULL,
  `shop_id` int(4) DEFAULT NULL,
  `stock` int(8) DEFAULT NULL,
  `per_limit` int(2) NOT NULL DEFAULT '1',
  `suite_limit` int(2) NOT NULL DEFAULT '0',
  `is_campaign` tinyint(1) DEFAULT '0' COMMENT '是否促销活动',
  `campaign_img` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `campaign_scene` int(4) DEFAULT '0',
  `is_platform` tinyint(1) DEFAULT '0',
  `is_self_use` tinyint(1) DEFAULT '0',
  `is_present` tinyint(1) DEFAULT '0',
  `present_fee` float DEFAULT '0',
  `is_show` tinyint(1) DEFAULT '0',
  `is_show_home` tinyint(1) DEFAULT '0',
  `desc` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `send_now` tinyint(1) DEFAULT '0',
  `begin_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `due_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `goods_id_list` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_coupon` */

/*Table structure for table `app_coupon_customer` */

DROP TABLE IF EXISTS `app_coupon_customer`;

CREATE TABLE `app_coupon_customer` (
  `id` int(64) NOT NULL AUTO_INCREMENT,
  `customer_id` int(32) DEFAULT NULL,
  `coupon_id` int(32) DEFAULT NULL,
  `is_used` tinyint(1) DEFAULT '0',
  `accept_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_coupon_customer` */

/*Table structure for table `app_customer` */

DROP TABLE IF EXISTS `app_customer`;

CREATE TABLE `app_customer` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `open_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `nick_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar_url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL COMMENT '1男 2女 0未知',
  `province` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `language` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000005 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_customer` */

insert  into `app_customer`(`id`,`open_id`,`nick_name`,`avatar_url`,`gender`,`province`,`city`,`country`,`language`,`create_time`,`update_time`) values (1000000,'ENWA-ssMGjD3cBPDCKj1N6jss9LNGv','中国红','https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=380101692,1602047999&fm=27&gp=0.jpg',NULL,NULL,NULL,NULL,NULL,'2018-05-10 10:56:29',NULL),(1000001,'ENWA-ssMGjD3cBPDCKj1N6jss9LNGv','hellodog','https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=380101692,1602047999&fm=27&gp=0.jpg',NULL,NULL,NULL,NULL,NULL,'2018-05-10 10:56:38',NULL),(1000002,'ENWA-ssMGjD3cBPDCKj1N6jss9LNGv','test','https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=380101692,1602047999&fm=27&gp=0.jpg',NULL,NULL,NULL,NULL,NULL,'2018-05-11 11:57:48',NULL),(1000003,'testhello','小红帽',NULL,1,'北京','北京','海淀区',NULL,'2018-05-11 17:02:27','2018-05-16 18:04:39'),(1000004,'oagCl5LzDBvUHXU0i9o6VRFS_w1g',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2018-05-11 22:33:12',NULL);

/*Table structure for table `app_customer_address` */

DROP TABLE IF EXISTS `app_customer_address`;

CREATE TABLE `app_customer_address` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `customer_id` int(32) NOT NULL,
  `name` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sex` tinyint(1) DEFAULT NULL COMMENT '1男士 2女士',
  `phone` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT '0',
  `detail` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `full_address` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `province` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `town` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_customer_address` */

insert  into `app_customer_address`(`id`,`customer_id`,`name`,`sex`,`phone`,`is_default`,`detail`,`full_address`,`province`,`city`,`country`,`town`,`latitude`,`longitude`) values (1,1000004,'张三',1,'13939391199',1,'5号楼','北京市昌平区政府街19号昌平区政府(政府街北)5号楼','北京市','北京市','昌平区','城北街道',40.2208,116.231),(2,1000004,'李四',2,'13838384438',0,'205室','河北省张家口市崇礼区长青路30崇礼区政府205室','河北省','张家口市','崇礼区',NULL,40.9746,115.283),(3,1000004,'于生龙',2,'13688886666',0,'202室','河北省张家口市崇礼区中国邮政储蓄银行崇礼县支行附近崇礼冰雪博物馆202室','河北省','张家口市','崇礼区',NULL,40.9783,115.289);

/*Table structure for table `app_customer_token` */

DROP TABLE IF EXISTS `app_customer_token`;

CREATE TABLE `app_customer_token` (
  `customer_id` int(32) NOT NULL,
  `token` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `expire_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_customer_token` */

insert  into `app_customer_token`(`customer_id`,`token`,`expire_time`,`update_time`) values (1000003,'7d5c0b23f8a208256e72ac33f9beab0b','2018-05-31 06:06:11','2018-05-11 18:06:11'),(1000004,'4534a715a92ccdddc7ac3c0a0624efe4','2018-06-04 21:28:06','2018-05-16 22:50:24');

/*Table structure for table `app_favorite_goods` */

DROP TABLE IF EXISTS `app_favorite_goods`;

CREATE TABLE `app_favorite_goods` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `customer_id` int(32) NOT NULL,
  `goods_id` int(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_favorite_goods` */

/*Table structure for table `app_goods` */

DROP TABLE IF EXISTS `app_goods`;

CREATE TABLE `app_goods` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `subhead` text COLLATE utf8_unicode_ci,
  `shop_id` tinyint(2) NOT NULL DEFAULT '3',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `original_price` double NOT NULL,
  `sell_price` double NOT NULL,
  `is_recommend` tinyint(1) NOT NULL DEFAULT '0',
  `category_id` int(4) NOT NULL,
  `sales_volume` int(8) NOT NULL DEFAULT '0',
  `total_stock` int(8) NOT NULL DEFAULT '0',
  `post_type` tinyint(1) DEFAULT '0',
  `post_fee` float DEFAULT '0',
  `favorite_count` int(32) NOT NULL DEFAULT '0',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100008 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_goods` */

insert  into `app_goods`(`id`,`name`,`subhead`,`shop_id`,`status`,`original_price`,`sell_price`,`is_recommend`,`category_id`,`sales_volume`,`total_stock`,`post_type`,`post_fee`,`favorite_count`,`create_time`,`update_time`) values (1,'中国白酒 茅台51度汉酱500ml','中国白酒 茅台51度汉酱500ml',3,0,12.9,9.9,1,1,7,99,0,0,0,'2018-04-19 11:39:49','2018-05-16 21:49:53'),(100000,'国窖1573十年陈酿','国窖1573十年陈酿',3,0,99.9,89.9,1,1,5,88,0,0,0,'2018-04-20 14:55:48','2018-05-16 21:37:38'),(100001,'国窖1573十年陈酿',NULL,3,0,999,999,1,2,12,100,0,0,0,'2018-05-16 14:59:06','2018-05-16 22:24:52'),(100002,'海之蓝',NULL,3,0,128,128,1,2,22,99,0,0,0,NULL,'2018-05-16 22:24:53'),(100003,'天之蓝',NULL,3,0,358,358,1,2,34,99,0,0,0,NULL,'2018-05-16 22:24:54'),(100004,'梦之蓝',NULL,3,0,788,788,1,2,34,99,0,0,0,NULL,'2018-05-16 22:24:55'),(100005,'飞天茅台',NULL,3,0,1288,1288,1,2,55,99,0,0,0,NULL,'2018-05-16 22:24:56'),(100006,'五粮液1988',NULL,3,0,998,998,1,2,24,99,0,0,0,NULL,'2018-05-16 22:24:58');

/*Table structure for table `app_goods_detail` */

DROP TABLE IF EXISTS `app_goods_detail`;

CREATE TABLE `app_goods_detail` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) DEFAULT NULL,
  `sequence` int(8) NOT NULL DEFAULT '0',
  `content` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` tinyint(2) NOT NULL DEFAULT '2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_goods_detail` */

insert  into `app_goods_detail`(`id`,`goods_id`,`sequence`,`content`,`type`) values (1,1,0,'http://gfs2.gomein.net.cn/T1T7EvB7E_1RCvBVdK',2),(2,1,1,'http://gfs.gomein.net.cn/T1kcLvBCZg1RCvBVdK',2),(3,100000,0,'http://img.leshare.shop/Fh4_7_BKLOw-kGaCO57c_r0UluK0',2),(4,100000,1,'http://img.leshare.shop/FivqLKQXz2nFU4waQBvAHRBqHNVt',2),(5,1,2,'http://gfs.gomein.net.cn/T1n2hvBjJT1RCvBVdK',2),(6,1,3,'http://gfs.gomein.net.cn/T1JcLvBTWg1RCvBVdK',2);

/*Table structure for table `app_goods_image` */

DROP TABLE IF EXISTS `app_goods_image`;

CREATE TABLE `app_goods_image` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) NOT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_goods_image` */

insert  into `app_goods_image`(`id`,`goods_id`,`url`,`create_time`) values (1,1,'http://gfs17.gomein.net.cn/T1mmbvB_Ab1RCvBVdK_450.jpg','2018-05-16 21:50:24'),(2,1,'http://gfs.gomein.net.cn/T1s0JvBKL_1RCvBVdK_450.jpg','2018-05-16 21:50:48'),(3,100000,'http://gfs17.gomein.net.cn/T1XidTBjYT1RCvBVdK_360.jpg','2018-05-16 21:38:50'),(4,100000,'http://gfs1.gomein.net.cn/T1oQDTB_KT1RCvBVdK_360.jpg','2018-05-16 21:38:57'),(5,100001,'http://gfs17.gomein.net.cn/T1XidTBjYT1RCvBVdK_360.jpg','2018-05-16 21:19:44'),(6,100002,'http://gfs17.gomein.net.cn/T14OJvB5Vg1RCvBVdK_450.jpg','2018-05-16 21:22:14'),(7,100003,'http://gfs17.gomein.net.cn/T1KPJQB5JT1RCvBVdK_360.jpg','2018-05-16 21:23:08'),(8,100004,'http://gfs17.gomein.net.cn/T1wwbjBCLT1RCvBVdK_360.jpg','2018-05-16 21:23:59'),(9,100005,'http://gfs17.gomein.net.cn/T1yDA_BvJT1RCvBVdK_360.jpg','2018-05-16 21:24:46'),(10,100006,'http://gfs17.gomein.net.cn/T1BcLvBTJj1RCvBVdK_450.jpg','2018-05-16 21:25:22');

/*Table structure for table `app_goods_sku` */

DROP TABLE IF EXISTS `app_goods_sku`;

CREATE TABLE `app_goods_sku` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) NOT NULL,
  `sku` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `price` float DEFAULT NULL,
  `stock` int(8) DEFAULT NULL,
  `image_url` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_goods_sku` */

/*Table structure for table `app_goods_stock` */

DROP TABLE IF EXISTS `app_goods_stock`;

CREATE TABLE `app_goods_stock` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) NOT NULL,
  `sku_id` int(8) NOT NULL,
  `stock` int(8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_goods_stock` */

/*Table structure for table `app_order` */

DROP TABLE IF EXISTS `app_order`;

CREATE TABLE `app_order` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) NOT NULL,
  `customer_id` int(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `deal_price` float NOT NULL,
  `final_price` float NOT NULL,
  `payment_type` tinyint(2) NOT NULL DEFAULT '1',
  `order_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `payment_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `coupon_used_id` int(8) NOT NULL DEFAULT '0',
  `seller_note` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `receive_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `receive_phone` int(11) NOT NULL,
  `shop_id` int(8) DEFAULT '3',
  `shop_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `post_fee` float NOT NULL DEFAULT '0',
  `order_type` tinyint(2) NOT NULL DEFAULT '10',
  `arrive_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000002 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_order` */

insert  into `app_order`(`id`,`goods_id`,`customer_id`,`status`,`deal_price`,`final_price`,`payment_type`,`order_time`,`payment_time`,`coupon_used_id`,`seller_note`,`address`,`receive_name`,`receive_phone`,`shop_id`,`shop_name`,`post_fee`,`order_type`,`arrive_time`) values (10000000,100001,0,0,0,0,1,'2018-04-23 11:01:28','0000-00-00 00:00:00',0,NULL,'','',0,3,NULL,0,10,'0000-00-00 00:00:00'),(10000001,1,0,0,0,0,1,'2018-04-22 11:01:37','0000-00-00 00:00:00',0,NULL,'','',0,3,NULL,0,10,'0000-00-00 00:00:00');

/*Table structure for table `app_page` */

DROP TABLE IF EXISTS `app_page`;

CREATE TABLE `app_page` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'HOME',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_page` */

insert  into `app_page`(`id`,`name`,`type`) values (1,'HelloMe','CUSTOM'),(2,'HelloShop','HOME');

/*Table structure for table `app_page_component` */

DROP TABLE IF EXISTS `app_page_component`;

CREATE TABLE `app_page_component` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `type` enum('SEARCH_BAR','SWIPER','NOTICE_BAR','IMAGE_BOX','COUPON_BOX','GOODS_BOX','VIP_CARD','BALANCE_BAR','SEPARATOR','ORDER_BAR','NAV_GRID','COPYRIGHT') COLLATE utf8_unicode_ci DEFAULT NULL,
  `seq` int(4) NOT NULL,
  `page_id` int(4) DEFAULT '2',
  `shop_id` int(4) DEFAULT '3',
  `title` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `param` text COLLATE utf8_unicode_ci,
  `is_use` tinyint(1) DEFAULT '1',
  `create_time` timestamp NOT NULL DEFAULT '2018-04-19 11:06:00',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_page_component` */

insert  into `app_page_component`(`id`,`type`,`seq`,`page_id`,`shop_id`,`title`,`param`,`is_use`,`create_time`,`update_time`) values (1,'SEARCH_BAR',1,2,3,'搜索栏','{\"isContact\": true, \"border\":\"none\"}',1,'2018-04-19 11:06:00','2018-05-08 22:10:27'),(2,'SWIPER',2,2,3,'轮播图','{\"height\": \"234rpx\",\"count\": 3}',1,'2018-04-19 11:06:00','2018-05-08 22:10:42'),(3,'NOTICE_BAR',3,2,3,'公告栏',NULL,1,'2018-04-19 11:06:00','0000-00-00 00:00:00'),(4,'IMAGE_BOX',4,2,3,'首页菜单','{\"count\": 4,\"height\": \"55px\",\"width\": \"55px\",\"isShowTitle\": true}',1,'2018-04-19 11:06:00','2018-05-08 22:12:06'),(5,'COUPON_BOX',5,2,3,'领券优惠','{\"isTitle\": false,\"layout\": \"ROW\",\"source\": \"COUPONS_ALL\"}',1,'2018-04-19 11:06:00','2018-05-08 22:12:27'),(6,'IMAGE_BOX',6,2,3,'酒水区','{\"count\": 1,\"height\": \"55px\",\"width\": \"400px\",\"isShowTitle\": false, \"backgroundColor\": \"#F5F5F5\"}',1,'2018-04-19 11:06:00','2018-05-16 22:06:48'),(7,'IMAGE_BOX',7,2,3,'分类-纸品','{\"count\": 5,\"height\": \"55px\",\"width\": \"55px\",\"isShowTitle\": true,\"border\": \"none\"}',1,'2018-04-19 11:06:00','2018-05-08 22:13:51'),(8,'GOODS_BOX',8,2,3,'推荐商品','{\"count\": 3,\"source\": \"GOODS\",\"layout\": \"ROW\",\"content\": null,\"categoryId\": null,\"by\": null,\"sort\": null,\"isSales\": true,\"isTitle\": false,\"isMore\": false,\"isCart\": true,\"isPrice\": true,\"isGoodsName\": true,\"isTips\": true,\"skuMode\": \"SLIDER\",\"moreText\": \"\",\"border\": \"none\"}',1,'2018-04-19 11:06:00','2018-05-16 14:55:53'),(9,'GOODS_BOX',9,2,3,'白酒-精选','{\"count\": 9,  \"source\": \"GOODS\",  \"layout\": \"TIGHT\",  \"content\": \"啤酒\",  \"categoryId\": null,  \"by\": \"sales_volume\",  \"sort\": \"desc\",  \"isSales\": true,  \"isTitle\": false,  \"isMore\": true,  \"isCart\": true,  \"isPrice\": true,  \"isGoodsName\": true,  \"isTips\": true,  \"skuMode\": \"SLIDER\",  \"moreText\": \"查看更多\",  \"border\": \"none\"}',1,'2018-04-19 11:06:00','2018-05-16 14:56:04'),(10,'VIP_CARD',1,1,3,'会员卡',NULL,1,'2018-04-19 11:06:00','2018-05-15 12:05:12'),(11,'BALANCE_BAR',2,1,3,'余额栏',NULL,1,'2018-04-19 11:06:00','2018-05-15 12:05:12'),(12,'SEPARATOR',3,1,3,'分隔符','{\"height\": \"10rpx\",  \"backgroundColor\": \"#F5F5F5\",  \"borderTop\": true,  \"borderBottom\": false}',1,'2018-04-19 11:06:00','2018-05-15 12:05:56'),(13,'ORDER_BAR',4,1,3,'订单栏',NULL,1,'2018-04-19 11:06:00','2018-05-15 12:06:50'),(14,'SEPARATOR',5,1,3,'分隔符','{\"height\": \"10rpx\",  \"backgroundColor\": \"#F5F5F5\",  \"borderTop\": false,  \"borderBottom\": false}',1,'2018-04-19 11:06:00','2018-05-15 12:07:24'),(15,'NAV_GRID',6,1,3,'工具栏',NULL,1,'2018-04-19 11:06:00','2018-05-15 12:08:06'),(16,'COPYRIGHT',7,1,3,'版权信息',NULL,1,'2018-04-19 11:06:00','2018-05-15 12:08:45');

/*Table structure for table `app_page_plugin` */

DROP TABLE IF EXISTS `app_page_plugin`;

CREATE TABLE `app_page_plugin` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `page_id` int(4) NOT NULL,
  `shop_id` int(4) NOT NULL,
  `type` enum('SKU_SLIDE_PANEL','CART_WIDGET') COLLATE utf8_unicode_ci NOT NULL,
  `is_use` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_page_plugin` */

insert  into `app_page_plugin`(`id`,`page_id`,`shop_id`,`type`,`is_use`) values (1,2,3,'SKU_SLIDE_PANEL',1),(2,2,3,'CART_WIDGET',1);

/*Table structure for table `app_shop` */

DROP TABLE IF EXISTS `app_shop`;

CREATE TABLE `app_shop` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `category_id` int(4) DEFAULT NULL,
  `category_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `describe` text COLLATE utf8_unicode_ci,
  `address` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `avatar` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `auto_order` tinyint(1) NOT NULL DEFAULT '1',
  `off_pay` tinyint(1) NOT NULL DEFAULT '1',
  `support_member` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_shop` */

insert  into `app_shop`(`id`,`name`,`category_id`,`category_name`,`describe`,`address`,`phone`,`create_time`,`update_time`,`avatar`,`auto_order`,`off_pay`,`support_member`) values (3,'小酌怡情',19,NULL,'testtesttest','长青路19号','12939399999','2018-05-14 10:36:45','2018-05-14 10:38:45',NULL,1,1,1);

/*Table structure for table `app_shop_notice` */

DROP TABLE IF EXISTS `app_shop_notice`;

CREATE TABLE `app_shop_notice` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `shop_id` int(4) DEFAULT NULL,
  `content` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_show` tinyint(1) DEFAULT '1',
  `is_home` tinyint(1) DEFAULT '1',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_shop_notice` */

insert  into `app_shop_notice`(`id`,`shop_id`,`content`,`is_show`,`is_home`,`update_time`,`create_time`) values (1,3,'满99元下单立减10元',1,1,'2018-05-14 10:41:33','2018-05-14 10:41:20'),(2,3,'满39远免费配送，30分钟立达',1,1,'2018-05-14 10:42:24','2018-05-14 10:42:45');

/*Table structure for table `app_shop_status` */

DROP TABLE IF EXISTS `app_shop_status`;

CREATE TABLE `app_shop_status` (
  `shop_id` int(4) NOT NULL,
  `status` varchar(8) COLLATE utf8_unicode_ci DEFAULT 'NORMAL',
  `open` tinyint(1) DEFAULT '1',
  `begin_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`shop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `app_shop_status` */

insert  into `app_shop_status`(`shop_id`,`status`,`open`,`begin_time`,`end_time`) values (3,'NORMAL',1,'00:00:00','23:59:59');

/*Table structure for table `schedule_job` */

DROP TABLE IF EXISTS `schedule_job`;

CREATE TABLE `schedule_job` (
  `job_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '任务id',
  `bean_name` varchar(200) DEFAULT NULL COMMENT 'spring bean名称',
  `method_name` varchar(100) DEFAULT NULL COMMENT '方法名',
  `params` varchar(2000) DEFAULT NULL COMMENT '参数',
  `cron_expression` varchar(100) DEFAULT NULL COMMENT 'cron表达式',
  `status` tinyint(4) DEFAULT NULL COMMENT '任务状态  0：正常  1：暂停',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='定时任务';

/*Data for the table `schedule_job` */

insert  into `schedule_job`(`job_id`,`bean_name`,`method_name`,`params`,`cron_expression`,`status`,`remark`,`create_time`) values (1,'testTask','test','renren','0 0/30 * * * ?',0,'有参数测试','2016-12-01 23:16:46'),(2,'testTask','test2',NULL,'0 0/30 * * * ?',1,'无参数测试','2016-12-03 14:55:56');

/*Table structure for table `schedule_job_log` */

DROP TABLE IF EXISTS `schedule_job_log`;

CREATE TABLE `schedule_job_log` (
  `log_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '任务日志id',
  `job_id` bigint(20) NOT NULL COMMENT '任务id',
  `bean_name` varchar(200) DEFAULT NULL COMMENT 'spring bean名称',
  `method_name` varchar(100) DEFAULT NULL COMMENT '方法名',
  `params` varchar(2000) DEFAULT NULL COMMENT '参数',
  `status` tinyint(4) NOT NULL COMMENT '任务状态    0：成功    1：失败',
  `error` varchar(2000) DEFAULT NULL COMMENT '失败信息',
  `times` int(11) NOT NULL COMMENT '耗时(单位：毫秒)',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`log_id`),
  KEY `job_id` (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8 COMMENT='定时任务日志';

/*Data for the table `schedule_job_log` */

insert  into `schedule_job_log`(`log_id`,`job_id`,`bean_name`,`method_name`,`params`,`status`,`error`,`times`,`create_time`) values (1,1,'testTask','test','renren',0,NULL,1119,'2018-05-04 15:30:00'),(2,1,'testTask','test','renren',0,NULL,1037,'2018-05-07 18:30:00'),(3,1,'testTask','test','renren',0,NULL,1102,'2018-05-08 14:30:00'),(4,1,'testTask','test','renren',0,NULL,1018,'2018-05-08 15:00:00'),(5,1,'testTask','test','renren',0,NULL,1035,'2018-05-08 16:00:00'),(6,1,'testTask','test','renren',0,NULL,1082,'2018-05-08 17:00:00'),(7,1,'testTask','test','renren',0,NULL,1019,'2018-05-08 17:30:00'),(8,1,'testTask','test','renren',0,NULL,1138,'2018-05-08 18:30:00'),(9,1,'testTask','test','renren',0,NULL,1018,'2018-05-08 21:30:00'),(10,1,'testTask','test','renren',0,NULL,1024,'2018-05-08 22:00:00'),(11,1,'testTask','test','renren',0,NULL,1022,'2018-05-08 22:30:00'),(12,1,'testTask','test','renren',0,NULL,1034,'2018-05-09 11:30:00'),(13,1,'testTask','test','renren',0,NULL,1004,'2018-05-09 12:00:00'),(14,1,'testTask','test','renren',0,NULL,1009,'2018-05-09 12:30:00'),(15,1,'testTask','test','renren',0,NULL,1005,'2018-05-09 14:30:00'),(16,1,'testTask','test','renren',0,NULL,1004,'2018-05-09 15:00:00'),(17,1,'testTask','test','renren',0,NULL,1023,'2018-05-09 17:30:00'),(18,1,'testTask','test','renren',0,NULL,1025,'2018-05-09 21:30:00'),(19,1,'testTask','test','renren',0,NULL,1019,'2018-05-09 22:00:00'),(20,1,'testTask','test','renren',0,NULL,1031,'2018-05-10 12:00:00'),(21,1,'testTask','test','renren',0,NULL,1045,'2018-05-10 14:30:00'),(22,1,'testTask','test','renren',0,NULL,1022,'2018-05-10 21:00:01'),(23,1,'testTask','test','renren',0,NULL,1020,'2018-05-10 21:30:00'),(24,1,'testTask','test','renren',0,NULL,1015,'2018-05-10 22:00:00'),(25,1,'testTask','test','renren',0,NULL,1171,'2018-05-11 17:00:00'),(26,1,'testTask','test','renren',0,NULL,1066,'2018-05-11 18:00:00'),(27,1,'testTask','test','renren',0,NULL,1024,'2018-05-11 18:30:00'),(28,1,'testTask','test','renren',0,NULL,1023,'2018-05-11 20:30:00'),(29,1,'testTask','test','renren',0,NULL,1024,'2018-05-11 21:00:00'),(30,1,'testTask','test','renren',0,NULL,1020,'2018-05-11 21:30:00'),(31,1,'testTask','test','renren',0,NULL,1020,'2018-05-11 22:00:00'),(32,1,'testTask','test','renren',0,NULL,1028,'2018-05-11 22:30:00'),(33,1,'testTask','test','renren',0,NULL,1019,'2018-05-11 23:00:00'),(34,1,'testTask','test','renren',0,NULL,1029,'2018-05-14 17:00:00'),(35,1,'testTask','test','renren',0,NULL,1005,'2018-05-14 17:30:00'),(36,1,'testTask','test','renren',0,NULL,1004,'2018-05-14 18:00:00'),(37,1,'testTask','test','renren',0,NULL,1007,'2018-05-14 18:30:00'),(38,1,'testTask','test','renren',0,NULL,1028,'2018-05-14 21:00:00'),(39,1,'testTask','test','renren',0,NULL,1018,'2018-05-14 21:30:00'),(40,1,'testTask','test','renren',0,NULL,1021,'2018-05-14 22:00:00'),(41,1,'testTask','test','renren',0,NULL,1014,'2018-05-14 22:30:00'),(42,1,'testTask','test','renren',0,NULL,1072,'2018-05-15 15:00:00'),(43,1,'testTask','test','renren',0,NULL,1197,'2018-05-15 15:30:01'),(44,1,'testTask','test','renren',0,NULL,1020,'2018-05-15 16:00:00'),(45,1,'testTask','test','renren',0,NULL,1051,'2018-05-15 16:30:00'),(46,1,'testTask','test','renren',0,NULL,1024,'2018-05-15 17:00:00'),(47,1,'testTask','test','renren',0,NULL,1123,'2018-05-15 18:00:00'),(48,1,'testTask','test','renren',0,NULL,1023,'2018-05-15 21:30:00'),(49,1,'testTask','test','renren',0,NULL,1022,'2018-05-15 22:00:00'),(50,1,'testTask','test','renren',0,NULL,1088,'2018-05-16 15:30:00'),(51,1,'testTask','test','renren',0,NULL,1034,'2018-05-16 18:00:00'),(52,1,'testTask','test','renren',0,NULL,1023,'2018-05-16 21:00:00'),(53,1,'testTask','test','renren',0,NULL,1018,'2018-05-16 21:30:00'),(54,1,'testTask','test','renren',0,NULL,1008,'2018-05-16 22:00:00'),(55,1,'testTask','test','renren',0,NULL,1013,'2018-05-16 22:30:00');

/*Table structure for table `sys_config` */

DROP TABLE IF EXISTS `sys_config`;

CREATE TABLE `sys_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `key` varchar(50) DEFAULT NULL COMMENT 'key',
  `value` varchar(2000) DEFAULT NULL COMMENT 'value',
  `status` tinyint(4) DEFAULT '1' COMMENT '状态   0：隐藏   1：显示',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='系统配置信息表';

/*Data for the table `sys_config` */

insert  into `sys_config`(`id`,`key`,`value`,`status`,`remark`) values (1,'CLOUD_STORAGE_CONFIG_KEY','{\"aliyunAccessKeyId\":\"\",\"aliyunAccessKeySecret\":\"\",\"aliyunBucketName\":\"\",\"aliyunDomain\":\"\",\"aliyunEndPoint\":\"\",\"aliyunPrefix\":\"\",\"qcloudBucketName\":\"\",\"qcloudDomain\":\"\",\"qcloudPrefix\":\"\",\"qcloudSecretId\":\"\",\"qcloudSecretKey\":\"\",\"qiniuAccessKey\":\"NrgMfABZxWLo5B-YYSjoE8-AZ1EISdi1Z3ubLOeZ\",\"qiniuBucketName\":\"ios-app\",\"qiniuDomain\":\"http://7xqbwh.dl1.z0.glb.clouddn.com\",\"qiniuPrefix\":\"upload\",\"qiniuSecretKey\":\"uIwJHevMRWU0VLxFvgy0tAcOdGqasdtVlJkdy6vV\",\"type\":1}',0,'云存储配置信息');

/*Table structure for table `sys_log` */

DROP TABLE IF EXISTS `sys_log`;

CREATE TABLE `sys_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL COMMENT '用户名',
  `operation` varchar(50) DEFAULT NULL COMMENT '用户操作',
  `method` varchar(200) DEFAULT NULL COMMENT '请求方法',
  `params` varchar(5000) DEFAULT NULL COMMENT '请求参数',
  `time` bigint(20) NOT NULL COMMENT '执行时长(毫秒)',
  `ip` varchar(64) DEFAULT NULL COMMENT 'IP地址',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统日志';

/*Data for the table `sys_log` */

/*Table structure for table `sys_menu` */

DROP TABLE IF EXISTS `sys_menu`;

CREATE TABLE `sys_menu` (
  `menu_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `parent_id` bigint(20) DEFAULT NULL COMMENT '父菜单ID，一级菜单为0',
  `name` varchar(50) DEFAULT NULL COMMENT '菜单名称',
  `url` varchar(200) DEFAULT NULL COMMENT '菜单URL',
  `perms` varchar(500) DEFAULT NULL COMMENT '授权(多个用逗号分隔，如：user:list,user:create)',
  `type` int(11) DEFAULT NULL COMMENT '类型   0：目录   1：菜单   2：按钮',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `order_num` int(11) DEFAULT NULL COMMENT '排序',
  PRIMARY KEY (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COMMENT='菜单管理';

/*Data for the table `sys_menu` */

insert  into `sys_menu`(`menu_id`,`parent_id`,`name`,`url`,`perms`,`type`,`icon`,`order_num`) values (1,0,'系统管理',NULL,NULL,0,'fa fa-cog',0),(2,1,'管理员列表','modules/sys/user.html',NULL,1,'fa fa-user',1),(3,1,'角色管理','modules/sys/role.html',NULL,1,'fa fa-user-secret',2),(4,1,'菜单管理','modules/sys/menu.html',NULL,1,'fa fa-th-list',3),(5,1,'SQL监控','druid/sql.html',NULL,1,'fa fa-bug',4),(6,1,'定时任务','modules/job/schedule.html',NULL,1,'fa fa-tasks',5),(7,6,'查看',NULL,'sys:schedule:list,sys:schedule:info',2,NULL,0),(8,6,'新增',NULL,'sys:schedule:save',2,NULL,0),(9,6,'修改',NULL,'sys:schedule:update',2,NULL,0),(10,6,'删除',NULL,'sys:schedule:delete',2,NULL,0),(11,6,'暂停',NULL,'sys:schedule:pause',2,NULL,0),(12,6,'恢复',NULL,'sys:schedule:resume',2,NULL,0),(13,6,'立即执行',NULL,'sys:schedule:run',2,NULL,0),(14,6,'日志列表',NULL,'sys:schedule:log',2,NULL,0),(15,2,'查看',NULL,'sys:user:list,sys:user:info',2,NULL,0),(16,2,'新增',NULL,'sys:user:save,sys:role:select',2,NULL,0),(17,2,'修改',NULL,'sys:user:update,sys:role:select',2,NULL,0),(18,2,'删除',NULL,'sys:user:delete',2,NULL,0),(19,3,'查看',NULL,'sys:role:list,sys:role:info',2,NULL,0),(20,3,'新增',NULL,'sys:role:save,sys:menu:list',2,NULL,0),(21,3,'修改',NULL,'sys:role:update,sys:menu:list',2,NULL,0),(22,3,'删除',NULL,'sys:role:delete',2,NULL,0),(23,4,'查看',NULL,'sys:menu:list,sys:menu:info',2,NULL,0),(24,4,'新增',NULL,'sys:menu:save,sys:menu:select',2,NULL,0),(25,4,'修改',NULL,'sys:menu:update,sys:menu:select',2,NULL,0),(26,4,'删除',NULL,'sys:menu:delete',2,NULL,0),(27,1,'参数管理','modules/sys/config.html','sys:config:list,sys:config:info,sys:config:save,sys:config:update,sys:config:delete',1,'fa fa-sun-o',6),(29,1,'系统日志','modules/sys/log.html','sys:log:list',1,'fa fa-file-text-o',7),(30,1,'文件上传','modules/oss/oss.html','sys:oss:all',1,'fa fa-file-image-o',6),(31,0,'压力测试',NULL,NULL,0,'fa fa-bolt',0),(32,31,'性能测试用例管理','modules/test/stressTest.html','test:stress',1,'fa fa-briefcase',1);

/*Table structure for table `sys_oss` */

DROP TABLE IF EXISTS `sys_oss`;

CREATE TABLE `sys_oss` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) DEFAULT NULL COMMENT 'URL地址',
  `create_date` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文件上传';

/*Data for the table `sys_oss` */

/*Table structure for table `sys_role` */

DROP TABLE IF EXISTS `sys_role`;

CREATE TABLE `sys_role` (
  `role_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) DEFAULT NULL COMMENT '角色名称',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `create_user_id` bigint(20) DEFAULT NULL COMMENT '创建者ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色';

/*Data for the table `sys_role` */

/*Table structure for table `sys_role_menu` */

DROP TABLE IF EXISTS `sys_role_menu`;

CREATE TABLE `sys_role_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role_id` bigint(20) DEFAULT NULL COMMENT '角色ID',
  `menu_id` bigint(20) DEFAULT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色与菜单对应关系';

/*Data for the table `sys_role_menu` */

/*Table structure for table `sys_user` */

DROP TABLE IF EXISTS `sys_user`;

CREATE TABLE `sys_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) DEFAULT NULL COMMENT '密码',
  `salt` varchar(20) DEFAULT NULL COMMENT '盐',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `mobile` varchar(100) DEFAULT NULL COMMENT '手机号',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态  0：禁用   1：正常',
  `create_user_id` bigint(20) DEFAULT NULL COMMENT '创建者ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='系统用户';

/*Data for the table `sys_user` */

insert  into `sys_user`(`user_id`,`username`,`password`,`salt`,`email`,`mobile`,`status`,`create_user_id`,`create_time`) values (1,'admin','9ec9750e709431dad22365cabc5c625482e574c74adaebba7dd02f1129e4ce1d','YzcmCZNvbXocrsz9dm8e','root@renren.io','13612345678',1,1,'2016-11-11 11:11:11');

/*Table structure for table `sys_user_role` */

DROP TABLE IF EXISTS `sys_user_role`;

CREATE TABLE `sys_user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户ID',
  `role_id` bigint(20) DEFAULT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户与角色对应关系';

/*Data for the table `sys_user_role` */

/*Table structure for table `sys_user_token` */

DROP TABLE IF EXISTS `sys_user_token`;

CREATE TABLE `sys_user_token` (
  `user_id` bigint(20) NOT NULL,
  `token` varchar(100) NOT NULL COMMENT 'token',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统用户Token';

/*Data for the table `sys_user_token` */

insert  into `sys_user_token`(`user_id`,`token`,`expire_time`,`update_time`) values (1,'194a005da2dee8e08905d567d241beb8','2018-05-05 03:17:24','2018-05-04 15:17:24');

/*Table structure for table `tb_user` */

DROP TABLE IF EXISTS `tb_user`;

CREATE TABLE `tb_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `mobile` varchar(20) NOT NULL COMMENT '手机号',
  `password` varchar(64) DEFAULT NULL COMMENT '密码',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='用户';

/*Data for the table `tb_user` */

insert  into `tb_user`(`user_id`,`username`,`mobile`,`password`,`create_time`) values (1,'mark','13612345678','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918','2017-03-23 22:37:41');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
