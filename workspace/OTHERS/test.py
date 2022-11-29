#!/usr/bin/env python3

initialized = False

if not initialized:
    print("not yet initialized")
    initialized = True
    print("initialized")

if initialized:
    print("running initialized thing")

on_network = [0, 1,2,3,4,5,6]

mb_no = 2

string_list = str(on_network)

def string_to_list(string):
    #string = string[4:] # remove leading type signifier
    return [element.strip(",").strip("[").strip("]") for element in string.split()]

#print(string_to_list(string_list))

n = 7 /3
print(int(n))