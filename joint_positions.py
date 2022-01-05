import math
import numpy as np
import matplotlib.pyplot as plt
import timeit
"""
Constants for movement, subject to change.
May also make hor_offset a non-constant to allow matplotlib to 
"animate" the wave moving from left to right.
"""
AMPLITUDE = 140
WAVELENGTH = 450
HOR_OFFSET = 0
VER_OFFSET = 0

SEG_LEN = 140
HEAD_LEN = 270
NUM_JOINTS = 6

def sine(x : float) -> float:
    """
    Trig Sine Function in the form f(x) = (a * sin((2pi/wv)*x + c)) + d
    :param x: angle in radians
    :return: sin value given the constants
    """

    return (AMPLITUDE * np.sin((2 * np.pi / WAVELENGTH) * x + HOR_OFFSET)) + VER_OFFSET

def find_joint_coords(sine_func) -> list:
    """
    Function using euclidean distance formula and sine function to solve the
    positions of each joint according to the given sine function. Assuming the
    snake is oriented with its head on the left hand side at x = 0, and all "tail"
    to the right of the head in positive x-axis.
    :param: sine function callable
    :return: array of tuples in format [(0, y_0), (x_1, y_1)...]
        representing position of each joint. y_0 representing the leftmost tip
        of the head of the snake, which will be x = 0.
    """

    result = [[0.0], [sine_func(0)]]

    for i in range(0, NUM_JOINTS):
        guessed_dist = 0.0
        min_x = 0.0 + result[0][i]
        max_x = 140.0 + result[0][i]
        guessed_x = 0.0
        # essentially estimate the x coordinate of the next joint in the sequence
        # getting down to +/- 1mm in precision to the ideal distance.
        while not ((guessed_dist <= SEG_LEN + 0.5) and (guessed_dist >= SEG_LEN - 0.5)
                   or (max_x - min_x <= 1.0)):
            guessed_x = ((max_x - min_x) / 5.0) + min_x
            # guessed_x = ((max_x + min_x) / 2.0)
            guessed_dist = math.sqrt((guessed_x - result[0][i])**2
                                     + (sine_func(guessed_x) - result[1][i])**2)
            if guessed_dist < SEG_LEN:
                min_x = guessed_x
            else:
                max_x = guessed_x
        result[0].append(guessed_x)
        result[1].append(sine_func(guessed_x))

    return result


if __name__ == "__main__":
    found_coords = find_joint_coords(sine)
    print(found_coords)
    print("Time taken: " + str(timeit.timeit(lambda: find_joint_coords(sine), number = 1)))

    plt.plot(found_coords[0], found_coords[1])

    sine_x = range(0, WAVELENGTH * 2)
    sine_y = []
    for i in sine_x:
        sine_y.append(sine(i))
    plt.plot(sine_x, sine_y)
    plt.xlim([0, 4 * AMPLITUDE])
    plt.ylim([-2 * AMPLITUDE, 2 * AMPLITUDE])
    plt.show()