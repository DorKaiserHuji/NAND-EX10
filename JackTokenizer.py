"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

_SYMBOL_LIST = '{}()[].,;+-*/&|<>=~^#'  # All symbols in the Jack language.


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        self.input_lines = input_stream.read().splitlines()
        self.comment_removal()
        self.input = ' '.join(self.input_lines)
        self.current_token = ''
        self.input_index = 0

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self.input_index < len(self.input)

    def advance(self) -> typing.Generator:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        while self.input_index < len(self.input):
            if self.current_token in _SYMBOL_LIST and self.current_token != '':
                yield self.current_token
                self.current_token = ''
            if self.input[self.input_index] in _SYMBOL_LIST:
                if self.current_token != '':
                    yield self.current_token
                    self.current_token = ''
                self.current_token = self.input[self.input_index].strip()
                if self.current_token in _SYMBOL_LIST and self.current_token != '':
                    yield self.current_token
                    self.current_token = ''
                    self.input_index += 1
            if self.input[self.input_index]  == '"' or self.current_token == '"':
                self.current_token = self.input[self.input_index]
                self.input_index += 1
                while self.input[self.input_index] != '"':
                    self.current_token += self.input[self.input_index]
                    self.input_index += 1
                self.current_token += self.input[self.input_index]
                yield self.current_token
                self.current_token = ''
                self.input_index += 1

            if self.input[self.input_index] == ' ' or self.input[self.input_index] == '\t' or self.input[
                self.input_index] == '\n':
                if self.current_token != '':
                    yield self.current_token
                    self.current_token = ''
                self.input_index += 1

            self.current_token += self.input[self.input_index].strip()
            self.input_index += 1

        yield self.current_token

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        match self.current_token:
            case 'class':
                return 'KEYWORD'
            case 'constructor':
                return 'KEYWORD'
            case 'function':
                return 'KEYWORD'
            case 'method':
                return 'KEYWORD'
            case 'field':
                return 'KEYWORD'
            case 'static':
                return 'KEYWORD'
            case 'var':
                return 'KEYWORD'
            case 'int':
                return 'KEYWORD'
            case 'char':
                return 'KEYWORD'
            case 'boolean':
                return 'KEYWORD'
            case 'void':
                return 'KEYWORD'
            case 'true':
                return 'KEYWORD'
            case 'false':
                return 'KEYWORD'
            case 'null':
                return 'KEYWORD'
            case 'this':
                return 'KEYWORD'
            case 'let':
                return 'KEYWORD'
            case 'do':
                return 'KEYWORD'
            case 'if':
                return 'KEYWORD'
            case 'else':
                return 'KEYWORD'
            case 'while':
                return 'KEYWORD'
            case 'return':
                return 'KEYWORD'
            case '{':
                return 'SYMBOL'
            case '}':
                return 'SYMBOL'
            case '(':
                return 'SYMBOL'
            case ')':
                return 'SYMBOL'
            case '[':
                return 'SYMBOL'
            case ']':
                return 'SYMBOL'
            case '.':
                return 'SYMBOL'
            case ',':
                return 'SYMBOL'
            case ';':
                return 'SYMBOL'
            case '+':
                return 'SYMBOL'
            case '-':
                return 'SYMBOL'
            case '*':
                return 'SYMBOL'
            case '/':
                return 'SYMBOL'
            case '&':
                return 'SYMBOL'
            case '|':
                return 'SYMBOL'
            case '<':
                return 'SYMBOL'
            case '>':
                return 'SYMBOL'
            case '=':
                return 'SYMBOL'
            case '~':
                return 'SYMBOL'
            case '^':
                return 'SYMBOL'
            case '#':
                return 'SYMBOL'
        if self.current_token.isdigit():
            return 'INT_CONST'
        if self.current_token.startswith('"'):
            return 'STRING_CONST'
        return 'IDENTIFIER'

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        match self.current_token:
            case 'class':
                return 'CLASS'
            case 'constructor':
                return 'CONSTRUCTOR'
            case 'function':
                return 'FUNCTION'
            case 'method':
                return 'METHOD'
            case 'field':
                return 'FIELD'
            case 'static':
                return 'STATIC'
            case 'var':
                return 'VAR'
            case 'int':
                return 'INT'
            case 'char':
                return 'CHAR'
            case 'boolean':
                return 'BOOLEAN'
            case 'void':
                return 'VOID'
            case 'true':
                return 'TRUE'
            case 'false':
                return 'FALSE'
            case 'null':
                return 'NULL'
            case 'this':
                return 'THIS'
            case 'let':
                return 'LET'
            case 'do':
                return 'DO'
            case 'if':
                return 'IF'
            case 'else':
                return 'ELSE'
            case 'while':
                return 'WHILE'
            case 'return':
                return 'RETURN'
        raise ValueError('Invalid keyword')

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if self.current_token in _SYMBOL_LIST:
            return self.current_token
        raise ValueError('Invalid symbol')

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        return self.current_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        return int(self.current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        return self.current_token[1:-1]

    def comment_removal(self) -> None:
        """Removes comments from the input lines."""
        i = 0
        while i < len(self.input_lines):
            self.input_lines[i] = self.input_lines[i].strip()
            if self.input_lines[i].strip().find('//') != -1:
                self.input_lines[i] = self.input_lines[i][:self.input_lines[i].find('//')]
            if len(self.input_lines[i]) == 0:
                self.input_lines.remove(self.input_lines[i])
            elif self.input_lines[i].startswith('/*') or self.input_lines[i].startswith('/**'):
                if self.input_lines[i].endswith('*/'):
                    self.input_lines.remove(self.input_lines[i])
                    continue
                while not self.input_lines[i].endswith('*/'):
                    self.input_lines.remove(self.input_lines[i])
                self.input_lines.remove(self.input_lines[i])
            elif self.input_lines[i] == '':
                self.input_lines.remove(self.input_lines[i])
            else:
                i += 1
