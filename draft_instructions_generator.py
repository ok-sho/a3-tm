"""
Spigot algorithm for pi digits Turing Machine macro generator
"""
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
    # START | LEN | ARRAY | PREDIGIT | NINES | OUTPUT | WORK
    start_pos = 0
    len_pos = start_pos + 1
    array_pos = len_pos + 1
    predigit_pos = array_pos + array_length
    nines_pos = predigit_pos + 1
    output_pos = nines_pos + 1
    work_pos = output_pos + n_digits

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
            "PREDIGIT": predigit_pos,
            "NINES": nines_pos,
            "OUTPUT": output_pos,
            "WORK": work_pos,
        },
        
        # fire it up
        "initial_tape": {
            start_pos: "START",
            len_pos: array_length,
            predigit_pos: -1,  # -1 bc first iteration
            nines_pos: 0,
            work_pos: 0,
        },
        
        "instructions": [
            # following the steps in the high-level/Sipsery description
            # shared on discord, but I broke that stage 4 into two
            
            # -----------------------------------------------
            # Stage 1: Initialize the tape w lotsa 2s -------
            # -----------------------------------------------
            "LABEL STAGE_1_INIT",
            f"ARRAY_INIT ARRAY {array_length} 2",
            
            # ----------------------------------------------
            # Stage 2: Main loop ---------------------------
            # ----------------------------------------------
            "LABEL STAGE_2_MAIN_LOOP",
            
            # Move to WORK and read the counter.
            # If counter = 33, go to stage 10.
            # Otherwise, continue to stage 3.
            "VAR_READ WORK counter",
            f"COMPARE counter {n_digits}",
            "JUMP_IF_GE STAGE_11_FINALIZE",
            
            # -----------------------------------------------
            # Stage 3: 10*2 over and over -------------------
            # -----------------------------------------------
            "LABEL STAGE_3_MULTIPLY",
            "ARRAY_MULTIPLY ARRAY 10",
            
            # -----------------------------------------------
            # Stage 4: Modulo reduction w carry -------------
            # -----------------------------------------------
            "LABEL STAGE_4_MOD_REDUCE",
            
            "SET q 0",  # initialize carry q = 0
            "VAR_READ LEN len",
            
            # for i from len-1 down to 1
            "FOR_REVERSE i len 1",
            
            # read a[i]
            "ARRAY_GET ARRAY i a_i",
            "SET x a_i",
            
            # compute x = a[i] + qi
            "MULTIPLY_ADD x q i"
            
            # compute modulus m = 2i-1
            "SET m i",
            "MULTIPLY m 2",
            "SUBTRACT m 1",
            
            # find q = x / m  and  r = x mod m ,
            "DIVIDE_MOD x m q r"
            
            # write r back to a[i], and update carry q
            "ARRAY_SET ARRAY i r",
            "END_FOR",
            
            # ----------------------------------------------
            # Stage 5: Handle a[0] separately --------------
            # ----------------------------------------------
            "LABEL STAGE_5_HANDLE_A0",
            
            # after the loop, read a[0],
            "ARRAY_GET ARRAY 0 a_0",
            
            # divide it by 10 to get quotient q (the new predigit)
            # and get remainder r = q mod 10,
            "DIVIDE_MOD a_0 10 predigit remainder",
            
            # and write r to a[0]
            "ARRAY_SET ARRAY 0 remainder",
            
            # ----------------------------------------------
            # Stage 6: Handle predigit ---------------------
            # ----------------------------------------------
            "LABEL STAGE_6_HANDLE_PREDIGIT",
            
            # if q = 9, go to stage 7
            "COMPARE predigit 9",
            "JUMP_IF_EQ STAGE_7_PREDIGIT_9",
            
            # If q = 10, go to stage 8
            "COMPARE predigit 10",
            "JUMP_IF_EQ STAGE_8_PREDIGIT_10",
            
            # if q ∈ {0,1,2,3,4,5,6,7,8}, go to stage 9
            "JUMP STAGE_9_PREDIGITS_0_TO_8",
            
            # --------------------------------------------------
            # Stage 7: When predigit is 9 ----------------------
            # --------------------------------------------------
            "LABEL STAGE_7_PREDIGIT_9",
            
            # increment the nines counter by 1. Go to stage 10.
            "VAR_INCREMENT NINES",
            "JUMP STAGE_10_INCREMENT",
            
            # --------------------------------------------------
            # Stage 8: When predigit is 10 ---------------------
            # --------------------------------------------------
            "LABEL STAGE_8_PREDIGIT_10",
            
            # Move to PREDIGIT and read the held predigit p.
            "VAR_READ PREDIGIT p",
            
            # Write digit p+1 to the next empty position in OUTPUT.
            "ADD p 1",
            "OUTPUT_DIGIT p",
            
            # write a number of zeros equal to the
            # counter in NINES to OUTPUT.
            "VAR_READ NINES nines_count",
            "FOR_REPEAT nines_count",
            "OUTPUT_DIGIT 0",
            "END_FOR",
            
            # Reset PREDIGIT to 0 and NINES to 0. Go to stage 10.
            "VAR_WRITE PREDIGIT 0",
            "VAR_WRITE NINES 0",
            "JUMP STAGE_10_INCREMENT",
            
            # --------------------------------------------------
            # Stage 9: When predigit is 0 to 8 -------------------
            # --------------------------------------------------
            "LABEL STAGE_9_PREDIGITS_0_TO_8",
            
            # If PREDIGIT =/= -1 (not first iteration),
            "VAR_READ PREDIGIT p",
            "COMPARE p -1",
            "JUMP_IF_NEQ OUTPUT_PREDIGIT",
            "JUMP SKIP_OUTPUT_PREDIGIT",
            
            # write the held predigit to the next
            # empty position in OUTPUT.
            "LABEL OUTPUT_PREDIGIT",
            "OUTPUT_DIGIT p",
            
            # Then write a number of 9s
            # equal to the counter in NINES
            # to OUTPUT.
            "LABEL SKIP_OUTPUT_PREDIGIT",
            "VAR_READ NINES nines_count",
            "FOR_REPEAT nines_count",
            "OUTPUT_DIGIT 9",
            "END_FOR",
            
            # Store q in PREDIGIT and
            # reset NINES to 0. Go to stage 10.
            "VAR_WRITE PREDIGIT predigit",
            "VAR_WRITE NINES 0",
            
            # --------------------------------------------------
            # Stage 10: Increment counter and loop -------------
            # -------------------------------------------------
            "LABEL STAGE_10_INCREMENT",
            "VAR_INCREMENT WORK",
            "JUMP STAGE_2_MAIN_LOOP",
            
            # --------------------------------------------------
            # Stage 11: Output final predigit and accept -------
            # --------------------------------------------------
            "LABEL STAGE_11_FINALIZE",
            
            # Move to PREDIGIT and write its value to the
            # next empty position in OUTPUT. *Accept*."
            "VAR_READ PREDIGIT p",
            "OUTPUT_DIGIT p",
            
            # yeehaw
            "ACCEPT", 
        ],
        
        #--------------------------------------------------------
        # --------------------------------------------------
        # Definitions for higher level macros --------------
        # ---------------------------------------------------
        # --------------------------------------------------------
        
        "macro_defs": {
            
            # Array operations --------------------------------
            
            "ARRAY_INIT": {
                "description": "Initialize array with length copies of value",
                "parameters": ["array_marker", "length", "value"],
                "expands_to": [
                    "MOVE_TO {array_marker}",
                    "SET _i 0",
                    "LABEL ARRAY_INIT_LOOP",
                    "COMPARE _i {length}",
                    "JUMP_IF_GE ARRAY_INIT_END",
                    "WRITE {value}",
                    "MOVE_RIGHT 1",
                    "ADD _i 1",
                    "JUMP ARRAY_INIT_LOOP",
                    "LABEL ARRAY_INIT_END",
                ],
            },
            
            "ARRAY_GET": {
                "description": "Read array[index] into variable",
                "parameters": ["array_marker", "index", "var"],
                "expands_to": [
                    "MOVE_TO {array_marker}",
                    "MOVE_RIGHT {index}",
                    "READ {var}",
                ],
            },
            
            "ARRAY_SET": {
                "description": "Write value to array[index]",
                "parameters": ["array_marker", "index", "value"],
                "expands_to": [
                    "MOVE_TO {array_marker}",
                    "MOVE_RIGHT {index}",
                    "WRITE {value}",
                ],
            },
            
            "ARRAY_MULTIPLY": {
                "description": "Multiply each array element by multiplier",
                "parameters": ["array_marker", "multiplier"],
                "expands_to": [
                    "VAR_READ LEN _len",
                    "SET _i 0",
                    "LABEL ARRAY_MULTIPLY_LOOP",
                    "COMPARE _i _len",
                    "JUMP_IF_GE ARRAY_MULTIPLY_END",
                    "ARRAY_GET {array_marker} _i _elem",
                    "MULTIPLY _elem {multiplier}",
                    "ARRAY_SET {array_marker} _i _elem",
                    "ADD _i 1",
                    "JUMP ARRAY_MULTIPLY_LOOP",
                    "LABEL ARRAY_MULTIPLY_END",
                ],
            },
            
            # Variable operations -------------------------------
            
            "VAR_READ": {
                "description": "Read value at marker into variable",
                "parameters": ["marker", "var"],
                "expands_to": [
                    "MOVE_TO {marker}",
                    "READ {var}",
                ],
            },
            
            "VAR_WRITE": {
                "description": "Write variable value to marker",
                "parameters": ["marker", "value"],
                "expands_to": [
                    "MOVE_TO {marker}",
                    "WRITE {value}",
                ],
            },
            
            "VAR_INCREMENT": {
                "description": "Increment value at marker by 1",
                "parameters": ["marker"],
                "expands_to": [
                    "MOVE_TO {marker}",
                    "READ _val",
                    "ADD _val 1",
                    "WRITE _val",
                ],
            },
            
            # Loopssss ---------------------------------------
            
            "FOR_REVERSE": {
                "description": "Loop from start-1 down to end (inclusive)",
                "parameters": ["var", "start", "end"],
                "expands_to": [
                    "SET {var} {start}",
                    "SUBTRACT {var} 1",
                    "LABEL FOR_REVERSE_LOOP",
                    "COMPARE {var} {end}",
                    "JUMP_IF_LT FOR_REVERSE_END",
                    
                    "LOOP_BODY_PLACEHOLDER",
                    
                    "SUBTRACT {var} 1",
                    "JUMP FOR_REVERSE_LOOP",
                    "LABEL FOR_REVERSE_END",
                ],
            },
            
            "FOR_REPEAT": {
                "description": "Repeat loop body count times",
                "parameters": ["count"],
                "expands_to": [
                    "SET _loop_counter 0",
                    "LABEL FOR_REPEAT_LOOP",
                    "COMPARE _loop_counter {count}",
                    "JUMP_IF_GE FOR_REPEAT_END",
                    
                    "LOOP_BODY_PLACEHOLDER",
                    
                    "ADD _loop_counter 1",
                    "JUMP FOR_REPEAT_LOOP",
                    "LABEL FOR_REPEAT_END",
                ],
            },
            
            "END_FOR": {
                "description": "Label indicating end of a for loop",
                "parameters": [],
                "expands_to": [],
            },
            
            # Output those digits --------------------------------
            
            "OUTPUT_DIGIT": {
                "description": "append digit to OUTPUT section",
                "parameters": ["digit"],
                "expands_to": [
                    "MOVE_TO OUTPUT",
                    "LABEL OUTPUT_FIND_END",
                    "READ _temp",
                    # assumes empty spots contain 0
                    "COMPARE _temp 0",
                    "JUMP_IF_EQ OUTPUT_FOUND_END",
                    "MOVE_RIGHT 1",
                    "JUMP OUTPUT_FIND_END",
                    "LABEL OUTPUT_FOUND_END",
                    "WRITE {digit}",
                ],
            },
            
            # Arithmetic helper ------------------------------
            
            "MULTIPLY_ADD": {
                "description": "dest = dest + (multiplier * adder)",
                "parameters": ["dest", "multiplier", "adder"],
                "expands_to": [
                    "SET _temp {multiplier}",
                    "MULTIPLY _temp {adder}",
                    "ADD {dest} _temp",
                ],
            },
            
            #-------------------------------------------------------------
            # -------------------------------------------------------------
            # Basic instructions the simulator will implement -------------
            # -------------------------------------------------------------
            
            "MOVE_TO": {
                "description": "Move tape head to marker position",
                "parameters": ["marker"],
                "primitive": True,
            },
            
            "MOVE_RIGHT": {
                "description": "Move tape head n steps to the right",
                "parameters": ["n"],
                "primitive": True,
            },
            
            "READ": {
                "description": "Read value at current tape head into variable",
                "parameters": ["var"],
                "primitive": True,
            },
            
            "WRITE": {
                "description": "Write value to current tape head",
                "parameters": ["value"],
                "primitive": True,
            },
            
            "SET": {
                "description": "Set variable to value",
                "parameters": ["var", "value"],
                "primitive": True,
            },
            
            "ADD": {
                "description": "Add value to variable",
                "parameters": ["var", "value"],
                "primitive": True,
            },
            
            "SUBTRACT": {
                "description": "Subtract value from variable",
                "parameters": ["var", "value"],
                "primitive": True,
            },
            
            "MULTIPLY": {
                "description": "Multiply variable by value",
                "parameters": ["var", "value"],
                "primitive": True,
            },
            
            "DIVIDE_MOD": {
                "description": "Divide and get quotient and remainder",
                "parameters": [
                    "numerator",
                    "denominator",
                    "quotient_var",
                    "remainder_var",
                ],
                "primitive": True,
            },
            
            "COMPARE": {
                "description": "Compare two values, set flags",
                "parameters": ["value1", "value2"],
                "primitive": True,
                # will need to set flags for LT, EQ, or GT
            },
            
            "JUMP": {
                "description": "Unconditional jump to label",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "JUMP_IF_EQ": {
                "description": "Jump to label if last comparison was equal",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "JUMP_IF_NEQ": {
                "description": "Jump to label if last comparison was not equal",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "JUMP_IF_LT": {
                "description": "Jump to label if last comparison was less than",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "JUMP_IF_GE": {
                "description": "Jump to label if last comparison was greater than or equal",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "LABEL": {
                "description": "Define a label for jumps",
                "parameters": ["label"],
                "primitive": True,
            },
            
            "ACCEPT": {"description": "All done!", "parameters": [], "primitive": True},
            
            
            # will also need other stuff in simulator like REJECT
            # but this TM doesn't use it
        },
    }

    return tm_macro


if __name__ == "__main__":
    pi_tm_macro = generate_pi_tm_macro(33)
    pprint.pprint(pi_tm_macro)
