from re import search
import re

def POS(sop):
    combine = sop.split("+")
    character = "\w"
    incorrect = "\+'"
    result = []
    for idx, val in enumerate(combine):
        combine[idx] = combine[idx].strip()
        combine[idx] = '+'.join(combine[idx])
        combine[idx] = (re.sub(incorrect, "'", combine[idx]))
        for p, q in enumerate(combine[idx]):
            if search(character, q):
                combine[idx] = combine[idx].replace(q, q + "'")
                doubleComplement = "\''"
                combine[idx] = (re.sub(doubleComplement, '', combine[idx]))
        x = '(' + combine[idx] + ')'
        result.append(x)
    pos = '.'.join(result)
    return pos
