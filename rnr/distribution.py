import matplotlib.pyplot as plt
import numpy as np
from time import time

from scipy.integrate import quad

from typing import Callable, Optional
from numpy.typing import NDArray

from .config import setup_logging
from .utils import biasi_params


# TODO: Check the validity domain when computing Biasi mean and stdv values.


class Distribution:
    def __init__(self,
                 radius: float,
                 count: NDArray[np.int_],
                 center: NDArray[np.float64],
                 edge: NDArray[np.float64],
                 width: NDArray[np.float64],
                 ) -> None:
        self.radius = radius
        self.count = count
        self.center = center
        self.edge = edge
        self.width = width

    @property
    def partnumber(self, ):
        return np.sum(self.count)

    @property
    def mean(self, ) -> float:
        return np.sum(self.center * self.count) / self.partnumber

    def plot(self, scale: str) -> None:
        # Clear figure
        plt.clf()

        plt.bar(self.center, self.count, width=self.width, )

        plt.yscale(scale)


class DistributionBuilder:
    _logger = setup_logging(__name__, "./logs/output.log")

    def __init__(self,
                 radius: float,
                 nparts: int,
                 nbins: int,
                 fmin: float,
                 fmax: float,
                 pdf: Optional[Callable] = None,
                 pdf_args: Optional[tuple] = None,
                 ) -> None:

        self.radius = radius
        self.nparts = nparts
        self.nbins = nbins
        self.fmin = fmin
        self.fmax = fmax

        # If the provided pdf is not callable, the program defaults to the default pdf.
        if callable(pdf):
            self.pdf = pdf
            self.pdf_args = pdf_args
        else:
            self.pdf = self._default_pdf
            self.pdf_args = biasi_params(radius)

            self._logger.info("Default pdf used.")
            self._logger.debug(f"mean: {self.pdf_args[0]}, stdv: {self.pdf_args[1]}")

    @staticmethod
    def _default_pdf(fadh_norm: float, mean: float, stdv: float) -> float:
        """Default probability function. It is a lognormal distrib expressed with the geometric parameters."""
        proba_density = (1 / np.sqrt(2 * np.pi)) * (1 / (fadh_norm * np.log(stdv))) * np.exp(
            -0.5 * (np.log(fadh_norm / mean) / np.log(stdv)) ** 2)

        return proba_density

    def generate(self, ) -> Distribution:
        """
        Generate a discretized ditribution using the provided probability density function.

        Return a Distribution object.
        """
        # Create bin edges, widths and centers
        edge = np.linspace(self.fmin, self.fmax, self.nbins + 1)

        width = edge[1:] - edge[:-1]
        center = np.mean([edge[:-1], edge[1:]], axis=0)

        self._logger.info("Generating particle distribution...")
        tstart = time()

        # Compute the bin probabilities
        count = np.zeros_like(center)
        for i in range(np.shape(count)[0]):
            count[i] = quad(self.pdf, edge[i], edge[i + 1], args=self.pdf_args)[0]

        # Normalize the bin probabilities and convert to integers
        count = count * self.nparts / np.sum(count)
        count = np.round(count).astype(int)

        # Instanciate the distribution
        distrib = Distribution(self.radius, count, center, edge, width)

        self._logger.info(f"Distribution generated in {time() - tstart:.2f} seconds.")
        self._logger.debug(
            f"Distrib stats: {distrib.partnumber} parts, {np.shape(distrib.count)[0]} bins, mean = {distrib.mean:.4f}")

        return distrib
