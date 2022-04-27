from re import search


def NAND(s):
    pattern = "\w{1}'"
    x = search(pattern, s)
    if not x:
        combine = s.split("+")
        result = []
        for item in combine:
            item = item.strip()
            x = '(' + item + ')' + "'"
            result.append(x)
        y = '(' + '.'.join(result) + ')' + "'"
        return y
    else:
        idx = x.end()
        minterm = s[idx - 2] + s[idx - 1]
        newMinterm = '(' + s[idx - 2] + '.' + s[idx - 2] + ')' + "'"
        s = s.replace(minterm, newMinterm)
        return NAND(s)