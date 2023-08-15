# https://www.codewars.com/kata/52dc4688eca89d0f820004c6/train/python

# to help with debugging
def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

def parse_num(q):
    sign = {" ": 1, "\t": -1}[q[0]]
    bits = {" ": 0, "\t": 1}
    n = 0
    for i, char in enumerate(q[1:-1]):
        n += bits[char] * 2**(len(q[1:-1]) - i - 1)
    n *= sign
    return n

def parse_label(q):
    return q

class Parser:

    def __init__(self):
        self.inp = []
        self.output = []
        self.stack = []
        self.heap = {}
        self.gotos = {}
        self.mode = "imp"
        self.i = 0
        self.i_save = None
        self.q = ""
        self.exit_flag = False
        self.imp_list = []

    def clear_q(self):
        self.q = ""

    def goto(self, i, save=None):
        if save:
            self.i_save = save
        self.i = i

    def goback(self):
        if self.i_save:
            self.i = self.i_save
        else:
            raise Exception("Return outside of subroutine call")

    def trigger_exit(self):
        self.exit_flag = True

    def verify(self, n):
        if 0 <= n < len(self.stack):
            return n
        else:
            raise Exception("Stack index out of bounds")
        
    def parse_imp(self):
        imps = {
            # Stack Manipulation
            "  ":       lambda n: self.stack.append(n),                                 # Push n onto the stack.
            " \t ":     lambda n: self.stack.append(self.stack[-self.verify(n)-1]),                      # Duplicate the nth value from the top of the stack and push onto the stack.
            " \t\n":    lambda n: [self.stack.pop(-2) for _ in range(min(abs(n), len(self.stack)-1))],                 # Discard the top n values below the top of the stack from the stack.
            " \n ":     lambda: self.stack.append(self.stack[-1]),                           # Duplicate the top value on the stack.
            " \n\t":    lambda: (self.stack.append(self.stack[-2]), self.stack.pop(-3)),     # Swap the top two value on the stack.
            " \n\n":    lambda: self.stack.pop(),                                       # Discard the top value on the stack.
            # Arithmetic
            "\t   ":    lambda: self.stack.append(self.stack.pop(-2) + self.stack.pop()), # Pop a and b, then push b+a.
            "\t  \t":   lambda: self.stack.append(self.stack.pop(-2) - self.stack.pop()),    # Pop a and b, then push b-a.
            "\t  \n":   lambda: self.stack.append(self.stack.pop(-2) * self.stack.pop()),    # Pop a and b, then push b*a.
            "\t \t ":   lambda: self.stack.append(self.stack.pop(-2) // self.stack.pop()),    # Pop a and b, then push b/a*. If a is zero, throw an error.
            "\t \t\t":  lambda: self.stack.append(self.stack.pop(-2) % self.stack.pop()),    # Pop a and b, then push b%a*. If a is zero, throw an error.
            # Heap Access
            "\t\t ":    lambda: self.heap.update({self.stack.pop(-2): self.stack.pop()}),    # Pop a and b, then store a at heap address b.
            "\t\t\t":   lambda: self.stack.append(self.heap[self.stack.pop()]),            # Pop a and then push the value at heap address a onto the stack.
            # Input/Output
            "\t\n  ":   lambda: self.output.append(chr(self.stack.pop())),                   # Pop a value off the stack and output it as a character.
            "\t\n \t":  lambda: self.output.append(str(self.stack.pop())),   # Pop a value off the stack and output it as a number.
            "\t\n\t ":  lambda: self.heap.update({self.stack.pop(): ord(self.inp.pop(0))}),            # Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
            "\t\n\t\t": lambda: self.heap.update({self.stack.pop(): self.inp.pop(0)}), # Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.
            # Flow Control
            # "\n  ":     "LABEL", # lambda l: self.gotos.update({l: self.i}),              # Mark a location in the program with label n.
            "\n \t":    lambda l: self.goto(self.gotos[l], save=self.i),  # Call a subroutine with the location specified by label n.
            "\n \n":    lambda l: self.goto(self.gotos[l]), # Jump unconditionally to the position specified by label n.
            "\n\t ":    lambda l: None if self.stack.pop() != 0 else self.goto(self.gotos[l]), # Pop a value off the stack and jump to the label specified by n if the value is zero.
            "\n\t\t":   lambda l: None if self.stack.pop() >= 0 else self.goto(self.gotos[l]),   # Pop a value off the stack and jump to the label specified by n if the value is less than zero.
            "\n\t\n":   self.goback, # Exit a subroutine and return control to the location from which the subroutine was called.
            "\n\n\n":   self.trigger_exit                                               # Exit the program.
        }
        if self.q in imps:
            return imps[self.q]
        
    def compile(self, code):
        for char in code:
            if char not in {" ", "\t", "\n"}:
                continue
            self.q += char
            if self.mode == "imp":
                imp = self.parse_imp()
                if self.q == "\n  ":
                    self.mode = "label"
                    self.clear_q()
                    continue
                elif not imp:
                    continue
                print(unbleach(self.q))
                self.clear_q()
                if "n" in imp.__code__.co_varnames:
                    self.mode = "n"
                elif "l" in imp.__code__.co_varnames:
                    self.mode = "l"
                else:
                    self.imp_list.append((imp, None))
                    imp = None
            elif self.mode == "n" and char == "\n":
                n = parse_num(self.q)
                print(n)
                self.imp_list.append((imp, n))
                self.mode = "imp"
                self.clear_q()
                imp = None
            elif self.mode == "l" and char == "\n":
                l = self.q
                print(unbleach(l))
                self.imp_list.append((imp, l))
                self.mode = "imp"
                self.clear_q()
                imp = None
            elif self.mode =="label" and char == "\n":
                l = self.q
                print(unbleach(l))
                if l in self.gotos:
                    raise Exception("Labels must be unique")
                self.gotos[l] = len(self.imp_list) - 1
                print(self.gotos)
                self.mode = "imp"
                self.clear_q()
                imp = None
    
    def execute(self, inp):
        self.inp = [c for line in inp.split("\n") for c in line]
        while not self.exit_flag:
            print(self.i, end=" ")
            imp, n = self.imp_list[self.i]
            if n is not None:
                imp(n)
            else:
                imp()
            print(self.i_save, self.stack)
            self.i += 1
        print("".join(self.output))
        return "".join(self.output)
        raise Exception("Unclean termination")

def whitespace(code, inp=""):
    print(unbleach(code))
    print(inp)
    parser = Parser()
    parser.compile(code)
    return parser.execute(inp)