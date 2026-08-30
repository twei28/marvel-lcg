# -*- coding: utf-8 -*-
"""Recette des images du pack SPEED : assets/pics/ est gitignore, donc cette
recette est la seule chose reproductible. Source : zip fan-made
'Speed-20260813T091219Z-1-001.zip' (CptScorp), extrait par
`python3 -m zipfile -e`.
"""
import os
import shutil

SRC = "/tmp/claude-1000/speed_zip/Speed"
DST = ("/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Jeu Marvel Champions/"
       ".claude/worktrees/okoye/Fusion/marvel-lcg-src/assets/pics")

MAP = {
    "sd001a": "Speed Hero.png",
    "sd001b": "Speed AE.png",
    "sd002": "Hero Cards/01. Quicksilver.png",
    "sd003": "Hero Cards/02. Blasting Velocity.png",
    "sd004": "Hero Cards/03. Blasting Velocity.png",
    "sd005": "Hero Cards/04. I_m Out.png",
    "sd006": "Hero Cards/05. Kinetic Flurry.png",
    "sd007": "Hero Cards/06. Kinetic Flurry.png",
    "sd008": "Hero Cards/07. Swift Strikes.png",
    "sd009": "Hero Cards/08. Swift Strikes.png",
    "sd010": "Hero Cards/09. Swift Strikes.png",
    "sd011": "Hero Cards/10. Top Speed.png",
    "sd012": "Hero Cards/11. Top Speed.png",
    "sd013": "Hero Cards/12. Mother_s Protection.png",
    "sd014": "Hero Cards/13. Explosive Touch.png",
    "sd015": "Hero Cards/14. Never Ending Spark.png",
    "sd016": "Hero Cards/15. Quick Adaptation.png",
    "sd017": "Encounter Cards/Obligation Speed.png",
    "sd018": "Encounter Cards/01. The Real Question.png",
    "sd019": "Encounter Cards/02. Coat of Arms.png",
    "sd020": "Encounter Cards/03. Inspirational Art.png",
    "sd021": "Encounter Cards/04. Magic Chains.png",
    "sd022": "Encounter Cards/05. Conflicted Feelings.png",
}

if __name__ == "__main__":
    for cid, rel in sorted(MAP.items()):
        s = os.path.join(SRC, rel)
        assert os.path.exists(s), s
        shutil.copyfile(s, os.path.join(DST, cid + ".png"))
    print(len(MAP), "images copiees dans assets/pics/")
