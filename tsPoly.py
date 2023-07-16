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

def assignOfferToClass(offers, solution):
    offer_index = 0
    num_rows = len(solution.classSlots)
    num_cols = len(solution.classSlots[0])

    for col_idx in range(num_cols):
            for row_idx in range(num_rows):
                    slot = solution.classSlots[row_idx][col_idx]
                    if slot == -1:
                    # Assign the offer to the class slot
                            solution.classSlots[row_idx][col_idx] = offers[offer_index]
                            solution.assignWeek(row_idx, col_idx, offers[offer_index])
                            offer_index += 1
                            if offer_index == len(offers):
                                    random.shuffle(offers)
                                    offer_index = 0
                                    break


solution1 = TSolutionInfo()
solution1.Id = 1

assignOfferToClass(offers, solution1)

# Print the assigned offers
for row in solution1.classSlots:
    for slot in row:
        if slot != -1:
            # Access and process the element
            print(slot.Id, end=' ')
        else:
            print(slot, end=' ')
    print()

solution1.solutionCosts()

#print(solution1.days_of_week[1][0][0].Professor)

#solution1.days_of_week[Turma(0-2)][Day(0-4)][Slot(0-6)]