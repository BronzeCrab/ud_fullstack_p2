import webbrowser
import os
import fileinput
import sys
import random

def replaceAll(file,searchExp,replaceExp):
    found = False
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
            found = True
        sys.stdout.write(line)
    return found


def gen_html(data):

    """Making new html file for further visualization, Crearing initial
    list of the names on the canvas.

     Args:
      data: list of tuples with players ids and names, looks like [(id1,'name1'),(id2,'name2')...]
     Returns:
      positions: list of positions of right edge of the names on the canvas, looks like 
      [(id1, name1, xpos1, ypos1),(id2, name2, xpos2, ypos2)...]
    """

    f = open('tournament.html','w')

    element = """ctx.fillText("{name}", {x_pos}, {y_pos});"""
    elements = ""
    # initial positon of first elemnt on canvas:
    y = 1000
    x = 10
    # positions - a list, containing positions of all names on canvas, it looks like
    # [(id1, x_pos1, y_pos1),(id2, x_pos2, y_pos2)...]. This list will be returned by gen_html()
    positions = []
    for player_data in data:
        elements += element.format(
            name = player_data[1],
            y_pos = str(y),
            x_pos = str(x)
        )

        positions.append((player_data[0], player_data[1], x, y))
        # next names should lie lower on canvas, so increment y coordinate
        y += 27

    content = """
    <!DOCTYPE html>
    <html>
    <body>
    <canvas id="myCanvas" width="3000" height="3000" style="border:1px solid #d3d3d3;">
    Your browser does not support the HTML5 canvas tag.</canvas>

    <script>

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.textAlign = "start";
    ctx.font = "15px Verdana";

    {elements}
    //lines
    //next_name
    //placeholder

    </script>

    </body>
    </html>
    """
    content = content.format(elements = elements)
    f.write(content)
    f.close()
    return positions


def drawLines(winner_id, positions, t_round, looser_id=None):
    """Drawing lines for each round.

    Args:
      winner_id: id of the winner in certain pair,
      looser_id: id of the looser in certain pair,
      positions: list of positions of right edge of the names on the canvas, looks like 
      [(id1, name1, xpos1, ypos1),(id2, name2, xpos2, ypos2)...],
      t_round - number of tournament's round
    Returns:
      endPos: list of positions of right ends of lines, drawed in function,
      this list is necessary to draw new list of names. endPos looks like:
      [(id1, name1, xpos1, ypos1),(id2, name2, xpos2, ypos2)...]
    """

    lines_win = """
    ctx.beginPath();
    ctx.moveTo(ctx.measureText("{name}").width * {round} + {x_value}, {y_value});
    ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} - 100);
    ctx.strokeStyle = 'red';
    ctx.stroke();
    //next_line
    """
    lines_loose = """
    ctx.beginPath();
    ctx.moveTo(ctx.measureText("{name}").width * {round} + {x_value}, {y_value});
    ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} + 100);
    ctx.strokeStyle = 'blue';
    ctx.stroke();
    //next_line
    """

    add_lines = ""
    for index, player in enumerate(positions):
        if player[0] == winner_id or (player[0] == winner_id and looser_id == None):
            winner_name = player[1]
            x = player[2]
            y = player[3]
            add_lines = lines_win.format(
                name = winner_name,
                y_value = y,
                x_value = x,
                round = t_round
            )
            if not replaceAll("tournament.html", "//lines", add_lines):
                replaceAll("tournament.html", "//next_line", add_lines)
            # updating positions:
            x += 100
            y -= 100
            positions[index] = (player[0], player[1], x, y)
        elif player[0] == looser_id:
            looser_name = player[1]
            x = player[2]
            y = player[3]
            add_lines = lines_loose.format(
                name = looser_name,
                y_value = y,
                x_value = x,
                round = t_round
            )
            if not replaceAll("tournament.html", "//lines", add_lines):
                replaceAll("tournament.html", "//next_line", add_lines)
            # updating positions:
            x += 100
            y += 100
            positions[index] = (player[0], player[1], x, y)
    return positions


def check_collisions(positions):
    """Checking if names of the players overlap each other for certain round

    Args:
      positions: list of positions of right ends of lines, drawed in function drawLines(),
      this list is necessary to draw new list of names. endPos looks like:
      [(id1, name1, xpos1, ypos1),(id2, name2, xpos2, ypos2)...],
    Returns:
      col_detected: True if collision was detected
      collided_ids: list of ids of names that collides and boolean upper, looks like [(id1, upper),(id2, upper)...]
        upper: boolean, True, if name on the canvas with colided id is upper then that another name,
               which is in collision 
    """

    # for each player's data inside 'positions' list check if any other name overlap with it's name
    col_detected = False
    collided_ids = []
    for i in xrange(len(positions)):
        for j in xrange(len(positions)):
            if j != i and (abs(positions[i][3] - positions[j][3]) < 15 \
               and positions[j][0] not in [el[0] for el in collided_ids]):
                col_detected = True
                upper = False
                if positions[i][3] < positions[j][3]:
                    upper = True
                # append id's to list
                collided_ids.append((positions[i][0], upper))
    return col_detected, collided_ids

def fix_collisions(pos_copy, positions, col_ids, loosers_list, t_round):
    # redraw line on the canvas for collided names:
    for player in pos_copy:
        if player[0] in [el[0] for el in col_ids]:
            # get index of player[0] id:
            ind = [el[0] for el in col_ids].index(player[0])
            if player[0] in loosers_list:
                replace_line = """  ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} + 100);"""
                new_line = """  ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} + 100);"""
            else:
                replace_line = """  ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} - 100);"""
                new_line = """  ctx.lineTo(ctx.measureText("{name}").width * {round} + {x_value} + 100, {y_value} - 100);"""
            replace_line = replace_line.format(
            name = player[1],
            x_value = player[2],
            y_value = player[3],
            round = t_round
            )
            if col_ids[ind][1]:
                new_line = new_line.format(
                name = player[1],
                x_value = player[2],
                y_value = player[3] - 7,
                round = t_round
                )
            else:
                new_line = new_line.format(
                name = player[1],
                x_value = player[2],
                y_value = player[3] + 7,
                round = t_round
                )

            found = replaceAll("tournament.html", replace_line, new_line)
    # updating data in positions list after fixing lines
    for index, pl in enumerate(positions):
        if pl[0] in [el[0] for el in col_ids]:
            ind = [el[0] for el in col_ids].index(pl[0])
            if col_ids[ind][1]:
                positions[index] = (pl[0], pl[1], pl[2], pl[3] - 7)
            else:
                positions[index] = (pl[0], pl[1], pl[2], pl[3] + 7)
    return positions

def drawNames(positions, t_round):
    """Drawing player's names after each held round

    Args:
      positions: list of positions of right ends of lines, drawed in function drawLines(),
      this list is necessary to draw new list of names. endPos looks like:
      [(id1, name1, xpos1, ypos1),(id2, name2, xpos2, ypos2)...],
      t_round: current round of the tournament
    """
    
    element = """ctx.fillText("{name}", {x_pos} + ctx.measureText("{name}").width * {round} , {y_pos});"""
    elements = ""
    for player in positions:
        elements += element.format(
            name = player[1],
            x_pos = str(player[2]),
            y_pos = str(player[3]),
            round = t_round
        )
    for line in fileinput.input('tournament.html', inplace=1):
        print line,
        if line.startswith("    //placeholder"):
            print "//placeholder2"
      

    replaceAll("tournament.html", "//next_name", elements)
    replaceAll("tournament.html", "//placeholder2", "//next_name")

    return positions


def run_html(filename):
    # open the output file in the browser
    url = os.path.abspath(filename)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible





