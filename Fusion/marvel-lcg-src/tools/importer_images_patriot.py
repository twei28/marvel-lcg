# -*- coding: utf-8 -*-
"""Recette des images du pack PATRIOT : assets/pics/ est gitignore, donc cette
recette est la seule chose reproductible. Source : zip fan-made
'Patriot-20260813T091207Z-1-001.zip' (CptScorp, Marvel Champions Custom
Project, Cycle 2), extrait par `python3 -m zipfile -e`.

Le zip contient en plus '11 HP Patriot Counter.png', une banniere cosmetique
sans texte de regle : ce n'est pas une carte, elle n'est pas importee.
"""
import os
import shutil

SRC = "/tmp/claude-1000/patriot_zip/Patriot"
DST = ("/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/"
       ".claude/worktrees/okoye/Fusion/marvel-lcg-src/assets/pics")

MAP = {
    "pt001a": "Patriot Hero.png",
    "pt001b": "Patriot AE.png",
    "pt002": "Hero Cards/01. Hawkingbird.png",
    "pt003": "Hero Cards/02. Aided Defense.png",
    "pt004": "Hero Cards/03. Aided Defense.png",
    "pt005": "Hero Cards/04. Covered Fire.png",
    "pt006": "Hero Cards/05. Covered Fire.png",
    "pt007": "Hero Cards/06. Isaiah Bradley.png",
    "pt008": "Hero Cards/07. Commandeer.png",
    "pt009": "Hero Cards/08. Commander_s Orders.png",
    "pt010": "Hero Cards/09. Follow My Lead.png",
    "pt011": "Hero Cards/10. On Your Feet.png",
    "pt012": "Hero Cards/11. Patriot_s Shield.png",
    "pt013": "Hero Cards/12. Revenge.png",
    "pt014": "Hero Cards/13. The Chosen Leader.png",
    "pt015": "Hero Cards/14. Throwing Stars.png",
    "pt016": "Hero Cards/15. Working Together.png",
    "pt017": "Encounter Cards/MGH Addiction.png",
    "pt018": "Encounter Cards/01. Mr. Hyde_s Lab.png",
    "pt019": "Encounter Cards/02. Mr. Hyde.png",
    "pt020": "Encounter Cards/03. MGH Drug.png",
    "pt021": "Encounter Cards/04. Bulldozing Charge.png",
    "pt022": "Encounter Cards/05. Bulldozing Charge.png",
}

if __name__ == "__main__":
    for cid, rel in sorted(MAP.items()):
        s = os.path.join(SRC, rel)
        assert os.path.exists(s), s
        shutil.copyfile(s, os.path.join(DST, cid + ".png"))
    print(len(MAP), "images copiees dans assets/pics/")
