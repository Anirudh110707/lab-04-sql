-- Combine users and posts and return posts
-- belonging to the first five users.

SELECT
    users.user_id,
    users.name,
    users.email,
    posts.title,
    posts.created_at
FROM users
JOIN posts
    ON users.user_id = posts.user_id
WHERE users.user_id <= 5
ORDER BY posts.created_at;