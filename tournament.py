#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys
import gen_and_run_html
import random
import math
import copy

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # deleting all match records:
    cur.execute("ALTER TABLE players DROP COLUMN wins;")
    cur.execute("ALTER TABLE players ADD COLUMN wins int DEFAULT 0;")
    cur.execute("ALTER TABLE players DROP COLUMN matches;")
    cur.execute("ALTER TABLE players ADD COLUMN matches int DEFAULT 0;")
    # writing changes into db:
    conn.commit()
    # closing connection:
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # deleting all rows from players table
    cur.execute("DELETE FROM players")
    # resetting id_seq to 1 after clearing the table,
    # so next players will have id's started from 1
    # for the great justice
    cur.execute("ALTER SEQUENCE players_id_seq RESTART WITH 1;")
    # writing changes into db:
    conn.commit()
    # closing connection:
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # counting number of players:
    cur.execute("SELECT COUNT(*) FROM players;")
    number_of_players = cur.fetchone()[0]
    # closing connection:
    cur.close()
    conn.close()
    return number_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # adding player inside 'players' table:
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    # writing changes into db:
    conn.commit()
    # closing connection:
    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # selecting all info about players, ordering by wins:
    cur.execute("SELECT * FROM players ORDER BY wins DESC")
    standings = cur.fetchall()
     # closing connection:
    cur.close()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # updating info about players:
    cur.execute("""UPDATE players SET wins = wins + 1,
                   matches = matches + 1 WHERE id = (%s)""", (winner,))
    cur.execute("""UPDATE players SET 
                   matches = matches + 1 WHERE id = (%s)""", (loser,))
    # writing changes into db:
    conn.commit()
    # closing connection:
    cur.close()
    conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
        list_of_pairs: A list of tuples, looks like [(id1, name1, id2, name2),...]
          id1: the first player's unique id
          name1: the first player's name
          id2: the second player's unique id
          name2: the second player's name
        alone: tuple (id, name) with lonely player (if not exist empty tuple)
    """
    # retrieving list of tuples with all data
    standings = playerStandings()
    # reverse standings for more comfortable use of pop() function,
    # to pop() form top of the standings list
    standings = list(reversed(standings))
    # preparing returned value        
    list_of_pairs = []
    count = 0
    pair = []
    alone = ()
    while standings:
        # remove two players from 'standings' list
        # and appending them to list_of_pairs
        for count in xrange(2):
            # use try, because maybe we have odd number of players,
            # if it's true, then when I'll pop all
            # all the players except one and then
            # there will be a try to pop from empty list and it will be an IndexError
            try:
                pair.append(standings.pop()[0:2])
            except IndexError:
                # if there is a player (it will be the only one in 'pair' list) 
                # without pair, then give free win to him. In this case in 'pair'
                # list has just one player, so he is lonely, not paired
                lonely = pair 
                giveFreeWin(lonely[0][0])
                # appending to list of player lonely, he looks like just (id, name)
                alone = (lonely[0][0], lonely[0][1])
                break
        # if there wasn't any break inside for loop:        
        else:         
            pair = (pair[0][0], pair[0][1], pair[1][0], pair[1][1])
            list_of_pairs.append(pair)
            count = 0
            pair = []
    return list_of_pairs, alone


def giveFreeWin(unpaired):
    """Give free win to a player without a pair in case of odd number
    of players
    Args:
      unpaired: the id number of lonely player
    """
    # connecting to our db:
    conn = connect()
    # defining cursor:
    cur = conn.cursor()
    # giving free win:
    cur.execute("""UPDATE players SET wins = wins + 1,
                   matches = matches + 1 WHERE id = (%s)""", (unpaired,))
    # writing changes into db:
    conn.commit()
    # closing connection:
    cur.close()
    conn.close()


def preventRematch(all_pairs, pairs_list, alone):
    """Checking if any pair from current (for this round) pairs list is
       already is in all_pairs list (list of pairs for all rounds) and
       fixing this by shuffeling players
    Args:
      all_pairs: 'all_pairs' - list of all pairs for all rounds,
                  looks like [(id1, name1, id2, name2),()...]
      pairs_list: list of pairs for current round, looks like
                  [(id1, name1, id2, name2),()...]
      alone: tuple for lonely player, it is empty if even number of player or (id , name) if odd
    Returns:
      pairs_list: A list of fixed pairs [(id_fixed, name_fixed, id2, name2),()...]
    """
    for index, pair in enumerate(pairs_list):
        # take in considiration only paired players, not lonely
        i = 1
        reversed_pair = (pair[2], pair[3], pair[0], pair[1])
        while (pair in all_pairs or reversed_pair in all_pairs) and index + i <= len(pairs_list) - 1:
            if (pair[0], pair[1], pairs_list[index + i][0], pairs_list[index + i][1]) not in all_pairs\
            and (pairs_list[index + i][0], pairs_list[index + i][1], pair[0], pair[1]) not in all_pairs\
            and (pair[2], pair[3], pairs_list[index + i][2], pairs_list[index + i][3]) not in all_pairs\
            and (pairs_list[index + i][2], pairs_list[index + i][3], pair[2], pair[3]) not in all_pairs:
                pairs_list[index] = (pair[0], pair[1], pairs_list[index + i][0], pairs_list[index + i][1])
                pairs_list[index + i] = (pair[2], pair[3], pairs_list[index + i][2], pairs_list[index + i][3])
                break
            elif (pair[0], pair[1], pairs_list[index + i][2], pairs_list[index + i][3]) not in all_pairs\
            and (pairs_list[index + i][2], pairs_list[index + i][3], pair[0], pair[1]) not in all_pairs\
            and (pairs_list[index + i][0], pairs_list[index + i][1], pair[2], pair[3]) not in all_pairs\
            and (pair[2], pair[3], pairs_list[index + i][2], pairs_list[index + i][3]) not in all_pairs:
                pairs_list[index] = (pair[0], pair[1], pairs_list[index + i][2], pairs_list[index + i][3])
                pairs_list[index + i] = (pairs_list[index + i][0], pairs_list[index + i][1], pair[2], pair[3])
                break
            i += 1
        else:
            j = -1
            while (pair in all_pairs or reversed_pair in all_pairs) and index + j >= 0:
                if (pairs_list[index + j][2], pairs_list[index + j][3], pair[2], pair[3]) not in all_pairs\
                and (pair[2], pair[3], pairs_list[index + j][2], pairs_list[index + j][3]) not in all_pairs\
                and (pairs_list[index + j][0], pairs_list[index + j][1], pair[0], pair[1]) not in all_pairs\
                and (pair[0], pair[1], pairs_list[index + j][0], pairs_list[index + j][1]) not in all_pairs:
                    pairs_list[index] = (pairs_list[index + j][2], pairs_list[index + j][3], pair[2], pair[3])
                    pairs_list[index + j] = (pairs_list[index + j][0], pairs_list[index + j][1], pair[0], pair[1])
                    break
                elif (pairs_list[index + j][0], pairs_list[index + j][1], pair[2], pair[3]) not in all_pairs\
                and (pair[2], pair[3], pairs_list[index + j][0], pairs_list[index + j][1]) not in all_pairs\
                and (pair[0], pair[1], pairs_list[index + j][2], pairs_list[index + j][3]) not in all_pairs\
                and (pair[0], pair[1], pairs_list[index + j][2], pairs_list[index + j][3]) not in all_pairs:
                    pairs_list[index] = (pairs_list[index + j][0], pairs_list[index + j][1], pair[2], pair[3])
                    pairs_list[index + j] = (pair[0], pair[1], pairs_list[index + j][2], pairs_list[index + j][3])
                    break
                j -= 1
    else:
        if alone:
            k = 0
            print index
            # for lonely player also prevent rematch 'between him and himself' - i mean
            # prevent giving free win twice for one player
            while alone in all_pairs and index >= 0:
                if (pairs_list[index + k][2], pairs_list[index + k][3]) not in all_pairs and\
                (pairs_list[index + k][0], pairs_list[index + k][1], alone[0], alone[1]) not in all_pairs and\
                (alone[0], alone[1], pairs_list[index + k][0], pairs_list[index + k][1]) not in all_pairs:
                    temp1 = pairs_list[index + k][2]
                    temp2 = pairs_list[index + k][3]
                    pairs_list[index + k] = (pairs_list[index + k][0], pairs_list[index + k][1], alone[0], alone[1])
                    alone = (temp1, temp2)
                    break
                elif (pairs_list[index + k][0], pairs_list[index + k][1]) not in all_pairs and\
                (alone[0], alone[1], pairs_list[index + k][2], pairs_list[index + k][3]) not in all_pairs and\
                (pairs_list[index + k][0], pairs_list[index + k][1], alone[0], alone[1]) not in all_pairs:
                    temp1 = pairs_list[index + k][0]
                    temp2 = pairs_list[index + k][1]
                    pairs_list[index + k] = (alone[0], alone[1], pairs_list[index + k][2], pairs_list[index + k][3])
                    alone = (temp1, temp2)
                    break
                k -= 1
    return pairs_list, alone


def prepare():
    """Doing initial things - asking if user wants
       to delete or add players into the table"""
    # checking if user wants to delete all entities from table
    erase = raw_input("Would you like to erase players table? y/n\n")
    if erase.lower() == 'y':
        deletePlayers()
        number_of_players = raw_input("How many players will play?\n")
        number_of_players = int(number_of_players)
        if number_of_players <= 1:
            print "Incorrect number of players"
            sys.exit()    
        # registering players
        print "Please enter names of players, each name on new line"
        for i in xrange(number_of_players):
            name = raw_input("Please specify name: ")
            registerPlayer(name)
    else:
        add = raw_input("Would you like to add some new players? y/n\n")
        if add.lower() == 'y':
            how_many_to_add = raw_input("How many to add?\n")
            how_many_to_add = int(how_many_to_add)
            for i in xrange(how_many_to_add): 
                name = raw_input("Please specify name: ")
                registerPlayer(name)
        # deleting previos matches        
        deleteMatches()

# I've added this function to hold the tournament, had big feeling
# of incompleteness about our tournament without it...

def main():
    """Registering players and holds the tournament, printing
    standings after each round"""

    # preparing for the battle...
    prepare()     
    # printing initial state:
    print "Let's get ready to rumble (initial state)"
    standings = playerStandings()
    
    # printing players (initial list of names) and fetching function gen_html
    # inside gen_and_run_html.py,
    # tuples inside 'standings' list looks like (id, name, wins, matches), so 
    # to get names and id's i must extract element with index 1 and 0, so
    # 'names' is a list of player's ids and names

    id_n_names = []
    for player in standings:
        print player
        id_n_names.append((player[0], player[1]))

    # gen_html() function makes initial html file with initial list of names.   
    # Result of it returned to 'positions' variable
    # positions for now - a list, containing initial (before the first round)
    # positions of all names on canvas, it looks like
    # [(id1, name1, x_pos1, y_pos1),(id2, name2, x_pos2, y_pos2)...]

    positions = gen_and_run_html.gen_html(id_n_names)

    # holding the tournament    
    # number of rounds is log2 of number of players, so:
    # to get number of rounds i use math.ceil, it will give us rounded value
    # e.g. math.log() can produce 2.8422, but math.ceil() will return 3.0 from it,
    # then take int(), so then we would have 3 round exactly

    number_of_players = countPlayers()   
    rounds = int(math.ceil(math.log(number_of_players,2)))
    t_round = 1
    # 'all_pairs' - list of all pairs for all rounds, used for preventRematch() function
    all_pairs = []
    for i in xrange(rounds):
        # defining pairs for current round, each element inside 
        # 'pairs_list' looks like (id1, name1, id2, name2)
        # alone is a tuple looks like (id, name), or can be empty:
        pairs_list, alone = swissPairings()
        # calling preventRematch for each pair in current round. Only if
        # round of tournament != 1. Cause if we are in the begining, then there are
        # no pairs yet
        if t_round != 1:
            pairs_list, alone = preventRematch(all_pairs, pairs_list, alone)
        # appending pairs for this round to 'all_pairs' to fetch preventRematch() function
        for pair in pairs_list:
            all_pairs.append(pair)
        # appending also lonely player if exists:
        if alone:
            all_pairs.append(alone)
            print "lonely player for round number {0} is {1}" \
                  " he will has free win".format(t_round, alone) 
        print "\nPairs for %s round of torunament:" % t_round
        print pairs_list
        # randomly defining winners in pairs:
        # id in pairs_list has index 0 or 2
        loosers_list = []
        # save deepcopy of initial postitons list for this round
        pos_copy = copy.deepcopy(positions)
        for ind, pair in enumerate(pairs_list):
            # generate random number: 0 or 2
            randomed = 2*random.randrange(2)
            winner_id = pair[randomed]
            if randomed == 0:
                looser_id, looser_name = pair[2], pair[3]
                winner_name = pair[1]
            else:
                looser_id, looser_name = pair[0], pair[1]
                winner_name = pair[3]
            # reporting match results:
            reportMatch(winner_id, looser_id)
            # drawing winner and looser lines for this round inside html
            if ind == 0:
                positions = gen_and_run_html.drawLines(winner_id, looser_id,
                                                       positions, t_round, alone)
            else:
                positions = gen_and_run_html.drawLines(winner_id, looser_id,
                                                       positions, t_round)
            loosers_list.append(looser_id)
        # checking for collisions of the names on canvas after each round:
        col_detected, col_ids = gen_and_run_html.check_collisions(positions)
        if col_detected:
            positions = gen_and_run_html.fix_collisions(pos_copy, positions, 
                                                        col_ids, loosers_list, 
                                                        t_round)
        # got new positions of ends of lines, so can draw new list of names
        positions = gen_and_run_html.drawNames(positions, t_round)
        # printing out standings:
        print "\nResults after %s round:" % t_round
        standings = playerStandings()
        for player in standings:
            print player
        t_round += 1
    # finally run html:    
    gen_and_run_html.run_html("tournament.html")

if __name__ == '__main__':
    main()
   

