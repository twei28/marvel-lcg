# -*- coding: utf-8 -*-
"""Recette des images du pack MS. AMERICA : assets/pics/ est gitignore, donc
cette recette est la seule chose reproductible. Source : zip fan-made
'Ms. America-20260829T085658Z-1-001.zip' (jakxin), extrait par
`python3 -m zipfile -e`.

Les QUATRE re-skins (ma026 a ma029) ont bien leur propre image : `full_link`
clone les REGLES, pas l'image — `Cache.LoadImage` essaie `assets/pics/<card_id>`
AVANT `link_pic`.

Non importes, ce ne sont pas des cartes : AmericaBag, AmericaDeck,
AmericaHealth, AmericaInsert (fiche de regles), AmericaPack, AmericaPlaymat,
et AmericaObligation (1).png qui est un DOUBLON exact d'AmericaObligation.png
(meme MD5).
"""
import os
import shutil

SRC = "/tmp/claude-1000/america_zip/Ms. America"
DST = ("/mnt/c/Users/arnau/Desktop/Marvel LCG/"
       ".claude/worktrees/okoye/Fusion/marvel-lcg-src/assets/pics")

MAP = {
    "ma001a": "AmericaHero.png",
    "ma001b": "AmericaAE.png",
    "ma002": "America01A - Alloy.png",
    "ma003": "America02A - Hawkeye.png",
    "ma004": "America03S - Santana Family.png",
    "ma005": "America04U - Star Light.png",
    "ma006": "America05U - Star Flight.png",
    "ma007": "America06U - HyperCosmic Awareness.png",
    "ma008": "America07R - Energy Infusion.png",
    "ma009": "America08E - Americas Anger.png",
    "ma010": "America09E - Americas Anger.png",
    "ma011": "America10E - Bulletproof Chica.png",
    "ma012": "America11E - Bulletproof Chica.png",
    "ma013": "America12E - Star Portal.png",
    "ma014": "America13E - Star Portal.png",
    "ma015": "America14E - Break Through.png",
    "ma016": "America15E - Break Through.png",
    "ma017": "AmericaObligation.png",
    "ma018": "AmericaNem01 - Catalina Chavez.png",
    "ma019": "AmericaNem02 - Search for the Cure.png",
    "ma020": "AmericaNem03 - Star Lightning.png",
    "ma021": "AmericaNem04 - Star Lightning.png",
    "ma022": "AvengerAlly - Gwenpool.png",
    "ma023": "AvengerAlly - Marvel Boy.png",
    "ma024": "AvengerSupport - Noh-Varr_s Ship.png",
    "ma025": "MarvelEvent - Power Stomp.png",
    "ma026": "MarvelEvent - Moment of Triumph reskin.png",
    "ma027": "AmericaEnergy.png",
    "ma028": "AmericaGenius.png",
    "ma029": "AmericaStrength.png",
}

if __name__ == "__main__":
    for cid, rel in sorted(MAP.items()):
        s = os.path.join(SRC, rel)
        assert os.path.exists(s), s
        shutil.copyfile(s, os.path.join(DST, cid + ".png"))
    print(len(MAP), "images copiees dans assets/pics/")
