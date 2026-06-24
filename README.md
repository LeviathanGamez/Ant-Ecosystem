# Ant-Ecosystem
An agent-based ant colony simulation built in Python using Pygame, designed to model swarm intelligence and emergent pathfinding. Simulates ants forming efficient routes through pheromone-based communication between agents.

![Simulation Demo](<img width="1106" height="720" alt="AntGif-ezgif com-optimize (1)" src="https://github.com/user-attachments/assets/8dc69d5f-626d-4990-9d5f-19b506dccdb7" />)

Ants operate as independent agents that explore the environment using directional sensors to detect pheromone concentrations. Beginning at the central anthill, they initially move in random directions while laying homing pheromones. Upon discovering food, ants follow these home pheromone trails back to the colony while depositing food pheromones, creating an emergent trail network that other agents can follow.

As more ants travel along successful routes, more efficient paths are reinforced by pheromones while less-traveled routes gradually lose influence. Over time, the colony naturally converges toward more efficient paths, demonstrating how simple local interactions can produce complex collective behavior, resembling real-world ant colonies. 

Each ant functions as an independent agent and uses three directional sensors—forward, left, and right—to measure nearby pheromone concentrations and determine its movement. Through these local decisions, ants are able to navigate, explore, and collectively optimize routes without centralized coordination, resulting in emergent swarm intelligence and adaptive path formation.

To improve performance, the simulation uses spatial partitioning, dividing pheromones into a grid-based structure so ants only evaluate nearby pheromones rather than the entire environment. This significantly reduces computation and allows smooth simulations with dozens of active agents.
Full Video: https://youtu.be/M9s3M4ELz9w

Features:
-Pheromone-based pathfinding and trail formation
-Sensor-driven agent navigation
-Emergent swarm intelligence
-Grid-based spatial partitioning optimization
-Object-oriented agent architecture
-Real-time simulation built with Pygame

Controls:

- D -> Draw Debug Lines
- F -> Pheromone mapping
- G -> Render Info Texts
