#!/usr/bin/python
################################################################################
# UTILS CONTROLLER
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/07/2015 Original construction
################################################################################

from random import randrange

def sucky_uuid():
    hex_alpha_bet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

    uuid = ""
    
    for i in range(0, 8):
        uuid += hex_alpha_bet[randrange(0, 15, 1)]

    uuid += "-"

    for i in range(0, 4):
        uuid += hex_alpha_bet[randrange(0, 15, 1)]

    uuid += "-"

    for i in range(0, 4):
        uuid += hex_alpha_bet[randrange(0, 15, 1)]

    uuid += "-"

    for i in range(0, 4):
        uuid += hex_alpha_bet[randrange(0, 15, 1)]

    uuid += "-"

    for i in range(0, 12):
        uuid += hex_alpha_bet[randrange(0, 15, 1)]

    return uuid
