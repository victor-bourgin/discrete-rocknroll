import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import quad
from typing import Callable, Optional

from .config import setup_logging
from .utils import biasi_params

class Distribution:
    def __init__(self, count, centers, edges, width):
        self.count = count
        self.centers = centers
        self.edges = edges
        self.width = width

    def plot(self):
        # Clear figure
        plt.clf()

        plt.bar(self.centers, self.count, width=self.width,)

        plt.yscale('log')

        plt.savefig("./figs/binned_distrib.pdf", dpi=300)


class DistributionBuilder:

    _logger = setup_logging(__name__, "./logs/output.log")

    def __init__(self,
                 nparts: int,
                 nbins: int,
                 fmin: float,
                 fmax: float,
                 pdf: Optional[Callable] = None,
                 pdf_args: Optional[tuple] = None,
                 ) -> None:

        self.fmin = fmin
        self.fmax = fmax
        self.pdf = pdf or self._default_pdf
        self.pdf_args = pdf_args or ()
        self.distribution = self._generate_distribution(nparts, nbins)

    @staticmethod
    def _default_pdf(fadh_norm, radius):
        # Compute geometric mean and deviation from Biasia experiments.
        mean, stdv = biasi_params(radius)

        # Compute density for this
        proba_density = (1 / np.sqrt(2 * np.pi)) * (1 / (fadh_norm * np.log(stdv))) * np.exp(
            -0.5 * (np.log(fadh_norm / mean) / np.log(stdv)) ** 2)

        return proba_density

    def _generate_distribution(self, nparts, nbins):
        bin_edges = np.linspace(self.fmin, self.fmax, nbins)

        bin_widths = bin_edges[1:] - bin_edges[:-1]
        bin_centers = np.mean([bin_edges[:-1], bin_edges[1:]], axis=0)

        # Calculate the bin probabilities
        bin_counts = np.zeros_like(bin_centers)
        for i in range(np.shape(bin_counts)[0]):
            bin_counts[i] = quad(self.pdf, bin_edges[i], bin_edges[i + 1], args=self.pdf_args)[0]

        # Normalize the bin probabilities
        bin_counts = bin_counts * nparts / np.sum(bin_counts)
        bin_counts = np.where(bin_counts < 1, 0, bin_counts)
        bin_counts = np.round(bin_counts)

        distrib = Distribution(bin_counts, bin_centers, bin_edges, bin_widths)

        return distrib
