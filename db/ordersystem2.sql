-- phpMyAdmin SQL Dump
-- version 5.1.3-2.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 24, 2024 at 05:44 AM
-- Server version: 8.0.29
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ordersystem2`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `added_date` datetime DEFAULT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `address1` varchar(255) NOT NULL,
  `address2` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state_country` varchar(255) NOT NULL,
  `postcode` varchar(255) NOT NULL,
  `is_wholesale` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `first_name`, `added_date`, `last_name`, `email`, `company`, `phone`, `country`, `address1`, `address2`, `city`, `state_country`, `postcode`, `is_wholesale`) VALUES
(1, 'Sujan', '2023-10-04 07:52:08', 'Basnet', 'itssujan167@gmail.com', 'XYZ', '9862913309', 'Nepal', 'Kathmandu Model College (KMC), Bag Bazar Sadak, Kathmandu, Nepal', '', 'Kathmandu', 'Bagmati Province', '44600', 0),
(2, 'John', '2023-10-04 07:54:36', 'Cena', 'itsmeyoursujan@gmail.com', 'ABC', '23', 'India', 'Illam Hospitality & Banquets, Rajiv Gandhi Salai, OMR, Sholinganallur, Chennai, Tamil Nadu, India', '', 'Chennai', 'Tamil Nadu', '600119', 0),
(3, 'Manjul2', '2023-10-04 08:04:01', 'Bhattrai2', 'test@gmail.com', 'ABC', '123456789', 'Nepal', 'Kathmandu Model College (KMC), Bag Bazar Sadak, Kathmandu, Nepal', '', 'Kathmandu', 'Bagmati Province', '44600', 0),
(4, 'Jacoob', '2023-10-07 05:01:34', 'Johnson', 'itssujan167@gmail.com', 'Import Export', '9876543210', 'United States', '555 Main Street, Manchester, CT, USA', '', 'Hartford County', 'Connecticut', '06040', 0),
(5, 'John', '2023-10-07 06:36:04', 'Doe', 'itsmeyoursujan@gmail.com', 'company', '12123121', 'United States', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', 0),
(6, 'Sujan', '2023-10-07 06:49:07', 'Basnet', 'itssujan167@gmail.com', 'MyCompany', '9862913309', 'Nepal', 'Gaighat Bazar, Udayapur, Gaighat, Nepal', '', 'Udayapur', 'Koshi Province', '56300', 0);

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `product_id` int NOT NULL,
  `product_code` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`product_id`, `product_code`, `description`, `price`, `name`) VALUES
(4, 'BC-16', '0', '0.00', 'BC-16 Cap Assembly'),
(5, 'BC-20', '0', '0.00', '20 PSI Billet Cap Assembly'),
(6, '1425', '', '0.00', '1425'),
(7, '1427', '', '0.00', '1427'),
(8, 'RAD-2370S', '', '0.00', 'RAD-2370S'),
(9, '1429', '', '0.00', '1429'),
(10, '1426', '', '0.00', '1426-AT'),
(11, 'N03A', '', '0.00', 'N03A'),
(12, 'N03B', '', '0.00', 'N03B'),
(13, 'RAD-1492-DFZ', '', '0.00', 'RAD-1492-DFZ'),
(14, 'RAD-1052', '', '0.00', 'RAD-1052'),
(15, 'RAD-1052-MT', '', '0.00', 'RAD-1052-MT'),
(16, 'RAD-1440', '', '0.00', 'RAD-1440'),
(17, 'RAD-1470S', '', '0.00', 'RAD-1470S'),
(18, 'RAD-1472S', '', '0.00', 'RAD-1472S'),
(19, 'RAD-1480', '', '0.00', 'RAD-1480'),
(20, 'RAD-1480A', '', '0.00', 'RAD-1480A'),
(21, 'BC-16-1', '', '0.00', 'Machined Billet Cap For BC-16'),
(22, 'RAD-1486', '', '0.00', 'RAD-1486'),
(23, 'RAD-1486-MT', '', '0.00', 'RAD-1486-MT'),
(24, 'RAD-1492', '', '0.00', 'RAD-1492'),
(25, 'RAD-1537S', '', '0.00', 'RAD-1537S'),
(26, 'RAD-1635S', '', '0.00', 'RAD-1635S'),
(27, 'RAD-2374S', '', '0.00', 'RAD-2374S'),
(28, 'RAD-2375S', '', '0.00', 'RAD-2375S'),
(29, 'RAD-526S', '', '0.00', 'RAD-526S'),
(30, 'RAD-5711S', '', '0.00', 'RAD-5711S'),
(31, 'RAD-6161S', '', '0.00', 'RAD-6161S'),
(32, 'RAD-6161SX2', '', '0.00', 'RAD-6161SX2'),
(33, 'RAD-6162S', '', '0.00', 'RAD-6162S'),
(34, 'RAD-6251S', '', '0.00', 'RAD-6251S'),
(35, 'RAD-6281S', '', '0.00', 'RAD-6281S'),
(36, 'RAD-6284', '', '0.00', 'RAD-6284'),
(37, 'RAD-6289S', '', '0.00', 'RAD-6289S'),
(38, 'RAD-6339S', '', '0.00', 'RAD-6339S'),
(39, 'RAD-6340S', '', '0.00', 'RAD-6340S'),
(40, 'RAD-6369S', '', '0.00', 'RAD-6369S'),
(41, 'RAD-6370S', '', '0.00', 'RAD-6370S'),
(42, 'RAD-6374S', '', '0.00', 'RAD-6374S'),
(43, 'RAD-6375S', '', '0.00', 'RAD-6375S'),
(44, 'RAD-6379', '', '0.00', 'RAD-6379'),
(45, 'RAD-6571S', '', '0.00', 'RAD-6571S'),
(46, 'RAD-6573S', '', '0.00', 'RAD-6573S'),
(47, 'RAD-6718S', '', '0.00', 'RAD-6718S'),
(48, 'RAD-6829', '', '0.00', 'RAD-6829'),
(49, 'RAD-7104S', '', '0.00', 'RAD-7104S'),
(50, 'RAD-7829', '', '0.00', 'RAD-7829'),
(51, 'RAD-7829-DFZ', '', '0.00', 'RAD-7829-DFZ'),
(52, 'RAD-9472', '', '0.00', 'RAD-9472 Assembly'),
(53, 'SZ015A', '', '0.00', 'SZ015A'),
(54, 'SZ015AT', '', '0.00', 'SZ015AT'),
(55, 'S10FAN-11INCH', '', '0.00', 'S10FAN-11INCH'),
(56, 'LNF-228101X', '', '0.00', '11'),
(57, 'HPX-16-THIN', '0', '0.00', '16'),
(58, 'JG-1016-BLK', '', '0.00', 'JG-1016-BLK'),
(59, 'JG-1016-CHR', '', '0.00', 'JG-1016-CHR'),
(60, 'SPAL-11-MP', '', '0.00', 'SPAL-11-MP'),
(61, 'SPAL-14-HP', '', '0.00', 'Spal-14-HP'),
(62, 'SPAL-14-MP', '', '0.00', 'Spal-14-MP'),
(63, 'SPAL-14-LP', '', '0.00', 'Spal-14-LP'),
(64, 'SPAL-13-HP', '', '0.00', 'Spal-13-HP'),
(65, 'SPAL-13-MP', '', '0.00', 'Spal-13-MP'),
(66, 'SPAL-13-LP', '', '0.00', 'Spal-13-LP'),
(67, 'spal-16-MP', '', '0.00', 'spal-16-MP'),
(68, 'spal-16-HP', '', '0.00', 'spal-16-HP'),
(69, 'TNK-3012B', '', '0.00', 'GM lower inlet tank'),
(70, 'TNK-3012A', '', '0.00', 'GM uppet inlet tank'),
(71, 'TNK-3031', '', '0.00', 'Downflow 3'),
(72, 'TNK-3032', '', '0.00', 'Downlfow 3'),
(73, 'TNK-3440-C', '', '0.00', 'LSX passenger side upper'),
(74, 'TNK-3440-D', '', '0.00', 'LSX passenger side lower'),
(75, 'TNK-3055', '', '0.00', 'Full size (9370-AT) automatic tank'),
(76, 'TNK-3058', '', '0.00', 'Full size LSX-AT tank'),
(77, 'TNK-3059', '', '0.00', 'Full size blank tank'),
(78, 'TNK-3061-D', '', '0.00', 'Camaro SBC inlet tank upper'),
(79, 'TNK-3061-E', '', '0.00', 'Camaro SBC inlet tank lower'),
(80, 'TNK-3066', '', '0.00', 'GM cut core 9161, 9162, 9951 manual transmission tank '),
(81, 'TNK-3067', '', '0.00', 'GM cut core 9161, 9162, 9951 Automatic transmission tank '),
(82, 'TNK-9161-20', '', '0.00', 'LSX drivers side auto transmission tank'),
(83, 'TNK-9161-21', '', '0.00', 'LSX drivers side automatic tank'),
(84, 'TNK-9161-22', '', '0.00', 'LSX passenger side upper tank'),
(85, 'TNK-9161-23', '', '0.00', 'LSX passenger side lower tank'),
(86, 'TNK-9284-LOW', '', '0.00', '9284 lower tank for 2-3/4'),
(87, 'TNK-9284-GTO', '', '0.00', 'GTO upper tank for 2-3/4'),
(88, 'TNK-9284-TRUCK1', '', '0.00', '9284 upper tank with recessed filler neck'),
(89, 'TNK-9284-TRK2', '', '0.00', 'Filler neck panel for TNK-9284-TRK'),
(90, 'FAN-9369-14', '', '0.00', '11'),
(91, 'FAN-9369-2', '', '0.00', 'Top panel for 9161, 9162, 9951'),
(92, 'FAN-3014A', '', '0.00', 'Fan shroud for 9370'),
(93, 'FAN-3014D', '', '0.00', 'Top panel for 9370'),
(94, 'FAN-3014E', '', '0.00', 'Top panel for 9370HD 1-1/4'),
(95, 'FAN-3014K-14', '', '0.00', 'Dual 14'),
(96, 'FAN-3440-3', '', '0.00', 'Top panel for 20-3/4'),
(97, 'FAN-3440-2', '', '0.00', 'Filler panels for FAN-9441 shroud'),
(98, 'FAN-9441', '', '0.00', 'Fan shroud for 9440/9571 radiator'),
(99, 'FAN-9369-3', '', '0.00', '16'),
(100, 'FAN-9369-4', '', '0.00', '16'),
(101, 'FAN-9212-2', '', '0.00', 'Shroud Bracket'),
(102, 'FAN-9212-1', '', '0.00', 'Fan shroud'),
(103, 'BRK-3024-PS', '', '0.00', 'Jeep YJ passenger side bracket'),
(104, 'BRK-3024-DS', '', '0.00', 'Jeep YJ drivers side bracket'),
(105, 'BRK-3035', '', '0.00', 'Camaro 67-69'),
(106, 'BRK-3036', '', '0.00', 'Camaro 67-69'),
(107, 'BRK-3044-PS', '', '0.00', 'Passenger side bracket for 9440'),
(108, 'BRK-3044-DS', '', '0.00', 'Drivers side bracket for 9440'),
(109, 'BRK-7259-DS', '', '0.00', 'Bracket for 5711HD/6251HD - DS'),
(110, 'BRK-7259-PS', '', '0.00', 'Bracket for 5711HD/6251HD - PS'),
(111, 'FAN-7289', '', '0.00', 'Shroud for 6289 11'),
(112, 'FAN-3011', '', '0.00', 'Fan shroud for 6161SX2, 6161S, 6162S, 6369S, 6573S'),
(113, 'FAN-3016', '', '0.00', 'Shroud for 6284'),
(114, 'FAN-3012', '', '0.00', 'Shroud for 6718S'),
(115, 'FAN-7259-2', '', '0.00', 'Shroud for 6251S, 5711S'),
(116, 'FAN-7339', '', '0.00', 'Shroud for 6339S. 6340S'),
(117, 'FAN-147X', '', '0.00', 'Shroud for 1470S, 1472S. Needs to be modified for 1470S'),
(118, 'FAN-7440', '', '0.00', 'Shroud for 1440, 6379'),
(119, 'FAN-2375', '', '0.00', 'Shroud for 2374S, 2375S'),
(120, 'FAN-637X', '', '0.00', 'Shroud for 6374S, 6375S'),
(121, 'FAN-3018A', '', '0.00', 'Shroud for fox body Mustang'),
(122, 'FAN-7104X', '', '0.00', 'Shroud for RAD-7104S'),
(123, 'FAN-1425', '', '0.00', 'Shroud for 1425'),
(124, 'FAN-1426', '', '0.00', 'Shroud for 1426'),
(125, 'FAN-7571', '', '0.00', 'Shroud for 6571S'),
(126, 'FAN-1429', '', '0.00', 'Shroud for 1429'),
(127, 'FAN-7829-4', '', '0.00', 'Shroud for 7829'),
(128, 'FAN-4269', '', '0.00', 'Shroud for 6289S with 13'),
(129, 'ECP-370-1', '', '0.00', 'Shroud for 6370S'),
(130, 'ECP-370-2', '', '0.00', 'Lower bracket for 6370S'),
(131, 'ECP-370-3', '', '0.00', 'Cover for 6370S'),
(132, 'FAN-1635', '', '0.00', 'Shroud for 1635S'),
(133, 'RAD-6161SX2-HDDF', '1968 - 1977 Chevelle/A-Body aluminum radiator, 2-rows of 1\" tubes, dual HP 11\" Fans, Aluminum Shroud', '0.00', '1968 - 1977 Chevelle/A-Body aluminum radiator, 2-rows of 1'),
(134, 'RAD-6369S-HDDF', '1967 - 1972 Chevy/GMC Truck aluminum radiator,  2-rows of 1\" tubes, dual HP 11\" Fans, Aluminum Shroud', '0.00', '1967 - 1972 Chevy/GMC Truck aluminum radiator,  2-rows of 1'),
(135, 'RAD-6162S-HDDF', '1970 - 1981 Camaro/G-Body aluminum radiator,  2-rows of 1\" tubes, dual HP 11\" Fans, Aluminum Shroud', '0.00', '1970 - 1981 Camaro/G-Body aluminum radiator,  2-rows of 1'),
(136, 'RAD-6573S-HDDF', '1970 -1981 Firebird/TA aluminum radiator,  2-rows of 1\" tubes, dual HP 11\" Fans, Aluminum Shroud', '0.00', '1970 -1981 Firebird/TA aluminum radiator,  2-rows of 1'),
(137, 'HPX-11-BLK', '', '0.00', 'Black 11'),
(138, '1429-HDDF', '0', '0.00', '1955 - 1959 Chevy Truck Aluminum Radiator - Dual Fans - Aluminum Shroud'),
(139, '1425-SFB', '0', '0.00', '1955 - 1957 Chevy Radiator - Aluminum Shroud - Black 16'),
(140, '1425-SFC', '0', '0.00', '1955 - 1957 Chevy Radiator - Aluminum Shroud - Chrome 16'),
(141, 'RAD-6251S-FAN-BLK', '0', '0.00', '1964 - 1966 Mustang Aluminum Radiator - 302 V8 - Black 16'),
(142, 'RAD-5711S-FAN-BLK', '0', '0.00', 'RAD-5711S-FAN-BLK'),
(143, 'CORE-9440-R2', '', '0.00', 'Dewitts- 32-1-20.75R2'),
(144, 'RAD-2057S', '', '0.00', '1988 - 1998 Chevy Truck Aluminum Radiator Upgrade'),
(145, 'RAD-9428-LSX', '0', '0.00', '9428 LSX Version'),
(146, 'TNK-1427-LOW-W/H', '', '0.00', 'RAD-1427 Lower tank with holes'),
(147, 'TNK-1427-UP-W/H', '', '0.00', 'RAD-1427 Top tank with holes'),
(148, 'MP280 MALE Set - Dual', '', '0.00', 'MP280 Male Set - Dual (Harness Side)'),
(149, 'RAD-1492-LP', '0', '0.00', '1996 - 2003 S10 Aluminum Radiator - Dual Fans With Aluminum Shroud -  Low Profile'),
(150, 'RAD-6289S-HDDF', '0', '0.00', '66-67 Chevelle, 63-68 Impala Aluminum Radiator, Aluminum Shroud, 11'),
(151, 'RAD-6289S-BIGBLOCK-13LP', '0', '0.00', '66-67 Chevelle, 63-68 Impala, Aluminum Shroud, Dual 11'),
(152, 'RAD-7829-LP', '0', '0.00', 'S10 Dual Fan Radiator with Black 11'),
(153, 'RAD-7829-HDDF', '0', '0.00', 'S10 Dual Fan Radiator with Black HP 11'),
(154, 'RAD-6339S-FAN-BLK', '0', '0.00', '6339S with 16'),
(155, 'RAD-6340S-FAN-BLK', '0', '0.00', '1967 - 1970 Mustang 6340S Aluminum Radiator - Aluminum Shroud - 16'),
(156, 'RAD-6718S-HDDF', '0', '0.00', '77 - 82 Corvette Aluminum Radiator, Dual Fan, Dual 11'),
(157, 'FAN-3113-A', '', '0.00', 'FAN-3113-A'),
(158, 'RAD-7104S-FAN-BLK', '0', '0.00', 'RAD-7104S-FAN-BLK'),
(159, 'RAD-1635S-HDDF', '0', '0.00', 'RAD-1635S-HDDF'),
(160, 'RAD-2374S-HDDF', '0', '0.00', 'RAD-2374S-HDDF'),
(161, 'RAD-6375S-HDDF', '0', '0.00', 'RAD-6375S-HDDF'),
(162, 'RAD-2375S-HDDF', '0', '0.00', 'RAD-2375S-HDDF'),
(163, 'RAD-1440-HDDF', '0', '0.00', 'RAD-1440-HDDF'),
(164, 'RAD-6374S-HDDF', '0', '0.00', 'RAD-6374S-HDDF'),
(165, 'RAD-1470S-HDDF', '0', '0.00', 'RAD-1470S-HDDF'),
(166, 'RAD-1472S-HDDF', '0', '0.00', 'RAD-1472S-HDDF'),
(167, 'CORE-9212HD', '', '0.00', 'Dewitts- 32-7-18.00R3'),
(168, 'CORE-9217-LSX', '', '0.00', 'Dewitts- 32-X20.00-22.00R1'),
(169, 'CORE-9162BA', '', '0.00', 'Dewitts- 32-7-26.25H3'),
(170, 'CORE-9754', '', '0.00', 'Dewitts- 32-7-34.00R3'),
(171, 'CORE-9104HD', '', '0.00', 'Dewitts- 32-X19.8-20.5R3'),
(172, 'CORE-9161', '', '0.00', 'Dewitts- 32-1-28.25H2/ API- 04-1148'),
(173, 'FAN-9217-OEM', '', '0.00', 'JEEP J/K OEM Fan Shroud'),
(174, 'FAN-3072', '', '0.00', 'HPX 16\" Motor + Blade Assy Thin'),
(175, 'CORE-9289HD', '', '0.00', 'Dewitts- 32-21-15.25R1'),
(176, 'RAD-9754-LSX-BADASS', '', '0.00', 'RAD-9754-LSX Assembly BADASS'),
(177, 'CORE-GM-CUSTOM', '', '0.00', 'API- 04-1036'),
(178, 'RAC-01', '', '0.00', 'A/C Harness for fan switch'),
(179, 'CORE-9429HD', '', '0.00', 'Dewitts- 32-X21.87-19.50R3'),
(180, 'CORE-9284HD', '', '0.00', 'Dewitts- 32-21.17.25R3'),
(181, 'CORE-MOPAR-23', '', '0.00', 'Dewitts- 32-7-23.00R3'),
(182, 'RAD-6284-HDDF', '0', '0.00', 'RAD-6284-HDDF'),
(183, 'KIT-5711S-HPX', '0', '0.00', 'Shroud and 16'),
(184, 'CAP-20', '', '0.00', '20 PSI cap component for BC-20 assembly'),
(185, 'FAN-3039', '', '0.00', 'BRK'),
(186, 'BRK-9289-DS', '', '0.00', 'BRACKET'),
(187, 'BRK-9289-PS', '', '0.00', 'BRACKET'),
(188, 'BRK-9375-DS', '', '0.00', 'BRACKET'),
(189, 'BRK-9375-PS', '', '0.00', 'BRACKET'),
(190, '1426-AT-FAN-BLK', '0', '0.00', '1426 with 16 inch fan and shroud'),
(191, 'RAD-8161-BADASS', '', '0.00', 'RAD-8161-BADASS Assembly'),
(192, 'X-1000-MT', '', '0.00', 'Radiator'),
(193, 'x-1000', '', '0.00', 'radiator'),
(194, 'ce-01', '', '0.00', 'consumable electroid'),
(195, 'RAD-6375S-13MP', '0', '0.00', 'With Spal 13MP'),
(196, 'RAD-6370S-HDDF', '0', '0.00', 'RAD-6370S-HDDF'),
(197, 'RAD-9215-LSX', '', '0.00', 'RAD-9215-LSX Assembly'),
(198, 'RAD-138-MT-HDDF', '0', '0.00', 'RAD-138-MT-HDDF'),
(199, 'TNK-1427-LOW', '', '0.00', 'RAD-1427 Lower tank no holes'),
(200, 'RAD-9217-HEMI', '', '0.00', 'RAD-9217-HEMI Assembly'),
(201, 'RAD-9429', '0', '0.00', 'RAD-9429 with HPX fans'),
(202, 'AS060', '', '0.00', 'Liquid Intercooler Heat Exchanger (CCHE) – 550 HP'),
(203, 'RAD-6571s-FAN-BLK', '0', '0.00', 'RAD-6571S-FAN-BLK'),
(204, 'RAD-6161S-HDDF', '0', '0.00', 'For 6161S Truck Applications'),
(205, 'CORE-9425HD', '', '0.00', 'Dewitts- 32-X21.87-17.25R3'),
(206, 'RAD-6379-HDDF', '0', '0.00', 'RAD-6379-HDDF'),
(207, '9162-LSX-AT-HPX', '0', '0.00', '9162-LSX-AT-HPX'),
(208, 'RAD-9571-HPX', '', '0.00', 'RAD-9571-HPX Assembly'),
(209, 'RAD-8369', '', '0.00', 'RAD-8369 Assembly'),
(210, 'RAD-9077-BADASS', '', '0.00', 'RAD-9077 Assembly'),
(211, 'BRK-9217-7-1', '', '0.00', 'Billet mounting lug'),
(212, 'RAD-6284-HPX', '0', '0.00', 'RAD-6284-HPX'),
(213, '1429-HPX-BLK', '0', '0.00', 'RAD-1429-HPX-BLK'),
(214, 'RAD-1492-HPX', '0', '0.00', 'RAD-1492-HPX'),
(215, 'KIT-6289S-13MP', '0', '0.00', 'KIT-6289S-13MP'),
(216, 'RAD-6379-HPX', '0', '0.00', 'RAD-6379-HPX'),
(217, 'RAD-6404', '', '0.00', 'RAD-6404'),
(218, 'CORE-9161BA', '', '0.00', 'Dewitts- 32-7-28.25H3'),
(219, 'SZ015A-HDDF', '0', '0.00', 'SZO15A-HDDF'),
(220, 'SZ015-AT-HDDF', '0', '0.00', 'RAD-SZ015-AT-HDDF'),
(221, 'RAD-9261', '', '0.00', 'RAD-9261 Assembly'),
(222, 'RAD-1480-QD', '0', '0.00', 'RAD-1480 with quick disconnect trans fittings'),
(223, 'RAD-1537S-HPX', '0', '0.00', 'RAD-1537S-HPX'),
(224, 'RAD-7104s-SFC', '0', '0.00', 'RAD-7104s-SFC'),
(225, 'RAD-9369-MT-BADASS', '', '0.00', 'RAD-9369-MT-BADASS Assembly'),
(226, 'FAN-9223-2', '', '0.00', 'FAN-9223-2'),
(227, 'FAN-9223-3', '', '0.00', 'FAN-9223-3'),
(228, 'BRK-1425RL', '', '0.00', 'BRK-1425RL'),
(229, '9289HD-AT-HPX', '0', '0.00', '9289HD-AT-HPX'),
(230, 'RAD-6375S-HPX', '0', '0.00', 'RAD-6375S-HPX'),
(231, 'RAD-6374s-13MP', '0', '0.00', 'RAD-6374S-13MP'),
(232, 'KIT-6289s-HDDF', '0', '0.00', 'KIT-6289s-HDDF'),
(233, 'RAD-9212-SBF', '', '0.00', 'RAD-9212-SBF'),
(234, '9370-MT-HPX', '0', '0.00', '9370-MT-HPX'),
(235, 'RAD-1440-HPX', '0', '0.00', 'RAD-1440-HPX'),
(236, 'RAD-6251SHD', '', '0.00', 'RAD-6251SHD'),
(237, 'RAD-6369S-HPX', '0', '0.00', 'RAD-6369S-HPX'),
(238, 'RAD-6289S-HPX', '0', '0.00', 'RAD-6289S-HPX'),
(239, 'TNK-6339-UP', '', '0.00', 'TNK-6339S with 6339S top tank holes'),
(240, 'TNK-1427-UP', '', '0.00', 'RAD-1427 Top tank no holes'),
(241, '1428', '0', '0.00', 'RAD-1428'),
(242, 'RAD-1537S-HDDF', '0', '0.00', '1537s-HDDF'),
(243, 'KIT-SZ015A-HDDF', '0', '0.00', 'KIT-SZ015A-HDDF'),
(244, 'RAD-6162S-HPX', '0', '0.00', 'RAD-6162S-HPX'),
(245, 'RAD-6161SX2-HPX', '0', '0.00', 'RAD-6161SX2-HPX'),
(246, 'RAD-9829-LSX', '', '0.00', 'RAD-9829-LSX Assembly'),
(247, 'RAD-1537HD-HDDF', '0', '0.00', 'RAD-1537HD-HDDF'),
(248, 'KIT-6284-HDDF', '0', '0.00', 'KIT-6284-HDDF'),
(249, 'RAD-9951-LSX', '', '0.00', 'RAD-9951-LSX Assembly'),
(250, 'RAD-2375HD-AT-HPX', '0', '0.00', 'RAD-2375HD-AT-HPX'),
(251, 'FAN-9369-11', '', '0.00', 'FAN-9369-11'),
(252, 'FAN-7440-HDDF', '', '0.00', 'FAN-7440-HDDF'),
(253, 'RAD-9718-LSX', '', '0.00', 'RAD-9718-LSX Assembly'),
(254, 'MP280 Female Set - DUAL', '', '0.00', 'MP280 Female Set - Dual (FAN END)'),
(255, 'CAP-16', '', '0.00', 'Radiator cap component for BC-16'),
(256, 'BRK-7104', '', '0.00', 'RAD-7104 Bracket'),
(257, 'CORE-IMPALA-SS', '', '0.00', 'Dewitts- 32-7-30.5.R3'),
(258, 'RAD-9369-BADASS', '', '0.00', 'RAD-9369-BADASS Assembly'),
(259, 'RAD-8212-LSX', '', '0.00', 'RAD-8212-LSX Assembly'),
(260, 'FAN-3014K-FLAPS14', '', '0.00', 'FAN-3014K-FLAPS14'),
(261, 'CORE-9370HD', '', '0.00', 'Dewitts- 32-7-24.00R3'),
(262, 'CORE-9162', '', '0.00', 'Dewitts- 32-1-26.25H2/ API- 04-1042'),
(263, 'RAD-6951', '', '0.00', 'RAD-6951'),
(264, 'RAD-6281S-HDDF', '0', '0.00', 'RAD-6281S-HDDF'),
(265, 'RAD-6951-HDDF', '0', '0.00', 'Radiator'),
(266, 'RAD-1480-BLEM', '', '0.00', 'RAD-1480-BLEM'),
(267, 'FAN-3011-HDDF', '0', '0.00', 'FAN-3011 Assembly with fans'),
(268, 'RAD-9289', '', '0.00', 'RAD-9289 Assembly'),
(269, 'LNF-230503X', '', '0.00', '12\"HDDF'),
(270, 'RAD-9057-LSX', '', '0.00', 'RAD-9057-LSX Assembly'),
(271, 'RAD-2707-R', '', '0.00', '	2004 – 2012 Chevy Colorado, GMC Canyon, Hummer H3'),
(272, 'TNK-3076', '', '0.00', '	Blank tank for 9440 with flat filler neck top'),
(273, 'FAN-3113-B', '', '0.00', 'FAN-3113-B'),
(274, 'RAD-6161S-HPX', '0', '0.00', 'RAD-6161S-HPX'),
(275, 'RH-02', '0', '0.00', 'Dual HD Electric Cooling Fan Harness Kit '),
(276, 'RH-02-CHINA', '', '0.00', 'DUAL HD Electric Cooling Fan Harness'),
(277, 'RH-01', '0', '0.00', 'Single HD Electric Cooling Fan Harness Kit '),
(278, 'RH-01-CHINA', '', '0.00', 'Single HD Electric Cooling Fan Harness '),
(279, 'TNK-3075', '', '0.00', 'Blank tank for 9440 with flat filler neck top'),
(280, 'RAD-6370S-HPX', '0', '0.00', '6370S with dual HPX fans'),
(281, 'FAN-9217-SWITCH', '', '0.00', 'RAD-9217 FAN SWITCH HOUSING'),
(282, 'RAD-2754S', '', '0.00', '1995 - 1998 Chevy Truck Aluminum Radiator Upgrade - 40'),
(283, 'RAD-5711S-HPX', '0', '0.00', '1964 - 1966 Mustang 289 V8 Aluminum Radiator - Aluminum Shroud - HPX 16'),
(284, 'CORE-9573', '', '0.00', 'Dewitts- 32-1-27.50H2/ API- 04-1043'),
(285, 'CORE-5711HD', '', '0.00', 'Dewitts- 32-X17.38-16.50R1'),
(286, 'CORE-9370', '', '0.00', 'Dewitts- 32-1-24.50R2/ API- 04-1519'),
(287, 'HPX-16-Black', '', '0.00', '16in HPX Black'),
(288, 'VR-951-3', '', '0.00', 'RAD-VR-951-3'),
(289, 'RAD-6251S-HPX', '0', '0.00', '1964 - 1966 Mustang Aluminum Radiator - 302 V8 - HPX 16'),
(290, 'FAN-7951', '', '0.00', '	RAD-6951 Dual 11 inch Fan Shroud'),
(291, 'CE-02-KIT', '', '0.00', 'Consumable Electrode Kit'),
(292, 'CORE-9440', '', '0.00', 'Dewitts- 32-1-20.75H2/ API- 04-1144'),
(293, 'FAN-3213', '', '0.00', 'Fan Shroud - Dual 12\"'),
(294, '1426-HPX', '0', '0.00', '1957 Chevy Aluminum Radiator - 6 Cylinder Or Big Block Mounting - 3300 CFM Fan And Shroud'),
(295, 'FAN-9217-1', '', '0.00', 'RAD-9217 TOP PANEL'),
(296, 'FAN-9212-3', '', '0.00', 'Shroud Bracket'),
(297, 'FAN-1492-B', '', '0.00', '1492 Dual 11 inch Fan Shroud'),
(298, 'FAN-2370-1', '', '0.00', 'Dual 16 in Fan Shroud 2370'),
(299, 'FAN-9161-BA-16', '', '0.00', '9161 BADASS Shroud'),
(300, 'FAN-9369-26', '', '0.00', '9161 BA Top Shroud Mounting Cover'),
(301, 'FAN-9369-30', '', '0.00', 'Fan Shroud For 9185'),
(302, 'TNK-3071-1', '', '0.00', '9440 Driver Side Tank'),
(303, 'TNK-3073', '', '0.00', 'Automatic 9440 PS Tank'),
(304, 'TNK-3074', '', '0.00', 'Manual 9440 PS Tank'),
(305, 'RAD-6340S-HPX', '0', '0.00', '6340S with 16'),
(306, '1429-HPX', '0', '0.00', '1429 dual 11'),
(307, 'RAD-7104S-HPX', '0', '0.00', '1948 - 1954 Chevy Truck Aluminum Radiator - 3300 CFM Fan And Shroud'),
(308, 'FAN-3073', '', '0.00', 'HPX 16\" Motor + Blade Assy Thick'),
(309, 'RAD-6571S-HPX', '0', '0.00', 'RAD-6571S-HPX'),
(310, 'FAN-6404', '', '0.00', 'FAN-6404'),
(311, 'BRK-1426', '', '0.00', 'RAD-1426 Brackets'),
(312, 'RAD-6339S-HPX', '0', '0.00', 'RAD-6339S-HPX'),
(313, 'KIT-1470-HDDF', '0', '0.00', 'KIT-1470-HDDF'),
(314, 'TNK-9217-3-PS', '', '0.00', 'PS Filler'),
(315, 'TNK-9217-3-DS', '', '0.00', 'DS Filler'),
(316, 'TNK-9217-PS', '', '0.00', 'PS Tank'),
(317, 'TNK-9217-DS', '', '0.00', 'DS Tank'),
(318, 'BOSS-9217', '', '0.00', 'Mounting Boss'),
(319, 'BRK-9217-3', '', '0.00', 'Block'),
(320, 'TNK-9217-PS-2', '', '0.00', 'Top Filler PS'),
(321, 'BRK-9217-1', '', '0.00', 'Block'),
(322, 'BRK-9217-4', '', '0.00', 'Clip'),
(323, 'BRK-9217-6', '', '0.00', 'Z Clip'),
(324, 'BRK-9217-7', '', '0.00', 'Weldment'),
(325, 'BRK-9217-8-DS', '', '0.00', 'Hanger DS'),
(326, 'BRK-9217-8-PS', '', '0.00', 'Hanger PS'),
(327, 'CORE-9217-JK', '', '0.00', 'Dewitts- 32-X21.00-22.00R1'),
(328, 'TNK-9245-PS', '', '0.00', 'PS Tank'),
(329, 'BRK-9217-7-2', '', '0.00', 'Mounting Pin'),
(330, 'RAD-8191', '', '0.00', 'RAD-8191 Assembly'),
(331, 'TNK-9245-DS', '', '0.00', 'DS Tank'),
(332, 'MCN-9245-5', '', '0.00', 'Bottom Mounting Boss'),
(333, 'MCN-9245-6', '', '0.00', 'Top Mounting Boss'),
(334, 'TNK-9245-3', '', '0.00', 'Filler'),
(335, 'MCN-9245-4', '', '0.00', 'Block'),
(336, 'RAD-9162-LSX', '', '0.00', 'RAD-9162-LSX Assembly'),
(337, 'TNK-1537-UP', '', '0.00', 'RAD-1537 Upper tank no holes'),
(338, 'TNK-2375-LOW', '', '0.00', 'RAD-2375 Lower tank no holes'),
(339, 'TNK-5711', '', '0.00', 'RAD-5711 Tank no holes'),
(340, 'TNK-5711-UP', '', '0.00', 'TNK-5711 with 5711 top tank holes'),
(341, 'TNK-5711-LOW', '', '0.00', 'TNK-5711 with 5711 lower tank holes'),
(342, 'TNK-6251-LOW', '', '0.00', 'TNK-5711 With 6251 Lower tank holes'),
(343, 'TNK-6289', '', '0.00', 'RAD-6289S Tank no holes'),
(344, 'TNK-6375-LOW', '', '0.00', 'RAD-6375 Lower tank no holes'),
(345, 'TNK-6161-DS', '', '0.00', 'RAD-6161S Driver side tank no holes'),
(346, 'TNK-6161-PS', '', '0.00', 'RAD-6161S passenger side tank no holes'),
(347, 'TNK-6339', '', '0.00', 'RAD-6339S Tank no holes'),
(348, '1428-HPX', '0', '0.00', '1948 - 1954 Chevy Radiator - 3000 CFM HPX Fan + Shroud'),
(349, 'CORE-9707', '', '0.00', 'Dewitts- 32-X22.75-18.50R1'),
(350, 'RAD-2754S-HPX16', '0', '0.00', 'RAD-2754-HPX16'),
(351, 'RAD-9375-13HP', '', '0.00', 'RAD-9375-13HP Assembly'),
(352, 'RAD-9517', '', '0.00', 'RAD-9517 Assembly'),
(353, 'RAD-9067', '', '0.00', 'RAD-9067 Assembly'),
(354, 'RAD-2370S-HPX16', '0', '0.00', '1999 - 2013 Chevy Silverado Humer H2 Aluminum Radiator dual 16in polished fans'),
(355, '1425-HPX', '0', '0.00', '1955 - 1957 Chevy 6 Cylinder Mount With 3000 CFM HPX Fan'),
(356, 'RAD-6404-HPX', '0', '0.00', 'Jeep TJ 1987 - 2004 Aluminum Radiator For Small Block Chevy Conversion - 16'),
(357, 'RAD-9573HD-14HP', '', '0.00', 'RAD-9573HD-14HP Assembly'),
(358, 'RAD-1472S-HPX', '0', '0.00', 'RAD-1472S-HPX'),
(359, 'RAD-9470', '', '0.00', 'RAD-9470 Assembly'),
(360, 'BC-16-BLEM', '', '0.00', 'Blemished 16 PSI -Billet Cap'),
(361, 'QD-01', '', '0.00', '3/8\" GM Quick Disconnect Adapters'),
(362, 'RAD-9440-LSX-13MP', '', '0.00', 'RAD-9440-LSX-13MP Assembly'),
(363, 'WK-1066', '', '0.00', '185 Temp Switch'),
(364, 'UPGRADE', '', '0.00', 'Upgrade charge for anything '),
(365, 'KIT-6951-HDDF', '0', '0.00', 'HDDF 11 kit for RAD-6951'),
(366, 'CORE-9440HD', '', '0.00', '32-7-20.75H3'),
(367, 'BRK-9289-DS-IMP', '', '0.00', 'RAD-9289-IMP Driver side bracket'),
(368, 'BRK-9289-PS-IMP', '', '0.00', 'RAD-9289-IMP Passenger side bracket'),
(369, 'BRK-1429-DS', '', '0.00', 'RAD-1429/HD Driver side mounting bracket'),
(370, 'BRK-1429-PS', '', '0.00', 'RAD-1429/HD Passenger side mounting bracket	'),
(371, 'BRK-2370-3', '', '0.00', 'RAD-2370S Top Bracket'),
(372, 'BRK-2370-4', '', '0.00', 'RAD-2370S Top Bracket	'),
(373, 'MCN-2370-10', '', '0.00', 'RAD-2370S top or bottom mounting pins'),
(374, 'MCN-2370-11', '', '0.00', 'RAD-2370S top or bottom mounting pins'),
(375, 'MCN-2707-10', '', '0.00', 'RAD-9707 top or bottom pins'),
(376, 'MCN-9707-2', '', '0.00', 'RAD-9707 Top or bottom mounting pin'),
(377, 'FAN-3035', '', '0.00', 'HPX 11\" Housing'),
(378, 'KIT-6161-HPX', '0', '0.00', 'KIT for 6161, 6162, 6369, 6573 with HPX'),
(379, 'FAN-3035-2', '', '0.00', 'HPX 11 Motor and Blade ASSY'),
(380, 'FAN-3538', '', '0.00', 'HPX Fan Motor Cover'),
(381, 'FAN-3068', '', '0.00', '16\" HPX Housing'),
(382, 'HPX-11', '0', '0.00', 'HPX-11'),
(383, 'EXPEDITE', '', '0.00', 'Expedite Fee'),
(384, 'HPX-16-HP', '0', '0.00', '16'),
(385, 'MP280 Female Set - SINGLE', '', '0.00', 'MP280 Single Set - FAN SIDE'),
(386, 'MP280 MALE Set - Single', '', '0.00', 'MP280 Male Set - Single (Harness Side)'),
(387, 'Shipping Surcharge', '', '0.00', 'Shipping Surcharge For Express Shipping'),
(388, 'RAD-9707', '', '0.00', 'RAD-9707 Assembly'),
(389, 'RAD-9370', '', '0.00', 'RAD-9370 Assembly'),
(390, 'RAD-9185-LSX', '', '0.00', 'RAD-9185-LSX Assembly'),
(391, 'RAD-9138-HPX', '', '0.00', 'RAD-9138-HPX Assembly'),
(392, 'RAD-8369-LSX', '', '0.00', 'RAD-8369-LSX Assembly'),
(393, 'RAD-9204', '', '0.00', 'RAD-9204 Assembly'),
(394, 'RAD-CUSTOM', '', '0.00', 'RAD-CUSTOM Assembly'),
(395, 'RAD-9161-LSX', '', '0.00', 'RAD-9161-LSX Assembly'),
(396, 'RAD-9217-LSX', '', '0.00', 'RAD-9217-LSX Assembly'),
(397, 'RAD-9221-LSX', '', '0.00', 'RAD-9221-LSX Assembly'),
(398, 'RAD-8370-LSX', '', '0.00', 'RAD-8370-LSX Assembly'),
(399, 'RAD-9370HD', '', '0.00', 'RAD-9370HD Assembly'),
(400, 'RAD-9057-BADASS', '', '0.00', 'RAD-9057-BADASS Assembly'),
(401, 'RAD-9212-MT', '', '0.00', 'RAD-9212-MT Assembly'),
(402, 'RAD-9191-13HP', '', '0.00', 'RAD-9191-13HP Assembly'),
(403, 'RAD-9951', '', '0.00', 'RAD-9951 Assembly'),
(404, 'RAD-8440', '', '0.00', 'RAD-8440 Assembly'),
(405, 'RAD-9440HD-HPX', '', '0.00', 'RAD-9440HD-HPX Assembly'),
(406, 'RAD-9185-LSX-BADASS', '', '0.00', 'RAD-9185-LSX-BADASS Assembly'),
(407, 'RAD-9212', '', '0.00', 'RAD-9212 Assembly'),
(408, 'RAD-9202', '', '0.00', 'RAD-9202 Assembly'),
(409, 'RAD-9216', '', '0.00', 'RAD-9216 Assembly'),
(410, 'RAD-9440HD-13MP', '', '0.00', 'RAD-9440HD-13MP Assembly'),
(411, 'RAD-9217', '', '0.00', 'RAD-9217 Assembly'),
(412, 'RAD-9161', '', '0.00', 'RAD-9161 Assembly'),
(413, 'RAD-9440-LSX-HPX', '', '0.00', 'RAD-9440-LSX-HPX Assembly'),
(414, 'RAD-9375', '', '0.00', 'RAD-9375 Assembly'),
(415, 'RAD-9573', '', '0.00', 'RAD-9573 Assembly'),
(416, 'RAD-9215', '', '0.00', 'RAD-9215 Assembly'),
(417, 'RAD-8240', '', '0.00', 'RAD-8240 Assembly'),
(418, 'RAD-9162', '', '0.00', 'RAD-9162 Assembly'),
(419, 'RAD-9161BADASS-LSX', '', '0.00', 'RAD-9161-BADASS-LSX Assembly'),
(420, 'RAD-9374', '', '0.00', 'RAD-9374 Assembly'),
(421, 'RAD-9379', '', '0.00', 'RAD-9379 Assembly'),
(422, 'RAD-9190', '', '0.00', 'RAD-9190 Assembly'),
(423, 'RAD-9219', '', '0.00', 'RAD-9219 Assembly'),
(424, 'RAD-9573-LSX', '', '0.00', 'RAD-9573-LSX Assembly'),
(425, 'RAD-9370HD-LSX', '', '0.00', 'RAD-9370HD-LSX Assembly'),
(426, 'RAD-8959-LSX', '', '0.00', 'RAD-8959-LSX Assembly'),
(427, 'RAD-9754-BADASS', '', '0.00', 'RAD-9754-BADASS'),
(428, 'RAD-9191', '', '0.00', 'RAD-9191 Assembly'),
(429, 'RAD-9185', '', '0.00', 'RAD-9185 Assembly'),
(430, 'RAD-9370HD-MT-13HP', '', '0.00', 'RAD-9370HD-MT-13HP Assembly'),
(431, 'RAD-9138HD-14HP', '', '0.00', 'RAD-9138HD-14HP Assembly'),
(432, 'RAD-9197', '', '0.00', 'GTO radiator with 17-1/2 core, 22 overall'),
(433, 'RAD-9077-LSX-BADASS', '', '0.00', 'RAD-9077-BADASS Assembly'),
(434, 'RAD-9289-IMP-13MP', '', '0.00', 'RAD-9289-IMP-13MP Assembly'),
(435, 'RAD-9440HD-LSX-HPX', '', '0.00', 'RAD-9440HD-LSX-HPX Assembly'),
(436, 'RAD-9431', '', '0.00', 'RAD-9431'),
(437, 'RAD-9425', '', '0.00', 'RAD-9425 Assembly'),
(438, 'RAD-9289-IMP-13LP', '', '0.00', 'RAD-9289-IMP-13LP Assembly'),
(439, 'RAD-9370HD-MT-LSX', '', '0.00', 'RAD-9370HD-MT-LSX Assembly'),
(440, 'RAD-9185-BADASS', '', '0.00', 'RAD-9185-BADASS Assembly'),
(441, 'RAD-9212-LSX-MT', '', '0.00', 'RAD-9212-LSX-MT Assembly'),
(442, 'RAD-9245HD', '', '0.00', 'RAD-9245HD Assembly'),
(443, 'RAD-8289', '', '0.00', 'RAD-8289 Assembly'),
(444, 'RAD-9289-IMP', '', '0.00', 'RAD-9289-IMP Assembly'),
(445, 'RAD-9057-BADASS-LSX', '', '0.00', 'RAD-9057-BADASS-LSX Assembly'),
(446, 'RAD-9212-LSX', '', '0.00', 'RAD-9212-LSX Assembly'),
(447, 'RAD-9370HD-13HP', '', '0.00', 'RAD-9370HD-13HP Assembly'),
(448, 'RAD-9221', '', '0.00', 'RAD-9221 Assembly'),
(449, 'RAD-8162-LSX', '', '0.00', 'RAD-8162-LSX Assembly'),
(450, 'RAD-9375-13MP', '', '0.00', 'RAD-9375-13MP Assembly'),
(451, 'RAD-9370-14HP', '', '0.00', 'RAD-9370-14HP Assembly'),
(452, 'RAD-9369', '', '0.00', 'RAD-9369 Assembly'),
(453, 'RAD-9440-MT-LSX-13MP', '', '0.00', 'RAD-9440-MT-LSX-13MP Assembly'),
(454, 'RAD-9468', '', '0.00', 'RAD-9468 Assembly'),
(455, 'RAD-8951', '', '0.00', 'RAD-8951 Assembly'),
(456, 'RAD-8212', '', '0.00', 'RAD-8212 Assembly'),
(457, 'RAD-9246', '', '0.00', 'RAD-9246 Assembly'),
(458, 'RAD-9370HD-14HP', '', '0.00', 'RAD-9370HD-14HP Assembly'),
(459, 'RAD-9284', '', '0.00', 'RAD-9284 Assembly'),
(460, 'RAD-9289-13LP', '', '0.00', 'RAD-9289-13LP Assembly'),
(461, 'RAD-9240HD', '', '0.00', 'RAD-9240HD Assembly'),
(462, 'RAD-9370-13HP', '', '0.00', 'RAD-9370-13HP Assembly'),
(463, 'RAD-9162HD-14HP', '', '0.00', 'RAD-9162HD-14HP Assembly'),
(464, 'RAD-9245', '', '0.00', 'RAD-9245 Assembly'),
(465, 'RAD-9161-BADASS', '', '0.00', 'RAD-9161BADASS Assembly'),
(466, 'RAD-8370', '', '0.00', 'RAD-8370 Assembly'),
(467, 'RAD-9951HD-14HP', '', '0.00', 'RAD-9951HD-14HP Assembly'),
(468, 'RAD-9138HD-HPX', '', '0.00', 'RAD-9138HD-HPX Assembly'),
(469, 'RAD-9440-HPX', '', '0.00', 'RAD-9440-HPX Assembly'),
(470, 'RAD-9369-LSX', '', '0.00', 'RAD-9369-LSX Assembly'),
(471, 'RAD-9133HD', '0', '0.00', 'RAD-9133HD Assembly'),
(472, 'RAD-8185-LSX', '', '0.00', 'RAD-8185-LSX Assembly'),
(473, 'RAD-9240', '', '0.00', 'RAD-9240 Assembly'),
(474, 'RAD-8162', '', '0.00', 'RAD-8162 Assembly'),
(475, 'RAD-9517-HPX', '', '0.00', 'RAD-9517-HPX Assembly'),
(476, 'RAD-8375', '', '0.00', 'RAD-8375 Assembly'),
(477, 'RAD-9057', '', '0.00', 'RAD-9057 Assembly'),
(478, 'RAD-9369-BADASS-LSX', '', '0.00', 'RAD-9369-BADASS-LSX Assembly'),
(479, 'RAD-8573', '', '0.00', 'RAD-8573 Assembly'),
(480, 'RAD-9571-LSX', '', '0.00', 'RAD-9571-LSX Assembly'),
(481, 'RAD-9370HD-MT', '', '0.00', 'RAD-9370HD-MT Assembly'),
(482, 'RAD-8571', '', '0.00', 'RAD-8571 Assembly'),
(483, 'RAD-9289-13MP', '', '0.00', 'RAD-9289-13MP Assembly'),
(484, 'RAD-9370-LSX', '', '0.00', 'RAD-9370-LSX Assembly'),
(485, 'RAD-8161', '', '0.00', 'RAD-8161 Assembly'),
(486, 'RAD-9281', '', '0.00', 'RAD-9281 Assembly'),
(487, 'RAD-9370-MT-13HP', '', '0.00', 'RAD-9370-MT-13HP Assembly'),
(488, 'RAD-9573HD-LSX-14HP', '', '0.00', 'RAD-9573HD-LSX-14HP Assembly'),
(489, '1426HD-HPX', '0', '0.00', '1426HD version, sheet metal tanks, 16 '),
(490, 'RAD-2057S-HDDF', '0', '0.00', '2057 with dual 11'),
(491, 'RAD-2057S-HPX', '0', '0.00', '2057 with dual 11'),
(492, 'AC-CONDENSER-MOUNTED', '', '0.00', 'Parallel Flow A/C Condenser - Mounted to radiator'),
(493, 'RAD-6718S-HPX', '0', '0.00', '77 - 82 Corvette Aluminum Radiator, Dual HPX Fans'),
(494, 'BUNG', '', '0.00', 'BUNG'),
(495, 'MISC', '', '0.00', 'Miscellaneous order'),
(496, 'RAD-9104', '0', '0.00', 'RAD-9104 with SHEET METAL tanks'),
(497, 'RAD-9104ST', '', '0.00', 'RAD-9104 with stamped tanks'),
(498, 'KIT-6161-HDDF', '0', '0.00', 'Dual 11'),
(499, '1425-RELO-BRK', '0', '0.00', 'Relocation brackets set of 2 for 1425'),
(500, 'RAD-9284-LSX', '0', '0.00', '9284 LSX Version'),
(501, 'RAD-6573S-HPX', '0', '0.00', 'RAD-6573 with dual 11\" HPX fans'),
(502, 'RAD-9104-LSX', '0', '0.00', 'RAD-9104, LSX conversion, sheet metal tanks'),
(503, 'RAD-6375S-13HP', '0', '0.00', 'RAD-6375S with 13 inch Spal HP fans'),
(504, 'RAD-9207', '0', '0.00', '1955 - 1959 Chevy Corvette Radiator - Dual HPX Fans'),
(505, 'RAD-9370HD-14MP', '0', '0.00', 'RAD-9370HD with dual 14'),
(506, 'RAD-CUSTOM-002', '0', '0.00', 'RAD-CUSTOM-002'),
(507, 'RAD-9263', '0', '0.00', 'RAD-9263'),
(508, 'SZ015-AT-HPX', '0', '0.00', 'SZ015-AT-HPX'),
(509, 'SZ015A-HPX', '0', '0.00', 'SZ015A-HPX'),
(510, 'RAD-9289-IMP-ST', '0', '0.00', 'RAD-9289-IMP with stamped tanks'),
(511, 'RAD-9440HD-12HP', '0', '0.00', '9440HD with our 12'),
(512, 'TF-03', '', '0.00', 'Male 3/8 inverted flare to Female 5/16 inverted flare'),
(513, 'RAD-9442-LTX', '0', '0.00', 'LTX assembly'),
(514, 'RAD-9442-LTX-12MP', '0', '0.00', 'LTX assembly with 12 inch LNF fans'),
(515, 'Spal-12MP', '', '0.00', 'Spal 12\" mid profile fan'),
(516, 'OVERFLOW-CUSTOM', '', '0.00', 'Custom Overflow Tank'),
(517, 'AN-FITTINGS', '', '0.00', 'Add AN hose fittings to radiator'),
(518, 'TF-01', '', '0.00', 'Male 5/16 inverted flare to Female 3/8 inverted flare'),
(519, 'TF-02', '', '0.00', 'Male 1/4 NPT to Female 5/16 inverted flare'),
(520, 'RAD-9289-LSX', '0', '0.00', '66 - 67 Chevelle LSX conversion rad with HPX fans'),
(521, 'QD-02', '', '0.00', 'EOC GM Quick Disconnect Adapters'),
(522, 'QD-03', '', '0.00', 'Duramax GM Quick Disconnect Adapters'),
(523, 'KIT-1425-HPX', '0', '0.00', '1425 shroud with 16'),
(524, 'RAD-1492-HDDF', '0', '0.00', '1492 with HDDF fans'),
(525, 'RAD-7829-HPX', '0', '0.00', 'S10 Dual Fan Radiator with HPX 11'),
(526, 'RAD-9370-LSX-HDDF', '0', '0.00', 'With 11'),
(527, 'RAD-6289S-13MP', '0', '0.00', '66-67 Chevelle, 63-68 Impala, Aluminum Shroud, 13 inch Spal Mids'),
(528, 'RAD-9425-LSX', '0', '0.00', '9425 LSX Assembly, 16'),
(529, 'RAD-9429-LSX', '0', '0.00', 'RAD-9429 LSX with HPX 16 in fan'),
(530, 'RAD-9707-LSX', '0', '0.00', 'RAD-9707 LSX Setup'),
(531, 'CCHE-CUSTOM', '0', '0.00', 'Custom heat exchanger for liquid intercooler'),
(532, 'KIT-1429-HDDF', '0', '0.00', '1429 fans shroud assembly with dual 11'),
(533, 'KIT-1429-HPX', '0', '0.00', '1429 fans shroud assembly with dual 11'),
(534, 'KIT-237X-HDDF', '0', '0.00', '2374 and 2375 fan shroud and dual 11 HDDF fans'),
(535, 'KIT-237X-HPX', '0', '0.00', '2374 and 2375 fan shroud and dual 11 HPX fans'),
(536, 'SHOP-FAB', '', '0.00', 'Shop fabrication time'),
(537, 'KIT-637X-HDDF', '0', '0.00', '11 inch HDDF fans + shroud for 6374S and 6375S'),
(538, 'RAD-8428', '0', '0.00', 'Entropy version of 1428 without shroud - 1-1/4'),
(539, 'RAD-9426-LSX', '0', '0.00', '9426 LSX Assembly, 16'),
(540, 'RAD-6375S-13LP', '0', '0.00', '6375s- Spal 13 Low Pro'),
(541, 'RAD-9261-LSX', '0', '0.00', 'RAD-9261 for LSX conversions'),
(542, 'KIT-7104-HPX', '0', '0.00', 'Shroud and 16'),
(543, 'KIT-6339S-HPX', '0', '0.00', 'RAD-6339S with 16 HPX-THIN fan and shroud'),
(544, 'RAD-6161SHD', '0', '0.00', 'RAD-6161SHD'),
(545, 'KIT-6161-HPX16', '0', '0.00', 'Dual 16'),
(546, 'KIT-637X-13MP', '0', '0.00', 'Mid Spal 13 assembly for RAD-6374 and 6375'),
(547, 'KIT-9217-HPX', '0', '0.00', 'shroud and 16'),
(548, 'KIT-7440-HPX', '0', '0.00', 'dual 11 HPX fans and FAN-7440 shroud assy'),
(549, 'RH-RELAY', '', '0.00', 'Replacement RH MP630 Relay'),
(550, 'RAD-9951HD-LSX-14HP', '0', '0.00', 'RAD-9951 HD LSX with Spal 14HP'),
(551, 'RAD-9571-BADASS-LSX', '0', '0.00', 'RAD-9571-BADASS-LSX'),
(552, 'RAD-9197-LSX', '0', '0.00', 'GTO radiator 17-1/2 core 22 overall  for LSX conversion'),
(553, 'RAD-9195', '0', '0.00', 'GTO radiator with 15-1/2 core, 22 overall'),
(554, 'RAD-9195-LSX', '0', '0.00', 'GTO radiator with 15-1/2 core, 22 overall for LSX'),
(555, 'RAD-9212-HEMI', '0', '0.00', 'HEMI conversion rad for TJ/YJ'),
(556, 'RAD-9718', '0', '0.00', '77 - 82 Corvette Radiator'),
(557, 'RAD-9289-IMP-LSX', '0', '0.00', '59 - 67 Impala LSX conversion rad'),
(558, 'RAD-9472-LSX', '0', '0.00', 'Jeep CJ LSX conversion rad with LSX fans'),
(559, '1429HD-LSX-HPX', '0', '0.00', '1429HD for LSX with HPX fans'),
(560, 'RAD-1486HD', '0', '0.00', 'HD version of 1486'),
(561, 'RAD-9106', '0', '0.00', 'RAD-9106 with SHEET METAL tanks'),
(562, 'RAD-9106-LSX', '0', '0.00', 'RAD-9106 with SHEET METAL tanks for LSX'),
(563, 'RAD-2374S-HPX', '0', '0.00', 'RAD-2374S-HPX'),
(564, 'RAD-2375S-HPX', '0', '0.00', 'RAD-2375S-HPX'),
(565, 'RAD-6161S-HPX16', '0', '0.00', 'RAD-6161 with dual HPX16-HP fans'),
(566, 'KIT-6370S-HPX', '0', '0.00', 'Kit for 6370 HPX with all components'),
(567, 'RAD-9440HD-LSX-12HP', '0', '0.00', 'RAD-9440 with 12 inch LNF HP fans'),
(568, 'CUSTOM-ECP-SHROUD', '', '0.00', 'Custom ECP Shroud'),
(569, 'RAD-9718-LSX-BADASS', '0', '0.00', 'RAD-9718 LSX BADASS TWIN SPAL 13 HP FANS'),
(570, 'RAD-9901-LSX', '0', '0.00', '1955 - 1960 Corvette downflow LSX conversion radiator'),
(571, 'TNK-6339-LOW', '', '0.00', 'TNK-6339 with 6339S lower tank holes'),
(572, 'FAN-3024-Samlpe', '', '0.00', 'RAD-1480/NO3 Shroud'),
(573, 'RAD-9204-LSX', '0', '0.00', 'RAD-9204-LSX'),
(574, 'RAD-7829-LSX', '', '0.00', 'RAD-7829-LSX with fan shroud - no fans'),
(575, 'RAD-7829-LSX-HDDF', '0', '0.00', 'RAD-7829-LSX-HDDF'),
(576, 'KIT-7829-HDDF', '0', '0.00', 'KIT-7829-HDDF'),
(577, 'KIT-2370-HPX16', '0', '0.00', 'KIT-2370-HPX16'),
(578, 'KIT-9161-BADASS', '0', '0.00', 'KIT-9161-BADASS'),
(579, 'KIT-4269-13HP', '0', '0.00', 'FAN-4269 with 13 HP Spal Fans'),
(580, 'RAD-9426-HPX', '0', '0.00', 'RAD-9426 Entropy Assembly'),
(581, 'RAD-CUSTOM-001', '0', '0.00', '9289HD CORE, FAN-7440, HPX-11'),
(582, 'RAD-CUSTOM-003', '0', '0.00', 'CORE-1429, FAN-1429, HPX-11'),
(583, 'RAD-CUSTOM-004', '0', '0.00', 'CORE-9370HD'),
(584, 'RAD-9431-LSX', '0', '0.00', 'RAD-9431-LSX'),
(585, 'RAD-6161SHD-HDDF', '0', '0.00', 'RAD-6161SHD-HDDF'),
(586, 'KIT-1428-HPX', '0', '0.00', 'KIT-1428-HPX'),
(587, '1429HD-HPX', '0', '0.00', '1429HD-HPX'),
(588, 'RAD-6374S-HPX', '0', '0.00', 'RAD-6374S-HPX'),
(589, 'RAD-6951-HPX', '0', '0.00', 'RAD-6951-HPX'),
(590, 'RAD-9370HD-LSX-14HP', '0', '0.00', 'RAD-9370HD-LSX-14HP'),
(591, 'RAD-8284', '0', '0.00', 'RAD-8284'),
(592, 'RAD-8185', '0', '0.00', 'RAD-8185'),
(593, 'TNK-6340', '', '0.00', 'TNK-6339 with 6340S lower tank holes'),
(594, 'TNK-7104-UP', '', '0.00', 'RAD-7104S Top tank with no holes'),
(595, 'TNK-7104-UP-W/H', '', '0.00', 'TNK-7104-UP With holes'),
(596, 'TNK-7104-LOW', '', '0.00', 'RAD-7104S Lower tank with holes'),
(597, '1425HD-HPX', '0', '0.00', '1425HD with HPX-16'),
(598, '1428HD-HPX', '0', '0.00', '1428HD with HPX-16'),
(599, 'KIT-7440-HDDF', '', '0.00', '7440 with HDDF fans'),
(600, 'RAD-8959', '0', '0.00', 'RAD-8959'),
(601, 'X-1000-HDDF', '0', '0.00', 'X-1000-HDDF'),
(602, 'RAD-9250', '0', '0.00', '1970 - 1971 Torino Aluminum Radiator'),
(603, 'RAD-9215-BADASS', '0', '0.00', 'RAD-9215-BADASS'),
(604, 'RAD-9219-LSX', '0', '0.00', '1966 - 1968 Corvette LSX Radiator'),
(605, 'KIT-9369-HPX', '0', '0.00', 'KIT-9369-HPX'),
(606, 'KIT-9370-HPX', '0', '0.00', 'HPX 11\" fan shroud assembly for 9370'),
(607, 'RAD-9216-LSX', '0', '0.00', '1973 - 1976 Corvette LSX Conversion Radiator - 11'),
(608, 'RAD-9437-LSX', '0', '0.00', '1958 Impala LSX Aluminum Radiator - 16'),
(609, 'GIFT', '', '0.00', 'Gift Certificate'),
(610, 'RH-03 CHINA', '', '0.00', 'RH-03 series/parallel harness'),
(611, 'RH-03', '0', '0.00', 'RH-03 series/parallel harness'),
(612, 'SPAL-16-LP', '', '0.00', 'Spal 16\" LP Fan'),
(613, 'KIT-9440-HPX', '0', '0.00', '9440 fan shroud assembly with 11'),
(614, 'RAD-1470S-HPX', '0', '0.00', 'RAD-1470S with dual HPX fans'),
(615, 'KIT-6718-HDDF', '0', '0.00', 'Dual 11 inch HDDF fans and shroud for RAD-6718S'),
(616, 'KIT-6281S-HDDF', '0', '0.00', 'FAN SHROUD KIT FOR 6281S HDDF - INCLUDE WELD ON BRACKETS'),
(617, 'KIT-1492-HDDF', '0', '0.00', 'HDDF FAN KIT FOR 1492'),
(618, 'RAD-9218', '0', '0.00', 'RAD-9217 without fan and shroud'),
(619, 'RAD-9213', '0', '0.00', 'Jeep TJ/YJ OEM Replacement for 4L Engine'),
(620, 'RAD-6716', '', '0.00', '1973 - 1987 21 inch tall Chevy Truck Radiator'),
(621, 'RAD-9829', '0', '0.00', 'Corvette C4 Radiator With Dual 11 HPX Fans'),
(622, 'FAN-3716', '', '0.00', '--'),
(623, 'RAD-6716-HPX', '0', '0.00', 'RAD 6716 HPX'),
(624, 'RAD-9162HD-LSX-14HP', '0', '0.00', '9162 HD LSX 14HP'),
(625, 'RAD-9829HD', '0', '0.00', 'Corvette C4 HD radiator with HPX fans'),
(626, 'MCN-3057', '', '0.00', 'OVERFLOW - ENTROPY'),
(627, 'KIT-1635-HDDF', '0', '0.00', '1635 with 11 HDDF fans'),
(628, 'KIT-1470-11MP', '0', '0.00', '1470 fan shroud with 11 Spal MP'),
(629, 'KIT-1440-HDDF', '0', '0.00', '7440 shroud with dual 11 inch HDDF fans'),
(630, 'RAD-7829-LSX-HPX', '0', '0.00', 'RAD-7829-LSX-HPX'),
(631, 'RAD-9470-HEMI', '0', '0.00', 'Setup for 5.7L Hemi'),
(632, 'RAD-4754-BADASS-LT', '0', '0.00', 'LTX version of the RAD-9754 LSX'),
(633, 'RAD-4369-LT', '0', '0.00', 'LTX version of RAD-4369-LT'),
(634, 'RAD-2707-V2', '', '0.00', '	2004 – 2012 Chevy Colorado, GMC Canyon, Hummer H3'),
(635, 'RAD-6716-HDDF', '0', '0.00', 'RAD-6716-HDDF'),
(636, 'RAD-9247-LSX-BADASS', '0', '0.00', '94 - 96 Impala SS BADASS conversion rad'),
(637, 'RAD-9374-13MP', '0', '0.00', 'With 13MP Spal '),
(638, 'KIT-1470-HPX', '0', '0.00', 'Dual 11 inch HPX fans and shroud for RAD-1470S	'),
(639, 'FAN-2707-1', '', '0.00', 'RAD-2707 Sroud'),
(640, 'BRK-9104-GMC', '', '0.00', 'RAD-9104-GMC Mounting Brackets'),
(641, 'BRK-9104-DS', '', '0.00', 'RAD-9104 DS Mounting Bracket'),
(642, 'BRK-9104-PS', '', '0.00', 'RAD-9104 PS Mounting Bracket'),
(643, 'RAD-6281S-HPX', '0', '0.00', 'RAD-6281S-HPX'),
(644, 'RAD-9209-LSX', '0', '0.00', '55 - 59 Corvette Aluminum Radiator LSX Conversion 11 HPX FANS'),
(645, 'RAD-9236-LSX', '0', '0.00', '1958 Impala LSX Conversion Rad - HPX 16 HP Fan'),
(646, 'RAD-4185-LT', '0', '0.00', '1973 – 1987 Chevy Truck Pickup LT Conversion'),
(647, 'RAD-1635S-11MP', '0', '0.00', 'RAD-1635S with 11MP Spal'),
(648, 'RAD-6245', '', '0.00', '2008 - 2022 Dodge Charger Challenger Radiator'),
(649, 'X-1000-MT-HDDF', '0', '0.00', 'X-1000 with dual HDDF fans'),
(650, 'RAD-6379-13MP', '0', '0.00', 'RAD-6379-13MP'),
(651, 'RAD-9442', '0', '0.00', '1962 - 1967 Nova Downflow HD 1 1 1/4 Aluminum Radiator With 12 HP Fans'),
(652, 'ECP-MOD', '', '0.00', 'MISC ECP-MODIFICATION'),
(653, 'SPAL-16-HP-PUSH', '', '0.00', 'Spal 16 inch pusher fan - HP'),
(654, 'RAD-9468-LSX', '0', '0.00', '1968 - 1974 AMC Javelin/AMX Radiator LSX Conversion With Dual HPX Fans'),
(655, 'RAD-9213-LSX', '0', '0.00', 'Jeep TJ/YJ LS Swap'),
(656, 'RAD-9361', '0', '0.00', 'Bronco Radiator'),
(657, 'RAD-6281-13MP', '0', '0.00', '1964 - 1965 Chevelle 13MP Assembly'),
(658, 'FAN-7829-2', '', '0.00', '7829-LSX 11\" Shroud'),
(659, 'CORE-9289', '', '0.00', 'H15.5-S25-5-2X100-2U'),
(660, 'Misc Screws', '', '0.00', 'Somebody screwed up.'),
(661, '	RAD-9214', '', '0.00', '1987 - 2004 Jeep Wrangler SBC Conversion Radiator	'),
(662, 'Misc Brakets', '', '0.00', 'Misc missing / Damaged Brackets'),
(663, 'RAD-6339HD', '', '0.00', 'HD RAD-6369'),
(664, 'Entropy Radiator Mod', '', '0.00', 'Entropy Radiator Modification'),
(665, 'RAD-6716-HPX16', '0', '0.00', 'RAD 6716 HPX16'),
(666, 'RAD-9375-HEMI', '0', '0.00', 'Mopar 1966 - 1974 Big Block Aluminum Radiator - 26'),
(667, 'RAD-9192', '0', '0.00', '64 - 67 GTO Tall'),
(668, 'RAD-9442-LSX', '0', '0.00', '1962 - 1967 Nova Downflow HD 1 1 1/4 Aluminum Radiator With 12 HP Fans'),
(669, 'RAD-6374s-13LP', '0', '0.00', 'RAD-6374S-13LP'),
(670, 'KIT-6289S-HPX', '0', '0.00', 'KIT-6289S-HPX'),
(671, 'CORE-1426', '', '0.00', '32-8-16.62R1'),
(672, 'RAD-6289S-13-11', '0', '0.00', '66-67 Chevelle, 63-68 Impala, Aluminum Shroud, 13 inch Seal mid, 11 inch mid'),
(673, 'CORE-1429', '', '0.00', '32-8-19.50R1'),
(674, 'ECP Shroud', '', '0.00', 'ECP-RAD Dual or Single Fan Shroud'),
(675, 'ECP-KIT-HDDF', '0', '0.00', 'ECP shroud with dual HDDF-11 or HDDF 12 fans'),
(676, 'ECP-KIT-HPX ', '0', '0.00', 'ECP shroud with dual HPX-11 fans'),
(677, 'ECP-KIT-16', '0', '0.00', 'ECP Shroud with single HPX-16-THIN or HPX-16-HP'),
(678, 'ECP-KIT-16DF', '0', '0.00', 'ECP shroud with dual HPX-16-THIN or HPX-16-HP fans'),
(679, 'ECP-KIT-SPAL ', '0', '0.00', 'ECP shroud with any single or dual Spal 11 -16'),
(680, 'ENTROPY-KIT', '0', '0.00', 'Entropy shroud with HPX-11 fans'),
(681, 'Entropy-Shroud', '', '0.00', 'Entropy-RAD Dual or Single Fan Shroud'),
(682, 'ENTROPY-KIT-16', '0', '0.00', 'Entropy shroud with  single HPX-16-THIN or HPX-16-HP'),
(683, 'ENTROPY-KIT-16DF', '0', '0.00', 'Entropy shroud with dual HPX-16-THIN or HPX-16-HP fans'),
(684, 'SPAL-FAN', '', '0.00', 'SPAL FANS'),
(685, 'ENTROPY-KIT-SPAL ', '0', '0.00', 'Entropy shroud with any Spal 11'),
(686, 'ENTROPY-KIT-HDDF', '0', '0.00', 'Entropy shroud with HDDF-11 or HDDF 12 fans'),
(687, 'X-1000-HPX', '0', '0.00', 'X-1000-HPX'),
(688, 'FAN-9370-10', '', '0.00', 'Detachable Top panel for 9370	'),
(689, 'FAN-9370-12', '', '0.00', 'Top Cover Mount for 9370'),
(690, 'FAN-9369-13', '', '0.00', 'Bottom Cover for 9370'),
(691, 'FAN-9370-11', '', '0.00', 'Detachable Top panel for 9370HD'),
(692, 'FAN-9370-14', '', '0.00', 'Bottom Cover for 9370	'),
(693, 'FAN-9369-37', '', '0.00', 'GM 28\" Core Detachable Top Panel'),
(694, 'FAN-9369-34', '', '0.00', 'GM 28\" Core Top cover mount'),
(695, 'FAN-9369-38', '', '0.00', 'GM 28\" Core Bottom Cover'),
(696, 'FAN-9369-33', '', '0.00', 'GM 28\" BADASS Core Detachable Top Panel'),
(697, 'FAN-9369-39', '', '0.00', 'GM 28\" BADASS Core Bottom Coverl'),
(698, 'X-1000-MT-HPX', '0', '0.00', 'X-1000-MT-HPX'),
(699, 'RAD-6375S-1311', '0', '0.00', 'RAD-6375S with low pro 11 and 13 '),
(700, 'CORE-9284', '', '0.00', 'H17.5-S25-5-2X100-2U'),
(701, 'RAD-9369-LSX-ST', '0', '0.00', 'RAD--9161/9369-LSX/LT-ST Assembly'),
(702, 'KIT-ENTROPY-CUSTOM-HPX', '0', '0.00', 'Custom Entropy Shoud with 11\' HPX Fans'),
(703, 'RAD-2460', '', '0.00', '1991 - 1993 Dodge Cummings 5.9L'),
(704, 'RAD-9202-LSX', '0', '0.00', 'RAD-9202-LSX Assembly'),
(705, 'KIT-4269-LP', '0', '0.00', 'FAN-4269 with spal 13 LP fans'),
(706, 'CUSTOM-ENTROPY-SHROUD', '', '0.00', 'Custom Entropy Shroud no Fans');

-- --------------------------------------------------------

--
-- Table structure for table `inventory_prices`
--

CREATE TABLE `inventory_prices` (
  `id` int NOT NULL,
  `sales_price` decimal(8,2) DEFAULT NULL,
  `description` text,
  `sku` varchar(255) NOT NULL,
  `product_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int NOT NULL,
  `customer_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `gross_cost` decimal(8,2) DEFAULT NULL,
  `discount_type` varchar(255) DEFAULT NULL,
  `discount_value` decimal(8,2) DEFAULT NULL,
  `discount_amount` decimal(8,2) DEFAULT NULL,
  `shipping_cost` decimal(8,2) DEFAULT NULL,
  `total_amount` decimal(8,2) DEFAULT NULL,
  `ship_to` decimal(8,2) DEFAULT NULL,
  `payment_status` varchar(255) NOT NULL DEFAULT '0',
  `transactionId` varchar(255) DEFAULT NULL,
  `invoice_no` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_id`, `created_date`, `gross_cost`, `discount_type`, `discount_value`, `discount_amount`, `shipping_cost`, `total_amount`, `ship_to`, `payment_status`, `transactionId`, `invoice_no`) VALUES
(15, 3, '2024-01-03 05:38:47', '25.16', 'percentage', '0.00', '0.00', '0.00', '25.16', '18.00', '1', '80012056933', NULL),
(17, 1, '2024-01-03 05:47:17', '1641.60', 'percentage', '0.00', '0.00', '100.00', '1741.60', '19.00', '1', '80012056990', NULL),
(19, 5, '2024-01-03 07:43:00', '2578.00', 'percentage', '0.00', '0.00', '10.00', '2588.00', '21.00', '1', '80012058735', NULL),
(20, 5, '2024-01-04 05:15:15', '1601.60', 'percentage', '0.00', '0.00', '11.00', '1612.60', '21.00', '1', '80012140966', NULL),
(21, 5, '2024-01-04 06:28:56', '1590.00', 'percentage', '0.00', '0.00', '0.00', '1590.00', '21.00', '1', '80012142325', '4001'),
(22, 5, '2024-01-09 15:17:50', '41.68', 'percentage', '0.00', '0.00', '49.00', '90.68', '21.00', '0', NULL, NULL),
(23, 5, '2024-01-09 15:45:09', '27.14', 'percentage', '0.00', '0.00', '30.00', '57.14', '21.00', '0', NULL, NULL),
(24, 4, '2024-01-09 16:56:59', '28.48', 'percentage', '0.00', '0.00', '0.00', '28.48', '27.00', '0', NULL, NULL),
(25, 4, '2024-01-09 16:57:00', '28.48', 'percentage', '0.00', '0.00', '0.00', '28.48', '27.00', '0', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--

CREATE TABLE `order_details` (
  `id` int NOT NULL,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_code` varchar(255) DEFAULT NULL,
  `product_description` text,
  `unit_price` decimal(8,2) DEFAULT NULL,
  `discount_type` varchar(255) DEFAULT NULL,
  `discount_value` decimal(8,2) DEFAULT NULL,
  `item_quantity` int NOT NULL,
  `subtotal_amount` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `order_details`
--

INSERT INTO `order_details` (`id`, `order_id`, `product_id`, `product_code`, `product_description`, `unit_price`, `discount_type`, `discount_value`, `item_quantity`, `subtotal_amount`) VALUES
(18, 15, 1, 'BC-16 Cap Assembly', 'This is a test description', '12.58', NULL, NULL, 2, '25.16'),
(20, 17, 4, 'RAD1480A', 'A general RAD product with very effective things in it', '25.78', NULL, NULL, 10, '257.80'),
(21, 17, 1, 'BC-16 Cap Assembly', 'This is a test description', '12.58', NULL, NULL, 110, '1383.80'),
(23, 19, 4, 'RAD1480A', 'A general RAD product with very effective things in it', '25.78', NULL, NULL, 100, '2578.00'),
(24, 20, 3, 'N03A', 'This is a general product', '14.56', NULL, NULL, 110, '1601.60'),
(25, 21, 2, '20 PSI Billet Cap Assembly', '20 PSI Billet Cap Assembly', '15.90', NULL, NULL, 100, '1590.00'),
(26, 22, 2, '20 PSI Billet Cap Assembly', '20 PSI Billet Cap Assembly', '15.90', NULL, NULL, 1, '15.90'),
(27, 22, 4, 'RAD1480A', 'A general RAD product with very effective things in it', '25.78', NULL, NULL, 1, '25.78'),
(28, 23, 1, 'BC-16 Cap Assembly', 'This is a test description', '12.58', NULL, NULL, 1, '12.58'),
(29, 23, 3, 'N03A', 'This is a general product', '14.56', NULL, NULL, 1, '14.56'),
(30, 24, 1, 'BC-16 Cap Assembly', 'This is a test description', '12.58', NULL, NULL, 1, '12.58'),
(31, 24, 2, '20 PSI Billet Cap Assembly', '20 PSI Billet Cap Assembly', '15.90', NULL, NULL, 1, '15.90'),
(32, 25, 1, 'BC-16 Cap Assembly', 'This is a test description', '12.58', NULL, NULL, 1, '12.58'),
(33, 25, 2, '20 PSI Billet Cap Assembly', '20 PSI Billet Cap Assembly', '15.90', NULL, NULL, 1, '15.90');

-- --------------------------------------------------------

--
-- Table structure for table `sales_details`
--

CREATE TABLE `sales_details` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `brand` varchar(255) NOT NULL,
  `description` text,
  `sku` varchar(255) NOT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `product_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `sales_details`
--

INSERT INTO `sales_details` (`id`, `name`, `brand`, `description`, `sku`, `price`, `product_id`) VALUES
(1, 'BC-16 Cap Assembly', 'entropy', 'This is a test description', 'SKU-BC-16', '12.58', 4),
(2, '20 PSI Billet Cap Assembly', 'entropy', '20 PSI Billet Cap Assembly', 'SKU-20-PSI', '15.90', 5),
(3, 'N03A', 'entropy', 'This is a general product', 'N03A-SKU', '14.56', 11),
(4, 'RAD1480A', 'entropy', 'A general RAD product with very effective things in it', 'RAD1480-A', '25.78', 14),
(5, 'Spal14HP', 'ecp', 'A general product', 'Spal14-SKU', '15.67', 61),
(6, 'S10FAN', 'ecp', 'This is S10FAN product. This is very good. I love this.', 'S10FAN', '20.56', 55),
(7, 'TestProd', 'ecp', 'This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts. This is Dewitts.  This is Dewitts. This is Dewitts. This is Dewitts.', 'SKU-1001', '13.89', 179);

-- --------------------------------------------------------

--
-- Table structure for table `ship_to`
--

CREATE TABLE `ship_to` (
  `id` int NOT NULL,
  `name` varchar(40) NOT NULL,
  `address_1` varchar(400) NOT NULL,
  `address_2` varchar(400) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `postal_code` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ship_to`
--

INSERT INTO `ship_to` (`id`, `name`, `address_1`, `address_2`, `city`, `state`, `postal_code`, `country`, `contact`, `phone_number`) VALUES
(15, 'John Cena', 'Illam Hospitality & Banquets, Rajiv Gandhi Salai, OMR, Sholinganallur, Chennai, Tamil Nadu, India', '', 'Chennai', 'Tamil Nadu', '600119', 'India', '', '23'),
(17, 'John Cena', 'Illam Hospitality & Banquets, Rajiv Gandhi Salai, OMR, Sholinganallur, Chennai, Tamil Nadu, India', '', 'Chennai', 'Tamil Nadu', '600119', 'India', '', '23'),
(19, 'Sujan Basnet', 'Gaighat Bazar, Udayapur, Gaighat, Nepal', '', 'Udayapur', 'Koshi Province', '56300', 'Nepal', '', '9862913309'),
(20, 'Sujan Basnet', 'Kathmandu Model College (KMC), Bag Bazar Sadak, Kathmandu, Nepal', '', 'Kathmandu', 'Bagmati Province', '44600', 'Nepal', '', '9862913309'),
(21, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(22, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(23, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(24, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(25, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(26, 'John Doe', '555 Main Street, Racine, WI, USA', '', 'Racine County', 'Wisconsin', '53403', '', '', '12123121'),
(27, 'Jacoob Johnson', '555 Main Street, Manchester, CT, USA', '', 'Hartford County', 'Connecticut', '06040', '', '', '9876543210');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'manjul', 'pass'),
(2, 'manjul1', 'pbkdf2:sha256:600000$peMBpFR2N6wC8hXu$8f2ef08c63710f0a4fc60ac14d7b68eb66ee56a8b40ad62e723b5f3d87efa6dd'),
(3, 'manjul2', 'pbkdf2:sha256:600000$Flyc4HP7iCQz8nO8$becf65f45d115d775f03d2d707e767dc9a446be2fe93644ab3628088c17d798e'),
(4, 'admin', 'pbkdf2:sha256:600000$AkEVVwsHLVR6I5Kg$2a0de80cea76f942711ff865194185016eff1e37386f942efdefcb66efedccdd');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `inventory_prices`
--
ALTER TABLE `inventory_prices`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sales_details`
--
ALTER TABLE `sales_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ship_to`
--
ALTER TABLE `ship_to`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=707;

--
-- AUTO_INCREMENT for table `inventory_prices`
--
ALTER TABLE `inventory_prices`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `order_details`
--
ALTER TABLE `order_details`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `sales_details`
--
ALTER TABLE `sales_details`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ship_to`
--
ALTER TABLE `ship_to`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
