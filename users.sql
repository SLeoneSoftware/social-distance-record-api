--
-- Schema for Users Database for Social Distancing Record
-- It's a pretty simple layout so far; nothing fancy.
--



create table IF NOT EXISTS users(
id integer NOT NULL,
firstname TEXT,
email  TEXT,
phone TEXT CHECK (phone NOT LIKE '%[^0-9]%') CHECK (length(phone) == 10),
zipcode TEXT CHECK (zipcode NOT LIKE '%[^0-9]%') CHECK (length(zipcode) == 5),
latitude integer NOT NULL,
longitude integer NOT NULL,
PRIMARY KEY(id)
);
