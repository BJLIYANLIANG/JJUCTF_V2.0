-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: jjuctf
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(30) NOT NULL,
  `admin_email` varchar(30) NOT NULL,
  `admin_mobile` varchar(20) NOT NULL,
  `admin_photo` varchar(300) DEFAULT NULL,
  `admin_password` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (12,'hsm','905008677@qq.com','18579266908',NULL,'6f8c33aa2d7257eb96a3852b32e9ac9a');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `challenge_list`
--

DROP TABLE IF EXISTS `challenge_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenge_list` (
  `challenge_id` int NOT NULL AUTO_INCREMENT,
  `challenge_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `challenge_score` int NOT NULL,
  `challenge_hint` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `challenge_type` int NOT NULL,
  `docker_flag` int NOT NULL,
  `docker_path` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `challenge_flag` int NOT NULL,
  `challenge_file` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Success_num` int DEFAULT NULL,
  PRIMARY KEY (`challenge_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `challenge_list`
--

LOCK TABLES `challenge_list` WRITE;
/*!40000 ALTER TABLE `challenge_list` DISABLE KEYS */;
INSERT INTO `challenge_list` VALUES (1,'easyPython',50,'SSTI漏洞',0,1,'EasyPython',0,NULL,NULL),(3,'easymisc',100,'简单的misc',1,0,NULL,0,NULL,NULL),(4,'easycrypto',50,'简单逆向',2,0,NULL,0,NULL,NULL),(7,'easypwn',100,'简单的PWN',4,0,NULL,0,NULL,NULL),(8,'easyReverse',150,'简单的逆向',3,0,NULL,0,NULL,NULL),(9,'hardreverse',150,'很难逆向',3,0,NULL,0,NULL,NULL),(10,'easyWeb',150,'easyWEB',0,0,NULL,0,NULL,NULL);
/*!40000 ALTER TABLE `challenge_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `Student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_name` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_age` int DEFAULT NULL,
  `Student_sex` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_email` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Student_part` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_pro` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`Student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_login`
--

DROP TABLE IF EXISTS `student_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_login` (
  `Student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_email` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Student_password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`Student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_login`
--

LOCK TABLES `student_login` WRITE;
/*!40000 ALTER TABLE `student_login` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `target`
--

DROP TABLE IF EXISTS `target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `target` (
  `tar_id` int NOT NULL,
  `tar_group_id` int NOT NULL DEFAULT '0',
  `tar_name` varchar(40) NOT NULL,
  `tar_hint` varchar(200) DEFAULT NULL,
  `tar_score` int NOT NULL,
  `tar_file_path` varchar(300) DEFAULT NULL,
  `tar_con_path` varchar(300) DEFAULT NULL,
  `user_id` int NOT NULL,
  `tar_cretime` date NOT NULL,
  PRIMARY KEY (`tar_id`),
  KEY `tar_con_path` (`tar_con_path`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `target`
--

LOCK TABLES `target` WRITE;
/*!40000 ALTER TABLE `target` DISABLE KEYS */;
INSERT INTO `target` VALUES (0,0,'upload_me','this hint',300,'file/backup.zip','web/uploadme',0,'2020-12-01'),(1,1,'this_misc','this misc',100,'file/misc/this_misc.zip',NULL,0,'2020-12-01'),(2,2,'Reverse1','Reverse1',300,'reverse/reverse.zip',NULL,0,'2020-12-31'),(3,3,'crypto','crypto',400,'file/crypto.zip',NULL,0,'2020-12-16');
/*!40000 ALTER TABLE `target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `target_run`
--

DROP TABLE IF EXISTS `target_run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `target_run` (
  `tar_run_id` int NOT NULL AUTO_INCREMENT,
  `tar_group` int NOT NULL,
  `tar_id` int NOT NULL,
  `tar_ip` varchar(200) NOT NULL,
  `tar_status` int NOT NULL DEFAULT '1',
  `tar_flag` varchar(100) NOT NULL,
  `create_user_id` int NOT NULL,
  `creat_time` date NOT NULL,
  PRIMARY KEY (`tar_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `target_run`
--

LOCK TABLES `target_run` WRITE;
/*!40000 ALTER TABLE `target_run` DISABLE KEYS */;
/*!40000 ALTER TABLE `target_run` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test1`
--

DROP TABLE IF EXISTS `test1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test1` (
  `id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test1`
--

LOCK TABLES `test1` WRITE;
/*!40000 ALTER TABLE `test1` DISABLE KEYS */;
INSERT INTO `test1` VALUES (1);
/*!40000 ALTER TABLE `test1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test2`
--

DROP TABLE IF EXISTS `test2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test2` (
  `id2` int DEFAULT NULL,
  KEY `id2` (`id2`),
  CONSTRAINT `test2_ibfk_1` FOREIGN KEY (`id2`) REFERENCES `test1` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test2`
--

LOCK TABLES `test2` WRITE;
/*!40000 ALTER TABLE `test2` DISABLE KEYS */;
/*!40000 ALTER TABLE `test2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) NOT NULL,
  `real_name` varchar(20) NOT NULL,
  `role` int NOT NULL,
  `status` int NOT NULL,
  `password` char(32) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile` char(11) DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `user_photo` varchar(200) DEFAULT NULL,
  `user_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (15,'20180201420','贺述明',1,1,'6f8c33aa2d7257eb96a3852b32e9ac9a','905008677@qq.com','18579266908',1861,'','hsm'),(16,'20180201421','张三',0,0,'e10adc3949ba59abbe56e057f20f883e','448843264@qq.com','15387721403',1861,'','zzh'),(17,'20180201421','张三',0,0,'e10adc3949ba59abbe56e057f20f883e','448843264@qq.com','15387721403',1861,'','admin'),(18,'12345','aaa',0,0,'594f803b380a41396ed63dca39503542','aaa@qq.com','123456789',1861,'','aaa');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlogin`
--

DROP TABLE IF EXISTS `userlogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userlogin` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `user_email` varchar(100) DEFAULT NULL,
  `user_password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlogin`
--

LOCK TABLES `userlogin` WRITE;
/*!40000 ALTER TABLE `userlogin` DISABLE KEYS */;
INSERT INTO `userlogin` VALUES (5,'hsm','905008677@qq.com','6f8c33aa2d7257eb96a3852b32e9ac9a'),(16,'llz','911324234@qq.com','6f8c33aa2d7257eb96a3852b32e9ac9a'),(20,'user','sadfds@gmail.com','e10adc3949ba59abbe56e057f20f883e'),(23,'zzh','12344@gmail.com','25d55ad283aa400af464c76d713c07ad'),(24,'hello','dsafs@qq.com','e10adc3949ba59abbe56e057f20f883e'),(25,'fsadfsad','11sdaf@qa.cc','275721264bf7e5b013614bf6ca59629e');
/*!40000 ALTER TABLE `userlogin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-19 13:20:06
