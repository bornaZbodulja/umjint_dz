f = open("ai.txt", "r")
lines = []
# ucitavamo tekstualnu datoteku s prostorom stanja i cijenama prijelaza
for line in f.readlines():
    # citamo liniju po liniju
    if "#" not in line: lines.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
f.close()
# zavrsili smo s citanjem prostora stanja

b = open("ai_fail.txt", "r")
heur = []
# ucitavamo tekstualnu datoteku s vrijednostima heuristike za pojedina stanja
for line in b.readlines():
    # citamo liniju po liniju
    if "#" not in line: heur.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
b.close()
# zavrsili smo s citanjem vrijednosti heuristike

class Node:
    def __init__(self, state, cost, parent):
        self.state = state
        self.cost = cost
        self.parent = parent
        # definiramo razred Node s atributima stanja, cijene i cvora roditelja

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
                child = Node("", 0, "")
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
                        child.parent = self
                        # u atribut parent pohranjujemo roditeljski cvor
                        list.append(child)
                        # pohranjujemo cvor na listu sljedbenika
                        word = ''
                        child = Node("", 0, "")
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


def getCities():
    # funkcija koja za dani prostor stanja vraca listu svih stanja
    cities = []
    for line in heur:
        index = line.find(':')
        word = line[0:index]
        cities.append(word)

    return cities


def initial(s0):
    return Node(s0, 0, "None")
    # vracamo pocetni cvor s cijenom nula

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


def insertSortedBy(open, node):
    # funkcija koja sortira listu otvorenih cvorova s obzirom na cijenu
    if(open == []):
        open.append(node)
        # ako nam je lista otvorenih cvorova prazna samo dodajemo cvor u listu open
        return open
    for i in range(len(open)):
        if (open[i].cost > node.cost):
            open.insert(i, node)
            return open

    open.append(node)
    # ako cvor ima vecu cijenu od svih cvorova na listu dodajemo ga na kraj liste open
    return open

def modifiedUniformCostSearch(s0, goal):
    open = []
    # definiramo listu otvorenih cvorova
    open.append(initial(s0))
    # na listu otvorenih cvorova dodajemo cvor s pocetnim stanjem i cijenom nula

    while open != []:
        n = open.pop(0)
        # s liste ostvorenih cvorova skidamo prvi po redu

        if(n.state in goal):
            # provjeravamo jesmo li dosli na cilj
            return n.cost
            # varacamo samo cijenu puta do cilja

        children = n.succ()
        # preko metode klase Node vracamo listu sljedbenika trenutnog cvora

        if children != None:
            # provjeravamo ima li trenutni cvor sljedbenika, tj. jesmo li dosli do lista
            for child in children:
                open = insertSortedBy(open, child)

    return "fail"


def checkOptimisticHeuristic(states, goal):
    print("Checking if heuristic is optimistic: ")
    optimistic = True
    for city in states:# za svako stanje u prostou stanja provjeravamo uvjet optimisticnosti
        n = initial(city)
        optimal_cost = modifiedUniformCostSearch(city, goal)
        # definiramo varijablu koja predstavlja optimalnu cijenu puta od trenutnog stanja do
        # ciljnog stanja
        heuristic = n.getHeuristic()
        # definiramo varijablu koja predstavlja vrijednost heuristike za trenutno stanje
        if(optimal_cost < heuristic):
            # provjeravamo uvjet optimisticnosti
            optimistic = False
            print("[ERR] h(" + city + ") > h*: " + str(heuristic) + " > " + str(optimal_cost))

    if not optimistic: print("Heuristic is not optimistic.")
    else: print("Heuristic is optimistic.")


goal = goals()
cities = getCities()
checkOptimisticHeuristic(cities, goal)
