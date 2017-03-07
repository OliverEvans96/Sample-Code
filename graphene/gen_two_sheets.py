# Generate two parallel graphene sheets of different sizes

# Imports
from numpy import *
from lammps_gen import *
from os import system

# Simulation parameters
bounds = array([[-50,50],[-50,50],[-50,50]])
sim = Simulation(bounds)
sim_name = 'two_sheets'

# Lower Sheet
g1 = GrapheneSheet(sim,55,55)
g1.set_loc(0,0,0)

g1.set_bond_length(1)
g1.set_bond_strength(1e3)

g1.set_angle_measure(120)
g1.set_angle_strength(1e3)

g1.set_pair_length(1)
g1.set_pair_strength(1e-4)


# Upper Sheet
g2 = GrapheneSheet(sim,29,29)
g2.set_loc(0,0,5)

g2.set_bond_length(1.5)
g2.set_bond_strength(1e3)

g2.set_angle_measure(120)
g2.set_angle_strength(5e1)

g2.set_pair_length(1.5)
g2.set_pair_strength(1e-4)

# Save
sim.write('{}.data'.format(sim_name))

# Run Simulation
print("Starting simulation")
system('nohup mpirun -np 4 lammps < {}.in &> {}.log &'.format(sim_name,sim_name))
print("Job submitted")
