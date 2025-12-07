import HigherLevelTM
import json

# Wait time between instructions in seconds
# Ideal demo speed is 0.0001 to show final result
SPEED = 0.1
# Wether or not to display visuals
VISUALS = True

if __name__ == "__main__":
    with open('TM_instructions.json', 'r') as f:
        tm_macro = json.load(f)

    turingMachine = HigherLevelTM.HigherLevelTM(tm_macro, SPEED, VISUALS)
    print(turingMachine.executeInstructions())