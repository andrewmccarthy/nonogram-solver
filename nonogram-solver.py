#!/usr/bin/env python3

#width = 5
#height = 5
#clues_x = [[1], [5], [1], [3], [1,2]]
#clues_y = [[1,2], [2,1], [4], [1,1], [1]]
## 01011
## 11010
## 01111
## 01001
## 01000

width = 15
height = 25
clues_x = [
        [1],
        [1,5,8,2],
        [1,1,1,1,1,4,1],
        [1,1,2,1,1],
        [1,2,2,1,1,5],

        [1,1,5,1,10],
        [1,2,1,2,1,1],
        [1,1,2,1,2,1],
        [1,1,9],
        [2,1],

        [3,1],
        [2,3],
        [3,2,5],
        [3,6,2],
        [7]]

clues_y = [
        [7],
        [1,1],
        [3,3],
        [1,1],
        [2,2,1],

        [1,2,1],
        [1,2],
        [4,1],
        [4,1],
        [1,3,2],

        [1,3,1,1],
        [1,2,2],
        [1,1,1],
        [1,1,2,1],
        [1,1,2,1],

        [1,2,1,3],
        [1,1,1,2],
        [1,1,1,2],
        [1,1,1,1],
        [1,2,1,2],

        [1,3,1,2],
        [1,2,1,2],
        [1,2,1,3],
        [5,6],
        [3]]

board = [[0 for x in range(width)] for y in range(height)]


def printboard(board):
    for line in board:
        for el in line:
            if el == 0:
                print('?', end='')
            elif el == 1:
                print('#', end='')
            elif el == -1:
                print('.', end='')
            else:
                print('x', end='')
        print('')
    print('')

def it(blocks, start, end):
    if(len(blocks) < 1):
        return [set()]

    res = []
    for s in range(start, end + 1 - (sum(blocks) + len(blocks) - 1)):
        base = {x for x in range(s, s+blocks[0])}
        for ext in it(blocks[1:], s+blocks[0]+1, end):
            res.append(base | ext)
    return res

def solve(brd, clues, length):
    changed = False
    for line, c in enumerate(clues):
        known_unset = {x for x, v in enumerate(brd[line]) if v==0}
        known_yes = {x for x, v in enumerate(brd[line]) if v==1}
        known_no = {x for x, v in enumerate(brd[line]) if v==-1}

        # Get all possible options, remove ones that conflict with known state
        options = it(c, 0, length)
        options = [x for x in options if known_yes <= x and x.isdisjoint(known_no)]
        if options:
            new_yes = set.intersection(*options) - known_yes
            for el in new_yes:
                brd[line][el] = 1
                changed = True

            new_no = known_unset - set.union(*options)
            for el in new_no:
                brd[line][el] = -1
                changed = True
    return changed

def flip(board):
    newheight = len(board[0])
    newboard = [[] for x in range(newheight)]
    for line in board:
        for n, el in enumerate(line):
            newboard[n].append(el)
    return newboard

printboard(board)
again = True
count = 0
while again:
    again = False
    # do clues_y
    again = again or solve(board, clues_y, width)

    # do clues_x
    board = flip(board)
    again = again or solve(board, clues_x, height)
    board = flip(board)
    printboard(board)
    count = count + 1

print(count)
