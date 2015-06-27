-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Creating database "tournament"
CREATE DATABASE tournament;
-- connecting to tournament db:
\c tournament
-- Creating table players inside "tournament"
CREATE TABLE players(
   id      serial PRIMARY KEY  NOT NULL,
   name    TEXT   NOT NULL,
   wins    int    DEFAULT 0,
   matches int    DEFAULT 0        
);

