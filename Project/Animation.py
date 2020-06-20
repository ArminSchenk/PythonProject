from Data_model import *
from matplotlib import pyplot as plt
from matplotlib import animation


# function that takes a population and animates the movement and status of its members
def make_animation(population):
    fig = plt.figure()
    ax = plt.axes(xlim=(0, population.room_size), ylim=(0, population.room_size))
    # 4 scatter plots with different color which express the different status of the members
    scat = [0] * 4
    scat[0] = ax.scatter([], [], c="blue", label="vulnerable")
    scat[1] = ax.scatter([], [], c="red", label="infected")
    scat[2] = ax.scatter([], [], c="green", label="cured")
    scat[3] = ax.scatter([], [], c="black", label="deceased")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, ncol=2)

    ani = animation.FuncAnimation(fig, animate, fargs=(scat, population), interval=100)
    plt.show()


# function that is called each iteration to change the position and color of the points in the animation
def animate(i, scat, population):
    points = [[], [], [], []]
    test = [0] * 4
    # assign each member to the points of the color which matches his status
    # if there is at least one member of a given status/color set the corresponding test value to 1
    for person in population.members:
        for status, i in zip(["vulnerable", "infected", "cured", "deceased"], range(4)):
            if person.status == status:
                points[i].append([person.x_pos, person.y_pos])
                test[i] = 1
                break

    # update the data for each scatter plot
    for i in range(4):
        # only if the test value of the scatter plot is 1 (which means there is at least one point of that color)
        if test[i]:
            scat[i].set_offsets(np.array(points[i]))

    # update status and location of all members of the population
    population.update_status()
    population.update_positions()
    return scat
