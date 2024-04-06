
MAX_CONSTANTS = 10
totalConstants = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
availableConstants = []
usedConstantsDict = {}

def tokenize(fmla):
    tokens = []
    i = 0
    while i < len(fmla):
        if fmla[i] in ["p","q","r","s"]:
                tokens.append(["PROP",fmla[i]])
                i += 1
        elif i < len(fmla)-5 and fmla[i] in ["P", "Q", "R", "S"]:
            if fmla[i+1] == "(" and (fmla[i+2] in ["x","y","w","z"] or fmla[i+2] in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]) and fmla[i+3] == "," and (fmla[i+4] in ["x","y","w","z"] or fmla[i+4] in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]) and fmla[i+5] == ")":
                tokens.append(["PREDICATE", fmla[i:i+6], fmla[i+2], fmla[i+4]])
                i += 6
            else:
                return False
        elif fmla[i] == "~":
            tokens.append(["NEGATION", fmla[i]])
            i += 1
        elif fmla[i] == "(":
            tokens.append(["LEFT", fmla[i]])
            i += 1
        elif fmla[i] == ")":
            tokens.append(["CLOSE", fmla[i]])
            i += 1
        elif i < len(fmla) - 1 and fmla[i:i+2] in ["=>", "\/", "/\\"]:
            tokens.append(["CONNECTIVE", fmla[i:i+2]])
            i += 2
        elif fmla[i] in ["A","E"]:
            if fmla[i+1] in ["x","y","w","z"] or fmla[i+1] in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]:
                tokens.append(["QUANTIFIER", fmla[i:i+2], fmla[i+1]])
                i += 2
        # elif fmla[i] in ["a","b","c","d","e","f","g","h","i","j"]:
        #     tokens.append(["CONSTANT", fmla[i]])
        #     i += 1
        else:
            return False
    
    if tokens.count(["LEFT", "("]) != tokens.count(["CLOSE", ")"]):
        return False
    
    return tokens

def tokenToString(tokens):
    string = ""
    for token in tokens:
        string += token[1]
    return string

# returns True if formula is FOL, False if formula is propositional logic.
def isFOL(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "PREDICATE":
            return True
        elif tokens[i][0] == "PROP":
            return False
        else:
            i += 1
    
#finding the index of the main connective
def findMiddleConnectiveIndex(tokens):
    leftCount = 0
    for i in range(len(tokens)):
        if tokens[i][0] == "CONNECTIVE" and leftCount == 1:
            return i
        elif tokens[i][0] == "LEFT":
            leftCount += 1
        elif tokens[i][0] == "CLOSE":
            leftCount -= 1
        else:
            continue
    return -1

#build a string of the RHS of the formula
def rhsTokens(tokens):
    rhsFormula = ""
    conIndex = findMiddleConnectiveIndex(tokens) 
    for token in tokens[conIndex+1:len(tokens)-1]:
        rhsFormula += token[1]
    return rhsFormula

def lhsTokens(tokens):
    lhsFormula = ""
    conIndex = findMiddleConnectiveIndex(tokens) 
    for token in tokens[1:conIndex]:
        lhsFormula += token[1]
    return lhsFormula

# Return the LHS of a binary connective formula
def lhs(fmla):
    tokens = tokenize(fmla)
    lhsFormula = ""
    conIndex = findMiddleConnectiveIndex(tokens) 
    for token in tokens[1:conIndex]:
        lhsFormula += token[1]
    return lhsFormula
    
def lhsUsingTokens(tokens):
    conIndex = findMiddleConnectiveIndex(tokens)
    if conIndex == -1:
        return None
    else:
        return tokens[1:conIndex]

# Return the connective symbol of a binary connective formula
def con(fmla):
    tokens = tokenize(fmla)
    conIndex = findMiddleConnectiveIndex(tokens)
    if conIndex == -1:
        return None
    else:
        return tokens[conIndex][1]
    

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    tokens = tokenize(fmla)
    rhsFormula = ""
    conIndex = findMiddleConnectiveIndex(tokens) 
    for token in tokens[conIndex+1:len(tokens)-1]:
        rhsFormula += token[1]
    return rhsFormula
    
def rhsUsingTokens(tokens):
    conIndex = findMiddleConnectiveIndex(tokens)
    if conIndex == -1:
        return None
    else:
        return tokens[conIndex+1:len(tokens)-1]

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    if tokenize(fmla) == False:
        return 0
    else:
        tokens = tokenize(fmla)
        return parseFormula(tokens)

def parseFormula(tokens):
    if len(tokens) == 0:
        return 0
    
    elif len(tokens) == 1:
        if tokens[0][0] == "PROP":
            return 6
        elif tokens[0][0] == "PREDICATE":
            return 1
        else:
            return 0
    
    elif tokens[0][0] == "NEGATION":
        tokens.pop(0)
        if parseFormula(tokens) == 0:
            return 0
        elif isFOL(tokens):
            return 2
        else:
            return 7
    # FOL: existential quantifiers
    elif tokens[0][0] == "QUANTIFIER" and tokens[0][1][0] == "E":
        tokens.pop(0)
        if parseFormula(tokens) == 0:
            return 0
        else:
            return 4
        
    # FOL: universal quantifiers
    elif tokens[0][0] == "QUANTIFIER" and tokens[0][1][0] == "A":
        tokens.pop(0)
        if parseFormula(tokens) == 0:
            return 0
        else:
            return 3
        
    # brackets
    elif tokens[0][0] == "LEFT":
        index = findMiddleConnectiveIndex(tokens)
        if index == -1 or parseFormula(lhsUsingTokens(tokens)) == 0 or parseFormula(rhsUsingTokens(tokens)) == 0:
            return 0
        elif isFOL(tokens):
            return 5
        else:
            return 8
    # random characters-even though this is not needed
    else:
        return 0



# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return [fmla]

def fullyExpanded(theory):
    for formula in theory:
        if 'A' not in formula and 'E' not in formula and '/\\' not in formula and '\/' not in formula and '=>' not in formula:
            continue
        else:
            return False
    return True
            
def isContradiction(theory):
    for formula in theory:
        if formula[0] == '~' and formula[1:] in theory:
            return True
        if '~' + formula in theory:
            return True
    return False

def handleNegations(tokens):
    negation = False
    while tokens[0][0] == "NEGATION":
        tokens.pop(0)
        negation = not negation
    return negation

def handleAlphaFormula(tokens, theory, tableau, conIndex):
    rhsFormula = lhsFormula = ""
    if tokens[conIndex][1] == "=>":
        lhsFormula = lhsTokens(tokens)
        rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]
    elif tokens[conIndex][1] == "/\\": 
        lhsFormula = lhsTokens(tokens)
        rhsFormula = rhsTokens(tokens)
    elif tokens[conIndex][1] == "\/":
        lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
        rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]
    theory.append(lhsFormula)
    theory.append(rhsFormula)
    tableau.append(theory)
    return tableau

def handleBetaFormula(tokens, theory, tableau, conIndex):
    lhsFormula = rhsFormula = ""
    if tokens[conIndex][1] == "=>":
        lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
        rhsFormula = rhsTokens(tokens)
    elif tokens[conIndex][1] == "/\\": 
        lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
        rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]
    elif tokens[conIndex][1] == "\/":
        lhsFormula = lhsTokens(tokens)
        rhsFormula = rhsTokens(tokens)
    newTheory = theory.copy()
    theory.append(lhsFormula)    
    newTheory.append(rhsFormula)
    tableau.append(theory)
    tableau.append(newTheory)
    return tableau

def handleDeltaFormula(tokens, theory, tableau):
    global availableConstants
    global totalConstants

    quantifierToken = tokens.pop(0)
    variable = quantifierToken[2]

    if quantifierToken[1][0] == "A":
        if totalConstants:
            if tokens[0][0] == "LEFT" or tokens[0][0] == "PREDICATE":
                tokens.insert(0, ["NEGATION", "~"])
            elif tokens[0][0] == "NEGATION":
                tokens.pop(0)
        
    if totalConstants:
        constant = totalConstants.pop(0)
        availableConstants.append(constant)            
        for token in tokens:
            if token[0] == "PREDICATE":
                token[2] = constant if token [2] == variable else token[2]
                token[3] = constant if token[3] == variable else token[3]
                token[1] = token[1][0] + "(" + token[2] + "," + token[3] + ")"
            elif token[0] == "QUANTIFIER":
                token[2] = constant
                token[1] = token[1][0] + token[2]
        theory.append(tokenToString(tokens))
        tableau.append(theory)
    return tableau

def deltaChecker(fmla):
    #return (fmla[0] == "A" and (parse(fmla[2:]) == 1 or gammaChecker(fmla[2:]))) or ((fmla[0] == "~" and fmla[1] == "E") and (parse(fmla[3:] == 1) or gammaChecker(fmla[3:])))
    #~~A(~E)
    tokens = tokenize(fmla)
    negation = handleNegations(tokens)
    
    if (tokens[0][1][0] == "E" and negation == False) or (tokens[0][1][0] == "A" and negation == True):
        return True
    
    if len(tokens) <= 2:
        return False

    else:
        if (tokens[0][1][0] == "E" and negation == True) or (tokens[0][1][0] == "A" and negation == False):
            tokens.pop(0)
            return deltaChecker(tokenToString(tokens))
        else:
            #~(P(x,x)=>P(x,x))
            conIndex = findMiddleConnectiveIndex(tokens)
            lhsFormula = rhsFormula = ""

            if ((tokens[conIndex][1] == "=>" and negation == True) or (tokens[conIndex][1] == "/\\" and negation == False)
            or (tokens[conIndex][1] == "\/" and negation == True)):
                if tokens[conIndex][1] == "=>":
                    lhsFormula = lhsTokens(tokens)
                    rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]
                elif tokens[conIndex][1] == "/\\": 
                    lhsFormula = lhsTokens(tokens)
                    rhsFormula = rhsTokens(tokens)
                elif tokens[conIndex][1] == "\/":
                    lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
                    rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]

            elif ((tokens[conIndex][1] == "=>" and negation == False) or (tokens[conIndex][1] == "/\\" and negation == True) 
            or (tokens[conIndex][1] == "\/" and negation == False)):
                if tokens[conIndex][1] == "=>":
                    lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
                    rhsFormula = rhsTokens(tokens)
                elif tokens[conIndex][1] == "/\\": 
                    lhsFormula = "~" + lhsTokens(tokens) if lhsTokens(tokens)[0] != "~" else lhsTokens(tokens)[1:]
                    rhsFormula = "~" + rhsTokens(tokens) if rhsTokens(tokens)[0] != "~" else rhsTokens(tokens)[1:]
                elif tokens[conIndex][1] == "\/":
                    lhsFormula = lhsTokens(tokens)
                    rhsFormula = rhsTokens(tokens)
                
            return deltaChecker(rhsFormula) or deltaChecker(lhsFormula)


def handleGammaFormula(tokens, theory, tableau, formula):
    global availableConstants
    global usedConstantsDict

    quantifierToken = tokens.pop(0)
    variable = quantifierToken[2]
    if formula not in usedConstantsDict:
        usedConstantsDict[formula] = []

    if availableConstants:
        deltaExists = True
        for i in range(len(availableConstants)):
            constant = availableConstants[i]
            if constant not in usedConstantsDict[formula]:
                if quantifierToken[1][0] == "E":
                    if tokens[0][0] == "LEFT" or tokens[0][0] == "QUANTIFIER":
                        tokens.insert(0, ["NEGATION", "~"])
                    elif tokens[0][0] == "NEGATION":
                        tokens.pop(0)
                
                for token in tokens:
                    if token[0] == "PREDICATE":
                        first = constant if token[2] == variable else token[2]
                        second = constant if token[3] == variable else token[3]
                        token[1] = token[1][0] + "(" + first + "," + second + ")"
                theory.append(tokenToString(tokens))
                usedConstantsDict[formula].append(constant)
            else:
                deltaExists = False
                theory.append(formula)
                for fmla in theory:
                    if deltaChecker(fmla):
                        deltaExists = True
                        break
                theory.pop()

        if len(usedConstantsDict[formula]) < 10 and deltaExists:
            theory.append(formula)
        tableau.append(theory)
    else:
        theory.append(formula)
    return tableau

def handleDeltaGamma(tokens, theory, tableau, negation, formula):
    if (tokens[0][1][0] == "A" and negation == False) or (tokens[0][1][0] == "E" and negation == True):
        return handleGammaFormula(tokens, theory, tableau, formula)
    elif (tokens[0][1][0] == "E" and negation == False) or (tokens[0][1][0] == "A" and negation == True):
        return handleDeltaFormula(tokens, theory, tableau)

def handleAlphaBeta(tokens, theory, tableau, negation):
    conIndex = findMiddleConnectiveIndex(tokens)
    #handle alpha formulas
    if ((tokens[conIndex][1] == "=>" and negation == True) or (tokens[conIndex][1] == "/\\" and negation == False)
    or (tokens[conIndex][1] == "\/" and negation == True)):
        return handleAlphaFormula(tokens, theory, tableau, conIndex)
    #handle beta formulas
    elif ((tokens[conIndex][1] == "=>" and negation == False) or (tokens[conIndex][1] == "/\\" and negation == True) 
    or (tokens[conIndex][1] == "\/" and negation == False)):
        return handleBetaFormula(tokens, theory, tableau, conIndex)
#swap gamma formulas to the end of the theory when there is no available constant
def swapGammaFormula(theory):
    if not availableConstants:
        negation = False
        fmla = theory.pop(0)
        tokens = tokenize(fmla)
        if tokens[0][0] == "NEGATION":
            negation = handleNegations(tokens)
        if tokens[0][0] == "QUANTIFIER":
            if (tokens[0][1][0] == "A" and negation == False) or (tokens[0][1][0] == "E" and negation == True):
                theory.append(fmla)
                return theory
            else:
                theory.insert(0, fmla)
                return theory
        else:
            theory.insert(0, fmla)
            return theory
    else: 
        return theory
#switch case for different formula types
def switchFormulas(theory, tableau):
    negation = False
    theory = swapGammaFormula(theory)
    formula = theory.pop(0)
    tokens = tokenize(formula)
    
    if tokens[0][0] == "NEGATION":
        negation = handleNegations(tokens)

    firstToken = tokens[0][0]
    if firstToken == "QUANTIFIER":
        return handleDeltaGamma(tokens, theory, tableau, negation, formula)
    elif firstToken == "LEFT":
        return handleAlphaBeta(tokens, theory, tableau, negation)
    else:
        if isContradiction(theory):
            return tableau
        else:
            theory.append(formula)
            tableau.append(theory)
            return tableau
#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    global availableConstants
    global totalConstants
    global usedConstantsDict

    while tableau:
        #theory is the first branch in the tableau
        theory = tableau.pop(0)
        if fullyExpanded(theory):
            if not isContradiction(theory):
                totalConstants = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
                availableConstants = []
                usedConstantsDict = {}
                return 1
        else:
            tableau = switchFormulas(theory, tableau)
            if availableConstants and len(availableConstants) >= MAX_CONSTANTS:
                totalConstants = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
                availableConstants = []
                usedConstantsDict = {}
                return 2
    availableConstants = []
    totalConstants = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    usedConstantsDict = {}
    return 0

#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
