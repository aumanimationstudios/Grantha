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
INSERT INTO `DESCRIPTION` VALUES (''),('1TB-Blue'),('4GB-GT730'),('8GB-DDR3'),('One');
/*!40000 ALTER TABLE `DESCRIPTION` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ITEMS`
--

LOCK TABLES `ITEMS` WRITE;
/*!40000 ALTER TABLE `ITEMS` DISABLE KEYS */;
INSERT INTO `ITEMS` VALUES (1,'AOCJV26H2100067','MONITOR','','AOC','i2269VM',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(2,'1801SY09PG18','KEYBOARD','','LOGITECH','Y-U0011',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(3,'7CH3411077','MOUSE','','HP','A3P',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(4,'WCC6Y4KKTD43','HARD_DISK','1TB-Blue','WD','WD10EZEX',0.00,'2017-05-05','0000-00-00','blue0030',''),(5,'N170800019871','GRAPHICS_CARD','4GB-GT730','ZOTAC','ZT-7115-20L',0.00,'2017-05-05','0000-00-00','blue0030',''),(6,'165103339335958','RAM','8GB-DDR3','CORSAIR','VENGEANCE',0.00,'2017-05-05','0000-00-00','blue0030',''),(7,'165103339336047','RAM','8GB-DDR3','CORSAIR','VENGEANCE',0.00,'2017-05-05','0000-00-00','blue0030',''),(8,'I3FRCVPD0P','HEADPHONE','','PHILIPS','SHP1900',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(9,'123','RAM','','','',12300.00,'0000-00-00','0000-00-00','REPAIR',''),(15,'111','SMPS','test','ABC','abc',15000.00,'2018-08-14','0000-00-00','aum_r01_workspace_05','sanath.shetty'),(17,'1','SMPS','','','',0.00,'0000-00-00','0000-00-00','','syamkumar.sasidharan'),(43,'7LE00L1017685','PEN_TABLET','One','WACOM','CTL-472',0.00,'0000-00-00','0000-00-00','aum_r01_workspace_03',''),(71,'11223344','CABLE','1TB-Blue','AOC','CTL-472',999.00,'2018-11-17','2018-11-17','aum_r01_stock01','shiva');
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
INSERT INTO `ITEM_TYPE` VALUES ('CABLE'),('GRAPHICS_CARD'),('HARD_DISK'),('HEADPHONE'),('KEYBOARD'),('MONITOR'),('MOUSE'),('PEN_DISPLAY'),('PEN_TABLET'),('RAM'),('SMPS');
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
INSERT INTO `LOCATION` VALUES ('',NULL),('aum_r01_stock01',NULL),('aum_r01_workspace_01',NULL),('aum_r01_workspace_02',NULL),('aum_r01_workspace_03',NULL),('aum_r01_workspace_04',NULL),('aum_r01_workspace_05',NULL),('aum_r01_workspace_06',NULL),('aum_r01_workspace_07',NULL),('aum_r01_workspace_08',NULL),('aum_r01_workspace_09',NULL),('aum_r01_workspace_10',NULL),('aum_r02_stock01',NULL),('aum_r02_workspace_M01',NULL),('aum_r02_workspace_pA1',NULL),('aum_r02_workspace_pA10',NULL),('aum_r02_workspace_pA2',NULL),('aum_r02_workspace_pA3',NULL),('aum_r02_workspace_pA4',NULL),('aum_r02_workspace_pA5',NULL),('aum_r02_workspace_pA6',NULL),('aum_r02_workspace_pA7',NULL),('aum_r02_workspace_pA8',NULL),('aum_r02_workspace_pA9',NULL),('aum_r02_workspace_pB1',NULL),('aum_r02_workspace_pB2',NULL),('aum_r02_workspace_pB3',NULL),('aum_r02_workspace_pB4',NULL),('aum_r02_workspace_pB5',NULL),('aum_r02_workspace_pB6',NULL),('aum_r02_workspace_pB7',NULL),('aum_r02_workspace_pB8',NULL),('aum_r02_workspace_pC1',NULL),('aum_r02_workspace_pC2',NULL),('aum_r02_workspace_pC3',NULL),('aum_r02_workspace_pC4',NULL),('aum_r02_workspace_pC5',NULL),('aum_r02_workspace_pC6',NULL),('aum_r02_workspace_pC7',NULL),('aum_r02_workspace_pC8',NULL),('aum_r02_workspace_pC9',NULL),('aum_r03_stock01',NULL),('blue0030','aum_r01_workspace_03'),('REPAIR',NULL);
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
INSERT INTO `MAKE` VALUES (''),('AOC'),('BENQ'),('CASIO'),('CORSAIR'),('DELL'),('HP'),('LOGITECH'),('PHILIPS'),('VIEWSONIC'),('WACOM'),('WD'),('ZOTAC');
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
INSERT INTO `MODEL` VALUES (''),('A3P'),('CTL-472'),('i2269VM'),('SHP1900'),('VENGEANCE'),('WD10EZEX'),('Y-U0011'),('ZT-7115-20L');
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
  PRIMARY KEY (`serial_no`),
  UNIQUE KEY `serial_no_UNIQUE` (`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SERIAL_NO`
--

LOCK TABLES `SERIAL_NO` WRITE;
/*!40000 ALTER TABLE `SERIAL_NO` DISABLE KEYS */;
INSERT INTO `SERIAL_NO` VALUES ('1'),('111'),('11223344'),('123'),('165103339335958'),('165103339336047'),('1801SY09PG18'),('7CH3411077'),('7LE00L1017685'),('AOCJV26H2100067'),('I3FRCVPD0P'),('N170800019871'),('WCC6Y4KKTD43');
/*!40000 ALTER TABLE `SERIAL_NO` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UPDATE_LOG`
--

LOCK TABLES `UPDATE_LOG` WRITE;
/*!40000 ALTER TABLE `UPDATE_LOG` DISABLE KEYS */;
INSERT INTO `UPDATE_LOG` VALUES (1,'2018-08-02 14:40:22.000000','7CH3411077','aum_r01_workspace_03','aum_r01_workspace_04',''),(2,'2018-08-02 14:41:51.000000','7CH3411077','aum_r01_workspace_04','aum_r01_workspace_03',''),(3,'2018-08-04 15:33:07.000000','1801SY09PG18','aum_r01_workspace_03','aum_r01_workspace_04',''),(4,'2018-08-04 15:46:06.000000','1801SY09PG18','aum_r01_workspace_04','aum_r01_workspace_03',''),(5,'2018-08-04 15:57:17.000000','I3FRCVPD0P','aum_r01_workspace_03','aum_r01_workspace_04','sanath.shetty'),(6,'2018-08-04 15:58:21.000000','I3FRCVPD0P','aum_r01_workspace_04','aum_r01_workspace_03','sanath.shetty'),(7,'2018-08-08 14:50:24.000000','123','aum_r02_workspace_pC8','aum_r02_workspace_pC9','sanath.shetty'),(8,'2018-08-08 15:05:23.000000','123','aum_r02_workspace_pC9','REPAIR','sanath.shetty'),(9,'2018-08-14 17:38:18.000000','111','aum_r02_workspace_pC7','aum_r02_workspace_pB4','sanath.shetty'),(10,'2018-09-22 13:07:16.000000','111','aum_r02_workspace_pB8','aum_r01_workspace_05','sanath.shetty');
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

-- Dump completed on 2018-12-08 12:21:11
