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
INSERT INTO `Message` VALUES (1,'oQDEJuHL_iXI3C_qmMKeZhIN2RaQ','ä½ å¥½',1,now(),now());
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
