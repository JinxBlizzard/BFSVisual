import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def displayMaze(maze, stdscr, path=[]):
    color_blue = curses.color_pair(1)
    color_red = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, 'X', color_red)
            else:
                stdscr.addstr(i, j * 2, cell, color_blue)


def startFinder(maze, start):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == start:
                return i, j


def findNeighbours(maze, row, col):
    neighbours = []

    if row > 0:
        neighbours.append((row-1, col))
    if row < len(maze) - 1:
        neighbours.append((row+1, col))
    if col > 0:
        neighbours.append((row, col - 1))
    if col < len(maze[0]) - 1:
        neighbours.append((row, col + 1))

    return neighbours


def pathFinder(maze, stdscr):
    start = 'O'
    end = 'X'

    spos = startFinder(maze, start)
    q = queue.Queue()
    q.put((spos, [spos]))

    vis = set()

    while not q.empty():
        curr, path = q.get()
        r, c = curr

        stdscr.clear()
        displayMaze(maze, stdscr, path)
        stdscr.refresh()
        # stdscr.getch() # key based traversal
        time.sleep(1) # time based traversal

        if maze[r][c] == end:
            return path

        neighbours = findNeighbours(maze, r, c)
        for neighbour in neighbours:
            r, c = neighbour
            if neighbour not in vis and maze[r][c] != '#':
                npath = path + [neighbour]
                q.put((neighbour, npath))
                vis.add(neighbour)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    path = pathFinder(maze, stdscr)
    stdscr.getch()


wrapper(main)
