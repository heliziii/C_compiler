from scanner import Scanner
from utils import FIRST, FOLLOW
from semantic_analyzer import SemanticAnalyzer
from symbol_table import SymbolTable
from memory_manager import MemoryManager
from code_generator import CodeGenerator

def prepare_input(address):
    input_list = []
    with open(address, 'r') as f:
        for line in f:
            for s in line.split(' '):
                if s[-1] == '\n':
                    s = s[:-1]
                input_list.append(s)
    return input_list


class Parser(object):
    def __init__(self, address):
        self.stack = []
        self.stack.append('$')
        self.scanner = Scanner(open(address).read())
        self.build_diagram()
        self.first = FIRST
        self.follow = FOLLOW
        self.panic_mode = False
        self.need_token = True
        self.symbol_table = SymbolTable()
        self.semantic_stack = []
        self.while_switch = []
        self.program_block = []
        self.program_block.append("")
        self.memory_manager = MemoryManager(10000, 20000)
        self.semantic_analyzer = SemanticAnalyzer(self.semantic_stack, self.symbol_table, self.memory_manager, self.while_switch, self.program_block)
        self.code_generator = CodeGenerator(self.semantic_stack, self.symbol_table, self.memory_manager, self.while_switch, self.program_block)



    def build_diagram(self):
        inp = prepare_input('diagram.txt')
        pointer = 0
        self.nt_counts = int(inp[pointer])
        self.node_counts = int(inp[pointer+1])
        pointer += 2
        self.nt_dicts = {}
        self.adj = [[] for i in range(self.node_counts + 1)]
        for i in range(self.nt_counts):
            name, start, end, edges = inp[pointer], int(inp[pointer + 1]), int(inp[pointer + 2]), int(inp[pointer + 3])
            self.nt_dicts[name] = (start, end)
            pointer += 4
            for j in range(edges):
                u, v, w = int(inp[pointer]), int(inp[pointer + 1]), inp[pointer + 2]
                pointer += 3
                self.adj[u].append((v, w))


    def parse(self):
        node = 0
        current_nt = 'program'
        while True:
            self.panic_mode = False
            if self.need_token:
                token = self.scanner.get_token()
            find = False
            for edge in self.adj[node]:
                v, w = edge[0], edge[1]
                if w in self.nt_dicts:
                    if token[0] in self.first[w] or ('eps' in self.first[w] and token[0] in self.follow[w]):
                        self.stack.append((node, v, current_nt))
                        #print('change graph', node, self.nt_dicts[w][0])
                        node = self.nt_dicts[w][0]
                        current_nt = w
                        self.need_token = False
                        find = True
                        break
                elif w == 'eps':
                    if token[0] in self.follow[current_nt]:
                        #print('go', node, v)
                        self.need_token = False
                        self.semantic(node, v, token[0], token[1], token[2])
                        self.code_generate(node, v, token[0], token[1])
                        node = v
                        find = True
                        break
                else:
                    if token[0] == w:
                        #print('go', node, v)
                        self.semantic(node, v, token[0], token[1], token[2])
                        self.code_generate(node, v, token[0], token[1])
                        node = v
                        self.need_token = True
                        find = True
                        break
            if not find:
                print('--------------------')
                print("panic mode")
                print('--------------------')
                if token[0] == 'EOF':
                    exit()
            while node == self.nt_dicts[current_nt][1]:
                if current_nt == 'program':
                    self.stack = self.stack[:-1]
                    break
                w = current_nt
                tmp_node = node
                last, node, current_nt = self.stack[-1][0], self.stack[-1][1], self.stack[-1][2]
                #print('back', tmp_node, node)
                self.semantic(last, node, token[0], token[1], token[2])
                self.code_generate(last, node, token[0], token[1])
                self.stack = self.stack[:-1]

            if len(self.stack) == 0:
                break
        for i in range(len(self.program_block)):
            print(i,self.program_block[i])


    def semantic(self, _from, _to, _token, _value, _line):
        #print(_from, _to, _token, _value)
        #print(self.semantic_stack)
        ## additive expression
        if _from == 107 and _to == 106:
            self.semantic_analyzer.push(_token)
        if _from == 106 and _to == 107:
            self.semantic_analyzer.check_op_type(_line)

        ## simple expression
        if _from == 103 and _to == 104:
            self.semantic_analyzer.push(_token)
        if _from == 104 and _to == 105:
            self.semantic_analyzer.check_op_type(_line)

        ## var
        if _from == 98 and _to == 101:
            self.semantic_analyzer.check_id(_line)
        if _from == 99 and _to == 100:
            self.semantic_analyzer.check_array(_line)

        ## expression
        if _from == 133 and _to == 93:
            self.semantic_analyzer.push(_value)
        if _to == 132:
            self.semantic_analyzer.push(_token)
        if _from == 94 and _to == 95:
            self.semantic_analyzer.push('=')
        if _from == 95 and _to == 96:
            self.semantic_analyzer.check_op_type(_line)
        if _to == 128:
            self.semantic_analyzer.push('*')
        if _to == 130:
            self.semantic_analyzer.push(_token)
        if _from == 128 and _to == 127:
            self.semantic_analyzer.check_op_type(_line)
        if _from == 130 and _to == 131:
            self.semantic_analyzer.check_op_type(_line)
        if _from == 132 and _to == 96:
            self.semantic_analyzer.check_op_type(_line)

        ## term
        if _from == 110 and _to == 111:
            self.semantic_analyzer.push('*')
        if _from == 111 and _to == 110:
            self.semantic_analyzer.check_op_type(_line)

        ## while
        if _from == 64 and _to == 65:
            self.semantic_analyzer.check_int(_line)

        ## if
        if _from == 56 and _to == 57:
            self.semantic_analyzer.check_int(_line)

        ## case
        if _from == 76 and _to == 77:
            self.semantic_analyzer.check_int(_line)
        if _from == 85 and _to == 86:
            self.semantic_analyzer.push(_value)

        ## compound_stmt
        if _from == 41 and _to == 42:
            self.semantic_analyzer.increase_scope()
        if _from == 44 and _to == 45:
            self.semantic_analyzer.decrease_scope()

        ## program
        if _from == 0 and _to == 2:
            self.semantic_analyzer.check_main()

        ## declaration
        if _from == 7 and _to == 10:
            self.semantic_analyzer.push(_value)
        if _from == 10 and _to == 11:
            self.semantic_analyzer.push(_value)

        ## var declaration
        if _from == 15 and _to == 16:
            self.semantic_analyzer.scope_search(_line)
            self.semantic_analyzer.insert_array_size(_value, _line)
        if _from == 13 and _to == 14:
            self.semantic_analyzer.scope_search(_line)
            self.semantic_analyzer.insert_id()
            self.semantic_analyzer.check_var_int(_line)

        ## func declaration
        if _from == 21 and _to == 22:
            self.semantic_analyzer.push_line()
            self.semantic_analyzer.insert_function()
            self.semantic_analyzer.increase_scope()
        if _from == 34 and _to == 35:
            self.semantic_analyzer.push(_value)
        if _from == 35 and _to == 36:
            self.semantic_analyzer.push(_value)
            self.semantic_analyzer.scope_search(_line)
        if _from == 38 and _to == 40:
            self.semantic_analyzer.insert_param_id()
        if _from == 38 and _to == 39:
            self.semantic_analyzer.insert_param_array()
        if _from == 24 and _to == 25:
            self.semantic_analyzer.decrease_scope()
            self.semantic_analyzer.finalize_function(_line)
            self.semantic_analyzer.pop_function()

        ## return
        if _from == 70 and _to == 71:
            self.semantic_analyzer.check_func_void(_line)
        if _from == 72 and _to == 71:
            self.semantic_analyzer.check_func_int(_line)

        ## expression stmt
        if _from == 50 and _to == 51 and _token == 'continue':
            self.semantic_analyzer.check_continue(_line)
        if _from == 50 and _to == 51 and _token == 'break':
            self.semantic_analyzer.check_break(_line)
        if _from == 50 and _to == 51 and _token == ';':
            self.semantic_stack.pop()


        ## call
        if _from == 118 and _to == 119:
            self.semantic_analyzer.add_function_count()
            self.semantic_analyzer.check_function(_line)
        if _from == 122 and _to == 123:
            self.semantic_analyzer.check_arg(_line)
        if _from == 120 and _to == 121:
            self.semantic_analyzer.check_args_count(_line)

        ## factor
        if _from == 113 and _to == 134:
            self.semantic_analyzer.push(_value)

    def code_generate(self, _from, _to, _token, _value):
        ## additive expression
        if _from == 106 and _to == 107:
            self.code_generator.op()

        ## simple expression
        if _from == 104 and _to == 105:
            self.code_generator.op()

        ## var
        if _from == 100 and _to == 101:
            self.code_generator.push_array()

        ## expression
        if _from == 133 and _to == 127:
            self.code_generator.push_immediate(_value)
        if _from == 95 and _to == 96:
            self.code_generator.assign()
        if _from == 130 and _to == 131:
            self.code_generator.op()
        if _from == 132 and _to == 96:
            self.code_generator.op()
        if _from == 128 and _to == 127:
            self.code_generator.mult()


        ## term
        if _from == 111 and _to == 110:
            self.code_generator.mult()

        ## while
        if _from == 61 and _to == 62:
            self.code_generator.while_jump()
            self.code_generator.save()
            self.code_generator.label()
            self.while_switch.append(('while', self.semantic_stack[-1]))
        if _from == 64 and _to == 65:
            self.code_generator.save()
        if _from == 65 and _to == 66:
            self.code_generator.finish_while()
            self.while_switch.pop()

        ## if
        if _from == 56 and _to == 57:
            self.code_generator.save()
        if _from == 58 and _to == 59:
            self.code_generator.save()
            self.code_generator.finish_if()
        if _from == 59 and _to == 60:
            self.code_generator.finish_else()

        ## case
        if _from == 76 and _to == 77:
            self.code_generator.save()
            self.while_switch.append(('switch', self.semantic_stack[-1]))
        if _from == 85 and _to == 86:
            self.code_generator.compare()
            self.code_generator.save()
        if _from == 87 and _to == 88:
            self.code_generator.finish_case()
        if _from == 80 and _to == 81:
            self.code_generator.finish_switch()
            self.while_switch.pop()

        ## factor
        if _from == 113 and _to == 116:
            self.code_generator.push_immediate(_value)

        ## program
        if _from == 0 and _to == 2:
            self.code_generator.jump_to_main()

        ## expression stmt
        if _from == 50 and _to == 51 and _token == 'continue':
            self.code_generator.handle_continue()
        if _from == 50 and _to == 51 and _token == 'break':
            self.code_generator.handle_break()

        ## return
        if _from == 72 and _to == 71:
            self.code_generator.return_int()

        ## call
        if _from == 122 and _to == 123:
            self.code_generator.assign_arg()
        if _from == 120 and _to == 121:
            self.code_generator.jump_return()

parser = Parser('test.txt')
parser.parse()