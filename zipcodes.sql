--
-- Schema for Zipcodes Database
-- Used for converting latitude and longitude to zipcodes
--



create table IF NOT EXISTS zipcodes(
zipcode TEXT CHECK (zipcode NOT LIKE '%[^0-9]%') CHECK (length(zipcode) == 5),
latitude REAL NOT NULL,
longitude REAL NOT NULL,
PRIMARY KEY(zipcode)
);
