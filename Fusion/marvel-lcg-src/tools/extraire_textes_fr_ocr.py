"""Texte francais des cartes, lu par OCR sur les vrais scans FR officiels.

    python tools/extraire_textes_fr_ocr.py [--tessdata DIR] [--jobs 8] [--cartes 01006,50170] [--rapport R.json]

POURQUOI (27/10/2026). `textes-fr-complets.ts` vient de fr.marvelcdb.com et
mc4db (scrape) : il porte des erreurs averees (anglais au milieu d'une phrase
sur 01006, « inflgez », « sbier atatché », mots manquants sur 50170...). Les
4 500 scans `assets/pics-fr/fr_<code>.jpg` sont, eux, l'imprime officiel. Ce
script relit le texte DIRECTEMENT sur ces images et ecrit
`ui-app/src/board/textes-fr-ocr.ts`, au MEME format que textes-fr-complets.ts
(cle = code carte, valeur = texte avec <b>/<i>, [mental]/[energy]/..., [[TRAIT]],
→, \\n entre paragraphes), pour pouvoir remplacer l'un par l'autre plus tard.
Il NE remplace PAS textes-fr-complets.ts.

DEPENDANCES
    pip install tesserocr      (la roue manylinux embarque libtesseract 5.5 :
                                rien a installer cote systeme)
    fra.traineddata (tessdata_best) dans --tessdata ou $TESSDATA_PREFIX
    (https://github.com/tesseract-ocr/tessdata_best/raw/main/fra.traineddata)
    Pillow.

METHODE
1. OCR. Tesseract (LSTM, langue `fra`, segmentation automatique PSM 3) sur
   la carte ENTIERE en niveaux de gris, agrandie x2 (calibrage : x1 rate des
   boites de texte entieres, x3 fait remonter le bruit de l'illustration).
   On garde chaque MOT avec sa confiance (0-100) et sa ligne. Les coupures de
   fin de ligne « dé- / faussez » sont recollees (sans tiret si le mot recolle
   est connu du vocabulaire, avec sinon). Cache JSON par carte et par echelle.

2. GABARIT. Le texte d'une carte n'est pas reconstruit a partir de rien : on
   prend comme GABARIT de structure le texte deja connu de la meme carte
   (textes-fr-complets.ts : meme langue, donc alignable mot a mot ; il porte
   deja <b>, <i>, icones, [[traits]], → et \\n aux bons endroits). Le gabarit
   est decoupe en elements ALIGNABLES (mots, icones, →, —, guillemets) et en
   COLLE fixe (balises, [[ ]], espaces, \\n), qui ne bouge jamais.

3. ALIGNEMENT. Programmation dynamique semi-globale (Needleman-Wunsch avec
   extremites libres cote OCR) entre les elements alignables du gabarit et la
   suite des mots OCR : le titre, les traits, l'ambiance, le pied de carte et
   le bruit de l'illustration tombent dans les extremites libres. Score de
   substitution = 2*similarite-1 (difflib sur les formes sans accents ni
   ponctuation, bonus si egales) ; une icone du gabarit s'aligne sur un
   « mot » OCR sans lettres (®, @, #...), qui est ce que Tesseract lit a la
   place des pictogrammes.

4. CHOIX MOT A MOT (c'est ici que l'imprime l'emporte sur le scrape) :
   - icone, →, — du gabarit : toujours le gabarit (l'OCR ne sait pas les lire) ;
   - meme mot aux accents/casse/ponctuation pres : le gabarit (l'OCR perd des
     accents sur les petites capitales, « COMITE ») ;
   - mot OCR present dans le vocabulaire FR (mots vus >= 2 fois dans tout le
     corpus) et confiance >= 55 : l'OCR (corrige « inflgez », « heal ») ;
   - mot du gabarit connu, mot OCR inconnu : le gabarit (bruit OCR) ;
   - sinon : l'OCR si confiance >= 85, le gabarit s'il ressemble (>= 0.5),
     l'OCR si confiance >= 50, le gabarit en dernier recours.
   Mot du gabarit SANS vis-a-vis OCR : garde (l'OCR fusionne parfois deux mots),
   sauf s'il est anglais (vocabulaire EN de cards.json, absent du FR).
   Mot OCR SANS vis-a-vis dans le gabarit (a l'interieur de la zone alignee) :
   insere s'il est connu et lu a >= 60, ou lu a >= 90 (mots manquants du
   scrape : « Attachez [cette carte] au Baron Zemo »).
   Qualite = part des mots du gabarit retrouves a l'identique dans l'OCR. Sous
   0,85 on relance l'OCR a x3 puis x1,5 et on garde la meilleure echelle.

5. SANS GABARIT (cartes que le scrape n'a pas) : lignes OCR de confiance
   moyenne >= 75, hors pied de carte / traits / ambiance ; libelles en gras
   (« Action de héros », « Une fois révélée »...) reconnus par la liste des
   <b>...</b> du corpus. Icones non reconstituees : ces cartes sont listees
   dans le rapport (« sans_gabarit ») pour relecture humaine.

6. NETTOYAGE (typographie FR, apres reconstruction) : apostrophes et
   guillemets droits, « .. » -> « . », espace (simple, comme le format
   existant) avant : ; ! ? et a l'interieur de « », pas d'espace avant , . ),
   espaces multiples, balises vides. Confusions l/I/1 et 0/O : traitees par
   le choix mot a mot (un mot OCR inconnu du vocabulaire ne passe pas) plus
   des regles ciblees (« l'» en debut de mot lu « I' », chiffres dans des mots).

7. TRAITS ET AMBIANCE (exports compagnons du meme fichier) :
   - TRAITS_FR_OCR[code] : la ligne de traits telle qu'imprimee (« AVENGER. »).
     Cherchee dans les 3 lignes OCR au-dessus du texte de regles ; comparee a
     la traduction attendue (traits EN de cards.json passes par traits-fr.ts) :
     chaque trait proche a l'accent pres prend la forme du dictionnaire, un
     trait different (« MEMBRE DU COMITÉ » imprime ≠ « MEMBRE DU CONSEIL » du
     dictionnaire) garde l'imprime. Ligne introuvable : dictionnaire.
   - AMBIANCE_FR_OCR[code] : la citation en italique sous le texte, seulement
     si elle s'ouvre par un guillemet (sinon rien : on n'invente pas), jusqu'au
     guillemet fermant, plus la ligne d'attribution « — Nom » qui suit.

8. ERRATA_FR de generer_textes_fr_complets.py reappliques par-dessus (meme
   politique que la source actuelle).

Le rapport JSON (--rapport) donne, par carte : qualite, echelle, source, et la
liste des echecs (qualite < 0,5, texte vide) a relire a la main.
"""
from __future__ import annotations

import argparse
import ast
import collections
import difflib
import json
import os
import re
import sys
import unicodedata
from multiprocessing import Pool
from pathlib import Path

ICI = Path(__file__).resolve().parent
MARVEL = ICI.parent
RACINE = MARVEL.parent.parent
SCANS = MARVEL / "assets" / "pics-fr"
CARTES_JEU = MARVEL / "data" / "cards.json"
BOARD = RACINE / "ui-app" / "src" / "board"
GABARITS = BOARD / "textes-fr-complets.ts"
TRAITS_TS = BOARD / "traits-fr.ts"
SORTIE = BOARD / "textes-fr-ocr.ts"
# Corrections manuelles (relecture a l'oeil des cartes mal lues par l'OCR) : source
# de verite, reappliquee EN DERNIER par-dessus le resultat OCR a chaque regeneration.
CORRECTIONS = ICI / "corrections-fr-ocr.json"
CACHE = Path(os.environ.get("OCR_FR_CACHE", Path.home() / ".cache" / "marvel-ocr-fr"))

# (echelle, mode epars) essayes dans l'ordre tant que la qualite reste < SEUIL_RELANCE.
# Le mode epars (PSM 11, contraste etire) retrouve les textes courts sur fond gris
# (« 1 max par deck. » des ressources de base) que la segmentation auto ignore.
ECHELLES = ((2.0, False), (3.0, False), (1.5, False), (2.0, True))
ECHELLE_BASE = ECHELLES[0][0]
SEUIL_REPLI = 0.3  # en dessous, l'OCR n'a pas trouve le texte : on garde le gabarit (signale)
PART_ANGLAIS = 0.4  # gabarit dont >= 40 % des mots sont anglais : inutilisable comme gabarit
SEUIL_RELANCE = 0.85

# ---------------------------------------------------------------- utilitaires


def sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norme(s: str) -> str:
    """Forme de comparaison : minuscules, sans accents, alphanumerique seul."""
    return re.sub(r"[^0-9a-z]", "", sans_accents(s.lower()))


def coeur(s: str) -> str:
    """Forme de vocabulaire : minuscules, accents gardes, ponctuation de bord retiree."""
    s = s.replace("’", "'").lower()
    return re.sub(r"^[^\w]+|[^\w]+$", "", s)


def lire_dico_ts(chemin: Path) -> dict[str, str]:
    d = {}
    for m in re.finditer(r'^  ("(?:[^"\\]|\\.)+"): (".*"),$', chemin.read_text(encoding="utf-8"), re.M):
        d[json.loads(m.group(1))] = json.loads(m.group(2))
    return d


def lire_errata() -> dict[str, str]:
    src = (ICI / "generer_textes_fr_complets.py").read_text(encoding="utf-8")
    m = re.search(r"^ERRATA_FR = (\{.*?^\})", src, re.M | re.S)
    return ast.literal_eval(m.group(1)) if m else {}


def lire_corrections() -> dict[str, dict]:
    """Corrections manuelles {card_id: {texte?, traits?, ambiance?}} ou {} si absent."""
    if not CORRECTIONS.exists():
        return {}
    return json.loads(CORRECTIONS.read_text(encoding="utf-8"))


def appliquer_corrections(textes: dict, traits: dict, ambiances: dict, rapport: dict) -> None:
    """Override final : les corrections relues a l'oeil l'emportent sur l'OCR."""
    champ = {"texte": textes, "traits": traits, "ambiance": ambiances}
    for cid, fields in lire_corrections().items():
        for nom, dico in champ.items():
            val = fields.get(nom)
            if val is not None:
                dico[cid] = val
        if cid in rapport:
            rapport[cid]["correction"] = True


def charger_cartes() -> dict[str, dict]:
    cartes = {}
    for paquet in json.loads(CARTES_JEU.read_text(encoding="utf-8")).values():
        if isinstance(paquet, list):
            for c in paquet:
                if isinstance(c, dict) and isinstance(c.get("card_id"), str):
                    cartes.setdefault(c["card_id"], c)
    return cartes


# ---------------------------------------------------------------- OCR

_API: dict = {}


def _api(tessdata: str, epars: bool = False):
    if epars not in _API:
        import tesserocr

        psm = tesserocr.PSM.SPARSE_TEXT if epars else tesserocr.PSM.AUTO
        _API[epars] = tesserocr.PyTessBaseAPI(path=tessdata, lang="fra", psm=psm)
    return _API[epars]


def ocr(code: str, echelle: float, tessdata: str, epars: bool = False) -> list[list[tuple[str, float]]]:
    """Lignes OCR de la carte : [[(mot, confiance), ...], ...] (cache disque)."""
    fichier = CACHE / f"{code}@{echelle}{'s' if epars else ''}.json"
    if fichier.exists():
        return json.loads(fichier.read_text(encoding="utf-8"))
    import tesserocr
    from PIL import Image, ImageOps

    im = Image.open(SCANS / f"fr_{code}.jpg").convert("L")
    if epars:
        im = ImageOps.autocontrast(im, cutoff=1)
    im = im.resize((int(im.width * echelle), int(im.height * echelle)), Image.LANCZOS)
    api = _api(tessdata, epars)
    api.SetImage(im)
    api.Recognize()
    lignes: list[list[tuple[str, float]]] = []
    it = api.GetIterator()
    niveau = tesserocr.RIL.WORD
    if it is not None:
        while True:
            try:
                mot = it.GetUTF8Text(niveau)
            except RuntimeError:  # « No text returned » : element vide
                mot = None
            if mot:
                if it.IsAtBeginningOf(tesserocr.RIL.TEXTLINE) or not lignes:
                    lignes.append([])
                lignes[-1].append((mot, round(it.Confidence(niveau), 1)))
            if not it.Next(niveau):
                break
    lignes = [l for l in lignes if l]
    CACHE.mkdir(parents=True, exist_ok=True)
    fichier.write_text(json.dumps(lignes, ensure_ascii=False), encoding="utf-8")
    return lignes


def _tache_ocr(args):
    code, echelle, tessdata = args
    try:
        ocr(code, echelle, tessdata)
        return code, None
    except Exception as e:  # noqa: BLE001
        return code, repr(e)


# ---------------------------------------------------------------- gabarit

RE_GABARIT = re.compile(
    r"(?P<icone>\[[A-Za-z_]+\])|(?P<colle></?[a-z]+>|\[\[|\]\]|\n|[ \t]+)|(?P<sym>→|—|«|»)|(?P<mot>[^\s<\[\]→—«»]+|[\[\]<])"
)


def decouper_gabarit(texte: str) -> list[tuple[str, str]]:
    parts = []
    for m in RE_GABARIT.finditer(texte):
        genre = m.lastgroup
        parts.append(({"icone": "icone", "sym": "icone"}.get(genre, genre), m.group()))
    return parts


def est_bruit(mot: str) -> bool:
    """Ce que Tesseract lit a la place d'un pictogramme : pas de lettre ou presque."""
    lettres = sum(c.isalpha() for c in mot)
    return lettres == 0 or (len(mot) <= 2 and not mot.isalpha()) or bool(re.fullmatch(r"[#@®©&%$£*xX+=]+", mot))


ARROWS = {"—", "–", "-", "->", "+", "=>", "→", "=", "—>", ">"}


def similarite(t: str, o: str) -> float:
    nt, no = norme(t), norme(o)
    if not nt and not no:
        return 1.0 if t == o else 0.4
    if not nt or not no:
        return 0.0
    if nt == no:
        return 1.0
    return difflib.SequenceMatcher(None, nt, no).ratio()


def score_sub(t: str, genre: str, o: str) -> float:
    if genre == "icone":
        if o == t or (t == "→" and o in ARROWS) or (t in "«»" and o in "«»\"“”"):
            return 1.0
        return 0.5 if est_bruit(o) else -0.9
    if norme(t) and norme(t) == norme(o):
        return 1.3
    return 2 * similarite(t, o) - 1


def aligner(gab: list[tuple[str, str]], mots: list[tuple[str, float]]):
    """Alignement semi-global. Renvoie la liste de paires (i_gab|None, j_ocr|None) et le score."""
    m, n = len(gab), len(mots)
    DEL, DEL_ICONE = -0.5, -0.2
    NEG = -1e9
    S = [[0.0] * (n + 1) for _ in range(m + 1)]
    B = [[0] * (n + 1) for _ in range(m + 1)]  # 0 diag 1 haut(del gab) 2 gauche(ins ocr) 3 debut libre
    for i in range(1, m + 1):
        S[i][0] = S[i - 1][0] + (DEL_ICONE if gab[i - 1][0] == "icone" else DEL)
        B[i][0] = 1
    for j in range(1, n + 1):
        S[0][j] = 0.0
        B[0][j] = 3
    ins_cout = [(-0.1 if est_bruit(w) else -0.4) for w, _ in mots]
    for i in range(1, m + 1):
        g, t = gab[i - 1]
        d = DEL_ICONE if g == "icone" else DEL
        Si, Sp = S[i], S[i - 1]
        Bi = B[i]
        for j in range(1, n + 1):
            a = Sp[j - 1] + score_sub(t, g, mots[j - 1][0])
            b = Sp[j] + d
            c = Si[j - 1] + ins_cout[j - 1]
            if a >= b and a >= c:
                Si[j], Bi[j] = a, 0
            elif b >= c:
                Si[j], Bi[j] = b, 1
            else:
                Si[j], Bi[j] = c, 2
    jfin = max(range(n + 1), key=lambda j: S[m][j])
    score = S[m][jfin]
    paires = []
    i, j = m, jfin
    while i > 0:
        bk = B[i][j]
        if j == 0 or bk == 1:
            paires.append((i - 1, None))
            i -= 1
        elif bk == 0:
            paires.append((i - 1, j - 1))
            i -= 1
            j -= 1
        else:
            paires.append((None, j - 1))
            j -= 1
    paires.reverse()
    return paires, score


# ---------------------------------------------------------------- choix des mots


class Lexique:
    """Vocabulaire FR = mots lus par l'OCR a >= 90 sur >= 3 cartes (imprime, donc
    propre) + mots des gabarits vus >= 2 fois qui ne sont pas de l'anglais
    (le scrape contient des restes anglais : « heal », « from »)."""

    def __init__(self, gabarits: dict[str, str], cartes: dict[str, dict], cache: Path = CACHE):
        en = collections.Counter()
        for carte in cartes.values():
            for w in re.sub(r"<[^>]+>|\[[a-z_]+\]", " ", carte.get("text") or "").split():
                en[coeur(w)] += 1
        lu = collections.Counter()
        lu_large = collections.Counter()
        for f in cache.glob(f"*@{ECHELLE_BASE}.json"):
            vus, vus_large = set(), set()
            for ligne in json.loads(f.read_text(encoding="utf-8")):
                for w, c in ligne:
                    if c >= 90:
                        vus.add(coeur(w))
                    if c >= 60:
                        vus_large.add(coeur(w))
            lu.update(vus)
            lu_large.update(vus_large)
        self.ocr = {w for w, k in lu.items() if k >= 3 and w}
        c = collections.Counter()
        for t in gabarits.values():
            for w in re.sub(r"<[^>]+>|\[[a-z_]+\]", " ", t).split():
                c[coeur(w)] += 1
        en_set = {w for w, k in en.items() if k >= 2 and w}
        # Un mot lu par l'OCR mais absent de TOUT gabarit n'est pas admis (« fe » = pictogramme
        # lu comme texte, « etinfligez » = deux mots colles) : l'OCR ne fait que confirmer.
        self.fr = {w for w, k in c.items() if w and ((k >= 2 and w not in en_set) or (k >= 1 and w in self.ocr))}
        # anglais = vu dans les textes EN et jamais lu sur un scan FR
        # (« permanent », « distance » sont aussi francais : lus sur les scans FR, ils ne sont pas anglais)
        self.en = en_set - {w for w, k in lu_large.items() if k >= 3}
        gras = collections.Counter()
        for t in gabarits.values():
            for b in re.findall(r"<b>([^<]+)</b>", t):
                gras[b.strip()] += 1
        self.gras = sorted((b for b, k in gras.items() if k >= 3 and len(b) > 3), key=len, reverse=True)

    traits_en: set = set()
    traits_fr: dict = {}

    def charger_traits(self, dico: dict[str, str], gabarits: dict[str, str]):
        """Mots des traits anglais (cles de traits-fr.ts) et formes francaises accentuees
        connues (valeurs + contenus [[...]] des gabarits), indexees par forme sans accents."""
        fr_mots = set()
        for v in dico.values():
            fr_mots |= {coeur(w) for w in v.split()}
        for k in dico:
            self.traits_en |= {coeur(w) for w in k.split()}
        self.traits_en -= fr_mots
        formes = list(dico.values())
        for t in gabarits.values():
            formes += re.findall(r"\[\[([^\]]+)\]\]", t)
        for f in formes:
            self.traits_fr.setdefault(norme(f), f.upper())

    def connu(self, w: str) -> bool:
        k = coeur(w)
        return bool(k) and (k in self.fr or k.isdigit())


RE_ROMAIN = re.compile(r"^\(?[IVX]{1,4}\)?[.,;:)]*$")


def choisir(t: str, genre: str, o: str, conf: float, lex: Lexique, dans_trait: bool = False) -> str:
    if genre == "icone":
        return t
    if RE_ROMAIN.match(t):
        return t  # « Stryfe (II) » : l'OCR lit « (Il) »
    if re.search(r"\d", t) and re.search(r"\d", o):
        return t  # « 1[per_hero] » lu « 12. » : le pictogramme colle au chiffre devient un chiffre
    if sum(ch.isalpha() for ch in o) >= 2 and o.upper() == o and not dans_trait:
        return t  # capitales (ATQ lu ATO ; titre, autocollant lus a la place du texte courant)
    nt, no = norme(t), norme(o)
    if no and no != nt and (nt.startswith(no) or nt.endswith(no)) and lex.connu(t):
        return t  # mot tronque par l'OCR (« l'environnement » lu « 'environnement »)
    if dans_trait:
        # trait du gabarit deja francais : il fait foi ; anglais (« Team ») : l'imprime, accents restitues
        if coeur(t) not in lex.traits_en:
            return t
        lu = re.sub(r"[^\w' \-]", "", o)
        return lex.traits_fr.get(norme(lu), lu) if lu else t
    if norme(t) == norme(o) and norme(t):
        return t
    if not norme(t) and not norme(o):  # ponctuation seule
        return t
    o_ok, t_ok = lex.connu(o), lex.connu(t)
    if o_ok and conf >= 55:
        return o
    if t_ok and not o_ok:
        return t
    if conf >= 85 and not est_bruit(o):
        return o
    if similarite(t, o) >= 0.5:
        return t
    if conf >= 50 and not est_bruit(o):
        return o
    return t


def inserer(o: str, conf: float, lex: Lexique) -> bool:
    k = coeur(o)
    if o in (":", ";") and conf >= 75:
        return True
    if not k or est_bruit(o):
        return False
    if len(k) == 1 and not k.isdigit():
        return o == k and conf >= 90 and k in lex.fr  # « (Y) » parasite refuse
    if k.isdigit():
        return conf >= 80
    if sum(c.isalpha() for c in o) >= 2 and o.upper() == o and any(c.isalpha() for c in o):
        return False  # capitales : titre, traits, autocollant (« VOTRE ALLIÉ » de 44022), jamais du texte courant
    if k in lex.fr:
        return conf >= 60
    # inconnu : seulement s'il est tres net et n'est pas en capitales (titre de carte, traits)
    return conf >= 90 and len(k) >= 4 and k.replace("'", "").replace("-", "").isalpha() and not (o.isupper() and len(k) > 2)


# ---------------------------------------------------------------- reconstruction


def mots_ocr(lignes, lex: Lexique) -> list[tuple[str, float, int]]:
    """Mots a plat (mot, conf, no de ligne), coupures de fin de ligne recollees."""
    mots: list[tuple[str, float, int]] = []
    for nl, ligne in enumerate(lignes):
        for k, (w, c) in enumerate(ligne):
            w = w.replace("’", "'").replace("‘", "'")
            w = re.sub(r"\|(?=[a-zàâéèêîôûç])|(?<=[a-zàâéèêîôûç])\|", "l", w)  # « |es » -> « les »
            if k == 0 and mots and mots[-1][0].endswith("-") and len(mots[-1][0]) > 2 and w[:1].isalpha() and mots[-1][2] == nl - 1:
                p, pc, pl = mots.pop()
                colle = p[:-1] + w
                # « dé- / faussez » -> « défaussez » ; « Spider- / Woman » -> « Spider-Woman »
                w = colle if (w[:1].islower() and lex.connu(colle)) else p + w
                c = min(c, pc)
            mots.append((w, c, nl))
    return mots


def reconstruire(gabarit: str, lignes, lex: Lexique):
    gabarit = gabarit.replace("\\n", "\n")  # « \\n » litteral du scrape (32175b)
    gabarit = re.sub(r"\s*:\s*</b>", "</b> :", gabarit)  # « <b>Ressource:</b> » -> « <b>Ressource</b> : »
    gabarit = re.sub(r" +</b>", "</b> ", gabarit)
    parts = decouper_gabarit(gabarit)
    trait = set()
    dedans = False
    for k, (g, t) in enumerate(parts):
        if t == "[[":
            dedans = True
        elif t == "]]":
            dedans = False
        elif dedans:
            trait.add(k)
    alignables = [(g, t) for g, t in parts if g in ("mot", "icone")]
    idx_parts = [k for k, (g, _) in enumerate(parts) if g in ("mot", "icone")]
    mots = mots_ocr(lignes, lex)
    if not alignables:
        return gabarit, 0.0, None
    paires, _ = aligner(alignables, [(w, c) for w, c, _ in mots])
    sortie = {k: t for k, (g, t) in enumerate(parts)}
    apres: dict[int, list[str]] = collections.defaultdict(list)
    exacts = 0
    total = sum(1 for g, _ in alignables if g == "mot" and norme(_))
    dernier = -1
    lignes_utilisees = []
    supprimes: list[tuple[int, int, int]] = []  # (part du mot du gabarit, part de l'ancre precedente, indice alignable)
    reformule: set[int] = set()  # alignables ou l'OCR a remplace un mot different du gabarit
    for ig, jo in paires:
        if ig is not None and jo is not None:
            g, t = alignables[ig]
            w, c, nl = mots[jo]
            if g == "mot" and norme(t) and norme(t) == norme(w):
                exacts += 1
            sortie[idx_parts[ig]] = choisir(t, g, w, c, lex, idx_parts[ig] in trait)
            if g == "mot" and norme(sortie[idx_parts[ig]]) != norme(t) and similarite(t, w) < 0.5:
                reformule.add(ig)
            dernier = ig
            lignes_utilisees.append(nl)
        elif ig is not None:
            g, t = alignables[ig]
            if g == "mot" and coeur(t) in lex.en and not RE_ROMAIN.match(t) and idx_parts[ig] not in trait:
                sortie[idx_parts[ig]] = ""
            elif g == "mot" and not RE_ROMAIN.match(t) and idx_parts[ig] not in trait:
                supprimes.append((idx_parts[ig], idx_parts[dernier] if dernier >= 0 else -1, ig))
            dernier = ig
        else:
            w, c, nl = mots[jo]
            if dernier >= 0 and inserer(w, c, lex) and dernier < len(alignables) - 1:
                ancre = idx_parts[dernier]
                if ancre in trait:  # jamais a l'interieur de [[...]] : apres le « ]] »
                    ancre = next((k for k in range(ancre, len(parts)) if parts[k][1] == "]]"), ancre)
                deja = apres[ancre][-1] if apres[ancre] else sortie.get(ancre, "")
                if norme(w) != norme(deja):  # « un un un » : pas de repetition
                    apres[ancre].append(w)
                lignes_utilisees.append(nl)
    for k, ancre, ig in supprimes:
        # « Réponse de héros » / imprime « Réponse forcée » (32122b) : « de » -> « forcée », « héros » sans vis-a-vis
        if apres.get(k) or apres.get(ancre) or (ig - 1) in reformule or (ig + 1) in reformule:
            # « déplacez le jeton Actif sur lui » / imprime « vers ce méchant » (45091)
            sortie[k] = ""
    morceaux = []
    for k in range(len(parts)):
        morceaux.append(sortie[k])
        if apres.get(k):
            morceaux.append(" " + " ".join(apres[k]))
    qualite = exacts / total if total else 0.0
    zone = (min(lignes_utilisees), max(lignes_utilisees)) if lignes_utilisees else None
    return "".join(morceaux), qualite, zone


RE_PIED = re.compile(r"©|MARVEL|FFG|Illus|\b\d{1,3}/\d{1,3}\b|\(\d+/\d+\)")


def texte_ligne(ligne) -> str:
    return " ".join(w for w, _ in ligne)


def conf_ligne(ligne) -> float:
    return sum(c for _, c in ligne) / len(ligne) if ligne else 0.0


def sans_gabarit(lignes, lex: Lexique):
    """Repli sans gabarit : lignes propres de la boite de texte, libelles en gras.
    Renvoie (texte, (premiere, derniere) ligne retenue | None)."""
    paras: list[str] = []
    retenues: list[int] = []
    for nl, ligne in enumerate(lignes):
        mots = [w.replace("’", "'") for w, c in ligne if not (est_bruit(w) and c < 80) and w not in "|=_~"]
        txt = " ".join(mots).strip()
        suite = len(mots) == 1 and paras and not paras[-1].endswith((".", ")")) and conf_ligne(ligne) >= 80
        if (len(mots) < 2 and not suite) or conf_ligne(ligne) < 75 or RE_PIED.search(txt):
            continue
        if txt.lstrip().startswith(("«", "“", '"')):
            break  # l'ambiance commence : le texte de regles est fini
        if re.fullmatch(r"[A-ZÀ-ÖØ-Ý0-9' \-!.]+\.", txt):
            continue  # ligne de traits
        lettres = [c for c in txt if c.isalpha()]
        if lettres and sum(c.isupper() for c in lettres) > 0.5 * len(lettres):
            continue  # titre en petites capitales, pied de carte
        nouveau = any(txt.startswith(b) for b in lex.gras) or not paras or paras[-1].endswith((".", ")"))
        if nouveau and paras and not any(txt.startswith(b) for b in lex.gras) and not paras[-1].endswith((".", ")")):
            nouveau = False
        txt = re.sub(r"^[e•°·] (?=[A-ZÀ-Ý])", "• ", txt)  # puce lue « e »
        if txt.startswith("• "):
            nouveau = True
        retenues.append(nl)
        if nouveau:
            paras.append(txt)
        else:
            paras[-1] += " " + txt
    sortie = []
    for p in paras:
        prefixe = ""
        m = re.match(r"^([^—:]{2,40}?) — ", p)  # « Sens d'Araignée — Interruption : » (capacite nommee)
        if m:
            prefixe, p = m.group(0), p[m.end():]
        for b in lex.gras:
            if p.startswith(b + " :") or p.startswith(b + " ("):
                p = f"<b>{b}</b>" + p[len(b):]
                break
        else:
            if prefixe:
                p, prefixe = prefixe + p, ""
        p = re.sub(r" [—–-] (?=[a-zàâéèêîôû])", " → ", p)
        p = re.sub(r"</b> (\([^)]{2,20}\))", r"</b> <i>\1</i>", p)  # <b>Action de héros</b> <i>(attaque)</i>  # cout → effet (le tiret de capacite nommee precede une majuscule)
        sortie.append(prefixe + p)
    return "\n".join(sortie), ((retenues[0], retenues[-1]) if retenues else None)


def nettoyer(t: str) -> str:
    t = t.replace("’", "'").replace("‘", "'").replace("“", "«").replace("”", "»")
    t = re.sub(r"(?<![.])\.\.(?!\.)", ".", t)
    t = re.sub(r"\bI'(?=[a-zàâéèêëîïôûü])", "l'", t)  # « I'ennemi » -> « l'ennemi »
    t = re.sub(r"(?<=[a-zé])0(?=[a-z])", "o", t)
    t = re.sub(r"(?<=[a-zé])1(?=[a-z])", "l", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"(?<=[^\s\n(])([:;!?])", r" \1", t)  # espace avant : ; ! ?
    t = re.sub(r"(?<=\[[a-z]) :", ":", t)  # ne pas toucher l'interieur des icones
    t = re.sub(r"( ?:)(\s*(?:</b>)?\s*:)+", lambda m: (" </b> :" if "</b>" in m.group(0) else " :"), t)
    t = re.sub(r"(?<=\d)–(?=[A-ZÀ-Ý])", " – ", t)
    t = re.sub(r" +([,.)])", r"\1", t)
    t = re.sub(r"\( +", "(", t)
    t = re.sub(r"«(?=\S)", "« ", t)
    t = re.sub(r"(?<=\S)»", " »", t)
    t = re.sub(r"(?<=\S)→", " →", t)
    t = re.sub(r"→(?=\S)", "→ ", t)
    t = re.sub(r"<(b|i)>\s*</\1>", "", t)
    t = re.sub(r"<(b|i)> ", r" <\1>", t)
    t = re.sub(r" </(b|i)>", r"</\1> ", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return t.strip()


# ---------------------------------------------------------------- traits / ambiance


def traits_attendus(carte: dict, dico: dict[str, str]) -> list[str]:
    return [dico.get(t.upper(), t.upper()) for t in (carte.get("traits") or [])]


def extraire_traits(lignes, zone, attendus: list[str]):
    """(texte imprime, source) ; source = 'ocr' | 'dico' | None."""
    if not attendus:
        return None, None
    attendu = ". ".join(attendus) + "."
    candidats = []
    debut = zone[0] if zone else len(lignes)
    for nl in range(max(0, debut - 4), debut + (1 if zone else 0)):
        if nl >= len(lignes):
            continue
        txt = re.sub(r"[:;,](?=\s|$)", ".", texte_ligne(lignes[nl]))
        txt = re.sub(r"^[^A-ZÀ-Ý]+", "", txt).strip(" |'\"")
        if txt and "." in txt and sum(c.isupper() for c in txt) >= 0.7 * max(1, sum(c.isalpha() for c in txt)):
            candidats.append((difflib.SequenceMatcher(None, norme(txt), norme(attendu)).ratio(), txt, conf_ligne(lignes[nl])))
    if not zone:  # sans zone : toute la carte
        for l in lignes:
            txt = re.sub(r"^[^A-ZÀ-Ý]+", "", texte_ligne(l)).strip(" |'\"")
            if txt.endswith(".") and txt.upper() == txt and sum(c.isalpha() for c in txt) >= 3:
                candidats.append((difflib.SequenceMatcher(None, norme(txt), norme(attendu)).ratio(), txt, conf_ligne(l)))
    if not candidats:
        return attendu, "dico"
    sim, txt, conf = max(candidats)
    if sim < 0.5:
        return attendu, "dico"
    # « S.H.I.E.L.D. » : on ne coupe que sur un point suivi d'un blanc ou final
    morceaux = [p.strip(" ,") for p in re.split(r"\.(?=\s|$)", txt) if p.strip(" ,")]
    sortie = []
    restants = list(attendus)
    for p in morceaux:
        meilleur = max(restants, key=lambda a: difflib.SequenceMatcher(None, norme(p), norme(a)).ratio(), default=None)
        if meilleur and difflib.SequenceMatcher(None, norme(p), norme(meilleur)).ratio() >= 0.8:
            sortie.append(meilleur)
            restants.remove(meilleur)
        elif (
            conf >= 85
            and len(morceaux) == len(attendus)
            and re.fullmatch(r"[A-ZÀ-ÖØ-Ý' \-!]{3,}", p)
        ):
            # trait imprime different du dictionnaire (« MEMBRE DU COMITÉ ») : ligne nette, meme nombre de traits
            sortie.append(p)
            if meilleur:
                restants.remove(meilleur)
    if restants and len(sortie) + len(restants) == len(attendus) and all(x in attendus for x in sortie):
        return attendu, "dico"  # ligne lue en partie seulement : l'ordre de cards.json (celui de l'imprime) vaut mieux
    sortie += restants  # traits non lus : forme du dictionnaire
    if not sortie:
        return attendu, "dico"
    return ". ".join(sortie) + ".", "ocr"


def extraire_ambiance(lignes, zone) -> str | None:
    debut = zone[1] + 1 if zone else 0
    morceaux: list[str] = []
    ouvert = False
    for nl in range(debut, min(len(lignes), debut + 8) if zone else len(lignes)):
        brut = lignes[nl]
        mots = [
            ("!" if w in ("1", "l", "I", "|") and k + 1 < len(brut) and brut[k + 1][0].startswith("»") else w)
            for k, (w, c) in enumerate(brut)
            if (w in ("1", "l", "I", "|") and k + 1 < len(brut) and brut[k + 1][0].startswith("»"))
            or not (w in "|=_~[]" or (est_bruit(w) and not set(w) <= set("«»“”\"—–-!?….,") and c < 70))
        ]
        txt = " ".join(mots).strip()
        if not txt:
            continue
        if RE_PIED.search(txt):
            break
        if not ouvert:
            m = re.search(r"[«“\"]", txt)
            if m and m.start() <= 3:
                ouvert = True
                txt = txt[m.start():]
            else:
                if morceaux:
                    break
                continue
        morceaux.append(txt)
        if re.search(r"[»”\"]\s*$", txt) or re.search(r"[»”]", txt[1:]):
            # attribution eventuelle sur la meme ligne ou la suivante
            if not re.search(r"[—–-]\s*\w", txt.split("»")[-1] if "»" in txt else ""):
                if nl + 1 < len(lignes):
                    suiv = texte_ligne(lignes[nl + 1]).strip(" |")
                    if re.match(r"^[—–-]\s*[A-ZÀ-Ý]", suiv) and not RE_PIED.search(suiv):
                        morceaux.append(suiv)
            break
    if not morceaux:
        return None
    t = " ".join(morceaux)
    t = t.replace("“", "«").replace("”", "»").replace('"', "«", 1)
    t = re.sub(r'"', "»", t)
    t = re.sub(r"\s*[–-]\s+(?=[A-ZÀ-Ý])", " — ", t)
    t = re.sub(r"»\s*—", "» —", t)
    t = re.sub(r"(?<=\w) [1l|I] ?(?=»)", " ! ", t)  # « ! » final lu « 1 »
    t = nettoyer(t)
    if len(re.sub(r"[^a-zA-Zà-ÿ]", "", t)) < 4:
        return None
    return t


# ---------------------------------------------------------------- pilote


def part_anglaise(gabarit: str, lex: Lexique) -> float:
    mots = [t for g, t in decouper_gabarit(gabarit) if g == "mot" and norme(t)]
    return sum(coeur(t) in lex.en for t in mots) / len(mots) if mots else 0.0


def traiter(code, carte, gabarit, lex, dico_traits, tessdata):
    source = "gabarit"
    if gabarit and part_anglaise(gabarit, lex) >= PART_ANGLAIS:
        gabarit, source = None, "gabarit_anglais"  # scrape non traduit : on lit le scan seul
    elif not gabarit:
        source = "sans_gabarit"
    essais = []
    for e, epars in ECHELLES:
        lignes = ocr(code, e, tessdata, epars)
        if gabarit:
            txt, q, zone = reconstruire(gabarit, lignes, lex)
        else:
            (txt, zone), q = sans_gabarit(lignes, lex), None
        essais.append((q if q is not None else 0, f"{e}{' epars' if epars else ''}", txt, zone, lignes))
        if q is None or q >= SEUIL_RELANCE:
            break
    q, e, txt, zone, lignes = max(essais, key=lambda x: x[0])
    if gabarit and q < SEUIL_REPLI:
        txt, source = gabarit, "repli_scrape"
    traits, src_traits = extraire_traits(lignes, zone, traits_attendus(carte, dico_traits))
    ambiance = extraire_ambiance(lignes, zone)
    if source == "sans_gabarit" and not (carte.get("text") or "").strip():
        # Pas de texte de regles en anglais (face A de manigance, ressource de base...) : ce que
        # l'OCR a lu est le texte d'ambiance narratif, pas une capacite.
        if txt and not ambiance:
            ambiance = nettoyer(txt.replace("\n", " "))
        txt, source = "", "sans_texte"
    return {
        "texte": nettoyer(txt) if txt else "",
        "qualite": round(q, 3) if gabarit else None,
        "echelle": e,
        "source": source,
        "traits": traits,
        "source_traits": src_traits,
        "ambiance": ambiance,
    }


def ecrire_ts(textes: dict, traits: dict, ambiances: dict):
    def bloc(nom, d, doc):
        out = [*doc, f"export const {nom}: Readonly<Record<string, string | undefined>> = {{"]
        for k in sorted(d):
            out.append(f"  {json.dumps(k)}: {json.dumps(d[k], ensure_ascii=False)},")
        out.append("}")
        return out

    lignes = [
        "// Genere par tools/extraire_textes_fr_ocr.py — NE PAS EDITER A LA MAIN.",
        "//",
        "// Texte francais lu par OCR (Tesseract, fra) sur les scans officiels",
        "// assets/pics-fr/fr_<code>.jpg, structure (<b>, <i>, icones, [[traits]], →, \\n)",
        "// reprise de textes-fr-complets.ts par alignement mot a mot : voir l'en-tete",
        "// du script. Meme format que TEXTES_FR_COMPLETS, qu'il a vocation a remplacer.",
    ]
    lignes += bloc("TEXTES_FR_OCR", textes, [])
    lignes += [""]
    lignes += bloc(
        "TRAITS_FR_OCR",
        traits,
        ["// Ligne de traits imprimee (« AVENGER. SOLDAT. »), OCR confrontee a traits-fr.ts."],
    )
    lignes += [""]
    lignes += bloc(
        "AMBIANCE_FR_OCR",
        ambiances,
        ["// Phrase d'ambiance (citation en italique sous le texte), absente si la carte n'en a pas."],
    )
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tessdata", default=os.environ.get("TESSDATA_PREFIX", ""))
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--cartes", default="")
    ap.add_argument("--rapport", default="")
    ap.add_argument("--pas-ecrire", action="store_true")
    a = ap.parse_args()
    if not a.tessdata or not (Path(a.tessdata) / "fra.traineddata").exists():
        print("fra.traineddata introuvable : --tessdata DIR ou TESSDATA_PREFIX", file=sys.stderr)
        return 2
    cartes = charger_cartes()
    gabarits = lire_dico_ts(GABARITS)
    dico_traits = lire_dico_ts(TRAITS_TS)
    codes = sorted(f.name[3:-4] for f in SCANS.glob("fr_*.jpg"))
    codes = [c for c in codes if c in cartes]
    if a.cartes:
        voulus = set(a.cartes.split(","))
        codes = [c for c in codes if c in voulus]
    # 1) OCR a x2 en parallele (le plus long)
    with Pool(a.jobs) as pool:
        for k, (code, err) in enumerate(pool.imap_unordered(_tache_ocr, [(c, ECHELLE_BASE, a.tessdata) for c in codes], chunksize=4)):
            if err:
                print("OCR", code, err, file=sys.stderr)
            if k % 200 == 0:
                print(f"OCR {k}/{len(codes)}", file=sys.stderr, flush=True)
    lex = Lexique(gabarits, cartes)  # apres l'OCR : il lit le vocabulaire imprime dans le cache
    # 2) reconstruction (relances OCR aux autres echelles si besoin)
    rapport = {}
    global _LEX, _DT
    lex.charger_traits(dico_traits, gabarits)
    _LEX, _DT = lex, dico_traits  # avant le fork : les ouvriers en heritent
    with Pool(a.jobs) as pool:
        args = [(c, cartes[c], gabarits.get(c), a.tessdata) for c in codes]
        for k, (code, r) in enumerate(pool.imap_unordered(_tache_rec, args, chunksize=4)):
            rapport[code] = r
            if k % 200 == 0:
                print(f"reconstruction {k}/{len(codes)}", file=sys.stderr)
    errata = lire_errata()
    textes = {c: r["texte"] for c, r in rapport.items() if r["texte"]}
    for c, t in errata.items():
        if c in textes:
            textes[c] = t
            rapport[c]["errata"] = True
    traits = {c: r["traits"] for c, r in rapport.items() if r["traits"]}
    ambiances = {c: r["ambiance"] for c, r in rapport.items() if r["ambiance"]}
    # Override final : corrections manuelles (relecture a l'oeil) par-dessus l'OCR.
    appliquer_corrections(textes, traits, ambiances, rapport)
    if not a.pas_ecrire:
        ecrire_ts(textes, traits, ambiances)
    if a.rapport:
        Path(a.rapport).write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    qs = [r["qualite"] for r in rapport.values() if r["qualite"] is not None]
    print(f"{len(rapport)} cartes, {len(textes)} textes, {len(traits)} traits, {len(ambiances)} ambiances")
    if qs:
        print(f"qualite moyenne {sum(qs)/len(qs):.3f} ; < 0.5 : {sum(q < 0.5 for q in qs)} ; < 0.85 : {sum(q < 0.85 for q in qs)}")
    return 0


_LEX = None
_DT = None


def _tache_rec(args):
    code, carte, gabarit, tessdata = args
    try:
        return code, traiter(code, carte, gabarit, _LEX, _DT, tessdata)
    except Exception as e:  # noqa: BLE001
        return code, {"texte": "", "qualite": 0.0 if gabarit else None, "echelle": None, "source": "erreur",
                      "erreur": repr(e), "traits": None, "source_traits": None, "ambiance": None}


if __name__ == "__main__":
    raise SystemExit(main())
