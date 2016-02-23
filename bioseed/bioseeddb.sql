-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2015 at 04:41 AM
-- Server version: 5.5.43-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `bioseeddb`
--

DROP DATABASE IF EXISTS bioseeddb;
CREATE DATABASE bioseeddb;
USE bioseeddb;

-- --------------------------------------------------------

--
-- Table structure for table `contributor`
--

CREATE TABLE IF NOT EXISTS `contributor` (
  `contributor_id` varchar(45) NOT NULL,
  `phone` int(11) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`contributor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE IF NOT EXISTS `role` (
  `admin` int(11) DEFAULT NULL,
  `privileged` int(11) DEFAULT NULL,
  `base` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `seed_stock`
--

CREATE TABLE IF NOT EXISTS `seed_stock` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  `stock_id` int(11) NOT NULL UNIQUE,
  `cross_id` varchar(45) NOT NULL DEFAULT '',
  `genotype` varchar(45) NOT NULL DEFAULT '',
  `generation` varchar(5) NOT NULL DEFAULT '',
  `female_parent` varchar(45) NOT NULL DEFAULT '',
  `male_parent` varchar(45) NOT NULL DEFAULT '',
  `species` varchar(30) NOT NULL DEFAULT '',
  `date_collected` date DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `contributor_id` varchar(45) DEFAULT NULL,
  `antibiotics_resistance` varchar(10) DEFAULT NULL,
  `oligo_1` varchar(20) DEFAULT NULL,
  `oligo_2` varchar(20) DEFAULT NULL,
  `notes` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `seed_stock`
--

INSERT INTO `seed_stock` (`stock_id`, `cross_id`, `genotype`, `generation`, `female_parent`, `male_parent`, `species`, `date_collected`, `location`, `contributor_id`, `antibiotics_resistance`, `oligo_1`, `oligo_2`, `notes`) VALUES
(123, '4567', 'testing', 'test', 'test', 'test', 'test', '2011-01-19', 'test', 'test', 'test', 'test', 'test', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL DEFAULT 'guest',
  `password` varchar(42) NOT NULL DEFAULT 'password',
  `active` tinyint(1) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=48 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `active`, `email`) VALUES
(2, 'guest', '*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19', 1, 'None'),
(26, 'admin', '*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19', 1, 'None');

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE IF NOT EXISTS `user_role` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=48 ;

--
-- Dumping data for table `user_role`
--

INSERT INTO `user_role` (`user_id`, `role`) VALUES
(2, 2),
(26, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
