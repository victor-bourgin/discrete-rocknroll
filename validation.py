import matplotlib.pyplot as plt
import numpy as np
import toml

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.simulation import Simulation
from rnr.utils import read_exp_res


def main():
    # Load config file
    with open("configs/validation.toml", "r") as f:
        config = toml.load(f)

    # Initialize velocity and remaining fraction arrays
    velocities = np.arange(0.1, 10, 0.01)
    fr = np.zeros([2, len(velocities)])

    # Read experimental data
    alumina10run10 = read_exp_res("data/alumina10_run10.csv")
    alumina20run8 = read_exp_res("data/alumina20_run8.csv")

    for (i, radius) in enumerate([5, 10]):

        # Initialize adhesion distribution
        builder = DistributionBuilder(radius,
                                      int(config["distribution"]["nparts"]),
                                      config["distribution"]["nbins"],
                                      config["distribution"]["fmin"],
                                      config["distribution"]["fmax"],
                                      )

        distrib = builder.generate()

        for (j, vel) in enumerate(velocities):
            # Initialize the flow
            flow = Flow(vel,
                        config["flow"]["fluid_density"],
                        config["flow"]["kin_visco"],
                        config["flow"]["surf_energy"],
                        )

            # Instanciate simulation and run it
            sim = Simulation(distrib, flow)
            _, total_parts, _ = sim.run(duration=1e0,
                                        dt=1e-1,
                                        )
            fr[i, j] = total_parts[-1]

    # Plot results
    plt.clf()

    # Create and adjust figure
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, constrained_layout=True)
    fig.set_figwidth(12)

    # Draw plots
    ax1.plot(velocities, fr[0]/(config["distribution"]["nparts"]+0), color='red', label='Discretized RnR')
    ax1.scatter(alumina10run10[0], alumina10run10[1], color='black', marker='s', facecolors='none', label='Exp. run 10')
    ax2.plot(velocities, fr[1]/(config["distribution"]["nparts"]+0), color='red', label='Discretized RnR')
    ax2.scatter(alumina20run8[0], alumina20run8[1], color='black', marker='s', facecolors='none', label='Exp. run 10')

    # Set limits
    ax1.set_xlim([0.1, 10])
    ax1.set_ylim([0.0, 1.0])
    ax2.set_xlim([0.1, 10])
    ax2.set_ylim([0.0, 1.0])

    # Set axis and grids
    ax1.grid()
    ax2.grid()
    ax1.set_xscale('log')
    ax2.set_xscale('log')

    # Set legends and titles
    ax1.legend()
    ax1.set_xlabel('friction velocity [m/s]')
    ax1.set_ylabel('remaining fraction')

    plt.savefig("figs/validation.pdf", dpi=300)


if __name__ == "__main__":
    main()
