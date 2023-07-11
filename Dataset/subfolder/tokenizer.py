import tokenize
import subprocess

"""subprocess.run(["black", "hello.py"])

tokens_list = []
with tokenize.open("hello.py") as f:
    tokens = tokenize.generate_tokens(f.readline)
    for token in tokens:
        if token.string == "\n":
            tokens_list.append("NEWLINE")
        elif token.string == "    ":
            tokens_list.append("INDENT")
        else:
            tokens_list.append(token.string)

tokens_list = tokens_list[0:-2]
for token in tokens_list:
    print(token)

with open("tokens.txt", "w") as f:
    for token in tokens_list:
        f.write(token + " ")
        
token_list = list(open("tokens.txt", "r").read().split(" "))
print(token_list)

with open("token_Refactor.py", "w") as f:
    for token in token_list:
        if token == "NEWLINE":
            f.write("\n")
        elif token == "INDENT":
            f.write("    ")
        elif token == '':
            continue
        else:
            f.write(token + " ")
            
subprocess.run(["black", "token_Refactor.py"])"""

"""with open('hello.py', 'rb') as f:
    tokens = tokenize.tokenize(f.readline)
    for token in tokens:
        print(token)"""
        

from textwrap import dedent, indent

def test():
    # end first line with \ to avoid the empty line!
    s = '''\
    def write_to_file(file, diff_list):
    file.write("-------------------------------\n")
    for i in range(diff_list.__len__()):
        file.write(str(diff_list[i]) + "\n")
    file.write("-------------------------------")
    '''
    print(repr(s))          # prints '    hello\n      world\n    '
    print(repr(dedent(s)))  # prints 'hello\n  world\n'

    return repr(dedent(s))
x = test()

with open("hello.txt", "w") as f:
    f.write(x)