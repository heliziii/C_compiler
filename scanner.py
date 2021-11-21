class Scanner(object):

    KEYWORD = ["EOF", "void", "continue", "break", "if", "while", "return", "switch", "case", "default", "else", "int"]
    SKIP_CHAR = [' ', '\n', '\t', '\r']

    def __init__(self, source_code):
        self.code = source_code
        self.pointer = 0
        self.pre_token = None
        self.line = 1

    def get_token(self):
        while True:
            if self.pointer >= len(self.code):
                return "Done", "Done", self.line
            current_char = self.code[self.pointer]
            if current_char.isalpha():
                word = current_char
                self.pointer += 1
                while self.pointer != len(self.code) and (self.code[self.pointer].isalpha() or self.code[self.pointer].isdigit()):
                    word += self.code[self.pointer]
                    self.pointer += 1
                if word in Scanner.KEYWORD:
                    self.pre_token = word
                    return word, word, self.line
                else:
                    self.pre_token = 'ID'
                    return 'ID', word, self.line

            ##number
            elif current_char.isdigit():
                digit = current_char
                self.pointer += 1
                while self.pointer != len(self.code) and self.code[self.pointer].isdigit():
                    digit += self.code[self.pointer]
                    self.pointer += 1
                self.pre_token = 'NUM'
                return 'NUM', int(digit), self.line

            ##badihi
            elif current_char in ["(", ")", "[", "]", ";", "<", "{", "}", ":", "*", ","]:
                self.pre_token = current_char
                self.pointer += 1
                return current_char, current_char, self.line

            ## == and =
            elif current_char == "=":

                if self.pointer + 1 != len(self.code) and self.code[self.pointer + 1] == "=":
                    self.pointer += 2
                    self.pre_token = "=="
                    return "==", "=="
                else:
                    self.pointer += 1
                    self.pre_token = current_char
                    return current_char, current_char, self.line

            ##+,-
            elif current_char == "+" or current_char == "-":
                if self.pre_token == "]" or self.pre_token == ")" or self.pre_token == "NUM" or self.pre_token == "ID":
                    self.pre_token = current_char
                    self.pointer += 1
                    return current_char, current_char, self.line
                else:
                    if self.pointer + 1 != len(self.code) and self.code[self.pointer + 1].isdigit():
                        num = current_char
                        self.pointer += 1
                        while self.pointer != len(self.code) and self.code[self.pointer].isdigit():
                            num += self.code[self.pointer]
                            self.pointer += 1
                        self.pre_token = 'NUM'
                        self.pointer += 1
                        return 'NUM', int(num), self.line

            elif current_char == "/":
                if self.pointer + 1 != len(self.code) and self.code[self.pointer + 1] == "*":
                    self.pointer += 2
                    while self.code[self.pointer] != "*":
                        self.pointer += 1
                    if self.pointer == len(self.code) or (self.pointer + 1 < len(self.code) and self.code[self.pointer + 1] != '/'):
                        print("/* doesn't terminate")
                    self.pointer += 2
                else:
                    print("error unknown /")
                    self.pointer += 1

            elif current_char in Scanner.SKIP_CHAR:
                self.pointer += 1
                if current_char == '\n':
                    self.line += 1

            else:
                print(current_char)
                print("error, unknown character")
                return None, None, self.line

