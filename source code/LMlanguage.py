from runtime import task
from parser import tasksplit
from complete import completeness
import re

def query_execution(query:str):
    completeness(query)
    public_scope = {}
    pattern_argmax = re.compile(r'argmax')
    pattern_top = re.compile(r'(top_k[ ]*?=[ ]*?)([0-9]+?)')
    match_argmax = pattern_argmax.search(query)
    match_top = pattern_top.findall(query)
    if match_argmax != None:
        decoding = 1
    elif len(match_top) == 1 and int(match_top[0][1]) > 0 and int(match_top[0][1]) < 6:
        decoding = int(match_top[0][1])
    else:
        raise Exception('Invalid decoding method!')
    tasks = tasksplit(query)
    for t in tasks:
        one_task = task(t, public_scope, decoding)
        output = one_task.run()
        public_scope.update(output)