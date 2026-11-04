-- =====================================================================
-- Model bazy danych systemu rezerwacji i ewidencji sklepu warzywnego
-- MySQL Community Server 8.4 LTS, InnoDB, utf8mb4
--
-- Plik odpowiada rozdziałowi „Model bazy danych” sprawozdania (słownik danych).
-- Służy do odtworzenia diagramu ERD w Visual Paradigm (baza/README.md).
-- Tabele aplikacji docelowo tworzą migracje Django (Meta.db_table = nazwy poniżej);
-- tabele auth_* tworzy django.contrib.auth i odtworzono je tu w postaci z Django 5.2.
-- Uruchamiać na osobnej bazie testowej — skrypt usuwa i tworzy tabele od nowa.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS warzywniak_model
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_pl_0900_ai_ci;
USE warzywniak_model;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS rozliczenie_zaleglosci;
DROP TABLE IF EXISTS ubytek;
DROP TABLE IF EXISTS pozycja_sprzedazy;
DROP TABLE IF EXISTS sprzedaz;
DROP TABLE IF EXISTS pozycja_rezerwacji;
DROP TABLE IF EXISTS rezerwacja;
DROP TABLE IF EXISTS pozycja_dostawy;
DROP TABLE IF EXISTS dostawa;
DROP TABLE IF EXISTS plan_dostawy;
DROP TABLE IF EXISTS cena_produktu;
DROP TABLE IF EXISTS produkt;
DROP TABLE IF EXISTS profil_klienta;
DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_user;
SET FOREIGN_KEY_CHECKS = 1;

-- ---------------------------------------------------------------------
-- Konta i role (django.contrib.auth)
-- ---------------------------------------------------------------------

-- Konto użytkownika: personel i klienci. Unikalność adresu e-mail (WF login)
-- sprawdzają formularze aplikacji, bo tabela Django nie ma na nim ograniczenia.
CREATE TABLE auth_user (
	id           INT          NOT NULL AUTO_INCREMENT,
	password     VARCHAR(128) NOT NULL,
	last_login   DATETIME(6)  NULL,
	is_superuser BOOL         NOT NULL,
	username     VARCHAR(150) NOT NULL,
	first_name   VARCHAR(150) NOT NULL,
	last_name    VARCHAR(150) NOT NULL,
	email        VARCHAR(254) NOT NULL,
	is_staff     BOOL         NOT NULL,
	is_active    BOOL         NOT NULL,
	date_joined  DATETIME(6)  NOT NULL,
	CONSTRAINT pk_auth_user PRIMARY KEY (id),
	CONSTRAINT uq_auth_user_username UNIQUE (username)
) ENGINE = InnoDB;

-- Rola: klient, sprzedawca, właściciel.
CREATE TABLE auth_group (
	id   INT          NOT NULL AUTO_INCREMENT,
	name VARCHAR(150) NOT NULL,
	CONSTRAINT pk_auth_group PRIMARY KEY (id),
	CONSTRAINT uq_auth_group_name UNIQUE (name)
) ENGINE = InnoDB;

-- Przypisanie roli do konta. Dokładnie jedną rolę na konto pilnuje aplikacja.
CREATE TABLE auth_user_groups (
	id       BIGINT NOT NULL AUTO_INCREMENT,
	user_id  INT    NOT NULL,
	group_id INT    NOT NULL,
	CONSTRAINT pk_auth_user_groups PRIMARY KEY (id),
	CONSTRAINT uq_auth_user_groups UNIQUE (user_id, group_id),
	CONSTRAINT fk_aug_user  FOREIGN KEY (user_id)  REFERENCES auth_user (id),
	CONSTRAINT fk_aug_group FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE = InnoDB;

-- Dane klienta spoza auth_user (WN3). Klucz główny = klucz obcy konta (związek 1:1).
CREATE TABLE profil_klienta (
	uzytkownik_id       INT         NOT NULL,
	telefon             VARCHAR(20) NOT NULL,
	identyfikator_karty VARCHAR(64) NULL,
	CONSTRAINT pk_profil_klienta PRIMARY KEY (uzytkownik_id),
	CONSTRAINT uq_profil_karta UNIQUE (identyfikator_karty),
	CONSTRAINT fk_profil_uzytkownik FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id),
	INDEX ix_profil_telefon (telefon)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Asortyment i plan dostawy
-- ---------------------------------------------------------------------

CREATE TABLE produkt (
	id                   BIGINT       NOT NULL AUTO_INCREMENT,
	nazwa                VARCHAR(60)  NOT NULL,
	odmiana              VARCHAR(60)  NOT NULL DEFAULT '',
	standardowa_ilosc_kg DECIMAL(7,2) NOT NULL,
	w_ofercie            BOOL         NOT NULL DEFAULT TRUE,
	CONSTRAINT pk_produkt PRIMARY KEY (id),
	CONSTRAINT uq_produkt_nazwa_odmiana UNIQUE (nazwa, odmiana),
	CONSTRAINT ck_produkt_standardowa CHECK (standardowa_ilosc_kg >= 0)
) ENGINE = InnoDB;

-- Historia cen: cena obowiązuje od podanego dnia do dnia przed kolejną zmianą.
CREATE TABLE cena_produktu (
	id            BIGINT       NOT NULL AUTO_INCREMENT,
	produkt_id    BIGINT       NOT NULL,
	cena_za_kg    DECIMAL(7,2) NOT NULL,
	obowiazuje_od DATE         NOT NULL,
	CONSTRAINT pk_cena_produktu PRIMARY KEY (id),
	CONSTRAINT uq_cena_produkt_od UNIQUE (produkt_id, obowiazuje_od),
	CONSTRAINT fk_cena_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT ck_cena_dodatnia CHECK (cena_za_kg > 0)
) ENGINE = InnoDB;

-- Plan dostawy produktu na dzień = pula rezerwacji. Wiersz powstaje przy pierwszej
-- zmianie planu albo pierwszej rezerwacji; do tego czasu plan = standardowa_ilosc_kg.
-- Wiersz blokuje się (SELECT ... FOR UPDATE) przy składaniu rezerwacji (p. 3.3.2).
CREATE TABLE plan_dostawy (
	id         BIGINT       NOT NULL AUTO_INCREMENT,
	produkt_id BIGINT       NOT NULL,
	dzien      DATE         NOT NULL,
	ilosc_kg   DECIMAL(7,2) NOT NULL,
	CONSTRAINT pk_plan_dostawy PRIMARY KEY (id),
	CONSTRAINT uq_plan_produkt_dzien UNIQUE (produkt_id, dzien),
	CONSTRAINT fk_plan_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT ck_plan_ilosc CHECK (ilosc_kg >= 0)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Ewidencja: dostawy, sprzedaż, ubytki
-- ---------------------------------------------------------------------

-- Jedna dostawa dziennie.
CREATE TABLE dostawa (
	id              BIGINT      NOT NULL AUTO_INCREMENT,
	dzien           DATE        NOT NULL,
	zarejestrowano  DATETIME(6) NOT NULL,
	zarejestrowal_id INT        NOT NULL,
	CONSTRAINT pk_dostawa PRIMARY KEY (id),
	CONSTRAINT uq_dostawa_dzien UNIQUE (dzien),
	CONSTRAINT fk_dostawa_uzytkownik FOREIGN KEY (zarejestrowal_id) REFERENCES auth_user (id)
) ENGINE = InnoDB;

CREATE TABLE pozycja_dostawy (
	id         BIGINT       NOT NULL AUTO_INCREMENT,
	dostawa_id BIGINT       NOT NULL,
	produkt_id BIGINT       NOT NULL,
	ilosc_kg   DECIMAL(7,2) NOT NULL,
	CONSTRAINT pk_pozycja_dostawy PRIMARY KEY (id),
	CONSTRAINT uq_pozycja_dostawy UNIQUE (dostawa_id, produkt_id),
	CONSTRAINT fk_pd_dostawa FOREIGN KEY (dostawa_id) REFERENCES dostawa (id),
	CONSTRAINT fk_pd_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT ck_pd_ilosc CHECK (ilosc_kg >= 0)
) ENGINE = InnoDB;

CREATE TABLE ubytek (
	id               BIGINT       NOT NULL AUTO_INCREMENT,
	produkt_id       BIGINT       NOT NULL,
	masa_kg          DECIMAL(7,2) NOT NULL,
	data_czas        DATETIME(6)  NOT NULL,
	zarejestrowal_id INT          NOT NULL,
	CONSTRAINT pk_ubytek PRIMARY KEY (id),
	CONSTRAINT fk_ubytek_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT fk_ubytek_uzytkownik FOREIGN KEY (zarejestrowal_id) REFERENCES auth_user (id),
	CONSTRAINT ck_ubytek_masa CHECK (masa_kg > 0),
	INDEX ix_ubytek_data (data_czas)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Rezerwacje
-- ---------------------------------------------------------------------

-- Stany: zlozona, przygotowana, odebrana, anulowana, nieodebrana (graf stanów, p. 6.7).
-- aktywny_klient_id ma wartość tylko dla rezerwacji niezakończonej, więc unikalność
-- (aktywny_klient_id, dzien_odbioru) dopuszcza jedną niezakończoną rezerwację klienta na dzień,
-- a anulowanych na ten sam dzień — dowolnie wiele (WF proc-zlozenie).
CREATE TABLE rezerwacja (
	id                     BIGINT       NOT NULL AUTO_INCREMENT,
	klient_id              INT          NOT NULL,
	dzien_odbioru          DATE         NOT NULL,
	stan                   VARCHAR(12)  NOT NULL DEFAULT 'zlozona',
	zlozono                DATETIME(6)  NOT NULL,
	zmieniono              DATETIME(6)  NOT NULL,
	oplata_za_nieodebranie DECIMAL(7,2) NULL,
	aktywny_klient_id      INT GENERATED ALWAYS AS
		(CASE WHEN stan IN ('zlozona', 'przygotowana') THEN klient_id END) STORED,
	CONSTRAINT pk_rezerwacja PRIMARY KEY (id),
	CONSTRAINT uq_rezerwacja_aktywna UNIQUE (aktywny_klient_id, dzien_odbioru),
	CONSTRAINT fk_rezerwacja_klient FOREIGN KEY (klient_id) REFERENCES profil_klienta (uzytkownik_id),
	CONSTRAINT ck_rezerwacja_stan
		CHECK (stan IN ('zlozona', 'przygotowana', 'odebrana', 'anulowana', 'nieodebrana')),
	CONSTRAINT ck_rezerwacja_oplata CHECK (
		(stan = 'nieodebrana' AND oplata_za_nieodebranie IS NOT NULL AND oplata_za_nieodebranie >= 0)
		OR (stan <> 'nieodebrana' AND oplata_za_nieodebranie IS NULL)),
	INDEX ix_rezerwacja_dzien_stan (dzien_odbioru, stan)
) ENGINE = InnoDB;

-- Łączną masę rezerwacji (≤ 20 kg) i pulę planu dostawy sprawdza aplikacja w transakcji.
CREATE TABLE pozycja_rezerwacji (
	id               BIGINT       NOT NULL AUTO_INCREMENT,
	rezerwacja_id    BIGINT       NOT NULL,
	produkt_id       BIGINT       NOT NULL,
	ilosc_kg         DECIMAL(4,1) NOT NULL,
	masa_odwazona_kg DECIMAL(6,2) NULL,
	CONSTRAINT pk_pozycja_rezerwacji PRIMARY KEY (id),
	CONSTRAINT uq_pozycja_rezerwacji UNIQUE (rezerwacja_id, produkt_id),
	CONSTRAINT fk_pr_rezerwacja FOREIGN KEY (rezerwacja_id) REFERENCES rezerwacja (id),
	CONSTRAINT fk_pr_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT ck_pr_ilosc CHECK (ilosc_kg > 0 AND ilosc_kg <= 20),
	CONSTRAINT ck_pr_masa CHECK (masa_odwazona_kg IS NULL OR masa_odwazona_kg >= 0)
) ENGINE = InnoDB;

-- Sprzedaż przy ladzie albo wydanie rezerwacji (rezerwacja_id ustawione).
CREATE TABLE sprzedaz (
	id            BIGINT      NOT NULL AUTO_INCREMENT,
	data_czas     DATETIME(6) NOT NULL,
	sprzedawca_id INT         NOT NULL,
	rezerwacja_id BIGINT      NULL,
	CONSTRAINT pk_sprzedaz PRIMARY KEY (id),
	CONSTRAINT uq_sprzedaz_rezerwacja UNIQUE (rezerwacja_id),
	CONSTRAINT fk_sprzedaz_sprzedawca FOREIGN KEY (sprzedawca_id) REFERENCES auth_user (id),
	CONSTRAINT fk_sprzedaz_rezerwacja FOREIGN KEY (rezerwacja_id) REFERENCES rezerwacja (id),
	INDEX ix_sprzedaz_data (data_czas)
) ENGINE = InnoDB;

-- cena_za_kg: cena obowiązująca w chwili sprzedaży (fakt historyczny, nie kopia ceny bieżącej).
CREATE TABLE pozycja_sprzedazy (
	id          BIGINT       NOT NULL AUTO_INCREMENT,
	sprzedaz_id BIGINT       NOT NULL,
	produkt_id  BIGINT       NOT NULL,
	masa_kg     DECIMAL(6,2) NOT NULL,
	cena_za_kg  DECIMAL(7,2) NOT NULL,
	CONSTRAINT pk_pozycja_sprzedazy PRIMARY KEY (id),
	CONSTRAINT uq_pozycja_sprzedazy UNIQUE (sprzedaz_id, produkt_id),
	CONSTRAINT fk_ps_sprzedaz FOREIGN KEY (sprzedaz_id) REFERENCES sprzedaz (id),
	CONSTRAINT fk_ps_produkt FOREIGN KEY (produkt_id) REFERENCES produkt (id),
	CONSTRAINT ck_ps_masa CHECK (masa_kg > 0),
	CONSTRAINT ck_ps_cena CHECK (cena_za_kg > 0)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Rozliczenia zaległości
-- ---------------------------------------------------------------------

-- Wpłata w sklepie (zawsze skuteczna) albo wynik comiesięcznego obciążenia karty.
-- Zaległość klienta = suma opłat za nieodebranie − suma skutecznych rozliczeń.
CREATE TABLE rozliczenie_zaleglosci (
	id               BIGINT       NOT NULL AUTO_INCREMENT,
	klient_id        INT          NOT NULL,
	rodzaj           VARCHAR(10)  NOT NULL,
	kwota            DECIMAL(8,2) NOT NULL,
	skuteczne        BOOL         NOT NULL,
	data_czas        DATETIME(6)  NOT NULL,
	zarejestrowal_id INT          NOT NULL,
	CONSTRAINT pk_rozliczenie PRIMARY KEY (id),
	CONSTRAINT fk_rozliczenie_klient FOREIGN KEY (klient_id) REFERENCES profil_klienta (uzytkownik_id),
	CONSTRAINT fk_rozliczenie_uzytkownik FOREIGN KEY (zarejestrowal_id) REFERENCES auth_user (id),
	CONSTRAINT ck_rozliczenie_rodzaj CHECK (rodzaj IN ('wplata', 'obciazenie')),
	CONSTRAINT ck_rozliczenie_kwota CHECK (kwota > 0),
	CONSTRAINT ck_rozliczenie_wplata CHECK (rodzaj = 'obciazenie' OR skuteczne),
	INDEX ix_rozliczenie_data (data_czas)
) ENGINE = InnoDB;
