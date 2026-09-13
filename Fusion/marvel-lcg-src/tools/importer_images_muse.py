# -*- coding: utf-8 -*-
"""Recette des images du SET MODULAIRE MUSE : `assets/pics/` est gitignore,
cette recette est la seule chose reproductible du depot.

Source : archive fan-made `Muse-20260902T074120Z-1-001.zip` (Rainy), rangee
dans `A creer/` et extraite par `python3 -m zipfile -e`.

⚠ Sept fichiers pour SIX cartes : `6 Obsession.jpg` et `7 Obsession.jpg` sont
le meme carton, seul le numero de collection imprime differe (compare au
pixel sur la zone de regles, md5 differents pour cette seule raison). Le
moteur ne distingue pas les tirages : on importe le 6, le 7 n'a pas de
card_id.
"""
import os
import shutil

SRC = "/tmp/muse/Muse"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "pics")

MAP = {
    "mu001": "1 Art Imitates Death.jpg",
    "mu002": "2 Supply Run.jpg",
    "mu003": "3 Muse.jpg",
    "mu004": "4 Graffitied Streets.jpg",
    "mu005": "5 Grim Inspiration.jpg",
    "mu006": "6 Obsession.jpg",
}

if __name__ == "__main__":
    for cid, rel in sorted(MAP.items()):
        s = os.path.join(SRC, rel)
        assert os.path.exists(s), s
        shutil.copyfile(s, os.path.join(DST, cid + ".jpg"))
    print(len(MAP), "images copiees dans assets/pics/")
