from bbs import kocka
from structures import *

def main():
    igra_je_krenula = False
    print('Igrate igru Ne ljuti se čoveče!')
    i = 0

    while True:
        print('____MENI____')
        print('1. Inicijalizacija')
        print('2. Prikaz')
        print('3. Odigraj potez')
        print('4. Kraj igre')
        try:
            x = int(input())
        except:
            print('Nevalidan unos')
            continue

        if x == 1 and not igra_je_krenula:
            broj_igraca = int(input('Broj igrača (2-4): '))
            while broj_igraca < 2 or broj_igraca > 4:
                broj_igraca = int(input('Unesite broj između 2 i 4: '))
            n = int(input('Veličina table (neparan >6): '))
            while n % 2 == 0 or n < 7:
                n = int(input('Unesite neparan broj >6: '))
            v, c, r = napravi_vcr(n)
            igraci = inicijalizuj_igrace(broj_igraca)
            igra_je_krenula = True
        elif x == 2 and igra_je_krenula:
            iz_vcr_u_matricu(v, c, r, n)
            for idx, igrac in enumerate(igraci):
                print(f"Igrac {idx+1}: {igrac}")
        elif x == 3 and igra_je_krenula:
            igrac = i % broj_igraca
            id_figura = ['a', 'b', 'c', 'd']
            print(f'Igrač {igrac+1} je na potezu')
            if id_figura[igrac] not in ''.join(v):
                print('Bacate kockicu 3 puta...')
                for _ in range(3):
                    input()
                    koraci = kocka()
                    print(f'Dobili ste {koraci}')
                    if koraci == 6:
                        if izbaci_na_teren(v, c, r, n, igrac, igraci):
                            print('Izbačena figura!')
                        else:
                            print('Ne može se izbaciti!')
                        break
                i += 1
            else:
                input('Bacite kockicu...')
                koraci = kocka()
                print(f'Dobili ste {koraci}')
                if koraci == 6:
                    izbor = input("Želite li da izbacite figuru (da/ne): ").lower()
                    if izbor == 'da' and izbaci_na_teren(v, c, r, n, igrac, igraci):
                        i += 1
                        continue

                figure_na_talonu = [id_figura[igrac] + str(k) for k in range(5) if id_figura[igrac] + str(k) in v]
                moguci_potezi = [pomeri_figuru(v, c, r, n, f, koraci) for f in figure_na_talonu]
                moguce_figure = [f for f, idx in zip(figure_na_talonu, moguci_potezi) if idx != -1]
                if not moguce_figure:
                    print('Nema mogućih poteza')
                    i += 1
                    continue

                print('Odaberite figuru:', *moguce_figure)
                figura_koja_se_pomera = input()
                while figura_koja_se_pomera not in moguce_figure:
                    figura_koja_se_pomera = input('Ponovite unos: ')
                idx = moguce_figure.index(figura_koja_se_pomera)
                cilj = moguci_potezi[idx]
                if v[cilj][0] in "abcd":
                    dodajNaKraj(igraci[ord(v[cilj][0]) - ord('a')], ElementListe(v[cilj]))
                v[v.index(figura_koja_se_pomera)] = '0'
                v[cilj] = figura_koja_se_pomera
                if kraj_igre(v, c, r, n, igraci, igrac):
                    print(f'Pobedio je igrač {igrac+1}')
                    break
                i += 1
            iz_vcr_u_matricu(v, c, r, n)
        elif x == 4:
            print('Kraj igre.')
            break
        else:
            print('Morate prvo inicijalizovati igru!')

if __name__ == "__main__":
    main()
