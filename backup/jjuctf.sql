-- phpMyAdmin SQL Dump
-- version 4.9.7deb1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:3306
-- 生成日期： 2021-02-25 07:17:21
-- 服务器版本： 10.3.25-MariaDB-0ubuntu1
-- PHP 版本： 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `jjuctf`
--

-- --------------------------------------------------------

--
-- 表的结构 `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(30) NOT NULL,
  `admin_email` varchar(30) NOT NULL,
  `admin_mobile` varchar(20) NOT NULL,
  `admin_photo` varchar(300) DEFAULT NULL,
  `admin_password` varchar(100) NOT NULL,
  `status` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `admin_email`, `admin_mobile`, `admin_photo`, `admin_password`, `status`) VALUES
(12, 'hsm', '905008677@qq.com', '18579266908', NULL, '6f8c33aa2d7257eb96a3852b32e9ac9a', 0),
(21, 'admin', 'admin@qq.com', '123456', NULL, '21232f297a57a5a743894a0e4a801fc3', 1);

-- --------------------------------------------------------

--
-- 表的结构 `awd_config`
--

CREATE TABLE `awd_config` (
  `id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `update_time` int(11) NOT NULL,
  `check_time` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `check_down_score` int(11) NOT NULL,
  `salt` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `awd_config`
--

INSERT INTO `awd_config` (`id`, `start_time`, `end_time`, `update_time`, `check_time`, `score`, `check_down_score`, `salt`) VALUES
(2, '2021-02-20 14:19:00', '2021-02-27 14:19:00', 10, 10, 10, 50, '10');

-- --------------------------------------------------------

--
-- 表的结构 `awd_config_ip_pool`
--

CREATE TABLE `awd_config_ip_pool` (
  `id` int(11) NOT NULL,
  `start_ip` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_ip` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `point_ip` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `awd_config_ip_pool`
--

INSERT INTO `awd_config_ip_pool` (`id`, `start_ip`, `end_ip`, `point_ip`) VALUES
(1, '172.18.0.2', '172.18.0.254', '172.18.0.35');

-- --------------------------------------------------------

--
-- 表的结构 `awd_exam`
--

CREATE TABLE `awd_exam` (
  `id` int(11) NOT NULL,
  `image_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ssh` int(11) NOT NULL,
  `other_port` int(11) NOT NULL,
  `user` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` datetime NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `awd_exam`
--

INSERT INTO `awd_exam` (`id`, `image_id`, `name`, `ssh`, `other_port`, `user`, `time`, `status`) VALUES
(25, '56d86fcbf109', 'Pwn1', 22, 80, 'glzjin', '2021-02-19 14:08:57', 1),
(27, ' fd216fa6d0f7', 'WEB1', 22, 80, ' glzjin', '2021-02-20 11:01:15', 1),
(28, '0f3eddf395aa', 'new_web1', 22, 80, 'glzjin', '2021-02-21 15:26:23', 1);

-- --------------------------------------------------------

--
-- 表的结构 `awd_exam_instance`
--

CREATE TABLE `awd_exam_instance` (
  `id` int(11) NOT NULL,
  `awd_exam_id` int(11) DEFAULT NULL,
  `groupname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `container_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ssh_port` int(11) NOT NULL,
  `other_port` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `flag` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tag` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `ssh_user` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `arrangement` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT=' 完整内容	 id image_id name ssh other_port time';

--
-- 转存表中的数据 `awd_exam_instance`
--

INSERT INTO `awd_exam_instance` (`id`, `awd_exam_id`, `groupname`, `container_id`, `name`, `ssh_port`, `other_port`, `time`, `flag`, `ip`, `tag`, `status`, `ssh_user`, `password`, `arrangement`) VALUES
(825, NULL, 'admin', '414f0c7c3898', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.245', 'tag', 1, 'glzjin', '048c375eb414', 0),
(826, NULL, 'HSM', 'f044f41dcce0', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.244', 'tag', 1, 'glzjin', '74ddcdc6d755', 0),
(827, NULL, 'test1', '2cf2d403fb53', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.243', 'tag', 1, 'glzjin', '068aa61a42dc', 0),
(828, NULL, 'test2', '141dfa6e88c9', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.242', 'tag', 1, 'glzjin', '99c9cb8583a9', 0),
(829, NULL, 'test3', '11068d1219a7', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.241', 'tag', 1, 'glzjin', 'd5a2f0bda151', 0),
(830, NULL, 'test4', 'a011c611f28f', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.240', 'tag', 1, 'glzjin', '72192a572f37', 0),
(831, NULL, 'test5', '5dc75e454fa8', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.239', 'tag', 1, 'glzjin', 'aa1ee3d9977a', 0),
(832, NULL, '葫芦娃', 'bfb573d4e51d', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.238', 'tag', 1, 'glzjin', 'f93cb39f0a20', 0),
(833, NULL, 'test123', '74796a81498b', 'Pwn1', 22, 80, '2021-02-24 13:39:23', '', '172.18.0.237', 'tag', 1, 'glzjin', 'ed6104f48779', 0),
(834, NULL, 'admin', 'e703e9c3f7db', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.254', 'tag', 1, ' glzjin', 'e2f61c891c70', 0),
(835, NULL, 'HSM', '09c6abc0a4a9', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.253', 'tag', 1, ' glzjin', 'a5b5f3c3483c', 0),
(836, NULL, 'test1', '97b19f631ecf', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.252', 'tag', 1, ' glzjin', '4f50040083b0', 0),
(837, NULL, 'test2', '007391fa8a12', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.251', 'tag', 1, ' glzjin', 'c19195c415b3', 0),
(838, NULL, 'test3', '25cc018fa917', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.250', 'tag', 1, ' glzjin', '5c9a464b0c18', 0),
(839, NULL, 'test4', '9fb425228203', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.249', 'tag', 1, ' glzjin', '3fd298cd33b6', 0),
(840, NULL, 'test5', '62a5581e3d39', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.248', 'tag', 1, ' glzjin', 'e3c56eacd04f', 0),
(841, NULL, '葫芦娃', '0f07f41d41b7', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.247', 'tag', 1, ' glzjin', '52eaa4d84f78', 0),
(842, NULL, 'test123', 'bea847ce8dd9', 'WEB1', 22, 80, '2021-02-24 13:39:34', '', '172.18.0.246', 'tag', 1, ' glzjin', 'ad545894cb34', 0),
(843, NULL, 'admin', 'a7901dcb7358', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.236', 'tag', 1, 'glzjin', 'c98351bbcdac', 0),
(844, NULL, 'HSM', 'd82f50608124', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.235', 'tag', 1, 'glzjin', '09c43f479633', 0),
(845, NULL, 'test1', '1ced6a739a9b', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.234', 'tag', 1, 'glzjin', 'c719025d9af6', 0),
(846, NULL, 'test2', '4710c36efea1', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.233', 'tag', 1, 'glzjin', '6848d24ec475', 0),
(847, NULL, 'test3', '3a58eca47ff7', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.232', 'tag', 1, 'glzjin', '2ae097fd3acf', 0),
(848, NULL, 'test4', '24cb7da1a1f8', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.231', 'tag', 1, 'glzjin', 'c043d1f1da32', 0),
(849, NULL, 'test5', '6d4642f962b2', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.230', 'tag', 1, 'glzjin', '2d57f57f12fa', 0),
(850, NULL, '葫芦娃', '7b9e398d3f90', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.229', 'tag', 1, 'glzjin', 'fed93cb7e981', 0),
(851, NULL, 'test123', '65a581ad7d65', 'new_web1', 22, 80, '2021-02-24 13:39:46', '', '172.18.0.228', 'tag', 1, 'glzjin', '5af2bd6e8569', 0);

-- --------------------------------------------------------

--
-- 表的结构 `awd_ranks`
--

CREATE TABLE `awd_ranks` (
  `id` int(11) NOT NULL,
  `group_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `awd_ranks`
--

INSERT INTO `awd_ranks` (`id`, `group_name`, `score`) VALUES
(394, 'admin', 5000),
(395, 'HSM', 5000),
(396, 'test1', 5000),
(397, 'test2', 5000),
(398, 'test3', 5000),
(399, 'test4', 5000),
(400, 'test5', 5000),
(401, '葫芦娃', 5000);

-- --------------------------------------------------------

--
-- 表的结构 `awd_ranks_detail`
--

CREATE TABLE `awd_ranks_detail` (
  `id` int(11) NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `groupname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int(10) NOT NULL,
  `target_id` int(11) NOT NULL,
  `target_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target_group` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` datetime NOT NULL,
  `arrangement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `awd_ranks_detail`
--

INSERT INTO `awd_ranks_detail` (`id`, `username`, `groupname`, `score`, `target_id`, `target_name`, `target_group`, `time`, `arrangement`) VALUES
(6, 'admin', 'admin', 50, 699, 'Pwn1', 'test5', '2021-02-22 14:19:51', 0);

-- --------------------------------------------------------

--
-- 表的结构 `challenge_list`
--

CREATE TABLE `challenge_list` (
  `group_id` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `ctf_exam_id` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int(11) NOT NULL,
  `hint` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` int(11) NOT NULL,
  `docker_flag` int(11) NOT NULL,
  `docker_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `docker_info` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_flag` int(11) NOT NULL,
  `file_path` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `flag` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `challenge_list`
--

INSERT INTO `challenge_list` (`group_id`, `id`, `ctf_exam_id`, `name`, `score`, `hint`, `type`, `docker_flag`, `docker_id`, `docker_info`, `file_flag`, `file_path`, `flag`, `date`) VALUES
(0, 33, 20, 'misc1', 100, 'misc1', 1, 0, NULL, NULL, 0, '', 'flag{misc1}', '2021-01-12 21:59:23'),
(0, 34, 21, 'web1', 100, 'web1', 0, 0, NULL, NULL, 0, '', 'flag{web1}', '2021-01-12 21:59:26'),
(0, 35, 22, 'crypto1', 200, 'crypto1', 2, 0, NULL, NULL, 0, '', 'flag{crypto1}', '2021-01-12 22:01:22'),
(0, 36, 23, 'Reverse1', 150, 'Reverse1', 3, 0, NULL, NULL, 0, '', 'flag{Reverse1}', '2021-01-12 22:01:24'),
(0, 37, 24, 'pwn1', 300, 'pwn1', 4, 0, NULL, NULL, 0, '', 'flag{pwn1}', '2021-01-12 22:01:28'),
(0, 38, 25, 'misc2', 300, 'misc2', 1, 0, NULL, NULL, 0, '', 'flag{misc2}', '2021-01-12 22:01:31'),
(0, 39, 31, 'web2', 200, 'easy web2', 0, 0, NULL, NULL, 0, '', 'flag{web2}', '2021-01-19 16:28:45'),
(0, 53, 35, 'easymisc1', 150, 'easymisc1 hhh!', 1, 0, 'None', '', 1, 'test.zip', 'flag{easymisc1}', '2021-02-05 13:58:17');

-- --------------------------------------------------------

--
-- 表的结构 `challenge_type_num`
--

CREATE TABLE `challenge_type_num` (
  `type_id` int(11) NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `challenge_type_num`
--

INSERT INTO `challenge_type_num` (`type_id`, `type`, `num`) VALUES
(2, 'Web', 2),
(3, 'Misc', 1),
(4, 'Crypto', 1),
(5, 'Reverse', 2),
(6, 'Pwn', 1);

-- --------------------------------------------------------

--
-- 表的结构 `competition`
--

CREATE TABLE `competition` (
  `id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `info` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `competition`
--

INSERT INTO `competition` (`id`, `status`, `name`, `info`, `start_date`, `end_date`) VALUES
(0, 0, '九江学院第一届网络安全大赛', 'zzz', '2021-02-11 20:45:00', '2021-02-28 20:45:00');

-- --------------------------------------------------------

--
-- 表的结构 `ctf_exam`
--

CREATE TABLE `ctf_exam` (
  `id` int(11) NOT NULL,
  `own_id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `hint` varchar(200) DEFAULT NULL,
  `base_score` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `flag_type` int(11) NOT NULL,
  `base_flag` varchar(100) NOT NULL,
  `file_flag` int(11) NOT NULL,
  `file_path` varchar(300) DEFAULT NULL,
  `docker_flag` int(11) NOT NULL,
  `docker_path` varchar(300) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `info` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `ctf_exam`
--

INSERT INTO `ctf_exam` (`id`, `own_id`, `type`, `name`, `hint`, `base_score`, `status`, `flag_type`, `base_flag`, `file_flag`, `file_path`, `docker_flag`, `docker_path`, `create_time`, `info`) VALUES
(20, 12, 1, 'misc1', 'misc1', 100, 1, 0, 'flag{misc1}', 0, '', 0, '', '2021-01-12 21:56:10', ''),
(21, 12, 0, 'web1', 'web1', 100, 1, 0, 'flag{web1}', 0, '', 0, '', '2021-01-12 21:59:14', ''),
(22, 12, 2, 'crypto1', 'crypto1', 200, 1, 0, 'flag{crypto1}', 0, '', 0, '', '2021-01-12 21:59:58', ''),
(23, 12, 3, 'Reverse1', 'Reverse1', 150, 1, 0, 'flag{Reverse1}', 0, '', 0, '', '2021-01-12 22:00:19', ''),
(24, 12, 4, 'pwn1', 'pwn1', 300, 1, 0, 'flag{pwn1}', 0, '', 0, '', '2021-01-12 22:00:40', ''),
(25, 12, 1, 'misc2', 'misc2', 300, 1, 0, 'flag{misc2}', 0, '', 0, '', '2021-01-12 22:01:03', ''),
(31, 21, 0, 'web2', 'easy web2', 200, 1, 0, 'flag{web2}', 0, '', 0, '', '2021-01-19 16:28:41', ''),
(34, 21, 1, 'python', 'python', 200, 1, 0, '123', 0, '', 1, 'EasyPython.zip', '2021-01-20 14:41:04', ''),
(35, 21, 1, 'easymisc1', 'easymisc1 hhh!', 150, 1, 0, 'flag{easymisc1}', 1, 'test.zip', 0, '', '2021-02-05 13:58:09', '');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `real_name` varchar(20) DEFAULT NULL,
  `role` int(11) NOT NULL DEFAULT 0,
  `status` int(11) DEFAULT 0,
  `password` char(32) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile` char(11) DEFAULT NULL,
  `class_id` varchar(20) DEFAULT NULL,
  `user_photo` varchar(200) DEFAULT NULL,
  `user_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `user_id`, `real_name`, `role`, `status`, `password`, `email`, `mobile`, `class_id`, `user_photo`, `user_name`) VALUES
(55, '20180201420', '管理员', 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'admin@qq.com', '18579266908', 'A1861', NULL, 'admin'),
(56, '20180201420', '贺述明', 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'hsmcool@163.com', '18579266908', 'A1861', NULL, 'hsm'),
(57, NULL, NULL, 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test1@hsm.cool', NULL, NULL, NULL, 'test1'),
(58, NULL, NULL, 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test2@cc.io', NULL, NULL, NULL, 'test2'),
(59, NULL, NULL, 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test3@qq.com', NULL, NULL, NULL, 'test3'),
(60, NULL, NULL, 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test4@qq.com', NULL, NULL, NULL, 'test4'),
(61, NULL, NULL, 0, 0, 'c22169dd8be57624603d20faf855a75f', '2329825358@qq.com', NULL, NULL, NULL, 'fzbangbangda'),
(62, NULL, NULL, 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test5@hsm.cool', NULL, NULL, NULL, 'test5'),
(63, NULL, NULL, 0, 0, 'e10adc3949ba59abbe56e057f20f883e', 'test123@qq.com', NULL, NULL, NULL, 'test123');

-- --------------------------------------------------------

--
-- 表的结构 `user_challenge_list`
--

CREATE TABLE `user_challenge_list` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `ctf_exam_id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `challenge_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `date` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_challenge_list`
--

INSERT INTO `user_challenge_list` (`id`, `group_id`, `ctf_exam_id`, `type`, `challenge_id`, `user_id`, `score`, `date`) VALUES
(68, 18, 21, 0, 34, 63, 100, '12:48:49'),
(69, 18, 25, 1, 38, 63, 300, '13:01:04'),
(70, 18, 20, 1, 33, 63, 100, '13:02:40'),
(71, 10, 21, 0, 34, 55, 100, '13:42:47'),
(72, 10, 31, 0, 39, 55, 200, '13:44:35');

-- --------------------------------------------------------

--
-- 表的结构 `user_ctf_docker_list`
--

CREATE TABLE `user_ctf_docker_list` (
  `id` int(11) NOT NULL,
  `challenge_id` int(11) NOT NULL,
  `docker_status` int(11) NOT NULL,
  `docker_info` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `user_group`
--

CREATE TABLE `user_group` (
  `group_id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `info` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `token` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_group`
--

INSERT INTO `user_group` (`group_id`, `name`, `info`, `user_id`, `create_time`, `token`) VALUES
(10, 'admin', 'admin yes', 55, '2021-02-16 15:54:57', NULL),
(11, 'HSM', 'HSM YES', 56, '2021-02-16 16:21:51', NULL),
(12, 'test1', 'test1', 57, '2021-02-22 05:14:26', NULL),
(13, 'test2', '', 58, '2021-02-22 05:15:08', NULL),
(14, 'test3', '', 59, '2021-02-22 05:44:28', NULL),
(15, 'test4', '', 60, '2021-02-22 05:45:03', NULL),
(16, 'test5', '', 62, '2021-02-22 05:46:46', NULL),
(18, 'test123', '', 63, '2021-02-24 11:33:12', NULL);

-- --------------------------------------------------------

--
-- 表的结构 `user_group_apply`
--

CREATE TABLE `user_group_apply` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_group_apply`
--

INSERT INTO `user_group_apply` (`id`, `user_id`, `group_id`) VALUES
(1, 34, 50),
(7, 55, 13);

-- --------------------------------------------------------

--
-- 表的结构 `user_group_list`
--

CREATE TABLE `user_group_list` (
  `id` int(11) NOT NULL,
  `g_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_group_list`
--

INSERT INTO `user_group_list` (`id`, `g_id`, `user_id`, `role`) VALUES
(44, 10, 55, 1),
(45, 11, 56, 1),
(46, 12, 57, 1),
(47, 13, 58, 1),
(48, 14, 59, 1),
(49, 15, 60, 1),
(50, 16, 62, 1);

-- --------------------------------------------------------

--
-- 表的结构 `user_notice`
--

CREATE TABLE `user_notice` (
  `id` int(11) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `info` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_notice`
--

INSERT INTO `user_notice` (`id`, `uid`, `info`, `date`) VALUES
(2, 0, '本届赛事期间，请大家留意裁判人员的电话（尾号2710），并积极配合，如果以任何理由拒接，无法沟通以及不配合裁判质询要求，将进行禁赛处理。比赛期间禁止以任何形式进行跨队交流，一起维护公平、清朗的竞赛环境。', '2020-12-27 00:00:00'),
(3, 0, '比赛时间：2020年12月26日10：00-18：00', '2020-12-27 00:00:00'),
(4, 0, '注意：请选手时刻关注比赛公告，大赛执行规则以比赛公告为准。', '2020-12-27 00:00:00'),
(6, 0, '注意：请选手时刻关注比赛公告，大赛执行规则以比赛公告为准。', '2020-12-27 00:00:00'),
(19, 21, '比赛过程中遇到问题请技术反馈到九江学院网络安全靶场实训平台团队', '2021-01-28 15:31:52');

-- --------------------------------------------------------

--
-- 表的结构 `user_score_list`
--

CREATE TABLE `user_score_list` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `gid` int(11) NOT NULL,
  `ctf_exam_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_score_list`
--

INSERT INTO `user_score_list` (`id`, `uid`, `gid`, `ctf_exam_id`, `score`, `date`) VALUES
(1, 15, 2, 1, 0, '0000-00-00 00:00:00'),
(2, 2, 1, 1, 40, '2020-12-10 15:17:33'),
(3, 2, 1, 2, 50, '2020-12-03 15:18:13'),
(4, 3, 3, 1, 50, '2020-12-04 15:21:45');

--
-- 转储表的索引
--

--
-- 表的索引 `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- 表的索引 `awd_config`
--
ALTER TABLE `awd_config`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `awd_config_ip_pool`
--
ALTER TABLE `awd_config_ip_pool`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `awd_exam`
--
ALTER TABLE `awd_exam`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `awd_exam_instance`
--
ALTER TABLE `awd_exam_instance`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `awd_ranks`
--
ALTER TABLE `awd_ranks`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `awd_ranks_detail`
--
ALTER TABLE `awd_ranks_detail`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `challenge_list`
--
ALTER TABLE `challenge_list`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `challenge_list_ctf_exam_id` (`ctf_exam_id`);

--
-- 表的索引 `challenge_type_num`
--
ALTER TABLE `challenge_type_num`
  ADD PRIMARY KEY (`type_id`);

--
-- 表的索引 `competition`
--
ALTER TABLE `competition`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `ctf_exam`
--
ALTER TABLE `ctf_exam`
  ADD PRIMARY KEY (`id`,`own_id`),
  ADD KEY `ctf_exam1` (`own_id`);

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`,`user_name`) USING BTREE;

--
-- 表的索引 `user_challenge_list`
--
ALTER TABLE `user_challenge_list`
  ADD PRIMARY KEY (`id`,`group_id`) USING BTREE,
  ADD KEY `group1` (`group_id`),
  ADD KEY `user_challenge_list_user` (`user_id`);

--
-- 表的索引 `user_ctf_docker_list`
--
ALTER TABLE `user_ctf_docker_list`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user_group`
--
ALTER TABLE `user_group`
  ADD PRIMARY KEY (`group_id`) USING BTREE;

--
-- 表的索引 `user_group_apply`
--
ALTER TABLE `user_group_apply`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user_group_list`
--
ALTER TABLE `user_group_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group` (`g_id`),
  ADD KEY `user` (`user_id`);

--
-- 表的索引 `user_notice`
--
ALTER TABLE `user_notice`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `user_score_list`
--
ALTER TABLE `user_score_list`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- 使用表AUTO_INCREMENT `awd_config`
--
ALTER TABLE `awd_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `awd_config_ip_pool`
--
ALTER TABLE `awd_config_ip_pool`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `awd_exam`
--
ALTER TABLE `awd_exam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- 使用表AUTO_INCREMENT `awd_exam_instance`
--
ALTER TABLE `awd_exam_instance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=852;

--
-- 使用表AUTO_INCREMENT `awd_ranks`
--
ALTER TABLE `awd_ranks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=402;

--
-- 使用表AUTO_INCREMENT `awd_ranks_detail`
--
ALTER TABLE `awd_ranks_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用表AUTO_INCREMENT `challenge_list`
--
ALTER TABLE `challenge_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- 使用表AUTO_INCREMENT `challenge_type_num`
--
ALTER TABLE `challenge_type_num`
  MODIFY `type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用表AUTO_INCREMENT `competition`
--
ALTER TABLE `competition`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `ctf_exam`
--
ALTER TABLE `ctf_exam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- 使用表AUTO_INCREMENT `user_challenge_list`
--
ALTER TABLE `user_challenge_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- 使用表AUTO_INCREMENT `user_ctf_docker_list`
--
ALTER TABLE `user_ctf_docker_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user_group`
--
ALTER TABLE `user_group`
  MODIFY `group_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- 使用表AUTO_INCREMENT `user_group_apply`
--
ALTER TABLE `user_group_apply`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用表AUTO_INCREMENT `user_group_list`
--
ALTER TABLE `user_group_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- 使用表AUTO_INCREMENT `user_notice`
--
ALTER TABLE `user_notice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用表AUTO_INCREMENT `user_score_list`
--
ALTER TABLE `user_score_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 限制导出的表
--

--
-- 限制表 `challenge_list`
--
ALTER TABLE `challenge_list`
  ADD CONSTRAINT `challenge_list_ctf_exam_id` FOREIGN KEY (`ctf_exam_id`) REFERENCES `ctf_exam` (`id`);

--
-- 限制表 `ctf_exam`
--
ALTER TABLE `ctf_exam`
  ADD CONSTRAINT `ctf_exam1` FOREIGN KEY (`own_id`) REFERENCES `admin` (`admin_id`);

--
-- 限制表 `user_challenge_list`
--
ALTER TABLE `user_challenge_list`
  ADD CONSTRAINT `group1` FOREIGN KEY (`group_id`) REFERENCES `user_group` (`group_id`),
  ADD CONSTRAINT `user_challenge_list_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- 限制表 `user_group_list`
--
ALTER TABLE `user_group_list`
  ADD CONSTRAINT `group` FOREIGN KEY (`g_id`) REFERENCES `user_group` (`group_id`),
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
