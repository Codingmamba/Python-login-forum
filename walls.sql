
INSERT INTO messages(user_id, message, created_at, updated_at)
VALUES
(1, "This should join with darnell", now(), now()),
(2, 'This is for nique', now(), now());

SELECT first_name FROM users WHERE first_name = 'Darnell';

SELECT * FROM users;

SELECT * FROM messages 
LEFT JOIN users ON messages.user_id=users.id
LEFT JOIN comments ON messages.user_id=users.id;

-- for the messages
SELECT users.first_name, messages.* FROM users INNER JOIN messages on messages.user_id=users.id;


-- for the comments
-- USER ID IS SESSION
-- 
-- 

DELETE from messages where id = 36;

select * from messages;


select * from comments;

-- SELECT * FROM users;
-- SELECT * FROM users where users.email = 'darnell@email.com' AND users.password = '1234567890';