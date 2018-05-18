import datetime


class PrzygotujDane:
    """Przekształcanie struktury danych z pliku tekstowego na strukture obslugiwana przez sqlalchemy"""

    def __init__(self, adres_banki, adres_kir):

        self.adres_banki = adres_banki
        self.adres_kir = adres_kir

    def _banki(self):
        """
        :param adres_pliku: adres do pliku
        :return: zwraca dane banku, godziny sesji przychodzacych, godziny sesji wychodzacych
        """
        with open(self.adres_banki) as seb:

            id = 0
            #sprawdzenie godziny kolejne godziny nie sa oznaczone ze to sesja przychodzaca czy wychodzaca
            #wiec kiedy kolejna godzina jest mniejsza od poprzedniej oznacza to ze zaczyna sie sesja wychodzaca
            #spr_godz to zapis ostatniej odczytanej godziny
            spr_godz = 0
            nr_sesji = 1
            #sesja_bool: wartosc True oznacza ze dopisywane godziny sa do sesja_in, False do sesja_out
            sesja_bool=True
            #oczyszczona lista kolejnych wierszy o znaki 'newline'

            SEB_czysty=[line.strip() for line in seb if line.strip()]

            nazwy_bankow = []
            banki_sesja_in = []
            banki_sesja_out = []
            bufor_s_in = dict()
            bufor_s_out = dict()

            for danka in SEB_czysty:
                # sprawdzenie pierwszego znaku w linijce
                # jesli litera to nowy bank, dane sesji sa zerowane
                if danka[0].isalpha():

                    id += 1
                    spr_godz = 0
                    sesja_bool = True
                    nr_sesji = 1
                    nazwy_bankow.append({'id_banku': id, 'nazwa': danka})

                else:

                    godzina, minuta = danka.split(':')
                    dt = datetime.time(int(godzina), int(minuta))

                    if int(godzina) >= spr_godz:

                        if sesja_bool:

                            #format TIME w SQLITE
                            #tworze tymczasowy slownik do update`u slownika buforowego
                            s_tmp={'bank_ses_out_{}'.format(nr_sesji):dt, 'id_banku':id}
                            bufor_s_out.update(s_tmp)
                            spr_godz = int(godzina)

                            if nr_sesji == 3:
                                #trzeba skopiowac slownik zeby stworzyc nowy obiekt a nie nawiazanie do niego
                                #bo jak go dodaje do listy, i zmieniam obiekt podstawowy to ten w liscie sie tez zmienia
                                s_bufor_copy = bufor_s_out.copy()
                                banki_sesja_out.append(s_bufor_copy)

                            nr_sesji += 1

                        else:

                            s_tmp = {'bank_ses_in_{}'.format(nr_sesji):dt, 'id_banku':id}
                            bufor_s_in.update(s_tmp)

                            if nr_sesji == 3:
                                s_bufor_copy = bufor_s_in.copy()
                                banki_sesja_in.append(s_bufor_copy)
                            nr_sesji += 1

                    else:

                        spr_godz = 0
                        nr_sesji = 1
                        s_tmp = {'bank_ses_in_{}'.format(nr_sesji): dt, 'id_banku': id}
                        bufor_s_in.update(s_tmp)
                        sesja_bool = False
                        nr_sesji += 1

        return {'nazwy_bankow': nazwy_bankow, 'banki_ses_in': banki_sesja_in, 'banki_ses_out': banki_sesja_out}

    def _kir(self):

        kir_ses_1=[]
        kir_ses_2=[]
        kir_ses_3=[]

        bufor_sesji = dict()

        sesje={1: kir_ses_1, 2: kir_ses_2, 3: kir_ses_3}
        tryby={1: 'open_ses_{}', 2: 'close_ses_{}', 3: 'execute_ses_{}'}

        nr_kontrolny_trybu=0
        nr_kontrolny_sesji=0

        with open(self.adres_kir) as plik:

            plik_clean = [wiersz.strip() for wiersz in plik if wiersz.strip()]

            for wiersz in plik_clean:

                if len(wiersz) == 1:

                    nr_kontrolny_sesji = int(wiersz)
                    nr_kontrolny_trybu = 0

                else:

                    godzina, minuta = wiersz.split(':')
                    nr_kontrolny_trybu += 1
                    bufor_sesji.update({tryby[nr_kontrolny_trybu].format(nr_kontrolny_sesji):\
                                            datetime.time(int(godzina), int(minuta))})

                    if nr_kontrolny_trybu==3:
                        kopia_bufora = bufor_sesji.copy()
                        sesje[nr_kontrolny_sesji].append(kopia_bufora)

        return {'kir_ses_1': kir_ses_1, 'kir_ses_2': kir_ses_2, 'kir_ses_3': kir_ses_3}

    def banki_lista(self):
        with open(self.adres_banki) as plik:
            return [wiersz.strip() for wiersz in plik if wiersz.strip() and wiersz.strip()[0].isalpha()]

    def dane_sql(self):
        dane_skul = dict()
        dane_skul.update(self._banki())
        dane_skul.update(self._kir())
        return dane_skul