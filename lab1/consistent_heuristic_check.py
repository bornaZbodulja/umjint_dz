f = open("ai.txt", "r")
lines = []
# ucitavamo tekstualnu datoteku s prostorom stanja i cijenama prijelaza
for line in f.readlines():
    # citamo liniju po liniju
    if "#" not in line: lines.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
f.close()
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
            if (self.state in line):
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


def checkConsistentHeuristic(states):
    print("Checking if heuristic is consistent: ")
    consistent = True
    for city in states:
        # za svako stanje u prostoru stanja provjeravamo uvjet konzistentnosti
        n = initial(city)
        parent_heuristic = n.getHeuristic()
        # definiramo varijablu u koju pohranjujemo vrijednost heuristike
        # roditeljskog cvora
        children = n.succ()
        # lista u kojoj pohranjujemo cvorove sljedbenike

        if children != None:
            for child in children:
                child_heuristic = child.getHeuristic()
                # definiramo varijablu u kojoj pohranjujemo vrijednost heuristike
                # cvora dijeteta
                if (parent_heuristic > (child_heuristic + child.cost)):
                    # provjera uvjeta konzistentnosti
                    consistent = False
                    print("[ERR] h(" + city + ") > h(" + child.state + ") + c: " +
                        str(parent_heuristic) + " > " + str(child_heuristic) + " + " + str(child.cost))

    if not consistent:
        print("Heuristic is not consistent.")
    else:
        print("Heuristic is consistent.")


cities = getCities()
checkConsistentHeuristic(cities)
