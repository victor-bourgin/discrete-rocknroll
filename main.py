import matplotlib.pyplot as plt

from rnr.distribution import DistributionBuilder

def main():
    # PARAMETERS
    nparts = int(1e6)
    radius = 5
    nbins = 50
    fmin = 0.0
    fmax = 1.0

    # Initialize adhesion distribution
    builder = DistributionBuilder(radius, nparts, nbins, fmin, fmax)
    distrib = builder.generate()

    # Plot distribution
    distrib.plot()
    plt.savefig("./figs/binned_distrib.pdf", dpi=300)


if __name__ == '__main__':
    main()