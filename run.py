import sys

import matplotlib.pyplot as plt
import toml

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.plotting import plot_instant_rate, plot_remaining_fraction
from rnr.simulation import Simulation


def main():
    # Load config file
    with open(f"configs/{sys.argv[1]}.toml", "r") as f:
        config = toml.load(f)

    # Initialize adhesion distribution
    builder = DistributionBuilder(config["distribution"]["radius"],
                                  int(config["distribution"]["nparts"]),
                                  config["distribution"]["nbins"],
                                  config["distribution"]["fmin"],
                                  config["distribution"]["fmax"],
                                  )

    distrib = builder.generate()
    # Plot initial distribution
    distrib.plot(scale='log')
    plt.savefig("./figs/initial_distrib.pdf", dpi=300)

    # Initialize the flow
    flow = Flow(
                config["simulation"]["duration"],
                config["simulation"]["dt"],
                config["flow"]["spinup_time"],
                config["flow"]["friction_vel"],
                config["flow"]["fluid_density"],
                config["flow"]["kin_visco"],
                config["flow"]["surf_energy"],
                )

    # Instanciate simulation and run it
    sim = Simulation(distrib, flow)
    time, total_parts, instant_rate = sim.run()
    # Plot output
    plt.clf()
    plot_instant_rate(time, instant_rate)
    plt.savefig("figs/instant_rate.pdf", dpi=300)

    plt.clf()
    plot_remaining_fraction(time, total_parts)
    plt.savefig("figs/remaining_fraction.pdf", dpi=300)



if __name__ == "__main__":
    main()
