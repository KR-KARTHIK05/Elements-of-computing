import re

jack_code = """
class Main {
    function void main() {
        var int x;
        let x = 42;
        do Output.printInt(x);
        return;
    }
}
"""



#predefined
keywords = {
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
    'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'
}
symbols = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
}



def tokenize_jack_code(jack_code):
    token_specification = [
        ('KEYWORD', r'\b(?:' + '|'.join(keywords) + r')\b'),
        ('SYMBOL', r'[' + re.escape(''.join(symbols)) + r']'),
        ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),
        
        ('NUMBER', r'\b\d+\b'),
        ('STRING', r'"[^"\n]*"'),
        ('SKIP', r'[ \t\n]+'),
        ('MISMATCH', r'.')
    ]



    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    return re.compile(tok_regex)
tokenizer = tokenize_jack_code(jack_code)
tokens = tokenizer.finditer(jack_code)



#output segment
for match in tokens:
    for kind, value in match.groupdict().items():
        if value is not None:
            if kind == 'KEYWORD':
                print(f'<keyword>{value}</keyword>')
            elif kind == 'SYMBOL':
                symbol_map = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
                value = symbol_map.get(value, value)
                print(f'<symbol>{value}</symbol>')
            elif kind == 'IDENTIFIER':
                print(f'<identifier>{value}</identifier>')
            elif kind == 'NUMBER':
                print(f'<integerConstant>{value}</integerConstant>')
            elif kind == 'STRING':
                print(f'<stringConstant>{value[1:-1]}</stringConstant>')
