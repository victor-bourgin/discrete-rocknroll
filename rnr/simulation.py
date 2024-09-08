import numpy as np
from time import time

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

    def run(self, duration: float, dt: float,) -> None:

        # Initialize arrays
        time_array = np.arange(self.current_time, duration, dt)
        nsteps = len(time_array)

        self._logger.info("Starting simulation...")
        tstart = time()

        for i in range(nsteps):
            change = rate_binned(self.distribution, self.flow, dt)
            change = np.where(change > self.distribution.count, self.distribution.count, change)

            self.distribution.count = self.distribution.count - change

        self._logger.info(f"Finished simulation in {time() - tstart:.2f}s")
