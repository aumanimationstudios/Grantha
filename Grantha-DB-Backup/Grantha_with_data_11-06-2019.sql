-- MySQL dump 10.13  Distrib 5.6.41, for Linux (x86_64)
--
-- Host: localhost    Database: INVENTORY
-- ------------------------------------------------------
-- Server version	5.6.41-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AUTH_USERS`
--

DROP TABLE IF EXISTS `AUTH_USERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AUTH_USERS` (
  `auth_users` varchar(100) NOT NULL,
  PRIMARY KEY (`auth_users`),
  UNIQUE KEY `auth_users_UNIQUE` (`auth_users`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AUTH_USERS`
--

LOCK TABLES `AUTH_USERS` WRITE;
/*!40000 ALTER TABLE `AUTH_USERS` DISABLE KEYS */;
INSERT INTO `AUTH_USERS` VALUES ('sanath.shetty');
/*!40000 ALTER TABLE `AUTH_USERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DESCRIPTION`
--

DROP TABLE IF EXISTS `DESCRIPTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DESCRIPTION` (
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DESCRIPTION`
--

LOCK TABLES `DESCRIPTION` WRITE;
/*!40000 ALTER TABLE `DESCRIPTION` DISABLE KEYS */;
INSERT INTO `DESCRIPTION` VALUES (''),('1TB-Blue'),('1TB-Purple'),('21.5-inch-Monitor'),('2GB-DDR3'),('2GB-GT610'),('4GB-DDR3'),('4GB-GT730'),('4GB-GTX970'),('600W'),('8GB-DDR3'),('Hydro-Series-H80'),('One');
/*!40000 ALTER TABLE `DESCRIPTION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `IMAGES`
--

DROP TABLE IF EXISTS `IMAGES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IMAGES` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_UNIQUE` (`image`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `IMAGES`
--

LOCK TABLES `IMAGES` WRITE;
/*!40000 ALTER TABLE `IMAGES` DISABLE KEYS */;
INSERT INTO `IMAGES` VALUES (9,'/crap/crap.server/image09.jpeg'),(5,'/crap/crap.server/image10.jpeg'),(14,'/crap/crap.server/image11.jpeg'),(3,'/crap/crap.server/image14.jpeg'),(4,'/crap/crap.server/Kuppi.jpg');
/*!40000 ALTER TABLE `IMAGES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ITEMS`
--

DROP TABLE IF EXISTS `ITEMS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ITEMS` (
  `item_id` int(50) NOT NULL AUTO_INCREMENT,
  `serial_no` varchar(100) NOT NULL,
  `item_type` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `make` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  `price` decimal(13,2) NOT NULL,
  `purchased_on` date NOT NULL,
  `warranty_valid_till` date NOT NULL,
  `location` varchar(100) NOT NULL,
  `user` varchar(100) NOT NULL,
  PRIMARY KEY (`item_id`),
  UNIQUE KEY `serial_no_UNIQUE` (`serial_no`),
  KEY `item_type_idx` (`item_type`),
  KEY `location_idx` (`location`),
  KEY `user_idx` (`user`),
  CONSTRAINT `item_type` FOREIGN KEY (`item_type`) REFERENCES `ITEM_TYPE` (`item_type`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `location` FOREIGN KEY (`location`) REFERENCES `LOCATION` (`location`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user` FOREIGN KEY (`user`) REFERENCES `USER` (`user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ITEMS`
--

LOCK TABLES `ITEMS` WRITE;
/*!40000 ALTER TABLE `ITEMS` DISABLE KEYS */;
INSERT INTO `ITEMS` VALUES (1,'AOCJV26H2100067','MONITOR','','AOC','i2269VM',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(2,'1801SY09PG18','KEYBOARD','','LOGITECH','Y-U0011',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(3,'7CH3411077','MOUSE','','HP','A3P',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_04','jayaram'),(4,'WCC6Y4KKTD43','HARD_DISK','1TB-Blue','WD','WD10EZEX',0.00,'2017-05-05','0000-00-00','blue0030',''),(5,'N170800019871','GRAPHICS_CARD','4GB-GT730','ZOTAC','ZT-7115-20L',0.00,'2017-05-05','0000-00-00','blue0030',''),(6,'165103339335958','RAM','8GB-DDR3','CORSAIR','VENGEANCE',0.00,'2017-05-05','0000-00-00','blue0030',''),(7,'165103339336047','RAM','8GB-DDR3','CORSAIR','VENGEANCE',0.00,'2017-05-05','0000-00-00','blue0030',''),(8,'I3FRCVPD0P','HEADPHONE','','PHILIPS','SHP1900',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(9,'123','RAM','','','',12300.00,'0000-00-00','0000-00-00','REPAIR','rama'),(15,'111','SMPS','test','ABC','abc',303.00,'2018-08-14','0000-00-00','aum_r01_workspace_03','shrinidhi'),(17,'1','SMPS','','','',0.00,'0000-00-00','0000-00-00','','syamkumar.sasidharan'),(43,'7LE00L1017685','PEN_TABLET','One','WACOM','CTL-472',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(71,'11223344','CABLE','1TB-Blue','AOC','CTL-472',999.00,'2018-11-17','2018-11-17','aum_r01_stock01','shiva'),(73,'AOCJV26H2100057','MONITOR','','AOC','i2269VM',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(74,'E1CVCM016713','GRAPHICS_CARD','2GB-GT610','ASUS','SL-2GD3-L',0.00,'0000-00-00','0000-00-00','OUTDATED',''),(76,'N153900032554','GRAPHICS_CARD','4GB-GTX970','ZOTAC','ZT-90101-10P',55000.00,'2016-07-06','0000-00-00','blue0666old',''),(77,'WCC4J6ZC3689','HARD_DISK','1TB-Purple','WD','WD10PURX',3600.00,'2016-05-18','0000-00-00','blue0666old',''),(78,'RS600ACABD31142401484','SMPS','600W','COOLER MASTER','THUNDER600W',5500.00,'0000-00-00','0000-00-00','blue0666old',''),(79,'XLLPVU98MJUNXRFB','RAM','8GB-DDR3','HYPERX','HX316C10F/8',4000.00,'2016-05-18','0000-00-00','blue0012',''),(80,'QTLAMK9KM58HX7Q6','RAM','8GB-DDR3','HYPERX','HX318C10FR/8',4000.00,'2016-05-18','0000-00-00','blue0666old',''),(81,'431419113403978','RAM','4GB-DDR3','CORSAIR','CMZ4GX3M1A1600C9',2600.00,'0000-00-00','0000-00-00','blue0666old',''),(82,'300626114706801','RAM','4GB-DDR3','CORSAIR','CMZ4GX3M1A1600C9',2600.00,'0000-00-00','0000-00-00','blue0666old',''),(83,'001CWE11249402','CPU_COOLER','Hydro-Series-H80','CORSAIR','CWCH80',7000.00,'0000-00-00','0000-00-00','blue0666old',''),(84,'AOCJV26H2100109','MONITOR','21.5-inch-Monitor','AOC','I2269VWM',10000.00,'0000-00-00','0000-00-00','blue0666old',''),(85,'867893-0403','KEYBOARD','','LOGITECH','Y-SAH83',600.00,'0000-00-00','0000-00-00','blue0666old',''),(86,'5397024639','RAM','2GB-DDR3','TRANSCEND','1333-DIMM-CL9',1400.00,'0000-00-00','0000-00-00','blue0026',''),(87,'5397023961','RAM','2GB-DDR3','TRANSCEND','1333-DIMM-CL9',1400.00,'0000-00-00','0000-00-00','blue0026','');
/*!40000 ALTER TABLE `ITEMS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ITEM_TYPE`
--

DROP TABLE IF EXISTS `ITEM_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ITEM_TYPE` (
  `item_type` varchar(100) NOT NULL,
  PRIMARY KEY (`item_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ITEM_TYPE`
--

LOCK TABLES `ITEM_TYPE` WRITE;
/*!40000 ALTER TABLE `ITEM_TYPE` DISABLE KEYS */;
INSERT INTO `ITEM_TYPE` VALUES ('CABLE'),('CPU_COOLER'),('GRAPHICS_CARD'),('HARD_DISK'),('HEADPHONE'),('KEYBOARD'),('MONITOR'),('MOTHERBOARD'),('MOUSE'),('PEN_DISPLAY'),('PEN_TABLET'),('RAM'),('SMPS');
/*!40000 ALTER TABLE `ITEM_TYPE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOCATION`
--

DROP TABLE IF EXISTS `LOCATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LOCATION` (
  `location` varchar(100) NOT NULL,
  `parent_location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOCATION`
--

LOCK TABLES `LOCATION` WRITE;
/*!40000 ALTER TABLE `LOCATION` DISABLE KEYS */;
INSERT INTO `LOCATION` VALUES ('',''),('aum_r01_stock01',NULL),('aum_r01_workspace_01',NULL),('aum_r01_workspace_02',NULL),('aum_r01_workspace_03',NULL),('aum_r01_workspace_04',NULL),('aum_r01_workspace_05',NULL),('aum_r01_workspace_06',NULL),('aum_r01_workspace_07',NULL),('aum_r01_workspace_08',NULL),('aum_r01_workspace_09',NULL),('aum_r01_workspace_10',NULL),('aum_r02_stock01',NULL),('aum_r02_workspace_M01',NULL),('aum_r02_workspace_pA1',NULL),('aum_r02_workspace_pA10',NULL),('aum_r02_workspace_pA2',NULL),('aum_r02_workspace_pA3',NULL),('aum_r02_workspace_pA4',NULL),('aum_r02_workspace_pA5',NULL),('aum_r02_workspace_pA6',NULL),('aum_r02_workspace_pA7',NULL),('aum_r02_workspace_pA8',NULL),('aum_r02_workspace_pA9',NULL),('aum_r02_workspace_pB1',NULL),('aum_r02_workspace_pB2',NULL),('aum_r02_workspace_pB3',NULL),('aum_r02_workspace_pB4',NULL),('aum_r02_workspace_pB5',NULL),('aum_r02_workspace_pB6',NULL),('aum_r02_workspace_pB7',NULL),('aum_r02_workspace_pB8',NULL),('aum_r02_workspace_pC1',NULL),('aum_r02_workspace_pC2',NULL),('aum_r02_workspace_pC3',NULL),('aum_r02_workspace_pC4',NULL),('aum_r02_workspace_pC5',NULL),('aum_r02_workspace_pC6',NULL),('aum_r02_workspace_pC7',NULL),('aum_r02_workspace_pC8',NULL),('aum_r02_workspace_pC9',NULL),('aum_r03_stock01',NULL),('blue0003','aum_r02_workspace_pC6'),('blue0004','aum_r02_workspace_pB2'),('blue0006','aum_r02_workspace_pA3'),('blue0007','aum_r02_workspace_pB4'),('blue0008','aum_r02_workspace_pC1'),('blue0009','aum_r02_workspace_pC8'),('blue0010','aum_r02_workspace_pA2'),('blue0011','aum_r01_workspace_06'),('blue0012','aum_r02_workspace_pA1'),('blue0014','aum_r02_workspace_pC9'),('blue0015','aum_r01_workspace_07'),('blue0016','aum_r02_workspace_pB3'),('blue0017','aum_r02_workspace_pB1'),('blue0018','aum_r02_workspace_pA6'),('blue0019','aum_r02_workspace_pB8'),('blue0020','aum_r02_workspace_pA10'),('blue0021','aum_r02_workspace_pC4'),('blue0022','aum_r01_workspace_10'),('blue0023','aum_r02_workspace_pA9'),('blue0024','aum_r02_workspace_pA5'),('blue0025','aum_r02_workspace_pC2'),('blue0026','aum_r01_workspace_02'),('blue0028','aum_r02_workspace_pC5'),('blue0029','aum_r01_workspace_04'),('blue0030','aum_r01_workspace_03'),('blue0031','aum_r02_workspace_pB6'),('blue0032','aum_r02_workspace_pA7'),('blue0033','aum_r02_workspace_pB7'),('blue0034','aum_r02_workspace_pC3'),('blue0035','aum_r01_workspace_08'),('blue0036','aum_r02_workspace_pA4'),('blue0037','aum_r02_workspace_pB5'),('blue0038','aum_r01_workspace_09'),('blue0039','aum_r02_workspace_pA8'),('blue0040','aum_r01_workspace_05'),('blue0666','aum_r02_workspace_pC7'),('blue0666old','aum_r03_stock01'),('OUTDATED',NULL),('REPAIR',NULL);
/*!40000 ALTER TABLE `LOCATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MAKE`
--

DROP TABLE IF EXISTS `MAKE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MAKE` (
  `make` varchar(100) NOT NULL,
  PRIMARY KEY (`make`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MAKE`
--

LOCK TABLES `MAKE` WRITE;
/*!40000 ALTER TABLE `MAKE` DISABLE KEYS */;
INSERT INTO `MAKE` VALUES (''),('AOC'),('ASUS'),('BENQ'),('CASIO'),('COOLER MASTER'),('CORSAIR'),('DELL'),('HP'),('HYPERX'),('LOGITECH'),('PHILIPS'),('TRANSCEND'),('VIEWSONIC'),('WACOM'),('WD'),('ZOTAC');
/*!40000 ALTER TABLE `MAKE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MODEL`
--

DROP TABLE IF EXISTS `MODEL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MODEL` (
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MODEL`
--

LOCK TABLES `MODEL` WRITE;
/*!40000 ALTER TABLE `MODEL` DISABLE KEYS */;
INSERT INTO `MODEL` VALUES (''),('1333-DIMM-CL9'),('A3P'),('CMZ4GX3M1A1600C9'),('CTL-472'),('CWCH80'),('HX316C10F/8'),('HX318C10FR/8'),('i2269VM'),('I2269VWM'),('SHP1900'),('SL-2GD3-L'),('THUNDER600W'),('VENGEANCE'),('WD10EZEX'),('WD10PURX'),('Y-SAH83'),('Y-U0011'),('ZT-7115-20L'),('ZT-90101-10P');
/*!40000 ALTER TABLE `MODEL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SERIAL_NO`
--

DROP TABLE IF EXISTS `SERIAL_NO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SERIAL_NO` (
  `serial_no` varchar(100) NOT NULL,
  `tag_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`serial_no`),
  UNIQUE KEY `tag_id_UNIQUE` (`tag_id`),
  KEY `fk_SERIAL_NO_1_idx` (`tag_id`),
  CONSTRAINT `fk_SERIAL_NO_1` FOREIGN KEY (`tag_id`) REFERENCES `TAG_ID` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SERIAL_NO`
--

LOCK TABLES `SERIAL_NO` WRITE;
/*!40000 ALTER TABLE `SERIAL_NO` DISABLE KEYS */;
INSERT INTO `SERIAL_NO` VALUES ('1',NULL),('111',NULL),('11223344',NULL),('123',NULL),('165103339335958',NULL),('165103339336047',NULL),('7CH3411077',NULL),('7LE00L1017685',NULL),('AOCJV26H2100067',NULL),('N170800019871','00000007'),('WCC6Y4KKTD43','00000008'),('1801SY09PG18','00000009'),('AOCJV26H2100057','00000010'),('431419113403978','2F6A0292'),('I3FRCVPD0P','6AD2373F'),('AOCJV26H2100109','72C32E26'),('WCC4J6ZC3689','736712E4'),('RS600ACABD31142401484','812D22E3'),('867893-0403','85FB3971'),('001CWE11249402','8DCAC5A5'),('QTLAMK9KM58HX7Q6','9FFCD2A1'),('XLLPVU98MJUNXRFB','B3F81D46'),('300626114706801','BB2254D9'),('E1CVCM016713','E6A6476C'),('5397024639','E78AB025'),('5397023961','EFD685AA'),('N153900032554','F0220F20');
/*!40000 ALTER TABLE `SERIAL_NO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TAG_ID`
--

DROP TABLE IF EXISTS `TAG_ID`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TAG_ID` (
  `id` varchar(64) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '1' COMMENT '1 = Active, 0 = Inactive',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TAG_ID`
--

LOCK TABLES `TAG_ID` WRITE;
/*!40000 ALTER TABLE `TAG_ID` DISABLE KEYS */;
INSERT INTO `TAG_ID` VALUES ('00000002',0),('00000007',1),('00000008',1),('00000009',1),('00000010',1),('2F6A0292',1),('6AD2373F',1),('72C32E26',1),('736712E4',1),('812D22E3',1),('85FB3971',1),('8DCAC5A5',1),('9FFCD2A1',1),('B3F81D46',1),('BB2254D9',1),('E6A6476C',1),('E78AB025',1),('EFD685AA',1),('F0220F20',1);
/*!40000 ALTER TABLE `TAG_ID` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UPDATE_LOG`
--

DROP TABLE IF EXISTS `UPDATE_LOG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UPDATE_LOG` (
  `no` int(45) NOT NULL AUTO_INCREMENT,
  `date_time` datetime(6) NOT NULL,
  `serial_no` varchar(100) NOT NULL,
  `old_location` varchar(100) NOT NULL,
  `new_location` varchar(100) NOT NULL,
  `updated_by` varchar(100) NOT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UPDATE_LOG`
--

LOCK TABLES `UPDATE_LOG` WRITE;
/*!40000 ALTER TABLE `UPDATE_LOG` DISABLE KEYS */;
INSERT INTO `UPDATE_LOG` VALUES (1,'2018-08-02 14:40:22.000000','7CH3411077','aum_r01_workspace_03','aum_r01_workspace_04',''),(2,'2018-08-02 14:41:51.000000','7CH3411077','aum_r01_workspace_04','aum_r01_workspace_03',''),(3,'2018-08-04 15:33:07.000000','1801SY09PG18','aum_r01_workspace_03','aum_r01_workspace_04',''),(4,'2018-08-04 15:46:06.000000','1801SY09PG18','aum_r01_workspace_04','aum_r01_workspace_03',''),(5,'2018-08-04 15:57:17.000000','I3FRCVPD0P','aum_r01_workspace_03','aum_r01_workspace_04','sanath.shetty'),(6,'2018-08-04 15:58:21.000000','I3FRCVPD0P','aum_r01_workspace_04','aum_r01_workspace_03','sanath.shetty'),(7,'2018-08-08 14:50:24.000000','123','aum_r02_workspace_pC8','aum_r02_workspace_pC9','sanath.shetty'),(8,'2018-08-08 15:05:23.000000','123','aum_r02_workspace_pC9','REPAIR','sanath.shetty'),(9,'2018-08-14 17:38:18.000000','111','aum_r02_workspace_pC7','aum_r02_workspace_pB4','sanath.shetty'),(10,'2018-09-22 13:07:16.000000','111','aum_r02_workspace_pB8','aum_r01_workspace_05','sanath.shetty'),(11,'2019-01-02 09:19:39.000000','7CH3411077','aum_r01_workspace_03','aum_r01_workspace_04','sanath.shetty');
/*!40000 ALTER TABLE `UPDATE_LOG` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USER` (
  `user` varchar(100) NOT NULL,
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (''),('akadam'),('avittal'),('bnag'),('gokul.gs'),('gprasad'),('gsanadi'),('harshith.shetty'),('jayaram'),('karthik.r'),('lokanath.s'),('navaraj'),('nsomakiran'),('ppaul'),('pradeep.shakthinagar'),('racharya'),('rama'),('roopesh.poojary'),('rshetty'),('sanath.shetty'),('sbangera'),('shashanka.shetty'),('shiva'),('shravan.kl'),('shrinidhi'),('skulal'),('sshetty'),('suhas'),('syamkumar.sasidharan'),('ujwal.kb'),('vivek');
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-11 10:35:16
