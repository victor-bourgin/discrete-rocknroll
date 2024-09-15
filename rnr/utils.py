import csv
import os
import re

import numpy as np


def rplus(radius, friction_vel, kin_visco):
    return radius * friction_vel / kin_visco


def biasi_params(radius):
    mean = 0.016 - 0.0023 * (radius ** 0.545)
    stdv = 1.8 + 0.136 * (radius ** 1.4)
    return mean, stdv


def normalize_adhesion(fadh_norm, radius, surf_energy):
    return fadh_norm / ((3 / 2) * np.pi * surf_energy * radius)


def denormalize_adhesion(fadh_norm, radius, surf_energy):
    return fadh_norm * (3 / 2) * np.pi * surf_energy * radius


def read_exp_data() -> dict:
    # Name pattern of the exp data files
    pattern = re.compile(r"alumina(\d+)_run(\d+)\.csv")

    data = {}

    for filename in os.listdir("data/"):
        match = pattern.match(filename)
        # Extract the diameter and run number
        if match:
            diameter = int(match.group(1))
            run_nb = int(match.group(2))

            # Initialize data[diameter] if it doesn't exist
            if diameter not in data:
                data[diameter] = {}

            # Read data from file and store it
            with open(f"data/{filename}", mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                data[diameter][run_nb] = [[], []]

                for row in reader:
                    data[diameter][run_nb][0].append(float(row[0]))
                    data[diameter][run_nb][1].append(float(row[1]))
    return data
