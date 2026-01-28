from typing import List, Tuple
import numpy as np
import random

def return_distance(path: List, edges: dict):
    total_distance = 0
    for i in range(len(path) - 1):
        current_city = path[i]
        next_city = path[i+1]
        distance = edges[current_city, next_city]
        total_distance += distance
    total_distance += edges[path[-1], path[0]]
    return total_distance

def return_neighborhood_distance(path: List, edges: dict):
    total_distance = 0
    for i in range(len(path) - 1):
        current_city = path[i]
        next_city = path[i+1]
        distance = edges[current_city, next_city]
        total_distance += distance
    return total_distance

def convolutional_optimization(path: List, edges: dict, num_neighborhoods: int, overlap: int):
    '''
    The idea is to divide the full path into num_neighborhoods and swap cities inside each
    neighborhood. This way we do a local search without having to have a crazy global space to 
    swap. In theory, this should converge towards somewhat a optimal soluton, however, there
    is a core problem. If the last city in neighboorhood 1 and first city in neighboorhood 2 gets
    a worse distance, it can potentially worsen the overall distance. To try to fix this,
    we introduce a overlap. In other words, this would act as a convolutional solution. 
    '''
    interval = int(len(path) / num_neighborhoods)
    for i in range(num_neighborhoods):
        tries = 0
        if i == 0:  
            current_neighborhood = path[interval * i:interval * (i + 1) + overlap]
        else:
            current_neighborhood = path[interval * i-overlap:interval * (i + 1) + overlap]
        #print(f"Current neighborhood: {current_neighborhood}")
        while tries < 100:
            #print(f"This is try {tries} for neighborhood {i}")
            city1 = random.choice(current_neighborhood)
            city2 = random.choice(current_neighborhood)
            if city1 == city2:
                tries += 1
                continue
            city1_idx = current_neighborhood.index(city1)
            city2_idx = current_neighborhood.index(city2)
            # need to check for idx - 1 and idx + 1
            temp_neighborhood = current_neighborhood.copy()
            temp_neighborhood[city1_idx] = city2
            temp_neighborhood[city2_idx] = city1
            new_distance = return_neighborhood_distance(temp_neighborhood, edges)
            current_distance = return_neighborhood_distance(current_neighborhood, edges)
            if new_distance < current_distance:
                global_city1_idx = path.index(city1)
                global_city2_idx = path.index(city2)
                path[global_city1_idx] = city2
                path[global_city2_idx] = city1
                #print(f"Swapped {city1} and {city2}")
                tries = 0
                if i == 0:  
                    current_neighborhood = path[interval * i:interval * (i + 1) + overlap]
                else:
                    current_neighborhood = path[interval * i-overlap:interval * (i + 1) + overlap]
            else:
                tries += 1

    return path

def greedy_algorithm(cities: List, edges: dict) -> Tuple:
    total_distance = 0
    path = []
    current_city = random.choice(cities)
    cities.remove(current_city)
    path.append(current_city)
    i = 0
    while cities:
        best_destination = None
        best_distance = 10 # just put 10 since the max distance is
        for possible_city in cities:
            #print(f"This is the current city: {current_city}")
            #print(f"This is the possible city: {possible_city}")
            #print(f"These are the possible cities: {cities}")
            current_distance = edges[current_city, possible_city]
            #print(f"Current distance: {current_distance}")
            if current_distance < best_distance:
                best_distance = current_distance
                best_destination = possible_city
        i += 1
        #print(f"The best destination is: {best_destination}")
        path.append(best_destination)
        #print(f"Current path: {path}")
        current_city = best_destination
        total_distance += best_distance
        cities.remove(current_city)

    first_city = path[0]
    last_city = path[len(path)-1]
    edge = edges[first_city, last_city]
    total_distance += edge
    return total_distance, path

def random_algorithm(cities: List, edges: dict) -> Tuple:
    total_distance = 0
    path = []
    i = 0
    while cities:
        chosen_city = random.choice(cities)
        #print(f"We have chose this city: {chosen_city}")
        path.append(chosen_city)
        #print(f"Current path: {path}")
        cities.remove(chosen_city)
        if len(path) > 1:
            i += 1
            previous_city = path[i-1]
            #print(f"Previous city: {previous_city}")
            distance = edges[chosen_city, previous_city]
            #print(f"Distance between {previous_city} and {chosen_city}: {distance}")
            total_distance += distance

    first_city = path[0]
    last_city = path[len(path) - 1]
    distance = edges[first_city, last_city]
    total_distance += distance
    return total_distance, path

def _create_cities(number_of_cities: int) -> list:
    cities = []
    for i in range(number_of_cities):
        cities.append(i)
    return cities

def _create_edges(cities: list) -> dict:
    edges = {}
    for i in cities:
        for j in cities:
            if i != j and (i, j) not in edges and (j, i) not in edges:
                edges[(i, j)] = np.random.randint(3, 9)
            elif i != j and (j, i) in edges:
                edges[(i, j)] = edges[(j, i)]
        
    return edges

def init_cities(num_cities):
    num_cities
    cities = _create_cities(num_cities)
    edges = _create_edges(cities)
    return cities, edges

if __name__ == "__main__":
    num_cities = 100
    cities, edges = init_cities(num_cities)
    #print("Cities:", cities)
    #print("Edges:", edges)
    rand_distance, rand_path = random_algorithm(cities.copy(), edges)
    print(f"Total distance of Random: {rand_distance}")
    #print(f"Taken path for Random {rand_path}")

    greedy_distance, greedy_path = greedy_algorithm(cities.copy(), edges)
    print(f"Total distance of Greedy: {greedy_distance}")
    #print(f"Taken path for Greedy {greedy_path}")

    optimized_path = convolutional_optimization(rand_path.copy(), edges, 5, 10)
    optimized_distance = return_distance(optimized_path, edges)
    print(f"Optimized Random distance: {optimized_distance}")

    optimized_path = convolutional_optimization(greedy_path.copy(), edges, 5, 10)
    optimized_distance = return_distance(optimized_path, edges)
    print(f"Optimized Greedy distance: {optimized_distance}")


