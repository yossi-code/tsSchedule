slots = 35
turmas = 3

class TSolutionInfo:
    Id = 0
    classSlots = [[-1] * turmas for _ in range(slots)]
    days_of_week = [
        [[None] * 7 for _ in range(5)],
        [[None] * 7 for _ in range(5)],
        [[None] * 7 for _ in range(5)],
    ]

    def assignWeek(self, offer_index, Turma, Offer):
        self.days_of_week[Turma][offer_index // 7][offer_index % 7] = Offer

    def printWeekDay(self, turma):
        print(self.days_of_week[turma])

    def solutionCosts(self):
        # For each turma (3)
        cost = 0
        for index_turma, turma in enumerate(self.days_of_week):
            # For i in range (5) - Week Days
            for index_day, day in enumerate(turma):
                # Reset empty slots count each day
                empty_slots_count = 0
                for index_slot, slot in enumerate(day):
                    if (slot is None):
                        empty_slots_count += 1
                        print('Turma: ', index_turma, 'Day: ', index_day, 'Slot - vago: ', index_slot, 'Slot Count: ', empty_slots_count)
                    else:
                        print('Turma: ', index_turma, 'Day: ', index_day, 'OfferId: ', slot.Id)
                if empty_slots_count // 7 > 0:
                        cost += 10
    
        print("Total cost:", cost)



class Offer:
    def __init__(self):
        self.Disciplina = ''
        self.Professor = ''
        self.Id = 0

    def assignOffer(self, Id, Disciplina, Professor):
        self.Disciplina = Disciplina
        self.Professor = Professor
        self.Id = Id
        print("Offer assigned, this is the Offer ID:", Id)
        return self  # Return the modified instance of the class