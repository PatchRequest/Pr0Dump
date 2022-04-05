CREATE TABLE `users`(
    `id` INT NOT NULL,
    `currentName` VARCHAR(255) NOT NULL,
    `registered` INT NOT NULL,
    `uploadCount` INT NOT NULL,
    `score` INT NOT NULL,
    PRIMARY KEY (id)
); 

CREATE TABLE `posts`(
    `id` INT NOT NULL ,
    `userId` INT NOT NULL,
    `up` INT NOT NULL,
    `down` INT NOT NULL,
    `created` INT NOT NULL,
    `width` INT NOT NULL,
    `height` INT NOT NULL,
    `audio` INT NOT NULL,
    `flags` INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (userId) REFERENCES users(id)
);

CREATE TABLE   `comments`(
    `id` INT NOT NULL,
    `postId` INT NOT NULL,
    `parentId` INT NOT NULL,
    `userId` INT NOT NULL,
    `up` INT NOT NULL,
    `down` INT NOT NULL,
    `created` INT NOT NULL,
    `content` TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (postId) REFERENCES posts(id),
    FOREIGN KEY (userId) REFERENCES users(id)
);

CREATE TABLE   `tags`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE   `badges`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `image` VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE   `post_tags`(
    `postId` INT NOT NULL,
    `tagId` INT NOT NULL,
    `confidence` FLOAT NOT NULL,
    FOREIGN KEY (postId) REFERENCES posts(id),
    FOREIGN KEY (tagId) REFERENCES tags(id)
);

CREATE TABLE   `user_badges`(
    `userId` INT NOT NULL,
    `badgeId` INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (badgeId) REFERENCES badges(id)
);