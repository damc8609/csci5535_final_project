from parser import tasksplit, constructionsplit
from typing import List
import re

def completeness(inputsentences:str):
    public_scope = []
    tasks = tasksplit(inputsentences)
    for t in tasks:
        private_scope = []
        private_scope.extend(public_scope)
        parsed = constructionsplit(t)
        checkcomplete_s(parsed[0], private_scope)
        if parsed[1] != '':
            private_scope.append(parsed[1].strip('\[\] '))
            public_scope.append(parsed[1].strip('\[\] '))
        if parsed[2] != {}:
            checkcomplete_c(parsed[2], private_scope)

def checkcomplete_s(s_list:List[str], scope:List[str]):
    for s in s_list:
        if re.search(r'\[[a-zA-Z0-9]+?\]', s) != None:
            com_var_brackets(s, scope)
        elif re.search(r'\{[a-zA-Z0-9]+?\}', s) != None:
            com_var_curlybraces(s, scope)
        else:
            com_string(s)

def com_string(s:str):
    pass

def com_var_brackets(s:str, scope:List[str]):
    variablename = re.search(r'\[[a-zA-Z0-9]+?\]', s).group(0).strip('\[\] ')
    scope.append(variablename)

def com_var_curlybraces(s:str, scope:List[str]):
    variablename = re.search(r'\{[a-zA-Z0-9]+?\}', s).group(0).strip('\{\} ')
    if scope.count(variablename) == 0:
        raise Exception('Not defined variable: ' + variablename)

def checkcomplete_c(c_list:List[str], scope:List[str]):
    for c in c_list:
        if c.find(r' or ') != -1:
            return com_or(c, scope)
        elif c.find(' and ') != -1:
            return com_and(c, scope)
        elif re.search(r'[ ]?not ', c) != None:
            return com_not(c, scope)
        elif re.search(r'equal[ ]*?\([\s\S]*?\)', c) != None:
            return com_equal(c, scope)
        elif re.search(r'stop_at[ ]*?\([\s\S]*?\)', c) != None:
            return com_stop_at(c, scope)
        elif re.search(r'[a-z]*?[ ]*?\([\s\S]*?\)', c) != None:
            return com_type(c, scope)
        elif c.find(' in ') != -1:
            return com_in(c, scope)
        else:
            raise Exception('Invalid constraint: ' + c)

def com_or(c:str, scope:List[str]):
    pattern = re.compile(r' or ')
    match = pattern.search(c)
    c1 = c[0:match.start(0)].strip(' ')
    c2 = c[match.start(0) + 4:].strip(' ')
    c1_var = checkcomplete_c([c1], scope)
    c2_var = checkcomplete_c([c2], scope)
    if c1_var != c2_var:
        raise Exception('Two variables are not the same one!')

def com_and(c:str, scope:List[str]):
    pattern = re.compile(r' and ')
    match = pattern.search(c)
    c1 = c[0:match.start(0)].strip(' ')
    c2 = c[match.start(0) + 5:].strip(' ')
    c1_var = checkcomplete_c([c1], scope)
    c2_var = checkcomplete_c([c2], scope)
    if c1_var != c2_var:
        raise Exception('Two variables are not the same one!')

def com_not(c:str, scope:List[str]) -> str:
    pattern = re.compile(r'[ ]?not ')
    match = pattern.search(c)
    c1 = c[match.start(0) + 5:].strip('\(\) ')
    return checkcomplete_c([c1], scope)

def com_equal(c:str, scope:List[str]) -> str:
    pattern = re.compile(r'\([ ]*?([a-zA-Z0-9]*?)[ ]*?,[ ]*?(.*?)[ ]*?\)')
    match = pattern.findall(c)[0]
    variablename = match[0].strip('\(\) ')
    pyexp = match[1].strip('\(\) ')
    if scope.count(variablename) == 0:
        raise Exception('Not defined variable: ' + variablename)
    eval(pyexp)
    return variablename

def com_stop_at(c:str, scope:List[str]):
    pattern = re.compile(r'\([ ]*?([a-zA-Z0-9]*?)[ ]*?,[ ]*?(.*?)[ ]*?\)')
    match = pattern.findall(c)[0]
    variablename = match[0].strip('\(\) ')
    pyexp = match[1].strip('\(\) ')
    if scope.count(variablename) == 0:
        raise Exception('Not defined variable: ' + variablename)
    eval(pyexp)
    return variablename

def com_type(c:str, scope:List[str]):
    pattern = re.compile(r'\([ ]*?[a-zA-Z0-9]*?[ ]*?\)')
    match = pattern.search(c)
    variablename = match.group(0).strip('\(\) ')
    if scope.count(variablename) == 0:
        raise Exception('Not defined variable: ' + variablename)
    return variablename

def com_in(c:str, scope:List[str]):
    pattern = re.compile(r' in ')
    match = pattern.search(c)
    variablename = c[0:match.start(0)].strip('\(\) ')
    pyexp = c[match.start(0) + 4:].strip('\(\) ')
    if scope.count(variablename) == 0:
        raise Exception('Not defined variable: ' + variablename)
    eval(pyexp)
    return variablename