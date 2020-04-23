--
-- Schema for Contacted Database for Social Distancing Record
-- It's a pretty simple layout so far; nothing fancy.
--

create table IF NOT EXISTS contacted(
user integer NOT NULL,
contacteduser integer NOT NULL,
datemark varchar CHECK (datemark LIKE '[0-1][0-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]'),
timemark varchar CHECK (timemark LIKE '[0-2][0-9]:[0-5][0-9]'),
FOREIGN KEY (user) REFERENCES users(id),
FOREIGN KEY (contacteduser) REFERENCES users(id)
)