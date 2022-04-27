import itertools
import math
from re import search
from .NAND import NAND
from .POS import POS
from .NOR import NOR

response = {
    "PI": "",
    "EPI": "",
    "optimisedSolution": ""
}


def returnMinterms(a):  # Function for finding out which minterms are merged. For example, 10-1 is obtained by merging
    # 9(1001) and 11(1011)
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a, 2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
    temp = []
    for i in range(pow(2, gaps)):
        temp2, ind = a[:], -1
        for j in x[0]:
            if ind != -1:
                ind = ind + temp2[ind + 1:].find('-') + 1
            else:
                ind = temp2[ind + 1:].find('-')
            temp2 = temp2[:ind] + j + temp2[ind + 1:]
        temp.append(str(int(temp2, 2)))
        x.pop(0)
    return temp


# Convert List to JSON
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


# compare two binary strings, check where there is one difference
def compElement(s1, s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count += 1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None


# compare if the number is same as implicant term
def compBinarySame(term, number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True


# combine pairs and make new group
def combineMinterms(group, unchecked):
    # check list
    check_list = []

    # create next group
    next_group = [[] for x in range(len(group) - 1)]
    substring = "-"
    # go through the groups
    for i in range(len(group) - 1):
        for elem1 in group[i]:
            for elem2 in group[i + 1]:
                b, pos = compElement(elem1, elem2)
                if b:
                    if search(substring, elem1) or search(substring, elem2):
                        check_list.append(elem1 + " " + elem2)
                    else:
                        check_list.append(str(int(elem1, 2)) + "," + str(int(elem2, 2)))
                    # replace the different bit with '-'
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)  #
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked, check_list


# remove redundant lists in 2d list
def remove_redundant(group):
    new_group = []
    for j in group:
        new = []
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group


# remove redundant in 1d list
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


# return True if empty
def check_empty(group):
    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count += 1
        if count == 0:
            return True
    return False


# find essential prime implicants
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            # find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime


def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True


# multiply two terms (ex. (p1 + p2)(p1+p4+p5) )..it returns the product
def multiply(list1, list2):
    list_result = []
    # if empty
    if len(list1) == 0 and len(list2) == 0:
        return list_result
    # if one is empty
    elif len(list1) == 0:
        return list2
    # if another is empty
    elif len(list2) == 0:
        return list1
    else:
        for i in list1:
            for j in list2:
                if i == j:
                    list_result.append(i)
                else:
                    list_result.append(list(set(i + j)))

        # sort and remove redundant lists and return this list
        list_result.sort()
        return list(list_result for list_result, _ in itertools.groupby(list_result))


def petrick_method(Chart):
    # initial P
    P = []
    for col in range(len(Chart[0])):
        p = []
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    # do multiplication
    for l in range(len(P) - 1):
        P[l + 1] = multiply(P[l], P[l + 1])

    P = sorted(P[len(P) - 1], key=len)
    final = []
    # find the terms with min length = this is the one with lowest cost (optimized result)
    min = len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    # final is the result of petrick's method
    return final


def find_minimum_cost(Chart, unchecked):
    P_final = []
    # essential_prime = list with terms with only one 1 (Essential Prime Implicants)
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    # Assign essential primes
    if len(essential_prime) > 0:
        s = ""
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s = s + binary_to_letter(unchecked[i], True) + ' , '
                    response["EPI"] = (s[:(len(s) - 3)])

    # modifiy the chart to exclude the covered terms
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    # if all zero, no need for petrick method
    if check_all_zero(Chart):
        P_final = [essential_prime]
    else:
        # petrick's method
        P = petrick_method(Chart)

        # find the one with minimum cost
        # see "Introduction to Logic Design" - Alan B.Marcovitz Example 4.6 pg 213
        '''
        Although Petrick's method gives the minimum terms that cover all,
        it does not mean that it is the solution for minimum cost!
        '''

        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count + cal_efficient(unchecked[i])
            P_cost.append(count)

        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        # append prime implicants to the solution of Petrick's method
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)

    return P_final


# calculate the number of literals


def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count += 1
    return count


# print the binary code to letter


def binary_to_letter(s, POS):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        # if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c + '\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n += 1
        # conditions for next operations
        if c == 'z' and more == False:
            c = 'A'
        elif c == 'Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c) + 1)
    return out


def returnDecimal(val):
    decimal = []
    for item in val:
        decimal.append(str(int(item, 2)))
    return decimal

#Store binary pairs
def pairingResults(group):
    firstPassPI = []
    decimal = []

    for items in group:
        for item in items:
            y = ','.join(returnMinterms(item))
            decimal.append(y)
    j = 0
    for idx, val in enumerate(group):
        i = len(group[idx]) + j
        firstPassPI.extend([["Group", idx, "Binary", val, "Pairs", decimal[j:i]]])
        j = i
    return firstPassPI


def createPairs(group):
    firstPass = []
    initialPairing = []
    try:
        for idx, val in enumerate(group):
            if group[idx]:
                firstPass.extend([val])

        x = pairingResults(firstPass)
        for i in range(len(x)):
            initialPairing.append(Convert(x[i]))
        return initialPairing
    except:
        return ''


def returnSolution(a, n_var, unchecked):
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range(len(unchecked)):
            # term is same as number
            if compBinarySame(unchecked[j], a[i]):
                Chart[j][i] = 1

    primes = find_minimum_cost(Chart, unchecked)
    primes = remove_redundant(primes)

    for prime in primes:
        s = ''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s = s + binary_to_letter(unchecked[i], True) + ' + '
        response["optimisedSolution"] = s[:(len(s) - 3)]
        if math.log(len(a), 2) == n_var:
            response["optimisedSolution"] = '1'
        return response


def toBinary(a, n_var):
    group = [[] for x in range(n_var + 1)]
    decimal = []
    for i in range(len(a)):
        # convert to binary
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            # add zeros to fill the n-bits
            for j in range(n_var - len(a[i])):
                a[i] = '0' + a[i]
        elif len(a[i]) > n_var:
            print('\nError : Choose the correct number of variables(bits)\n')
            return
        # count the num of 1
        index = a[i].count('1')
        # group by num of 1 separately
        group[index].append(a[i])
    return group


# main function
def main(a, n_var, solutionType):
    # make a group list
    group = toBinary(a, n_var)
    all_group = []
    unchecked = []
    checked = []
    # combine the pairs in series until nothing new can be combined
    while not check_empty(group):
        all_group.append(group)
        next_group, unchecked, check_list = combineMinterms(group, unchecked)
        checked.append(check_list)
        group = remove_redundant(next_group)

    primeImplicants = []
    for idx, val in enumerate(all_group[0]):
        if all_group[0][idx]:
            primeImplicants.extend([["Group", idx, "Binary", val, "Decimal", returnDecimal(val)]])

    initialGroups = []
    initialPairing = []
    secondPairing = []
    for i in range(len(primeImplicants)):
        initialGroups.append(Convert(primeImplicants[i]))
    if len(all_group) > 1:
        initialPairing = createPairs(all_group[1])

    if len(all_group) > 2:
        secondPairing = createPairs(all_group[2])
    s = ""
    for i in unchecked:
        s = s + binary_to_letter(i, True) + " , "
        response["PI"] = (s[:(len(s) - 3)])

    if math.log(len(a), 2) == n_var:
        response["optimisedSolution"] = '1'
        solution = response
    else:
        # make the prime implicant chart
        solution = returnSolution(a, n_var, unchecked)
    if solutionType == "NAND":
        response["optimisedSolution"] = (NAND(response["optimisedSolution"]))
        solution = response
    elif solutionType == "POS":
        response["optimisedSolution"] = (POS(response["optimisedSolution"]))
        solution = response
    elif solutionType == "NOR":
        response["optimisedSolution"] = (NOR(POS(response["optimisedSolution"])))
        solution = response
    print(solution["optimisedSolution"])
    print(solutionType)
    return solution, initialGroups, initialPairing, secondPairing