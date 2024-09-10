import matplotlib.pyplot as plt

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.plot import plot_part_number, plot_instant_rate
from rnr.simulation import Simulation


def main():
    # DISTRIBUTION PARAMETERS
    nparts = int(1e9)
    radius = 5
    nbins = 1000
    fmin = 0.0
    fmax = 0.1

    # FLOW PARAMETERS
    friction_vel = 1.5
    fluid_density = 1.204
    kin_visco = 1.48e-5
    surf_energy = 0.15

    # SIMULATION PARAMETERS
    duration = 1e2
    dt = 1e0

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

    print(total_parts[-1]/nparts)

    # Plot final distribution
    distrib.plot(scale='linear')
    plt.savefig("./figs/final_distrib.pdf", dpi=300)

    plot_part_number(time, total_parts)
    plt.savefig("./figs/total_parts.pdf", dpi=300)

    plot_instant_rate(time, instant_rate)
    plt.savefig("./figs/instant_rate.pdf", dpi=300)


if __name__ == '__main__':
    main()
