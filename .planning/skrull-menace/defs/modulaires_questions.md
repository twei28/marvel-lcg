# Sets modulaires restants (sk228-sk262) — questions ouvertes pour l'utilisateur

Format : card_id, phrase imprimee, lectures possibles, lecture RETENUE (implementee), chemin de l'image.
Images : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Modular Sets/<dossier>/` (`<dossier>` :
`Shaper of Worlds (Skrull Menace Expansion Content)`, `Crusader (Skrull Elite) (...)`, `Jazinda (Skrull Elite) (...)`,
`Skymax (...)`, `War Skrull (...)`, `Xavin (...)`, `Standard Skrull-Expert Skrull (...)`).

## Lectures d'icones faites sur les scans (a confirmer)

Methode : decoupe de la boite de texte + glyphes de `public/fonts/ChampionsIcons.ttf` (`H` Hazard, `A` Acceleration,
`C` Crisis), comparaison cote a cote (fiche `docs/reference/mots-cles/hazard.md`). La transcription disait « box-with-plus ».

| card_id | Icone lue | Image |
|---|---|---|
| sk229 Cosmic Cube Creation | ACCELERATION (croix + pointe + barre) | `Shaper of Worlds/2 cosmic cube creation.png` |
| sk239 Stealing for the Empire | ACCELERATION | `Jazinda/4 stealing for the empire.png` |
| sk234 Spy Training | HAZARD (carte penchee nue) | `Crusader/4 spy training.png` |
| sk248 Skrull Geneticist (au milieu de la boite de texte, la transcription disait « acceleration-style ») | HAZARD | `War Skrull/4 skrull geneticist.png` |
| sk252 Super-Skrull Training Program (transcription : « Y/arrow shape ») | AMPLIFY (croix + avion) | `Xavin/4 skrull training program.png` |
| sk243 Surprising Alliance, sk249 Cloning Program | AUCUNE icone au milieu de la boite | `Skymax/4 ...`, `War Skrull/5 ...` |

Si l'une de ces lectures est fausse : corriger la cle `desc` (`Hazard` / `Acceleration` / `Amplify`) dans `defs/modulaires_cards.py`
et rejouer `defs/inserer_modulaires.py`.

## 1. sk234 Spy Training — « Defeat an ally you control **and** give the villain 1 facedown boost card »

- Lectures : (a) deux effets independants : la carte de boost est donnee meme si le joueur n'a aucun allie ; (b) la carte de
  boost n'est donnee que si un allie a ete vaincu.
- RETENU : (a) (le « and » n'est pas conditionnel ; rien d'autre n'est imprime). Cas `sk234 ... SANS allie`.
- Image : `Crusader/4 spy training.png`.

## 2. sk243 Surprising Alliance — « Forced **Response**: When a player discards an ally from their hand, they put that ally into play ... **instead** »

- Phrase : le type imprime est Reponse forcee (« apres »), mais le texte dit « instead » (remplacement de la defausse).
- Lectures : (a) remplacement de la defausse (l'allie ne va jamais a la defausse) ; (b) apres la defausse, l'allie est repris de la
  defausse et mis en jeu.
- RETENU : (a), en `WhenCardWouldDiscard` + `SetBeInstead` (capacite automatique, sans etape de reponse). Toute defausse d'un
  allie DEPUIS LA MAIN est visee (fin de tour, cout d'une carte, effet adverse), « a player » = n'importe quel joueur.
- Image : `Skymax/4 surprising alliance.png`.

## 3. sk229 Cosmic Cube Creation / insert Shaper of Worlds — moment de la mise de cote

- Insert : « During setup, set Shaper of Worlds minion and all four Cosmic Cube Fragment resources aside ».
- Le moteur cree les cartes d'un set modulaire AVANT toute capacite de carte du set ; seule sk229, qui reste dans le deck rencontre,
  les remet de cote, a la fin de la mise en place (`AfterGameSetup`, apres les mulligans). Un effet de mise en place du mechant qui
  fouillerait le deck rencontre AVANT cette fenetre pourrait donc croiser Shaper ou un fragment (aucun mechant du coffret ne le fait).
- RETENU : mise de cote par sk229 (`MettreDeCoteLeSet`, `shaper_of_worlds/__init__.py`) ; la campagne (agent suivant) devra, pour un
  Shaper deja en jeu / dans la zone de cooperation, ne pas rappeler cette fonction. Alternative moteur (modifier `world.py`) refusee : fichier partage.

## 4. sk228 Shaper of Worlds — « Forced **Interrupt**: When Shaper of Worlds enters your hand »

- RETENU : `AfterCardEnterHand(ForcedInterrupt, "This")` : la carte entre en main, puis (sans fenetre de reponse intermediaire)
  4 cartes du deck rencontre sont defaussees et Shaper est mis en jeu engage. Observable : identique a un vrai « when ».
- Limite de mesure : `Puzzle.Gain` (le harnais) ne declenche pas la fenetre « enters your hand » ; le cas passe par `Puzzle.Draw`
  (vrai chemin du moteur, meme que pour les cartes officielles `bk002` / `vz036`).

## 5. sk250 Xavin — « Discard cards from the encounter deck until a **treachery** is discarded »

- Lectures : (a) type Treachery seulement ; (b) type Treachery OU trait TREACHERY (les evenements de Lyja, qui se melangent au
  deck rencontre et s'y comportent en traitrises : decision utilisateur du 15/10/2026 pour sk066 Paibok).
- RETENU : (b) (`EstTraitrise`, `skrull_elite_xavin/__init__.py`), par coherence avec la decision de sk066. Sans heros Lyja le deck ne
  contient que des traitrises de type Treachery : aucune difference.

## 6. sk253 Going Nova — « Assign 2[per_hero] indirect damage **among players** »

- Lectures : le premier joueur reparti ; le joueur qui revele reparti.
- RETENU : le PREMIER joueur reparti entre les personnages de TOUS les joueurs (meme lecture que sk163 Asti, deja validee dans le lot 1).
  Un seul joueur : aucune difference.

## 7. sk249 Cloning Program — « Each SKRULL minion activates 1 additional time **during the step two** of the villain phase »

- Lectures : (a) l'activation de surcroit suit IMMEDIATEMENT l'activation de chaque sbire SKRULL ; (b) toutes les activations de
  surcroit viennent apres les activations normales (fin de l'etape 2).
- RETENU : (a) (`AfterEnemyActivationEnd` filtre sur l'etape 2). Deux exemplaires en jeu = deux activations de surcroit (cumul).
  Une activation de surcroit n'en declenche pas d'autre. Visee : le meme joueur que l'activation d'origine.

## 8. sk260 Replaced Archenemy — « find your nemesis minion, **attach this card to it and reveal it** »

- Phrase : l'ordre imprime est « attachez, puis revelez ». Le moteur refuse d'attacher a une carte encore hors jeu (`AttachTo2` echoue
  en silence), donc le sbire est REVELE d'abord, puis la carte s'y attache. Difference observable : le « When Revealed » du sbire
  nemesis se resout sans le trait SKRULL ni le +1 MNG (aucun sbire nemesis officiel ne lit SKRULL a sa revelation).
- Aucun sbire nemesis trouvable : la carte est defaussee (non precise par le texte).

## 9. sk262 Tricky Assault — numero imprime « 162 »

- Coquille evidente (Angar the Screamer, sk162, porte deja ce numero ; l'ensemble est « EXPERT SKRULL (3/3) ») : card_id **sk262**.
- Image : `Standard Skrull-Expert Skrull/13 tricky assault.png`.

## 10. sk237 Skrull Energy Gun — « Hero Action: Spend a [physical] resource → attach this card to **another enemy** »

- RETENU : UNE ressource physique (`Cost("R")`) ; « another enemy » = tout ennemi en jeu (sbire ou mechant, SKRULL ou non) different de
  l'hote ; la cible est choisie dans l'effet (apres le cout) et l'action n'est pas offerte s'il n'y a aucun autre ennemi. Sur un hote
  non-SKRULL, les trois mots-cles (Deferlement, Perçant, Distance) ne s'appliquent pas, le +1 ATQ imprime reste.
- Raison technique du choix « cible dans l'effet » : une cible obligatoire declaree sur l'action la rend « forcee » pour le pilote de
  l'autoplay, qui la rejouait sans fin quand la ressource manquait (partie « bloquee », graine 2 du 15/10/2026).

## 11. sk251 Invisible Forcefield — mechants a PV infinis

- « The enemy with the highest printed hit points » : dans le scenario Skrull Empire les mechants ont des PV infinis (`INF`) et
  porteraient donc toujours la carte, alors que leurs degats sont deja detournes sur l'environnement. Non traite specialement (le texte
  ne le prevoit pas) ; a revoir quand le scenario 1 et ce set se rencontrent (campagne).

## 12. Alternatives Standard Skrull / Expert Skrull — interface

- Les ensembles sont les fichiers `data/encounter_sets/standard_skrull.json` et `expert_skrull.json` : leur NOM commence par
  « standard » / « expert » (convention du moteur : `SetModularSetsAside` ne les compte pas comme modulaires ; `catalog.js` les classe
  `standard` / `expert`). Ils remplacent bien Standard / Expert quand un scenario les declare.
- L'ecran de choix de niveau (`public/js/prepare/niveau-standard.js`, `NIVEAUX_STANDARD`) ne les propose PAS (fichier d'interface
  partage, hors perimetre) : ajouter « Standard Skrull » (et un equivalent pour Expert) est une decision d'interface a prendre.
