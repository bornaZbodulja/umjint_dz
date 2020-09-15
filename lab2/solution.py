import sys

class Clause():
    def __init__(self, clause, level, used, parent):
        self.clause = clause
        self.level = level
        self.used = used
        self.parents = parent

    def isValid(self):
        for element in self.clause:
            if '~' in element:
                element = element.replace('~', '')
                if element in self.clause: return True
        return False

    def factorize(self):
        for element in self.clause:
            if self.clause.count(element) > 1:
                self.clause.remove(element)
                self.clause.sort()

    def negateGoal(self):
        for element in self.clause:
            if '~' in element:
                self.clause.remove(element)
                element = element.replace('~', '')
                self.clause.append(element)
                self.clause.sort()
            else:
                self.clause.remove(element)
                element = "~" + element
                self.clause.append(element)
                self.clause.sort()

def getBase(path):
    a = open(path, 'r')
    parent_clauses = []
    i = 1
    for line in a.readlines():
        if line[0] != '#':
            line = line.lower()
            line = line.replace('\n', '')
            clause = (line.split(" v "))
            newClause = Clause(list.copy(clause), i, 0, "None")
            newClause.factorize()
            if newClause.isValid() == False:
                parent_clauses.append(newClause)
                i+=1
            clause.clear()

    a.close()

    goal = parent_clauses.pop(len(parent_clauses) - 1)
    goals = []
    k = len(parent_clauses) + 1
    for elem in goal.clause:
        cl = Clause([elem], k, 0, "None")
        cl.negateGoal()
        goals.append(cl)
        k += 1
    return parent_clauses, goals


def getBaseCooking(path):
    a = open(path, 'r')
    parent_clauses = []
    i = 1
    for line in a.readlines():
        if line[0] != '#':
            line = line.lower()
            line = line.replace('\n', '')
            clause = (line.split(" v "))
            newClause = Clause(list.copy(clause), i, 0, "None")
            newClause.factorize()
            if newClause.isValid() == False:
                parent_clauses.append(newClause)
                i+=1
            clause.clear()

    a.close()
    return parent_clauses

def negateLiteral(literal):
    if '~' in literal: return literal.replace('~', '')
    else: return '~' + literal


def printParents(parents):
    for cl in parents:
        string = str(cl.level) + "    " + printClause(cl.clause) + "\n"
        print(string)
    print("---------------------------------------------------")

def printGoal(goal):
    for elem in goal:
        string = str(elem.level) + "    " + printClause(elem.clause) + "\n"
        print(string)
    print("---------------------------------------------------")

def printGl(goals):
    str = ""
    i = 1
    for item in goals:
        if i == len(goals):
            str += item
        else:
            str += item + " v "
        i += 1
    #str += "\n"
    return str

def printMulti(goals):
    str = ""
    i = 1
    for item in goals:
        if i != len(goals): str += printGl(item.clause) + " v "
        else: str += printGl(item.clause)
        i += 1
    #str += "\n"
    return str


def plResolve(c1, c2, level):
    rezolvent = []
    for literal in c1.clause:
        if negateLiteral(literal) in c2.clause:
            rezolvent = c1.clause + c2.clause
            rezolvent.remove(literal)
            rezolvent.remove(negateLiteral(literal))
            rezolvent.sort()
            parent = c1
            if rezolvent != []:
                if c1.level>c2.level: parent = c1
                else: parent = c2
                result = Clause(rezolvent, level, [c1.level, c2.level], parent)
                result.factorize()
                return result
            elif rezolvent == []:
                if c1.level>c2.level: parent = c1
                else: parent = c2
                return Clause("NIL", level, [c1.level, c2.level], parent)
    return False


def selectClauses(sos, clauses):
    listOfClauses = []
    for c1 in sos:
        for c2 in clauses+sos:
            if(c1.clause != c2.clause): listOfClauses.append([c1, c2])
    return listOfClauses


def isRedundant(resolvent, new):
    if new == []:
        new.append(resolvent.clause)
        return
    for clause in new:
        if all(elem in clause for elem in resolvent.clause):
            new.remove(clause)
            new.append(resolvent.clause)
            return
        elif all(elem in resolvent.clause for elem in clause):
            return
    new.append(resolvent.clause)
    return


def sosRedundant(sos, resolvent, parent_clauses):
    for element in sos+parent_clauses:
        if all(elem in element.clause for elem in resolvent.clause):
            if element in sos: sos.remove(element)
            sos.append(resolvent)
            return
        elif all(elem in resolvent.clause for elem in element.clause):
            return
    sos.append(resolvent)
    return



def printPath(nil):
    level = []
    path = []
    #path.append(goal.clause)
    parent = nil.parents
    pars = []
    pars.append(nil.used)
    level.append(nil.level)
    #print(parent.clause)
    while(parent != "None"):
        path.append(parent.clause)
        #print(parent.clause)
        if parent.used != 0: pars.append(parent.used)
        level.append(parent.level)
        parent = parent.parents

    path.pop(len(path)-1)
    level.pop(len(level)-1)
    #print(level)
    #print(pars)
    path.reverse()
    #print(path)
    pars.reverse()
    level.reverse()

    i = 0
    for elem in path:
        string = str(level[i]) + "    "
        string += printClause(elem)
        string += "    (" + str(pars[i][1]) + ", " + str(pars[i][0]) + ")\n"
        print(string)
        i += 1
    print(str(level[i]) + "    " + "NIL" + "     (" + str(pars[i][1]) + ", " + str(pars[i][0]) + ")\n")

    #print(pars)


def printClause(clause):
    i = 0
    cl = ""
    for element in clause:
        if i == len(clause) - 1:
            cl += element
        else: cl += element + " v "
        i+=1
    return cl


def plResolution(parents, goal, verbose):
    sos = []
    clauses = [hm.clause for hm in parents]
    for elem in goal:
        clauses.append(elem.clause)
    #print(clauses)
    sos = [cl for cl in goal]
    #print(goal[0].level)
    j = len(clauses) + 1
    while(1):
        ver = selectClauses(sos, parents)
        if ver != []:
            new = []
            i = 0
            for c1, c2 in ver:
                resolvent = plResolve(c1, c2, j)
                #print(resolvent)
                if resolvent != False:
                    #i += 1
                    if resolvent.clause == "NIL":
                        if verbose:
                            printParents(parents)
                            printGoal(goal)
                            printPath(resolvent)
                        for elem in goal: elem.negateGoal()
                        print (printMulti(goal).lower() + " is true")
                        return True
                    elif resolvent.isValid() == False:
                        #print(resolvent.clause)
                        isRedundant(resolvent, new)
                        sosRedundant(sos,resolvent, parents)
            j += 1

            #print(new)
            if (all(elem in clauses for elem in [cl.clause for cl in sos])) or (ver == []):
                for elem in goal: elem.negateGoal()
                print(printMulti(goal).lower() + " is unknown")
                return False
            if new != []: clauses = clauses + new

def readInput(path, parents, verbose):
    b = open(path, 'r')
    for line in b.readlines():
        if line[0] != "#":
            line = line.replace("\n", "")
            line = line.lower()
            #print(line)
            if line[-1] == '+':
                line = line.replace('+', '')
                line = line.strip()
                clause = line.split(" v ")
                addClause(parents, clause)
            elif line[-1] == "-":
                line = line.replace('-', '')
                line = line.strip()
                clause = line.split(" v ")
                removeClause(parents, clause)
            elif line[-1] == "?":
                line = line.replace('?', '')
                line = line.strip()
                goal = line.split(" v ")
                gl = addGoal(goal, len(parent_clauses))
                #gl.negateGoal()
                #gl.level = len(parents) + 1
                plResolution(parents, gl, verbose)
    b.close()



def removeClause(parents, clause):
    for element in parents:
        if clause == element.clause:
            parents.remove(element)

    k = 1
    for element in parents:
        element.level = k
        k += 1
    return

def addClause(parents, clause):
    newCl = Clause(clause, len(parents) + 1, 0, "None")
    if newCl.isValid() == False:
        parents.append(newCl)
    return

def addGoal(clause, len):
    goal = Clause(clause, 0, 0, "None")
    goals = []
    for elem in goal.clause:
        cl = Clause([elem], len + 1, 0, "None")
        len += 1
        cl.negateGoal()
        goals.append(cl)
        #k += 1
    return goals

if __name__ == "__main__":
    inp = sys.argv
    #print(inp)
    verbose = False
    #inp = str(input())
    #print(inp)
    #print(inp[0])
    if "true" in inp: verbose = True
    if inp[1] == "resolution":
        parent_clauses, goal = getBase(inp[2])
        plResolution(parent_clauses, goal, verbose)
        exit()
    elif inp[1] == "cooking_test":
        parent_clauses = getBaseCooking(inp[2])
        #print("Resolution system constructed with knowledge:")
        readInput(inp[3], parent_clauses, verbose)
    elif inp[1] == "cooking_interactive":
        parent_clauses = getBaseCooking(inp[2])
        print("Resolution system constructed with knowledge:")
        for clause in parent_clauses:
            print(printClause(clause.clause))
        while(1):
            print("Please enter your query")
            cmd = str(input())
            cmd.replace("\n", '')
            cmd = cmd.lower()
            if cmd[-1] == "+":
                cmd = cmd.replace("+", '')
                cmd = cmd.strip()
                cl = cmd.split(" v ")
                addClause(parent_clauses, cl)
                print(cmd + " is added")
            elif cmd[-1] == "-":
                cmd = cmd.replace("-", '')
                cmd = cmd.strip()
                cl = cmd.split(" v ")
                removeClause(parent_clauses, cl)
                print(cmd + " is removed")
            elif cmd[-1] == '?':
                cmd = cmd.replace("?", '')
                cmd = cmd.strip()
                cl = cmd.split(" v ")
                gl = addGoal(cl, len(parent_clauses))
                #gl.negateGoal()
                #gl.level = len(parent_clauses) + 1
                plResolution(parent_clauses, gl, verbose)
            elif cmd.lower() == "exit":
                exit()
