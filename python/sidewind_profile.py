import joint_positions as jp


# builds dictionary in the form:
"""
{
ticks = [0.0, 0.01, ....]
h_joints = {0: [...], 1: [...], ...}
v_joints = {0: [...], 1: [...], ...}
}
"""

def build_profile(wait_time, cycles, h_amp, h_wv, v_amp, v_wv,
                h_joints = 6, v_joints = 5, seg_len = 280,
                  ticks_per_cycle = 200, s_per_tick = 0.01):
    return dict()