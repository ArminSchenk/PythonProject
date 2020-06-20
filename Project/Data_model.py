import numpy as np


# class for the individual persons in a population
# each person has a location (x and y), a velocity (in x and y direction)
# and a status (vulnerable, infected, cured or deceased)
class Person:
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.status = "vulnerable"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel

    # function to calculate the distance between two persons
    def dist(self, other):
        return np.sqrt((self.x_pos - other.x_pos) ** 2 + (self.y_pos - other.y_pos) ** 2)


# class to simulate a population:
# number_persons: how many persons should be in the population
# number_infected_persons: how many of those should be infected at the start
# room_size: members of the population exist and move in a square of this size
# vel_max: determines how far a person can move in x or y direction per iteration
# infectious_range: the range in which an infected person can infect a vulnerable one
# infection_probability: the probability that an infected person infects a vulnerable one per iteration
# cure_probability: the probability that an infected person gets cured
# death_probability: the probability that an infected person dies
class Population:
    def __init__(self, number_persons, number_infected_persons, room_size, vel_max, infectious_range,
                 infection_probability, cure_probability, death_probability):

        self.number_persons = number_persons
        self.number_infected_persons = number_infected_persons
        self.room_size = room_size
        self.vel_max = vel_max
        self.infectious_range = infectious_range
        self.infection_probability = infection_probability
        self.cure_probability = cure_probability
        self.death_probability = death_probability

        # create {number_persons} persons with random location and velocity and save them in a list
        self.members = [Person(np.random.random() * room_size, np.random.random() * room_size,
                               (np.random.random() - 0.5) * 2 * vel_max,
                               (np.random.random() - 0.5) * 2 * vel_max) for i in range(number_persons)]
        # infect {number_infected_persons} randomly chosen persons
        for i in np.random.choice(range(number_persons), number_infected_persons, replace=False):
            self.members[i].status = "infected"

    # function to update the status of all members of a population
    def update_status(self):
        ind = []
        # go through all members
        for i in range(self.number_persons):
            # is the member i infected?
            if self.members[i].status == "infected":
                # if yes, go through all other members
                for j in range(self.number_persons):
                    # is the other member vulnerable?
                    if self.members[j].status == "vulnerable":
                        # is the other member in the infectious range of the first?
                        if self.members[i].dist(self.members[j]) <= self.infectious_range:
                            # does he get infected?
                            if np.random.random() <= self.infection_probability:
                                ind.append(j)
                # does the infected member get cured?
                if np.random.random() <= self.cure_probability:
                    self.members[i].status = "cured"
                # does the infected person die?
                elif np.random.random() <= self.death_probability:
                    self.members[i].status = "deceased"

        # update status of all members that got infected
        for i in ind:
            self.members[i].status = "infected"

    # function to update the locations of all members of a population
    def update_positions(self):
        # go through all members
        for i in range(self.number_persons):
            # is member i dead?
            if self.members[i].status != "deceased":
                # if not, update his position
                self.members[i].x_pos += self.members[i].x_vel
                self.members[i].y_pos += self.members[i].y_vel

                # change directions when member would hit a wall of the room
                if self.members[i].x_pos > self.room_size:
                    self.members[i].x_pos = 2 * self.room_size - self.members[i].x_pos
                    self.members[i].x_vel = - self.members[i].x_vel
                elif self.members[i].x_pos < 0:
                    self.members[i].x_pos = - self.members[i].x_pos
                    self.members[i].x_vel = - self.members[i].x_vel
                if self.members[i].y_pos > self.room_size:
                    self.members[i].y_pos = 2 * self.room_size - self.members[i].y_pos
                    self.members[i].y_vel = - self.members[i].y_vel
                elif self.members[i].y_pos < 0:
                    self.members[i].y_pos = - self.members[i].y_pos
                    self.members[i].y_vel = - self.members[i].y_vel