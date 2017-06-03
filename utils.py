from tables import x2, x3

from copy import deepcopy

def multiply(a, b):
    if b == 2:
        return x2[a]
    if b == 3:
        return x3[a]
    return a

def set_offset(msg):
    msg += ' ' * (16 - len(msg))
    return msg

def fill_state(state, msg):
    msg = set_offset(msg)
    msg = bytes(msg, 'utf-8')

    i = 0
    for y in range(4):
        for x in range(4):
            state[x][y] = msg[i]
            i += 1

def new_matrix(rows, cols):
    return [[None for i in range(cols)] for i in range(rows)]

def get_last_4_bytes(array):
    length = len(array)
    offset = array.count(None)
    last_byte = length - offset
    return array[last_byte - 4: last_byte]

def add_last_4_bytes(expanded_key, tmp):
    last_byte = len(expanded_key) - expanded_key.count(None)
    last_first_row = last_byte - 16

    for i in range(4):
            expanded_key[last_byte + i] = \
                expanded_key[last_first_row + i] ^ tmp[i]

def rotate_row(row, rotation):
    old = deepcopy(row)
    for j in range(4):
        row[(j + rotation) % 4] = old[j]

def format_byte(hex_str):
    _hex = hex(hex_str)[2:]
    offset = '0' * (2 - len(_hex))
    return offset + _hex.upper()

def state_to_string(state):
    msg = ''
    for y in range(4):
        for x in range(4):
            msg += format_byte(state[x][y]) + ' '
    return msg.strip()
