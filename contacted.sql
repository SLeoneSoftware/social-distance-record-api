--
-- Schema for Contacted Database for Social Distancing Record
-- It's a pretty simple layout so far; nothing fancy.
-- Removed constraint CHECK (datemark LIKE '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]')
-- Removed constraint CHECK (timemark LIKE '[0-2][0-9]:[0-5][0-9]')
--

create table IF NOT EXISTS contacted(
user integer NOT NULL,
contacteduser integer NOT NULL,
datemark TEXT,
timemark TEXT,
FOREIGN KEY (user) REFERENCES users(id),
FOREIGN KEY (contacteduser) REFERENCES users(id)
)