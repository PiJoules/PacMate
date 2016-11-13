#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import math
import time
import socket
import threading
import SocketServer
import sys


#FOV = 70.42  # deg
FOV = 37.69
ABS_PLATE_RAD = 2.75  # 11" paper folded in half == diameter of color circle
HORIZ_RES = 1280
VERT_RES = 720


Y_RANGE_ABS = 187
X_RANGE_ABS = 72.25


GRID_W = 9  # num of blocks along width
GRID_L = 9

SOURCE_IP = "0.0.0.0"
TCP_PORT = 8000



back_row = [(785, 45), (850, 45), (920, 44), (998, 45), (1070, 43), (1130, 43), (1210, 44), (1279, 46), (1340, 47)]
right_side = [(1340, 47), (1510, 52), (1540, 56), (1600, 63), (1660, 72), (1704, 80), (1740, 90), (1770, 106)]
front_row = list(reversed([(1770, 106), (1625, 107), (1480, 110), (1310, 110), (1130, 110), (910, 113), (710, 113), (530, 114), (360, 112)]))
left_side = list(reversed([(470, 100), (540, 82), (600, 74), (640, 66), (700, 59), (728, 53), (760, 49), (760, 45)]))

BACK_LIM = 43
FRONT_LIM = 114
LEFT_LIM = 470
RIGHT_LIM = 1770

assert len(back_row) == len(front_row)
assert len(right_side) == len(left_side)


def normalize_x_off(x_off):
    norm_x_off = x_off - LEFT_LIM
    norm_x_off = float(norm_x_off) / (RIGHT_LIM - LEFT_LIM)
    return norm_x_off


def normalize_rad(rad):
    norm_rad = rad - BACK_LIM
    norm_rad = float(norm_rad) / (FRONT_LIM - BACK_LIM)
    return norm_rad


def grid_from_sides():
    grid = []

    for y in xrange(len(right_side)):
        grid.append([])
        for x in xrange(len(back_row)):
            x_offset = left_side[y][0] + x*(right_side[y][0] - left_side[y][0])/len(back_row)
            y_int = back_row[x][1]
            slope = (front_row[x][1] - back_row[x][1])/len(left_side)
            rad = y_int + y*slope

            grid[y].append((x_offset, rad))
    return grid


GRID = grid_from_sides()
MEAN_RADS = [0] * len(right_side)
for y, row in enumerate(GRID):
    s = 0
    for x_off, rad in row:
        s += rad
    MEAN_RADS[y] = s / len(back_row)
print(MEAN_RADS)

def nearest_coord(grid, x_off, rad):
    min_dist = float("Inf")
    min_coord = (0,0)


    for y, row in enumerate(grid):
        if MEAN_RADS[y] > rad:
            for x, pair in enumerate(row):
                if pair[0] > x_off:
                    return (x, y)
            break

    return (len(grid[0])-1, len(grid)-1)



def latest_data():
    while True:
        line = sys.stdin.readline().strip()
        print("latest_data:", line)

        x_off, rad = line.split(",")
        x_off = int(x_off)
        rad = int(rad)

        # Ignore ones that are out of bounds
        if x_off < LEFT_LIM or x_off > RIGHT_LIM:
            continue
        if rad < BACK_LIM or rad > FRONT_LIM:
            continue

        print("x_off: {}, rad: {}".format(x_off, rad))
        coord = nearest_coord(GRID, x_off, rad)

        print("coord:", coord)


def test_coords():
    server = ThreadedTCPServer((SOURCE_IP, TCP_PORT), ThreadedTCPRequestHandler)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    while True:
        time.sleep(1)


"""
1st attempt
"""


def img_to_absolute(x_off, rad):
    """
    x_off: x offset from left of img in pixels
    rad: radius of circle in pixels

    output is in inches
    """
    L = HORIZ_RES / rad * ABS_PLATE_RAD
    y = (L/2)/math.tan(math.radians(FOV))
    x = x_off / HORIZ_RES * L
    return x, y


def abs_to_grid(x, y):
    x = int(x * GRID_W / X_RANGE_ABS)
    y = int(y * GRID_L / Y_RANGE_ABS)
    return x, y


def in_to_ft(inches):
    return inches / 12.0


def main():
    x, y = img_to_absolute(265, 7)
    print(x, y)
    print(in_to_ft(x), in_to_ft(y))
    print(abs_to_grid(x, y))
    return 0


if __name__ == "__main__":
    #main()
    #test_coords()
    latest_data()

