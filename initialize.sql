-- Remove the tables first so this script can safely be rerun.
-- posts must be removed before users because posts references users.
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- Create the users table.
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Create the posts table.
CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert 10 users.
INSERT INTO users (user_id, name, email, created_at)
VALUES (1, 'Alex Johnson', 'alex@example.com', '2026-09-01 09:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (2, 'Jordan Smith', 'jordan@example.com', '2026-09-02 10:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (3, 'Taylor Brown', 'taylor@example.com', '2026-09-03 11:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (4, 'Morgan Davis', 'morgan@example.com', '2026-09-04 12:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (5, 'Casey Wilson', 'casey@example.com', '2026-09-05 13:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (6, 'Jamie Miller', 'jamie@example.com', '2026-09-06 14:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (7, 'Riley Moore', 'riley@example.com', '2026-09-07 15:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (8, 'Cameron Lee', 'cameron@example.com', '2026-09-08 16:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (9, 'Avery Clark', 'avery@example.com', '2026-09-09 17:00:00');

INSERT INTO users (user_id, name, email, created_at)
VALUES (10, 'Parker Hall', 'parker@example.com', '2026-09-10 18:00:00');

-- Insert 10 posts.
INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (1, 1, 'First Post', 'This is the first post.', '2026-09-11 09:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (2, 1, 'SQL Practice', 'Learning how SQL tables work.', '2026-09-12 10:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (3, 2, 'Databases', 'Databases are useful for storing data.', '2026-09-13 11:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (4, 3, 'Python', 'Python can connect to MySQL.', '2026-09-14 12:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (5, 4, 'Data Engineering', 'Data engineering combines many tools.', '2026-09-15 13:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (6, 5, 'Pandas', 'Pandas is useful for working with tabular data.', '2026-09-16 14:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (7, 6, 'ETL', 'ETL means extract transform and load.', '2026-09-17 15:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (8, 7, 'MySQL', 'MySQL is a relational database system.', '2026-09-18 16:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (9, 8, 'Cloud Databases', 'Cloud databases can be accessed remotely.', '2026-09-19 17:00:00');

INSERT INTO posts (post_id, user_id, title, content, created_at)
VALUES (10, 9, 'Final Post', 'This is the final sample post.', '2026-09-20 18:00:00');