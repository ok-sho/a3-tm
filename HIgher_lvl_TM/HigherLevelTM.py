
class HigherLevelTM:
    INSTRUCTION_LIMIT = 100000
    def __init__(self, turing_machine):
        self.instructions = turing_machine["instructions"]
        self.state = "start"
        self.headPos = 0
        self.head = None
        self.tape = []
        
        self.variables = turing_machine['tape_markers']

        self.currInstruction = 0

    def read_instruction(self, instruction):
        print(instruction)
        type = instruction.split()[0]
        parameters = []
        

        if len(instruction.split()) > 1: 
            for parameter in instruction.split()[1:]:
                parameters.append(parameter)
        print(parameters)

        # FOR ALL THESE INSTRUCTIONS, value can be either an integer or a variable name <--- IMPORTANT
        match type:
            # Reads value at head position into "head" variable
            case "READ":
                self.head = self.tape[self.headPos]

            # Adds value to head position (ADD <value>) or variable (ADD <var> <value>)
            case "ADD": 
                if len(parameters) == 1:
                    self.tape[self.headPos] += self.readValue(parameters[0])
                else:
                    self.tape[self.variables[parameters[0]]] += self.readValue(parameters[1])

            # Subtracts value from head position (SUB <value>) or variable (SUB <var> <value>)
            case "SUB": 
                if len(parameters) == 1:
                    self.tape[self.headPos] -= self.readValue(parameters[0])
                else:
                    self.tape[self.variables[parameters[0]]] -= self.readValue(parameters[1])

            # Multiplies head position by value (MUL <value>)
            case "MUL": 
                if len(parameters) == 1:
                    self.tape[self.headPos] *= self.readValue(parameters[0])
                else:
                    self.tape[self.variables[parameters[0]]] *= self.readValue(parameters[1])

            # Devides head position by value (MUL <value>)
            case "DIV": 
                if len(parameters) == 1:
                    self.tape[self.headPos] //= self.readValue(parameters[0])
                else:
                    self.tape[self.variables[parameters[0]]] //= self.readValue(parameters[1])

            # Modulo head position by value (MOD <value>)
            case "MOD":
                self.tape[self.headPos] %= self.readValue(parameters[0])

            # Sets head position to value (SET <value>) or variable (SET <var> <value>)
            case "SET":
                if len(parameters) == 1:
                    self.tape[self.headPos] = self.readValue(parameters[0])
                else:
                    self.setVar(parameters[0], self.readValue(parameters[1]))

            # Move head to absolute position or relative to section start
            case "MOVE":
                self.headPos = self.readValue(parameters[0])
                self.checkArrSize(self.headPos)

            case "GOTO":
                self.headPos = self.variables[parameters[0]]
                self.checkArrSize(self.headPos)

            case "MOVE_LEFT":
                if len(parameters) == 0:
                    self.headPos -= 1
                    self.checkArrSize(self.headPos)
                else:
                    self.headPos -= self.readValue(parameters[0])
            
            case "MOVE_RIGHT":
                if len(parameters) == 0:
                    self.headPos += 1
                    self.checkArrSize(self.headPos)
                else:
                    self.headPos += self.readValue(parameters[0])
            
            # Conditional statements (IF <value1> <compare type> <value2> <instruction>)
            case "IF":
                value1 = self.readValue(parameters[0])
                value2 = self.readValue(parameters[2])
                boolean = parameters[1]

                match boolean:
                    case "==":
                        if value1 == value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)
                    
                    case "!=":
                        if value1 != value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)
                    
                    case "<=":
                        if value1 <= value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)
                    
                    case ">=":
                        if value1 >= value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)
                    
                    case "<":
                        if value1 < value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)
                    
                    case ">":
                        if value1 > value2:
                            instruction = " ".join(parameters[3:])
                            self.read_instruction(instruction)

            case "STATE": 
                self.state = parameters[0]
                self.currInstruction = -1  # Will be incremented to 0 after this function

                # print(self.tape[self.variables["ARRAY"]:self.variables["ARRAY_END"]+1])
                # print(self.tape[self.variables["PREDIGIT"]])
                # print(self.tape[self.variables["NINES"]])
                # print(self.tape[self.variables["OUTPUT"]:self.variables["WORK"]])
                print(self.tape) # <------------------------------------------------------------ PRINT TAPE



    def executeInstructions(self):
        i = 0
        while(self.state != "ACCEPT" and i <= self.INSTRUCTION_LIMIT ):
            
            self.read_instruction(self.getInstruction())
            self.updateDisplay() # HARVIE
            self.currInstruction += 1

            i += 1
        
        output = str(self.tape[self.variables["OUTPUT"]+1]) + '.'
        for char in self.tape[self.variables["OUTPUT"]+2:self.variables["WORK"]]:
            output += str(char)

        return output

    def getVar(self, varName):
        return self.tape[self.variables[varName]]
    
    def setVar(self, varName, value):
        self.checkArrSize(self.variables[varName])
        self.tape[self.variables[varName]] = value

    def checkArrSize(self, position): # make sure the array is big enough for location
        arrSize = len(self.tape)
        if position >= arrSize:
            self.tape.extend([0]*(position - arrSize + 1))

    def getInstruction(self):
        # if self.currInstruction >= len(self.instructions[self.state]):
        #     self.currInstruction = 0
        return self.instructions[self.state][self.currInstruction]
        

    def readValue(self, value) -> int:
        if value.isnumeric():
            return int(value)
        
        elif value in self.variables.keys():
            return self.getVar(value)
        elif value == "HEAD":
            return self.head

        
    def updateDisplay(self): # HARVIE
        self.tape
        self.headPos


