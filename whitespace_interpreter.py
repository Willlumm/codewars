# https://www.codewars.com/kata/52dc4688eca89d0f820004c6/train/python

class Parser:

    def __init__(self):
        self.imps =  {
            # Stack Manipulation
            "  ":       lambda n: self.stack.append(self.parse_num(n)),                                                 # Push n onto the stack.
            " \t ":     lambda n: self.stack.append(self.stack[-self.verify(self.parse_num(n))-1]),                     # Duplicate the nth value from the top of the stack and push onto the stack.
            " \t\n":    lambda n: [self.stack.pop(-2) for _ in range(min(abs(self.parse_num(n)), len(self.stack)-1))],  # Discard the top n values below the top of the stack from the stack.
            " \n ":     lambda: self.stack.append(self.stack[-1]),                                                      # Duplicate the top value on the stack.
            " \n\t":    lambda: (self.stack.append(self.stack[-2]), self.stack.pop(-3)),                                # Swap the top two value on the stack.
            " \n\n":    lambda: self.stack.pop(),                                                                       # Discard the top value on the stack.
            # Arithmetic
            "\t   ":    lambda: self.stack.append(self.stack.pop(-2) + self.stack.pop()),                               # Pop a and b, then push b+a.
            "\t  \t":   lambda: self.stack.append(self.stack.pop(-2) - self.stack.pop()),                               # Pop a and b, then push b-a.
            "\t  \n":   lambda: self.stack.append(self.stack.pop(-2) * self.stack.pop()),                               # Pop a and b, then push b*a.
            "\t \t ":   lambda: self.stack.append(self.stack.pop(-2) // self.stack.pop()),                              # Pop a and b, then push b/a*. If a is zero, throw an error.
            "\t \t\t":  lambda: self.stack.append(self.stack.pop(-2) % self.stack.pop()),                               # Pop a and b, then push b%a*. If a is zero, throw an error.
            # Heap Access
            "\t\t ":    lambda: self.heap.update({self.stack.pop(-2): self.stack.pop()}),                               # Pop a and b, then store a at heap address b.
            "\t\t\t":   lambda: self.stack.append(self.heap[self.stack.pop()]),                                         # Pop a and then push the value at heap address a onto the stack.
            # Input/Output
            "\t\n  ":   lambda: self.output.append(chr(self.stack.pop())),                                              # Pop a value off the stack and output it as a character.
            "\t\n \t":  lambda: self.output.append(str(self.stack.pop())),                                              # Pop a value off the stack and output it as a number.
            "\t\n\t ":  lambda: self.heap.update({self.stack.pop(): ord(self.inp.pop(0))}),                             # Read a character from input, a, Pop a value off the stack, b, then store the ASCII value of a at heap address b.
            "\t\n\t\t": lambda: self.heap.update({self.stack.pop(): self.inp.pop(0)}),                                  # Read a number from input, a, Pop a value off the stack, b, then store a at heap address b.
            # Flow Control
            "\n \t":    lambda n: self.goto(self.gotos[n], save=self.i),                                                # Call a subroutine with the location specified by label n.
            "\n \n":    lambda n: self.goto(self.gotos[n]),                                                             # Jump unconditionally to the position specified by label n.
            "\n\t ":    lambda n: self.goto(self.gotos[n]) if self.stack.pop() == 0 else None,                          # Pop a value off the stack and jump to the label specified by n if the value is zero.
            "\n\t\t":   lambda n: self.goto(self.gotos[n]) if self.stack.pop() < 0 else None,                           # Pop a value off the stack and jump to the label specified by n if the value is less than zero.
            "\n\t\n":   self.goback,                                                                                    # Exit a subroutine and return control to the location from which the subroutine was called.
            "\n\n\n":   self.exit                                                                                       # Exit the program.
        }
        self.inp        = []
        self.output     = []
        self.stack      = []
        self.heap       = {}
        self.i          = 0
        self.i_save     = None
        self.program    = []
        self.gotos      = {}
        self.exit_flag  = False

    def parse_num(self, q):
        n = 0
        for i, char in enumerate(q[1:-1]):
            n += {" ": 0, "\t": 1}[char] * 2**(len(q[1:-1]) - i - 1)
        return n * {" ": 1, "\t": -1}[q[0]]
    
    def verify(self, n):
        if 0 <= n < len(self.stack):
            return n
        raise Exception("Stack index out of bounds")

    def goto(self, i, save=None):
        if save:
            self.i_save = save
        self.i = i

    def goback(self):
        if self.i_save:
            self.i = self.i_save
        else:
            raise Exception("Return outside of subroutine call")

    def exit(self):
        self.exit_flag = True
        
    def compile(self, code):
        mode = "imp"
        q = ""
        for char in code:
            if char not in {" ", "\t", "\n"}:
                continue
            q += char
            if mode == "imp" and q in self.imps:
                imp = self.imps[q]
                q = ""
                if "n" in imp.__code__.co_varnames:
                    mode = "n"
                else:
                    self.program.append((imp, None))
            elif mode == "imp" and q == "\n  ":
                mode = "label"
                q = ""
            elif mode == "n" and char == "\n":
                self.program.append((imp, q))
                mode = "imp"
                q = ""
            elif mode =="label" and char == "\n":
                l = q
                if l in self.gotos:
                    raise Exception("Labels must be unique")
                self.gotos[l] = len(self.program) - 1
                mode = "imp"
                q = ""
    
    def execute(self, inp):
        self.inp = [c for line in inp.split("\n") for c in line]
        while not self.exit_flag:
            imp, n = self.program[self.i]
            if n is not None:
                imp(n)
            else:
                imp()
            self.i += 1
        return "".join(self.output)

def whitespace(code, inp=""):
    parser = Parser()
    parser.compile(code)
    return parser.execute(inp)