import numpy as np
from time import time

from typing import List, Tuple
from numpy.typing import NDArray
from .distribution import Distribution
from .flow import Flow

from .config import setup_logging
from .model import rate_binned


class Simulation:

    _logger = setup_logging(__name__, "./logs/output.log")

    def __init__(self,
                 distribution: Distribution,
                 flow: Flow,
                 ) -> None:

        self.distribution = distribution
        self.flow = flow
        self.current_time = 0

    def run(self, duration: float, dt: float,) -> Tuple[NDArray, NDArray, NDArray]:
        """
        Advances the simulation by the given time, starting from the current simulation time.
        """
        # Initialize arrays
        time_array = np.arange(self.current_time, duration, dt)
        nsteps = len(time_array)

        # Output quantities
        total_parts = np.zeros_like(time_array)
        instant_rate = np.zeros_like(time_array)

        self._logger.info("Starting simulation...")
        tstart = time()

        for i in range(nsteps):
            change = rate_binned(self.distribution, self.flow, dt)
            change = np.where(change > self.distribution.count, self.distribution.count, change)

            total_parts[i] = self.distribution.partnumber
            instant_rate[i] = np.sum(change)

            self.distribution.count = self.distribution.count - change

        self._logger.info(f"Finished simulation in {time() - tstart:.2f}s")

        return time_array, total_parts, instant_rate
