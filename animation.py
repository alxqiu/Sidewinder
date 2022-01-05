import numpy as np
import joint_positions as ag
from matplotlib import pyplot as plt
from matplotlib import animation

plt.rcParams["figure.figsize"] = [7.50, 6.0]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()
xdata, ydata = [], []
xdata2, ydata2 = [], []
ln, = plt.plot([], [], color='yellow')
ln2, = plt.plot([], [], color='black')


def init_wave():
    ax.set_xlim(0, 8 * ag.AMPLITUDE)
    ax.set_ylim(-4 * ag.AMPLITUDE, 4 * ag.AMPLITUDE)
    ln.set_data([], [])
    ln2.set_data([], [])
    return ln, ln2


def update_wave(frame):
    found_coords = ag.find_joint_coords(
        lambda x: ag.AMPLITUDE * np.sin((2 * np.pi / ag.WAVELENGTH) * x - np.pi / 100 * frame))
    ln2.set_data(found_coords[0], found_coords[1])
    x = np.linspace(0, ag.WAVELENGTH * 2)
    y = ag.AMPLITUDE * np.sin((2 * np.pi / ag.WAVELENGTH) * x - np.pi / 100 * frame)
    ln.set_data(x, y)
    return ln, ln2


"""
So i want it to happen over 5 seconds,
and have each frame be 20ms, so that its 1000/20 = 50fps
so in total 200 frames over course of animation
"""


def do_wave_animation():
    anim = animation.FuncAnimation(fig, update_wave, init_func=init_wave, frames=200, interval=20, blit=True)
    plt.show()
    # f = r"C:\Users\Alex\PycharmProjects\Sidewinder\animation.gif"
    # writergif = animation.PillowWriter(fps=30)
    # anim.save(f, writer=writergif)

if __name__ == "__main__":
    do_wave_animation()
