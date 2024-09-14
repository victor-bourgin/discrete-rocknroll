import matplotlib.pyplot as plt
import toml

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.simulation import Simulation

# TODO: Add plotting functionnalities


def main():
    # Load config file
    with open("configs/config.toml", "r") as f:
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
    flow = Flow(config["flow"]["friction_vel"],
                config["flow"]["fluid_density"],
                config["flow"]["kin_visco"],
                config["flow"]["surf_energy"],
                )

    # Instanciate simulation and run it
    sim = Simulation(distrib, flow)
    time, total_parts, instant_rate = sim.run(config["simulation"]["duration"],
                                              config["simulation"]["dt"],
                                              )


if __name__ == "__main__":
    main()
