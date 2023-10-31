import simpy
import random
import matplotlib.pyplot as plt

# Simulation parameters
SIMULATION_HOURS_PER_DAY = 8
WORKERS = 17
DAILY_WORK_HOURS = 8
DAILY_PRODUCTION_TARGET = 4000
WORKER_PROCESS_TIME_MEAN = 2  # Mean time for a worker to assemble one component (minutes)

# Data collection
production_counts = []
worker_production = [0] * WORKERS  # Initialize a list to track each worker's production

# Define the simulation environment
env = simpy.Environment()

# Define a worker process
def worker_process(env, worker_id):
    while True:
        yield env.timeout(random.expovariate(1.0 / WORKER_PROCESS_TIME_MEAN))
        production_counts.append(1)
        worker_production[worker_id] += 1  # Increment the worker's production count
        print(f"Worker {worker_id} assembled a component at {env.now} minutes")

# Define a factory process
def factory_process(env):
    workers = [env.process(worker_process(env, i)) for i in range(WORKERS)]
    while True:
        yield env.timeout(DAILY_WORK_HOURS * 60)  # Convert daily work hours to minutes
        daily_production = len(production_counts)
        production_counts.clear()
        print(f"Daily production: {daily_production} components")

# Create and start the factory process
env.process(factory_process(env))

# Run the simulation
env.run(until=SIMULATION_HOURS_PER_DAY * 60)  # Convert hours to minutes

# Calculate and print statistics
total_production = len(production_counts)
effectiveness = total_production/DAILY_PRODUCTION_TARGET * 100
print("Factory Simulation Results:")
if effectiveness <100:
    print(f"Effectiveness: {total_production/DAILY_PRODUCTION_TARGET * 100:.2f}% :(")
else:
    print(f"Effectiveness: {total_production/DAILY_PRODUCTION_TARGET * 100:.2f}% :)")
print(f"Total Production: {total_production} components")

# Plot worker production
# Plot worker production
plt.figure(figsize=(10, 5))
plt.bar(range(1, WORKERS + 1), worker_production)  # Adjust the range to start from 1
plt.title("Worker Production")
plt.xlabel("Worker ID")
plt.ylabel("Production Count")
plt.xticks(range(1, WORKERS + 1))  # Adjust the x-axis ticks to start from 1
plt.grid(True)
plt.show()

