"""Decoupe un livret de campagne officiel en pages pour l'ecran des campagnes.

L'ecran affiche, par scenario, une planche d'intro, une ou deux pages de
regles, et une planche d'epilogue (montree par le panneau de recompenses apres
la victoire, et sur l'ecran de conclusion pour le dernier scenario). Elles
vivent dans `public/stories/<code>/`, nommees par role, et le fichier de
campagne dit laquelle va ou.

Les livrets sont carres (540 x 540 points) et vectoriels : on les REND, on
n'extrait pas leurs images. Une page de regles est du texte compose, pas une
image ; seules les planches de BD sont des images encapsulees, et les rendre
plutot que les extraire donne un traitement uniforme et la meme taille pour
tout le monde, 975 px comme les scans deja en place.

    ~/marvel-work/python/bin/python3.10 tools/pages_livret.py mut_gen [--pour-de-vrai]

Sans `--pour-de-vrai`, rien n'est ecrit : l'outil dit ce qu'il ferait.

CARTES ci-dessous est la seule chose a fournir pour une nouvelle boite, et
c'est le vrai travail : dire quelle page du PDF joue quel role. Une planche qui
termine un scenario ET ouvre le suivant n'est PAS dupliquee ; elle garde son
nom d'epilogue et le scenario suivant la reference comme intro.
"""
import argparse
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Le Bureau, a cote du depot : c'est la que vivent les PDF officiels.
PDFS = os.path.abspath(os.path.join(RACINE, "..", "..", ".."))
LARGEUR = 975

CARTES = {
    "mts": {
        "pdf": "mc21_the_mad_titans_shadow_rulebook-compressed.pdf",
        # page 4 : regles du mode campagne et de la campagne experte.
        "regles_campagne": [4],
        # Deux planches entre chaque scenario, jamais une seule : l'epilogue de
        # l'un puis l'intro du suivant, deux scenes distinctes. Rien n'est donc
        # partage ici, contrairement a mut_gen.
        "scenarios": [
            ("ebony_maw", 1, 5, [6, 7], 8),
            ("the_tower_defense", 2, 9, [10, 11, 12, 13], 14),
            ("thanos", 3, 15, [16, 17], 18),
            ("hela", 4, 19, [20, 21], 22),
            ("loki", 5, 23, [24, 25], 26),
        ],
    },
    "mut_gen": {
        "pdf": "mc32_mutant_genesis_rulebook_v5-compressed.pdf",
        # page 4 : regles du mode campagne ; page 5 : les roles et l'expert.
        "regles_campagne": [4, 5],
        "scenarios": [
            # (id, numero, intro, [regles], epilogue)
            ("sabretooth", 1, 6, [7], 8),
            ("project_wideawake", 2, None, [9, 10], 11),
            ("master_mold", 3, None, [12], 13),
            ("mansion_attack", 4, 14, [15, 16], 17),
            ("magneto", 5, None, [18, 19], [20, 21]),
        ],
    },
}


def nom_fichier(numero, scenario, role, rang):
    if numero == 0:
        return "00-campagne-%s-%d.jpg" % (role, rang)
    return "%02d-%s-%s-%d.jpg" % (numero, scenario, role, rang)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code", help="code de la boite, par exemple mut_gen")
    ap.add_argument("--pour-de-vrai", action="store_true")
    options = ap.parse_args()

    import fitz

    carte = CARTES.get(options.code)
    if not carte:
        print("Aucune carte de pages pour « %s ». Voir CARTES dans ce fichier."
              % options.code, file=sys.stderr)
        return 1
    chemin_pdf = os.path.join(PDFS, carte["pdf"])
    if not os.path.exists(chemin_pdf):
        print("Livret introuvable : %s" % chemin_pdf, file=sys.stderr)
        return 1

    doc = fitz.open(chemin_pdf)
    zoom = LARGEUR / doc[0].rect.width
    dossier = os.path.join(RACINE, "public", "stories", options.code)

    # page du PDF -> nom de fichier, pour ne rendre chaque page qu'UNE fois
    a_rendre = {}
    pages_par_scenario = {}

    for rang, page in enumerate(carte["regles_campagne"], 1):
        a_rendre[page] = nom_fichier(0, None, "regles", rang)

    precedent_epilogue = None
    for scenario, numero, intro, regles, epilogue in carte["scenarios"]:
        bloc = {}
        # Pas d'intro propre : on reprend la planche qui a clos le scenario
        # precedent, sans la dupliquer.
        if intro is not None:
            f = nom_fichier(numero, scenario, "intro", 1)
            a_rendre[intro] = f
            bloc["intro"] = [f]
        elif precedent_epilogue:
            bloc["intro"] = [precedent_epilogue]
        bloc["regles"] = []
        for rang, page in enumerate(regles, 1):
            f = nom_fichier(numero, scenario, "regles", rang)
            a_rendre[page] = f
            bloc["regles"].append(f)
        epilogues = epilogue if isinstance(epilogue, list) else ([epilogue] if epilogue else [])
        if epilogues:
            noms = []
            for rang, page in enumerate(epilogues, 1):
                f = nom_fichier(numero, scenario, "epilogue", rang)
                a_rendre[page] = f
                noms.append(f)
            bloc["epilogue"] = noms
            precedent_epilogue = noms[0]
        else:
            precedent_epilogue = None
        pages_par_scenario[scenario] = bloc

    print("  %d page(s) a rendre depuis %s" % (len(a_rendre), carte["pdf"]))
    for page in sorted(a_rendre):
        print("    p%-3d -> %s" % (page, a_rendre[page]))

    if not options.pour_de_vrai:
        print()
        print("  Rien n'a ete ecrit. Relancer avec --pour-de-vrai.")
        return 0

    os.makedirs(dossier, exist_ok=True)
    for page, fichier in sorted(a_rendre.items()):
        pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        pix.pil_save(os.path.join(dossier, fichier), format="JPEG", quality=88)

    chemin_json = os.path.join(RACINE, "data", "campagnes", "%s.json" % options.code)
    definition = json.load(open(chemin_json, encoding="utf-8"))
    definition["pages_regles"] = [a_rendre[p] for p in carte["regles_campagne"]]
    for s in definition["scenarios"]:
        if s["id"] in pages_par_scenario:
            s["pages"] = pages_par_scenario[s["id"]]
    with open(chemin_json, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(definition, ensure_ascii=False, indent=2) + "\n")

    print()
    print("  %d image(s) ecrite(s) dans public/stories/%s/" % (len(a_rendre), options.code))
    print("  data/campagnes/%s.json : pages branchees" % options.code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
