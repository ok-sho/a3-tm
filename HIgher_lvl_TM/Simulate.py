import HigherLevelTM
import json

if __name__ == "__main__":
    with open('TM_instructions.json', 'r') as f:
        tm_macro = json.load(f)

    turingMachine = HigherLevelTM.HigherLevelTM(tm_macro)
    print(turingMachine.executeInstructions())