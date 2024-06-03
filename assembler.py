import re #The import re statement is necessary because it imports the Python module re, which provides support for working with regular expressions.
            #Regular expressions (regex) are patterns used to match character combinations in strings.
destination = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

computation = {
    '0': '0101010', '1': '0111111', '-1':'0111010', 'D':'0001100', 'A': '0110000', '!D': '0001101',
    '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D':'0000111',
    'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011',
    'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101'
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


predefined = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KEYBOARD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
}



def remove_whitespaces(line):
    line = re.sub(r"//.*", "", line)
    line = line.strip() #The strip() method removes any whitespace characters, such as spaces, tabs, and newline characters, from the beginning and end of the string
    return line if line else None




def c_instruction(line, assembler2):
    parts = line.split('=')
    dest_part = parts[0].strip() if len(parts) == 2 else 'null'
    comp_part, jump_part = parts[-1].split(';') if ';' in parts[-1] else (parts[-1].strip(), 'null')#if it has comp;jmp (;) in line, it will split there and assigns the value                                                                                                   #to comp and jump part
    if comp_part in computation and dest_part in destination and jump_part in jump:
        comp = computation[comp_part]
        dest = destination[dest_part]
        jmp = jump[jump_part]
    assembler2.write(f"111{comp}{dest}{jmp}\n")#f is used as formated text inwhich the value inside the braces will get calculated or added up



def a_instruction(line, assembler2, symbol_table):
    value = line[1:].strip() #remove @ symbol
    if value.isdigit():
        binary_value = format(int(value), '016b')
    elif value in predefined:
        binary_value = format(predefined[value], '016b')
    elif value in symbol_table:
        binary_value = format(symbol_table[value], '016b')
    else:
        symbol_table[value] = len(symbol_table)-10
        binary_value = format(symbol_table[value], '016b')
    assembler2.write(f"{binary_value}\n")



def translate_asm_to_hack(assembler1, assembler2):
    symbol_table = predefined.copy()
    with open(assembler1, 'r') as input_file, open(assembler2, 'w') as output_file:
        # First pass: handling labels
        line_number = 0
        for line in input_file:
            line = remove_whitespaces(line)
            if line is None:
                continue
            if line.startswith('('):
                label = line[1:-1]
                symbol_table[label] = line_number
            else:
                line_number += 1

        # Second pass: translating instructions
        input_file.seek(0)
        for line in input_file:
            line = remove_whitespaces(line)
            if line is None or line.startswith('('):
                continue
            if line.startswith('@'):
                a_instruction(line, output_file, symbol_table)
            else:
                c_instruction(line, output_file)



translate_asm_to_hack("assembler1.asm", "assembler2.hack")