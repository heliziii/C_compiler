from symbol_table import SymbolTable

class SemanticAnalyzer(object):
    def __init__(self, semantic_stack, symbol_table, memory_manager, while_switch, program_block):
        self.stack = semantic_stack
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.while_switch = while_switch
        self.program_block = program_block


    def push(self, token):
        self.stack.append(token)

    def check_op_type(self, _line):
        op = self.stack[-2]
        if op in ['+', '-', '*', '<', '==', '=']:
            l = self.stack[-3]
            r = self.stack[-1]
            if l[1] != 'int' or r[1] != 'int':
                print('Line', _line, ': incompatible operand types')
                exit()

    def check_id(self, _line):
        top = self.stack[-1]
        symbol = self.symbol_table.all_search(top)
        if symbol is None or symbol.typ != 'int':
            print('Line', _line, ': identifier is not defined', top)
            exit()
        self.stack.pop()
        self.stack.append((symbol.address, symbol.typ, symbol.name))

    def check_array(self, _line):
        top = self.stack[-2]
        index = self.stack[-1]
        symbol = self.symbol_table.all_search(top)
        if symbol is None or symbol.typ != 'array':
            print('Line', _line, ': array is not defined %s', top)
            exit()
        if index[1] != 'int':
            print('Line', _line, ': invalid index %s', top)
            exit()

    def check_int(self, _line):
        top = self.stack[-1]
        if top[1] != 'int':
            print('Line', _line, ': expression type should be int')
            exit()

    def increase_scope(self):
        self.symbol_table.increase_scope()

    def decrease_scope(self):
        self.symbol_table.decrease_scope()

    def check_main(self):
        symbol = self.symbol_table.all_search('main')
        if symbol is None or symbol.line is None or symbol.typ != 'void':
            print('can not find main')
            exit()

    def check_var_int(self, _line):
        top = self.stack[-1]
        if top != 'int':
            print('Line', _line, ': variable type should be int')
            exit()
        self.stack.pop()

    def scope_search(self, _line):
        top = self.stack[-1]
        symbol = self.symbol_table.scope_search(top)
        if symbol is not None:
            print('Line',_line,":", top ," is already defined")
            exit()

    def insert_array_size(self, value, _line):
        if value < 1:
            print('Line', _line, ': array size should be positive')
            exit()
        else:
            address = self.memory_manager.get_variable(value)
            self.symbol_table.insert(name = self.stack[-1], address = address, typ = 'array', length = value)
            self.stack.pop()
            self.stack.append('array_check_point')

    def insert_id(self):
        if len(self.stack) > 0 and self.stack[-1] == 'array_check_point':
            self.stack.pop()
        else:
            name = self.stack[-1]
            address = self.memory_manager.get_variable(1)
            self.symbol_table.insert(name = name, address = address, typ = 'int', length = 1)
            self.stack.pop()

    def check_break(self, _line):
        if len(self.while_switch) < 1:
            print('Line', _line, ': break is not in a switch or while')
            exit()

    def check_continue(self, _line):
        find = False
        for i in self.while_switch:
            if i[0] == 'while':
                find = True
        if find is False:
            print('Line', _line, ': continue is not in a while')
            exit()

    def push_line(self):
        self.stack.append(len(self.program_block))

    def insert_function(self):
        typ = self.stack[-3]
        function = self.stack[-2]
        line = self.stack[-1]
        address = self.memory_manager.get_variable(1)
        self.symbol_table.insert(name = function, address = address, typ = typ, length = 0, line = line, args = [])
        self.stack.pop()

    def insert_param_id(self):
        name = self.stack[-1]
        func_name = self.stack[-3]
        address = self.memory_manager.get_variable(1)
        self.symbol_table.insert(name = name, address = address, typ = 'int', length = 1, line = None)
        function = self.symbol_table.all_search(func_name)
        function.length += 1
        function.args.append((address, 'int'))
        self.pop_n(2)

    def insert_param_array(self):
        name = self.stack[-1]
        func_name = self.stack[-3]
        address = self.memory_manager.get_variable(1)
        self.symbol_table.insert(name=name, address=address, typ='array', length=1, line=None)
        function = self.symbol_table.all_search(func_name)
        function.length += 1
        function.args.append((address, 'array'))
        self.pop_n(2)

    def pop_function(self):
        self.pop_n(2)

    def check_func_int(self, _line):
        if len(self.stack) < 3:
            print('Line', _line,":return should be in the function.")
            exit()
        else:
            typ = self.stack[-3]
            expression = self.stack[-1]
            if typ != 'int':
                print('Line', _line, ':return type is not match with function definition')
                exit()
            if expression[1] != 'int':
                print('Line', _line, ':return type is not match with function definition')
                exit()

    def check_func_void(self, _line):
        if len(self.stack) < 2:
            print('Line', _line, ":return should be in the function")
            exit()
        else:
            typ = self.stack[-2]
            if typ != 'void':
                print('Line', _line, ':return type is not match with function definition')
                exit()

    def check_function(self, _line):
        top = self.stack[-1]
        symbol = self.symbol_table.all_search(top[0])
        if symbol is None or symbol.line is None:
            print('Line', _line, ':function is not defined', top[0])
            exit()


    def check_arg(self, _line):
        func_name = self.stack[-2]
        expression = self.stack[-1]
        function = self.symbol_table.all_search(func_name[0])
        if function.length < func_name[1] + 1:
            print('Line', _line, ":invalid number of arguments")
            exit()

        if function.args[func_name[1]][1] != expression[1]:
            print('Line', _line, ":invalid argument type" , function.args[func_name[1]][1] , expression[1])
            exit()


    def check_args_count(self, _line):
        func_name = self.stack[-1]
        function = self.symbol_table.all_search(func_name[0])
        if function.length > func_name[1]:
            print('Line', _line, ":more arguments are needed for function" , func_name[0])
            exit()


    def add_function_count(self):
        top = self.stack[-1]
        self.stack.pop()
        self.stack.append((top, 0))


    def finalize_function(self, _line):
        func_name = self.stack[-1]
        symbols = self.symbol_table.get_list_scope_search(func_name)
        function = symbols[0]
        if len(symbols) > 1:
            for i in range(1, len(symbols)):
                symbol = symbols[i]
                if symbol.line is None:
                    print('Line', _line,":", func_name, "was declared before")
                    exit()
                else:
                    if symbol.length == function.length:
                        find = False
                        for j in range(len(function.args)):
                            if function.args[j][1] != symbol.args[j][1]:
                                find = True
                        if not find:
                            print('Line', _line,":", func_name, "was declared before")
                            exit()


    def pop_n(self, n):
        for i in range(n):
            self.stack.pop()



