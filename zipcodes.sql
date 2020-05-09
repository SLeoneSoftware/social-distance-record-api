--
-- Schema for Zipcodes Database
-- Used for converting latitude and longitude to zipcodes
--



create table IF NOT EXISTS zipcodes(
zipcode TEXT CHECK (length(zipcode) == 5),
latitude REAL NOT NULL,
longitude REAL NOT NULL
);
