# Unicité par sous-titre : modification du moteur (`CanCoexistWith`), gabarit PROCESSUS-CARTE

17/10/2026. Branche `unicite-sous-titre`. Décision de l'utilisateur : le sous-titre d'un allié est le personnage.

- [x] Lecture : `CanCoexistWith` (`src/game/card/face/model/face_name.py`) jugeait « titre commun ET même sous-titre » ;
      `correspondent` (`public/js/deckbuilder/regles.js`, Rules Reference v1.8) juge en plus : sous-titre / titre d'alter ego
      de l'un égal au titre, sous-titre ou titre d'alter ego de l'autre, titres différents compris.
- [x] Cas écrits AVANT le code, rouges : 8 cas voulus (Michelangelo+Rōnin, Donatello+Doomsayer, Raphael+Stealth Fighter,
      Leonardo+Sōhei, Jennika+Heavy Metal, Heavy Metal+Nightwatcher, ub022+Heavy Metal, ub025+Sōhei) : 8 KO sur 22.
- [x] Code : bloc ajouté après l'ancien jugement ; côté joueur seulement, pas d'identité contre identité.
- [x] Après : `[unique-st]` 22/22. Témoins officiels verts : Spider-Man/Miles, Hobie, Hawkeye Kate/Clint, Spider-Woman de Madame Web,
      `50034` Fix (Nick Fury), copies 13019/27011.
- [x] Parité moteur / deck-builder : `node --test tools/tests-lanceur/unicite-sous-titre.test.mjs` (table JSON commune).
- [x] Portée (décision 17/10/2026) : règle limitée aux paires dont une carte est TMNT (`IsTmntPaper`, liste de `data/arts_alternatifs.json`). Témoins hors TMNT : `wd118` / Spider-Man et `ra002` / `25013` coexistent comme avant.
- [x] Doc : `docs/reference/RECETTES-MOTEUR.md` §12.
- Carte terminée : OUI (voir le rapport pour les filtres de non-régression).
