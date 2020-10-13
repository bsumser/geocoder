import math
import numpy as np


def main():
    visited = False
    address = np.array([' main st ', ' main st ', ' main st ', ' bob ave ',
                        ' bob ave ', ' bob ave ', ' sam ', ' sam ', ' tim rd ',
                        ' tim rd ', ' tim rd ', ' tim rd '])

    key = np.array([], dtype=int)  # initializes empty array using numpy library

    start = 0  # starting element to make the comparison
    n = (len(address)-1)  # n = number of total elements in the address
    end = n  # ending element to make the comparison
    key_points(start, end, key, address)


def key_points(start, end, key, address):

    n = (len(address)-1)  # n = number of total elements in the address
    midpoint = int(math.ceil((end - start) / 2) + start)  # ceiling function to find midpoint
    # print('midpoint', midpoint)

    end = midpoint

    # 1 Base case(s) 0 turns are made, or we have reached the end of the points.
    if address[start] == address[n]:
        # print('case1')
        key = np.append(key, n)
        print_key(key, address)
        exit()

    # 2 midpoint doesn't match starting and starting point is next to end point
    if address[start] != address[midpoint] and (start+1) == end:
            key = np.append(key, start)
            start = start+1
            end = n
            key_points(start, end, key, address)

    # 3 midpoint doesn't match starting and starting point is not next to end point
    if address[start] != address[midpoint] and (start+1) != end:
        # print('case3')
        key_points(start, end, key, address)

    # 4 starting point matches midpoint
    if address[start] == address[midpoint]:
        # print('case4')
        start = midpoint
        end = n
        key_points(start,end, key, address)


def print_key(key, address): # key is the array holding the elements

    if len(key) == 1:
        print('No turns made')

    i = 0
    print('\nYour turns were made at the points of the first column and the streets of the second column: \n')
    while i < len(key):
        print( key[i], address[key[i]])
        i = i+1


if __name__ == "__main__":
    main()
