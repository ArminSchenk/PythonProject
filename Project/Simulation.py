from Data_model import *
from matplotlib import pyplot as plt


# recursive function that updates the status and locations of a population until there are no more infected members
# (which means the status of the members doesn't change anymore)
# the function returns a list with values for how many members of the population
# - didn't get infected and are therefore still vulnerable
# - did get infected but got cured
# - did get infected and died
def outbreak_dynamics(population):
    counts = [0] * 4
    # counts how many members have a certain status
    for i in range(population.number_persons):
        for status, j in zip(["vulnerable", "infected", "cured", "deceased"], range(4)):
            if population.members[i].status == status:
                counts[j] += 1
                break
    # if there are no more infected people return counts for 'vulnerable', 'cured' and 'deceased'
    if counts[1] == 0:
        return counts[:1] + counts[2:]
    # else update status and positions
    else:
        population.update_status()
        population.update_positions()
        return outbreak_dynamics(population)


# function that takes a population, the name of an argument which is needed to generate a population object
# and plots how the outbreak dynamics change when changing the given parameter
def simulate_parameter_change(population, parameter, start, end, step):
    args = [population.number_persons, population.number_infected_persons, population.room_size,
            population.vel_max, population.infectious_range, population.infection_probability,
            population.cure_probability, population.death_probability]

    parameters = ["number_persons", "number_infected_persons", "room_size", "vel_max", "infectious_range",
                  "infection_probability", "cure_probability", "death_probability"]

    # index which indicates which parameter should be changed
    index = parameters.index(parameter)

    # if "number_persons" or "number_infected_persons" get changed the values start, end and step must be integers
    if index in [0, 1]:
        if not isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
            raise TypeError("If you want to change parameter 'number_persons' or 'number_infected_persons' the "
                            "arguments 'start', 'end' and 'step' must be of type integer")

    x_values = np.arange(start, end + step, step)
    y_values = [[], [], []]

    # get outbreak dynamics for different values of the parameter
    for changed_parameter in x_values:
        # change value of parameter
        args[index] = changed_parameter
        population = Population(*args)
        counts = outbreak_dynamics(population)
        for i in range(3):
            y_values[i].append(counts[i])

    # plot three lines
    plt.plot(x_values, y_values[0], c="blue", label="vulnerable")
    plt.plot(x_values, y_values[1], c="green", label="cured")
    plt.plot(x_values, y_values[2], c="black", label="deceased")
    plt.legend()
    plt.xlabel("changed parameter: '" + parameter + "'")
    plt.show()
