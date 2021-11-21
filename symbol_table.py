class Symbol(object):
    def __init__(self, name, address, typ, length, line, args):
        self.address = address
        self.typ = typ
        self.length = length
        self.name = name
        self.line = line
        self.args = args

    def __str__(self):
        return self.name

class SymbolTable(object):
    def __init__(self):
        self.rows = []
        self.stack = []
        self.stack.append(-1)

    def increase_scope(self):
        self.stack.append(len(self.rows) - 1)

    def decrease_scope(self):
        self.rows = self.rows[:self.stack[-1] + 1]
        self.stack = self.stack[:-1]

    def scope_search(self, name):
        for i in range(len(self.rows) - 1, self.stack[-1], -1):
            if self.rows[i].name == name:
                return self.rows[i]
        return None

    def get_list_scope_search(self, name):
        ret = []
        for i in range(len(self.rows) - 1, self.stack[-1], -1):
            if self.rows[i].name == name:
                ret.append(self.rows[i])
        return ret

    def all_search(self, name):
        for i in range(len(self.rows) - 1, -1, -1):
            if self.rows[i].name == name:
                return self.rows[i]
        return None

    def insert(self, name, address = None, typ = None, length = None, line = None, args = None):
        symbol = Symbol(name, address, typ, length, line, args)
        self.rows.append(symbol)

    def get_index(self, element):
        for i in range(len(self.rows) - 1, -1, -1):
            if self.rows[i] == element:
                return i
        return None

    def get_element(self, index):
        return self.rows[index]


    def __str__(self):
        ret = ""
        for i in self.rows:
            ret += i.name
            ret += " "
        return ret