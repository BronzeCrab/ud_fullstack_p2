
# project 2

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;My code passes all test from **tournament_test.py**. I've just slightly
modified last test case (line 119) inside **tournament_test.py**,
because I've changed returned values of **swissPairings()** function,
so **swissPairings()** returns not only list of pairs, but also a tuple, which is necessary for 
the case of odd number of players. And that is why i've modified last test case.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I've done 2 first steps from extracredit - I've prevented rematch by **preventRematch()** function and  I'm giving free win to lonely player (**giveFreeWin()** function).
I've also added **prepare()** function which is necessary to delete or to add some players into the
table and **main()** function, **main()** function holds the tournament and calling functions from 
**gen_and_run_html.py**. And that functions draw names and winner's (red)  or looser's (blue) lines on
the canvas, using html. And then browser starts and renders it. So I've also added this visialization.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To begin just run `python tournament.py` (database tournament should be created)

