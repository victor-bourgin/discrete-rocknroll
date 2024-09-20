# Discrete Rock'n'Roll resuspension module

This is a Python implementation of the Rock'n'Roll particle resuspension model. The quasi-static formulation described in
[1] is used. 

# How to run it
First, make sure you have all the required packages installed. The list of packages can be found in the requirements.txt file.

This can be done in two ways. Using pip :

`pip install -r requirements.txt`

Using conda:

`conda create --name <env_name> --file requirements.txt`

Once that is done, you can set your parameters in the configs/config.toml file. The simulation is ran in the main.py file :

`python3 main.py`

# Upcoming features
- User-defined adhesion distribution
- User-defined aerodynamic forces
- Variable friction velocity
- More convenient plotting functions

# Reference
[1] M.W. Reeks, D. Hall,
Kinetic models for particle resuspension in turbulent flows: theory and measurement,
Journal of Aerosol Science,
Volume 32, Issue 1,
2001,
Pages 1-31,
ISSN 0021-8502,
https://doi.org/10.1016/S0021-8502(00)00063-X.
