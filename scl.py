#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Fuzzy Logic: Temperature to Fan Speed
def low_temp(x):
    if x <= 20:
        return 1
    elif 20 < x < 30:
        return (30 - x) / 10
    else:
        return 0
def medium_temp(x):
    if 20 < x < 30:
        return (x - 20) / 10
    elif 30 <= x <= 40:
        return (40 - x) / 10
    else:
        return 0
def high_temp(x):
    if x <= 30:
        return 0
    elif 30 < x < 40:
        return (x - 30) / 10
    else:
        return 1
def fuzzy_logic(temp):
  #Fuzzification
    low = low_temp(temp)
    medium = medium_temp(temp)
    high = high_temp(temp)
    print(f"Low membership:    {low}")
    print(f"Medium membership: {medium}")
    print(f"High membership:   {high}")
    numerator = (low * 20) + (medium * 50) + (high * 80)
    denominator = low + medium + high
    if denominator == 0:
        return 0
    # Defuzzification
    speed = numerator / denominator
    return speed
# Input
temp = float(input("Enter temperature: "))
speed = fuzzy_logic(temp)
print(f"\nFinal Fan Speed: {speed:.2f}")


# In[13]:


## Defuzzification using Centroid Method
def alpha_cut(fs, lam):
    result = []
    for k in fs:
        if fs[k] >= lam:
            result.append(k)
    return result
# Mean of Maximum (MOM)
def mom(fs):
    max_val = None
    for k in fs:
        if max_val is None or fs[k] > max_val:
            max_val = fs[k]
    total = 0
    count = 0
    for k in fs:
        if fs[k] == max_val:
            total += k
            count += 1
    return total / count
def cog(fs):
    numerator = 0
    denominator = 0
    for i in fs:
        numerator += i*fs[i]
        denominator += fs[i]
    if denominator == 0:
        return 0
    return numerator / denominator
# Example fuzzy output values
fs1 = {"Low": 0.2, "Medium": 0.7, "High": 0.5}
print("Alpha-cut:", alpha_cut(fs1, 0.5))
fs2 = {1:0.2, 2:0.5, 3:0.8, 4:0.5}
print("MOM:", mom(fs2))
print("COG:", cog(fs2))


# In[21]:


#aco
import numpy as np
dist = np.array([[0, 2, 2, 1], [2, 0, 1, 2], [2, 1, 0, 2], [1, 2, 2, 0]])
n = len(dist)
num_ants = n
iterations = 20
alpha = 1        # pheromone importance
beta = 2         # distance importance
evaporation = 0.5
pheromone = np.ones((n, n))
def choose_next(current, unvisited):
   probs = []
   for j in unvisited:
        tau = pheromone[current][j] ** alpha
        eta = (1 / (dist[current][j] + 1e-10)) ** beta
        probs.append(tau * eta)
   probs = np.array(probs)
   probs = probs / probs.sum()
   return np.random.choice(unvisited, p=probs)
   
best_path = None
best_cost = float('inf')
for _ in range(iterations):
    all_paths = []
    for ant in range(num_ants):
        visited = [False] * n
        path = [0]
        visited[0] = True
        current = 0
        cost = 0
        # build path
        for _ in range(n - 1):
            unvisited = [j for j in range(n) if not visited[j]]
            next_city = choose_next(current, unvisited)
            cost += dist[current][next_city]
            path.append(next_city)
            visited[next_city] = True
            current = next_city
        # return to start
        cost += dist[current][0]
        path.append(0)
        all_paths.append((path, cost))
        # update global best
        if cost < best_cost:
            best_cost = cost
            best_path = path
    # -------------------------
     # evaporation
    pheromone *= (1 - evaporation)
    # add new pheromone
    for path, cost in all_paths:
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            pheromone[a][b] += 1 / cost
# --------------------------
# OUTPUT
# --------------------------
print("\nBest Path:", best_path)
print("Best Cost:", best_cost)


# In[3]:


#pso
import random
# Objective function (minimize)
def fitness(x):
    return x**2
# Parameters
num_particles = 5
iterations = 10
w = 0.5       # inertia
c1 = 1        # cognitive
c2 = 2        # social
# Initialize particles
particles = [random.uniform(-10, 10) for _ in range(num_particles)]
velocities = [random.uniform(-1, 1) for _ in range(num_particles)]
pBest = particles[:]
gBest = min(particles, key=fitness)
for i in range(iterations):
    for j in range(num_particles):
        r1 = random.random()
        r2 = random.random()
        # Update velocity
        velocities[j] = (w * velocities[j] +
                         c1 * r1 * (pBest[j] - particles[j]) +
                         c2 * r2 * (gBest - particles[j]))
        # Update position
        particles[j] += velocities[j]
        # Update Pbest
        if fitness(particles[j]) < fitness(pBest[j]):
            pBest[j] = particles[j]
    # Update Gbest
    gBest = min(pBest, key=fitness)
    print(f"Iteration {i+1}: gBest = {round(gBest, 4)}, f(x) = {round(fitness(gBest), 6)}")
print("\nBest Position (Solution):", round(gBest, 4))   
print("Minimum Value:", round(fitness(gBest), 4))


# In[4]:


##genetic algorithm
import random
# Fitness function (maximize)
def fitness(x):
    return x**3
# Parameters
population_size = 6
generations = 20
mutation_rate = 0.1
# Initialize population (random integers)
population = [random.randint(0, 10) for _ in range(population_size)]
for gen in range(generations):
    # Fitness Evaluation
    population = sorted(population, key=fitness, reverse=True)
    print(f"Generation {gen+1}: {population}")
    # Selection (top 2)
    parent1, parent2 = population[0], population[1]
    # Crossover (simple average)
    child = (parent1 + parent2) // 2
    # Mutation
    if random.random() < mutation_rate:
        child += random.randint(-2, 2)
    # Replace worst individual
    population[-1] = child
# Final result
best = max(population, key=fitness)
print("\n" + "=" * 35)
print("Best Solution:", best)
print("Maximum Value:", fitness(best))
print("=" * 35)


# In[18]:


import random #6. Grey wolf
def fitness(x):
    return x ** 2
# Parameters
WOLVES, ITERS = 5, 20
wolves = [random.uniform(-10, 10) for _ in range(WOLVES)]
for t in range(ITERS):
    wolves.sort(key=fitness)
    alpha, beta, delta = wolves[0], wolves[1], wolves[2]
    a = 2 - 2 * (t / ITERS)  # decreases from 2 to 0
    new_wolves = []
    for w in wolves:
        X_new = 0
        for leader in [alpha, beta, delta]:
            r1, r2 = random.random(), random.random()
            A = 2 * a * r1 - a
            C = 2 * r2
            D = abs(C * leader - w)
            X_new += leader - A * D
        new_wolves.append(X_new / 3)
    wolves = new_wolves
    print(f"Iter {t+1:2d} | Alpha: {round(alpha,4):8.4f} | Best f(x): {round(fitness(alpha),6):.6f}")

print("=" * 45)
print(f"Best Position : {round(alpha, 4)}")
print(f"Minimum Value : {round(fitness(alpha), 6)}")


# In[17]:


#inteligent water droplet
import numpy as np
n = 5  # number of nodes
soil = np.ones((n, n))  # initial soil
def select_next(current, visited):
    probs = []
    for j in range(n):
        if j not in visited:
            probs.append(1 / soil[current][j])
        else:
            probs.append(0)
    probs = np.array(probs)
    probs = probs / probs.sum()
    return np.random.choice(range(n), p=probs)
best_path = []
best_cost = float('inf')
for _ in range(10):  # iterations
    for i in range(n):
        visited = [i]
        current = i
    while len(visited) < n:
                nxt = select_next(current, visited)
                soil[current][nxt] += 0.1  # update soil
                visited.append(nxt)
                current = nxt
    cost = len(visited)
    if cost < best_cost:
        best_cost = cost
        best_path = visited
print("Best Path:", best_path)
print("Best Path:", best_cost)


# In[16]:


#firefly
import numpy as np
def fitness(x):
    return x**2  # minimize
n = 5
fireflies = np.random.rand(n)
for _ in range(20):
    for i in range(n):
        for j in range(n):
            if fitness(fireflies[j]) < fitness(fireflies[i]):
                r = abs(fireflies[i] - fireflies[j])
                beta = 1 / (1 + r**2)
                fireflies[i] += beta * (fireflies[j] - fireflies[i]) + np.random.rand()*0.1
    best = min(fireflies, key=fitness)
    print(f"Iter {t+1}: {best:.4f}")
best = fireflies[np.argmin([fitness(x) for x in fireflies])]
print("Best:", best)


# In[15]:


import random
def fitness(x): return x**2
# Parameters
S = 5          # Food sources
limit = 10     # Max failures before abandonment
iterations = 20
food_sources = [random.uniform(-10, 10) for _ in range(S)]
trials = [0] * S  # Counter for Scout phase

for t in range(iterations):
    # 1. EMPLOYED BEE PHASE
    for i in range(S):
        k = random.choice([n for n in range(S) if n != i])
        new_sol = food_sources[i] + random.uniform(-1, 1) * (food_sources[i] - food_sources[k])
        if fitness(new_sol) < fitness(food_sources[i]):
            food_sources[i], trials[i] = new_sol, 0
        else:
            trials[i] += 1

    # 2. ONLOOKER BEE PHASE (Based on Probability)
    # Calculate fitness (Inverse of fitness for minimization)
    fitness_vals = [1/(1+fitness(x)) if fitness(x)>=0 else 1+abs(fitness(x)) for x in food_sources]
    prob = [f/sum(fitness_vals) for f in fitness_vals]
    
    for _ in range(S):
        i = random.choices(range(S), weights=prob)[0] # Better sources chosen more
        k = random.choice([n for n in range(S) if n != i])
        new_sol = food_sources[i] + random.uniform(-1, 1) * (food_sources[i] - food_sources[k])
        if fitness(new_sol) < fitness(food_sources[i]):
            food_sources[i], trials[i] = new_sol, 0
        else:
            trials[i] += 1

    # 3. SCOUT BEE PHASE
    for i in range(S):
        if trials[i] > limit:
            food_sources[i] = random.uniform(-10, 10)
            trials[i] = 0

    best = min(food_sources, key=fitness)
    print(f"Iter {t+1}: {best:.4f}")
print("the best is ",best)


# In[14]:


import random
# 9. ARTIFICIAL BEE COLONY

def fitness(x):
    return x**2  # Objective function: minimize x^2

# Initialize random solutions (food sources)
solutions = [random.uniform(-10, 10) for _ in range(5)]

for t in range(20):  # Number of iterations (cycles)
    for i in range(len(solutions)):
        # Select a random neighbor solution
        k = random.randint(0, len(solutions) - 1)

        # Generate a new candidate solution
        phi = random.uniform(-1, 1)
        new_solution = solutions[i] + phi * (solutions[i] - solutions[k])

        # Greedy selection: keep the better solution
        if fitness(new_solution) < fitness(solutions[i]):
            solutions[i] = new_solution

    # Find best solution in current population
    best = min(solutions, key=fitness)

    print(f"[ABC] Iter {t+1:2d} | Best position: {best:.4f} | Minimum value: {fitness(best):.4f}")

# Final result
print(f"\nABC Result: Best position = {best:.4f}, Minimum value = {fitness(best):.4f}")


# In[ ]:




