/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.1.73 : Database - batman
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`batman` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `batman`;

/*Table structure for table `comments` */

DROP TABLE IF EXISTS `comments`;

CREATE TABLE `comments` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `orderId` int(32) NOT NULL,
  `customerId` int(32) NOT NULL,
  `shopId` int(8) NOT NULL DEFAULT '0',
  `goodsId` int(32) NOT NULL,
  `star` tinyint(2) NOT NULL,
  `comment` text COLLATE utf8_unicode_ci,
  `images` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updateTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `comments` */

insert  into `comments`(`id`,`orderId`,`customerId`,`shopId`,`goodsId`,`star`,`comment`,`images`,`createTime`,`updateTime`) values (1,10000001,1000000,0,1,5,'HelloWorld绝对好',NULL,'2018-04-23 11:02:42','2018-04-23 11:14:42'),(2,10000002,1000001,0,1,3,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-04-23 14:33:20'),(3,10000003,1000002,0,1,4,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-04-23 14:33:23'),(4,10000004,1000003,0,1,2,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-04-23 14:33:25'),(5,10000005,1000004,0,1,1,'HelloWorld绝对好',NULL,'2018-04-23 11:14:42','2018-04-23 14:33:30'),(6,10000006,1000004,0,100000,3,'HelloWorld绝对好',NULL,'0000-00-00 00:00:00','2018-04-23 14:36:25');

/*Table structure for table `customer` */

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `open_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `customer` */

insert  into `customer`(`id`,`open_id`,`name`,`createTime`) values (1000000,'ENWA-ssMGjD3cBPDCKj1N6jss9LNGv','春天来了','2018-04-23 11:15:34');

/*Table structure for table `favorite_goods` */

DROP TABLE IF EXISTS `favorite_goods`;

CREATE TABLE `favorite_goods` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `customerId` int(32) NOT NULL,
  `goodsId` int(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `favorite_goods` */

/*Table structure for table `goods` */

DROP TABLE IF EXISTS `goods`;

CREATE TABLE `goods` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `subhead` text COLLATE utf8_unicode_ci,
  `shopId` tinyint(2) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `originalPrice` double NOT NULL,
  `sellPrice` double NOT NULL,
  `isRecommend` tinyint(1) NOT NULL DEFAULT '0',
  `postType` tinyint(1) DEFAULT '0',
  `postFee` float DEFAULT '0',
  `favoriteCount` int(32) NOT NULL DEFAULT '0',
  `categoryId` int(4) NOT NULL,
  `salesVolume` int(8) NOT NULL DEFAULT '0',
  `totalStock` int(8) NOT NULL DEFAULT '0',
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updateTime` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100001 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `goods` */

insert  into `goods`(`id`,`name`,`subhead`,`shopId`,`status`,`originalPrice`,`sellPrice`,`isRecommend`,`postType`,`postFee`,`favoriteCount`,`categoryId`,`salesVolume`,`totalStock`,`createTime`,`updateTime`) values (1,'test','testtesttest',0,0,12.9,9.9,0,0,0,0,28,7,99,'2018-04-19 11:39:49','2018-04-23 21:25:32'),(100000,'卡卡西','鸣人佐助小樱',0,0,99.9,89.9,0,0,0,0,28,5,88,'2018-04-20 14:55:48','2018-04-23 21:25:28');

/*Table structure for table `goods_detail` */

DROP TABLE IF EXISTS `goods_detail`;

CREATE TABLE `goods_detail` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goodsId` int(32) DEFAULT NULL,
  `sequence` int(8) NOT NULL DEFAULT '0',
  `content` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` tinyint(2) NOT NULL DEFAULT '2',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `goods_detail` */

insert  into `goods_detail`(`id`,`goodsId`,`sequence`,`content`,`type`) values (1,1,0,'http://img.leshare.shop/Fh4_7_BKLOw-kGaCO57c_r0UluK0',2),(2,1,1,'http://img.leshare.shop/FivqLKQXz2nFU4waQBvAHRBqHNVt',2),(3,100000,0,'http://img.leshare.shop/Fh4_7_BKLOw-kGaCO57c_r0UluK0',2),(4,100000,1,'http://img.leshare.shop/FivqLKQXz2nFU4waQBvAHRBqHNVt',2);

/*Table structure for table `goods_images` */

DROP TABLE IF EXISTS `goods_images`;

CREATE TABLE `goods_images` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goodsId` int(32) NOT NULL,
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `goods_images` */

insert  into `goods_images`(`id`,`goodsId`,`url`,`createTime`) values (1,1,'http://img.leshare.shop/FhhjJ66nbzHgfkNEJJBUKIAZe2hC','2018-04-19 11:06:00'),(2,1,'http://img.leshare.shop/Fv8una9ZmDgmJntkPDIbe5XNPu2f','2018-04-19 11:06:25'),(3,100000,'http://img.leshare.shop/Fv8una9ZmDgmJntkPDIbe5XNPu2f','2018-04-20 16:19:51'),(4,100000,'http://img.leshare.shop/FhhjJ66nbzHgfkNEJJBUKIAZe2hC','2018-04-20 16:01:45');

/*Table structure for table `goods_stocks` */

DROP TABLE IF EXISTS `goods_stocks`;

CREATE TABLE `goods_stocks` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goods_id` int(32) NOT NULL,
  `totalStock` int(8) NOT NULL,
  `salesVolume` int(8) NOT NULL DEFAULT '0',
  `stock` int(8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `goods_stocks` */

/*Table structure for table `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `goodsId` int(32) NOT NULL,
  `customerId` int(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `dealPrice` float NOT NULL,
  `finalPrice` float NOT NULL,
  `paymentType` tinyint(2) NOT NULL DEFAULT '1',
  `orderTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `paymentTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `couponUsedId` int(8) NOT NULL DEFAULT '0',
  `sellerNote` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `receiveName` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `receivePhone` int(11) NOT NULL,
  `shopId` int(8) DEFAULT '3',
  `shopName` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `postFee` float NOT NULL DEFAULT '0',
  `orderType` tinyint(2) NOT NULL DEFAULT '10',
  `arriveTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000002 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Data for the table `orders` */

insert  into `orders`(`id`,`goodsId`,`customerId`,`status`,`dealPrice`,`finalPrice`,`paymentType`,`orderTime`,`paymentTime`,`couponUsedId`,`sellerNote`,`address`,`receiveName`,`receivePhone`,`shopId`,`shopName`,`postFee`,`orderType`,`arriveTime`) values (10000000,100001,0,0,0,0,1,'2018-04-23 11:01:28','0000-00-00 00:00:00',0,NULL,'','',0,3,NULL,0,10,'0000-00-00 00:00:00'),(10000001,1,0,0,0,0,1,'2018-04-22 11:01:37','0000-00-00 00:00:00',0,NULL,'','',0,3,NULL,0,10,'0000-00-00 00:00:00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
