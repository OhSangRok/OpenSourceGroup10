-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: school_event_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `buildings`
--

DROP TABLE IF EXISTS `buildings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildings` (
  `building_id` int NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) NOT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildings`
--

LOCK TABLES `buildings` WRITE;
/*!40000 ALTER TABLE `buildings` DISABLE KEYS */;
INSERT INTO `buildings` VALUES (1,'소프트웨어ICT관',37.3210000,127.1260000,'소프트웨어학과 건물'),(2,'혜당관',37.3220000,127.1270000,'강의 건물'),(3,'학생회관',37.3230000,127.1280000,'학생 편의시설');
/*!40000 ALTER TABLE `buildings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_schedules`
--

DROP TABLE IF EXISTS `bus_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `stop_id` int DEFAULT NULL,
  `bus_number` varchar(50) DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `weekday_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `stop_id` (`stop_id`),
  CONSTRAINT `bus_schedules_ibfk_1` FOREIGN KEY (`stop_id`) REFERENCES `bus_stops` (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_schedules`
--

LOCK TABLES `bus_schedules` WRITE;
/*!40000 ALTER TABLE `bus_schedules` DISABLE KEYS */;
INSERT INTO `bus_schedules` VALUES (1,1,'24번','08:10:00','weekday'),(2,1,'24번','08:30:00','weekday'),(3,1,'720-3번','08:20:00','weekday'),(4,2,'810번','09:00:00','weekday'),(5,2,'810번','09:20:00','weekday'),(6,1,'24번','23:50:00','weekday');
/*!40000 ALTER TABLE `bus_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_stops`
--

DROP TABLE IF EXISTS `bus_stops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_stops` (
  `stop_id` int NOT NULL AUTO_INCREMENT,
  `stop_name` varchar(100) NOT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_stops`
--

LOCK TABLES `bus_stops` WRITE;
/*!40000 ALTER TABLE `bus_stops` DISABLE KEYS */;
INSERT INTO `bus_stops` VALUES (1,'단국대.치과병원',37.3211000,127.1261000,'단국대학교 치과병원 앞 정류장'),(2,'단국대.종합실험동',37.3218000,127.1268000,'종합실험동 근처 정류장'),(3,'단국대.평화의광장',37.3225000,127.1275000,'평화의광장 근처 정류장'),(4,'단국대.인문관',37.3232000,127.1282000,'인문관 앞 정류장'),(5,'단국대정문',37.3240000,127.1290000,'단국대학교 정문 정류장'),(6,'단국대차고지',37.3250000,127.1300000,'단국대학교 차고지 정류장');
/*!40000 ALTER TABLE `bus_stops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text,
  `building_id` int DEFAULT NULL,
  `college` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `start_datetime` datetime DEFAULT NULL,
  `end_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `building_id` (`building_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'AI 세미나','AI 특강 진행',1,'소프트웨어융합대학','소프트웨어학과','2026-05-20 14:00:00','2026-05-20 16:00:00'),(2,'해커톤','팀 프로젝트 행사',2,'소프트웨어융합대학','컴퓨터공학과','2026-05-21 10:00:00','2026-05-21 18:00:00');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorite_events`
--

DROP TABLE IF EXISTS `favorite_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorite_events` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) NOT NULL,
  `event_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `student_id` (`student_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `favorite_events_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`student_id`),
  CONSTRAINT `favorite_events_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite_events`
--

LOCK TABLES `favorite_events` WRITE;
/*!40000 ALTER TABLE `favorite_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorite_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `student_id` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `college` varchar(50) NOT NULL,
  `department` varchar(50) NOT NULL,
  `grade` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('32253449','$2b$12$IjISqKx9ZfJNFlAyjMEqP.hutEw4b2zrYrAMgovIuSW8y2Z6kqo5G','이윤형','AI 융합대학','소프트웨어학과',2,'2026-05-11 06:30:32');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-27 18:56:30
