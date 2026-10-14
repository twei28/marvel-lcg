# Vérification groupe expert-hunter (hs206 à hs226)

Les 21 scans ont été lus. Les textes d'ambiance sont ignorés (consigne). Chaque carte du set Expert existe en 4 exemplaires (#1 à #4), chacun avec sa propre numérotation (n/4) ; les cartes sont recto simple.

## Récapitulatif

| card_id | verdict | résumé |
|---|---|---|
| hs206 | CONFORME | Son of Kraven, Minion, SCH 1, ATK 2, PV 2 (disque orange sous l'illustration), Hunter/Mercenary, Quickstrike. Set #1 (1/4) |
| hs207 | CONFORME | Captured!, Obligation, texte identique. #1 (2/4) |
| hs208 | CONFORME | Hunted!, Obligation, texte identique. #1 (3/4) |
| hs209 | CONFORME | Poisoned!, Treachery, texte identique (icône éclair = energy, voir note 1). #1 (4/4) |
| hs210 | CONFORME | Son of Kraven, identique à hs206. #2 (1/4) |
| hs211 | CONFORME | Captured!, identique. #2 (2/4) |
| hs212 | CONFORME | Hunted!, identique. #2 (3/4) |
| hs213 | CONFORME | Poisoned!, identique. #2 (4/4) |
| hs214 | CONFORME | Son of Kraven, identique. #3 (1/4) |
| hs215 | CONFORME | Captured!, identique. #3 (2/4) |
| hs216 | CONFORME | Hunted!, identique. #3 (3/4) |
| hs217 | CONFORME | Poisoned!, identique. #3 (4/4) |
| hs218 | CONFORME | Son of Kraven, identique. #4 (1/4) |
| hs219 | CONFORME | Captured!, identique. #4 (2/4) |
| hs220 | CONFORME | Hunted!, identique. #4 (3/4) |
| hs221 | CONFORME | Poisoned!, identique. #4 (4/4) |
| hs222 | ÉCART (mineur) | Rabid Rodents : "gets" au singulier et "Vermin (Clone)" ; mention "Hunter Mode Only." absente du JSON |
| hs223 | ÉCART | Sting of the Scorpion : texte reformulé ("must choose to either...or"), pas la liste de deux choix du scan |
| hs224 | ÉCART | Cold-Blooded : nom sans tiret, "each main scheme" au lieu de "the main scheme", "facedown" omis |
| hs225 | CONFORME | Aerial Excellence : texte identique (mention "Hunter Mode Only." non transcrite, voir note 2) |
| hs226 | ÉCART | Master Trapper : "1 facedown" omis deux fois, "from the TRAP deck" ajouté |

Note 1 (hs209, 213, 217, 221) : l'icône dans "spend a [icône] resource" est un éclair stylisé noir, forme du symbole d'énergie. Cohérent avec [energy]. Pas de doute notable, mais c'est une identification par la forme.
Note 2 : les 5 cartes Hunter Mode portent en italique "Hunter Mode Only." en tête de zone de texte. C'est une restriction de mise en place (carte utilisée uniquement en mode Hunter), pas de l'ambiance. Absente du JSON sur les 5 ; à vérifier que le script/la campagne ne met ces cartes en jeu qu'en mode Hunter. Pour hs225 c'est la seule différence.
Pied de carte des 5 Hunter Mode : "CAMPAIGN - HUNTER MODE", Cycle 2, aucune stat, aucun numéro de collection, recto simple.

## Détail des écarts

### hs222 Rabid Rodents (ÉCART mineur)
- Scan : "Hunter Mode Only. / Vermin and Vermin (Clone) gets +1 ATK. / Forced Response: After a RAT minion enters play, place 1 threat on it."
- JSON : "Vermin and Vermin Clone get +1 ATK.\n<b>Forced Response</b>: After a [[RAT]] minion enters play, place 1 threat on that minion."
- Différences : nom "Vermin (Clone)" avec parenthèses (nom exact de la carte à cibler, à vérifier dans le JSON de Vermin Clone) ; "Hunter Mode Only." absent ; "it" devenu "that minion" (équivalent).
- Effet : aucun si le nom de cible correspond bien à la carte ; sinon le +1 ATK ne s'appliquerait pas au clone.

### hs223 Sting of the Scorpion (ÉCART)
- Scan : "Forced Response: After the villain phase ends, the first player chooses: • Place 1 wound counter on J. Jonah Jameson. • Discard cards from the encounter deck until an attachment is discarded. Reveal that card."
- JSON : "After the villain phase ends, the first player must choose to either place 1 wound counter on J. Jonah Jameson or discard cards from the top of the encounter deck until an attachment is discarded and reveal it."
- Différences : reformulation en phrase unique ; "from the top of" ajouté ; "and reveal it" vs phrase séparée "Reveal that card". "the first player chooses" vs "must choose to either".
- Effet : sens de jeu identique. Écart de forme uniquement. Le moteur lira le même effet.

### hs224 Cold-Blooded (ÉCART)
- Scan : titre "Cold-Blooded" ; "The target threat value of the main scheme is reduced by 1[per hero, icône silhouette]. / Forced Response: After Curtis Connors activates against your hero, deal yourself 1 facedown encounter card."
- JSON : name "Cold Blooded" ; "The target threat value of each main scheme is reduced by 1[per_hero]." ; "deal yourself an encounter card."
- Différences : (a) tiret du nom perdu ; (b) "each main scheme" au lieu de "the main scheme" ; (c) "1 facedown" omis.
- Effet : (a) cosmétique ; (b) s'il y a plusieurs main schemes en jeu, le JSON réduit chacun, le scan ne vise que "the main scheme" (un seul normalement), risque faible ; (c) important : la carte doit être distribuée face cachée (mécanique "deal facedown", révélée plus tard), le JSON laisse ouvrir une distribution face visible/révélée immédiatement.

### hs226 Master Trapper (ÉCART)
- Scan : "Forced Response: After step one of the villain phase, deal each player 1 facedown TRAP card. / Forced Interrupt: When the TRAP discard pile is shuffled back into the TRAP deck, deal the first player 1 facedown encounter card."
- JSON : "...deal each player a [[TRAP]] card from the [[TRAP]] deck. / Forced Interrupt: When the [[TRAP]] discard pile is shuffled back into the [[TRAP]] deck, deal the first player an encounter card."
- Différences : "1 facedown" omis aux deux endroits ; "from the TRAP deck" ajouté (déduction, absent du scan).
- Effet : même risque que hs224, les cartes Trap et rencontre doivent être dealt face cachée ; l'ajout "from the TRAP deck" est cohérent avec le contexte mais n'est pas imprimé.
