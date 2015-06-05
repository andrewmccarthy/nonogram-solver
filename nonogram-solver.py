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

def build_clue_sets(blocks, start, end):
    if not blocks:
        return [set()]
    res = []
    for s in range(start, end + 1 - (sum(blocks) + len(blocks) - 1)):
        base = set(range(s, s+blocks[0]))
        for ext in build_clue_sets(blocks[1:], s+blocks[0]+1, end):
            res.append(base | ext)
    return res

def solve(brd, cluesets, length):
    changed = False
    for line, clueset in enumerate(cluesets):
        known_unset = {x for x, v in enumerate(brd[line]) if v==0}
        known_yes = {x for x, v in enumerate(brd[line]) if v==1}
        known_no = {x for x, v in enumerate(brd[line]) if v==-1}

        # Get all possible options, remove ones that conflict with known state
        clueset = [x for x in clueset if known_yes <= x and x.isdisjoint(known_no)]
        cluesets[line] = clueset
        new_yes = set.intersection(*clueset) - known_yes
        for el in new_yes:
            brd[line][el] = 1
            changed = True

        new_no = known_unset - set.union(*clueset)
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

cluesets_x = [build_clue_sets(clues_x[i], 0, height) for i in range(width)]
cluesets_y = [build_clue_sets(clues_y[i], 0, width) for i in range(height)]

printboard(board)
again = True
count = 0
while again:
    # do clues_y
    again = solve(board, cluesets_y, width)

    # do clues_x
    board = flip(board)
    again = solve(board, cluesets_x, height) or again
    board = flip(board)
    printboard(board)
    count = count + 1

print(count)
