
class CodeGenerator(object):
    def __init__(self, semantic_stack, symbol_table, memory_manager, while_switch, program_block):
        self.stack = semantic_stack
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.program_block = program_block
        self.while_switch = while_switch
        self.add_output()

    def add_output(self):
        address = self.memory_manager.get_variable(1)
        var_address = self.memory_manager.get_variable(1)
        self.symbol_table.insert(name='output', address=address, typ='void', length=1, line=1, args=[(var_address, 'int')])
        self.program_block.append(('PRINT', var_address))
        self.program_block.append(('JP', address))


    def op(self):
        if self.stack[-2] == '+':
            tmp = self.memory_manager.get_temp(1)
            self.program_block.append(('ADD', self.stack[-3][0], self.stack[-1][0], tmp))
            self.pop_n(3)
            self.stack.append((tmp, 'int'))

        if self.stack[-2] == '-':
            tmp = self.memory_manager.get_temp(1)
            self.program_block.append(('SUB', self.stack[-3][0], self.stack[-1][0], tmp))
            self.pop_n(3)
            self.stack.append((tmp, 'int'))

        if self.stack[-2] == '<':
            tmp = self.memory_manager.get_temp(1)
            self.program_block.append(('LT', self.stack[-3][0], self.stack[-1][0], tmp))
            self.pop_n(3)
            self.stack.append((tmp, 'int'))

        if self.stack[-2] == '==':
            tmp = self.memory_manager.get_temp(1)
            self.program_block.append(('EQ', self.stack[-3][0], self.stack[-1][0], tmp))
            self.pop_n(3)
            self.stack.append((tmp, 'int'))


    def push_array(self):
        tmp = self.memory_manager.get_temp(1)
        arr = self.stack[-2]
        print(arr)
        print(self.stack)
        index = self.stack[-1][0]
        symbol = self.symbol_table.all_search(arr[0])
        self.program_block.append(("MULT",index, "#4",tmp))
        self.program_block.append(('ADD', symbol.address, tmp, tmp))
        self.pop_n(2)
        self.stack.append((tmp, 'int'))

    def assign(self):
        l = self.stack[-3]
        r = self.stack[-1]
        self.program_block.append(('ASSIGN', r[0], l[0]))
        self.pop_n(2)


    def mult(self):
        l = self.stack[-3]
        r = self.stack[-1]
        tmp = self.memory_manager.get_temp(1)
        self.program_block.append(('MULT', l[0], r[0], tmp))
        self.pop_n(3)
        self.stack.append((tmp, 'int'))


    def label(self):
        self.stack.append(len(self.program_block))

    def save(self):
        self.stack.append(len(self.program_block))
        self.program_block.append("")

    def finish_while(self):
        break_address = self.stack[-4]
        save_address = self.stack[-1]
        expression = self.stack[-2]
        label_address = self.stack[-3]
        self.program_block.append(('JP', label_address))
        self.program_block[save_address] = ('JPF', expression[0], len(self.program_block))
        self.program_block[break_address] = ('JP', len(self.program_block))
        self.pop_n(4)

    def finish_if(self):
        save_address = self.stack[-2]
        expression = self.stack[-3]
        self.program_block[save_address] = ('JPF', expression[0], len(self.program_block))

    def finish_else(self):
        save_address = self.stack[-1]
        self.program_block[save_address] = ('JP', len(self.program_block))
        self.pop_n(3)

    def compare(self):
        num = self.stack[-1]
        expression = self.stack[-3]
        tmp = self.memory_manager.get_temp(1)
        self.program_block.append(('EQ', num, expression[0], tmp))
        self.stack.pop()
        self.stack.append(tmp)

    def finish_case(self):
        case_address = self.stack[-1]
        compare_result = self.stack[-2]
        self.program_block[case_address] = ('JPF', compare_result, len(self.program_block))
        self.pop_n(2)

    def finish_switch(self):
        break_address = self.stack[-1]
        self.program_block[break_address] = ('JP', len(self.program_block))
        self.pop_n(2)

    def push_immediate(self, value):
        tmp = self.memory_manager.get_temp(1)
        self.program_block.append(('ASSIGN', value, tmp, '# 2'))
        self.stack.append((tmp, 'int'))

    def jump_to_main(self):
        symbol = self.symbol_table.all_search('main')
        self.program_block[0] = ('JP', symbol.line)

    def while_jump(self):
        self.program_block.append(('JP', len(self.program_block) + 2))

    def handle_continue(self):
        for i in self.while_switch[::-1]:
            if i[0] == 'while':
                self.program_block.append(('JP', i[1]))

    def handle_break(self):
        last = self.while_switch[-1]
        if last[0] == 'while':
            self.program_block.append(('JP', last[1] - 1))
        else:
            self.program_block.append(('JP', last[1]))

    def return_int(self):
        func_name = self.stack[-2]
        expression = self.stack[-1]
        function = self.symbol_table.all_search(func_name)
        tmp = self.memory_manager.get_temp(1)
        self.program_block.append(('ASSIGN', function.address, tmp))
        self.program_block.append(('ASSIGN', expression[0], function.address))
        self.program_block.append(('JP', tmp))
        self.stack.pop()

    def assign_arg(self):
        func_name = self.stack[-2]
        expression = self.stack[-1]
        function = self.symbol_table.all_search(func_name[0])
        arg = function.args[func_name[1]]
        self.program_block.append(('ASSIGN', expression[0], arg[0], '# 2'))
        self.pop_n(2)
        self.stack.append((func_name[0], func_name[1] + 1))

    def jump_return(self):
        func_name = self.stack[-1]
        function = self.symbol_table.all_search(func_name[0])
        address = function.line
        return_address = function.address
        self.program_block.append(('ASSIGN', len(self.program_block) + 2, return_address, '# 2'))
        self.program_block.append(('JP', address))
        tmp = self.memory_manager.get_temp(1)
        self.program_block.append(('ASSIGN', return_address, tmp))
        self.stack.pop()
        self.stack.append((tmp, function.typ))

    def pop_n(self, n):
        for i in range(n):
            self.stack.pop()