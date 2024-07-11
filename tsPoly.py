import random
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tsSettings
from TabuClasses import TSolutionInfo, Offer

# Como achar o dia? Slot 10 -> 10 / 7 (Dia da semana) -> 10 MOD 7 (Slot daquele dia)


connector = tsSettings.DatabaseConnector()
utils = tsSettings.Utils()
connector.connect()

#parameters_data = utils.get_parameters(connector)
offers_data = utils.get_offers(connector)
availability_data = utils.get_teacher_availability(connector)

teacher_availability = {id_: {day: [False]*7 for day in range(5)} for id_ in range(101, 180)}
teacher_availability.update({id_: {day: [False]*7 for day in range(5)} for id_ in range(301, 373)})

for entry in availability_data:
    teacher_id, day_of_week, slot = entry
    teacher_availability[teacher_id][day_of_week][slot] = True

def print_teacher_availability(teacher_availability):
    for teacher, days in teacher_availability.items():
        print(f"Availability for {teacher}:")
        for day, slots in days.items():
            slot_status = ", ".join([f"Slot {i+1}: {'Available' if slot else 'Not Available'}" for i, slot in enumerate(slots)])
            print(f"  Day {day}: {slot_status}")
        print("\n")

random.shuffle(offers_data)


def visualize_local_search(solution_array):
    solution_costs = [solution.cost for solution in solution_array]
    plt.plot(range(1, len(solution_costs) + 1), solution_costs, marker='o', label='Solution Cost')
    plt.xlabel('Iteration')
    plt.ylabel('Solution Cost')
    plt.title('Local Search Graph')
    plt.legend()
    plt.grid(True)
    plt.show()


turmas = int(input("Number of Turmas?\n"))
number_iterations = int(input("Number of Iterations?\n"))

solution1 = TSolutionInfo(turmas, teacher_availability)
solution1.Id = 0

def get_user_weights(solution, connector):
    user_choice = input(f"Enter Y for Default Parameters or N for Default without Tabu or C for Custom").upper()
    if user_choice == 'Y':
        weights = utils.get_parameter_weights(1, connector)
        tabu_choice, = utils.get_parameter_tabu(1, connector)
        if weights:
            solution.incident_weights = list(weights[0])
            print("Default weights: ", solution.incident_weights)
            solution.useTabu = tabu_choice[0]
        else:
            print("Error assigning default weights/tabu")
    if user_choice == 'N':
        weights = utils.get_parameter_weights(1, connector)
        if weights:
            solution.incident_weights = list(weights[0])
            print("Default weights: ", solution.incident_weights)
            solution.useTabu = False
        else:
            print("Error assigning default weights/tabu")
    if user_choice == 'C':
        for i in range(len(solution.incident_weights)):
            userInput = input(f"Enter the value for the Weight {i}: ")
            solution.incident_weights[i] = int(userInput)
        print(solution.incident_weights)
        use_tabu_input = input("Do you want to use Tabu Search? (Y/N): ").upper()
        if use_tabu_input == 'Y':
            solution.useTabu = True
        elif use_tabu_input == 'N':
            solution.useTabu = False
        else:
            print("Invalid input. Defaulting to not using Tabu Search.")
            solution.useTabu = False

def calculate_number_of_switch_moves(class_slots):
    n = len(class_slots)  # Rows
    m = len(class_slots[0])  # Columns
    total_slots = n * m

    print("Rows: ", n)
    print("Columns: ", m)
    print("Total Slots: ", total_slots)
    
    number_of_switch_moves = (total_slots * (total_slots - 1)) // 2
    return number_of_switch_moves

max_offers = turmas * 35

for idx, offer_row in enumerate(offers_data):
    if idx >= max_offers:
        break
    offer = Offer()
    offer.Id = offer_row[0]
    offer.Disciplina = offer_row[3]
    offer.Professor = offer_row[4]
    offer.IdProfessor = offer_row[1]
    offer.assignOfferToClass(solution1)

get_user_weights(solution1, connector)

bestSolution = solution1

solution_array = []
bestSolutionCost = 0
noImprovement = 0
start_time = time.time()


for i in range(1, number_iterations):
    solution = bestSolution.generateRandomSolutions()
    solution.Id = i
    bestSolution = TSolutionInfo.checkAssignBestSolution(bestSolution, solution)
    bestSolutionCost = bestSolution.cost
    if bestSolutionCost < solution.cost:
        noImprovement += 1
    solution_array.append(solution)
    if noImprovement > 1000:
        break


print("Best Solution = ", bestSolution.Id)
print("Best Cost: ", bestSolution.cost)
print("--- %s seconds ---" % (time.time() - start_time))


def main():

    print("Welcome to the Schedule Manager!")

    while True:
        print("\nMenu:")
        print("1. View Schedule of a Solution")
        print("2. Manually Swap Slots")
        print("3. Check Professor Collision")
        print("4. View Graph")
        print("5. Number of Tabu Solutions")
        print("6. Calculate Number of Possible Switch Moves")
        print("7. Print Teacher Availability")
        print("8. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")

        if choice == "1":
            print("Select a solution to view the schedule:")
            for i, solution in enumerate(solution_array):
                print(f"{i + 1}. Solution {solution.Id} - Cost: {solution.cost} - Tabu: {solution.tabu_flag}")
            try:
                selected_solution_index = int(input("Enter the solution number: ")) - 1
                selected_solution = solution_array[selected_solution_index]
                selected_solution.printSchedule()
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        elif choice == "2":
            print("Select a solution to swap slots:")
            for i, solution in enumerate(solution_array):
                print(f"{i + 1}. Solution {solution.Id}")
            try:
                selected_solution_index = int(input("Enter the solution number: ")) - 1
                selected_solution = solution_array[selected_solution_index]
                selected_solution.printSchedule()
                print("Select the first slot you wanna change (Turma, Day and Slot)")
                turma1 = int(input("Turma: ")) -1
                day1 = int(input("Day: ")) -1
                slot1 = int(input("Slot: ")) -1
                print("Select the second slot you wanna change (Turma, Day and Slot)")
                turma2 = int(input("Turma: ")) -1
                day2 = int(input("Day: ")) -1
                slot2 = int(input("Slot: ")) -1
                selected_solution.swapSlotsManually(turma1,day1,slot1,turma2,day2,slot2)
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        elif choice == "3":
            # Check professor schedule
            selected_solution_index = int(input("Enter the solution number: ")) - 1
            selected_solution = solution_array[selected_solution_index]
            selected_solution.checkProfessorSchedule()
        
        elif choice == "4":
            visualize_local_search(solution_array)

        elif choice == "5":
                    print(f"Number of solutions with tabu_flag set to True: {bestSolution.tabu_flag}, Use Tabu:  {bestSolution.useTabu}")

        elif choice == "6":
            print("Calculating the number of possible switch moves:")
            if solution_array:
                num_moves = calculate_number_of_switch_moves(solution_array[0].class_slots)
                print(f"Number of possible switch moves: {num_moves}")
            else:
                print("No solutions available to calculate switch moves.")

        elif choice == "7":
            print_teacher_availability(teacher_availability)

        elif choice == "8":
            print("Exiting the Schedule Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




#print(solution1.days_of_week[1][0][0].Professor)

#solution1.days_of_week[Turma(0-2)][Day(0-4)][Slot(0-6)]