from .distribution import DistributionBuilder

def main():
    # PARAMETERS
    nparts = 1000
    nbins = 10
    fmin = 0.0
    fmax = 0.5

    distrib = DistributionBuilder(nparts, nbins, fmin, fmax).distribution

    distrib.plot()

if __name__ == '__main__':
    main()