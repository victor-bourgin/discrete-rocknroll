import numpy as np
from scipy.special import erf

from .config import setup_logging
from .utils import rplus, denormalize_adhesion, normalize_adhesion


logger = setup_logging(__name__, "./logs/output.log")


def burst_frequency(friction_vel, kin_visco):
    """Computes the frequency of bursts i.e. the frequency at which the particle sees an upward velocity."""
    return 0.00658 * (friction_vel ** 2) / kin_visco


def aerodynamic_forces(radius, friction_vel, fluid_density, kin_visco):
    """
    Estimates the mean and fluctations of the aerodynamic forces applying on a particle by the flow.

    The mean lift and the fluctuations are estimated from experimental results. The mean drag is estimated using
    Stokes formula.
    """
    rp = rplus(radius, friction_vel, kin_visco)

    faero_mean = 10.45 * fluid_density * (kin_visco ** 2) * (1 + 300 * (rp ** -0.31)) * (rp ** 2.31)
    faero_fluct = (0.2 * faero_mean) ** 2

    return faero_mean, faero_fluct


def rate_binned(distrib, flow,):
    # De-normalize adhesion force
    fadh = denormalize_adhesion(distrib.centers, distrib.radius*1e-6, flow.surf_energy)

    # Compute the resuspension rate for each bin
    rate = resuspension_rate(fadh,
                             distrib.radius*1e-6,
                             flow.friction_vel,
                             flow.fluid_density,
                             flow.kin_visco,
                             )

    return rate


def resuspension_rate(fadh: np.array,
                      radius: float,
                      friction_vel: float,
                      fluid_density: float,
                      kin_visco: float,
                      ) -> np.array:

    # Estimate burst frequency and aero forces
    freq = burst_frequency(friction_vel, kin_visco)
    faero_mean, faero_fluct = aerodynamic_forces(radius, friction_vel, fluid_density, kin_visco)

    logger.debug(f"Burst frequency: {freq:.4f} s-1")
    logger.debug(f"Aerodynamic force: {faero_mean:.4e}")

    rate = freq * np.exp(-(fadh - faero_mean) ** 2 / (2 * faero_fluct)) / (
                0.5 * (1 + erf((fadh - faero_mean) / np.sqrt(2 * faero_fluct))))

    # The maximum resuspension rate is the burst frequency
    rate = np.where(rate > freq, freq, rate)

    return rate
