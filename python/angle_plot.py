import joint_positions as ag
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# TICKS are ticks per cycle
TICKS = 200
S_PER_TICK = 0.01
CYCLES = 7

def tick_joint_pos(i):
    return ag.find_joint_coords(
            lambda x: ag.AMPLITUDE *
                      np.sin((2 * np.pi / ag.WAVELENGTH) *
                             x - (2 * np.pi / ag.WAVELENGTH * i)))

def show_joint_angle(n):
    if n < 0 or n > ag.NUM_JOINTS - 1:
        raise Exception("invalid joint #, must be between 0 and %d, "
                        "inclusive" % (ag.NUM_JOINTS - 1))

    angle_vals = []
    for i in range(0, ag.WAVELENGTH):
        coords = tick_joint_pos(i)
        angle = math.acos(
            (coords[0][n + 1] - coords[0][n]) /
            math.dist((coords[0][n], coords[1][n]),
                      (coords[0][n + 1], coords[1][n + 1])))
        # flip angle to negative if the second coordinate is
        # "lower" on y axis compared to first coord
        if coords[1][n] > coords[1][n + 1]:
            angle = -angle
        angle_vals.append(angle * (180/math.pi))

    plt.plot(np.arange(0, ag.WAVELENGTH), angle_vals)
    plt.xlim([0, ag.WAVELENGTH])

    plt.show()


def show_relative_angle(n):
    if n < 0 or n > ag.NUM_JOINTS - 1:
        raise Exception("invalid joint #, must be between 0 and %d, "
                        "inclusive" % (ag.NUM_JOINTS - 1))
    relative_plot = []
    for i in range(0, ag.WAVELENGTH):
        coords = tick_joint_pos(i)
        # absolute angles are relative to x axis
        abs_angles = []
        for k in range(0, ag.NUM_JOINTS):
            angle = math.acos(
                (coords[0][k + 1] - coords[0][k]) /
                math.dist((coords[0][k], coords[1][k]),
                          (coords[0][k + 1], coords[1][k + 1])))
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


def record_relative_angles(isHorizontal):
    # keep it at 200 ticks, each being 0.01 second, or 10 ms
    init_data = {"tick": [S_PER_TICK * i for i in range(TICKS)]}
    for i in range(0, ag.NUM_JOINTS):
        init_data[str(i)] = [0 for i in range(TICKS)]
    df = pd.DataFrame(data=init_data)

    for i in range(TICKS):
        coords = tick_joint_pos(float(i * ag.WAVELENGTH / TICKS))
        abs_angles = []
        for k in range(0, ag.NUM_JOINTS):
            angle = math.acos(
                (coords[0][k + 1] - coords[0][k]) /
                math.dist((coords[0][k], coords[1][k]),
                          (coords[0][k + 1], coords[1][k + 1])))
            if coords[1][k] > coords[1][k + 1]:
                angle = -angle
            abs_angles.append(float(angle * (180.0 / math.pi)))
        rel_angles = [abs_angles[0]]
        for k in range(1, ag.NUM_JOINTS):
            rel_angles.append(abs_angles[k] - abs_angles[k - 1])
        for k in range(len(rel_angles)):
            # adjust i (tick) for the row index in dataframe
            df.at[i, str(k)] = rel_angles[k]

    # copy contents of first row, save for tick, into last row with tick
    # last_row_dict = {"tick": MS_PER_TICK * TICKS}
    # for i in range(0, ag.NUM_JOINTS):
    #     last_row_dict[str(i)] = [df.at[0, str(i)]]
    # last_row = pd.DataFrame(data=last_row_dict)
    # df = pd.concat((df, last_row))

    # repeat for CYCLES
    cycle_profile = pd.DataFrame(df, index=[i for i in range(TICKS)],
                                 columns = [str(i) for i in range(ag.NUM_JOINTS)])

    for i in range(1, CYCLES):
        for j in range(TICKS):
            cycle_profile.at[j, "tick"] = (j + (i * TICKS)) * S_PER_TICK
        df = pd.concat((df, cycle_profile))
        # re_adjust tick column


    filename = "vertical_joints.csv"
    if isHorizontal:
        filename = "horizontal_joints.csv"
    df.to_csv("../big_snake/" + filename, index=False)


if __name__ == "__main__":
    # show_absolute_angle(3)
    # show_relative_angle(0)

    record_relative_angles(True)



