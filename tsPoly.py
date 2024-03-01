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

parameters = utils.get_parameters(connector)
offers_data = utils.get_offers(connector)

solution1 = TSolutionInfo()
solution1.Id = 0

for offer_row in offers_data:
    offer = Offer()
    offer.Id, offer.Disciplina, offer.Professor = offer_row
    offer.assignOfferToClass(solution1)

bestSolution = solution1

numberOfIterations = int(input("Number of Iterations?\n"))
TSolutionInfo.getUserWeights(solution1)
TSolutionInfo.getTabuBool(solution1)
solutionArray = []
bestSolutionCost = 0
noImprovement = 0
start_time = time.time()

for i in range(1, numberOfIterations):
    solution = bestSolution.generateRandomSolutions()
    solution.Id = i
    bestSolution = TSolutionInfo.checkAssignBestSolution(bestSolution, solution)
    bestSolutionCost = bestSolution.cost
    if bestSolutionCost < solution.cost:
        noImprovement += 1
    solutionArray.append(solution)
    if noImprovement > 200:
        break

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
            for i, solution in enumerate(solutionArray):
                print(f"{i + 1}. Solution {solution.Id} - Cost: {solution.cost}")
            try:
                selected_solution_index = int(input("Enter the solution number: ")) - 1
                selected_solution = solutionArray[selected_solution_index]
                selected_solution.printSchedule()
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        elif choice == "2":
            print("Select a solution to swap slots:")
            for i, solution in enumerate(solutionArray):
                print(f"{i + 1}. Solution {solution.Id}")
            try:
                selected_solution_index = int(input("Enter the solution number: ")) - 1
                selected_solution = solutionArray[selected_solution_index]
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
            selected_solution = solutionArray[selected_solution_index]
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