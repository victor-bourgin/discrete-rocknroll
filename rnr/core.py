import matplotlib.pyplot as plt
import toml

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.simulation import Simulation

# TODO: Add plotting functionnalities


def single_run():
    # Load config file
    with open("config.toml", "r") as f:
        config = toml.load(f)

    # DISTRIBUTION PARAMETERS
    nparts = int(config["distribution"]["nparts"])
    radius = config["distribution"]["radius"]
    nbins = config["distribution"]["nbins"]
    fmin = config["distribution"]["fmin"]
    fmax = config["distribution"]["fmax"]

    # FLOW PARAMETERS
    friction_vel = config["flow"]["friction_vel"]
    fluid_density = config["flow"]["fluid_density"]
    kin_visco = config["flow"]["kin_visco"]
    surf_energy = config["flow"]["surf_energy"]

    # SIMULATION PARAMETERS
    duration = config["simulation"]["duration"]
    dt = config["simulation"]["dt"]

    # Initialize adhesion distribution
    builder = DistributionBuilder(radius, nparts, nbins, fmin, fmax)
    distrib = builder.generate()

    # Plot initial distribution
    distrib.plot(scale='log')
    plt.savefig("./figs/initial_distrib.pdf", dpi=300)

    # Initialize the flow
    flow = Flow(friction_vel, fluid_density, kin_visco, surf_energy)

    # Instanciate simulation and run it
    sim = Simulation(distrib, flow)
    time, total_parts, instant_rate = sim.run(duration, dt)


def validation():
    pass
