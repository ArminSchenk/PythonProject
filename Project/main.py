from Animation import *
from Simulation import *

pop1 = Population(number_persons=100, number_infected_persons=3, room_size=100, vel_max=1, infectious_range=10,
                  infection_probability=0.1, cure_probability=0.01, death_probability=0.01)

make_animation(pop1)
simulate_parameter_change(pop1, "infectious_range", 1, 10, 1)
simulate_parameter_change(pop1, "room_size", 100, 1000, 100)