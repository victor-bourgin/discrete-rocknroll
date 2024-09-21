import matplotlib.pyplot as plt


def plot_instant_rate(time, instant_rate):
    plt.plot(time, instant_rate, color='red')

    plt.xscale('log')
    plt.yscale('log')

    plt.grid(which='both', axis='x')
    plt.grid(axis='y')

    plt.xlabel('Time (s)')
    plt.ylabel('Nb of parts. detached')

def plot_remaining_fraction(time, total_parts):
    plt.plot(time, 1 - total_parts/max(total_parts), color='red')

    plt.xscale('log')

    plt.ylim([0, 1])

    plt.grid(which='both', axis='x')
    plt.grid(axis='y')

    plt.xlabel('Time (s)')
    plt.ylabel('Remaining fraction')