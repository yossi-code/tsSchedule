import random
from tabulate import tabulate

slots = 35
tabu_list = []


# F0 = Dia vago (7 slots)  Peso -> 10
# F1 = Buraco 3 (3 slots)  Peso -> 5
# F2 = Buraco 1 (1 slot)   Peso -> 1
# F3 = Colisao no Prof     Peso -> 20
# F4 = Buraco 2 (2 slots)  Peso -> 3

class TSolutionInfo:
    def __init__(self, turmas):
        self.Id = 0 
        self.cost = 0
        self.turmas = turmas
        self.tabu_flag = False
        self.incident_weights = [0] * 5
        self.incident_counter = [0] * len(self.incident_weights)
        self.class_slots = [[-1] * self.turmas for _ in range(slots)]
        self.days_of_week = [
            [[-1] * 7 for _ in range(5)] for _ in range(self.turmas)
        ]
        self.useTabu = True

    def assignWeek(self, offer_index, Turma, Offer):
        self.days_of_week[Turma][offer_index // 7][offer_index % 7] = Offer
        print("Turma Assigned", Turma)

    def printWeekDay(self, turma):
        print(self.days_of_week[turma])

    def solutionCosts(self):
        self.incident_counter = [0 for _ in self.incident_counter]
        # For each turma (3)
        for index_turma, turma in enumerate(self.days_of_week):
            # For i in range (5) - Week Days
            for index_day, day in enumerate(turma):
                # Reset empty slots count each day
                self.empty_slots_count = 0 
                for index_slot, slot in enumerate(day):
                    if (slot == -1):
                        self.empty_slots_count += 1
                    else:
                        self.empty_slots_count = 0
                    if self.empty_slots_count // 7 > 0:
                        self.incident_counter[0] += 1
                        self.incident_counter[2] -= 6
                        self.empty_slots_count = 0
                    if self.empty_slots_count // 3 > 0:
                        self.incident_counter[1] += 1
                        self.incident_counter[2] -= 2
                        self.empty_slots_count = 0
                    if self.empty_slots_count // 2 > 0:
                        self.incident_counter[4] += 1
                        self.incident_counter[2] -= 1
                        self.empty_slots_count = 0
                    if self.empty_slots_count // 1 > 0:
                        self.incident_counter[2] += 1
                    
        self.checkProfessorSchedule()
        self.cost = sum([count * weight for count, weight in zip(self.incident_counter, self.incident_weights)])
        return(self.cost)
    
    def get_tabu_list(self):
        return tabu_list
    
    def printSolution(self):
        for row in self.class_slots:
            for slot in row:
                if slot != -1:
                    print(slot.Id, end=' ')
                else:
                    print(slot, end=' ')
            print()

    def generateRandomSolutions(self):
        while True:
            row_idx1 = random.randint(0, len(self.class_slots)-1)
            col_idx1 = random.randint(0, len(self.class_slots[0])-1) 
            row_idx2 = random.randint(0, len(self.class_slots)-1)
            col_idx2 = random.randint(0, len(self.class_slots[0])-1)

            in_tabu_list = (row_idx1, col_idx1, row_idx2, col_idx2) in tabu_list

            if in_tabu_list and self.useTabu:
                print("Solution is in Tabu list. Generating a new solution.")
                print("ID = ", self.Id)
                print("Tabu: ", row_idx1, col_idx1, row_idx2, col_idx2)
                self.tabu_flag = True

            solution2 = TSolutionInfo(self.turmas)
            solution2.incident_weights = self.incident_weights
            solution2.useTabu = self.useTabu
            solution2.class_slots = [row.copy() for row in self.class_slots]
            solution2.days_of_week = [
                [day.copy() for day in turma]
                for turma in self.days_of_week
            ]
            solution2.class_slots[row_idx1][col_idx1], solution2.class_slots[row_idx2][col_idx2] = \
                solution2.class_slots[row_idx2][col_idx2], solution2.class_slots[row_idx1][col_idx1]
            solution2.assignWeek(row_idx1, col_idx1, solution2.class_slots[row_idx1][col_idx1])
            solution2.assignWeek(row_idx2, col_idx2, solution2.class_slots[row_idx2][col_idx2])

            # Add the solution to the tabu list
            if self.useTabu:
                self.addTabuList(row_idx1, col_idx1, row_idx2, col_idx2)
                self.addTabuList(row_idx2, col_idx2, row_idx1, col_idx1)

            return solution2, in_tabu_list

    def addTabuList(self, row1, col1, row2, col2):
        tabu_list.append((row1, col1, row2, col2))
        while len(tabu_list) > 50:
            tabu_list.pop(0)


    def checkAssignBestSolution(solution1, solution2):
        if (solution2.solutionCosts() < solution1.solutionCosts()):
            #print('S1 Cost: ', solution1.solutionCosts())
            #print('S2 Cost: ', solution2.solutionCosts())
            return solution2
        else:
            #print('S1 Cost: ', solution1.solutionCosts())
            #print('S2 Cost: ', solution2.solutionCosts())
            return solution1
        
    def printSchedule(self):
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        turma_labels = [f"Turma {i+1}" for i in range(self.turmas)]

        for turma_idx, turma in enumerate(self.days_of_week):
            print(f"\n{turma_labels[turma_idx]} Schedule:\n")

            # Create table_data for the current turma
            table_data = []
            for day_idx, day in enumerate(turma):
                day_schedule = [week_days[day_idx]]
                for slot_idx, slot in enumerate(day):
                    if slot == -1:
                        day_schedule.append("Empty")
                    else:
                        day_schedule.append(f"{slot.Disciplina} - {slot.Professor}")
                table_data.append(day_schedule)

            print(tabulate(table_data, headers=["Day", "Slot 1", "Slot 2", "Slot 3", "Slot 4", "Slot 5", "Slot 6", "Slot 7"], tablefmt="pretty"))
            print(self.incident_counter)
            print(self.incident_weights)
            print("Solution Cost: ", self.solutionCosts())
            print("Tabu: ", self.tabu_flag)
    
    def checkProfessorSchedule(self):
        professor_slots = {}

        for turma_idx, turma in enumerate(self.days_of_week):
            for day_idx, day in enumerate(turma):
                for slot_idx, slot in enumerate(day):
                    if slot != -1:
                        professor = slot.Professor
                        professor_key = (professor, day_idx, slot_idx)  # Use tuple as the key
                        if professor_key in professor_slots:
                            professor_slots[professor_key].append(turma_idx)
                            self.incident_counter[3] += 1
                        else:
                            professor_slots[professor_key] = [turma_idx]

        # Print the professors assigned to the same day and slot in different turmas
        for professor_key, turmas in professor_slots.items():
            if len(turmas) > 1:
                professor, day_idx, slot_idx = professor_key
                day_display, slot_display = day_idx +1, slot_idx +1
                print(f"Professor {professor} is assigned to Day {day_display}, Slot {slot_display} in Turmas: {turmas}")

    def swapSlotsManually(self, turma1, day1, slot1, turma2, day2, slot2):
        if turma1 not in range(len(self.days_of_week)) or turma2 not in range(len(self.days_of_week)):
            print("Invalid Turma index.")
            return
        if day1 not in range(len(self.days_of_week[0])) or day2 not in range(len(self.days_of_week[0])):
            print("Invalid Day index.")
            return
        if slot1 not in range(len(self.days_of_week[0][0])) or slot2 not in range(len(self.days_of_week[0][0])):
            print("Invalid Slot index.")
            return

        self.days_of_week[turma1][day1][slot1], self.days_of_week[turma2][day2][slot2] = \
            self.days_of_week[turma2][day2][slot2], self.days_of_week[turma1][day1][slot1]

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
        return self
    
    def assignOfferToClass(self, solution):
        num_rows = len(solution.class_slots)
        num_cols = len(solution.class_slots[0])

        for col_idx in range(num_cols):
                for row_idx in range(num_rows):
                        slot = solution.class_slots[row_idx][col_idx]
                        if slot == -1:
                        # Assign the offer to the class slot
                                solution.class_slots[row_idx][col_idx] = self
                                solution.assignWeek(row_idx, col_idx, self)
                                break