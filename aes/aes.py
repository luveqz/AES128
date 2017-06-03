#!/usr/bin/env python3
# -*- coding: utf8 -*-
from tables import s_box, rcon
from utils import *

from copy import deepcopy

def key_expansion_core(row, i):
    rotate_row(row, -1)

    for j in range(4):
        row[j] = s_box[row[j]]

    row[0] ^= rcon[i]

def key_expansion(key, expanded_key):
    for i in range(16):
        expanded_key[i] = key[i]

    bytes_generated = 16
    rcon_i = 1
    tmp = []

    while bytes_generated < 176:
        tmp = get_last_4_bytes(expanded_key)

        if (bytes_generated % 16) == 0:
            key_expansion_core(tmp, rcon_i)
            rcon_i += 1

        add_last_4_bytes(expanded_key, tmp)
        bytes_generated += 4

def sub_bytes(state):
    old = deepcopy(state)
    for x in range(4):
        for y in range(4):
            state[x][y] = s_box[old[x][y]]

def shift_rows(state):
    old = deepcopy(state)
    for x in range(4):
        for y in range(4):
            y2 = (y - x) % 4
            state[x][y2] = old[x][y]

def mix_columns(state):
    c_matrix = state

    a_matrix = deepcopy(state)
    b_matrix = ((2, 3, 1, 1),
                (1, 2, 3, 1),
                (1, 1, 2, 3),
                (3, 1, 1, 2))

    for a_x in range(4):
        for b_y in range(4):
            dot_product = 0
            for i in range(4):
                dot_product ^= multiply(
                    a_matrix[i][a_x],
                    b_matrix[b_y][i]
                )
            c_matrix[b_y][a_x] = dot_product

def add_round_key(state, round_key):
    i = 0
    for x in range(4):
        for y in range(4):
            state[y][x] ^= round_key[i]
            i += 1

def encrypt(msg, key):
    expanded_key = [None] * 176
    state = new_matrix(4, 4)
    rounds = 10

    fill_state(state, msg)

    key_expansion(key, expanded_key)
    add_round_key(state, key)

    for i in range(1, rounds):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(
            state, expanded_key[16 * i:])

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, expanded_key[160:176])

    return state_to_string(state)


if __name__ == '__main__':
    msg = "Don't tell them."

    key =  [0x01, 0x02, 0x03, 0x04,
            0x05, 0x06, 0x07, 0x08,
            0x09, 0x0a, 0x0b, 0x0c,
            0x0d, 0x0e, 0x0f, 0x10]

    print(encrypt(msg, key))
