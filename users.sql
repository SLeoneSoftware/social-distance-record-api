--
-- Schema for Users Database for Social Distancing Record
-- It's a pretty simple layout so far; nothing fancy.
--


create table IF NOT EXISTS users(
id integer NOT NULL,
firstname varchar(255),
email  NVARCHAR(320),
phone varchar CHECK (phone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
zipcode integer CHECK (zipcode LIKE '[0-9][0-9][0-9][0-9][0-9]'),
latitude integer NOT NULL,
longitude integer NOT NULL,
PRIMARY KEY(id)
);
