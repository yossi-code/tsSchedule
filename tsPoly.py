import random
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TabuClasses import TSolutionInfo, Offer

# Como achar o dia? Slot 10 -> 10 / 7 (Dia da semana) -> 10 MOD 7 (Slot daquele dia)

start_time = time.time()

offers = []
offers.append(Offer().assignOffer('1', 'Matemática', 'Wanderley'))
offers.append(Offer().assignOffer('2', 'Matemática', 'Wanderley'))
offers.append(Offer().assignOffer('3', 'Matemática', 'Wanderley'))
offers.append(Offer().assignOffer('4', 'Matemática', 'Wanderley'))
offers.append(Offer().assignOffer('5', 'Física', 'Jose'))
offers.append(Offer().assignOffer('6', 'Física', 'Jose'))
offers.append(Offer().assignOffer('7', 'Física', 'Jose'))
offers.append(Offer().assignOffer('8', 'Física', 'Jose'))
offers.append(Offer().assignOffer('9', 'Química', 'Maria' ))
offers.append(Offer().assignOffer('10', 'Química', 'Maria'))
offers.append(Offer().assignOffer('11', 'Biologia', 'Fernando'))
offers.append(Offer().assignOffer('12', 'Biologia', 'Fernando'))
offers.append(Offer().assignOffer('13', 'História', 'Fernando'))
offers.append(Offer().assignOffer('14', 'História', 'Fernando'))
offers.append(Offer().assignOffer('15', 'Artes', 'Maria'))
offers.append(Offer().assignOffer('16', 'Artes', 'Maria'))
offers.append(Offer().assignOffer('17', 'Economia', 'Raquel'))
offers.append(Offer().assignOffer('18', 'Economia', 'Raquel'))
offers.append(Offer().assignOffer('19', 'Sociologia', 'Fernando'))
offers.append(Offer().assignOffer('20', 'Sociologia', 'Fernando'))
offers.append(Offer().assignOffer('21', 'Programacao', 'Geovanna'))
offers.append(Offer().assignOffer('22', 'Programacao', 'Geovanna'))
offers.append(Offer().assignOffer('23', 'Programacao', 'Geovanna'))
offers.append(Offer().assignOffer('24', 'Programacao', 'Geovanna'))
offers.append(Offer().assignOffer('25', 'Estatistica', 'Myrella'))
offers.append(Offer().assignOffer('28', 'Estatistica', 'Myrella'))
offers.append(Offer().assignOffer('26', 'Estatistica', 'Myrella'))

solution1 = TSolutionInfo()
solution1.Id = 0
Offer.assignOfferToClass(offers, solution1)

bestSolution = solution1

numberOfIterations = int(input("Number of Iterations?\n"))
TSolutionInfo.getUserWeights(solution1)
TSolutionInfo.getTabuBool(solution1)
solutionArray = []
bestSolutionCost = 0
noImprovement = 0

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

def saveSolutionsToCSV(solutionArray, filename='solutions.csv'):
    solutions_df = pd.DataFrame([solution.__dict__ for solution in solutionArray])
    solutions_df.to_csv(filename, index=False)

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
    saveSolutionsToCSV(solutionArray)




#print(solution1.days_of_week[1][0][0].Professor)

#solution1.days_of_week[Turma(0-2)][Day(0-4)][Slot(0-6)]