f = open("istra.txt", "r")
lines = []
# ucitavamo tekstualnu datoteku s prostorom stanja i cijenama prijelaza
for line in f.readlines():
    # citamo liniju po liniju
    if "#" not in line: lines.append(line)
    # ako se u liniji nalazi # preskacemo tu liniju
f.close()
# zavrsili smo s citanjem tekstualne datoteke

class Node:
    def __init__(self, state, depth, parent):
        self.state = state
        self.depth = depth
        self.parent = parent
        # definiramo razred Node s atributima stanja, dubine i cvora roditelja

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
                        child.depth = 1 + self.depth
                        # povecavamo dubinu dijeteta za 1 u odnosu na roditelja
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



def initial(s0):
    return Node(s0, 0, "None")
    # vracamo pocetni cvor na dubini nula

def insertSortedBy(open, node):
    # funkcija koja sortira listu otvorenih cvorova s obzirom na dubinu
    if(open == []):
        open.append(node)
        # ako nam je lista otvorenih cvorova prazna samo dodajemo cvor u listu open
        return open

    for i in range(len(open)):
        if (open[i].depth > node.depth):
            # cvor umecemo na
            open.insert(i, node)
            return open

    open.append(node)
    # ako cvor ima vecu dubinu od svih cvorova na listu dodajemo ga na kraj liste open
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



def breadthFirstSearch(s0, goal):
    print("Running bfs:")
    open = []
    # definiramo listu otvorenih cvorova
    closed = []
    # definiramo listu vec ekspandiranih stanja
    open.append(initial(s0))
    # na listu otvorenih cvorova dodajemo cvor s pocetnim stanjem i dubinom nula

    while open != []:
        n = open.pop(0)
        # s liste ostvorenih cvorova skidamo prvi po redu
        if(n.state not in closed):
            # provjeravamo jesmo li trenutno stanje cvora vec ekspandirali
            closed.append(n.state)
            # dodajemo stanje trenutnog cvora na listu vec ekspandiranih stanja
            if(n.state in goal):
                # provjeravamo jesmo li dosli na cilj
                print("States visited = " + str(len(closed)))
                path_to_goal = []
                current_node = n
                # rekonstrukcija puta do cilja
                while (current_node != "None"):
                    path_to_goal.append(current_node.state)
                    # idemo unazad po roditeljskim cvorovima
                    current_node = current_node.parent


                path_to_goal.reverse()
                print("Found path of length " + str(len(path_to_goal)) + ":")

                for item in path_to_goal:
                    # ispis pronadenog puta do cilja
                    if item not in goal: print(item + "=>")
                    else: print(item)

                return

            children = n.succ()
            # preko metode klase Node vracamo listu sljedbenika trenutnog cvora

            if children != None:
                # provjeravamo ima li trenutni cvor sljedbenika, tj. jesmo li dosli do lista
                for child in children:
                    open = insertSortedBy(open, child)
                    # svakog sljedbenika dodajemo na listu otvorenih cvorova


    return "fail"

s0 = lines[0].replace("\n", "")
# citamo pocetno stanje iz prve linije tekstualne datoteke
goal = goals()
print("Start state: " + s0)
print("Goal state(s): " + str(goal))
breadthFirstSearch(s0, goal)