-- MySQL dump 10.13  Distrib 5.5.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: WeChatTest
-- ------------------------------------------------------
-- Server version	5.5.49-0ubuntu0.14.04.1

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
-- Table structure for table `ChatPair`
--

DROP TABLE IF EXISTS `ChatPair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ChatPair` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `FromID` varchar(100) NOT NULL,
  `ToID` varchar(100) NOT NULL,
  `status` int(11) NOT NULL,
  `isScored` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ChatPair`
--

LOCK TABLES `ChatPair` WRITE;
/*!40000 ALTER TABLE `ChatPair` DISABLE KEYS */;
INSERT INTO `ChatPair` VALUES (5,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','oQDEJuMkre6P9Hs6zOEuxMla7s_E',1,0),(6,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','oQDEJuHL_iXI3C_qmMKeZhIN2RaQ',1,0),(7,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','oQDEJuHL_iXI3C_qmMKeZhIN2RaQ',1,0),(8,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','oQDEJuMkre6P9Hs6zOEuxMla7s_E',1,0);
/*!40000 ALTER TABLE `ChatPair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Message`
--

DROP TABLE IF EXISTS `Message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ReceiveID` varchar(100) NOT NULL,
  `msg` text,
  `isSend` int(11) NOT NULL,
  `FromSenderTime` datetime DEFAULT NULL,
  `ToReceiverTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=529 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Message`
--

LOCK TABLES `Message` WRITE;
/*!40000 ALTER TABLE `Message` DISABLE KEYS */;
INSERT INTO `Message` VALUES (493,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','ä½ å¥½',1,'2016-07-21 21:18:32','2016-07-21 21:18:55'),(494,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','æœ‰äººå—',1,'2016-07-21 21:18:34','2016-07-21 21:18:55'),(495,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','æœ‰äººå—',1,'2016-07-21 21:18:55','2016-07-21 21:18:59'),(496,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','ä½ å¥½',1,'2016-07-21 21:18:59','2016-07-21 21:23:11'),(497,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','æˆ‘æ˜¯å°ç±³',1,'2016-07-21 21:23:01','2016-07-21 21:23:11'),(498,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','æˆ‘æ˜¯å°çŽ‹',1,'2016-07-21 21:23:11','2016-07-22 11:47:26'),(499,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','æœ‰7å“¦å“¦',1,'2016-07-22 11:20:27','2016-07-22 11:47:26'),(500,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','644',1,'2016-07-22 11:47:26','2016-07-22 12:00:12'),(501,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','644ç‚¹',1,'2016-07-22 11:47:30','2016-07-22 12:00:12'),(502,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:47:34','2016-07-22 12:00:12'),(503,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:49:50','2016-07-22 12:00:12'),(504,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:51:15','2016-07-22 12:00:12'),(505,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:52:01','2016-07-22 12:00:12'),(506,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:54:08','2016-07-22 12:00:12'),(507,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:54:41','2016-07-22 12:00:12'),(508,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:55:41','2016-07-22 12:00:12'),(509,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:57:00','2016-07-22 12:00:12'),(510,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:58:57','2016-07-22 12:00:12'),(511,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',1,'2016-07-22 11:59:52','2016-07-22 12:00:12'),(512,'oQDEJuMkre6P9Hs6zOEuxMla7s_E','æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿(é¦™å±±è·¯åŒ—)',1,'2016-07-22 12:00:12','2016-07-22 12:00:50'),(513,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:00:50',NULL),(514,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','ä½ å¥½',0,'2016-07-22 12:02:45',NULL),(515,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:05:00',NULL),(516,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:08:28',NULL),(517,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:10:26',NULL),(518,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','å“ˆå–½',0,'2016-07-22 12:10:37',NULL),(519,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:11:32',NULL),(520,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:12:23',NULL),(521,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:14:43',NULL),(522,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','ä½ å¥½',0,'2016-07-22 12:14:59',NULL),(523,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:15:05',NULL),(524,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:15:54',NULL),(525,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:18:27',NULL),(526,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:19:22',NULL),(527,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:20:30',NULL),(528,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','åŒ—äº¬å¸‚æµ·æ·€åŒºåŒ—äº¬å¸‚è¥¿å±±è¯•éªŒæž—åœºè¥¿å—(é¦™å±±è·¯åŒ—)',0,'2016-07-22 12:22:00',NULL);
/*!40000 ALTER TABLE `Message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` varchar(100) NOT NULL,
  `sex` tinyint(4) DEFAULT '100',
  `longitude` float NOT NULL,
  `lantitude` float NOT NULL,
  `city` varchar(400) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'start',100,10.24,10.24,'北京');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Info`
--

DROP TABLE IF EXISTS `User_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_Info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` varchar(100) NOT NULL,
  `isLogin` int(11) NOT NULL,
  `isChat` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `score` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Info`
--

LOCK TABLES `User_Info` WRITE;
/*!40000 ALTER TABLE `User_Info` DISABLE KEYS */;
INSERT INTO `User_Info` VALUES (1,'start',1,1,'Start',0),(2,'start',1,1,'Start',0),(38,'oQDEJuMkre6P9Hs6zOEuxMla7s_E',1,0,'nobody',0),(39,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ',0,0,'nobody',0);
/*!40000 ALTER TABLE `User_Info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WeChatLog`
--

DROP TABLE IF EXISTS `WeChatLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WeChatLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userID` varchar(100) NOT NULL,
  `msg` text,
  `Time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WeChatLog`
--

LOCK TABLES `WeChatLog` WRITE;
/*!40000 ALTER TABLE `WeChatLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `WeChatLog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-24 17:51:23
