--
-- Schema for Users Database for Social Distancing Record
-- It's a pretty simple layout so far; just includes users. Location is a composite attribute from my ER model; nothing else is fancy.
--


create table users(
id integer NOT NULL,
firstname varchar(255),
email  NVARCHAR(320),
phone varchar CHECK (phone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
zipcode integer CHECK (zipcode LIKE '[0-9][0-9][0-9][0-9][0-9]'),
PRIMARY KEY(id)
)