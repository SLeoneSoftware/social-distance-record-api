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
latitude integer NOT NULL,
longitude integer NOT NULL,
PRIMARY KEY(id)
);

create table contacted(
user integer NOT NULL,
contacteduser integer NOT NULL,
datemark varchar CHECK (datemark LIKE '[0-1][0-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]'),
timemark varchar CHECK (timemark LIKE '[0-2][0-9]:[0-5][0-9]'),
FOREIGN KEY (user) REFERENCES users(id),
FOREIGN KEY (contacteduser) REFERENCES users(id),
);
