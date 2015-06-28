
# project 2

### To run my project:

1. You need to run code from `tournament.sql`, it will create database `tournament` and also create table `players` in it. You can do it either from `psql` shell or using command `\i tournament.sql` to import whole file.
2. My `tournament.py` script contains only one module not from standart library - `psycopg2`. In order to install it you should execute `sudo apt-get install python-psycopg2` on Debian or if you're using Mac or Windows please check this official install guide out http://initd.org/psycopg/docs/install.html

### Decription of `tournament.py` script:

1. After installing psycopg2 and creating database with table you are ready to run `python tournament.py`. Function `main()` will be called. First of all you will be asked if you wish to erase the table and if you wish to add some players to the table. Then you'll specidy names of the players, that names would be fetched to the `players` table.
2. Next, `main()` will hold the tournament, will print initial standings of the players, results after each round and pairs for each round.
3. Also I have `gen_and_run_html.py` script. `main()` function from `tournament.py` will give current data for each round to the `gen_and_run_html.py`. And this script will draw names and winner's or looser's lines using html.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; So, to begin `python tournament.py`. It can be like this:
![Example tournament](https://cloud.githubusercontent.com/assets/5002732/8395720/da150f96-1d89-11e5-9e5f-3acde2896c72.png)

### Few notes:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;My code passes all tests from **tournament_test.py**. I've just slightly
modified last test case (line 119) inside **tournament_test.py**,
because I've changed returned values of **swissPairings()** function,
so **swissPairings()** retu rns not only list of pairs, but also a tuple, which is necessary for 
the case of odd number of players. And that is why i've modified last test case.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I've done 2 first steps from extracredit - I've prevented rematch by **preventRematch()** function and  I'm giving free win to lonely player (**giveFreeWin()** function).
I've also added **prepare()** function which is necessary to delete or to add some players into the
table and **main()** function, **main()** function holds the tournament and calling functions from 
**gen_and_run_html.py**. And that functions draw names and winner's (red)  or looser's (blue) lines on
the canvas, using html. And then browser starts and renders it. So I've also added this visialization. I dind't do another steps from extracredit. 


