#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="script to demonstrate argparse usage")

    parser.add_argument("printme", help="The string to be printed")
    parser.add_argument("-r", "--repeat", help="number of times to print the string", type=int, default=1)

    arguments = parser.parse_args()

    for i in range(0, arguments.repeat):
        print(arguments.printme)

