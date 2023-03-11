Q = 0 #numarul de stari
A = [] #alfabetul
nr = 0 #numarul de muchii/tranzitii
D = {} #functia de tranzitie
qi = 0 #starea intiala
F = [] #starile finale

def citire_DFA(nume):
    global Q, A, nr, D, qi, F
    
    f = open(nume)
    Q = int(f.readline()) 
    A = [x for x in f.readline().split()] 
    nr = int(f.readline())
    
    for i in range(nr):
        qi, a, qf = f.readline().split()
        if qi not in D:
            D[qi] = {a : qf}
        else: 
            D[qi][a] = qf
    
    qi = f.readline().strip()
    F = [x for x in f.readline().split()]


def citire_NFA(nume):
    global Q, A, nr, D, qi, F
    
    f = open(nume)
    Q = int(f.readline()) 
    A = [x for x in f.readline().split()] 
    nr = int(f.readline())
    
    for i in range(nr):
        qi, a, qf = f.readline().split()
        if qi not in D:
            D[qi] = {a : [qf]}
        elif a not in D[qi]: 
            D[qi][a] = [qf]
        else:
            D[qi][a].append(qf)
    
    qi = f.readline().strip()
    F = [x for x in f.readline().split()]


def test_DFA(cuv):
    global A, D, qi, F
    respins = 0
    i = 0
    drum = [qi]
    sc = qi #starea curenta
    while i < len(cuv):
        su = D[sc].get(cuv[i], -1) #starea urmatoare
        if su == -1:
            respins = 1
            break
        else:
            sc = su
            drum.append(sc)
            i += 1
    #daca pe parcurs n-am mai gasit tranzitie / nu terminam intr-o stare finala
    if respins == 1 or drum[len(drum) - 1] not in F: 
        return 0, []
    else:
        return 1, drum


def test_NFA(cuv):
    global A, D, qi, F
    drum = [[qi]]

    def verificare(drumuri, i):
        if i < len(cuv):
            drumuri_viitoare = []
            for j in range(len(drumuri)):
                #pt fiecare drum partial pe care il avem luam un vector de viitoare stari prosibile valabile
                su = D[drumuri[j][len(drumuri[j]) - 1]].get(cuv[i], -1)
                if su != -1:
                    #avem in su toate starile in care putem ajunge cu cuv[i] din ultima stare a drumului
                    #la care suntem
                    drum_temp = []
                    for k in range(len(su)):
                        drum_temp = drumuri[j].copy()
                        drum_temp.append(su[k])
                        drumuri_viitoare.append(drum_temp)
                        #adaugam noile drumuri 
            return verificare(drumuri_viitoare, i + 1)
        else:
            return drumuri
        
    drum = verificare(drum, 0)

    drumuri_finale = []
    #verificam daca vreunul dintre drumurile obtinute ajung intr-un punct final
    for i in range(len(drum)):
        if drum[i][len(drum[i]) - 1] in F:
            drumuri_finale.append(drum[i])
    
    if len(drumuri_finale) == 0:
        return 0, []
    else:
        return 1, drumuri_finale


teste = [test_NFA, test_DFA]
#citim automatul
cerinta = int(input("Citim un AFD? \n[0/1]: "))
nume = input("Dati numele fisierului ce contine automatul: ")

if cerinta == 1:
    citire_DFA(nume)
else:
    citire_NFA(nume)

#trestam apartenenta cuvintelor la limbaj
k = 1
while k:
    cuv = input("\nDati cuvantul: ")
    apartine, drum = teste[cerinta](cuv)
    
    if apartine:
        print("Cuvant acceptat!") 
        if cerinta == 1:
            print("Drumul parcurs este: ", end = '')
            print(*drum)
        elif cerinta == 0 and len(drum) == 1:
            print("Drumul parcurs este: ", end = '')
            print(*drum[0])
        else:
            print("Drumurile parcurse sunt: ")
            for i in range(len(drum)):
                print(" - ", *drum[i])
    
    else:
        print("Cuvant respins!")

    k = int(input("\nVreti sa mai testati un cuvant? \n[0/1]: "))
