import matplotlib.pyplot as plt
import numpy as np
import toml

from rnr.distribution import DistributionBuilder
from rnr.flow import Flow
from rnr.simulation import Simulation
from rnr.utils import read_exp_data


def main():
    # Load config file
    with open("configs/validation.toml", "r") as f:
        config = toml.load(f)

    # Initialize velocity and remaining fraction arrays
    velocities = np.arange(0.1, 10.0, 0.01)
    fr = np.zeros([2, len(velocities)])

    # Read experimental data
    exp_data = read_exp_data()

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
            flow = Flow(
                        1e1,
                        1e0,
                        0.0,
                        vel,
                        config["flow"]["fluid_density"],
                        config["flow"]["kin_visco"],
                        config["flow"]["surf_energy"],
                        )

            # Instanciate simulation and run it
            sim = Simulation(distrib, flow)
            _, total_parts, _ = sim.run()
            fr[i, j] = total_parts[-1]

    # Plot results
    plt.clf()

    # Create and adjust figure
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, constrained_layout=True)
    fig.set_figwidth(12)

    # Draw plots
    ax1.plot(velocities, fr[0]/(config["distribution"]["nparts"]+0), color='red',)
    ax1.scatter(exp_data[10][9][0], exp_data[10][9][1], color='blue', marker='^', facecolors='none', label='Exp. run 9')
    ax1.scatter(exp_data[10][10][0], exp_data[10][10][1], color='black', marker='s', facecolors='none', label='Exp. run 10')
    ax1.scatter(exp_data[10][15][0], exp_data[10][15][1], color='red', marker='o', facecolors='none', label='Exp. run 15')

    ax2.plot(velocities, fr[1]/(config["distribution"]["nparts"]+0), color='red', label='Discretized RnR')
    ax2.scatter(exp_data[20][7][0], exp_data[20][7][1], color='blue', marker='^', facecolors='none', label='Exp. run 7')
    ax2.scatter(exp_data[20][8][0], exp_data[20][8][1], color='black', marker='s', facecolors='none', label='Exp. run 7')
    ax2.scatter(exp_data[20][20][0], exp_data[20][20][1], color='red', marker='o', facecolors='none', label='Exp. run 20')

    # Set limits
    for ax in (ax1, ax2):
        # Set limits
        ax.set_xlim([0.1, 10])
        ax.set_ylim([0.0, 1.0])

        # Set axis and grids
        ax.grid(axis='y')
        ax.grid(which='both', axis='x')
        ax.set_xscale('log')

        # Set legends and titles
        ax.legend()
        ax.set_xlabel('friction velocity [m/s]')

    ax1.set_title('Alumina d=10µm')
    ax2.set_title('Alumina d=20µm')

    ax1.set_ylabel('remaining fraction')

    plt.savefig("figs/validation.pdf", dpi=300)

    # Integral for convergence study
    area1 = np.sum(fr[0]/(config["distribution"]["nparts"])*0.01)
    area2 = np.sum(fr[1]/(config["distribution"]["nparts"])*0.01)

    print(area1, area2)

    smoothness1 = np.sum(np.abs(fr[0,2:-1]-2*fr[0,1:-2]+fr[0,0:-3])/config["distribution"]["nparts"])
    smoothness2 = np.sum(np.abs(fr[1,2:-1]-2*fr[1,1:-2]+fr[1,0:-3])/config["distribution"]["nparts"])

    print(smoothness1*1000, smoothness2*1000)


if __name__ == "__main__":
    main()
