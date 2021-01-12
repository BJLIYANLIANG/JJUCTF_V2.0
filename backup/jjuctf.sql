-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2021-01-12 14:03:23
-- 服务器版本： 10.5.8-MariaDB
-- PHP 版本： 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
(21, 'admin1', 'admin@qq.com', '123456', NULL, 'e00cf25ad42683b3df678c61f42c6bda', 1);

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
  `docker_info` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_flag` int(11) NOT NULL,
  `file_path` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `flag` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `challenge_list`
--

INSERT INTO `challenge_list` (`group_id`, `id`, `ctf_exam_id`, `name`, `score`, `hint`, `type`, `docker_flag`, `docker_info`, `file_flag`, `file_path`, `flag`, `date`) VALUES
(0, 33, 20, 'misc1', 100, 'misc1', 1, 0, NULL, 0, '', 'flag{misc1}', '2021-01-12 21:59:23'),
(0, 34, 21, 'web1', 100, 'web1', 0, 0, NULL, 0, '', 'flag{web1}', '2021-01-12 21:59:26'),
(0, 35, 22, 'crypto1', 200, 'crypto1', 2, 0, NULL, 0, '', 'flag{crypto1}', '2021-01-12 22:01:22'),
(0, 36, 23, 'Reverse1', 150, 'Reverse1', 3, 0, NULL, 0, '', 'flag{Reverse1}', '2021-01-12 22:01:24'),
(0, 37, 24, 'pwn1', 300, 'pwn1', 4, 0, NULL, 0, '', 'flag{pwn1}', '2021-01-12 22:01:28'),
(0, 38, 25, 'misc2', 300, 'misc2', 1, 0, NULL, 0, '', 'flag{misc2}', '2021-01-12 22:01:31');

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
(0, 0, '九江学院网络安全大赛', '九江学院网络安全大赛', '2021-01-05 20:46:00', '2021-01-21 20:47:00');

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
(25, 12, 1, 'misc2', 'misc2', 300, 1, 0, 'flag{misc2}', 0, '', 0, '', '2021-01-12 22:01:03', '');

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
(30, NULL, 'HSM', 0, 0, 'ff2e81f586eb5b79490294d06920f462', '905008677@qq.com', '18579266908', 'A1861', NULL, 'hsm'),
(33, NULL, 'hsm', 0, 0, '6f8c33aa2d7257eb96a3852b32e9ac9a', 'test1@qq.com', '1234567', 'A1861', NULL, 'hsm123'),
(34, NULL, NULL, 0, 0, '21232f297a57a5a743894a0e4a801fc3', 'admin@qq.com', NULL, NULL, NULL, 'admin');

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
(50, 'jjusec123', '1234', 0, '2021-01-05 16:54:16', NULL),
(55, 'admin', 'admin', 34, '2021-01-12 21:54:07', NULL);

-- --------------------------------------------------------

--
-- 表的结构 `user_group_apply`
--

CREATE TABLE `user_group_apply` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 表的结构 `user_group_list`
--

CREATE TABLE `user_group_list` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 转存表中的数据 `user_group_list`
--

INSERT INTO `user_group_list` (`id`, `group_id`, `user_id`, `role`) VALUES
(15, 50, 30, 1),
(16, 55, 34, 1);

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
(5, 0, '积分模式：动态积分模式（即每道题目的分值将根据解出队伍的数量动态变化），前3血没有额外奖励。', '2020-12-27 00:00:00'),
(6, 0, '注意：请选手时刻关注比赛公告，大赛执行规则以比赛公告为准。', '2020-12-27 00:00:00'),
(19, 12, 'hello world!', '2021-01-12 22:02:26');

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
  ADD PRIMARY KEY (`group_id`,`name`) USING BTREE;

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
  ADD KEY `group` (`group_id`),
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
-- 使用表AUTO_INCREMENT `challenge_list`
--
ALTER TABLE `challenge_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- 使用表AUTO_INCREMENT `user_challenge_list`
--
ALTER TABLE `user_challenge_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user_ctf_docker_list`
--
ALTER TABLE `user_ctf_docker_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user_group`
--
ALTER TABLE `user_group`
  MODIFY `group_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- 使用表AUTO_INCREMENT `user_group_apply`
--
ALTER TABLE `user_group_apply`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `user_group_list`
--
ALTER TABLE `user_group_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

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
  ADD CONSTRAINT `group` FOREIGN KEY (`group_id`) REFERENCES `user_group` (`group_id`),
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
