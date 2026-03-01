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

def sort_objects(objects, choice):
    if choice == "Weight":
        return sorted(objects, key=lambda k: objects[k][0], reverse=True)
    else:
        return sorted(objects, key=lambda k: objects[k][1], reverse=True)

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
    return [obj for obj in objects if obj not in bag]

def get_solution_stats(solution, objects):
    weight = 0
    value = 0
    for obj in solution:
        current_weight, current_value = objects[obj]
        weight += current_weight
        value += current_value
    return weight, value

def random_optimize(solution, objects, max_weight=35, max_tries=100):
    solution = solution.copy()
    leftover_bag = get_objects_not_in_bag(solution, objects)

    tries = 0

    while tries < max_tries and solution:
        choice = random.randint(0, 1)
        if choice == 0 and leftover_bag:
            rnd_in = random.choice(solution)
            rnd_out = random.choice(leftover_bag)

            tmp_solution = solution.copy()
            idx = tmp_solution.index(rnd_in)
            tmp_solution[idx] = rnd_out
            _, old_value = get_solution_stats(solution, objects)
            new_weight, new_value = get_solution_stats(tmp_solution, objects)

            diff = new_value - old_value

            if new_weight <= max_weight and diff > 0:
                solution = tmp_solution
                leftover_bag.remove(rnd_out)
                leftover_bag.append(rnd_in)
            else:
                tries += 1

        elif leftover_bag:
            rnd_out = random.choice(leftover_bag)
            w, _ = objects[rnd_out]

            curr_weight, _ = get_solution_stats(solution, objects)

            if curr_weight + w <= max_weight:
                solution.append(rnd_out)
                leftover_bag.remove(rnd_out)
            else:
                tries += 1
        else:
            break

    return solution

def greedy_optimize(solution, objects, max_weight=35, max_tries=100):
    solution = solution.copy()
    leftover_bag = get_objects_not_in_bag(solution, objects)

    tries = 0

    while tries < max_tries and solution:
        choice = random.randint(0, 1)

        if choice == 0 and leftover_bag:
            rand_in = random.choice(solution)
            old_weight, old_value = objects[rand_in]

            best_swap = None
            best_gain = 0

            curr_weight, curr_value = get_solution_stats(solution, objects)

            for obj in leftover_bag:
                new_weight, new_value = objects[obj]

                tmp_weight = curr_weight - old_weight + new_weight
                gain = new_value - old_value

                if tmp_weight <= max_weight and gain > best_gain:
                    best_gain = gain
                    best_swap = obj

            if best_swap is not None:
                idx = solution.index(rand_in)
                solution[idx] = best_swap

                leftover_bag.remove(best_swap)
                leftover_bag.append(rand_in)
            else:
                tries += 1

        elif leftover_bag:
            curr_weight, _ = get_solution_stats(solution, objects)

            best_item = None
            best_value = 0

            for obj in leftover_bag:
                w, v = objects[obj]

                if curr_weight + w <= max_weight and v > best_value:
                    best_item = obj
                    best_value = v

            if best_item is not None:
                solution.append(best_item)
                leftover_bag.remove(best_item)
            else:
                tries += 1
        else:
            break

    return solution


if __name__ == "__main__":
    print("Creating dataset...")
    objects = create_objects(100)
    sorted_objects_weight = sort_objects(objects.copy(), "Weight")
    sorted_objects_value = sort_objects(objects.copy(), "Value")
    b1, b1_value, b1_weight = add_to_bag(sorted_objects_weight.copy(), objects.copy(), 35)
    b2, b2_value, b2_weight = add_to_bag(sorted_objects_value.copy(), objects.copy(), 35)
    
    print("Optimizing solution")

    optimized_random_b1 = random_optimize(b1, objects)
    optimized_random_b2 = random_optimize(b2, objects)

    b1_weight,b1_value = get_solution_stats(b1, objects)
    b2_weight,b2_value,  = get_solution_stats(b2, objects)
    opt_random_b1_weight,opt_b1_value = get_solution_stats(optimized_random_b1, objects)
    opt_random_b2_weight,opt_b2_value = get_solution_stats(optimized_random_b2, objects)


    
    optimized_greedy_b1 = greedy_optimize(b1, objects)
    optimized_greedy_b2 = greedy_optimize(b2, objects)

    opt_greedy_b1_weight,opt_greedy_b1_value = get_solution_stats(optimized_greedy_b1, objects)
    opt_greedy_b2_weight,opt_greedy_b2_value = get_solution_stats(optimized_greedy_b2, objects)

    print("\nBEFORE OPTIMIZATION")
    print(f"b1 value: {b1_value}, weight: {b1_weight}")
    print(f"b2 value: {b2_value}, weight: {b2_weight}")

    print("\nAFTER OPTIMIZATION")
    print(f"optimized random b1 value: {opt_b1_value}, weight: {opt_random_b1_weight}")
    print(f"optimized random b2 value: {opt_b2_value}, weight: {opt_random_b2_weight}")


    print("\nAFTER GREEDY OPTIMIZATION")
    print(f"optimized greedy b1 value: {opt_greedy_b1_value}, weight: {opt_greedy_b1_weight}")
    print(f"optimized greedy b2 value: {opt_greedy_b2_value}, weight: {opt_greedy_b2_weight}")


