--
-- Schema for Contacted Database for Social Distancing Record
-- It's a pretty simple layout so far; nothing fancy.
-- Replaced date and time markers with an actual datetime type attribute
--

create table IF NOT EXISTS contacted(
user integer NOT NULL,
contacteduser integer NOT NULL,
datemark DATETIME DEFAULT   CURRENT_TIMESTAMP,
FOREIGN KEY (user) REFERENCES users(id),
FOREIGN KEY (contacteduser) REFERENCES users(id)
)