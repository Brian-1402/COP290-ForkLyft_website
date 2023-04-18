CREATE TABLE `contact_us` (
	`contact_id` int NOT NULL AUTO_INCREMENT,
	`user_id` int NOT NULL,
	`name_user` text NOT NULL,
	`mail` text NOT NULL,
	`message` text,
	PRIMARY KEY (`contact_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;


CREATE TABLE `menus` (
	`menu_id` int NOT NULL AUTO_INCREMENT,
	`image_url` text NOT NULL,
	`restaurant_id` int,
	`food_type` text NOT NULL,
	`food_name` text NOT NULL,
	`food_price` int NOT NULL,
	`food_desc` text,
	PRIMARY KEY (`menu_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE `my_cart` (
	`cart_id` int NOT NULL AUTO_INCREMENT,
	`item_id` int NOT NULL,
	`restaurant_id` int,
	`user_id` int NOT NULL,
	`order_id` int,
	`quantity` int NOT NULL DEFAULT '1',
	PRIMARY KEY (`cart_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE `orders` (
	`order_index` int NOT NULL AUTO_INCREMENT,
	`order_id` int NOT NULL,
	`restaurant_id` int NOT NULL,
	`user_id` int NOT NULL,
	`item_id` int NOT NULL,
	`quantity` int NOT NULL,
	PRIMARY KEY (`order_index`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE `pending_orders` (
	`p_order_id` int NOT NULL AUTO_INCREMENT,
	`user_id` int NOT NULL,
	`restaurant_id` int NOT NULL,
	`item_id` int NOT NULL,
	`quantity` int NOT NULL,
	`address` text,
	`order_id` int NOT NULL,
	PRIMARY KEY (`p_order_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;


CREATE TABLE `restaurants` (
	`restaurant_id` int NOT NULL AUTO_INCREMENT,
	`restaurant_name` text NOT NULL,
	`restaurant_location` text NOT NULL,
	`restaurant_rating_sum` int DEFAULT '1',
	`restaurant_rating_count` int DEFAULT '1',
	`restaurant_username` text NOT NULL,
	`restaurant_password` text NOT NULL,
	PRIMARY KEY (`restaurant_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;


CREATE TABLE `users` (
	`user_id` int NOT NULL AUTO_INCREMENT,
	`home` varchar(255),
	`work_add` text,
	`other_add` text,
	`username` text NOT NULL,
	`name_user` text NOT NULL,
	`user_pass` text NOT NULL,
	`mail` text,
	`phone_number` text,
	PRIMARY KEY (`user_id`)
) ENGINE InnoDB,
  CHARSET utf8mb4,
  COLLATE utf8mb4_0900_ai_ci;