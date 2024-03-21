import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define fuzzy variables
solution_quality = ctrl.Antecedent(np.arange(0, 11, 1), 'solution_quality')
diversity = ctrl.Antecedent(np.arange(0, 11, 1), 'diversity')
tabu_tenure = ctrl.Consequent(np.arange(0, 11, 1), 'tabu_tenure')

# Define fuzzy sets
solution_quality['low'] = fuzz.trimf(solution_quality.universe, [0, 0, 5])
solution_quality['medium'] = fuzz.trimf(solution_quality.universe, [0, 5, 10])
solution_quality['high'] = fuzz.trimf(solution_quality.universe, [5, 10, 10])

diversity['low'] = fuzz.trimf(diversity.universe, [0, 0, 5])
diversity['medium'] = fuzz.trimf(diversity.universe, [0, 5, 10])
diversity['high'] = fuzz.trimf(diversity.universe, [5, 10, 10])

tabu_tenure['low'] = fuzz.trimf(tabu_tenure.universe, [0, 0, 5])
tabu_tenure['medium'] = fuzz.trimf(tabu_tenure.universe, [0, 5, 10])
tabu_tenure['high'] = fuzz.trimf(tabu_tenure.universe, [5, 10, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(solution_quality['low'] & diversity['low'], tabu_tenure['high'])
rule2 = ctrl.Rule(solution_quality['medium'] | diversity['medium'], tabu_tenure['medium'])
rule3 = ctrl.Rule(solution_quality['high'] & diversity['high'], tabu_tenure['low'])

# Create control system
tabu_tenure_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tabu_tenure_simulation = ctrl.ControlSystemSimulation(tabu_tenure_ctrl)

# Simulate fuzzy inference
tabu_tenure_simulation.input['solution_quality'] = 7
tabu_tenure_simulation.input['diversity'] = 4
tabu_tenure_simulation.compute()

# Defuzzify result
print("New Tabu Tenure:", tabu_tenure_simulation.output['tabu_tenure'])