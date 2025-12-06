
"""
Spigot algorithm for pi digits Turing Machine macro generator
"""
import json
import math
import pprint
from typing import Dict, Any

def generate_pi_tm_macro(n_digits: int = 33) -> Dict[str, Any]:
    """
    Generate a TM macro description for computing pi to n_digits.

    Args:
        n_digits: Number of digits (not decimal places) to compute. Defaults to 33.

    Returns:
        Dict[str, Any]: Dictionary containing the TM macro description.
    """

    # calc array length based on formula in spigot algo paper
    # len = (10n/3)
    array_length = math.ceil(10 * n_digits / 3)

    # calc tape marker positions based on array length
    # START | LEN | ARRAY (includes a0 at position 0) | PREDIGIT | NINES | OUTPUT | WORK
    start_pos = 0
    len_pos = start_pos + 1
    array_pos = len_pos + 1
    array_end = array_pos + array_length - 1
    predigit_pos = array_pos + array_length
    nines_pos = predigit_pos + 1
    output_pos = nines_pos + 1
    work_pos = output_pos + n_digits

    i = work_pos
    

    tm_macro = {
        "name": f"M_PI_{n_digits}_DIGITS",
        
        "description": f"Compute pi to {n_digits} digits using spigot algorithm",
        
        "params": {
            "n_digits": n_digits,
            "array_length": array_length,
        },

        "tape_markers": {
            "START": start_pos,
            "LEN": len_pos,
            "ARRAY": array_pos,
            "ARRAY_END": array_end,
            "PREDIGIT": predigit_pos,
            "NINES": nines_pos,
            "OUTPUT": output_pos,
            "WORK": work_pos,
            "COUNTER": work_pos,
            "i": work_pos+1,
            "q": work_pos+2,
            "d": work_pos+3
        },
        
        # fire it up
        "initial_tape": {
            start_pos: "START",
            len_pos: array_length,
            predigit_pos: -1,  # -1 bc first iteration
            nines_pos: 0,
            work_pos: 0,
        },
        
        "instructions": {
            "start": [
                "GOTO START",
                "SET 0",
                "GOTO LEN",
                f"SET {array_length}",
                "SET i 0",
                "GOTO ARRAY",
                "STATE STAGE_1_ARRAY_INIT"
            ],

            "STAGE_1_ARRAY_INIT":[
                "SET 2",
                "ADD i 1",
                "IF i >= LEN STATE STAGE_2_MAIN_LOOP",
                "MOVE_RIGHT",
                "STATE STAGE_1_ARRAY_INIT"
            ],

            "STAGE_2_MAIN_LOOP": [
                f"IF COUNTER >= {n_digits} STATE STAGE_11_FINALIZE",
                "GOTO ARRAY",
                "SET i 0",
                "STATE STAGE_3_MULTIPLY"
            ],

            "STAGE_3_MULTIPLY":  [
                "MUL 10",
                "ADD i 1",
                "IF i >= LEN STATE STAGE_4_MOD_REDUCE",
                "MOVE_RIGHT",
                "STATE STAGE_3_MULTIPLY"
            ],

            "STAGE_4_MOD_REDUCE": [
                "SET i LEN",
                "SUB i 1",
                "GOTO ARRAY",
                "MOVE_RIGHT i",
                "STATE STAGE_5_MOD_LOOP"
            ],

            "STAGE_5_MOD_LOOP": [
                "READ",
                "SET q HEAD",
                "SET d i",
                "MUL d 2",
                "ADD d 1",
                "MOD d",
                "DIV q d",
                "MUL q i",
                "SUB i 1",
                "MOVE_LEFT",
                "ADD q",
                "IF i <= 0 STATE STAGE_6_HANDLE_A0",
                "STATE STAGE_5_MOD_LOOP"
            ],

            "STAGE_6_HANDLE_A0": [
                "GOTO ARRAY",
                "READ",
                "SET q HEAD",
                "DIV q 10",
                "MOD 10",
                "IF q == 9 STATE STAGE_7_PREDIGIT_9",
                "IF q == 10 STATE STAGE_8_PREDIGIT_10",
                "STATE STAGE_9_PREDIGITS_0_TO_8"
            ],

            "STAGE_7_PREDIGIT_9": [
                "GOTO NINES",
                "ADD 1",
                "STATE STAGE_2_MAIN_LOOP"
            ],

            "STAGE_8_PREDIGIT_10": [
                "GOTO PREDIGIT",
                "READ",
                "SET d HEAD",
                "IF d != -1 STATE STAGE_8_ADD",
                "STATE STAGE_8_PREDIGIT_10_B"
            ],

            "STAGE_8_ADD": [
                "ADD d 1",
                "GOTO OUTPUT",
                "MOVE_RIGHT COUNTER",
                "SET d",
                "ADD COUNTER 1",
                "STATE STAGE_8_PREDIGIT_10_B"
            ],

            "STAGE_8_PREDIGIT_10_B": [
                "GOTO NINES",
                "READ",
                "IF HEAD == 0 STATE STAGE_10_DONE",
                "GOTO OUTPUT",
                "MOVE_RIGHT COUNTER",
                "SET 0",
                "ADD COUNTER 1",
                "GOTO NINES",
                "SUB 1",
                "STATE STAGE_8_PREDIGIT_10_B"
            ],

            "STAGE_9_PREDIGITS_0_TO_8": [
                "GOTO PREDIGIT",
                "READ",
                "IF HEAD == -1 STATE STAGE_9_PREDIGITS_0_TO_8_B",
                "IF HEAD > 8 STATE ACCEPT",
                "GOTO OUTPUT",
                "MOVE_RIGHT COUNTER",
                "SET HEAD",
                "ADD COUNTER 1",
                "STATE STAGE_9_PREDIGITS_0_TO_8_B"
            ],

            "STAGE_9_PREDIGITS_0_TO_8_B": [
                "GOTO NINES",
                "READ",
                "IF HEAD == 0 STATE STAGE_10_DONE",
                "GOTO OUTPUT",
                "MOVE_RIGHT COUNTER",
                "SET 9",
                "ADD COUNTER 1",
                "GOTO NINES",
                "SUB 1",
                "STATE STAGE_9_PREDIGITS_0_TO_8_B"
            ],

            "STAGE_10_DONE": [
                "SET PREDIGIT q",
                "SET NINES 0",
                "STATE STAGE_2_MAIN_LOOP"
            ],

            "STAGE_11_FINALIZE": [
                "GOTO PREDIGIT",
                "READ",
                "IF HEAD == -1 STATE ACCEPT",
                "IF HEAD > 8 STATE ACCEPT",
                "GOTO OUTPUT",
                "MOVE_RIGHT COUNTER",
                "SET HEAD",
                "STATE ACCEPT"
            ]
        }
    }

    return tm_macro


if __name__ == "__main__":
    pi_tm_macro = generate_pi_tm_macro(33)
    with open('TM_instructions.json', 'w') as f:
        json.dump(pi_tm_macro, f, indent=4)

    pprint.pprint(pi_tm_macro)
