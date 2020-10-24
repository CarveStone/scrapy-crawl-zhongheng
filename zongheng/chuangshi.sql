CREATE DATABASE IF NOT EXISTS `zongheng`;

USE `zongheng`;


/*Table structure for table `xss` */

DROP TABLE IF EXISTS `novel`;

CREATE TABLE `novel` (
  `id` INT(11) NULL AUTO_INCREMENT,
  `novelName` VARCHAR(255) COLLATE utf8_bin NOT NULL UNIQUE,
  `author` VARCHAR(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*Data for the table `xss` */

/*Table structure for table `zjs` */

DROP TABLE IF EXISTS `chapter`;

CREATE TABLE `chapter` (
  `id` INT(11) NULL AUTO_INCREMENT,
  `chapterName` VARCHAR(255) COLLATE utf8_bin NOT NULL,
  `content` TEXT COLLATE utf8_bin NULL,
  `novelId` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_chapter` (`novelId`),
  CONSTRAINT `FK_chapter` FOREIGN KEY (`novelId`) REFERENCES `novel` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


DELETE FROM chapter;
DELETE FROM novel;
