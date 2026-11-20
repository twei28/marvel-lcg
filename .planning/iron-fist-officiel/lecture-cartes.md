# Iron Fist officiel (MC64EN) : lecture des cartes du héros, avant toute création (19/10/2026)

Étape de LECTURE seulement, selon `docs/reference/PROCESSUS-HEROS.md` et `PROCESSUS-CARTE.md` (étapes 2, 3 et 5 en amont) : rien n'est ajouté à `cards.json`,
aucun script, aucune image déposée. Périmètre décidé par l'utilisateur : le héros (1A/1B) et ses 11 cartes signature (15 exemplaires). Les cartes d'aspect du pack
(Protection, Basic, Aggression, Leadership) sont hors périmètre. Textes : `releve-hall-of-heroes.md`. Images : 13 sur 13 lues ; 2 en haute définition (Embody the Dragon, Keep 'Em Coming).

## Mots-clés et mécaniques rencontrés
| Élément | Cartes | Fiche `mots-cles/` | État |
|---|---|---|---|
| Temporary | 5 Techniques ; Danny Rand : « Your Technique cards lose temporary » | `temporary.md` | existe ; « perdre Temporary » à vérifier côté moteur |
| Retaliate X (X variable) | Embody the Dragon | `retaliate.md` | existe ; X = compteurs de chi sur la carte : valeur dynamique à vérifier |
| Chi (compteur) | héros, Lei Kung, 8 cartes | aucune | NOUVEAU compteur : à ajouter au moteur (comme `calm`, `samurai`) |
| Trait Technique / Martial Artist / K'un-Lun / Persona / Skill / Superpower | divers | aucune (traits, pas des mots-clés) | traits à ajouter |
| Uses | aucune carte du périmètre | — | — |
| Hero Interrupt / Hero Action (thwart/attack) / Hero Resource / Response | divers | `forced-action.md` seulement pour les forcées | sous-types dédiés (leçon `27009`) |
| Ressource d'icône (Redirect Chi, Deep Breathing…) | Redirect Chi : « generate (deux étoiles) resources » ; coin Redirect Chi : étoile verte | règle : jamais à vue | l'étoile = ressource wild (cf. Lockjaw : `lj002`, `RES=G`) ; à confirmer contre une carte du même pack à la sortie |

## Lecture carte par carte (points de vigilance du processus)
- **1A Iron Fist (héros)** : THW 1 ATK 2 DEF 2, main 5, PV 10. *Martial Arts Master* : Response « After you play a card, place 1 chi counter here » ; Forced Response « After the player phase ends, remove all but 4 chi counters from here and heal 1 damage for each removed ». Pièges : « play a card » (≠ « put into play », ≠ payer en ressource) ; « here » = la carte identité (les compteurs restent au retournement) ; Forced Response seulement en forme héros.
- **1B Danny Rand (alter ego)** : REC 4, main 6, PV 10. « Your Technique cards lose temporary. » *Meditation* Action : « Search your deck and discard pile for a Technique card. Put that card into play. (Limit once per phase.) ». Pièges : sur quoi s'attache l'amélioration mise en jeu ; ce qui arrive aux Techniques en jeu quand on retourne en héros ; mélange du deck après fouille.
- **Deep Breathing** (événement 0, ×3) : Hero Action, défausse du dessus du deck jusqu'à défausser une carte « Iron Fist », l'ajouter à la main. Pièges : « an Iron Fist card » = carte du jeu signature (identifiant `IRON FIST`) ; deck épuisé sans carte trouvée.
- **Dragon Punch** (événement 2) : Hero Action (attack), 2 dégâts, jusqu'à 5 chi retirés de l'identité pour +2 dégâts chacun, étourdit si au moins 3 retirés. Pièges : « up to », « your identity », décompte des compteurs retirés.
- **Fists of Fury** (événement 1, ×2) : trois fois « Deal 1 damage to an enemy » : cibles choisies séparément.
- **The Way of Things** (événement 1, ×2) : Hero Action (thwart), 2 menaces retirées d'une manigance, option 2 chi pour retirer 2 menaces d'« a scheme ». Piège : la seconde « a scheme » est-elle la même ?
- **Lei Kung** (support 1, unique) : Action « Exhaust Lei Kung and remove 1 chi counter from your identity → draw 1 card ». Coût à deux parties : aucune ne doit être oubliée.
- **Book of the Iron Fist** (amélioration 2, unique) : Hero Action « Exhaust this card → if the top card of your discard pile is a Technique, put it into play ». Pièges : attachement de la Technique ; condition vérifiée à la résolution (le dessus de la défausse).
- **Channel the Iron Fist** (Technique) : Temporary ; Hero Interrupt « When you attack, remove 1 chi counter from Iron Fist → +1 dégât (+2 si attaque de base) ». Pièges : « you attack » (déclencheur d'attaque du héros), « by 2 instead ».
- **Embody the Dragon** (Technique, 12/15) : Temporary ; Iron Fist gagne retaliate X (X = chi sur cette carte) ; Hero Action « Move 1 chi counter from Iron Fist to this card ». Pièges : valeur dynamique de retaliate ; les compteurs sur la carte.
- **Feel the Flow** (Technique) : Temporary ; Hero Action (thwart) « Remove 1 chi counter from Iron Fist → remove 1 threat from a scheme ».
- **Keep 'Em Coming** (Technique, 14/15) : Temporary ; Hero Action « Remove 2 chi counters from Iron Fist → ready him ».
- **Redirect Chi** (Technique) : Temporary ; **Hero Resource** « Remove 2 chi counters from Iron Fist → generate (✱✱) resources ».

## Questions ouvertes pour l'utilisateur (une à la fois, en multi-choix, scan à l'appui)
1. Sur quelle carte s'attache une Technique « mise en jeu » par Danny Rand ou par le Livre ?
2. Quand Iron Fist se retourne en forme héros, que deviennent les Techniques déjà en jeu (elles redeviennent Temporary) ?
3. The Way of Things : la seconde « a scheme » peut-elle être la même manigance ?
4. Deep Breathing : que se passe-t-il si le deck ne contient aucune carte « Iron Fist » ?
5. Les compteurs de chi restent-ils sur l'identité quand elle se retourne ?
(réponses : voir `lecture-reponses.md` au fur et à mesure)
