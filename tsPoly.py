import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TabuClasses import TSolutionInfo, Offer

# Como achar o dia? Slot 10 -> 10 / 7 (Dia da semana) -> 10 MOD 7 (Slot daquele dia)

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


solution1 = TSolutionInfo()
solution1.Id = 0
Offer.assignOfferToClass(offers, solution1)

bestSolution = solution1

# Print the assigned offers
solution1.printSolution()
print(solution1.solutionCosts())

numberOfIterations = 100
solutionArray = []
bestSolutionCost = 0
noImprovement = 0

for i in range(1, numberOfIterations):
    solution = TSolutionInfo()
    solution.Id = i
    TSolutionInfo.switchRandomSlots(bestSolution, solution)
    bestSolution = TSolutionInfo.checkAssignBestSolution(bestSolution, solution)
    bestSolutionCost = bestSolution.cost
    if bestSolutionCost < solution.cost:
         noImprovement += 1
    solutionArray.append(solution)
    if noImprovement > 100:
        break

print("Best Solution: ")
bestSolution.printSolution()
print("Best Solution Cost: ", bestSolution.solutionCosts())
bestSolution.printSchedule()




#print(solution1.days_of_week[1][0][0].Professor)

#solution1.days_of_week[Turma(0-2)][Day(0-4)][Slot(0-6)]