SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `doclab` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `doclab`;

CREATE TABLE `authors` (
  `id` int(11) UNSIGNED NOT NULL,
  `url` text,
  `last_crawl` date DEFAULT NULL,
  `locked` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `dictionary` (
  `id` int(11) UNSIGNED NOT NULL,
  `document_id` int(11) NOT NULL,
  `term` tinytext NOT NULL,
  `term_frequency` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `url` text NOT NULL,
  `content` longtext,
  `last_crawl` date DEFAULT NULL,
  `locked` tinyint(1) NOT NULL DEFAULT '0',
  `indexed` tinyint(1) DEFAULT '0',
  `index_locked` tinyint(1) DEFAULT '0',
  `title` mediumtext,
  `description` mediumtext,
  `authors` json DEFAULT NULL,
  `topic` varchar(20) DEFAULT '',
  `screenshot` varchar(35) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `authors`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `dictionary`
  ADD PRIMARY KEY (`id`),
  ADD KEY `document_id` (`document_id`);

ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `documents` ADD FULLTEXT KEY `title` (`title`,`description`);


ALTER TABLE `authors`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `dictionary`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `dictionary`
  ADD CONSTRAINT `dictionary_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`);
