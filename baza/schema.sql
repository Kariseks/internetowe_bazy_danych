-- MySQL 8.4.13 • stan po migracjach Django
-- Eksport definicji ze sklepu. Importować do osobnej, pustej bazy.
-- Dane i liczniki rekordów pominięto.
SET NAMES utf8mb4;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `produkt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(60) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `odmiana` varchar(60) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `standardowa_ilosc_kg` decimal(7,2) NOT NULL,
  `ilosc_na_lade_kg` decimal(7,2) NOT NULL,
  `w_ofercie` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_produkt_nazwa_odmiana` (`nazwa`,`odmiana`),
  CONSTRAINT `ck_produkt_plan_lada` CHECK (((`ilosc_na_lade_kg` >= 0) and (`standardowa_ilosc_kg` >= `ilosc_na_lade_kg`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_pl_0900_ai_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `dostawa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dzien` date NOT NULL,
  `zarejestrowano` datetime(6) NOT NULL,
  `zarejestrowal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dzien` (`dzien`),
  KEY `dostawa_zarejestrowal_id_58ea9bf7_fk_auth_user_id` (`zarejestrowal_id`),
  CONSTRAINT `dostawa_zarejestrowal_id_58ea9bf7_fk_auth_user_id` FOREIGN KEY (`zarejestrowal_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `profil_klienta` (
  `uzytkownik_id` int NOT NULL,
  `telefon` varchar(20) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `identyfikator_karty` varchar(64) COLLATE utf8mb4_pl_0900_ai_ci DEFAULT NULL,
  `regulamin_zaakceptowano` datetime(6) NOT NULL,
  `zanonimizowano` datetime(6) DEFAULT NULL,
  `jezyk` varchar(2) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  PRIMARY KEY (`uzytkownik_id`),
  UNIQUE KEY `identyfikator_karty` (`identyfikator_karty`),
  KEY `profil_klienta_telefon_df7e94ea` (`telefon`),
  CONSTRAINT `profil_klienta_uzytkownik_id_5ee274ab_fk_auth_user_id` FOREIGN KEY (`uzytkownik_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `ck_profil_jezyk` CHECK ((`jezyk` in (_utf8mb4'pl',_utf8mb4'en')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `cena_produktu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cena_za_kg` decimal(7,2) NOT NULL,
  `obowiazuje_od` date NOT NULL,
  `produkt_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cena_produkt_od` (`produkt_id`,`obowiazuje_od`),
  CONSTRAINT `cena_produktu_produkt_id_85a40d4e_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `ck_cena_dodatnia` CHECK ((`cena_za_kg` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `korekta_stanu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `roznica_kg` decimal(7,2) NOT NULL,
  `przyczyna` varchar(200) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `data_czas` datetime(6) NOT NULL,
  `zarejestrowal_id` int NOT NULL,
  `produkt_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `korekta_stanu_zarejestrowal_id_7175abb4_fk_auth_user_id` (`zarejestrowal_id`),
  KEY `korekta_stanu_produkt_id_b04e0190_fk_produkt_id` (`produkt_id`),
  KEY `korekta_stanu_data_czas_c9f4616b` (`data_czas`),
  CONSTRAINT `korekta_stanu_produkt_id_b04e0190_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `korekta_stanu_zarejestrowal_id_7175abb4_fk_auth_user_id` FOREIGN KEY (`zarejestrowal_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `ck_korekta_przyczyna` CHECK ((`przyczyna` <> _utf8mb4'')),
  CONSTRAINT `ck_korekta_roznica` CHECK ((`roznica_kg` <> 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `plan_dostawy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dzien` date NOT NULL,
  `ilosc_kg` decimal(7,2) NOT NULL,
  `produkt_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_plan_produkt_dzien` (`produkt_id`,`dzien`),
  CONSTRAINT `plan_dostawy_produkt_id_155fd0ef_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `ck_plan_ilosc` CHECK ((`ilosc_kg` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `ubytek` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `masa_kg` decimal(7,2) NOT NULL,
  `data_czas` datetime(6) NOT NULL,
  `produkt_id` bigint NOT NULL,
  `zarejestrowal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ubytek_data_czas_e9844e90` (`data_czas`),
  KEY `ubytek_produkt_id_02ad6f4d_fk_produkt_id` (`produkt_id`),
  KEY `ubytek_zarejestrowal_id_b0415ae2_fk_auth_user_id` (`zarejestrowal_id`),
  CONSTRAINT `ubytek_produkt_id_02ad6f4d_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `ubytek_zarejestrowal_id_b0415ae2_fk_auth_user_id` FOREIGN KEY (`zarejestrowal_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `ck_ubytek_masa` CHECK ((`masa_kg` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `pozycja_dostawy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ilosc_kg` decimal(7,2) NOT NULL,
  `dostawa_id` bigint NOT NULL,
  `produkt_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pozycja_dostawy` (`dostawa_id`,`produkt_id`),
  KEY `pozycja_dostawy_produkt_id_820625b0_fk_produkt_id` (`produkt_id`),
  CONSTRAINT `pozycja_dostawy_dostawa_id_246161ca_fk_dostawa_id` FOREIGN KEY (`dostawa_id`) REFERENCES `dostawa` (`id`),
  CONSTRAINT `pozycja_dostawy_produkt_id_820625b0_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `ck_pd_ilosc` CHECK ((`ilosc_kg` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `rezerwacja` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dzien_odbioru` date NOT NULL,
  `stan` varchar(12) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `zlozono` datetime(6) NOT NULL,
  `zmieniono` datetime(6) NOT NULL,
  `oplata_za_nieodebranie` decimal(7,2) DEFAULT NULL,
  `aktywny_klient_id` int GENERATED ALWAYS AS ((case when (`stan` in (_utf8mb4'zlozona',_utf8mb4'przygotowana')) then `klient_id` else NULL end)) STORED,
  `klient_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_rezerwacja_aktywna` (`aktywny_klient_id`,`dzien_odbioru`),
  KEY `ix_rezerwacja_dzien_stan` (`dzien_odbioru`,`stan`),
  KEY `rezerwacja_klient_id_03144cc6_fk_profil_klienta_uzytkownik_id` (`klient_id`),
  CONSTRAINT `rezerwacja_klient_id_03144cc6_fk_profil_klienta_uzytkownik_id` FOREIGN KEY (`klient_id`) REFERENCES `profil_klienta` (`uzytkownik_id`),
  CONSTRAINT `ck_rezerwacja_oplata` CHECK ((((`oplata_za_nieodebranie` >= 0) and (`oplata_za_nieodebranie` is not null) and (`stan` = _utf8mb4'nieodebrana')) or ((`stan` <> _utf8mb4'nieodebrana') and (`oplata_za_nieodebranie` is null)))),
  CONSTRAINT `ck_rezerwacja_stan` CHECK ((`stan` in (_utf8mb4'zlozona',_utf8mb4'przygotowana',_utf8mb4'odebrana',_utf8mb4'anulowana',_utf8mb4'nieodebrana')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `rozliczenie_zaleglosci` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rodzaj` varchar(10) COLLATE utf8mb4_pl_0900_ai_ci NOT NULL,
  `kwota` decimal(8,2) NOT NULL,
  `skuteczne` tinyint(1) NOT NULL,
  `data_czas` datetime(6) NOT NULL,
  `klient_id` int NOT NULL,
  `zarejestrowal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rozliczenie_zaleglos_klient_id_c627eab1_fk_profil_kl` (`klient_id`),
  KEY `rozliczenie_zaleglosci_zarejestrowal_id_b404b3a4_fk_auth_user_id` (`zarejestrowal_id`),
  KEY `rozliczenie_zaleglosci_data_czas_e8041bbf` (`data_czas`),
  CONSTRAINT `rozliczenie_zaleglos_klient_id_c627eab1_fk_profil_kl` FOREIGN KEY (`klient_id`) REFERENCES `profil_klienta` (`uzytkownik_id`),
  CONSTRAINT `rozliczenie_zaleglosci_zarejestrowal_id_b404b3a4_fk_auth_user_id` FOREIGN KEY (`zarejestrowal_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `ck_rozliczenie_kwota` CHECK ((`kwota` > 0)),
  CONSTRAINT `ck_rozliczenie_rodzaj` CHECK ((`rodzaj` in (_utf8mb4'wplata',_utf8mb4'obciazenie'))),
  CONSTRAINT `ck_rozliczenie_wplata` CHECK (((`rodzaj` = _utf8mb4'obciazenie') or (`skuteczne` = 0x01)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `pozycja_rezerwacji` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ilosc_kg` decimal(4,1) NOT NULL,
  `masa_odwazona_kg` decimal(6,2) DEFAULT NULL,
  `produkt_id` bigint NOT NULL,
  `rezerwacja_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pozycja_rezerwacji` (`rezerwacja_id`,`produkt_id`),
  KEY `pozycja_rezerwacji_produkt_id_37bedd6a_fk_produkt_id` (`produkt_id`),
  CONSTRAINT `pozycja_rezerwacji_produkt_id_37bedd6a_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `pozycja_rezerwacji_rezerwacja_id_57cd95e0_fk_rezerwacja_id` FOREIGN KEY (`rezerwacja_id`) REFERENCES `rezerwacja` (`id`),
  CONSTRAINT `ck_pr_ilosc` CHECK (((`ilosc_kg` > 0) and (`ilosc_kg` <= 20))),
  CONSTRAINT `ck_pr_masa` CHECK (((`masa_odwazona_kg` >= 0) or (`masa_odwazona_kg` is null)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `sprzedaz` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data_czas` datetime(6) NOT NULL,
  `rezerwacja_id` bigint DEFAULT NULL,
  `sprzedawca_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rezerwacja_id` (`rezerwacja_id`),
  KEY `sprzedaz_data_czas_6ac20c97` (`data_czas`),
  KEY `sprzedaz_sprzedawca_id_5978803a_fk_auth_user_id` (`sprzedawca_id`),
  CONSTRAINT `sprzedaz_rezerwacja_id_51a7b8e0_fk_rezerwacja_id` FOREIGN KEY (`rezerwacja_id`) REFERENCES `rezerwacja` (`id`),
  CONSTRAINT `sprzedaz_sprzedawca_id_5978803a_fk_auth_user_id` FOREIGN KEY (`sprzedawca_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;

CREATE TABLE `pozycja_sprzedazy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `masa_kg` decimal(6,2) NOT NULL,
  `cena_za_kg` decimal(7,2) NOT NULL,
  `produkt_id` bigint NOT NULL,
  `sprzedaz_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pozycja_sprzedazy` (`sprzedaz_id`,`produkt_id`),
  KEY `pozycja_sprzedazy_produkt_id_ec5e6f40_fk_produkt_id` (`produkt_id`),
  CONSTRAINT `pozycja_sprzedazy_produkt_id_ec5e6f40_fk_produkt_id` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `pozycja_sprzedazy_sprzedaz_id_115c28e1_fk_sprzedaz_id` FOREIGN KEY (`sprzedaz_id`) REFERENCES `sprzedaz` (`id`),
  CONSTRAINT `ck_ps_cena` CHECK ((`cena_za_kg` > 0)),
  CONSTRAINT `ck_ps_masa` CHECK ((`masa_kg` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_pl_0900_ai_ci;
