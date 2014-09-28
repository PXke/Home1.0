__author__ = 'berengere'

import random


def getCitation():
    mesCitations = open("./citations.txt", "r")
    mesCitations = mesCitations.readlines()
    rand = random.randint(0, len(mesCitations) - 1)
    return mesCitations[rand]