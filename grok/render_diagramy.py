#!/usr/bin/env python3
"""Kolorowe diagramy z liniami pod kątem prostym (Graphviz, splines=ortho)."""

from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent

NAVY = "#1F4E79"
GREEN = "#2E7D32"
PURPLE = "#6A1B9A"
ORANGE = "#E65100"
RED = "#C62828"
SLATE = "#546E7A"

ONE = "teetee"          # dokładnie jeden
ZERO_ONE = "odottee"    # zero lub jeden
ZERO_MANY = "crowodot"  # zero lub wiele
ONE_MANY = "crowtee"    # jeden lub wiele


FILL = {
    NAVY: "#D6EAF8",
    GREEN: "#E8F5E9",
    PURPLE: "#F3E5F5",
    ORANGE: "#FFF3E0",
    RED: "#FDECEA",
}


def html_box(title, subtitle, rows, color):
    # Zwykły prostokąt, nie tabela HTML: przy splines=ortho Graphviz
    # prowadzi linie przez środek tabeli HTML.
    lines = [title]
    if subtitle:
        lines.append(subtitle)
    lines.append("")
    lines.extend(rows)
    text = "\\l".join(lines) + "\\l"
    return (
        f'label="{text}", shape=box, style=filled, '
        f'fillcolor="{FILL[color]}", color="{color}", penwidth=1.6'
    )


def pk(name, extra=""):
    return f"{name}  PK{extra}"


def attr(name, extra=""):
    return f"{name}{extra}"


def edge(a, b, tail, head, color, **kw):
    opts = [
        f"arrowtail={tail}",
        f"arrowhead={head}",
        f'color="{color}"',
        "dir=both",
    ]
    quoted = {"label", "xlabel", "tailport", "headport"}
    for key, value in kw.items():
        opts.append(f'{key}="{value}"' if key in quoted else f"{key}={value}")
    return f"  {a} -> {b} [{', '.join(opts)}];"


def write_dot(path, body):
    path.write_text(body, encoding="utf-8")


def render(dot_path):
    png = dot_path.with_suffix(".png")
    subprocess.run(
        ["dot", "-Tpng", str(dot_path), "-o", str(png)],
        check=True,
    )
    return png


HEADER = """digraph {{
    graph [
    splines=ortho,
    rankdir=TB,
    nodesep=0.72,
    ranksep=0.78,
    pad=0.4,
    esep=18,
    dpi=140,
    bgcolor="white",
    fontname="DejaVu Sans",
    labeljust=l,
    labelloc=b
  ];
  node [shape=box, fontname="DejaVu Sans", fontsize=11];
  edge [fontname="DejaVu Sans", fontsize=9, penwidth=1.55, arrowsize=0.85];

{nodes}

  // siatka: wiersze
{ranks}

  // porządek w wierszu
{chains}

{edges}

{legend}
}}
"""


def ranks(groups):
    lines = []
    for group in groups:
        inner = "; ".join(group)
        lines.append(f"  {{ rank=same; {inner}; }}")
    return "\n".join(lines)


def node_decl(key, label, group):
    if key.startswith("gap"):
        return f'  {key} [shape=point, style=invis, width=0.2, label="", group="{group}"];'
    return f'  {key} [{label}, group="{group}"];'


def emit_nodes(nodes, groups):
    column = {}
    for row in groups:
        for index, key in enumerate(row):
            column[key] = f"c{index}"
    return "\n".join(
        node_decl(key, label, column.get(key, "c0"))
        for key, label in nodes.items()
    )


def chains(groups):
    lines = []
    for group in groups:
        if len(group) < 2:
            continue
        chain = " -> ".join(group)
        lines.append(f"  {chain} [style=invis, weight=30, arrowhead=none, arrowtail=none, dir=none];")
    # pionowe kotwice kolumn, żeby wiersze nie rozjechały się w lewo
    cols = max(len(g) for g in groups)
    for col in range(cols):
        column = [g[col] for g in groups if col < len(g)]
        if len(column) < 2:
            continue
        chain = " -> ".join(column)
        lines.append(f"  {chain} [style=invis, weight=12, arrowhead=none, arrowtail=none, dir=none];")
    return "\n".join(lines)


def legend_node():
    rows = [
        f'<FONT COLOR="{NAVY}"><B>■</B></FONT> konto i rola',
        f'<FONT COLOR="{GREEN}"><B>■</B></FONT> produkt',
        f'<FONT COLOR="{PURPLE}"><B>■</B></FONT> dostawa, ubytek i korekta stanu',
        f'<FONT COLOR="{ORANGE}"><B>■</B></FONT> rezerwacja',
        f'<FONT COLOR="{RED}"><B>■</B></FONT> sprzedaż i zaległość',
        f'<FONT COLOR="{SLATE}"><B>■</B></FONT> kto zarejestrował',
        "|| dokładnie jeden &nbsp; o zero lub jeden &nbsp; łapka wiele",
    ]
    body = "<BR ALIGN=\"LEFT\"/>".join(rows)
    return f"""  legend [
    label=<
      <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="#B0BEC5" BGCOLOR="#FAFAFA">
        <TR><TD ALIGN="LEFT"><B>Legenda</B><BR ALIGN="LEFT"/>{body}</TD></TR>
      </TABLE>
    >
  ];
  rozliczenie -> legend [style=invis, weight=1, arrowhead=none, arrowtail=none, dir=none];
"""


def conceptual():
    nodes = {
        "auth_group": html_box("Rola", "auth_group", [pk("id"), attr("nazwa", "  UK")], NAVY),
        "aug": html_box("Przypisanie roli", "auth_user_groups", [pk("id"), attr("konto", "  FK"), attr("rola", "  FK")], NAVY),
        "auth_user": html_box("Konto", "auth_user", [pk("id"), attr("username", "  UK"), "imię", "nazwisko", "e-mail", "aktywne"], NAVY),
        "profil": html_box("Profil klienta", "profil_klienta", [pk("konto", " FK"), "telefon", attr("identyfikator karty", "  UK"), "regulamin zaakceptowano", "zanonimizowano"], NAVY),
        "produkt": html_box("Produkt", "produkt", [pk("id"), "nazwa", "odmiana", "standardowa ilość", "ilość na ladę", "w ofercie"], GREEN),
        "cena": html_box("Cena produktu", "cena_produktu", [pk("id"), attr("produkt", "  FK"), "cena za kg", "obowiązuje od"], GREEN),
        "plan": html_box("Plan dostawy", "plan_dostawy", [pk("id"), attr("produkt", "  FK"), "dzień", "ilość"], GREEN),
        "dostawa": html_box("Dostawa", "dostawa", [pk("id"), attr("dzień", "  UK"), "zarejestrowano", attr("zarejestrował", "  FK")], PURPLE),
        "poz_d": html_box("Pozycja dostawy", "pozycja_dostawy", [pk("id"), attr("dostawa", "  FK"), attr("produkt", "  FK"), "ilość"], PURPLE),
        "ubytek": html_box("Ubytek", "ubytek", [pk("id"), attr("produkt", "  FK"), "masa", attr("zarejestrował", "  FK")], PURPLE),
        "korekta": html_box("Korekta stanu", "korekta_stanu", [pk("id"), attr("produkt", "  FK"), "różnica", "przyczyna", attr("zarejestrował", "  FK")], PURPLE),
        "rezerwacja": html_box("Rezerwacja", "rezerwacja", [pk("id"), attr("klient", "  FK"), "dzień odbioru", "stan", "opłata za nieodebranie"], ORANGE),
        "poz_r": html_box("Pozycja rezerwacji", "pozycja_rezerwacji", [pk("id"), attr("rezerwacja", "  FK"), attr("produkt", "  FK"), "ilość", "masa odważona"], ORANGE),
        "sprzedaz": html_box("Sprzedaż", "sprzedaz", [pk("id"), "data i czas", attr("sprzedawca", "  FK"), attr("rezerwacja", "  FK")], RED),
        "poz_s": html_box("Pozycja sprzedaży", "pozycja_sprzedazy", [pk("id"), attr("sprzedaż", "  FK"), attr("produkt", "  FK"), "masa", "cena za kg"], RED),
        "rozliczenie": html_box("Rozliczenie zaległości", "rozliczenie_zaleglosci", [pk("id"), attr("klient", "  FK"), "rodzaj", "kwota", "skuteczne", attr("zarejestrował", "  FK")], RED),
    }
    return nodes


def logical():
    nodes = {
        "auth_group": html_box("auth_group", "", [pk("id : INT"), attr("name : VARCHAR(150)", "  UK")], NAVY),
        "aug": html_box("auth_user_groups", "", [pk("id : BIGINT"), attr("user_id : INT", "  FK"), attr("group_id : INT", "  FK")], NAVY),
        "auth_user": html_box("auth_user", "", [
            pk("id : INT"), "password : VARCHAR(128)", "last_login : DATETIME(6)",
            "is_superuser : BOOL", attr("username : VARCHAR(150)", "  UK"),
            "first_name : VARCHAR(150)", "last_name : VARCHAR(150)", "email : VARCHAR(254)",
            "is_staff : BOOL", "is_active : BOOL", "date_joined : DATETIME(6)",
        ], NAVY),
        "profil": html_box("profil_klienta", "", [pk("uzytkownik_id : INT", " FK"), "telefon : VARCHAR(20)", attr("identyfikator_karty : VARCHAR(64)", "  UK"), "regulamin_zaakceptowano : DATETIME(6)", "zanonimizowano : DATETIME(6)"], NAVY),
        "produkt": html_box("produkt", "", [pk("id : BIGINT"), "nazwa : VARCHAR(60)", "odmiana : VARCHAR(60)", "standardowa_ilosc_kg : DECIMAL(7,2)", "ilosc_na_lade_kg : DECIMAL(7,2)", "w_ofercie : BOOL"], GREEN),
        "cena": html_box("cena_produktu", "", [pk("id : BIGINT"), attr("produkt_id : BIGINT", "  FK"), "cena_za_kg : DECIMAL(7,2)", "obowiazuje_od : DATE"], GREEN),
        "plan": html_box("plan_dostawy", "", [pk("id : BIGINT"), attr("produkt_id : BIGINT", "  FK"), "dzien : DATE", "ilosc_kg : DECIMAL(7,2)"], GREEN),
        "dostawa": html_box("dostawa", "", [pk("id : BIGINT"), attr("dzien : DATE", "  UK"), "zarejestrowano : DATETIME(6)", attr("zarejestrowal_id : INT", "  FK")], PURPLE),
        "poz_d": html_box("pozycja_dostawy", "", [pk("id : BIGINT"), attr("dostawa_id : BIGINT", "  FK"), attr("produkt_id : BIGINT", "  FK"), "ilosc_kg : DECIMAL(7,2)"], PURPLE),
        "ubytek": html_box("ubytek", "", [pk("id : BIGINT"), attr("produkt_id : BIGINT", "  FK"), "masa_kg : DECIMAL(7,2)", "data_czas : DATETIME(6)", attr("zarejestrowal_id : INT", "  FK")], PURPLE),
        "korekta": html_box("korekta_stanu", "", [pk("id : BIGINT"), attr("produkt_id : BIGINT", "  FK"), "roznica_kg : DECIMAL(7,2)", "przyczyna : VARCHAR(200)", "data_czas : DATETIME(6)", attr("zarejestrowal_id : INT", "  FK")], PURPLE),
        "rezerwacja": html_box("rezerwacja", "", [
            pk("id : BIGINT"), attr("klient_id : INT", "  FK"), "dzien_odbioru : DATE",
            "stan : VARCHAR(12)", "zlozono : DATETIME(6)", "zmieniono : DATETIME(6)",
            "oplata_za_nieodebranie : DECIMAL(7,2)", "aktywny_klient_id : INT  wyliczana",
        ], ORANGE),
        "poz_r": html_box("pozycja_rezerwacji", "", [pk("id : BIGINT"), attr("rezerwacja_id : BIGINT", "  FK"), attr("produkt_id : BIGINT", "  FK"), "ilosc_kg : DECIMAL(4,1)", "masa_odwazona_kg : DECIMAL(6,2)"], ORANGE),
        "sprzedaz": html_box("sprzedaz", "", [pk("id : BIGINT"), "data_czas : DATETIME(6)", attr("sprzedawca_id : INT", "  FK"), attr("rezerwacja_id : BIGINT", "  FK UK")], RED),
        "poz_s": html_box("pozycja_sprzedazy", "", [pk("id : BIGINT"), attr("sprzedaz_id : BIGINT", "  FK"), attr("produkt_id : BIGINT", "  FK"), "masa_kg : DECIMAL(6,2)", "cena_za_kg : DECIMAL(7,2)"], RED),
        "rozliczenie": html_box("rozliczenie_zaleglosci", "", [
            pk("id : BIGINT"), attr("klient_id : INT", "  FK"), "rodzaj : VARCHAR(10)",
            "kwota : DECIMAL(8,2)", "skuteczne : BOOL", "data_czas : DATETIME(6)",
            attr("zarejestrowal_id : INT", "  FK"),
        ], RED),
    }
    return nodes


def erd_edges():
    # Krawędź zawsze od lewej do prawej albo z góry na dół.
    # arrowtail jest przy pierwszym węźle, arrowhead przy drugim.
    return "\n".join([
        edge("auth_group", "aug", ONE, ZERO_MANY, NAVY),
        edge("aug", "auth_user", ZERO_MANY, ONE, NAVY),
        edge("auth_user", "profil", ONE, ZERO_ONE, NAVY),
        edge("profil", "rezerwacja", ONE, ZERO_MANY, ORANGE),
        edge("profil", "rozliczenie", ONE, ZERO_MANY, RED),
        edge("cena", "produkt", ONE_MANY, ONE, GREEN),
        edge("plan", "produkt", ZERO_MANY, ONE, GREEN),
        edge("produkt", "poz_d", ONE, ZERO_MANY, GREEN),
        edge("produkt", "ubytek", ONE, ZERO_MANY, GREEN),
        edge("produkt", "korekta", ONE, ZERO_MANY, GREEN, constraint="false"),
        edge("produkt", "poz_r", ONE, ZERO_MANY, GREEN),
        edge("produkt", "poz_s", ONE, ZERO_MANY, GREEN, tailport="e", headport="w"),
        edge("poz_d", "dostawa", ONE_MANY, ONE, PURPLE),
        edge("rezerwacja", "poz_r", ONE, ONE_MANY, ORANGE),
        edge("rezerwacja", "sprzedaz", ZERO_ONE, ZERO_ONE, RED),
        edge("sprzedaz", "poz_s", ONE, ZERO_MANY, RED),
        edge("auth_user", "dostawa", ONE, ZERO_MANY, SLATE, constraint="false"),
        edge("auth_user", "ubytek", ONE, ZERO_MANY, SLATE, constraint="false"),
        edge("auth_user", "korekta", ONE, ZERO_MANY, SLATE, constraint="false"),
        edge("auth_user", "sprzedaz", ONE, ZERO_MANY, SLATE, constraint="false"),
        edge("auth_user", "rozliczenie", ONE, ZERO_MANY, SLATE, constraint="false"),
    ])


def erd(name, nodes):
    groups = [
        ["auth_group", "aug", "auth_user", "profil"],
        ["plan", "cena", "produkt", "rezerwacja"],
        ["poz_d", "ubytek", "poz_r", "sprzedaz"],
        ["dostawa", "korekta", "rozliczenie", "poz_s"],
    ]
    nodes = dict(nodes)
    node_lines = emit_nodes(nodes, groups)
    body = HEADER.format(
        nodes=node_lines,
        ranks=ranks(groups),
        chains=chains(groups),
        edges=erd_edges(),
        legend=legend_node(),
    )
    path = OUT / f"{name}.dot"
    write_dot(path, body)
    return render(path)


def class_box(name, rows, color, stereotype=""):
    title = name if not stereotype else f"{name}"
    sub = stereotype
    return html_box(title, sub, rows, color)


def class_diagram():
    nodes = {
        "Group": class_box("Group", [pk("id : AutoField"), attr("name : CharField", "  UK")], NAVY, "Django"),
        "User": class_box("User", [
            pk("id : AutoField"), "username : CharField  UK", "email : EmailField",
            "first_name : CharField", "last_name : CharField", "is_staff : BooleanField",
            "is_active : BooleanField",
        ], NAVY, "Django"),
        "Profil": class_box("ProfilKlienta", [pk("uzytkownik : OneToOneField"), "telefon : CharField", "identyfikator_karty : CharField", "regulamin_zaakceptowano : DateTimeField", "zanonimizowano : DateTimeField"], NAVY),
        "Produkt": class_box("Produkt", [pk("id : BigAutoField"), "nazwa : CharField", "odmiana : CharField", "standardowa_ilosc_kg : DecimalField", "ilosc_na_lade_kg : DecimalField", "w_ofercie : BooleanField"], GREEN),
        "Cena": class_box("CenaProduktu", [pk("id : BigAutoField"), "produkt : ForeignKey", "cena_za_kg : DecimalField", "obowiazuje_od : DateField"], GREEN),
        "Plan": class_box("PlanDostawy", [pk("id : BigAutoField"), "produkt : ForeignKey", "dzien : DateField", "ilosc_kg : DecimalField"], GREEN),
        "Dostawa": class_box("Dostawa", [pk("id : BigAutoField"), attr("dzien : DateField", "  UK"), "zarejestrowano : DateTimeField", "zarejestrowal : ForeignKey"], PURPLE),
        "PozD": class_box("PozycjaDostawy", [pk("id : BigAutoField"), "dostawa : ForeignKey", "produkt : ForeignKey", "ilosc_kg : DecimalField"], PURPLE),
        "Ubytek": class_box("Ubytek", [pk("id : BigAutoField"), "produkt : ForeignKey", "masa_kg : DecimalField", "zarejestrowal : ForeignKey"], PURPLE),
        "Korekta": class_box("KorektaStanu", [pk("id : BigAutoField"), "produkt : ForeignKey", "roznica_kg : DecimalField", "przyczyna : CharField", "zarejestrowal : ForeignKey"], PURPLE),
        "Rezerwacja": class_box("Rezerwacja", [pk("id : BigAutoField"), "klient : ForeignKey", "dzien_odbioru : DateField", "stan : StanRezerwacji", "oplata_za_nieodebranie : DecimalField"], ORANGE),
        "Stan": class_box("StanRezerwacji", ["zlozona", "przygotowana", "odebrana", "anulowana", "nieodebrana"], ORANGE, "enum"),
        "PozR": class_box("PozycjaRezerwacji", [pk("id : BigAutoField"), "rezerwacja : ForeignKey", "produkt : ForeignKey", "ilosc_kg : DecimalField", "masa_odwazona_kg : DecimalField"], ORANGE),
        "Sprzedaz": class_box("Sprzedaz", [pk("id : BigAutoField"), "data_czas : DateTimeField", "sprzedawca : ForeignKey", "rezerwacja : ForeignKey"], RED),
        "PozS": class_box("PozycjaSprzedazy", [pk("id : BigAutoField"), "sprzedaz : ForeignKey", "produkt : ForeignKey", "masa_kg : DecimalField", "cena_za_kg : DecimalField"], RED),
        "Rozl": class_box("RozliczenieZaleglosci", [pk("id : BigAutoField"), "klient : ForeignKey", "rodzaj : CharField", "kwota : DecimalField", "skuteczne : BooleanField", "zarejestrowal : ForeignKey"], RED),
    }
    groups = [
        ["gap0", "Group", "User", "Profil"],
        ["Plan", "Cena", "Produkt", "Rezerwacja", "Stan"],
        ["PozD", "Ubytek", "PozR", "Sprzedaz"],
        ["Dostawa", "Korekta", "Rozl", "PozS"],
    ]

    def link(a, b, color, left, right, **kw):
        extra = ""
        for key, value in kw.items():
            extra += f", {key}={value}"
        return (
            f'  {a} -> {b} [dir=none, color="{color}", '
            f'taillabel="{left}", headlabel="{right}", '
            f'fontcolor="{color}", fontsize=11, penwidth=1.55, '
            f'labeldistance=2.6, labelangle=0{extra}];'
        )

    edges = "\n".join([
        link("Group", "User", NAVY, "0..*", "0..*"),
        link("User", "Profil", NAVY, "1", "0..1"),
        link("Cena", "Produkt", GREEN, "1..*", "1"),
        link("Plan", "Produkt", GREEN, "0..*", "1"),
        link("Produkt", "PozD", GREEN, "1", "0..*"),
        link("Produkt", "Ubytek", GREEN, "1", "0..*"),
        link("Produkt", "Korekta", GREEN, "1", "0..*", constraint="false"),
        link("Produkt", "PozR", GREEN, "1", "0..*"),
        link("Produkt", "PozS", GREEN, "1", "0..*", tailport="e", headport="w"),
        link("PozD", "Dostawa", PURPLE, "1..*", "1"),
        link("Profil", "Rezerwacja", ORANGE, "1", "0..*"),
        link("Rezerwacja", "PozR", ORANGE, "1", "1..*"),
        link("Rezerwacja", "Stan", ORANGE, "", ""),
        link("Rezerwacja", "Sprzedaz", RED, "0..1", "0..1"),
        link("Sprzedaz", "PozS", RED, "1", "0..*"),
        link("Profil", "Rozl", RED, "1", "0..*"),
        link("User", "Dostawa", SLATE, "1", "0..*", constraint="false"),
        link("User", "Ubytek", SLATE, "1", "0..*", constraint="false"),
        link("User", "Korekta", SLATE, "1", "0..*", constraint="false"),
        link("User", "Sprzedaz", SLATE, "1", "0..*", constraint="false"),
        link("User", "Rozl", SLATE, "1", "0..*", constraint="false"),
    ])

    nodes["gap0"] = ""
    node_lines = emit_nodes(nodes, groups)
    legend = """  legend [
    label=<
      <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="#B0BEC5" BGCOLOR="#FAFAFA">
        <TR><TD ALIGN="LEFT"><B>Legenda</B><BR ALIGN="LEFT"/>
          <FONT COLOR="#1F4E79"><B>■</B></FONT> konto
          &nbsp; <FONT COLOR="#2E7D32"><B>■</B></FONT> produkt
          &nbsp; <FONT COLOR="#6A1B9A"><B>■</B></FONT> dostawa, ubytek i korekta
          &nbsp; <FONT COLOR="#E65100"><B>■</B></FONT> rezerwacja
          &nbsp; <FONT COLOR="#C62828"><B>■</B></FONT> sprzedaż i zaległość
          &nbsp; <FONT COLOR="#546E7A"><B>■</B></FONT> kto zarejestrował
        </TD></TR>
      </TABLE>
    >
  ];
  Rozl -> legend [style=invis, weight=1, dir=none];
"""
    body = HEADER.format(
        nodes=node_lines,
        ranks=ranks(groups),
        chains=chains(groups),
        edges=edges,
        legend=legend,
    )
    path = OUT / "klasy-modele-orm.dot"
    write_dot(path, body)
    return render(path)


def main():
    erd("erd-konceptualny", conceptual())
    erd("erd-logiczny", logical())
    class_diagram()


if __name__ == "__main__":
    main()
