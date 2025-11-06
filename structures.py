class ElementListe:
    def __init__(self, data):
        self.podatak = data
        self.sledeci = None

    def __repr__(self):
        return self.podatak


class Lista:
    def __init__(self):
        self.prvi = None
        self.poslednji = None
        self.br_elem = 0

    def __repr__(self):
        if self.prvi is None:
            return "prazna"
        tek = self.prvi
        lista_ispis = [self.prvi.podatak]
        tek = tek.sledeci
        while tek != self.prvi:
            lista_ispis.append(tek.podatak)
            tek = tek.sledeci
        lista_ispis.append(str(self.prvi))
        return " -> ".join(lista_ispis)


def dodajNaKraj(lista, element):
    if lista.poslednji is not None:
        lista.poslednji.sledeci = element
    else:
        lista.prvi = element
    lista.poslednji = element
    lista.br_elem += 1
    lista.poslednji.sledeci = lista.prvi


def ukloniElementBr(lista, br: int):
    if (lista is None) or (br < 0) or (br >= lista.br_elem):
        return 0
    if lista.prvi == lista.poslednji:
        lista.prvi = None
        lista.br_elem = 0
        return 1
    izbacujemo = lista.prvi
    lista.prvi = izbacujemo.sledeci
    lista.poslednji.sledeci = lista.prvi
    del izbacujemo
    return 1


def inicijalizuj_igrace(broj_igraca):
    figure_igraca = []
    id_figura = ['a', 'b', 'c', 'd']
    for i in range(broj_igraca):
        lista = Lista()
        for j in range(1, 5):
            dodajNaKraj(lista, ElementListe(id_figura[i] + str(j)))
        figure_igraca.append(lista)
    return figure_igraca


def napravi_vcr(n):
    matrica = []
    for i in range(n):
        if not (i == 0) and not (i == n-1):
            matrica.append(["0"] + [' '] * (n-2) + ["0"])
        else:
            matrica.append(["0"] * n)
    for i in range(4):
        matrica[1][1+i] = '_'
        matrica[1+i][n-2] = '_'
        matrica[n-2][n-5+i] = '_'
        matrica[n-5+i][1] = '_'
    v = [1 for _ in range(4*n + 12)]
    c = [1 for _ in range(4*n + 12)]
    r = [1 for _ in range(n+1)]
    brojac = 0
    for vrsta in range(n):
        r[vrsta] = brojac
        for kolona in range(n):
            if not matrica[vrsta][kolona] == ' ':
                v[brojac] = matrica[vrsta][kolona]
                c[brojac] = kolona
                brojac += 1
    r[n] = brojac
    return [v, c, r]


def vrati_vrstu_iz_v(v, r, n, index):
    for i in range(n):
        if (r[i] <= index) and (index < r[i+1]):
            return i


def vrati_index_iz_vrste_i_kolone(v, c, r, n, kolona, vrsta):
    bot = r[vrsta]
    top = r[vrsta+1]
    for i in range(bot, top):
        if c[i] == kolona:
            return i


def izbaci_na_teren(v, c, r, n, igrac, igraci):
    if igrac == 0:
        vrsta, kolona = n-1, 0
    elif igrac == 1:
        vrsta, kolona = 0, 0
    elif igrac == 2:
        vrsta, kolona = 0, n-1
    else:
        vrsta, kolona = n-1, n-1

    index_izbacivanja = vrati_index_iz_vrste_i_kolone(v, c, r, n, kolona, vrsta)
    if v[index_izbacivanja] != '0':
        return False
    v[index_izbacivanja] = igraci[igrac].prvi.podatak
    ukloniElementBr(igraci[igrac], 0)
    return True


def pomeri_figuru_jednom(kolona, vrsta, igrac, n):
    if igrac == 0 and kolona == 1 and n-5 < vrsta < n:
        vrsta -= 1
    elif igrac == 1 and vrsta == 1 and 0 <= kolona < 4:
        kolona += 1
    elif igrac == 2 and kolona == n - 2 and 0 <= vrsta < 4:
        vrsta += 1
    elif igrac == 3 and vrsta == n - 2 and n-5 < kolona <= n-1:
        kolona -= 1
    elif kolona == 0 and 0 < vrsta < n:
        vrsta -= 1
    elif kolona == n-1 and 0 <= vrsta < n - 1:
        vrsta += 1
    elif vrsta == 0 and 0 <= kolona < n - 1:
        kolona += 1
    elif vrsta == n - 1 and 0 < kolona <= n - 1:
        kolona -= 1
    return kolona, vrsta


def pomeri_figuru(v, c, r, n, figura, broj_koraka):
    index = next((i for i in range(r[n]) if figura == v[i]), -1)
    if index == -1:
        return -1
    kolona = c[index]
    vrsta = vrati_vrstu_iz_v(v, r, n, index)
    for _ in range(broj_koraka):
        pr_kolona, pr_vrsta = kolona, vrsta
        kolona, vrsta = pomeri_figuru_jednom(kolona, vrsta, ord(figura[0]) - ord('a'), n)
        if pr_vrsta == vrsta and pr_kolona == kolona:
            return -1
    index = vrati_index_iz_vrste_i_kolone(v, c, r, n, kolona, vrsta)
    if v[index][0] == figura[0]:
        return -1
    return index


def iz_vcr_u_matricu(v, c, r, n):
    matrica = [[" "] * n for _ in range(n)]
    for i in range(r[n]):
        vrsta = vrati_vrstu_iz_v(v, r, n, i)
        kolona = c[i]
        matrica[vrsta][kolona] = v[i]
    for vrsta in matrica:
        print(*vrsta, sep=' ')


def kraj_igre(v, c, r, n, igraci, igrac):
    zone = {
        0: [(1, n-2), (1, n-3), (1, n-4), (1, n-5)],
        1: [(1, 1), (2, 1), (3, 1), (4, 1)],
        2: [(n-2, 1), (n-2, 2), (n-2, 3), (n-2, 4)],
        3: [(n-2, n-2), (n-3, n-2), (n-4, n-2), (n-5, n-2)],
    }
    indeksi = [vrati_index_iz_vrste_i_kolone(v, c, r, n, k, vrs) for k, vrs in zone[igrac]]
    s = ''.join(v[i] for i in indeksi)
    return not any(ch in s for ch in ['0', '_'])
