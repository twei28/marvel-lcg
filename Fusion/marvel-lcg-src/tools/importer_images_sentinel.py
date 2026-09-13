# -*- coding: utf-8 -*-
"""Recette des images du pack SENTINEL : `assets/pics/` est gitignore, donc
cette recette est la SEULE chose reproductible du depot.

Source : archive fan-made `Sentinel-20260912T162606Z-1-001.zip` (T-Wrecks),
deposee par l'utilisateur sur le Bureau et extraite par
`python3 -m zipfile -e Sentinel-*.zip /tmp/sentinel/`.

⚠ PIEGES DU MATERIEL, releves image par image le 12/09/2026 :
 - les noms de fichiers ne suivent AUCUNE convention : `Sentinel (18).png` est
   la face HEROS et `(19)` la face alter-ego, `Mark VII-A (2).png` est le seul
   exemplaire du sbire, et `Rogue Asset~3.jpg` est le seul JPG du lot ;
 - les exemplaires multiples portent des suffixes fantaisistes
   (`Hardwire Access.png`, `(1)`, `(2)` pour les trois memes cartes) : une
   seule image par card_id suffit, le moteur ne distingue pas les tirages ;
 - `Insert.jpg` (definition du mot-cle DESTROY) et `Cover.jpg` ne sont PAS des
   cartes : elles n'entrent pas au catalogue.
"""
import os
import shutil

SRC = "/tmp/sentinel/Sentinel"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "pics")

MAP = {
    "st001a": "Identity/Sentinel (18).png",
    "st001b": "Identity/Sentinel (19).png",
    "st002a": "Components (Setup)/Head A.png",
    "st002b": "Components (Setup)/Head B.png",
    "st003a": "Components (Setup)/Arms A.png",
    "st003b": "Components (Setup)/Arms B.png",
    "st004a": "Components (Setup)/Torso A.png",
    "st004b": "Components (Setup)/Torso B.png",
    "st005a": "Components (Setup)/Legs A.png",
    "st005b": "Components (Setup)/Legs B.png",
    "st006": "Deck/Exterminate (3).png",
    "st007": "Deck/Hardwire Access.png",
    "st008": "Deck/Rocket Punch (1).png",
    "st009": "Deck/Threat Suppression (1).png",
    "st010": "Deck/justonseyfert.png",
    "st011": "Deck/propulsionarray.png",
    "st012": "Deck/reinforcedplating.png",
    "st013": "Deck/targetingprotocol.png",
    "st014": "Ob-Nem/Obligation.png",
    "st015": "Ob-Nem/Mark VII-A (2).png",
    "st016": "Ob-Nem/Rogue Asset~3.jpg",
    "st017": "Ob-Nem/Disabled.png",
    "st018": "Ob-Nem/Viral Assault.png",
    "st019": "Ob-Nem/Hostile Override.png",
    "st020": "Extras/Size Advantage.png",
    "st021": "Extras/Reboot_1.png",
    # Quatrieme carte d'etat du moteur, pack `status` et non `sentinel` :
    # elle vit a cote de tough.jpg, stunned.jpg et confused.jpg.
    "exposed": "Exposed Status.png",
}

if __name__ == "__main__":
    for cid, rel in sorted(MAP.items()):
        s = os.path.join(SRC, rel)
        assert os.path.exists(s), s
        ext = ".jpg" if s.lower().endswith(".jpg") else ".png"
        shutil.copyfile(s, os.path.join(DST, cid + ext))
    print(len(MAP), "images copiees dans assets/pics/")
