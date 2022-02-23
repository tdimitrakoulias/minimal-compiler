
#########################################################################
#                                                                       #
#              Copyright (C) 2020 Thomas Dimitrakoulias                 #
#                                                                       #
#-----------------------------------------------------------------------#
#                                                                       #
#                    This program is free software                      #
#     It was developed for academic purposes as an assignment for       #
#     the 'Compilers' course of the department of Computer Science      #
#            and Engineering of the University of Ioannina              #
#                       <https://www.cs.uoi.gr.>                        #
#    You can redistribute it and/or modify it under the terms of the    #
#      GNU General Public License published by the  Free Software       #
#                           Foundation Inc.                             #
#                                                                       #
#-----------------------------------------------------------------------#
#                                                                       #
#                       GNU GENERAL PUBLIC LICENSE                      #
#               Copyright (C) 2007 Free Software Foundation             #
#                          <https://fsf.org/>                           #
#                                                                       #
#########################################################################

import sys

#################################
#USEFULL VARIABLES AND TABLES   #
#################################

temp_var_label = 1
quad_label = 1
linepointer = 1
token = []
token_buffer = []
quads = []
scopes = []
variables = []
current_block = -1
function_pars = []
current_quad = 0
is_first_par = True
pars = []
main_program_framelength = -1

#####################
#TOKEN TYPES        #
#####################


# EOF
eoftk = -2

# ERROR
errortk = -1

# LEX STATES
state0 = 0
state1 = 1
state2 = 2
state3 = 3
state4 = 4
state5 = 5
state6 = 6
state7 = 7
state8 = 8
state9 = 9

# brackets
left_parenthesistk = 10
right_parenthesistk = 11
left_bracetk = 12
right_bracetk = 13
left_brackettk = 14
right_brackettk = 15

#logical operators
equaltk = 16
less_than_or_equaltk = 17
greater_than_or_equaltk = 18
greatertk = 19
lesstk = 20
not_equaltk = 21

#arithmetic operators
plustk = 22
minustk = 23
multiplytk = 24
dividetk = 25

#punctuation
commatk = 26
semicolontk = 27
colontk = 28

#logical operators
andtk = 29
ortk = 30
nottk = 31

#assignment
assigntk = 32

idtk = 33
constanttk = 34

#reserved words
programtk = 35
iftk = 36
whiletk = 37
forcasetk = 38
nottk = 39
functiontk = 40
inputtk = 41
declaretk = 42
elsetk = 43
doublewhiletk = 44
incasetk = 45
andtk = 46
proceduretk = 47
printtk = 48
looptk = 49
whentk = 50
ortk = 51
calltk = 52
exittk = 53
defaulttk = 54
returntk = 55
intk = 56
inouttk = 57
thentk = 58


############################################################################
# state0" ----------------- new lex unit                                   #
# state1" ----------------- id or key word                                 #
# state2" ----------------- number                                         #
# state3" ----------------- read '*', expecting '*' or '*/'                #
# state4" ----------------- read '/', expecting '/','//','/*'              #
# state5" ----------------- read '<', epitrepetai na diavasw '<','<=','<>' #    
# state6" ----------------- read '>', epitrepetai na diavasw '>', '>='     #
# state7" ----------------- read ':', epitrepetai na diavasw ':',':='      #
# state8" ----------------- read '/*' agnow ta panta mexri na vrw '*/'     #
# idtk" ------------------- read an id                                     #
# constanttk" ------------- read a number                                  #
############################################################################

#################################
# Lexical analysis function     #
#################################

def lex():
    global token_buffer, linepointer, infile

    state = state0
    token_buffer = []

    while True:

        c = infile.read(1)

        if c== '': #end of file
            state = eoftk
            break

        if c == '\n':
            linepointer += 1


        token_buffer.append(c)
        if state == state0:

            if c.isspace():
                del token_buffer[-1]
                continue

            elif c.isalpha():

                state = state1
            elif c.isdigit():
                state = state2
            elif c=='+':

                state = plustk
                break
            elif c=='-':
                state = minustk
                break
            elif c=='*':
                state = state3
            elif c=='/':
                state = state4
            elif c=='<':
                state = state5
            elif c=='>':
                state = state6
            elif c=='=':
                state = equaltk
                break
            elif c==',':
                state = commatk
                break
            elif c==':':
                state = state7

            elif c == ';':
                state = semicolontk
                break
            elif c=='(':
                state = left_parenthesistk
                break
            elif c==')':
                state = right_parenthesistk

                break
            elif c=='[':
                state = left_brackettk
                break
            elif c==']':
                state = right_brackettk
                break
            elif c=='{':
                state = left_bracetk
                break
            elif c=='}':
                state = right_bracetk
                break
            else:
                print("error - invalid character at line ", linepointer)
                print("character - ", c)
                break

        elif state == state1:
            if c == '_':
                continue

            if not c.isalnum():

                state = idtk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state2:

            if not c.isdigit():

                state = constanttk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state3:

            if c == '/':
                print("comment closing without opening")
                state = errortk
                break
            else:

                state = multiplytk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state4:

            if c == '*':
                state = state8
            elif c == '/':
                del token_buffer[-2:]
                while True:
                    c = infile.read(1)
                    if c == '\n':
                        linepointer += 1
                        state = state0
                        break

            else:
                state = dividetk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state5:

            if c == '=':
                state = less_than_or_equaltk
                break
            elif c == '>':
                state = not_equaltk
                break
            else:
                state = lesstk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state6:

            if c == '=':
                state = greater_than_or_equaltk
                break
            else:
                state = greatertk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state7:

            if c == '=':
                state = assigntk
                break
            else:
                state = colontk
                del token_buffer[-1]
                if c == '\n':
                    linepointer -= 1
                infile.seek(infile.tell() - 1)
                break

        elif state == state8:

            if c == '*':
                state = state9
            if c == '':

                state = errortk
                print("error, end of file before end of comment")
                break

        elif state == state9:

            if c == '/':
                state = state0

            elif c == '':
                state = errortk
                break
            else:
                state = state8

    token_buffer = ''.join(token_buffer)

    if token_buffer == "program":
        state = programtk
    elif token_buffer == "if":
        state = iftk
    elif token_buffer == "while":
        state = whiletk
    elif token_buffer == "forcase":
        state = forcasetk
    elif token_buffer == "not":
        state = nottk
    elif token_buffer == "function":
        state = functiontk
    elif token_buffer == "input":
        state = inputtk
    elif token_buffer == "declare":
        state = declaretk
    elif token_buffer == "else":
        state = elsetk
    elif token_buffer == "doublewhile":
        state = doublewhiletk
    elif token_buffer == "incase":
        state = incasetk
    elif token_buffer == "and":
        state = andtk
    elif token_buffer == "procedure":
        state = proceduretk
    elif token_buffer == "print":
        state = printtk
    elif token_buffer == "loop":
        state = looptk
    elif token_buffer == "when":
        state = whentk
    elif token_buffer == "or":
        state = ortk
    elif token_buffer == "call":
        state = calltk
    elif token_buffer == "exit":
        state = exittk
    elif token_buffer == "default":
        state = defaulttk
    elif token_buffer == "return":
         state = returntk
    elif token_buffer == "in":
        state = intk
    elif token_buffer == "inout":
        state = inouttk
    elif token_buffer == "then":
        state = thentk


    return state

#################################
# Intermediate code functions   #
#################################

def nextquad():
    global quad_label
    return quad_label

def genquad(op, x, y, z):
    global quad_label, quads
    label = nextquad()
    quad_label += 1
    new_quad = [str(label) , str(op), str(x), str(y), str(z)]
    quads.append(new_quad)

def newtemp():
    global temp_var_label

    temp = "T_" + str(temp_var_label)
    variables.append(temp)
    offset = find_offset()
    add_new_entity_temporary_variable(temp, offset)
    temp_var_label += 1
    return temp

def emptylist():
    list = []
    return list

def makelist(x):
    global quad_label
    list = []
    list.append(x)
    return list

def merge(list1, list2):
    list = list1 + list2
    return list

def backpatch(list, x):
    global quads

    for i in range(len(list)):
        list[i] = str(list[i])

    for quad in quads:
        if str(quad[0]) in list:
            quad[4] = str(x)


def add_halt():
    global quads

    last_quad = quads[len(quads) - 1]
    halt_num = int(last_quad[0])
    last_quad[0] = str(int(last_quad[0]) + 1)
    quads.append(last_quad)
    quads[len(quads) - 2] = [str(halt_num), "halt", "_", "_", "_"]


def print_quads_to_file():
    global quads
    quadfile = open("quads.int", "w")

    for quad in quads:
        print("%s\t%s\t""%s\t%s\t%s" % (quad[0], quad[1], quad[2], quad[3], quad[4]) , file = quadfile)
    quadfile.close()


# variable declarations
def form_var_dec_line(variables):
    dec_line = "int "
    for var in variables:
        dec_line = dec_line + str(var) + ", "
    dec_line = dec_line[:-2] + ";\n"
    return dec_line


# make file with intermediate code in C
def print_intermediate_c_code_to_file():
    global main_program_name, variables
    cfile = open("intermediate_c_code.c", "w")

    print('#include <stdio.h>\n\n' , file = cfile) 

    for quad in quads:
        #op is jump
        if quad[1] == "jump":
            print("\tL_%s:\tgoto L_%s;" %(quad[0], quad[4]), file=cfile)
        #op is comparison
        elif quad[1] in ("=", "<>", "<", "<=", ">", ">="):
            temp_op = quad[1]
            if temp_op == "=":
                temp_op = "=="
            elif temp_op == "<>":
                temp_op = "!="
            print("\tL_%s:\tif ( %s %s %s ) goto L_%s;" %(quad[0], quad[2], temp_op, quad[3], quad[4]), file=cfile)
        #op is assignment
        elif quad[1] == ":=":
            print("\tL_%s:\t%s = %s;" %(quad[0], quad[4], quad[2]), file=cfile)
        #op is math oper
        elif quad[1] in ("+", "-", "*", "/"):
            print("\tL_%s:\t%s = %s %s %s;" %(quad[0], quad[4], quad[2], quad[1], quad[3]), file=cfile)
        #op is print
        elif quad[1] == "out":
            #print('\tL_%s:\tprintf("%d\\n", %s);' %(quad[0], quad[2]), file=cfile)
            retval = '\tL_' + str(quad[0]) + ':\tprintf("%d", ' + str(quad[2]) + ');'
            print("%s" %(retval), file=cfile)
        #op is scan
        elif quad[1] == "in":
            print('\tL_%s:\tscanf(" %d", &%s);' %(quad[0], quad[2]), file=cfile)
        #op is return
        elif quad[1] == "retv":
            print("\tL_%s:\treturn %s;" %(quad[0], quad[2]), file=cfile)
        
        #initiate block
        elif quad[1] == "begin_block":
            declare_line = '\t' + form_var_dec_line(variables)
            if quad[2] == main_program_name:
                retval = "int main (void){\n\n"
                retval += declare_line
                retval += '\n\tL_' + str(1) + ":"
                print("%s" %(retval), file=cfile)
            else:
                print("warning!! the C intermediate code cannot be print correctly because it contains procedures/functions")
                cfile.close()
                return
        #function or procedure
        elif quad[1] == "call":
            print("Warning!! The C intermediate code cannot be print correct because it contains procedures/functions!!")
            print("Ignore the .c file!!")
            cfile.close()
            return 
        elif quad[1] == "end_block":
            print("")
        #end of main()
        elif quad[1] == "halt":
            print("\tL_%s:\t{}\n}" % (quad[0]), file=cfile)


    cfile.close()

#############################
# Symbol table classes      #
#############################

class Scope():
    def __init__(self, entities, nesting_level):
        self.entities = entities
        self.nesting_level = nesting_level

class Argument():
    def __init__(self, name, par_mode):
        self.name = name
        self.par_mode = par_mode

class Entity():
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, "VARIABLE")
        self.name = name
        self.offset = offset

class Function(Entity):
    def __init__(self, name, start_quad, arguments, framelength):
        super().__init__(name, "FUNCTION")
        self.name = name
        self.start_quad = start_quad
        self.arguments = arguments
        self.framelength = framelength

class Parameter(Entity):
    def __init__(self, name, par_mode, offset, par_nesting_level):
        super().__init__(name, "PARAMETER")
        self.name = name
        self.par_mode = par_mode
        self.offset = offset
        self.par_nesting_level = par_nesting_level

class Temporary_variable(Entity):
    def __init__(self, name, offset):
        super().__init__(name, "TEMPORARY VARIABLE")
        self.name = name
        self.offset = offset

#############################
# Symbol table functions    #
#############################

# Handle scopes functions
def add_new_scope():
    global scopes
    enclosing_scope = scopes[-1]
    new_nesting_level = enclosing_scope.nesting_level + 1
    new_scope = Scope([], new_nesting_level)
    scopes.append(new_scope)

def add_program_scope():
    global scopes
    entities = []
    new_scope = Scope(entities, 0)
    scopes.append(new_scope)

def delete_scope():
    global scopes
    scopes.remove(scopes[-1])
    print_scopes()


# Handle entities functions
def add_new_entity(entity):
    global scopes
    enclosing_scope = scopes[-1]
    enclosing_scope.entities.append(entity)
    print_scopes()

def add_new_entity_variable(name, offset):
    new_variable = Variable(name, offset)
    add_new_entity(new_variable)

def add_new_entity_function(name):
    start_quad = nextquad()
    new_function = Function(name, start_quad ,arguments=[], framelength=0)
    add_new_entity(new_function)

def update_function_start_quad(name):
    global main_program_name
    
    block_start_quad = nextquad()
    if name == main_program_name:
        return block_start_quad
    function = search_entity(name)
    function.start_quad = block_start_quad
    return block_start_quad

def update_function_arguments(name, argument_name, argument_mode):
    function_entity = search_entity(name)
    argument = Argument(argument_name, argument_mode)
    function_entity.arguments.append(argument)

def update_function_framelength(name):
    global scopes, main_program_name, main_program_framelength

    offset = find_offset()
    framelength = offset

    if name == main_program_name:
        main_program_framelength = framelength
        return

    function_entity = search_entity(name)
    function_entity.framelength = framelength

def find_offset():
    global scopes
    enclosing_scope = scopes[-1]
    count = 0
    for entity in enclosing_scope.entities:
        if not isinstance(entity, Function):
            count += 1
    offset = 12 + ((count-1) * 4) + 4
    return offset

def add_new_entity_parameter(name, par_mode):
    global pars, scopes
    offset = find_offset()
    par_nesting_level = scopes[-1].nesting_level - 1

    new_parameter = Parameter(name, par_mode, offset, par_nesting_level)
    add_new_entity(new_parameter)
    pars.append(new_parameter)

def add_new_entity_temporary_variable(name, offset):
    new_temporary_variable = Temporary_variable(name, offset)
    add_new_entity(new_temporary_variable)


def search_entity(name):
    global scopes
    if scopes == []:
        return
    for scope in reversed(scopes):
        for entity in scope.entities:
            if entity.name == name:
                return entity

def print_scopes():
    global scopes, scopefile

    for scope in reversed(scopes):
        buf = []
        buf.append(str(scope.nesting_level) + " - ")
        for entity in scope.entities:
            if isinstance(entity, Function):
                buf.append(str(entity.name) + "/" + str(entity.framelength))
                for argument in entity.arguments:
                    buf.append("," + str(argument.name) + "-" + str(argument.par_mode))
                buf.append("\t")
            elif isinstance(entity, Parameter):
                buf.append(str(entity.name) + "/" + str(entity.offset) + "/" + str(entity.par_mode)  + "/" + str(entity.par_nesting_level) + "\t")
            else:
                buf.append(str(entity.name) + "/" + str(entity.offset) + "\t")
        buf = "".join(buf)
        print(buf, file=scopefile)
    print("\n\n" ,file=scopefile)


#############################
# Final code functions      #
#############################

def search_entity_final(name):
    global scopes

    for scope in reversed(scopes):
        for entity in reversed(scope.entities):
            if name == entity.name:
               return entity
    print("search_entity_final - 'den vrhka to %s'" %name)

def search_scope_final(name):
    global scopes

    for scope in reversed(scopes):
        for entity in reversed(scope.entities):
            if name == entity.name:
                return scope.nesting_level
    print("search_scope_final - 'den vrhka to scope tou %s'" %name)

def search_parameter_final(name):
    global scopes, pars
    return_value = pars[0]
    pars.remove(pars[0])
    return return_value

def gnvlcode(v):
    global scopes, outfile

    if isinstance(v, Parameter):
        v_entity = v
        v_nesting_level = v.par_nesting_level
    else:
        v_entity = search_entity_final(v)
        v_nesting_level = search_scope_final(v)
    current_nesting_level = scopes[-1].nesting_level

    print('\tlw $t0, -4($sp)', file=outfile)
    scopes_dif = current_nesting_level - v_nesting_level - 1
    for i in range(scopes_dif):
        print('\tlw $t0, -4($t0)', file=outfile)
    print('\taddi $t0, $t0, -%d' %v_entity.offset, file=outfile)

def print_scopes_to_stdout():
    global scopes

    for scope in reversed(scopes):
        buf = []
        buf.append(str(scope.nesting_level) + " - ")
        for entity in scope.entities:
            buf.append(entity.type + "/")
            if isinstance(entity, Function):
                buf.append(str(entity.name) + "/" + str(entity.framelength))
                for argument in entity.arguments:
                    buf.append("," + str(argument.name) + "-" + str(argument.par_mode))
                buf.append("\t")
            elif isinstance(entity, Parameter):
                buf.append(str(entity.name) + "/" + str(entity.offset) + "/" + str(entity.par_mode)  + "/" + str(entity.par_nesting_level) + "\t")
            else:
                buf.append(str(entity.name) + "/" + str(entity.offset) + "\t")
        buf = "".join(buf)
        print(buf)
    print("\n\n")

def print_pars():
    global pars
    print("PARS:")
    for par in pars:
        print("%s/%s/%d" %(par.name, par.par_mode, par.par_nesting_level))
    print("\n")

def loadvr(v, r):
    global scopes, outfile

    if str(v).isdigit():
        print('\tli %s, %s' % (r, v), file=outfile)
    else:

        if isinstance(v, Parameter):
            v_entity = v
            v_nesting_level = v.par_nesting_level
        else:
            v_entity = search_entity_final(v)
            v_nesting_level = search_scope_final(v)

        current_nesting_level = scopes[-1].nesting_level

        if v_entity.type == "VARIABLE" and v_nesting_level == 0:
            print('\tlw %s, -%d($s0)' % (r, v_entity.offset), file=outfile)

        elif (v_entity.type == "VARIABLE" and v_nesting_level == current_nesting_level) or \
                (v_entity.type == "PARAMETER" and v_entity.par_mode == "cv" and v_nesting_level==current_nesting_level) or \
                (v_entity.type == "TEMPORARY VARIABLE"):
            print('\tlw %s, -%d($sp)' % (r, v_entity.offset), file=outfile)

        elif (v_nesting_level == current_nesting_level) and (v_entity.type == "PARAMETER") and (v_entity.par_mode == "ref"):
            print('\tlw $t0, -%d($sp)' % v_entity.offset, file=outfile)
            print('\tlw %s, ($t0)' % r, file=outfile)

        elif (v_nesting_level < current_nesting_level and v_entity.type == "VARIABLE") or \
                (v_entity.type == "PARAMETER" and v_entity.par_mode == "cv" and v_nesting_level < current_nesting_level):
            gnvlcode(v_entity.name)
            print('\tlw %s, ($t0)' % r, file=outfile)

        elif v_nesting_level < current_nesting_level and v_entity.type == "PARAMETER" and v_entity.par_mode == "ref":
            gnvlcode(v_entity.name)
            print('\tlw $t0, ($t0)', file=outfile)
            print('\tlw %s, ($t0)' % r, file=outfile)

def storerv(r, v):
    global scopes, outfile

    if isinstance(v, Parameter):
        v_entity = v
        v_nesting_level = v.par_nesting_level
    else:
        v_entity = search_entity_final(v)
        v_nesting_level = search_scope_final(v)
    current_nesting_level = scopes[-1].nesting_level

    if v_nesting_level == 0 and v_entity.type == "VARIABLE" and v_nesting_level != current_nesting_level:
        print('\tsw %s, -%d($s0)' % (r, v_entity.offset), file=outfile)

    elif (v_entity.type == "VARIABLE" and v_nesting_level == current_nesting_level) or \
            (v_entity.type == "PARAMETER" and v_entity.par_mode == "cv" and v_nesting_level == current_nesting_level) or \
            (v_entity.type == "TEMPORARY VARIABLE"):
        print('\tsw %s, -%d($sp)' % (r, v_entity.offset), file = outfile)

    elif v_entity.type == "PARAMETER" and v_entity.par_mode == "ref" and v_nesting_level == current_nesting_level:
        print('\tlw $t0, -%d($sp)' % v_entity.offset, file = outfile)
        print('\tsw %s, ($t0)' %r, file=outfile)

    elif (v_entity.type == "VARIABLE" and v_nesting_level < current_nesting_level) or \
            (v_entity.type == "PARAMETER" and v_nesting_level < current_nesting_level and v_entity.par_mode == "cv"):
        gnvlcode(v_entity.name)
        print('\tsw %s, ($t0)' % r, file = outfile)

    elif v_entity.type == "PARAMETER" and v_nesting_level < current_nesting_level and v_entity.par_mode == "ref":
        gnvlcode(v_entity.name)
        print('\tlw $t0, ($t0)', file = outfile)
        print('\tsw %s, ($t0)' % r, file = outfile)

def relop_to_mips(relop):
    if relop == "<":
        return "blt"
    elif relop == ">":
        return "bgt"
    elif relop == "=":
        return "beq"
    elif relop == "<=":
        return "ble"
    elif relop == ">=":
        return "bge"
    elif relop == "<>":
        return "bne"

def op_to_mips(op):
    if op == "+":
        return "add"
    elif op == "-":
        return "sub"
    elif op == "*":
        return "mul"
    elif op == "/":
        return "div"

def find_par_offset(par_name):
    global function_pars

    function_pars.append(par_name)
    i = len(function_pars) - 1
    return (12 + 4*i)

def find_caller_function():
    global scopes
    if len(scopes) == 1:
        return "main"
    else:
        for entity in reversed(scopes[-2].entities):
            if entity.type == "FUNCTION":
                return entity

def find_caller_function_nesting_level(callee_func_name):
    global scopes
    for scope in reversed(scopes):
        for entity in reversed(scope.entities):
            if entity.name == callee_func_name:
                return scope.nesting_level

def find_callee_function(name):
    global scopes
    for scope in reversed(scopes):
        for entity in reversed(scope.entities):
            if entity.type == "FUNCTION" and entity.name == name:
                return entity

def find_callee_function_nesting_level(name):
    global scopes
    for scope in reversed(scopes):
        for entity in reversed(scope.entities):
            if entity.type == "FUNCTION" and entity.name == name:
                return (scope.nesting_level + 1)

def turn_to_mips_assembly(quad):
    global quads, outfile, current_block, main_program_name, main_program_framelength, is_first_par, function_pars

    if quad[1] != "par" and quad[1] != "call":
        is_first_par = True

    if quad[1] == "begin_block" and quad[2] == main_program_name:
        outfile.write('\nL_main:')

    print('\nL_' + str(quad[0]) + ':', file=outfile)

    if quad[1] == "jump":
        print('\tj L_%s\n' % quad[4], file=outfile)

    elif quad[1] in ("<", ">", "=", "<=", ">=", "<>"):
        relop = relop_to_mips(quad[1])
        loadvr(quad[2], "$t1")
        loadvr(quad[3], "$t2")
        print('\t%s $t1, $t2, L_%s\n' % (relop, quad[4]), file=outfile)

    elif quad[1] == ":=":
        loadvr(quad[2], "$t1")
        storerv("$t1", quad[4])

    elif quad[1] in ("+", "-", "*", "/"):
        op = op_to_mips(quad[1])
        loadvr(quad[2], "$t1")
        loadvr(quad[3], "$t2")
        print('\t%s $t1, $t1, $t2' % op, file=outfile)
        storerv("$t1", quad[4])

    elif quad[1] == "out":
        print('\tli $v0, 1', file=outfile)
        loadvr(quad[2], "$a0")
        print('\tsyscall', file=outfile)

    elif quad[1] == "inp":
        print('\t$v0,5', file=outfile)
        print('\tsyscall', file=outfile)
        storerv("$v0", quad[4])

    elif quad[1] == "retv":

        loadvr(quad[2], '$t1')
        print('\tlw $t0, -8($sp)', file=outfile)
        print('\tsw $t1, ($t0)', file=outfile)

    elif quad[1] == "par":

        if quad[3] != "RET":
            if main_program_framelength != -1:
                func_entity = "main"
                func_nesting_level = 0
                func_framelength = main_program_framelength

            for scope in reversed(scopes):
                for entity in reversed(scope.entities):
                    if entity.type == "FUNCTION":
                        func_entity = entity
                        func_nesting_level = scope.nesting_level
                        func_framelength = func_entity.framelength

            par_entity = search_parameter_final(quad[2])
            par_name = par_entity.name
            offset = find_par_offset(par_name)

        if is_first_par == True:
            print('\taddi $fp, $sp, %d' %func_framelength, file=outfile)
            is_first_par = False

        if quad[3] == "CV":
            loadvr(par_entity, "$t0")
            print('\tsw $t0, -%d($fp)' %offset, file=outfile)

        elif quad[3] == "REF":

            par_nesting_level = par_entity.par_nesting_level
            par_entity = Variable(par_entity.name, par_entity.offset)

            if par_nesting_level == func_nesting_level and ((par_entity.type == "VARIABLE") or (par_entity.type == "PARAMETER" and par_entity.par_mode == "cv")):
                print('\taddi $t0, $sp, -%s' %par_entity.offset, file=outfile)
                print('\tsw $t0, -%d($fp)' %offset, file=outfile)

            elif par_nesting_level == func_nesting_level and par_entity.type == "PARAMETER" and par_entity.par_mode == "ref":
                print('\tlw $t0, -%s($sp)' %par_entity.offset, file=outfile)
                print('\tsw $t0, -%d($fp)' %offset, file=outfile)

            elif par_nesting_level != func_nesting_level and ((par_entity.type == "TEMPORARY VARIABLE") or (par_entity.type == "PARAMETER" and par_entity.par_mode == "cv")):
                gnvlcode(quad[2])
                print('\tsw $t0, -%d($fp)' %offset, file=outfile)

            elif par_nesting_level != func_nesting_level and par_entity.type == "PARAMETER" and par_entity.par_mode == "ref":
                gnvlcode(quad[2])
                print('\tlw $t0, ($t0)', file=outfile)
                print('\tsw $t0, -%d($fp)' %offset, file=outfile)

        elif quad[3] == "RET":
            temp_var = search_entity_final(quad[2])
            
            print('\taddi $t0, $sp, -%s' %temp_var.offset, file=outfile)
            print('\tsw $t0, -8($fp)', file=outfile)

    elif quad[1] == "call":
        if is_first_par == True:
            for scope in reversed(scopes):
                for entity in reversed(scope.entities):
                    if entity.type == "FUNCTION" and entity.name == quad[4]:
                        func_entity = entity
                        func_framelength = func_entity.framelength

            print('\taddi $fp, $sp, %d' %func_framelength, file=outfile)
            is_first_par = False

        if current_block == main_program_name:
            caller_function_nesting_level = 0
        else:
            caller_function_nesting_level = find_caller_function_nesting_level(current_block)

        callee_function = find_callee_function(quad[4])
        callee_function_nesting_level = find_callee_function_nesting_level(quad[4])

        if caller_function_nesting_level == callee_function_nesting_level:
            print('\tlw $t0, -4($sp)', file=outfile)
            print('\tsw $t0, -4($fp)', file=outfile)

        elif caller_function_nesting_level != callee_function_nesting_level:
            print('\tsw $sp, -4($fp)', file=outfile)

        print('\taddi $sp, $sp, %s' %callee_function.framelength, file=outfile)
        print('\tjal L_%s' %callee_function.start_quad, file=outfile)
        print('\taddi $sp, $sp ,-%s' %callee_function.framelength, file=outfile)

    elif quad[1] == "begin_block":

        if quad[2] == main_program_name:
            print('\taddi $sp, $sp %d' %main_program_framelength, file=outfile)
            print('\tmove $s0, $sp', file=outfile)
        else:
            print('\tsw $ra, ($sp)', file=outfile)

    elif quad[1] == "end_block" and quad[2] != main_program_name:
        print('\tlw $ra, ($sp)', file=outfile)
        print('\tjr $ra', file=outfile)

#################################
# Syntax analysis functions     #
#################################

# <program> ::= program id { <block> }
def program():
    global token, linepointer, token_buffer, main_program_name

    #print("def program()")
    if token == programtk:
        token = lex()
        if token == idtk:

            add_program_scope()

            main_program_name = token_buffer

            token = lex()
            if token == left_bracetk:
                token = lex()
                block(main_program_name)
                if token == right_bracetk:
                    print("Syntax analysis completed without errors!!")

                else:
                    print("error in line %s, was expecting '}' but read '%s' instead" % (linepointer, token_buffer))
                    sys.exit()
            else:
                print("error in line %s, was expecting '{' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            print("error in line %s, was expecting program name but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting 'program' keyword but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <block> ::= <declarations> <subprograms> <statements>
def block(name):
    global program_name, quads, current_block, current_quad
    #print("def block()")

    declarations()
    subprograms()

    block_start_quad = update_function_start_quad(name)

    genquad("begin_block", name, "_", "_")
    statements()
    genquad("end_block", name, "_", "_")

    update_function_framelength(name)
    #print_scopes_to_stdout()
    for quad in quads[block_start_quad - 1:]:
        current_block = name
        current_quad = quad
        turn_to_mips_assembly(quad)
    delete_scope()

# <declarations> ::= (declare <varlist>;)*
def declarations():
    global token, linepointer, token_buffer

    #print("def declarations()")
    while True:
        if token == declaretk:
            token = lex()
            varlist()
            if token == semicolontk:
                token = lex()
            else:
                print("error in line %s, was expecting ';' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            break

# <varlist> ::= ε | id ( , id )*
def varlist():
    global token, linepointer, token_buffer, variables

    #print("def varlist()")
    if token == idtk:
        variable_name = token_buffer

        offset = find_offset()
        add_new_entity_variable(variable_name, offset)

        variables.append(variable_name)
        token = lex()
        while True:
            if token == commatk:
                token = lex()
                if token == idtk:
                    variable_name = token_buffer

                    offset = find_offset()
                    add_new_entity_variable(variable_name, offset)

                    variables.append(variable_name)
                    token = lex()
                else:
                    print("error in line %s, was expecting a variable name but read '%s' instead" %(linepointer, token_buffer))
                    sys.exit()
            else:
                break

# <subprograms> ::= (<subprogram>)*
def subprograms():

    #print("def subprograms()")
    while True:
        if token == functiontk or token == proceduretk:
            subprogram()
        else:
            break

# <subprogram> ::= function id <funcbody> | procedure id <funcbody>
def subprogram():
    global token, linepointer, token_buffer

    #print("def subprogram()")
    if token == functiontk:
        token = lex()
        if token == idtk:
            function_name = token_buffer

            add_new_entity_function(function_name)
            add_new_scope()

            token = lex()
            funcbody(function_name)
        else:
            print("error in line %s, was expecting function name but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    elif token == proceduretk:
        token = lex()
        if token == idtk:
            procedure_name = token_buffer

            add_new_entity_function(procedure_name)
            add_new_scope()

            token = lex()
            funcbody(procedure_name)
        else:
            print("error in line %s, was expecting procedure name but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()

# <funcbody> ::= <formalpars> { <block> }
def funcbody(name):
    global token, linepointer, token_buffer, quads

    #print("def funcbody()")
    formalpars(name)
    if token == left_bracetk:
        token = lex()
        block(name)
        if token == right_bracetk:
            #update_function_framelength(name)
            token = lex()
        else:
            print("error in line %s, was expecting '}' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '{' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <formalpars> ::= ( <formalparlist> )
def formalpars(name):
    global token, linepointer, token_buffer

    #print("def formalpars()")
    if token == left_parenthesistk:
        token = lex()
        formalparlist(name)
        if token == right_parenthesistk:
            token = lex()
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <formalparlist> ::= <formalparitem> ( , <formalparitem> )* | ε
def formalparlist(name):
    global token

    #print("def formalparlist()")
    if token == intk or token == inouttk:
        formalparitem(name)
        while True:
            if token == commatk:
                token = lex()
                formalparitem(name)
            else:
                break

# <formalparitem> ::= in id | inout id
def formalparitem(name):
    global token, linepointer, token_buffer

    #print("def formalparitem()")
    if token == intk:

        token = lex()
        if token == idtk:

            argument_name = token_buffer
            update_function_arguments(name, argument_name, "in")

            parameter_name = token_buffer
            add_new_entity_parameter(parameter_name, "cv")

            token = lex()
        else:
            print("error in line %s, was expecting an id after 'in' keyword but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    elif token == inouttk:

        token = lex()
        if token == idtk:

            argument_name = token_buffer
            update_function_arguments(name, argument_name, "inout")

            parameter_name = token_buffer
            add_new_entity_parameter(parameter_name, "ref")

            token = lex()
        else:
            print("error in line %s, was expecting an id after 'inout' keyword but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting 'in' or 'inout' keyword but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

#<statements> ::= <statement> | { <statement> ( ; <statement> )* }
def statements():
    global token, linepointer, token_buffer

    #print("def statements()")
    if token == left_bracetk:
        token = lex()
        statement()
        while True:
            if token == semicolontk:
                token = lex()
                statement()
            else:
                break

        if token == right_bracetk:
            token = lex()
        else:
            print("error in line %s, was expecting '}' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        statement()

# <statement> ::= <assignment-stat> | <if-stat> |
#                 <while-stat> | <doublewhile-stat> |
#                 <loop-stat> | <exit-stat> |
#                 <forcase-stat> | <incase-stat> |
#                 <call-stat> | <return-stat> |
#                 <input-stat> | <print-stat>

def statement():
    global token, token_buffer, quads

    if token == idtk:
        id = token_buffer
        token = lex()
        assignment_stat(id)
    elif token == iftk:
        token = lex()
        if_stat()
    elif token == whiletk:
        token = lex()
        while_stat()
    elif token == doublewhiletk:
        token = lex()
        doublewhile_stat()
    elif token == looptk:
        token = lex()
        loop_stat()
    elif token == exittk:
        token = lex()
        exit_stat()
    elif token == forcasetk:
        token = lex()
        forcase_stat()
    elif token == incasetk:
        token = lex()
        incase_stat()
    elif token == calltk:
        token = lex()
        call_stat()
    elif token == returntk:
        token = lex()
        return_stat()
    elif token == inputtk:
        token = lex()
        input_stat()
    elif token == printtk:
        token = lex()
        print_stat()
    else:
        print("error in line %s, was expecting a statement keyword(if, while, doublewhile...) or variable name but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <assignment-stat> ::= id := <expression>
def assignment_stat(id):
    global token, linepointer, token_buffer

    #print("def assignment_stat()")

    if token == assigntk:
        token = lex()
        Eplace = expression()
        # {P1}:
        genquad(":=", Eplace, "_", id)
    else:
        print("error in line %s, was expecting ':=' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()


# <if-stat> ::= if (<condition>) then <statements> <elsepart>
def if_stat():
    global token, linepointer, token_buffer

    #print("def if_stat()")

    if token == left_parenthesistk:
        token = lex()
        Btrue, Bfalse = condition()
        if token == right_parenthesistk:
            token = lex()
            if token == thentk:
                token = lex()
                #{P1}:
                backpatch(Btrue, nextquad())
                statements()
                #{P2}:
                ifList = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                backpatch(Bfalse, nextquad())
                elsepart()
                #{P3}:
                backpatch(ifList, nextquad())
            else:
                print("error in line %s, was expecting 'then' keyword but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
                print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()




# <elsepart> ::= ε | else <statements>
def elsepart():
    global token

    #print("def elsepart()")
    if token == elsetk:
        token = lex()
        statements()

# <while-stat> ::= while (<condition>) <statements>
def while_stat():
    global token, linepointer, token_buffer

    #print("def while_stat()")
    #{P1}:
    Bquad = nextquad()
    if token == left_parenthesistk:
        token = lex()
        Btrue, Bfalse = condition()
        if token == right_parenthesistk:
            token = lex()
            #{P2}:
            backpatch(Btrue, nextquad())
            statements()
            #{P3}:
            genquad("jump", "_", "_", Bquad)
            backpatch(Bfalse, nextquad())
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" % (linepointer, token_buffer))
        sys.exit()


# <doublewhile-stat> ::= doublewhile (<condition>) <statements> else <statements>
def doublewhile_stat():
    global token, linepointer, token_buffer

    #print("def doublewhile_stat()")

    if token == left_parenthesistk:
        token = lex()
        condition()
        if token == right_parenthesistk:
            token = lex()
            statements()
            if token == elsetk:
                token = lex()
                statements()
            else:
                print("error in line %s, was expecting 'then' keyword but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <loop-stat> ::= loop <statements>
def loop_stat():

    #print("def loop_stat()")

    statements()

# <exit-stat> ::= exit
def exit_stat():

    #print("def exit()")
    token = lex()

# <forcase-stat> ::= forcase
#                       ( when (<condition>) : <statements> )*
#                       default: <statements>
def forcase_stat():
    global token, linepointer, token_buffer

    #print("def forcase_stat()")

    #{P1}:
    condquad = nextquad()

    while True:
        if token == whentk:
            token = lex()
            if token == left_parenthesistk:
                token = lex()
                condtrue, condfalse = condition()
                if token == right_parenthesistk:
                    token = lex()
                    if token == colontk:
                        token = lex()
                        #{P2}:
                        backpatch(condtrue, nextquad())
                        statements()
                        genquad("jump", "_", "_", condquad)
                        backpatch(condfalse, nextquad())
                    else:
                        print("error in line %s, was expecting ':' but read '%s' instead" %(linepointer, token_buffer))
                        sys.exit()
                else:
                    print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
                    sys.exit()
            else:
                print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            break
        # {P3}:
        #genquad("jump", "_", "_", condquad)
        #backpatch(condfalse, nextquad())
    if token == defaulttk:
        token = lex()
        if token == colontk:
            token = lex()
            statements()
        else:
            print("error in line %s, was expecting ':' but read '%s' instead" % (linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting 'default' keyword but read '%s' instead" % (linepointer, token_buffer))
        sys.exit()



# <incase-stat> ::= incase ( when (<condition>) : <statements> )*
def incase_stat():
    global token, linepointer, token_buffer

    #print("def incase_stat()")

    while True:
        if token == whentk:
            token = lex()
            if token == left_parenthesistk:
                token = lex()
                condition()
                if token == right_parenthesistk:
                    token = lex()
                    if token == colontk:
                        token = lex()
                        statements()
                    else:
                        print("error in line %s, was expecting ':' but read '%s' instead" %(linepointer, token_buffer))
                        sys.exit()
                else:
                    print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
                    sys.exit()
            else:
                print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            break

# <return-stat> ::= return <expression>
def return_stat():

    #print("def return_stat()")

    Eplace = expression()
    genquad("retv", Eplace, "_", "_")

# <call-stat> ::= call id <actualpars>
def call_stat():
    global token, linepointer, token_buffer

    #print("def call_stat()")
    if token == idtk:
        id = token_buffer
        token = lex()
        actualpars()
        genquad("call", "_", "_", id)
    else:
        print("error in line %s, was expecting a variable name after 'call' keyword but read '%s' instead" % (linepointer, token_buffer))


# <print-stat> ::= print (<expression>)
def print_stat():
    global token, linepointer, token_buffer

    #print("def print_stat()")

    if token == left_parenthesistk:
        token = lex()
        Eplace = expression()
        if token == right_parenthesistk:
            #{P2}:
            genquad("out", Eplace, "_", "_")
            token = lex()
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()


# <input-stat> ::= input (id)
def input_stat():
    global token, linepointer, token_buffer

    #print("def input_stat()")

    if token == left_parenthesistk:
        token = lex()
        if token == idtk:
            idplace = token_buffer
            token = lex()
            if token == right_parenthesistk:
                # {P1}:
                genquad("inp", idplace, "_", "_")
                token = lex()

            else:
                print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            print("error in line %s, was expecting an id after 'input' keyword but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()


# <actualpars> ::= ( <actualparlist> )
def actualpars():
    global token, linepointer, token_buffer

    #print("def actualpars()")
    if token == left_parenthesistk:
        token = lex()
        if token == intk or token == inouttk:
            actualparlist()
        if token == right_parenthesistk:
            token = lex()
            return True
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting '(' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <actualparlist> ::= <actualparitem> ( , <actualparitem> )* | ε
def actualparlist():
    global token

    #print("def actualparlist()")
    actualparitem()
    while True:
        if token == commatk:
            token = lex()
            actualparitem()
        else:
            break

# <actualparitem> ::= in <expression> | inout id
def actualparitem():
    global token, linepointer, token_buffer

    #print("def actualparitem()")
    if token == intk:
        token = lex()
        Eplace = expression()
        genquad("par", Eplace, "CV", "_")

    elif token == inouttk:
        token = lex()
        if token == idtk:
            id = token_buffer
            genquad("par", id, "REF", "_")
            token = lex()

        else:
            print("error in line %s, was expecting an id after 'inout' keyword but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        print("error in line %s, was expecting 'in' or 'inout' keyword but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <condition> ::= <boolterm> (or <boolterm>)*
def condition():
    global token

    #print("def condition()")
    #{P1}:
    Q1true, Q1false = boolterm()
    Btrue = Q1true
    Bfalse = Q1false
    while True:
        if token == ortk:
            #{P2}:
            backpatch(Bfalse, nextquad())
            token = lex()
            Q2true, Q2false = boolterm()
            #{P3}:
            Btrue = merge(Btrue, Q2true)
            Bfalse = Q2false

        else:
            break
    return Btrue, Bfalse

# <boolterm> ::= <boolfactor> (and <boolfactor>)*
def boolterm():
    global token

    #print("def boolterm()")
    #Qtrue, Qfalse = R1true, R1false = boolfactor()
    R1true, R1false = boolfactor()
    #{P1}:
    Qtrue = R1true
    Qfalse = R1false
    while True:
        if token == andtk:
            backpatch(Qtrue, nextquad())
            token = lex()
            R2true, R2false = boolfactor()
            Qfalse = merge(Qfalse, R2false)
            Qtrue = R2true

        else:
            break
    return Qtrue, Qfalse

# <boolfactor> ::= not [<condition>]
#                    | [<condition>]
#                    | <expression> <relational-oper> <expression>
def boolfactor():
    global token, linepointer, token_buffer

    #print("def boolfactor()")
    if token == nottk:
        token = lex()
        if token == left_brackettk:
            token = lex()
            Btrue, Bfalse = condition()
            if token == right_brackettk:
                Rtrue = Bfalse
                Rfalse = Btrue
                token = lex()
                return Rtrue, Rfalse
            else:
                print("error in line %s, was expecting ']' but read '%s' instead" %(linepointer, token_buffer))
                sys.exit()
        else:
            print("error in line %s, was expecting '[' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    elif token == left_brackettk:
        token = lex()
        Btrue, Bfalse = condition()
        if token == right_brackettk:
            Rtrue = Btrue
            Rfalse = Bfalse
            token = lex()
            return Rtrue, Rfalse
        else:
            print("error in line %s, was expecting ']' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    else:
        E1place = expression()
        relop = relational_oper()
        E2place = expression()
        #{P1}:
        Rtrue = makelist(nextquad())
        genquad(relop, E1place, E2place, "_")
        Rfalse = makelist(nextquad())
        genquad("jump", "_", "_", "_")

        return Rtrue, Rfalse



# <expression> ::= <optional-sign> <term> ( <add-oper> <term>)* 
def expression():
    global token

    #print("def expression()")

    sign = optional_sign()
    T1place = term()
    if sign != None:
        x = newtemp()
        genquad("-", "0", T1place, x)
        T1place = x
    while True:
        if token == plustk or token == minustk:
            operation = add_oper()
            T2place = term()
            #{P1}:
            w = newtemp()
            genquad(operation, T1place, T2place, w)
            T1place = w
        else:
            break
    #{P2}:
    Eplace = T1place
    return Eplace


# <term> ::= <factor> (<mul-oper> <factor>)*
def term():
    global token, token_buffer

    #print("def term()")
    F1place = factor()
    while True:
        if token == multiplytk or token == dividetk:
            operation = mul_oper()
            F2place = factor()
            #{P1}:
            w = newtemp()
            genquad(operation, F1place, F2place, w)
            F1place = w
        else:
            break
    #{P2}:
    Tplace = F1place
    return Tplace


# <factor> ::= constant
#            | (<expression>)
#            | id <idtail>

def factor():
    global token, linepointer, token_buffer

    #print("def factor()")
    if token == constanttk:
        constant = token_buffer
        token = lex()
        return constant
    elif token == left_parenthesistk:

        token = lex()
        Eplace = expression()
        if token == right_parenthesistk:
            token = lex()
            return Eplace
        else:
            print("error in line %s, was expecting ')' but read '%s' instead" %(linepointer, token_buffer))
            sys.exit()
    elif token == idtk:
        id = token_buffer
        token = lex()
        tail = idtail()
        if tail != None:
            w = newtemp()
            genquad("par", w, "RET", "_")
            genquad("call", "_", "_", id)
            return w
        else:
            return id
    else:
        print("error in line %s, was expecting a constant, (<expression>) or the call of a function, but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <idtail> ::= ε | <actualpars>
def idtail():
    global token

    #print("def idtail()")

    if token == left_parenthesistk:
        actual_pars = actualpars()
        return actual_pars
    else:
        return None

# <relational-oper> ::= = | <= | >= | > | < | <>
def relational_oper():
    global token, linepointer, token_buffer

    #print("def relational_oper()")
    relop = token_buffer
    if token == equaltk:
        token = lex()
        return relop
    elif token == less_than_or_equaltk:
        token = lex()
        return relop
    elif token == greater_than_or_equaltk:
        token = lex()
        return relop
    elif token == greatertk:
        token = lex()
        return relop
    elif token == lesstk:
        token = lex()
        return relop
    elif token == not_equaltk:
        token = lex()
        return relop
    else:
        print("error in line %s, was expecting a relatioanal operator (<, >= ...), but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <add-oper> ::= + | -
def add_oper():
    global token, linepointer, token_buffer

    #print("def add_oper()")
    if token == plustk:
        operation = token_buffer
        token = lex()
        return operation
    elif token == minustk:
        operation = token_buffer
        token = lex()
        return operation
    else:
        print("error in line %s, was expecting a '+' or '-' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <mul-oper> ::= * | /
def mul_oper():
    global token, linepointer, token_buffer

    operation = token_buffer
    #print("mul_oper()")
    if token == multiplytk:
        token = lex()
        return operation
    elif token == dividetk:
        token = lex()
        return operation
    else:
        print("error in line %s, was expecting '*' or '/' but read '%s' instead" %(linepointer, token_buffer))
        sys.exit()

# <optional-sign> ::= ε | <add-oper>
def optional_sign():
    global token, token_buffer

    #print("def optional_sign()")
    if token == plustk or token == minustk:
       sign = token_buffer
       token = lex()
       return sign
    else:
        return None

#####################################
# Main function                     #
#####################################

def main():
    global infile, token, outfile, quads, scopefile

    if sys.argv[1][-4:] != ".min":
        print("error, the input file is not a .min file")


    scopefile = open("scopes.sym", "w")
    infile = open(sys.argv[1], "r")
    outfile = open("final.asm", "w")
    print('\n.data\n\n.text\n\n', file=outfile)
    print('L_0:', file=outfile)
    print('    j L_main', file=outfile)

    token = lex()
    program()
    add_halt()
    print_quads_to_file()
    print_intermediate_c_code_to_file()

    scopefile.close()
    infile.close()
    outfile.close()

if __name__ == "__main__":
    main()

#########################################################################
#                                                                       #
#              Copyright (C) 2020 Thomas Dimitrakoulias                 #
#                                                                       #
#########################################################################