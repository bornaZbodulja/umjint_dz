a = open("ai.txt", "r")
lines = []
# ucitavamo tekstualnu datoteku s prostorom stanja i cijenama prijelaza
for line in a.readlines():
    # citamo liniju po liniju
    if "#" not in line: lines.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
a.close()
# zavrsili smo s citanjem prostora stanja

b = open("ai_pass.txt", "r")
heur = []
# ucitavamo tekstualnu datoteku s vrijednostima heuristike za pojedina stanja
for line in b.readlines():
    # citamo liniju po liniju
    if "#" not in line: heur.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
b.close()
# zavrsili smo s citanjem vrijednosti heuristike

class Node:
    def __init__(self, state, cost, func, parent):
        self.state = state
        self.cost = cost
        self.func = func
        self.parent = parent
        # definiramo razred Node s atributima stanja, cijene, func koja predstavlja zbroj
        # vrijednosti heuristike i cijene prijelaza za pojedino stanja (g+h) i cvora roditelja

    def succ(self):
        city_tag = self.state + ": "
        # definiramo metodu koja vraca listu cvorova sljedbenika

        for i in range(len(lines)):
            if city_tag in lines[i]:
                # pretrazujemo prostor stanja i trazimo trenutno stanje
                line = lines[i].replace(self.state + ": ", '')
                # kad smo nasli trenutno stanje unutar linija, micemo taj pocetak linija
                # i krenemo citati sljedbenike
                list = []
                child = Node("", 0, 0,"")
                word = ""
                # definiramo radnu rijec
                for c in line:
                    # citamo svaki char u stringu
                    if (c == ','):
                        # char "," definira kraj stanja a pocetak citanja cijene
                        child.state = word
                        # postavljamo stanje cvora na trenutnu radnu rijec
                        word = ''
                        # resetiramo radnu rijec
                    elif (c == ' ' or c == '\n'):
                        # ako smo dosli do razmaka znaci da smo dosli do kraja cvora
                        child.cost = int(word) + self.cost
                        # povecavamo cijenu puta do dijeteta za cijenu puta od roditelja do dijeteta
                        child.func = child.getHeuristic() + child.cost
                        # vrijednost atributa func postavljamo na zbroj cijene puta do dijeteta
                        # i heuristike za dano stanje
                        child.parent = self
                        # u atribut parent pohranjujemo roditeljski cvor
                        list.append(child)
                        # pohranjujemo cvor na listu sljedbenika
                        word = ''
                        child = Node("", 0, 0, "")
                    else:
                        word = word + c
                        # radnoj rijeci dodajemo ucitani char

                return list
                # vracamo listu sljedbenika

    def getHeuristic(self):
        # metoda koja za dano stanje cvora vraca vrijednost heuristike
        for line in heur:
            if(self.state in line):
                return int(line.replace(self.state + ": ", ''))


def initial(s0):
    node = Node(s0, 0, 0, "None")
    # inicijaliziramo pocetni cvor
    node.func = node.getHeuristic()
    # dohvacamo heuristiku za pocetno stanje
    return node
    # vracamo pocetni cvor

def insertSortedBy(open, node):
    # funkcija koja sortira listu otvorenih cvorova s obzirom na atribut func,
    # tj. na zbroj cijene i vrijednosti heuristike(g+h)
    if(open == []):
        open.append(node)
        # ako nam je lista otvorenih cvorova prazna samo dodajemo cvor u listu open
        return open
    for i in range(len(open)):
        if (open[i].func > node.func):
            open.insert(i, node)
            return open

    open.append(node)
    # ako cvor ima vecu vrijednost atributa func od svih cvorova na
    # listi dodajemo ga na kraj liste open
    return open

def searchLower(open, closed, child):
    # funkcija koja provjerava jesmo li vec bili u trenutnom stanju i
    # imamo li na listi zatvorenih cvorova put s manjom cijenom
    # do trenutnog stanja
    visited = False
    # bool varijabla koja oznacava jesmo li vec bili u trenutnom
    # stanju ili ne

    for node in open + closed:
        # pretrazujemo liste open i closed
        if node.state == child.state:
            visited = True
            # ako smo vec bili u trenutnom stanje mijenjamo vrijednost bool
            # bool varijable
            if node.cost > child.cost:
                # provjeravamo jesmo li do trenutnog stanja dosli vec samo s
                # vecom cijenom

                if node in closed: closed.remove(node)
                if node in open: open.remove(node)
                # ako jesmo micemo taj cvor s liste open U {closed}
                open = insertSortedBy(open, child)
                # umecemo trenutni cvor na listu open
                return open

    if not visited:
        # ako u trenutnom stanju jos nismo bili umecemo trenutni cvor
        # na listu open
        open = insertSortedBy(open, child)
        return open

def goals():
    # funkcija koja vraca listu ciljnih stanja
    goals = []
    word = ''
    for c in lines[1]:
        # iz druge linije tekstualne datoteke ucitamo ciljna stanja
        if c == ' ' or c == '\n':
            goals.append(word)
            word = ''
        else:
            word = word + c

    return goals

def aStarSearch(s0, goal):
    print("Running a Star:")
    open = []
    # definiramo listu otvorenih cvorova
    closed = []
    # definiramo listu vec ekspandiranih cvorova
    open.append(initial(s0))
    # na listu otvorenih cvorova dodajemo cvor s pocetnim stanjem i cijenom nula


    while open != []:
        n = open.pop(0)
        # s liste ostvorenih cvorova skidamo prvi po redu
        if(n.state in goal):
            # provjeravamo jesmo li dosli na cilj
            print("States visited = " + str(len(closed) + 1))
            path_to_goal = []
            current_node = n
            # rekonstrukcija puta do cilja
            while (current_node != "None"):
                path_to_goal.append(current_node.state)
                # idemo unazad po roditeljskim cvorovima
                current_node = current_node.parent

            path_to_goal.reverse()
            print("Found path with of length " + str(len(path_to_goal)) + " with total cost of " + str(n.cost) + ":")
            for item in path_to_goal:
                # ispis pronadenog puta do cilja
                if item not in goal: print(item + "=>")
                else: print(item)


            return

        closed.append(n)
        # na listu zatvorenih cvorova dodajemo trenutni cvor
        children = n.succ()
        # preko metode klase Node vracamo listu sljedbenika trenutnog cvora

        if children != None:
            # provjeravamo ima li trenutni cvor sljedbenika, tj. jesmo li dosli do lista
            for child in children:
                searchLower(open, closed, child)

    return "fail"

goal = goals()
s0 = lines[0].replace("\n", "")
# citamo pocetno stanje iz prve linije tekstualne datoteke
print("Start state: " + s0)
print("Goal state(s): " + str(goal))
aStarSearch(s0, goal)