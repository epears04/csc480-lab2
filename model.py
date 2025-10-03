from mesa import Agent, Model
from mesa.space import MultiGrid
# from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
# from mesa.visualization.components import AgentPortrayalStyle
import random

# Steps for visualization:
# 1. Define an agent_portrayal function to specify how agents should be displayed
# 2. Set up model_params to define adjustable parameters
# 3. Create a SolaraViz instance with your model, parameters, and desired measures
# 4. Display the visualization in a Jupyter notebook or run as a Solara app


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

    def run(self):           
        if self.energy >= 75:
            self.energy -= 15
            self.move()

    def step(self):
        self.move()
        self.breed()
        rand_num = random.randint(1,10)
        if rand_num <= 5:
            self.eat()
        else:
            self.run()
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
        else:
            self.energy -= 20

    def breed(self):
        if self.energy >= 200:
            self.energy -= 100
            new_predator = Predator(self.model)
            self.model.grid.place_agent(new_predator, PLACEHOLDER_POS)
            self.model.grid.move_to_empty(new_predator)

    def fight(self):
        if self.energy >= 100:
            self.energy -= 50
            neighbors = self.model.grid.get_cell_list_contents([self.pos])
            predator_agents = [agent for agent in neighbors if isinstance(agent, Predator)]

            if len(predator_agents) > 2:
                predator_to_fight = random.choice(predator_agents)
                self.model.grid.remove_agent(predator_to_fight)
                predator_to_fight.remove()

    def step(self):
        self.move()
        self.eat()
        self.breed()
        rand_int = random.randint(1,10)
        if rand_int > 7:
            self.fight()
        self.energy -= 1

class Flower(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.energy = 100

    def grow(self):
        self.energy += 10
        if self.energy >= 200:
            self.energy -= 100
            new_flower = Flower(self.model)
            self.model.grid.place_agent(new_flower, PLACEHOLDER_POS)
            self.model.grid.move_to_empty(new_flower)

    def wilt(self):
        self.energy -= 5
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.remove()

    def step(self):
        rand_int = random.randint(1,2)
        if rand_int == 1:
            self.grow()
        else:
            self.wilt()

# the environment 
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

model = PreyPredatorModel(height=10, width=10, prey_count=40, predator_count=1)

for i in range(100):
    model.step()
    
    # Print population counts
    prey_count = sum(isinstance(agent, Prey) for agent in model.agents)
    predator_count = sum(isinstance(agent, Predator) for agent in model.agents)
    print(f"Step {i}: Prey={prey_count}, Predators={predator_count}")