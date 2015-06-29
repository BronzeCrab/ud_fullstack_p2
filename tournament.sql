-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- delete db if exist
DROP DATABASE IF EXISTS tournament;
-- Creating database "tournament"
CREATE DATABASE tournament;
-- connecting to tournament db:
\c tournament
-- Creating table players inside "tournament"
CREATE TABLE players(
   id      serial PRIMARY KEY,
   name    TEXT   NOT NULL,
   wins    int    DEFAULT 0,
   matches int    DEFAULT 0        
);
-- Also creating matches table
CREATE TABLE matches(
   round       int NOT NULL,
   winner_id   int REFERENCES players(id),
   looser_id   int REFERENCES players(id)
);
-- Create view for finall table:
-- I have a problem:
-- I've struggling to add also a column "looser_name" to this view,
-- but i can't do this, maybe you can help me with it?
CREATE VIEW matches_results AS
SELECT round, winner_id, players.name as winner_name, looser_id FROM matches
INNER JOIN players ON 
matches.winner_id = players.id;

