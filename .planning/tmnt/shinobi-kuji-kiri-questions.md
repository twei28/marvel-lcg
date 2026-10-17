# TMNT Shinobi Kuji-Kiri (`sj001`-`sj020`) : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/zip-shinobi/TMNT Shinobi/Kuji-Kiri/`.
Une question à la fois, scan à l'appui (montrer l'image avant de poser la question).

## Q-K1 : sj020 Æthreal Shift : « Hero Action » imprimée devant un déclencheur d'INTERRUPTION
- Scan : `K20 Aethreal Shift.png`. Texte imprimé : « **Hero Action** *(defense/thwart)*: **When your hero would take any amount of
  damage from an attack**, prevent all of that damage. Remove threat from a scheme equal to the amount of damage prevented this way. »
  Une Action se joue pendant VOTRE tour, quand vous avez la main ; « When ... would take damage » est la formulation d'une
  Interruption (cf. `up004` Autodefenestration : « **Hero Interrupt** *(defense)*: When you would take any amount of damage from an
  attack, prevent all of that damage »). Coquille probable de type de capacité.
- Options : (a) **Hero Interrupt (defense/thwart)** (recommandée : c'est le seul type qui puisse se jouer au moment des dégâts ;
  le reste du texte est inchangé) ; (b) lecture littérale « Hero Action » : la carte ne peut jamais se jouer utilement
  (aucun dégât « sur le point d'être subi » pendant votre tour hors attaque en cours), donc inerte ; (c) autre (précise).
- Effet en jeu : (a) la carte annule une attaque subie par le héros et retire autant de menace d'une manigance ; (b) carte morte.
- Provisoire : (a) (code en Interruption de héros, 5 cas verts ; le texte `cards.json` et le FR gardent le « Hero Action » IMPRIMÉ). `sj020` : **NON terminée** (attend Q-K1).
- À corriger si l'utilisateur répond autre chose : `src/cards/pack/tmnt_shinobi_kuji_kiri/sj020.py` (type de capacité), `data/cards.json`
  (texte, qui garde pour l'instant le « Hero Action » imprimé), `textes-fr-fanmade.ts` (`sj020`), cas `[sj] sj020`.

## Notes sans question (relevées, aucune décision en jeu)
- Fautes d'impression conservées telles quelles (le scan fait foi) : `sj015` Morphic Charm, citation « top three **wierdest** sensations » ;
  `sj006` Enthrall imprime « blank **textbox** » (les officielles : « blank text box »). Aucune conséquence en jeu.
- `sj014` imprime « Kuji-Kaij**ū** » (nom du fichier : `Kuji-Kaiju`) ; `sj020` imprime « **Æ**threal » (fichier : `Aethreal`). Les noms de
  `cards.json` suivent le scan.
- Homonymes d'officielles confirmés DIFFÉRENTS sur le scan : `sj001` Foresight (`mw009` Foresight de Madame Web : Interruption ;
  `vp008` Foresight de Venompool : amélioration). Aucun autre homonyme dans les 20 cartes (recherche par nom sur tout `cards.json`).
- `sj009` Armageddon : « each identity gets +1 hand size in hero form » est lu comme un bonus de la FORME HÉROS (l'alter ego ne gagne rien).
- Observation moteur PRÉEXISTANTE, hors périmètre (pas de décision prise) : un coût « défaussez les N cartes du dessus du deck de
  rencontre » (`CostFunc.DiscardDeckTopCards("EncounterDeck", N)`, déjà employé par `falcon/53002`, `53010`, `bp/51015`) ne se paie pas quand
  le deck de rencontre contient moins de N cartes (le moteur défausse, remélange et s'arrête : `continue_after_shuffle=False`), la carte
  n'est pas résolue et les cartes déjà défaussées ne sont PAS restituées. Concerne `sj010` Flash Ward (N = 2) et `sj011` Unravel (N = 3) dans
  le cas rarissime d'un deck de rencontre quasi vide. Non prouvé, non modifié.
