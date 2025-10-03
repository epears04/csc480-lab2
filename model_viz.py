from mesa.visualization import SolaraViz, make_space_component
from model import *

# how agents are portrayed
def agent_portrayal(agent):
    if agent is None:
        return {} 
    
    if isinstance(agent, Prey):
        return {
            "marker" : "o",
            "color" : "blue",
            "size" : 50,
        }
    elif isinstance(agent, Predator):
        return {
            "marker" : "o",
            "color" : "red",
            "size" : 50,
        }
    elif isinstance(agent, Flower):
        return {
            "marker" : "o",
            "color" : "green",  
            "size" : 50,
        }
    return {} # default

# grid formatting
def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Prey-Predator Simulation")

model_params = {
    "height" : 20,
    "width" : 20,
    "prey_count" : 50,
    "predator_count" : 10,
    "flower_count" : 20,
}

model = PreyPredatorModel(height=20, width=20, prey_count=50, predator_count=5, flower_count = 20)

# create space visualization component
SpaceGraph = make_space_component(
    agent_portrayal,
    post_process=post_process,
    draw_grid=True
)

page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="Prey-Predator Simulation",
)