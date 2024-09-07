import numpy as np
from scipy.special import erf

from typing import Tuple
from numpy.typing import NDArray
from .distribution import Distribution
from .flow import Flow

from .config import setup_logging
from .utils import rplus, denormalize_adhesion, normalize_adhesion


logger = setup_logging(__name__, "./logs/output.log")


def burst_frequency(friction_vel: float,
                    kin_visco: float,
                    ) -> float:
    """Computes the frequency of bursts i.e. the frequency at which the particle sees an upward velocity."""
    return 0.00658 * (friction_vel ** 2) / kin_visco


def aerodynamic_forces(radius: float,
                       friction_vel: float,
                       fluid_density: float,
                       kin_visco: float,
                       ) -> Tuple[float, float]:
    """
    Estimates the mean and fluctations of the aerodynamic forces applying on a particle by the flow.

    The mean lift and the fluctuations are estimated from experimental results. The mean drag is estimated using
    Stokes formula.
    """
    rp = rplus(radius, friction_vel, kin_visco)

    faero_mean = 10.45 * fluid_density * (kin_visco ** 2) * (1 + 300 * (rp ** -0.31)) * (rp ** 2.31)
    faero_fluct = (0.2 * faero_mean) ** 2

    return faero_mean, faero_fluct


def rate_binned(distrib: Distribution,
                flow: Flow,
                dt: float,
                threshold: float = 1e-3
                ) -> NDArray[np.float64]:
    """
    Wrapper for resuspension_rate. Handles denormalization of adhesion forces.

    Returns the average number of resuspension events expected to happen in each bin over time dt.
    """
    # De-normalize adhesion force
    fadh = denormalize_adhesion(distrib.centers, distrib.radius*1e-6, flow.surf_energy)

    # Compute the resuspension rate for each bin
    rate = resuspension_rate(fadh,
                             distrib.radius*1e-6,
                             flow.friction_vel,
                             flow.fluid_density,
                             flow.kin_visco,
                             )
    rate = rate * distrib.count * dt

    # If the rate is below the threshold, set to 0
    rate = np.where(rate < threshold, 0, rate)

    return rate


def resuspension_rate(fadh: NDArray,
                      radius: float,
                      friction_vel: float,
                      fluid_density: float,
                      kin_visco: float,
                      ) -> NDArray[np.float64]:
    """
    Estimate the resuspension rate for each value of adhesion force in the fadh array.

    The quasi-static Rock'n'Roll model by Reeks & Hall (2001) is used.
    """

    # Estimate burst frequency and aero forces
    freq = burst_frequency(friction_vel, kin_visco)
    faero_mean, faero_fluct = aerodynamic_forces(radius, friction_vel, fluid_density, kin_visco)

    rate = freq * np.exp(-(fadh - faero_mean) ** 2 / (2 * faero_fluct)) / (
                0.5 * (1 + erf((fadh - faero_mean) / np.sqrt(2 * faero_fluct))))

    # The maximum resuspension rate is the burst frequency
    rate = np.where(rate > freq, freq, rate)

    return rate
