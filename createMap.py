import numpy as np

def createMap():
    horizontal_line = np.zeros((4, 124))

    ## Top row  (12 sets 28 high, 3 sets 14 high)
    # Add 12 sets of 28 high
    arr1 = np.ones((28, 4), dtype=int)
    arr0 = np.zeros((28, 4), dtype=int)
    temp = np.concatenate((arr1, arr0), axis=1)
    top = np.zeros((28,4), dtype=int)

    for i in range(12):
        top = np.concatenate((top, temp), axis=1)

    # Add 3 sets of 14 high
    arr1 = np.ones((14, 4), dtype=int)
    arr0 = np.zeros((14, 4), dtype=int)
    arr0_2 = np.zeros((14, 4), dtype=int)
    temp0 = np.concatenate((arr0_2, arr0), axis=0)
    temp1 = np.concatenate((arr0_2, arr1), axis=0)
    temp = np.concatenate((temp1, temp0), axis=1)
    for i in range(3):
        top = np.concatenate((top, temp), axis=1)
    # Top has the top part by here

    ## Middle row (15 sets 22 high)
    arr1 = np.ones((22, 4), dtype=int)
    arr0 = np.zeros((22, 4), dtype=int)
    temp = np.concatenate((arr1, arr0), axis=1)
    middle = np.zeros((22,4), dtype=int)

    for i in range(15):
        middle = np.concatenate((middle, temp), axis=1)
    # Mid has the middle part by here

    ## Bottom row (12 sets 20 high)
    bottom = np.zeros((20, 28), dtype=int)
    arr0 = np.zeros((20, 4), dtype=int)
    arr1 = np.ones((20, 4), dtype=int)
    temp = np.concatenate((arr1, arr0), axis=1)
    for i in range(12):
        bottom = np.concatenate((bottom, temp), axis=1)
    # Bottom has the bottom part by here

    ## Build the map
    final = np.concatenate((horizontal_line, top, horizontal_line, middle, horizontal_line, bottom, horizontal_line), axis=0)

    # Output final to map2.txt
    np.savetxt('map2.txt', final, fmt='%d', delimiter='')

    return final

# Call the function to create the map and output to map2.txt
createMap()