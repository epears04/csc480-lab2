from mesa import Agent, Model
from mesa.space import MultiGrid
import random


PLACEHOLDER_POS = (0, 0)

class Prey(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.energy = 100

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def eat(self):
        self.energy += 10

    def breed(self):
        if self.energy >= 200:
            self.energy -= 100
            new_prey = Prey(self.model)
            self.model.grid.place_agent(new_prey, PLACEHOLDER_POS)
            self.model.grid.move_to_empty(new_prey)           

    def step(self):
        self.move()
        self.breed()
        self.energy -= 1

class Predator(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.energy = 100

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def eat(self):
        prey_neighbors = self.model.grid.get_cell_list_contents(
            [self.pos]
        )
        prey_agents = [agent for agent in prey_neighbors if isinstance(agent, Prey)]
        if prey_agents:
            prey_to_eat = random.choice(prey_agents)
            self.model.grid.remove_agent(prey_to_eat)
            prey_to_eat.remove()
            self.energy += 100

    def breed(self):
        if self.energy >= 200:
            self.energy -= 100
            new_predator = Predator(self.model)
            self.model.grid.place_agent(new_predator, PLACEHOLDER_POS)
            self.model.grid.move_to_empty(new_predator)

    def step(self):
        self.move()
        self.eat()
        self.breed()
        self.energy -= 1

class PreyPredatorModel(Model):
    def __init__(self, height, width, prey_count, predator_count):
        super().__init__()
        self.height = height
        self.width = width
        self.grid = MultiGrid(height, width, torus=True)
        self.running = True

        for i in range(prey_count):
            prey = Prey(self)
            self.grid.place_agent(prey, PLACEHOLDER_POS)
            self.grid.move_to_empty(prey)

        for i in range(predator_count):
            predator = Predator(self)
            self.grid.place_agent(predator, PLACEHOLDER_POS)
            self.grid.move_to_empty(predator)           

    def step(self):
        self.agents.shuffle_do("step")

model = PreyPredatorModel(height=10, width=10, prey_count=10, predator_count=1)

for i in range(100):
    model.step()
    
    # Print population counts
    prey_count = sum(isinstance(agent, Prey) for agent in model.agents)
    predator_count = sum(isinstance(agent, Predator) for agent in model.agents)
    print(f"Step {i}: Prey={prey_count}, Predators={predator_count}")