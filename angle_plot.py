import angle_generation as ag
import numpy as np
import matplotlib.pyplot as plt
import math

def joint_angle(n):
    if n < 0 or n > ag.NUM_JOINTS - 1:
        raise Exception("invalid joint #, must be between 0 and %d, inclusive" % (ag.NUM_JOINTS - 1))

    angle_vals = []
    for i in range(0, ag.WAVELENGTH):
        coords = ag.find_joint_coords(
            lambda x: ag.AMPLITUDE * np.sin((2 * np.pi / ag.WAVELENGTH) * x
                                            - (2 * np.pi / ag.WAVELENGTH * i)))
        angle = math.acos(
            (coords[0][n + 1] - coords[0][n]) /
            math.dist((coords[0][n], coords[1][n]), (coords[0][n + 1], coords[1][n + 1])))
        # flip angle to negative if the second coordinate is "lower" on y axis compared to first coord
        if coords[1][n] > coords[1][n + 1]:
            angle = -angle
        angle_vals.append(angle * (180/math.pi))

    plt.plot(np.arange(0, ag.WAVELENGTH), angle_vals)
    plt.xlim([0, ag.WAVELENGTH])

    plt.show()

joint_angle(5)


"""
Next steps: recursively find the angle in respect to the last joint's angle

As we want the angle that each joint turns at, and when. 

"""

