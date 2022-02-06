-- test1.users definition

CREATE TABLE `users` (
  `id` varchar(100) NOT NULL DEFAULT uuid(),
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
