# Hellfire Hunt, scénario 4 « Torn » + modules Negasonic Teenage Warhead et Immensity : vrais doutes

Sources (lecture seule, extraites du zip de Dipsome) : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/6c912ee0-c9ba-469c-a5ba-e4fc4b30f45a/scratchpad/hh/Hellfire Hunt Campaign/`
(`Scenario/Torn/`, `Modules/Immensity/`, `Modules/Negasonic Teenager Warhead/`) ; les scans portés sont aussi dans `Fusion/marvel-lcg-src/assets/pics/hfNNN.jpg`.
Règle du projet : trancher par les règles, le livret et la FAQ d'abord. **La FAQ du livret est « Still thinking » pour Torn (p. 22) : aucune réponse de l'auteur.**
Chaque question : carte, lectures possibles, ce que chacune change EN JEU, recommandation. Choix provisoire déjà codé, avec le cas qui le mesure.

---

## 1. Illusory Duty (hf352, Immensity 2/8) : « If no obligation was NOT revealed this way » (double négatif)
Scan : `Modules/Immensity/2.png`. Texte : « Discard 3 cards from the top of the encounter deck. Reveal each obligation discarded in this way. **If no obligation was not revealed this way**, search the encounter deck,
discard pile, set-aside area, and removed-from-game area for a copy of your obligation, then reveal it and remove this card from the game. »

| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire, recommandée)** : coquille pour « If no obligation was revealed this way » : on ne cherche SA PROPRE obligation que si les 3 cartes n'en contenaient AUCUNE | la carte est surtout une menace d'obligation : elle en sort une au hasard si le deck en cache, et ne vous force la vôtre que quand le tirage n'en a pas donné ; la carte quitte la partie dans ce seul cas |
| B : à la lettre (« aucune obligation n'est restée non révélée » = toujours vrai, puisque toute obligation défaussée est révélée) | chaque fois : on révèle les obligations défaussées PUIS la vôtre, et la carte quitte toujours la partie : bien plus dur (jusqu'à 2 obligations par révélation) |

Cas : `[hf] hf352 ...` (4 cas : obligation défaussée / aucune obligation / défausse / témoin). Recommandation : A.

## 2. Emma Frost, retour sur la face active : « set Emma Frost's hit point dial to her printed hit points » avec Psychic Paragon (hf509) en jeu
Scans : `Scenario/Torn/2a.png` (A2), `2b.png` (B2) ; Psychic Paragon = `Scenario/Torn/9.png` (« Emma Frost gets +10 hit point »).
| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire, recommandée)** : le cadran revient à son MAXIMUM courant (PV imprimés + bonus de Paragon : 7 + 10 = 17) | Paragon garde son intérêt après la 1re défaite d'Emma (elle revient « pleine ») |
| B : le cadran revient aux PV IMPRIMÉS seuls (7) alors que son maximum est 17 | Emma revient déjà blessée de 10 tant que Paragon est en jeu : Paragon ne sert alors qu'avant la première défaite |

Cas : `[hf] hf509 Psychic Paragon + cycle d'Emma Frost ...` (17 PV pleins, 0 dégât). Note de règle (non ambiguë) : l'interruption de défaite d'Emma retire 5 menaces de CHAQUE manigance, Paragon comprise ; à 4 menaces Paragon est vaincue (cas dédié).

## 3. Quelle version des cartes est la bonne ? (anciens brouillons dans le dossier)
`Scenario/Torn/` contient, en plus des cartes finales (fichiers de mai 2025 : `1a 1b 2a 2b 3 3B 4 4b 5-10`), des états antérieurs : `a1/a2/b1/b2.png` (déc. 2024) et `3b(1).png` (oct. 2024). `a2`/`b2` sont identiques à `2a`/`2b`.
Différences : `a1` (A1) : « When Emma attacks, the attack gains piercing if a boost card of this activation has PSIONIC. After Emma schemes, place 2 threat on each side scheme » ; `b1` (B1) : piercing ET overkill, « place the same amount of threat on each side scheme » ;
`3b(1)` (1B) : seuil 11 par joueur, « After the villain phase begins, place 1 threat here for each HELLFIRE minion in play » et « each player not engaged with a HELLFIRE minion MUST reveal the top card of the Hellfire deck » (au lieu de ELITE HELLFIRE).
**Porté : les textes de mai 2025** (les plus récents, cohérents avec les cartes 142-151 du pied de carte et avec le livret p. 14). Recommandation : garder mai 2025 ; si l'auteur préfère les anciens, ce sont des ajouts de texte sur quatre cartes.

## 4. Jumpstart (hf355 / hf356, Immensity 5-6/8) : « Attach to the highest hit-point minion »
Scan : `Modules/Immensity/5.png`. « Highest hit-point » = PV IMPRIMÉS les plus hauts (**provisoire**, `highest_printed_hp`) ou PV RESTANTS les plus hauts ?
| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire)** : PV imprimés | la carte vise toujours le même sbire (le plus gros), qu'il soit blessé ou non |
| B : PV restants | elle évite un sbire déjà blessé et vise le plus « en forme » ; un sbire à 7 PV imprimés mais à 1 PV restant ne la reçoit pas |
Recommandation : A (les cartes officielles disent « most remaining hit points » quand elles parlent de PV restants).

## 5. Matter Manipulation (hf346-hf348, Negasonic 6-8/8) : « Otherwise, this card gains surge »
Scan : `Modules/Negasonic Teenager Warhead/6.png`. « Discard a card you control, then search ... and put that card into play. Otherwise, this card gains surge. »
| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire)** : surge si RIEN n'est mis en jeu à la fin (aucune carte contrôlée, coût 0, ou aucune carte moins chère) ; la défausse, elle, a eu lieu | la carte peut vous coûter une carte ET vous donner une carte de rencontre de plus |
| B : surge seulement si la carte n'a pas pu défausser (rien à défausser) ; une recherche vide après défausse ne donne pas surge | moins dur : on perd la carte défaussée, sans carte de plus |
Recommandation : A (phrase unique, « Otherwise » vise l'ensemble).

## 6. White Queen (sbires hf301 / hf302 du module Perfection) en scénario 4 : correctif PROPOSÉ à l'autre pack
Scans : `Modules/Perfection/1.png`, `2.png` (« When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card and discard this card »).
Le port du scénario 1 faisait défausser ces sbires TOUJOURS : au scénario 4 ils ne pourraient jamais entrer en jeu, et **Hellfire Assault (hf510) « if it is White Queen, Emma Frost attacks the player » serait inatteignable**.
Lecture retenue (provisoire, **fichier d'un autre pack modifié** : `hellfire_hunt_white_queen/__init__.py`, `SbireWQEntreEnJeu`) : la carte est UNIQUE (« * White Queen ») ; l'interruption ne vaut que si le VILAIN White Queen est en jeu (scénario 1).
| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire, recommandée)** : interdit seulement avec le vilain White Queen | à Torn, White Queen (DIAMOND ou PSIONIC) vient du deck Hellfire comme les autres sbires ELITE HELLFIRE ; hf510 a un sens |
| B : toujours interdit (état d'avant) | à Torn les deux White Queen du deck Hellfire sont gaspillées (carte face cachée + défausse Hellfire, en boucle) |
Cas : `[hf] hf301 White Queen (sbire de Perfection) : au scénario 4 ...` ; le cas du scénario 1 de l'autre pack reste vert.

## 7. Psychic Entanglement (hf508) contre l'interruption de défaite d'Emma : qui l'emporte ?
Scans : `Scenario/Torn/8.png` (« Threat cannot be removed from other side schemes ») et `1a.png`.
| Lecture | Ce que ça change en jeu |
|---|---|
| **A (provisoire)** : « cannot » est absolu : quand Emma serait vaincue, 5 menaces partent du complot principal et d'Entanglement elle-même, PAS de Puppetry ni des autres annexes | Entanglement protège Puppetry du recul lié à Emma, et du recul de « After an ELITE minion is defeated » (qui vise « another side scheme » : seule Entanglement peut être choisie) |
| B : l'ordre d'Emma (« remove 5 threat from each scheme in play ») est plus précis et passe outre | Entanglement ne protège alors que des contrées du joueur |
Cas : `[hf] hf508 : l'interruption de defaite d'Emma ...`. Recommandation : A.

## 8. Premier tour : le sbire ELITE HELLFIRE est révélé dès la première phase des joueurs (hf503b)
Scan : `Scenario/Torn/3B.png`. « At the start of the player phase » : le moteur envoie l'interruption dès le **round 1** : chaque joueur commence donc avec un sbire ELITE HELLFIRE engagé (il n'y a pas d'exception pour le premier tour dans le texte).
Lecture retenue : oui, dès le round 1 (A). Variante B : pas au round 1. Recommandation : A (aucune exception imprimée). Les cas de test retirent ce sbire (`libre=False`) pour mesurer, sauf les cas de mise en place.

## TRI DU 01/11/2026 (chef)
Aucune question posée à l'utilisateur : 1 (coquille évidente, A), 2 (A, garde la valeur complète), 3 (mai 2025 = version la plus récente), 5, 6, 7 (« cannot » est absolu), 8 (aucune exception imprimée) sont tranchées par les règles ou le texte. 4 Jumpstart : GARDÉ en PV imprimés, car les cartes officielles de référence (01133, 04119) au même libellé « highest hit-point » utilisent `highest_printed_hp` ; l'utilisateur a répondu « PV restants » pour hf363 (même libellé « highest hit-point », mais sur un ALLIÉ) : divergence signalée à l'utilisateur dans le rapport final, à trancher s'il veut l'aligner. Aucun changement de code.
