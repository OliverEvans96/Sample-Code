## Modeling the Light Field in Kelp Aquaculture

We're attempting to use radiative transfer theory to determine how neighboring kelp plants shade one another, which determines the optimal growing conditions, and maximum harvestable biomass.

kelp_model.cpp calculates the irradiance as a function of position as a PDE using SOR, ignoring scattering.

vispy_volume.py is used to visualize the results using vispy. Results are shown in volume_img

Full project description given in summary.pdf

Summer 2016
REU @ Clarkson University
w/ Dr. Shane Rogers
