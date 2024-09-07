import numpy as np


def rplus(radius, friction_vel, kin_visco):
    return radius * friction_vel / kin_visco


def biasi_params(radius):
    mean = 0.016 - 0.0023 * (radius ** 0.545)
    stdv = 1.8 + 0.136 * (radius ** 1.4)
    return mean, stdv


def normalize_adhesion(fadh_norm, radius, surf_energy):
    return fadh_norm / ((3 / 2) * np.pi * surf_energy * radius)


def denormalize_adhesion(fadh_norm, radius, surf_energy):
    return fadh_norm * (3 / 2) * np.pi * surf_energy * radius
