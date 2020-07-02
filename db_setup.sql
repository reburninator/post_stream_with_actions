CREATE TABLE `tomc`.`post_queue` (
  `fullname` varchar(15) NOT NULL,
  `subreddit_name` varchar(30) NOT NULL,
  `username` varchar(25) NOT NULL,
  `number_of_reports` int NOT NULL DEFAULT '0',
  `ban_note` varchar(30) DEFAULT NULL,
  `permalink` varchar(256) DEFAULT NULL,
  `post_title` varchar(1024) DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `selftext` varchar(5000) DEFAULT NULL,
  `created_utc` bigint NOT NULL DEFAULT '0',
  `location` varchar(20) DEFAULT NULL,
  `message_id` bigint NOT NULL DEFAULT '0',
  `awaiting_action` int NOT NULL DEFAULT '1',
  `queued_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `streamed_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`fullname`)
);

CREATE TABLE `tomc`.`mod_action_history` (
  `mod_action_history_id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(15) NOT NULL,
  `subreddit_name` varchar(30) NOT NULL,
  `username` varchar(50) NOT NULL,
  `item_type` varchar(20) NOT NULL,
  `permalink` varchar(256) DEFAULT NULL,
  `mod_action` varchar(20) DEFAULT NULL,
  `mod_to_action` varchar(50) DEFAULT NULL,
  `mod_action_on` timestamp NULL DEFAULT NULL,
  `channel_id` bigint NOT NULL DEFAULT '0',
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `streamed_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`mod_action_history_id`)
);