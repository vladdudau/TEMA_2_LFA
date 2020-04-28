#fisierele de citire pentru fiecare automat
fisier_citire_lnfa = open('lnfa.in')
fisier_citire_nfa = open('nfa.in')
fisier_citire_dfa = open('dfa.in')

#functie de citire pentru LNFA

def Citire_LNFA(fisier):
    nr_stari = int(fisier.readline())
    lista_stari=[stare for stare in range(nr_stari)]   #de la 0 la nr_stari-1
    nr_litere_alfabet= int(fisier.readline())
    alfabet = []
    for litera in fisier.readline().split():
        alfabet += litera
    initiala = int(fisier.readline())
    nr_stari_finale = int(fisier.readline())
    finale = []
    for stare in fisier.readline().split():
        finale += [int(stare)]
    nr_tranzitii = int(fisier.readline())
    tranzitii = {}
    for i in range(nr_tranzitii):
        x = fisier.readline().split()
        if (int(x[0]),x[1]) not in tranzitii.keys():
            tranzitii[(int(x[0]),x[1])] = {int(x[2])}
        else:
            tranzitii[(int(x[0]), x[1])].add(int(x[2]))
    fisier.close()
    return nr_stari,lista_stari,nr_litere_alfabet,alfabet,initiala,nr_stari_finale,finale,nr_tranzitii,tranzitii

#Functie de citire pentru NFA

def Citire_NFA(fisier):
    nr_stari = int(fisier.readline())
    lista_stari=[stare for stare in range(nr_stari)]   #de la 0 la nr_stari-1
    nr_litere_alfabet= int(fisier.readline())
    alfabet = []
    for litera in fisier.readline().split():
        alfabet += litera
    initiala = int(fisier.readline())
    nr_stari_finale = int(fisier.readline())
    finale = []
    for stare in fisier.readline().split():
        finale += [int(stare)]
    nr_tranzitii = int(fisier.readline())
    tranzitii = {}
    for i in range(nr_tranzitii):
        x = fisier.readline().split()
        if (int(x[0]),x[1]) not in tranzitii.keys():
            tranzitii[(int(x[0]),x[1])] = {int(x[2])}
        else:
            tranzitii[(int(x[0]), x[1])].add(int(x[2]))
    fisier.close()
    return nr_stari,lista_stari,nr_litere_alfabet,alfabet,initiala,nr_stari_finale,finale,nr_tranzitii,tranzitii

#Functie de citire pentru DFA

def Citire_DFA(fisier):
    nr_stari = int(fisier.readline())
    lista_stari=[stare for stare in range(nr_stari)]   #de la 0 la nr_stari-1
    nr_litere_alfabet = int(fisier.readline())
    alfabet = []
    for litera in fisier.readline().split():
        alfabet += litera
    initiala = int(fisier.readline())
    nr_stari_finale = int(fisier.readline())
    finale = []
    for stare in fisier.readline().split():
        finale += [int(stare)]
    nr_tranzitii = int(fisier.readline())
    tranzitii = {}
    for i in range(nr_tranzitii):
        x = fisier.readline().split()
        tranzitii[(int(x[0]),x[1])] = int(x[2])
    fisier.close()
    return nr_stari,lista_stari,nr_litere_alfabet,alfabet,initiala,nr_stari_finale,finale,nr_tranzitii, tranzitii

#1.1 Pasul 1. Calcularea λ-inchiderii.

#Functie care calculeaza lambda inchiderea
#Orice stare face parte din propria sa λ-inchidere. Practic putem considera
#ca pentru orice stare exista o λ-tranzitie implicita catre ea insasi
#λ-inchiderea unei multimi de stari este egala cu reuniunea λ-inchiderii fiecarei
#stari din multime.

def lambda_inchidere(inceput,stare,inchideri,tranzitii):
    if inceput not in inchideri.keys():
        inchideri[inceput]={inceput}
    if (stare,'$') in tranzitii.keys():
        for x in tranzitii[(stare,'$')]:
            inchideri[inceput].add(x)
            lambda_inchidere(inceput,x,inchideri,tranzitii)
#apel recursiv, un fel de backtracking, verific in ce stari pot ajunge din fiecare stare

#1.2 Pasul 2. Calcularea functiei de tranzitie δ

#Cu ajutorul λ-inchiderii, putem calcula functia de tranzitie a NFA-ului pe care dorim sa il
#construim.

def calcularea_tranzitie_lambda_star(stare,litera,inchideri,transformare_in_nfa,tranzitii):
    for x in inchideri[stare]:
        if (x, litera) in tranzitii.keys():
            for i in tranzitii[(x, litera)]:
                if (stare, litera) in transformare_in_nfa.keys():
                    transformare_in_nfa[(stare, litera)].update(inchideri[i])
                else:
                    transformare_in_nfa[(stare, litera)] = inchideri[i].copy()

#functie care modifica pe a cu b intr un dictionar, imi va fi folositoare pentru cand calculez starile finale

def modifica(dict,a,b):           #il inlocuieste pe y cu x in dictionar
    for valori in dict.values():
        if b in valori:
            valori.discard(b)
            if a not in valori:
                valori.add(a)

#functia care transforma un LNFA in NFA utilizand cei 4 pasi

def transforma_LNFA_in_NFA(tranzitii,nr_stari,lista_stari,initiala,finale, alfabet):

    inchideri={}
    for stare_curenta in lista_stari:
        lambda_inchidere(stare_curenta,stare_curenta,inchideri,tranzitii)

    #pasul 1.1, am pus in lambda_inchidere stare_curenta de 2 ori deoarece stare_curenta este starea din care plecam, initiala

    transformare_in_nfa={}
    for stare_curenta in lista_stari:
        for litera in alfabet:
            calcularea_tranzitie_lambda_star(stare_curenta,litera,inchideri,transformare_in_nfa,tranzitii)

    #pasul 1.2, calcularea tranzitiei lambda star

    noile_stari_finale=finale.copy()
    for stare_curenta in lista_stari:
        for final in finale:
            if stare_curenta not in noile_stari_finale and final in inchideri[stare_curenta]:
                noile_stari_finale+=[stare_curenta]

    # pasul 1.3 Calcularea starilor finale si initiale.
    # Starea initiala ramane aceasi cu cea a automatlui initial, in cazul nostru 0.
    # Starile finale vor fi toate starile care contin o stare finala din automatul initial

    stare_curenta=0
    while stare_curenta< nr_stari:
        stare_urmatoare=stare_curenta+1
        while stare_urmatoare < nr_stari:
            gasit=1
            # daca starile au tranzitii diferite, nu sunt identice
            for litera in alfabet:
                if (lista_stari[stare_curenta],litera) in transformare_in_nfa.keys() and (lista_stari[stare_urmatoare],litera) in transformare_in_nfa.keys() and transformare_in_nfa[(lista_stari[stare_curenta],litera)]!=transformare_in_nfa[(lista_stari[stare_urmatoare],litera)]:
                    gasit=0
            # daca o stare e finala si alta nu, atunci nu s identice
            if (lista_stari[stare_urmatoare] not in noile_stari_finale and lista_stari[stare_curenta] in noile_stari_finale) or (lista_stari[stare_urmatoare] in noile_stari_finale and lista_stari[stare_curenta] not in noile_stari_finale):
                gasit=0
            if gasit==1:
                #se inlocuieste starea_curenta cu starea_urmatoare din noul dictionar
                modifica(transformare_in_nfa,lista_stari[stare_curenta], lista_stari[stare_urmatoare])
                if lista_stari[stare_urmatoare] in noile_stari_finale:
                    # se sterge din lista de stari finale, fiind redundanta
                    noile_stari_finale.remove(lista_stari[stare_urmatoare])
                #sterg legaturile dintre starea stearsa si celelalte stari
                for litera in alfabet:
                    if (lista_stari[stare_urmatoare],litera) in transformare_in_nfa.keys():
                        transformare_in_nfa.pop((lista_stari[stare_urmatoare],litera))
                #sterg starea
                lista_stari.pop(stare_urmatoare)
                stare_urmatoare-=1
                nr_stari-=1
            stare_urmatoare+=1
        stare_curenta+=1

        # pasul 1.4

    return transformare_in_nfa, nr_stari, lista_stari,initiala, noile_stari_finale, alfabet

#AM TRANSFORMAT LNFA IN NFA, urmand apoi sa transform NFA in DFA

def TRANSFORMA_NFA_IN_DFA(tranzitii,nr_stari,lista_stari,initiala,finale,alfabet):

    #PASUL 1 in NFA to DFA-ELIMIN NEDETERMINISMUL
    #Pornim cu o coada in care adaugam doar starea initiala q0. Apoi pentru ﬁecare stare din coada q
    # si ﬁecare caracter din alfabet α facem urmatorul calcul: daca δ(q,α) = qx0,...qxk,k ≥ 0 atunci:
    # creem starea qx0...xk(poate ﬁ si o stare care nu este compusa) Daca noua stare fromata qx0...xk nu a mai fost vizitata,
    # atunci o adaugam in coada. Tranzitia acestei stari cu un caracter α va ﬁ reuniunea starilor
    # accesibile cu caracterul α din toate starile componente. Repetam acest calcul pana cand coada devine vida.

    coada=[{initiala}]
    noua_lista_stari=[{initiala}]
    transformare_in_dfa={}
    while coada != []:              #Cat timp coada nu e vida
        for litera in alfabet:      #iau fiecare litera din alfabet
            multime = set()         #creez o multime
            for element in coada[0]:
                if(element,litera)in tranzitii.keys():
                    multime.update(tranzitii[element,litera])
            if multime!=set():
                if multime not in noua_lista_stari:
                    noua_lista_stari+=[multime]
                    coada+=[multime]
                transformare_in_dfa[(frozenset(coada[0]),litera)]=multime
        coada.pop(0)

    #PASUL 2 IN TRANSFORMAREA NFA IN DFA-CALCULAREA STARILOR INITIALE SI FINALE
    #Starea initiala ramane aceasi cu cea a automatlui initial, in cazul nostru 0.
    #Starile ﬁnale vor ﬁ toate starile care au in componenta o stare ﬁnala din automatul initial

    noile_stari_finale=[]                #aici stochez starile finale din noul automat
    for stare_curenta in noua_lista_stari:          #parcurg fiecare stare din noua lista de stari
        for stare_finala in finale:
            if stare_finala in stare_curenta and stare_curenta not in noile_stari_finale:
                noile_stari_finale+=[stare_curenta]

    #PASUL 3 in TRANSFORMAREA NFA IN DFA-REDENUMIREA STARILOR
    #Putem sa redenumim starile fara a afecta functionalitatea.
    initiala=0
    for index in range(len(noua_lista_stari)):
        for cheie in transformare_in_dfa.keys():
            if noua_lista_stari[index]==transformare_in_dfa[cheie]:
                transformare_in_dfa[cheie]=index
                    #^
                    #|
        #REDENUMESC FIECARE STARE DIN DICTIONAR

        for litera in alfabet:
            if (frozenset(noua_lista_stari[index]),litera) in transformare_in_dfa.keys():
              transformare_in_dfa[(index,litera)]=transformare_in_dfa[(frozenset(noua_lista_stari[index]),litera)]
              del transformare_in_dfa[(frozenset(noua_lista_stari[index]),litera)]

        if noua_lista_stari[index] in noile_stari_finale:
            noile_stari_finale.remove(noua_lista_stari[index])
            noile_stari_finale.append(index)

        #AFISEZ PENTRU FIECARE STARE VECHE NOUA EI DENUMIRE

        print("DENUMIREA VECHE IN NFA: ", noua_lista_stari[index]," / DENUMIRE NOUA IN DFA: ",index)
        noua_lista_stari[index]=index
    nr_stari=len(noua_lista_stari)
    return transformare_in_dfa, nr_stari, noua_lista_stari, initiala, noile_stari_finale, alfabet   #returnez noul automat

#FUNCTIE CARE STERGE O ANUMITA STARE DINTR-UN AUTOMAT DFA SI IMPLICIT SI LEGATURILE CU ALTA STARE

def STERGE_STARE(stare_curenta,tranzitii,lista_stari,alfabet):
    for litera in alfabet:
        if (stare_curenta,litera)in tranzitii.keys():
            del tranzitii[stare_curenta,litera]
        for stare in lista_stari:
            if (tuple(stare), litera) in tranzitii.keys() and tranzitii[tuple(stare),litera]==stare_curenta:
                del tranzitii[tuple(stare),litera]
    lista_stari.remove(set(stare_curenta))

#FUNCTIE CARE PARCURGE AUTOMATUL IN TOATE STARILE ACCESIBILE

def PARCURGERE_TOTALA(stare_curenta, alfabet,tranzitii,vizitat):
    #vectorul vizitat care verifica daca am trecut prin starea curenta sau nu
    if stare_curenta not in vizitat:
        vizitat.append(stare_curenta)
        for litera in alfabet:
            if (stare_curenta, litera) in tranzitii.keys():
                PARCURGERE_TOTALA(tranzitii[(stare_curenta, litera)], alfabet, tranzitii, vizitat)
#FUNCTIA ESTE ASEMANATOARE UNUI DFS, AVAND APEL RECURSIV, DINTR O STARE MA DUC IN TOATE STARILE ACCESBILIE

def PARCURGERE(stare_curenta, noile_stari_finale, alfabet, tranzitii, vizitat):
        #TRECE PRIN TOATE STARILE ACCESIBILE PANA AJUNGE IN STARE FINALA SAU PANA CAND NU MAI SUNT STARI NEVIZITATE
        global ok        #variabila de tip bool
        if stare_curenta not in vizitat:
            vizitat.append(stare_curenta)
            if set(stare_curenta) in noile_stari_finale:        #daca starea e finala, gasit e TRUE, deci ne oprim
                ok = True
            else:                                               #altfel parcurgem automatul pana ajungem intr o stare finala sau toate sunt vizitate
                for litera in alfabet:
                    if (stare_curenta, litera) in tranzitii.keys():
                        PARCURGERE(tranzitii[(stare_curenta, litera)], noile_stari_finale, alfabet, tranzitii, vizitat)
#FUNCTIA ESTE ASEMANATOARE UNUI DFS, AVAND APEL RECURSIV, DINTR-O STARE MA DUC IN TOATE STARILE ACCESIBILE

def TRANSFORMA_DFA_IN_DFAMIN(tranzitii,nr_stari,lista_stari,initiala,finale,alfabet):

    #PASUL 1 IN TRANSFORMAREA DFA IN DFA MINIMIZAT:
    #Doua stari sunt echivalente daca si numai daca pentru orice cuvant am alege,
    # plecand din cele doua stari, ajungem in doua stari ﬁe ﬁnale sau neﬁnale.
    #Construim lista de adiacenta si o marcam pe toata cu TRUE
    dictionar_stari_echivalente={}
    for stare in range(nr_stari):       #parcurg starile
        for copie_stare in range(stare+1):
            dictionar_stari_echivalente[stare,copie_stare]=True
    #Marcam cu FALSE toate perechile (q,r), unde q stare ﬁnala si r stare neﬁnala.
    for relatii in dictionar_stari_echivalente.keys():
        if (relatii[0] in finale and relatii[1] not in finale) or (relatii[0] not in finale and relatii[1] in finale):
            dictionar_stari_echivalente[relatii]=False

    gasit=1
    while(gasit==1):
        copie_dictionar_stari_echivalente=dictionar_stari_echivalente.copy()
        for litera in alfabet:
            for relatii in dictionar_stari_echivalente.keys():
                if dictionar_stari_echivalente[max(tranzitii[relatii[0], litera], tranzitii[relatii[1], litera]), min(tranzitii[relatii[0], litera], tranzitii[relatii[1], litera])]==False:
                    dictionar_stari_echivalente[relatii]=False
        if copie_dictionar_stari_echivalente==dictionar_stari_echivalente:
            gasit=0

    #PASUL 2 IN TRANSFORMAREA DFA IN DFA-MINIMIZAT-Gruparea starilor echivalente si calcularea functiei de tranzitie
    #Grupam starile echivalente rezultate din matricea de echivalenta intr-o unica stare.
    #Tranzitiile vor ﬁ aceleasi cu ale automatului initial dar tinand cont de aceasta grupare
    stari_DFA_MIN=[]                    #NOILE STARI DIN DFA-MIN
    for stare in range(nr_stari):       #PARCURG STARILE
        gasit=0
        for copie_stare in range(stare):
            if dictionar_stari_echivalente[stare,copie_stare]==True:
                for grupare in stari_DFA_MIN:
                    if copie_stare in grupare:
                        grupare.add(stare)
                        break
                gasit=1
                break
        if gasit==0:
            stari_DFA_MIN += [{stare}]

    transforma_DFA_in_DFAMIN={}
    for grupare in stari_DFA_MIN:
        calup=tuple(grupare)
        for stare in calup:
            for litera in alfabet:
                if (stare,litera) in tranzitii.keys():
                    for stare_curenta in stari_DFA_MIN:
                        if tranzitii[stare,litera] in stare_curenta:
                            transforma_DFA_in_DFAMIN[calup,litera]=tuple(stare_curenta)
                            break

    #PASUL 3 IN TRANSFORMAREA DFA IN DFA MINIMIZAT:Calcularea starilor ﬁnale si initiale.
    #Starea initiala devine starea ce contine starea initiala a automatului original
    #Starile ﬁnale sunt toate starile compuse din stari ﬁnale

    #STABILESC STAREA INITIALA
    noua_stare_initiala={}
    for stare in stari_DFA_MIN:
        if initiala in stare:
            noua_stare_initiala = stare
            break

    #ADAUG STARILE FINALE IN VECTOR
    noile_stari_finale=[]
    for stare in finale:
        for cop_stare in stari_DFA_MIN:
            if stare in cop_stare and cop_stare not in noile_stari_finale:
                noile_stari_finale.append(cop_stare)
                break

    #PASUL 4 IN TRANSFORMAREA DFA IN DFA MINIMIZAT:ELIMINAREA STARILOR DEAD-END
    #O stare s este dead-end daca nu exista niciun drum de la aceasta stare la o stare ﬁnala.
    for stare in stari_DFA_MIN:
        stare=tuple(stare)
        global ok
        ok = False
        vizitat=[]
        PARCURGERE(stare,noile_stari_finale,alfabet,transforma_DFA_in_DFAMIN,vizitat)
        #parcurg automatul
        if ok==False:       #inseamna ca nu este stare finala si o sterge, pentru ca este DEAD-END
            STERGE_STARE(stare,transforma_DFA_in_DFAMIN,stari_DFA_MIN,alfabet)

    #PASUL 5 IN TRANSFORMAREA DFA IN DFA MINIMIZAT:ELIMINAREA STARILOR NEACCESIBILE
    #O stare S este neaccesibila daca nu exista niciun drum de la starea initala S0 pana la Sk.

    vizitat=[]
    PARCURGERE_TOTALA(tuple(noua_stare_initiala),alfabet,transforma_DFA_in_DFAMIN,vizitat)

    for stare in stari_DFA_MIN:
        if tuple(stare) not in vizitat:             #daca starea nu a fost vizitata inseamna ca e inaccesibila deci o sterge
            sterge(tuple(stare),transforma_DFA_in_DFAMIN,stari_DFA_MIN,alfabet)

    #PASUL 6 IN TRANSFORMEA DFA IN DFA-MINIMIZAT-REDENUMIREA STARILOR
    #CA SI LA TRANSFORMAREA DIN NFA IN DFA, FIECARE STARE VA LUA INDEXUL DIN STARI_DFA_MIN
    initiala=0                                                          #STAREA INITIALA ESTE 0
    for stare in stari_DFA_MIN:             #parcurg starile
        if stare==noua_stare_initiala:
            val_aux=stari_DFA_MIN[0]                #interschimb valorile
            stari_DFA_MIN[0]=stare
            stare=val_aux

    #REDEFINESC STARILE DIN LISTA MEA
    #ALGORITMUL ESTE ACELASI CA LA NFA TO DFA
    for index in range(len(stari_DFA_MIN)):
        for cheie in transforma_DFA_in_DFAMIN.keys():
            if tuple(stari_DFA_MIN[index])==transforma_DFA_in_DFAMIN[cheie]:
                transforma_DFA_in_DFAMIN[cheie]=index
        for litera in alfabet:
            if (tuple(stari_DFA_MIN[index]),litera) in transforma_DFA_in_DFAMIN.keys():
              transforma_DFA_in_DFAMIN[(index,litera)]=transforma_DFA_in_DFAMIN[(tuple(stari_DFA_MIN[index]),litera)]
              del transforma_DFA_in_DFAMIN[(tuple(stari_DFA_MIN[index]),litera)]

        #Redefinesc starile finale

        if stari_DFA_MIN[index] in noile_stari_finale:
            noile_stari_finale.remove(stari_DFA_MIN[index])
            noile_stari_finale.append(index)

        #AFISEZ STARILE REDEFINITE

        print("DENUMIREA VECHE DIN DFA ESTE: ",stari_DFA_MIN," / DENUMIREA NOUA DIN DFA-MINIMAZAT ESTE: ", index)
        stari_DFA_MIN[index]=index
    nr_stari=len(stari_DFA_MIN)
    return transforma_DFA_in_DFAMIN, nr_stari, stari_DFA_MIN, initiala, noile_stari_finale, alfabet
    #returnez automatul

print('TRANSFORMA LNFA IN NFA: ')
nr_stari, lista_stari, nr_litere_alfabet ,alfabet,initiala, nr_stari_finale, finale,nr_tranzitii, tranzitii=Citire_LNFA(fisier_citire_lnfa)
LAMBDA_NFA_IN_NFA, nr_stari, lista_stari, initiala, finale, alfabet=transforma_LNFA_in_NFA(tranzitii,nr_stari,lista_stari,initiala,finale,alfabet)

print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('alfabet: ',alfabet)
print('stare initiala: ',initiala)
print('stari finale: ',finale)
print('tranzitii: ', LAMBDA_NFA_IN_NFA)
print('\n')

print('TRANSFORMA NFA IN DFA: ')
nr_stari, lista_stari, nr_litere_alfabet, alfabet, initiala, nr_stari_finale, finale, nr_tranzitii, tranzitii=Citire_NFA(fisier_citire_nfa)
NFA_IN_DFA, nr_stari, lista_stari, initiala, finale, alfabet=TRANSFORMA_NFA_IN_DFA(tranzitii, nr_stari, lista_stari, initiala, finale,alfabet)

print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('alfabet: ',alfabet)
print('stare initiala: ',initiala)
print('stari finale: ',finale)
print('tranzitii: ', NFA_IN_DFA)
print('\n')

print('TRANSFORMA DFA IN DFA MINIMIZAT: ')
nr_stari, lista_stari, nr_litere_alfabet, alfabet, initiala, nr_stari_finale, finale, nr_tranzitii, tranzitii=Citire_DFA(fisier_citire_dfa)
DFA_IN_DFAMIN, nr_stari, lista_stari, initiala, finale, alfabet=TRANSFORMA_DFA_IN_DFAMIN(tranzitii, nr_stari, lista_stari, initiala, finale, alfabet)

print('nr de stari: ',nr_stari)
print('lista stari: ',lista_stari)
print('alfabet: ',alfabet)
print('stare initiala: ',initiala)
print('stari finale: ',finale)
print('tranzitii: ', DFA_IN_DFAMIN)
print('\n')