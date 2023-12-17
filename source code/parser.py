from typing import List, Tuple
import re

def tasksplit(inputsentences:str) -> List[str]:
    pattern = re.compile(r'(task[ ]*\n)("[\s\S]*?"[ ]*?\n)(output as[\s\S]*?\n)?(where[\s\S]*?)?(end)')
    tasks = pattern.findall(inputsentences)
    return tasks

def constructionsplit(task:Tuple) -> Tuple[List[str], str, List[str]]:
    sentences = task[1].replace('\n', ' ').strip(' \"')
    s = re.split(r'([\[{][a-zA-Z0-9]*?[\]}])', sentences)
    if s[-1] == '':
        del s[-1]
    if task[3] != '':
        constraints = task[3][5:].replace('\n', ' ').strip(' \n')
        c = re.split(r';', constraints)
        c = [i.strip(' ') for i in c]
    else:
        c = {}
    outputas = re.search(r'\[[a-zA-Z0-9]*?\]', task[2])
    if outputas:
        outputas = outputas.group()
    else:
        outputas = ''
    return s, outputas, c