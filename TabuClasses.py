import random
from tabulate import tabulate

slots = 35
turmas = 3

class TSolutionInfo:
    Id = 0
    cost = 0
    classSlots = [[-1] * turmas for _ in range(slots)]
    days_of_week = [
        [[-1] * 7 for _ in range(5)],
        [[-1] * 7 for _ in range(5)],
        [[-1] * 7 for _ in range(5)],
    ]

    def assignWeek(self, offer_index, Turma, Offer):
        self.days_of_week[Turma][offer_index // 7][offer_index % 7] = Offer

    def printWeekDay(self, turma):
        print(self.days_of_week[turma])

    def solutionCosts(self):
        self.cost = 0
        # For each turma (3)
        for index_turma, turma in enumerate(self.days_of_week):
            # For i in range (5) - Week Days
            for index_day, day in enumerate(turma):
                # Reset empty slots count each day
                self.empty_slots_count = 0
                for index_slot, slot in enumerate(day):
                    if (slot == -1):
                        self.empty_slots_count += 1
                        self.cost += 1
                if self.empty_slots_count // 7 > 0:
                        self.cost += 10
                if self.empty_slots_count // 3 > 0:
                        self.cost += 2
        self.checkProfessorSchedule()
        return(self.cost)
    
    def printSolution(self):
        for row in self.classSlots:
            for slot in row:
                if slot != -1:
                    # Access and process the element
                    print(slot.Id, end=' ')
                else:
                    print(slot, end=' ')
            print()

    def switchRandomSlots(solution1, solution2):
        solution2.classSlots = [row.copy() for row in solution1.classSlots]
        solution2.days_of_week = [
            [day.copy() for day in turma]
            for turma in solution1.days_of_week
        ]

        # Randomly switch two class slots in solution2
        row_idx1 = random.randint(0, len(solution2.classSlots)-1)
        col_idx1 = random.randint(0, len(solution2.classSlots[0])-1)
        row_idx2 = random.randint(0, len(solution2.classSlots)-1)
        col_idx2 = random.randint(0, len(solution2.classSlots[0])-1)

        solution2.classSlots[row_idx1][col_idx1], solution2.classSlots[row_idx2][col_idx2] = \
        solution2.classSlots[row_idx2][col_idx2], solution2.classSlots[row_idx1][col_idx1]

        solution2.assignWeek(row_idx1, col_idx1, solution2.classSlots[row_idx1][col_idx1])
        solution2.assignWeek(row_idx2, col_idx2, solution2.classSlots[row_idx2][col_idx2])

    def checkAssignBestSolution(solution1, solution2):
        if (solution2.solutionCosts() <= solution1.solutionCosts()):
            print('S1 Cost: ', solution1.solutionCosts())
            print('S2 Cost: ', solution2.solutionCosts())
            return solution2
        else:
            print('Solution 1 < Solution 2, S1 Cost: ', solution1.cost, 'S2 Cost: ', solution2.cost)
            return solution1
        
    def printSchedule(self):
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        turma_labels = ["Turma 1", "Turma 2", "Turma 3"]

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
            self.solutionCosts()
            print("Solution Cost: ", self.cost)
    
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
                            self.cost += 20
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
        return self  # Return the modified instance of the class
    
    def assignOfferToClass(self, solution):
        offer_index = 0
        num_rows = len(solution.classSlots)
        num_cols = len(solution.classSlots[0])

        for col_idx in range(num_cols):
                for row_idx in range(num_rows):
                        slot = solution.classSlots[row_idx][col_idx]
                        if slot == -1:
                        # Assign the offer to the class slot
                                solution.classSlots[row_idx][col_idx] = self[offer_index]
                                solution.assignWeek(row_idx, col_idx, self[offer_index])
                                offer_index += 1
                                if offer_index == len(self):
                                        random.shuffle(self)
                                        offer_index = 0
                                        break