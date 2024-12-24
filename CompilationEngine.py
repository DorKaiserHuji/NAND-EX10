"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.tokenizer = input_stream

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.keyword() != "class":
            raise ValueError("Expected a class declaration")
        self.output_stream.write("<class>\n")
        self.output_stream.write("<keyword> class </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "{":
            raise ValueError("Expected an opening curly bracket.")
        self.output_stream.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        self.compile_class_var_dec()
        self.compile_subroutine()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "}":
            raise ValueError("Expected a closing curly bracket.")
        self.output_stream.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() not in ["static", "field"]:
            return
        self.output_stream.write("<classVarDec>\n")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
            raise ValueError("Expected a type.")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.output_stream.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            if self.tokenizer.token_type() != "IDENTIFIER":
                raise ValueError("Expected an identifier.")
            self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            raise ValueError("Expected a semicolon.")
        self.output_stream.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</classVarDec>\n")
        self.compile_class_var_dec()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
            return
        self.output_stream.write("<subroutineDec>\n")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
            raise ValueError("Expected a type.")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "(":
            raise ValueError("Expected an opening parenthesis.")
        self.output_stream.write("<symbol> ( </symbol>\n")
        self.tokenizer.advance()
        self.compile_parameter_list()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            raise ValueError("Expected a closing parenthesis.")
        self.output_stream.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "{":
            raise ValueError("Expected an opening curly bracket.")
        self.output_stream.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        self.compile_var_dec()
        self.compile_statements()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "}":
            raise ValueError("Expected a closing curly bracket.")
        self.output_stream.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</subroutineDec>\n")
        self.compile_subroutine()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            return
        self.output_stream.write("<parameterList>\n")
        if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
            raise ValueError("Expected a type.")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.output_stream.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
                raise ValueError("Expected a type.")
            self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
            self.tokenizer.advance()
            if self.tokenizer.token_type() != "IDENTIFIER":
                raise ValueError("Expected an identifier.")
            self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        self.output_stream.write("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "var":
            return
        self.output_stream.write("<varDec>\n")
        self.output_stream.write("<keyword> var </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() not in ["KEYWORD", "IDENTIFIER"]:
            raise ValueError("Expected a type.")
        self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.output_stream.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            if self.tokenizer.token_type() != "IDENTIFIER":
                raise ValueError("Expected an identifier.")
            self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            raise ValueError("Expected a semicolon.")
        self.output_stream.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() not in ["let", "if", "while", "do", "return"]:
            return
        self.output_stream.write("<statements>\n")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.key_word() in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.key_word() == "let":
                self.compile_let()
            elif self.tokenizer.key_word() == "if":
                self.compile_if()
            elif self.tokenizer.key_word() == "while":
                self.compile_while()
            elif self.tokenizer.key_word() == "do":
                self.compile_do()
            elif self.tokenizer.key_word() == "return":
                self.compile_return()
        self.output_stream.write("</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "do":
            raise ValueError("Expected a do statement.")
        self.output_stream.write("<doStatement>\n")
        self.output_stream.write("<keyword> do </keyword>\n")
        self.tokenizer.advance()
        self.compile_subroutine_call()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            raise ValueError("Expected a semicolon.")
        self.output_stream.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "let":
            raise ValueError("Expected a let statement.")
        self.output_stream.write("<letStatement>\n")
        self.output_stream.write("<keyword> let </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "IDENTIFIER":
            raise ValueError("Expected an identifier.")
        self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() not in "[=":
            raise ValueError("Expected an opening square bracket or an equal sign.")
        if self.tokenizer.symbol() == "[":
            self.output_stream.write("<symbol> [ </symbol>\n")
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "]":
                raise ValueError("Expected a closing square bracket.")
            self.output_stream.write("<symbol> ] </symbol>\n")
            self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "=":
            raise ValueError("Expected an equal sign.")
        self.output_stream.write("<symbol> = </symbol>\n")
        self.tokenizer.advance()
        self.compile_expression()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            raise ValueError("Expected a semicolon.")
        self.output_stream.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "while":
            raise ValueError("Expected a while statement.")
        self.output_stream.write("<whileStatement>\n")
        self.output_stream.write("<keyword> while </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "(":
            raise ValueError("Expected an opening parenthesis.")
        self.output_stream.write("<symbol> ( </symbol>\n")
        self.tokenizer.advance()
        self.compile_expression()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            raise ValueError("Expected a closing parenthesis.")
        self.output_stream.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "{":
            raise ValueError("Expected an opening curly bracket.")
        self.output_stream.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        self.compile_statements()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "}":
            raise ValueError("Expected a closing curly bracket.")
        self.output_stream.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "return":
            raise ValueError("Expected a return statement.")
        self.output_stream.write("<returnStatement>\n")
        self.output_stream.write("<keyword> return </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            raise ValueError("Expected a semicolon.")
        self.output_stream.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_stream.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        if self.tokenizer.token_type() != "KEYWORD" or self.tokenizer.key_word() != "if":
            raise ValueError("Expected an if statement.")
        self.output_stream.write("<ifStatement>\n")
        self.output_stream.write("<keyword> if </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "(":
            raise ValueError("Expected an opening parenthesis.")
        self.output_stream.write("<symbol> ( </symbol>\n")
        self.tokenizer.advance()
        self.compile_expression()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            raise ValueError("Expected a closing parenthesis.")
        self.output_stream.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "{":
            raise ValueError("Expected an opening curly bracket.")
        self.output_stream.write("<symbol> { </symbol>\n")
        self.tokenizer.advance()
        self.compile_statements()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "}":
            raise ValueError("Expected a closing curly bracket.")
        self.output_stream.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.key_word() == "else":
            self.output_stream.write("<keyword> else </keyword>\n")
            self.tokenizer.advance()
            if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "{":
                raise ValueError("Expected an opening curly bracket.")
            self.output_stream.write("<symbol> { </symbol>\n")
            self.tokenizer.advance()
            self.compile_statements()
            if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "}":
                raise ValueError("Expected a closing curly bracket.")
            self.output_stream.write("<symbol> } </symbol>\n")
            self.tokenizer.advance()
        self.output_stream.write("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        if self.tokenizer.token_type() not in ["INT_CONST", "STRING_CONST", "KEYWORD", "IDENTIFIER", "SYMBOL"]:
            return
        self.output_stream.write("<expression>\n")
        self.compile_term()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in "+-*/&|<>=":
            self.output_stream.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_term()
        self.output_stream.write("</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        if self.tokenizer.token_type() not in ["INT_CONST", "STRING_CONST", "KEYWORD", "IDENTIFIER", "SYMBOL"]:
            return
        self.output_stream.write("<term>\n")
        if self.tokenizer.token_type() == "INT_CONST":
            self.output_stream.write("<integerConstant> {} </integerConstant>\n".format(self.tokenizer.int_val()))
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.output_stream.write("<stringConstant> {} </stringConstant>\n".format(self.tokenizer.string_val()))
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.key_word() in ["true", "false", "null", "this"]:
            self.output_stream.write("<keyword> {} </keyword>\n".format(self.tokenizer.key_word()))
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in "-~":
            self.output_stream.write("<symbol> {} </symbol>\n".format(self.tokenizer.symbol()))
            self.tokenizer.advance()
            self.compile_term()
        elif self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "(":
            self.output_stream.write("<symbol> ( </symbol>\n")
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
                raise ValueError("Expected a closing parenthesis.")
            self.output_stream.write("<symbol> ) </symbol>\n")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "IDENTIFIER":
            self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in "[(":
                if self.tokenizer.symbol() == "[":
                    self.output_stream.write("<symbol> [ </symbol>\n")
                    self.tokenizer.advance()
                    self.compile_expression()
                    if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "]":
                        raise ValueError("Expected a closing square bracket.")
                    self.output_stream.write("<symbol> ] </symbol>\n")
                    self.tokenizer.advance()
                elif self.tokenizer.symbol() == "(":
                    self.output_stream.write("<symbol> ( </symbol>\n")
                    self.tokenizer.advance()
                    self.compile_expression_list()
                    if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
                        raise ValueError("Expected a closing parenthesis.")
                    self.output_stream.write("<symbol> ) </symbol>\n")
                    self.tokenizer.advance()
                elif self.tokenizer.symbol() == ".":
                    self.output_stream.write("<symbol> . </symbol>\n")
                    self.tokenizer.advance()
                    if self.tokenizer.token_type() != "IDENTIFIER":
                        raise ValueError("Expected an identifier.")
                    self.output_stream.write("<identifier> {} </identifier>\n".format(self.tokenizer.identifier()))
                    self.tokenizer.advance()
                    if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != "(":
                        raise ValueError("Expected an opening parenthesis.")
                    self.output_stream.write("<symbol> ( </symbol>\n")
                    self.tokenizer.advance()
                    self.compile_expression_list()
                    if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
                        raise ValueError("Expected a closing parenthesis.")
                    self.output_stream.write("<symbol> ) </symbol>\n")
                    self.tokenizer.advance()
        self.output_stream.write("</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            return
        self.output_stream.write("<expressionList>\n")
        self.compile_expression()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
            self.output_stream.write("<symbol> , </symbol>\n")
            self.tokenizer.advance()
            self.compile_expression()
        self.output_stream.write("</expressionList>\n")