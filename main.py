from rnr.distribution import DistributionBuilder

def main():
    # PARAMETERS
    nparts = int(10e9)
    radius = 5
    nbins = 50
    fmin = 0.0
    fmax = 1.0

    distrib = DistributionBuilder(nparts, nbins, fmin, fmax, pdf_args=(radius,)).distribution

    distrib.plot()

if __name__ == '__main__':
    main()