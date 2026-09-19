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

# Les livrets officiels, la ou ils se telechargent. Verifies le 19/09/2026
# (HTTP 200, application/pdf). Le nom de fichier attendu par CARTES est le
# dernier segment de l'URL.
#
# `www.fantasyflightgames.com` rend 403 derriere Cloudflare : c'est le CDN
# `images-cdn.fantasyflightgames.com` qui sert les fichiers, et la liste des
# liens se lit sur un instantane Wayback de la page produit.
LIVRETS = {
    "trors":     "https://images-cdn.fantasyflightgames.com/filer_public/92/1d/921ddef8-c28c-4096-a9e9-63142230a602/mc10_the_rise_of_red_skull_rules_web.pdf",
    "gmw":       "https://images-cdn.fantasyflightgames.com/filer_public/dd/86/dd86a2b4-4501-4435-8504-c4ac9df25a99/mc16_galaxys_most_wanted_rules_website-compressed.pdf",
    "mts":       "https://images-cdn.fantasyflightgames.com/filer_public/a7/e4/a7e4f10e-286f-4a8a-b90d-feb052a286a2/mc21_the_mad_titans_shadow_rulebook-compressed.pdf",
    "sm":        "https://images-cdn.fantasyflightgames.com/filer_public/77/cc/77cc5a70-52d8-4542-8588-aba3d6aa07bd/mc27_sinister_motives_rules_v5-compressed.pdf",
    "mut_gen":   "https://images-cdn.fantasyflightgames.com/filer_public/2c/52/2c52bcb0-4e21-4bf8-8052-b2ef41266737/mc32_mutant_genesis_rulebook_v5-compressed.pdf",
    "next_evol": "https://images-cdn.fantasyflightgames.com/filer_public/73/e2/73e23a2b-3f2a-4173-8fee-cf0073ab11c8/mc40_next_evolution_rulebook-web.pdf",
    "aoa":       "https://images-cdn.fantasyflightgames.com/filer_public/a2/bd/a2bd6f15-688b-4485-affa-f5a14d750d3a/mc45_age_of_apocalypse_rulebook.pdf",
    "aos":       "https://images-cdn.fantasyflightgames.com/filer_public/79/12/7912adc3-2461-4ea2-8606-4715880b8d1d/mc50_rulebook-web.pdf",
    # fne : pas de PDF public trouve, le livret vient du scan de la boite.
    # web_of_deceit : campagne maison, sans livret ; sa couverture est
    # recadree depuis `assets/textures/sets/120. Custom (Web of Deceit).webp`.
}

# La page 1 de tout livret officiel est sa COUVERTURE. Elle sert de vignette a
# la campagne dans l'ecran de selection (19/09/2026) : meme largeur que les
# planches, meme dossier, un nom reserve.
COUVERTURE = "00-couverture.jpg"

CARTES = {
    "next_evol": {
        "pdf": "mc40_next_evolution_rulebook-web.pdf",
        # p6 : regles du mode campagne. p7 : manigances de campagne et expert.
        "regles_campagne": [6, 7],
        # Mise en page melangee : tantot UNE planche entre deux scenarios (elle
        # sert alors des deux cotes), tantot DEUX (chacune la sienne).
        "scenarios": [
            ("morlock_siege", 1, 8, [9], 10),
            ("on_the_run", 2, None, [11], 12),
            ("juggernaut", 3, 13, [14], 15),
            ("mister_sinister", 4, None, [16], 17),
            ("stryfe", 5, None, [18], [19, 20]),
        ],
    },
    "aoa": {
        "pdf": "mc45_age_of_apocalypse_rulebook.pdf",
        # p4 regles du mode campagne, p5 les missions annexes, p6 les tentatives.
        "regles_campagne": [4, 5, 6],
        "scenarios": [
            ("unus", 1, 7, [8], 9),
            ("four_horsemen", 2, 10, [11, 12], 13),
            ("apocalypse", 3, None, [14], 15),
            ("dark_beast", 4, None, [16], 17),
            ("en_sabah_nur", 5, 18, [19, 20], 21),
        ],
    },
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
    "aos": {
        "pdf": "mc50_rulebook-web.pdf",
        # p4 : mode campagne. p5 : le Conseil et la preparation des preuves.
        # p6 : le set modulaire, la campagne experte, la collecte des preuves.
        "regles_campagne": [4, 5, 6],
        # Le scenario 5 est le seul dont la description et les instructions de
        # campagne tiennent sur deux pages (18 et 19).
        "scenarios": [
            ("black_widow", 1, 8, [9], 10),
            ("batroc", 2, None, [11], 12),
            ("modok", 3, None, [13], 14),
            ("thunderbolts", 4, None, [15], [16, 17]),
            ("baron_zemo", 5, None, [18, 19], [20, 21]),
        ],
    },
    "gmw": {
        "pdf": "mc16_galaxys_most_wanted_rules_website-compressed.pdf",
        # p4 : cartes de campagne et regles du mode. p5 : campagne experte,
        # unites et Marche.
        "regles_campagne": [4, 5],
        # Les planches vont par paires ici : la campagne ouvre sur une double
        # page (6-7), et la scene d'apres Nebula en occupe une autre (16-17).
        # Chaque planche unique sert d'epilogue a un scenario ET d'intro au
        # suivant, sans etre dupliquee.
        "scenarios": [
            ("brotherhood_of_badoon", 1, [6, 7], [8], 9),
            ("infiltrate_the_museum", 2, None, [10], 11),
            ("escape_the_museum", 3, None, [12], 13),
            ("nebula", 4, None, [14, 15], [16, 17]),
            ("ronan", 5, None, [18], 19),
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

    a_rendre[1] = COUVERTURE

    for rang, page in enumerate(carte["regles_campagne"], 1):
        a_rendre[page] = nom_fichier(0, None, "regles", rang)

    precedent_epilogue = None
    for scenario, numero, intro, regles, epilogue in carte["scenarios"]:
        bloc = {}
        # Pas d'intro propre : on reprend la planche qui a clos le scenario
        # precedent, sans la dupliquer.
        if intro is not None:
            # Une intro peut tenir sur une double page : gmw ouvre sur deux
            # planches qui ne se lisent qu'ensemble.
            pages_intro = intro if isinstance(intro, list) else [intro]
            noms = []
            for rang, page in enumerate(pages_intro, 1):
                f = nom_fichier(numero, scenario, "intro", rang)
                a_rendre[page] = f
                noms.append(f)
            bloc["intro"] = noms
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
