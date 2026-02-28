from typing import Dict, List
import numpy as np
import random

from src.solutions import Solution

def create_objects(number_of_objects):
    objects = dict()
    for key in range(number_of_objects):
        weight = np.random.randint(1, 6)
        value = np.random.randint(10, 21)
        objects[key] = [weight, value]
    return objects

def sort_objects(object, choice):
    sorted_objects = []
    for i in range(len(object)):
        if choice ==  "Weight":
            max_key = max(object, key=lambda k: object[k][0])
            print(f"MAXKEY: {max_key}")
            sorted_objects.append(max_key)
            object.pop(max_key)
        else:
            max_key = max(object, key=lambda k: object[k][1])
            sorted_objects.append(max_key)
            object.pop(max_key)
    return sorted_objects

def add_to_bag(sorted_objects, objects, max_weight=35):
    bag = []
    bag_value = 0
    current_weight = 0
    for i in range(len(sorted_objects)):
        if current_weight >= max_weight:
            return bag, bag_value, current_weight
        current_object = sorted_objects[i]
        object_weight, object_value = objects[current_object]
        total_weight = current_weight + object_weight
        if total_weight > max_weight:
            continue
        bag.append(current_object)
        bag_value += object_value
        current_weight += object_weight
    return bag, bag_value, current_weight

def get_objects_not_in_bag(bag, objects):
    not_in_bag = []
    for object in objects:
        if object in objects:
            continue
        else:
            not_in_bag.append(object)
    return not_in_bag

def get_solution_stats(solution, objects):
    weight = 0
    value = 0
    for i in range(len(solution)):
        current_object = solution[i]
        current_weight, current_value = objects[current_object]
        weight += current_weight
        value += current_value
    return weight, value

def random_optimize(solution, objects, max_weight=35, max_tries=100):
    tries = 0
    leftover_bag = get_objects_not_in_bag(solution, objects)
    while tries < max_tries:
        choice = np.random.randint(0, 2) % 2
        if choice == 0:
            random_object_bag = random.choice(solution)
            random_object_bag_idx = solution.index(random_object_bag)
            random_object_leftover = random.choice(leftover_bag)
            tmp_solution = solution.copy()
            tmp_solution[random_object_bag_idx] = random_object_leftover
            _, solution_value = get_solution_stats(solution, objects)
            tmp_solution_weight, tmp_solution_value = get_solution_stats(tmp_solution, objects)
            diff = tmp_solution_value - solution_value
            if tmp_solution_weight > max_weight and diff > 0:
                solution = tmp_solution
            else:
                tries += 1

        else: 



if __name__ == "__main__":
    print("Creating dataset...")
    objects = create_objects(100)
    sorted_objects_weight = sort_objects(objects.copy(), "Weight")
    sorted_objects_value = sort_objects(objects.copy(), "Value")
    print(f"All objects: {objects}")
    print(f"Sorted after weight: {sorted_objects_weight}")
    print(f"Sorted after value: {sorted_objects_value}")
    b1, b1_value, b1_weight = add_to_bag(sorted_objects_weight.copy(), objects.copy(), 35)
    b2, b2_value, b2_weight = add_to_bag(sorted_objects_value.copy(), objects.copy(), 35)
    print(b1)
    print(b2)




    



