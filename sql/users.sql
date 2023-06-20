CREATE TABLE users(
	user_id int auto_increment primary key not null,
	fullname varchar(300) not null,
	user_uname varchar(100) not null,
    user_email varchar(300) not null,
    user_google_id varchar(300) not null,
	created_at datetime default current_timestamp,
	updated_at datetime default current_timestamp
);
