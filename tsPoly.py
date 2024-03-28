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


'''
def visualize_local_search(solution_array, tabu_list_points):
    solution_costs = [solution.cost for solution in solution_array]

    plt.plot(range(1, len(solution_costs) + 1), solution_costs, marker='o', label='Solution Cost')
    
    if tabu_list_points:
        plt.scatter(tabu_list_points, [solution.cost for solution in solution_array if solution.in_tabu_list],
                    color='red', label='In Tabu List')

    plt.xlabel('Iteration')
    plt.ylabel('Solution Cost')
    plt.title('Local Search Graph')
    plt.legend()
    plt.grid(True)
    plt.show()
''' 

turmas = int(input("Number of Turmas?\n"))
number_iterations = int(input("Number of Iterations?\n"))

solution1 = TSolutionInfo(turmas)
solution1.Id = 0

def get_user_weights(solution, connector):
    user_choice = input(f"Enter Y for Default Parameters or N for Custom")
    if user_choice.upper() == 'Y':
        weights = utils.get_parameter_weights(1, connector)
        tabu_choice, = utils.get_parameter_tabu(1, connector)
        if weights:
            solution.incident_weights = list(weights[0])
            print("Default weights: ", solution.incident_weights)
        if tabu_choice[0]:
            solution.useTabu = True
        else:
            print("Error assigning default weights/tabu")
    if user_choice == 'N':
        for i in range(len(solution.incidentWeights)):
            userInput = input(f"Enter the value for the Weight {i}: ")
            solution.incidentWeights[i] = int(userInput)
        print(solution.incidentWeights)

max_offers = turmas * 35

for idx, offer_row in enumerate(offers_data):
    if idx >= max_offers:
        break

    offer = Offer()
    offer.Id = offer_row[0]
    offer.Disciplina = offer_row[3]
    offer.Professor = offer_row[4]
    offer.assignOfferToClass(solution1)

get_user_weights(solution1, connector)

bestSolution = solution1

solution_array = []
tabu_list_points = []
bestSolutionCost = 0
noImprovement = 0
start_time = time.time()


for i in range(1, number_iterations):
    solution, in_tabu_list = bestSolution.generateRandomSolutions()
#    if in_tabu_list:
#        tabu_list_points.append(i)
    solution.Id = i
    bestSolution = TSolutionInfo.checkAssignBestSolution(bestSolution, solution)
    bestSolutionCost = bestSolution.cost
    if bestSolutionCost < solution.cost:
        noImprovement += 1
    solution_array.append(solution)
    if noImprovement > 500:
        break

#visualize_local_search(solution_array, tabu_list_points)

print("Best Solution = ", bestSolution.Id)
print("--- %s seconds ---" % (time.time() - start_time))

    
def main():

    print("Welcome to the Schedule Manager!")

    while True:
        print("\nMenu:")
        print("1. View Schedule of a Solution")
        print("2. Manually Swap Slots")
        print("3. Check Professor Collision")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

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
            print("Exiting the Schedule Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




#print(solution1.days_of_week[1][0][0].Professor)

#solution1.days_of_week[Turma(0-2)][Day(0-4)][Slot(0-6)]