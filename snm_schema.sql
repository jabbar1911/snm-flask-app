-- Smart Note Management (SNM) Database Schema
-- Optimized for MySQL 8.0+ (Tested on Aiven MySQL)

/* 
   🚀 HOW TO USE WITH AIVEN:
   1. Log in to Aiven Console (console.aiven.io)
   2. Select your MySQL Service
   3. Click on "Query Editor" (left sidebar)
   4. Copy and paste ALL the code below into the editor
   5. Click "Run" or "Execute"
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------
-- Table structure for table `users`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `userid` int unsigned NOT NULL AUTO_INCREMENT,
  `username` TEXT NOT NULL,
  `useremail` varchar(100) NOT NULL,
  `userpassword` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `useremail` (`useremail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ------------------------------------------------------
-- Table structure for table `notesdata`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `notesdata`;
CREATE TABLE `notesdata` (
  `notesid` int unsigned NOT NULL AUTO_INCREMENT,
  `notestitle` varchar(100) NOT NULL,
  `notescontent` longtext,
  `userid` int unsigned NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notesid`),
  KEY `userid` (`userid`),
  CONSTRAINT `notesdata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ------------------------------------------------------
-- Table structure for table `filesdata`
-- ------------------------------------------------------
DROP TABLE IF EXISTS `filesdata`;
CREATE TABLE `filesdata` (
  `fileid` int unsigned NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `filecontent` longblob,
  `userid` int unsigned NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fileid`),
  KEY `userid` (`userid`),
  CONSTRAINT `filesdata_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
