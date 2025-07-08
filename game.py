import pygame

class Game:
    def __init__(self, okno):
        self.okno = okno
        self.szerokosc = 4
        self.wysokosc = 4
        self.rozmiar_kafelka = 100
        self.odstep = 10
        self.plansza = [[0 for _ in range(self.szerokosc)] for _ in range(self.wysokosc)]
        self.punkty = 0
        self.czcionka = pygame.font.SysFont("arial", 32)
        self.czcionka_duza = pygame.font.SysFont("arial", 48, bold=True)
        self.koniec = False
        self.wygrana = False
        self.resetuj_gre()

    def resetuj_gre(self):
        self.plansza = [[0 for _ in range(self.szerokosc)] for _ in range(self.wysokosc)]
        self.punkty = 0
        self.koniec = False
        self.wygrana = False
        self.dodaj_nowy_kafelek()
        self.dodaj_nowy_kafelek()

    def dodaj_nowy_kafelek(self):
        import random
        puste = [(r, c) for r in range(self.wysokosc) for c in range(self.szerokosc) if self.plansza[r][c] == 0]
        if puste:
            r, c = random.choice(puste)
            self.plansza[r][c] = 2 if random.random() < 0.9 else 4

    def przetworz_zdarzenie(self, zdarzenie):
        if self.koniec or self.wygrana:
            if zdarzenie.type == pygame.KEYDOWN and zdarzenie.key == pygame.K_r:
                self.resetuj_gre()
            return

        if zdarzenie.type == pygame.KEYDOWN:
            if zdarzenie.key == pygame.K_LEFT:
                self.ruch_lewo()
            elif zdarzenie.key == pygame.K_RIGHT:
                self.ruch_prawo()
            elif zdarzenie.key == pygame.K_UP:
                self.ruch_gora()
            elif zdarzenie.key == pygame.K_DOWN:
                self.ruch_dol()

    def aktualizuj(self):
        if not self.koniec and not self.wygrana:
            if self.czy_wygrana():
                self.wygrana = True
            elif not self.czy_mozliwy_ruch():
                self.koniec = True

    def rysuj(self):
        self.okno.fill((187, 173, 160))
        for r in range(self.wysokosc):
            for c in range(self.szerokosc):
                wartosc = self.plansza[r][c]
                kolor = (205, 193, 180) if wartosc == 0 else (238, 228, 218)
                x = c * (self.rozmiar_kafelka + self.odstep) + self.odstep
                y = r * (self.rozmiar_kafelka + self.odstep) + self.odstep + 100
                pygame.draw.rect(self.okno, kolor, (x, y, self.rozmiar_kafelka, self.rozmiar_kafelka), border_radius=8)
                if wartosc:
                    tekst = self.czcionka.render(str(wartosc), True, (119, 110, 101))
                    tekst_rect = tekst.get_rect(center=(x + self.rozmiar_kafelka // 2, y + self.rozmiar_kafelka // 2))
                    self.okno.blit(tekst, tekst_rect)
        # Wyświetlanie punktów
        punkty_tekst = self.czcionka.render(f"Punkty: {self.punkty}", True, (119, 110, 101))
        self.okno.blit(punkty_tekst, (10, 30))

        # Komunikaty końca gry
        if self.koniec:
            self.wyswietl_komunikat("Koniec gry!", "Naciśnij R aby zagrać ponownie")
        elif self.wygrana:
            self.wyswietl_komunikat("Wygrałeś!", "Naciśnij R aby zagrać ponownie")

    def wyswietl_komunikat(self, tekst1, tekst2):
        overlay = pygame.Surface(self.okno.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.okno.blit(overlay, (0, 0))
        t1 = self.czcionka_duza.render(tekst1, True, (119, 110, 101))
        t2 = self.czcionka.render(tekst2, True, (119, 110, 101))
        rect1 = t1.get_rect(center=(self.okno.get_width() // 2, self.okno.get_height() // 2 - 30))
        rect2 = t2.get_rect(center=(self.okno.get_width() // 2, self.okno.get_height() // 2 + 30))
        self.okno.blit(t1, rect1)
        self.okno.blit(t2, rect2)

    def ruch_lewo(self):
        zmieniono = False
        for r in range(self.wysokosc):
            wiersz = [v for v in self.plansza[r] if v != 0]
            nowy_wiersz = []
            i = 0
            while i < len(wiersz):
                if i + 1 < len(wiersz) and wiersz[i] == wiersz[i + 1]:
                    nowy_wiersz.append(wiersz[i] * 2)
                    self.punkty += wiersz[i] * 2
                    i += 2
                    zmieniono = True
                else:
                    nowy_wiersz.append(wiersz[i])
                    i += 1
            nowy_wiersz += [0] * (self.szerokosc - len(nowy_wiersz))
            if nowy_wiersz != self.plansza[r]:
                zmieniono = True
            self.plansza[r] = nowy_wiersz
        if zmieniono:
            self.dodaj_nowy_kafelek()

    def ruch_prawo(self):
        self.odwroc_plansze()
        self.ruch_lewo()
        self.odwroc_plansze()

    def ruch_gora(self):
        self.transponuj_plansze()
        self.ruch_lewo()
        self.transponuj_plansze()

    def ruch_dol(self):
        self.transponuj_plansze()
        self.ruch_prawo()
        self.transponuj_plansze()

    def odwroc_plansze(self):
        for r in range(self.wysokosc):
            self.plansza[r] = self.plansza[r][::-1]

    def transponuj_plansze(self):
        self.plansza = [list(w) for w in zip(*self.plansza)]

    def czy_wygrana(self):
        for r in range(self.wysokosc):
            for c in range(self.szerokosc):
                if self.plansza[r][c] == 2048:
                    return True
        return False

    def czy_mozliwy_ruch(self):
        # Czy są puste pola?
        for r in range(self.wysokosc):
            for c in range(self.szerokosc):
                if self.plansza[r][c] == 0:
                    return True
        # Czy są możliwe połączenia?
        for r in range(self.wysokosc):
            for c in range(self.szerokosc - 1):
                if self.plansza[r][c] == self.plansza[r][c + 1]:
                    return True
        for c in range(self.szerokosc):
            for r in range(self.wysokosc - 1):
                if self.plansza[r][c] == self.plansza[r + 1][c]:
                    return True
        return False