import datetime
import os
import os.path

from sqlalchemy import MetaData, create_engine, Table, Column, Time, Integer, String, ForeignKey
from sqlalchemy.sql import select


class SzkieletDanych:


    def __init__(self, adres_bazy):

        self.meta=MetaData()
        self.adres_bazy=adres_bazy
        self.dane= {
                    'nazwy_bankow': Table('nazwy_bankow', self.meta,
                                    Column('id_banku', Integer(), primary_key=True),
                                    Column('nazwa', String(50))),

                    'banki_ses_in': Table('banki_ses_in', self.meta,
                                    Column('id_sesji', Integer(), primary_key=True),
                                    Column('bank_ses_in_1', Time()),
                                    Column('bank_ses_in_2', Time()),
                                    Column('bank_ses_in_3', Time()),
                                    Column('id_banku', ForeignKey('nazwy_bankow.id_banku'))),

                    'banki_ses_out': Table('banki_ses_out', self.meta,
                                    Column('id_sesji', Integer(), primary_key=True),
                                    Column('bank_ses_out_1', Time()),
                                    Column('bank_ses_out_2', Time()),
                                    Column('bank_ses_out_3', Time()),
                                    Column('id_banku', ForeignKey('nazwy_bankow.id_banku'))),

                    'kir_ses_1': Table('kir_ses_1', self.meta,
                                    Column('ID_S1', Integer(), primary_key=True),
                                    Column('open_ses_1', Time()),
                                    Column('close_ses_1', Time()),
                                    Column('execute_ses_1', Time())),

                    'kir_ses_2': Table('kir_ses_2', self.meta,
                                    Column('ID_S2', Integer(), primary_key=True),
                                    Column('open_ses_2', Time()),
                                    Column('close_ses_2', Time()),
                                    Column('execute_ses_2', Time())),

                    'kir_ses_3': Table('kir_ses_3', self.meta,
                                    Column('ID_S3', Integer(), primary_key=True),
                                    Column('open_ses_3', Time()),
                                    Column('close_ses_3', Time()),
                                    Column('execute_ses_3', Time()))
                    }


    def _tworzenie_bazy(self):

        lokalizacja='sqlite:///{}'.format(self.adres_bazy)
        silnik=create_engine(lokalizacja)
        zaplon=silnik.connect()
        self.meta.create_all(silnik)
        return zaplon

    def stworz_baze(self,dane_sql):
        zaplon = self._tworzenie_bazy()
        for nazwy_tabeli in self.dane.keys():
            table_insertion=self.dane[nazwy_tabeli].insert()
            zaplon.execute(table_insertion, dane_sql[nazwy_tabeli])


class SkulKwery:
    '''Klasa w której przechowywane są kwerendy wyszukujące dane z istniejącej bazy danych.
    '''
    def __init__(self):

        self.__dict__ = {
                        'nazwy_banki' : "SELECT nazwa FROM nazwy_bankow",

                        'sesja_out_bank' : "SELECT "
                        "CASE "
                        "WHEN ('{g_p}' > banki_ses_out.bank_ses_out_3 OR '{g_p}' < banki_ses_out.bank_ses_out_1) "
                                           "THEN banki_ses_out.bank_ses_out_1 "
                        
                        "WHEN '{g_p}' < banki_ses_out.bank_ses_out_2 THEN banki_ses_out.bank_ses_out_2 "
                        "WHEN '{g_p}' < banki_ses_out.bank_ses_out_3 THEN banki_ses_out.bank_ses_out_3 "
                        "END AS G_P "
                        "FROM nazwy_bankow "
                        "INNER JOIN banki_ses_out ON banki_ses_out.id_banku=nazwy_bankow.id_banku "
                        "WHERE nazwy_bankow.nazwa='{b_out}'",

                        'sesja_in_out_kir' : "SELECT DISTINCT "
                        "CASE "
                        "WHEN ('{bank_out}' > kir_ses_1.open_ses_1 OR '{bank_out}' < kir_ses_1.close_ses_1) "
                                             "THEN kir_ses_1.execute_ses_1 "
                        "WHEN '{bank_out}' < kir_ses_2.close_ses_2 THEN kir_ses_2.execute_ses_2 "
                        "WHEN '{bank_out}' < kir_ses_3.close_ses_3 THEN kir_ses_3.execute_ses_3 "
                        "END AS kir_out "
                        "FROM kir_ses_1 "
                        "INNER JOIN kir_ses_2 "
                        "INNER JOIN kir_ses_3",

                        'sesja_in_bank' : "SELECT "
                        "nazwa, "
                        "CASE "
                        "WHEN ('{k_out}' < banki_ses_in.bank_ses_in_1 OR '{k_out}' > banki_ses_in.bank_ses_in_3) "
                                          "THEN banki_ses_in.bank_ses_in_1 "
                        "WHEN '{k_out}' < banki_ses_in.bank_ses_in_2 THEN banki_ses_in.bank_ses_in_2 "
                        "WHEN '{k_out}' < banki_ses_in.bank_ses_in_3 THEN banki_ses_in.bank_ses_in_3 "
                        "END AS banki_in "
                        "FROM nazwy_bankow "
                        "INNER JOIN banki_ses_in ON banki_ses_in.id_banku=nazwy_bankow.id_banku "
                        "WHERE nazwa='{nazwa_banku}'"
                        }

    def zapytanie(self, godzina_przelewu, bank_out, bank_in):
        bank_out_t = self._exec(self._ses_out(godzina_przelewu, bank_out)).fetchall()[0][0]
        kir_out_t = self._exec(self._ses_io_kir(bank_out_t)).fetchall()[0][0]
        bank_in_t = self._exec(self._ses_in(kir_out_t, bank_in)).fetchall()[0][1]
        return bank_out_t[:5], kir_out_t[:5], bank_in_t[:5]

    def wyświetl_banki(self):
        return [nazwa[0] for nazwa in self._exec(self.nazwy_banki)]

    def _adres(self):
        # folder='przelewy/przelewy/dane/'
        # return os.path.join(os.getcwd(), folder)
        return os.getcwd()

    def _exec(self, zlecenie):
        silnik = create_engine('sqlite:///{}/eliksir.db'.format(self._adres()))
        zaplon = silnik.connect()
        return zaplon.execute(zlecenie)

    def _ses_out(self, godzina_przelewu, bank_out):
        return self.sesja_out_bank.format(g_p=godzina_przelewu, b_out=bank_out)

    def _ses_io_kir(self, bank_out_time):
        return self.sesja_in_out_kir.format(bank_out=bank_out_time)

    def _ses_in(self,kir_out_time, bank_in):
        return self.sesja_in_bank.format(k_out=kir_out_time, nazwa_banku=bank_in)