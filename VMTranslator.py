import sys
import random

def parser(inst):
    items = (inst.strip()).split(" ")
    command = items[0]
    if len(items) == 1:
        return ('C_ARITHMETIC', (command, None))
    elif len(items) == 3:
        if command == "push":
            return ('C_PUSH', (command, (items[1], items[2])))
        else:
            return ('C_POP', (command, (items[1], items[2])))

def generateArithmetic(command):
    counterJmp = str(random.randint(0, 10000))
    retStr = ''  # Initialize retStr here
    if command == "add":
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M'
    elif command == "sub":
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D-M'
    elif command == 'neg':
        retStr = '@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1'
    elif command == 'and':
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M'
    elif command == 'or':
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M'
    elif command == 'not':
        retStr = '@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1'
    elif command == 'eq':
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMPTRUE'+counterJmp+'\nD;JEQ\n@SP\nA=M-1\nM=0\n@ENDJUMP'+counterJmp+'\n0;JMP\n(JUMPTRUE'+counterJmp+')\n@SP\nA=M-1\nM=-1\n(ENDJUMP'+counterJmp+')'
    elif command == 'gt':
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMPTRUE'+counterJmp+'\nD;JGT\n@SP\nA=M-1\nM=0\n@ENDJUMP'+counterJmp+'\n0;JMP\n(JUMPTRUE'+counterJmp+')\n@SP\nA=M-1\nM=-1\n(ENDJUMP'+counterJmp+')'
    elif command == 'lt':
        retStr = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@JUMPTRUE'+counterJmp+'\nD;JLT\n@SP\nA=M-1\nM=0\n@ENDJUMP'+counterJmp+'\n0;JMP\n(JUMPTRUE'+counterJmp+')\n@SP\nA=M-1\nM=-1\n(ENDJUMP'+counterJmp+')'
    return retStr


def generateMemoryAccess(command, segment, index):
    if command == "push":
        if segment == "constant":
            retStr = '@' + str(index) + '\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'local':
            retStr = '@LCL\nD=M\n@' + str(index) + '\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'argument':
            retStr = '@ARG\nD=M\n@' + str(index) + '\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'this':
            retStr = '@THIS\nD=M\n@' + str(index) + '\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'that':
            retStr = '@THAT\nD=M\n@' + str(index) + '\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'pointer':
            retStr = '@R3\nD=A\n@' + str(index) + '\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'temp':
            retStr = '@R5\nD=A\n@' + str(index) + '\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        elif segment == 'static':
            retStr = '@' + str((sys.argv[1].split('.'))[0]) + '.' + str(index) + '\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
    elif command == "pop":
        if segment == "local":
            retStr = '@SP\nM=M-1\n@LCL\nD=M\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'argument':
            retStr = '@SP\nM=M-1\n@ARG\nD=M\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'this':
            retStr = '@SP\nM=M-1\n@THIS\nD=M\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'that':
            retStr = '@SP\nM=M-1\n@THAT\nD=M\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'pointer':
            retStr = '@SP\nM=M-1\n@R3\nD=A\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif segment == 'temp':
            retStr = '@SP\nM=M-1\n@R5\nD=A\n@' + str(index) + '\nD=D+A\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
    return retStr

def removeComments(lineList):
    newList = []
    for line in lineList:
        if (line.strip()).startswith("//"):
            continue
        elif "//" in line:
            newList.append(line.split("//")[0].strip())
        else:
            newList.append(line.strip())
    return newList

def code(instruction_type, instruction_arguments):
    command, args = instruction_arguments
    if instruction_type == 'C_ARITHMETIC':
        return generateArithmetic(command)
    elif instruction_type in ['C_PUSH', 'C_POP']:
        return generateMemoryAccess(command, args[0], args[1])

def main():
    file_path = input("Enter the path of the file: ")
    
    # Open the input .vm file
    with open(file_path, 'r') as fdIn:
        # Create the output .asm file
        output_file_path = file_path.replace('.vm', '.asm')
        with open(output_file_path, 'w') as fdOut:
            # Read lines from the input file
            inFileRead = fdIn.readlines()
            # Remove comments from the input file
            inFileRead = removeComments(inFileRead)
            # Process each instruction
            for instruction in inFileRead:
                # Parse the instruction
                instruction_type, instruction_arguments = parser(instruction)
                # Generate assembly code for the instruction
                assembly_code = code(instruction_type, instruction_arguments)
                # Write the assembly code to the output file
                fdOut.write(assembly_code + '\n')

if __name__ == "__main__":
    main()


