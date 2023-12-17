from typing import Tuple
import re

def check_constraint(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip('\n ')
    if constraint.find(r' or ') != -1:
        return Or(constraint, sequence)
    elif constraint.find(' and ') != -1:
        return And(constraint, sequence)
    elif re.search(r'[ ]?not ', constraint) != None:
        return Not(constraint, sequence)
    elif re.search(r'equal[ ]*?\([\s\S]*?\)', constraint) != None:
        return Equal(constraint, sequence)
    elif re.search(r'stop_at[ ]*?\([\s\S]*?\)', constraint) != None:
        return Stop_at(constraint, sequence)
    elif re.search(r'[a-z]*?[ ]*?\([\s\S]*?\)', constraint) != None:
        return Type(constraint, sequence)
    elif constraint.find(' in ') != -1:
        return In(constraint, sequence)
    else:
        raise Exception('Invalid constraint: ' + constraint)

def Type(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r'\([ ]*?[a-zA-Z0-9]*?[ ]*?\)')
    match = pattern.search(constraint)
    vartype = constraint[0:match.start(0)].strip()
    length = len(sequence)
    if re.match(r'[0-9]+', sequence) != None and re.match(r'[0-9]+', sequence).group(0) == sequence:
        typ = 'int'
    elif re.match(r'[0-9]+\.[0-9]+', sequence) != None and re.match(r'[0-9]+\.[0-9]+', sequence).group(0) == sequence:
        typ = 'float'
    else:
        typ = 'str'
    return typ == vartype

def Equal(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r'\([ ]*?([a-zA-Z0-9]*?)[ ]*?,[ ]*?(.*?)[ ]*?\)')
    match = pattern.findall(constraint)[0]
    pyexp = match[1].strip('\(\) ')
    expression = str(eval(pyexp))
    return expression.find(sequence) == 0

def Stop_at(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r'\([ ]*?([a-zA-Z0-9]*?)[ ]*?,[ ]*?(.*?)[ ]*?\)')
    match = pattern.findall(constraint)[0]
    pyexp = match[1].strip('\(\) ')
    index = eval('sequence.find(' + pyexp +')')
    return index != -1

def In(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r' in ')
    match = pattern.search(constraint)
    pyexp = constraint[match.start(0) + 4:].strip('\(\) ')
    expression = eval(pyexp)
    if type(expression) == list:
        expression = [str(i) for i in expression]
        for e in expression:
            if e.find(sequence) == 0:
                return True
        return False
    elif type(expression) == str:
        if expression.find(sequence) != -1:
            return True
        else:
            return False
    else:
        raise Exception('This python expression is not supported!')
        
def Or(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r' or ')
    match = pattern.search(constraint)
    c1 = constraint[0:match.start(0)].strip(' ')
    c2 = constraint[match.start(0) + 4:].strip(' ')
    return check_constraint(c1, sequence) or check_constraint(c2, sequence)

def And(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r' and ')
    match = pattern.search(constraint)
    c1 = constraint[0:match.start(0)].strip(' ')
    c2 = constraint[match.start(0) + 5:].strip(' ')
    return check_constraint(c1, sequence) and check_constraint(c2, sequence)

def Not(constraint:str, sequence:str) -> bool:
    sequence = sequence.strip(' ')
    pattern = re.compile(r'[ ]?not ')
    match = pattern.search(constraint)
    c = constraint[match.start(0) + 4:].strip(' ')
    return not check_constraint(c, sequence)