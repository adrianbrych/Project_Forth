from asyncio.windows_events import NULL
from pythonds.basic import Stack
import sys
import math

#####################################
#
# FORTH PROJCET
#
#####################################

# Global variables of execption and compile mode

ExeptionError = 'InterpreterError'
NonError = "NonError"
Exec = 'Execution'
Def = 'Definition'
Forget = 'Forgetting'
Com = 'Comment'
Var = 'Variable'

# Class of Forth interprtere


class Interpreter:
    def __init__(self):
        # Create stack, lists and dictes of instance
        self.stack = Stack()
        self.rstack = Stack()

        self.operations = dict()
        self.vars = dict()
        self.ctl_struct = dict()
        self.user_list = list()
        self.variables_list = list()

        self.mode = Exec
        self.lastmode = Exec
        self.run_level = 0

        # init variables
        self.operations["."] = self.dot
        self.operations["+"] = self.plus
        self.operations["cr"] = self.cr
        self.operations["+"] = self.plus
        self.operations["-"] = self.minus
        self.operations["*"] = self.multiply
        self.operations["/"] = self.devide
        self.operations["umin"] = self.umin
        self.operations["^"] = self.exp
        self.operations["variable"] = self.variable
        self.operations["!"] = self.assing
        self.operations["@"] = self.dereference
        self.operations["dup"] = self.duplicate
        self.operations["swap"] = self.swap
        self.operations["bye"] = self.bye
        self.operations["forget"] = self.forget
        self.operations[":"] = self.col
        self.operations[";"] = self.semcol
        self.operations["("] = self.lparen
        self.operations[")"] = self.rparen
        self.operations["vlist"] = self.vlist
        self.operations["if"] = self.c_if
        self.operations["else"] = self.c_else
        self.operations["then"] = self.c_then
        self.operations["do"] = self.c_do
        self.operations["loop"] = self.c_loop
        self.operations["+loop"] = self.c_plus_loop

        self.ctl_struct["do"] = self.c_cc_do
        self.ctl_struct["loop"] = self.c_cc_loop
        self.ctl_struct["+loop"] = self.c_cc_plus_loop
        self.ctl_struct["if"] = self.c_cc_if
        self.ctl_struct["else"] = self.c_cc_else
        self.ctl_struct["then"] = self.c_cc_then

    # Function with basics operation of language
    def dot(self):
        result = self.stack.pop()
        sys.stdout.write(str(result) + " ")

    def cr(self):
        print()

    def plus(self):
        x = float(self.stack.pop())
        y = float(self.stack.pop())
        self.stack.push(x + y)

    def minus(self):
        y = float(self.stack.pop())
        x = float(self.stack.pop())
        self.stack.push(y - x)

    def multiply(self):
        y = float(self.stack.pop())
        x = float(self.stack.pop())
        self.stack.push(y * x)

    def devide(self):
        y = float(self.stack.pop())
        x = float(self.stack.pop())
        self.stack.push(y/x)

    def exp(self):
        y = float(self.stack.pop())
        x = float(self.stack.pop())
        self.stack.push(math.pow(x, y))

    def umin(self):
        x = float(self.stack.pop())
        self.stack.push(-x)

    def assing(self):
        word = self.stack.pop()
        value = self.stack.pop()
        if self.vars in word:
            self.vars[word] = value

    def dereference(self):
        word = self.stack.pop()
        try:
            self.stack.push(self.vars[word])
        except KeyError:
            raise ExeptionError

    def duplicate(self):
        value = self.stack.pop()
        self.stack.push(value)
        self.stack.push(value)

    def swap(self):
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.push(x)
        self.stack.push(y)

    def f_def(self):
        word = self.stack.pop()
        pr = self.stack.pop()
        self.operations[word] = pr
        self.user_list.append(word)

    def col(self):
        if self.mode == Exec:
            self.mode = Def
            self.colon = []
        else:
            raise ExeptionError

    def semcol(self):
        if self.mode == Def:
            pr = self.colon[1:]
            self.stack.push(pr)
            self.stack.push(self.colon[0])
            del self.colon
            self.f_def()
            self.mode = Exec
        else:
            raise ExeptionError

    def forget(self):
        self.mode = Forget

    def bye(self):
        raise NonError

    def compile(self, text):
        return text.split()

    def lparen(self):
        if self.mode != Com:
            self.lastmode = self.mode
            self.mode = Com

    def rparen(self):
        if self.mode == Com:
            self.mode = self.lastmode
        else:
            raise ExeptionError

    def do_forget(self, word):
        if self.operations in word or self.vars in word:
            ind = self.user_list.index(word)
            length = len(self.user_list)

            for k in range(ind, length):
                if self.operations in self.user_list[k]:
                    del self.operations[self.user_listp[k]]
                elif self.vars in self.user_list[k]:
                    del self.vars[self.user_list[k]]
                else:
                    raise ExeptionError
                del self.user_list[ind]
        else:
            raise ExeptionError
        self.mode = Exec

    def variable(self):
        self.last_mode = self.mode
        self.mode = Var

    def do_variable(self, name):
        self.vars[name] = self.stack.pop()
        self.user_list.append(name)
        self.mode = self.last_mode

    def vlist(self):
        olist = self.operations.keys()
        olist.sort()
        for k in olist:
            sys.stdout.write(k + " ")

    def c_if(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_else(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_then(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_do(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_cc_do(self, scan):
        self.rstack.push(scan[0:])
        scan = list()
        scan.append("do")
        return scan

    def c_cc_if(self, scan):
        self.rstack.push(scan[0:])
        scan = list()
        scan.append("if")
        return scan

    def c_loop(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_cc_loop(self, scan):
        scan.append("loop")
        result = self.rstack.pop()
        result.append(scan)
        return result

    def c_cc_plus_loop(self, scan):
        scan.append("+loop")
        result = self.rstack.pop()
        result.append(scan)
        return result

    def c_cc_else(self, scan):
        scan.append("else")
        result = self.rstack.pop()
        result.append(scan)
        return result

    def c_cc_then(self, scan):
        scan.append("then")
        result = self.rstack.pop()
        result.append(scan)
        return result

    def c_plus_loop(self):
        if self.run_level == 0:
            raise ExeptionError

    def c_prepass(self, pr):
        self.rstack.flush()
        scan = list()

        for w in pr:
            if self.ctl_struct in w:
                scan = self.ctl_struct[w](scan)
            else:
                scan.append(w)
        return scan
# Interpreter function

    def interpretation(self, instuction):
        for word in instuction:
            if self.mode == Com:
                if word == ")":
                    self.rparen()
                continue
            elif self.mode == Def:
                if word == ";":
                    self.semcol()
                else:
                    self.colon.append(word)
                continue
            elif self.mode == Var:
                self.do_variable(word)
                continue
            elif self.mode == Forget:
                self.do_forget(word)
                continue
            if word != NULL and word not in list(self.operations.keys()):
                self.stack.push(word)
                continue
            else:
                current_word = word
                try:
                    while(self.operations in self.operations[current_word]):
                        current_word = self.operations[current_word]
                except TypeError:
                    pass

                if type(current_word) == type([]):
                    self.run_level = self.run_level + 1
                    self.interpretation(current_word)
                    self.run_level = self.run_level + 1
                elif type(self.operations[current_word]) == type([]):
                    self.run_level = self.run_level + 1
                    self.interpretation(self.operations[current_word])
                    self.run_level = self.run_level - 1
                elif type(self.operations[current_word]) == type(self.f_def):
                    self.operations[current_word]()
                else:
                    self.stack.push(self.operations[current_word])


class ForthPy:
    def __init__(self, input=sys.stdin):
        self.input = input
        self.interpreter = Interpreter()

    def go(self):
        try:
            while(1):
                input = self.input.readline()
                code = self.interpreter.compile(input)
                self.interpreter.interp(code)
                if self.input.isatty() and self.interpreter.mode == Exec:
                    print("GOOD")
                else:
                    break
        except TypeError:
            print("ERROR")

# Tests of interpreter


def test_math():
    s = "2 3 + . 3 4 ^ ."
    forth_interpreter = Interpreter()
    t = forth_interpreter.compile(s)
    print(t)
    forth_interpreter.interpretation(t)


def test_variable():
    forth_interpreter = Interpreter()
    s = '19 variable a 3 a @ * . cr'
    t = forth_interpreter.compile(s)
    print(s, '->', t)
    forth_interpreter.interpretation(t)


def test_dup():
    forth_interpreter = Interpreter()
    s = '20 dup  . cr . cr'
    t = forth_interpreter.compile(s)
    print(s, '->', t)
    forth_interpreter.interpretation(t)


def test_swap():
    s = '5 10 swap . cr . cr'
    forth_interpreter = Interpreter()
    t = forth_interpreter.compile(s)
    print(s, '->', t)
    forth_interpreter.interpretation(t)


def test_forget_and_colon():
    s = ': sq dup * ; 2 sq 3 sq 100 sq . cr . cr . cr'
    forth_interpreter = Interpreter()
    t = forth_interpreter.compile(s)
    print(s, '->', t)
    forth_interpreter.interpretation(t)


def test_adding_new_word():
    forth_interpreter = Interpreter()
    s = '2 3 + . 3 4 ^ .'
    t = forth_interpreter.compile(s)
    print(s, '->', t)
    forth_interpreter.interpretation(t)

    forth_interpreter.stack.push(t)
    forth_interpreter.stack.push('junk')
    forth_interpreter.f_def()
    forth_interpreter.interpretation(['junk'])


if __name__ == "__main__":
    test_adding_new_word()
    test_forget_and_colon()
    test_swap()
    test_dup()
    test_variable()
    test_math()
