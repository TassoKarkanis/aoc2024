from .utils import *

Data1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

Data2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


FullData = """Register A: 52884621
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,4,7,0,3,1,5,5,5,3,0"""

# Decoded instructions:
#
# bst A  // B = A % 8
# bxl 3  // B = B ^ 3
# cdv B  // C = A / (2**B) 
# bxc    // B = B ^ C
# adv 3  // A = A / 8
# bxl B  // B = B ^ 5
# out B
# jnz
#
# Observations:
# 
# 1) The flow control is just one loop that ends when A is zero.
# 2) The low 3 bits of A are removed in every iteration.
# 3) B and C are reset in every iteration.

# register names
A = 0
B = 1
C = 2

# instruction names
InstructionNames = [
    "adv",
    "bxl",
    "bst",
    "jnz",
    "bxc",
    "out",
    "bdv",
    "cdv",
]

class Machine:
    def __init__(self, data):
        # initialize members
        self.reg = [0,0,0]       # register values
        self.IP = 0              # instruction point
        self.program = []        # program as a list of numbers
        self.output = []         # program output as a list of numbers

        # parse the register values
        lines = data.splitlines()
        prefix = "Register A: "
        self.reg[0] = int(lines[0][len(prefix):])
        self.reg[1] = int(lines[1][len(prefix):])
        self.reg[2] = int(lines[2][len(prefix):])

        # parse the program
        prefix = "Program: "
        program = lines[4][len(prefix):]
        program = program.split(",")
        self.program = list(map(int, program))

    def run(self, quiet=True):
        Instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        if not quiet:
            self.print()
            
        while self.IP < len(self.program):
            # get the opcode and argument
            opcode = self.program[self.IP]
            arg = self.program[self.IP+1]

            # execute the instructions
            Instructions[opcode](arg)

            if not quiet:
                self.print()

        output = map(str, self.output)
        return ",".join(output)

    def reset(self):
        self.reg = [0, 0, 0]
        self.IP = 0
        self.output = []

    def print(self):
        print("state:")
        print(f"  A:   {self.reg[A]}")
        print(f"  B:   {self.reg[B]}")
        print(f"  C:   {self.reg[C]}")
        print(f"  IP:  {self.IP}")
        print(f"  out: {self.output}")

        msg = "  end"
        if self.IP < len(self.program):
            opcode = self.program[self.IP]
            operand = self.program[self.IP+1]
            inst = InstructionNames[opcode]
                
            msg = f"{inst} opcode({opcode}) operand({operand})"
        print(f"  next: {msg}")
    
    def adv(self, arg):
        self.reg[A] = self.reg[A] // 2**self.combo_value(arg)
        self.IP += 2

    def bxl(self, arg):
        self.reg[B] ^= arg
        self.IP += 2

    def bst(self, arg):
        self.reg[B] = self.combo_value(arg) % 8
        self.IP += 2

    def jnz(self, arg):
        if self.reg[A] == 0:
            self.IP += 2
        else:
            self.IP = arg

    def bxc(self, arg):
        self.reg[B] ^= self.reg[C]
        self.IP += 2

    def out(self, arg):
        self.output.append(self.combo_value(arg) % 8)
        self.IP += 2

    def bdv(self, arg):
        self.reg[B] = self.reg[A] // 2**self.combo_value(arg)
        self.IP += 2

    def cdv(self, arg):
        self.reg[C] = self.reg[A] // 2**self.combo_value(arg)
        self.IP += 2
        
    def combo_value(self, arg):
        if arg < 4:
            return arg
        else:
            return self.reg[arg - 4]
    
def p17_part1():
    # run the tests
    m = Machine(Data1)
    output = m.run()
    assert output == "4,6,3,5,6,3,5,2,1,0"

    # run the tests
    m = Machine(FullData)
    output = m.run()
    # print(f"output: {output}")
    return output

def p17_part2():
    # run the tests
    m = Machine(Data2)
    m.reg[A] = 117440
    m.run()
    assert m.output == m.program

    # Compute the solution.  I have some reasoning based on the
    # sequence of instructions in the program and their arguments that
    # it is essentially selecting an octal digit of A and printing it
    # out in every iteration.  Multiple combinations of digits work.
    # I'm not 100% sure why the code below generates all possible
    # values of A.
    m = Machine(FullData)
    n = [0]
    for k in range(len(m.program)):
        target = ",".join(map(str,m.program[-k - 1:]))
        n2 = []
        for i in range(8):
            for j in n:
                m.reset()
                a = i + 8*j
                m.reg[A] = a
                if m.run() == target:
                    n2.append(a)
                    
        assert len(n2) > 0
        n = n2

    n = sorted(n)
    return n[0]
    
__all__ = ["p17_part1", "p17_part2"]
