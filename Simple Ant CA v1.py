# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 13:59:19 2026

@author: Louie
"""

import numpy as np
from numpy.random import default_rng
rng = default_rng()

import matplotlib.pyplot as plt
from matplotlib import colormaps
import matplotlib.animation as ani


# Grid Setup

grid_X, grid_Y = 32, 32 # simulation dimensions

# cell grid states (numbers determine display colors)
c_ground   = 0  # dark blue
c_home     = 2  # dark orange
c_resource = 4  # dark green
cell_grid = np.full((grid_X, grid_Y), c_ground)

# ant grid states
a_standing_empty =  11 # light brown
a_decided_empty  =  10 # dark brown
a_standing_full  =  7  # light red
a_decided_full   =  6  # dark red
a_blank          = -1  # not drawn
ant_grid = np.full((grid_X, grid_Y), a_blank)

# trail grid states
t_home     =  1 # light orange
t_blank    = -1 # not drawn
trail_grid = np.full((grid_X, grid_Y), t_blank)

# 2x2 square of home cells
cell_grid[15:17, 15:17] = c_home

# random distribution of resources, not overlapping home area
resource_ct = 50
resource_cells = rng.integers(1, high=[grid_X, grid_Y], size=(resource_ct, 2))
rc_x, rc_y = resource_cells[:, 0], resource_cells[:, 1]

mask = ~((13 < rc_x) & (rc_x < 18) & (13 < rc_y) & (rc_y < 18))
cell_grid[rc_x[mask], rc_y[mask]] = c_resource



# Ant Script

# standing - moves randomly when empty, looks for nearby trail cells when full,
#            reacts to a resource (empty) or home cell (full)
# decided - transfers to next cell
# resource removed when picked up, home cells immutable
# trail cells are cleared when full ant walks over them, all trails are cleared when it reaches home

# spawn ant
x,y = 15,15
ant_grid[x][y] = a_standing_empty


def bounds_check(x, y):
    # check if input coordinates are in bounds
    return (0 < x) & (x < grid_X-1) & (0 < y) & (y < grid_Y-1)


def pick(options):
    # choose randomly between given array and output new x, new y
    index = rng.integers(low=0, high=len(options))
    return options[index][0], options[index][1]


def decide(x, y, isFull):

    # get 4 neighboring cells
    nbrs  = np.array([[0,1], [1,0], [0,-1], [-1,0]])
    nbrs += np.array([x, y])

    # add in bounds points to nbrs2
    in_bounds = bounds_check(nbrs[:,0], nbrs[:,1])
    nbrs      = nbrs[in_bounds]

    # if carrying resource check for trails and add to move options, otherwise give empty bool vector
    if isFull: trails = trail_grid[nbrs[:,0], nbrs[:,1]] == t_home
    else:      trails = np.array([], dtype=bool)

    # if trails found (or looked for) pick among them, otherwise pick move cell randomly
    if trails.any(): return pick(nbrs[trails])
    else:            return pick(nbrs)


def display_matrix(merged):
    ax.cla()
    ax.axis('off')
    ax.matshow(merged, cmap='tab20')


def frame_cycle(frame):
    global x
    global y
    global aim_x
    global aim_y

    # standing after movement frame:
    if ant_grid[x][y] == a_standing_empty:

        if cell_grid[x][y] == c_resource:     # empty and on resource: pick up

            cell_grid[x][y] = c_ground        # delete resource
            ant_grid[x][y]  = a_decided_full  # switch to full
            aim_x, aim_y = decide(x, y, True) # follow trail to home (true for full)

        else:                                  # no resource

            ant_grid[x][y] = a_decided_empty   # stay empty and switch to decided
            aim_x, aim_y = decide(x, y, False) # choose random move (false for empty)


    elif ant_grid[x][y] == a_standing_full:

        if cell_grid[x][y] == c_home:          # full and on home: drop

            trail_grid[...] = t_blank          # reset all trails
            ant_grid[x][y]  = a_decided_empty  # switch to empty
            aim_x, aim_y = decide(x, y, False) # choose random move (false for empty)

        else:                                 # not on home

            ant_grid[x][y] = a_decided_full   # stay full and switch to decided
            aim_x, aim_y = decide(x, y, True) # follow trail to home (true for full)


    # movement after decision frame:
    elif ant_grid[x][y] == a_decided_empty:

        trail_grid[x][y]       = t_home           # leave trail if looking for a resource
        ant_grid[x][y]         = a_blank          # remove ant form prev cell
        ant_grid[aim_x][aim_y] = a_standing_empty # set to standing in new cell
        x, y = aim_x, aim_y                       # update position

    elif ant_grid[x][y] == a_decided_full:

        trail_grid[x][y]       = t_blank          # remove trail when going home
        ant_grid[x][y]         = a_blank          # remove ant form prev cell
        ant_grid[aim_x][aim_y] = a_standing_full  # set to standing in new cell
        x, y = aim_x, aim_y                       # update position


    # display:
    merged = np.where(ant_grid == a_blank,  cell_grid,  ant_grid) # shows cell grid under ant grid
    merged = np.where(merged   == c_ground, trail_grid, merged  ) # shows trail grid under cell and ant grids
    merged = np.where(merged   == t_blank,  cell_grid,  merged  ) # background of c_ground instead of t_blank

    merged[grid_X-1, grid_Y-1] = 0 # color corrections
    merged[0       , 0       ] = 19

    display_matrix(merged)



frtotal = 450
fig, ax = plt.subplots()
anim = ani.FuncAnimation(fig, frame_cycle, frames=frtotal, interval=16.7, repeat=False)
# anim.save('Saca.gif', writer='pillow', fps=60) // gives white screen until file saved