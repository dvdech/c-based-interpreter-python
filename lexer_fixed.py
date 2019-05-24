import re
import sys

# counter to avoid int assignment to token classifiers
def Counter():
    i = 0
    while True:
        yield i
        i += 1


class Lexer:
    """
    The Lexer class analyzes Clite tokens
    """


    # Constants that represent token classifiers
    cnt = Counter()
    FILENOTFOUND    = next(cnt) # similar to enums in Java or C/C++
    ILLEGALTOKEN    = [next(cnt), 'Illegal-Token']
    EOF             = next(cnt)
    INVALIDFILENAME = next(cnt)

    ID              = [next(cnt), 'Identifier']
    INTLIT          = next(cnt), "Int-Literal"
    FLOATLIT        = next(cnt), "Float-Literal"
    STRLIT          = [next(cnt), 'String-Literal']
    INT             = [next(cnt), 'Int']
    CMT             = next(cnt)
    REAL            = [next(cnt), 'Float-Literal']

    # operator constants
    OR              = next(cnt)
    PLUS            = next(cnt)
    MINUS           = next(cnt)
    LESS            = next(cnt)
    LESSEQ          = next(cnt)
    AND             = next(cnt)
    EQUAL           = next(cnt)
    NOTEQUAL        = next(cnt)
    GREATER         = next(cnt)
    GREATEREQ       = next(cnt)
    MUL             = next(cnt)
    DIV             = next(cnt)
    MOD             = next(cnt)
    LOGNOT          = next(cnt)

    # keyword constants
    KWDPRINT        = next(cnt)
    KWDBOOL         = next(cnt)
    KWDELSE         = next(cnt)
    KWDFALSE        = next(cnt)
    KWDIF           = next(cnt)
    KWDTRUE         = next(cnt)
    KWDFLOAT        = next(cnt)
    KWDINT          = next(cnt)
    KWDWHILE        = next(cnt)

    # punctuation constants
    PUNSEMICOL      = next(cnt)
    PUNCOMMA        = next(cnt)
    PUNLEFTCURLBRK  = next(cnt)
    PUNRIGHTCURLBRK = next(cnt)
    PUNLEFTPAREN    = next(cnt)
    PUNRIGHTPAREN   = next(cnt)


    # precompile the regex of patterns
    # to split tokens on.

    # filter for string literal
    strlit_patt = re.compile("\".*\"|\s$")

    # filter for comments
    cmt_patt = re.compile("//")

    # help organize output for tokens
    ky = 'Keyword'


    # split patter to capture specific tokens in the text file
    split_patt = re.compile(

        """
        \s   |    # whitespace
        (//) |    # cmt characters
        (\|\|)|   # operator ||
        (\+) |    # operator +
        (\-) |    # operator -
        (<=) |    # operator <=
        (<)  |    # operator <
        (&&) |    # operator &&
        (==) |    # operator ==
        (!=) |    # operator !=
        (>=) |    # operator >
        (>)  |    # operator >=
        (\*) |    # operator *
        (/)  |    # operator /
        (%)  |    # operator %
        (!)  |    # operator !
        (;)  |    # punctuation ;
        (,)  |    # punctuation ,
        (})  |    # punctuation {
        (\{) |    # punctuation }
        (\() |    # punctuation (
        (\)) |    # punctuation )
        (\".*\"|\s$)  # string literal




        """,
        re.VERBOSE
    )

    ## Regex expression to capture token that satisfy specific properties ##

    # regular expression (regex) for an identifier
    id_patt = re.compile("^[=a-zA-Z][a-zA-Z0-9_]*$")    # should id's be able to start with _

    # regular expression (regex) for an integer
    int_patt = re.compile("^[0-9][0-9]*$")

    # regular expression (regex) for an real number
    realnum_patt = re.compile("^([0-9])+(\.)(\d*)$")

    # token dictionary
    td = {
        '//':            CMT,
        '||':             [OR, 'Or'],
        '+':            [PLUS, 'Plus'],
        '-':           [MINUS, 'Minus'],
        '<':            [LESS, 'Less'],
        '<=' :        [LESSEQ, 'Less-Equal'],
        '&&':            [AND, 'And'],
        '==':          [EQUAL, 'Equal'],
        '!=' :      [NOTEQUAL, 'Not-Equal'],
        '>':         [GREATER, 'Greater'],
        '>=':      [GREATEREQ, 'Greater-Equal'],
        '*':             [MUL, 'Multiply'],
        '/':             [DIV, 'Divide'],
        '%':             [MOD, 'Modul'],
        '!':          [LOGNOT, 'Logical-Not'],
        ';':      [PUNSEMICOL,'Semi-Col'],
        ',':        [PUNCOMMA, 'Comma'],
        '{':  [PUNLEFTCURLBRK, 'Left-Curly-Brace'],
        '}': [PUNRIGHTCURLBRK, 'Right-Curly-Brace'],
        '(':    [PUNLEFTPAREN, 'Left-Paren'],
        ')':    [PUNRIGHTPAREN, 'Right-Paren'],
    }

    # keyword dictionary
    kwd = {
        'print': [KWDPRINT, ky],
        'bool':   [KWDBOOL, ky],
        'else':   [KWDELSE, ky],
        'false': [KWDFALSE, ky],
        'if':       [KWDIF, ky],
        'true':   [KWDTRUE, ky],
        'float': [KWDFLOAT, ky],
        'int':     [KWDINT, ky],
        'while':  [KWDWHILE, ky],
        'main':  [KWDWHILE, ky]
    }

    def token_generator(self, argv):

        # try to open the file
        # if not determine which error to throw
        # either invalid file name or specific file could not be found
        try:
            file = open(argv)
        except FileNotFoundError("File could not be located"):
            yield (Lexer.FILENOTFOUND, argv)
        except ValueError("Invalid file name"):
            yield (Lexer.INVALIDFILENAME, argv)


        # keep track of line number
        line_num = 0

        # Read each line
        for line in file:

            # check for entire line comments and void them
            if line.startswith('//'):
                line = line[-1:0] # pass over comment line

            # increment line number
            line_num += 1

            # get individual tokens per line
            tokens = Lexer.split_patt.split(line)
            tokens = [t for t in tokens if t]

            # loop through each individual token
            for t in tokens:

                # check for comments that arent entire lines
                if t == '//':
                    break

                ## CHECK WHICH TOKEN IS BEING CLASSIFIED ##

                elif t in Lexer.td:
                    yield (Lexer.td[t][1], t, line_num)

                elif Lexer.strlit_patt.match(t):
                   yield (Lexer.STRLIT[1], t, line_num)

                elif Lexer.id_patt.search(t):
                    if t in Lexer.kwd:
                        yield (Lexer.kwd[t][1], t, line_num)
                    else:
                        yield (Lexer.ID[1], t, line_num)

                elif Lexer.int_patt.search(t):
                    yield (Lexer.INT[1], t, line_num)

                elif Lexer.realnum_patt.search(t):
                    yield (Lexer.REAL[1], t, line_num)

                else:
                    yield (Lexer.ILLEGALTOKEN[1], t, line_num)


# test main
if __name__ == "__main__":

    print(sys.argv[0])
    # use sys.argv to get command line inputs
    f = "lexertest.c"

    # more then 1 argument passed
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments passed: Expect only 1.")

    # create lexer argument
    lex = Lexer()
    tg = lex.token_generator(f)

    # while possible print each new token with specified classifiers
    # when impossible return specific error: either end of file or
    # unexpected token (if not handled by ILLEGALTOKEN output above)
    while True:
        try:
            tok = next(tg)
            print(tok)
        except StopIteration:
            print("End of File" + ": " + str(Lexer.EOF) + "(EOF Code)")
            break
        except ValueError("Unrecognized token on line"):
            print("Invalid token" + tok)
            break