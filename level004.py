#! /usr/bin/env python
# -*- coding: utf-8 -*-

from level import BaseLevel

class Level(BaseLevel):
    """Level 1 of the PyMan Game"""

    def getLayout(self):
        return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 2, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

