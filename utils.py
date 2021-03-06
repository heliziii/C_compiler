FIRST = {'program': ['EOF', 'int', 'void'],
         'declaration-list': ['eps', 'int', 'void'],
         'declaration': ['int', 'void'],
		 'var-declaration': ['int', 'void'],
		 'P_var-declaration': [';', '['],
		 'type-specifier': ['int', 'void'],
		 'fun-declaration': ['('],
		 'params': ['int', 'void'],
		 'param-list': ['int'],
		 'R_param-list': [',', 'eps'],
		 'param': ['int'],
		 'P_param': ['[', 'eps'],
		 'compound-stmt': ['{'],
		 'statement-list': ['eps', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM'],
		 'statement': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM'],
		 'expression-stmt': ['continue', 'break', ';', 'ID', '(', 'NUM'],
		 'selection-stmt': ['if'],
		 'iteration-stmt': ['while'],
		 'return-stmt': ['return'],
		 'R': [';', 'ID', '(', 'NUM'],
		 'switch-stmt': ['switch'],
		 'case-stmts': ['case', 'eps'],
		 'case-stmt': ['case'],
		 'default-stmt': ['default', 'eps'],
		 'expression': ['ID', '(', 'NUM'],
		 'var': ['[', 'eps'],
		 'simple-expression': ['ID', '(', 'NUM'],
		 'additive-expression': ['ID', '(', 'NUM'],
		 'term': ['ID', '(', 'NUM'],
		 'factor': ['ID', '(', 'NUM'],
		 'call': ['('],
		 'args': ['ID', '(', 'NUM', 'eps'],
		 'arg-list': ['ID', '(', 'NUM']
         }

FOLLOW = {'program': ['$'],
         'declaration-list': ['EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}'],
         'declaration': ['int', 'void', 'EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}'],
		 'var-declaration': ['int', 'void', 'EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}'],
		 'P_var-declaration': ['int', 'void', 'EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}'],
		 'type-specifier': ['ID'],
		 'fun-declaration': ['int', 'void', 'EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}'],
		 'params': [')'],
		 'param-list': [')'],
		 'R_param-list': [')'],
		 'param': [',', ')'],
		 'P_param': [',', ')'],
		 'compound-stmt': ['int', 'void', 'EOF', '{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'statement-list': ['}', 'case', 'default'],
		 'statement': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'expression-stmt': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'selection-stmt': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'iteration-stmt': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'return-stmt': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'R': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'switch-stmt': ['{', 'continue', 'break', ';', 'if', 'while', 'return', 'switch', 'ID', '(', 'NUM', '}', 'else', 'case', 'default'],
		 'case-stmts': ['default', '}'],
		 'case-stmt': ['case', 'default', '}'],
		 'default-stmt': ['}'],
		 'expression': [';', ')', ']', ','],
		 'var': ['=', '*', '+', '-', '<', '==', ';', ')', '*', ']', ','],
		 'simple-expression': [';', ')', ']', ','],
		 'additive-expression': ['<', '==', ';', ')', ']', ','],
		 'term': ['+', '-', '<', '==', ';', ')', '*', ']', ','],
		 'factor': ['+', '-', '<', '==', ';', ')', '*', ']', ','],
		 'call': ['+', '-', '<', '==', ';', ')', '*', ']', ','],
		 'args': [')'],
		 'arg-list': [')']
         }








