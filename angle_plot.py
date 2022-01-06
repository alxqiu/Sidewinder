import joint_positions as ag
import numpy as np
import pandas as pd
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

def relative_angle(n):
    if n < 0 or n > ag.NUM_JOINTS - 1:
        raise Exception("invalid joint #, must be between 0 and %d, inclusive" % (ag.NUM_JOINTS - 1))
    relative_plot = []
    for i in range(0, ag.WAVELENGTH):
        coords = ag.find_joint_coords(
            lambda x: ag.AMPLITUDE * np.sin((2 * np.pi / ag.WAVELENGTH) * x
                                            - (2 * np.pi / ag.WAVELENGTH * i)))
        # absolute angles are relative to x axis
        abs_angles = []
        for k in range(0, ag.NUM_JOINTS):
            angle = math.acos(
                (coords[0][k + 1] - coords[0][k]) /
                math.dist((coords[0][k], coords[1][k]), (coords[0][k + 1], coords[1][k + 1])))
            if coords[1][k] > coords[1][k + 1]:
                angle = -angle
            abs_angles.append(angle * (180 / math.pi))
        # relative angles are relative to the last angle
        # rel(0) = abs(0)
        # rel(k) = abs(k) - abs(k - 1)
        rel_angles = [abs_angles[0]]
        for k in range(1, ag.NUM_JOINTS):
            rel_angles.append(abs_angles[k] - abs_angles[k - 1])
        relative_plot.append(rel_angles[n])

    plt.plot(np.arange(0, ag.WAVELENGTH), relative_plot)
    plt.xlim([0, ag.WAVELENGTH])

    plt.show()

def record_relative_angles():
    # put it in a csv file using pandas
    # with leftmost column being the "ticks" at 5 unit intervals
    # and then have each column to its right be the i-th joint i = [0...NUM_JOINTS]
    init_data = {"tick": [5*i for i in range(0, int(ag.WAVELENGTH / 5))]}
    for i in range(0, ag.NUM_JOINTS):
        init_data[str(i)] = [0 for i in range(0, int(ag.WAVELENGTH / 5))]
    df = pd.DataFrame(data=init_data)

    for i in df["tick"].tolist():
        coords = ag.find_joint_coords(
            lambda x: ag.AMPLITUDE * np.sin((2 * np.pi / ag.WAVELENGTH) * x
                                            - (2 * np.pi / ag.WAVELENGTH * i)))
        abs_angles = []
        for k in range(0, ag.NUM_JOINTS):
            angle = math.acos(
                (coords[0][k + 1] - coords[0][k]) /
                math.dist((coords[0][k], coords[1][k]), (coords[0][k + 1], coords[1][k + 1])))
            if coords[1][k] > coords[1][k + 1]:
                angle = -angle
            abs_angles.append(angle * (180 / math.pi))
        rel_angles = [abs_angles[0]]
        for k in range(1, ag.NUM_JOINTS):
            rel_angles.append(abs_angles[k] - abs_angles[k - 1])
        for k in range(len(rel_angles)):
            # adjust i (tick) for the row index in dataframe
            df.at[i / 5, str(k)] = rel_angles[k]

    df.to_csv("relative_joints.csv", index=False)



if __name__ == "__main__":
    # joint_angle(0)
    # relative_angle(2)

    record_relative_angles()


"""
Next steps: recursively find the angle in respect to the last joint's angle

As we want the angle that each joint turns at, and when. 

"""

