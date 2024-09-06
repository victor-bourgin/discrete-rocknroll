import numpy as np
from scipy.special import erf

from .utils import rplus, denormalize_adhesion


def burst_frequency(friction_vel, kin_visco):
    return 0.00658 * (friction_vel ** 2) / kin_visco


def aerodynamic_forces(radius, friction_vel, fluid_density, kin_visco):
    rp = rplus(radius, friction_vel, kin_visco)

    faero_mean = 10.45 * fluid_density * (kin_visco ** 2) * (1 + 300 * (rp ** -0.31)) * (rp ** 2.31)
    faero_fluct = (0.2 * faero_mean) ** 2

    return faero_mean, faero_fluct


def rate_binned(distrib, flow, dt):
    # De-normalize adhesion force
    fadh = denormalize_adhesion(distrib.centers, distrib.radius, flow.surf_energy)

    # Compute the resuspension rate for each bin
    rate = resuspension_rate(fadh,
                             distrib.radius,
                             flow.friction_vel,
                             flow.fluid_density,
                             flow.kin_visco,
                             flow.surf_energy)

    return rate * distrib.count * dt


def resuspension_rate(fadh, radius, friction_vel, fluid_density, kin_visco, surf_energy, threshold=1e-3):
    return []