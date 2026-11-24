# Verdicts Batman (bm) — règles + scans relus le 26/10/2026

Sources : RR v1.8 (scratchpad/rr_v18.txt), livret de l'auteur `Batman_Rules_Insert_v1.png` (zip, extrait dans scratchpad/bm_zip/ins0-2.jpg), scans `Fusion/marvel-lcg-src/assets/pics/bmXXX.jpg`.
Images : chemin = `Fusion/marvel-lcg-src/assets/pics/<code>.jpg`.

## Vraies questions d'interprétation

1. **bm001a / bm001c Batman — plafond de 3 mélanges**
   Texte : « You are allowed to shuffle a maximum of 3 deterrence cards into the encounter deck in a round. »
   Verdict : **A confirmé** (par joueur).
   Règle : YOU, YOUR (RR p.49) : « if the word "you" can be resolved as referring to the player's identity, it must be resolved as such ». Le plafond est celui du joueur Batman. Les remélanges imposés par le livret (carte défaussée non résolue) ne sont pas faits par « you » et ne comptent pas dans les 3.

2. **bm001b Bruce Wayne — Trillionaire et les soutiens**
   Texte : « Reduce the cost of the next ARMOR, ITEM, LOCATION, TECH, VEHICLE, or WEAPON card played this round by 1. »
   Verdict : **B : le code doit changer.**
   Règle : le texte filtre par TRAIT, pas par type ; LOCATION et VEHICLE sont des traits de soutiens (Batcave, Quincarrier). Rien dans RR ne limite aux améliorations. Le moteur qui ne réduit pas un soutien est un défaut à corriger, pas une interprétation.

3. **bm002 Robin — ordre des cartes / source des dégâts**
   Texte : « After Robin defeats an enemy or removes the last threat from a scheme… place the remaining cards on top of the deck in any order. »
   Verdict : **A confirmé** sur les deux points.
   Règle : « in any order » sans sujet sur une carte joueur = le contrôleur de la carte choisit (YOU, YOUR : le joueur qui résout la capacité l'effectue). « Robin defeats » = Robin lui-même ; RR YOU, YOUR : les événements sont une extension de l'IDENTITÉ (« Attacks, thwarts… that resolve from a player playing an event are also considered to be performed by that player's identity »), donc pas par Robin.

4. **bm008 Contingency Plan — « basic power » inclut-il DEF ?**
   Texte : « Choose a basic power, Batman gets +2 for his next use of the chosen basic power this round. »
   Verdict : **B : le code doit changer** (DEF doit être proposée).
   Règle : BASIC POWER (RR p.10) : « There are five different basic powers » : ATK, THW, DEF, REC, SCH. Batman (forme héros) possède THW, ATK et DEF : les trois doivent être offertes. (REC n'existe pas sur la face Batman ; SCH ne concerne pas un héros.)

5. **bm014 Split Decision — icône à côté de la menace**
   Texte : pictogramme « carte + » sous le texte, menace 4.
   Verdict : **B : le code doit changer** : c'est une icône **Danger (Hazard)**, ajouter Hazard 1.
   Preuve : pictogramme identique à celui de 01107 Breakin' & Takin' (Rhino) dont la donnée est `Hazard: 1` et le texte « (Hazard Icon: Deal +1 encounter card during the villain phase.) ». Règle : HAZARD ICON (RR p.21).

6. **bm014 Split Decision — déclenchement sur une dissuasion retournée en BOOST ?**
   Texte : « Forced Interrupt: When a Deterrence card is revealed… »
   Verdict : **A confirmé** (non).
   Règle : BOOST (RR p.11) : les cartes de boost sont « turned face up », pas révélées ; seules les capacités « Boost » s'appliquent (« Only the ability text beneath the divider line is active on a card that is resolving as a boost card »).

7. **bm014 Split Decision / bm016 Heads I Win — icônes d'une dissuasion défaussée (point NOUVEAU, trouvé à la relecture du livret)**
   Textes : Split Decision « If that discarded card has an odd number of boost icons » ; Heads I Win « takes indirect damage equal to the number of boost icons discarded this way ».
   Verdict : **B : le code doit changer.**
   Règle (livret de l'auteur) : « If an effect references icons on a deterrence card that would have ended up in the discard pile, use the top card of the discard pile instead, otherwise discard another card for the purposes of that effect. » Aujourd'hui le code compte les icônes de la dissuasion elle-même. (La phrase de Heads I Win « If a deterrence card was discarded this way, this card gains surge » reste vraie : elle ne parle pas d'icônes.)

8. **bm015 Two-Face — quels mélanges déclenchent le bonus ? « Max twice »**
   Texte : « Forced Response: After a deterrence card is shuffled into the encounter deck, Two-Face gets +1 SCH and +1 ATK until the end of the round. (Max twice per round.) »
   Verdict : **B : le code doit changer** (en partie).
   Règle : le texte ne restreint pas la source du mélange. Ghosts of the Past ne mélange pas de dissuasion dans le deck (il les en RETIRE) : sans objet. Mais le livret dit d'une dissuasion défaussée sans être résolue : « shuffle the deterrence card/s back into the encounter deck » : c'est un mélange de dissuasion dans le deck rencontre, il doit réveiller Two-Face. Le code n'appelle `ApresMelange` que dans `MelangerUneDissuasion`, pas dans `RemelangerEnAttente`. « Max twice per round » = par Two-Face, par round : **A confirmé**.

9. **bm016 Heads I Win — égalité de PV**
   Texte : « The player with the most remaining hit points takes indirect damage… »
   Verdict : **B : le code doit changer.**
   Règle : FIRST PLAYER (RR) : « If an encounter card targets a specific player or card, and there are multiple eligible targets, the first player selects among the eligible options. » Le code prend `max()` (premier de la liste, sans choix).

10. **bm018 Sudden Strike — surge sans Batman en jeu**
    Texte : « If Batman is in play, Batman deals 3 damage to an enemy of your choice. This card gains surge. »
    Verdict : **A confirmé.** La condition « If Batman is in play » est dans la 1re phrase seulement ; « This card gains surge. » est une phrase séparée, inconditionnelle.

11. **bm020 Detective Work — « Investigate » en boost**
    Texte : « ★ Boost: Investigate. Give the enemy 1 additional boost card for this activation. »
    Verdict : **DOUTE RÉEL.**
    Règle : « Investigate » n'existe ni dans RR v1.8 ni dans le livret Batman. Le seul « Investigate X » connu (fiche `docs/reference/mots-cles/investigate-x.md`, Jessica Jones fan-made) est un mot-clé de MANIGANCE ANNEXE avec un nombre (« move X threat from the main scheme to here ») : inapplicable à une traîtrise en boost, sans X. Le fichier du zip s'appelle « UncoveringthePlan » : reste probable d'une ancienne version.
    Question pour l'utilisateur : « Detective Work, en boost : "Investigate. Give the enemy 1 additional boost card…" — le mot "Investigate" n'est défini nulle part. Que fait-on ? »
    Options : A) l'ignorer (reste d'une ancienne version), seule la carte de boost supplémentaire s'applique (Recommandé, codé) ; B) le demander à l'auteur (ES) et laisser la carte provisoire ; C) lui donner un effet maison (à préciser).

12. **bm023 / bm024 / bm025 Energy / Genius / Strength (reskins)**
    Texte : « Max 1 per deck. » (scan bm023 : « Energy », ressource double, BASIC, « By EmbitteredSoul »).
    Verdict : **B : traiter comme la même carte que 01088 / 01089 / 01090.**
    Règle : COPY (RR) : « A copy of a card is defined by title… regardless of card's type, text, artwork ». Et MAX (RR) : « The words "max" and "maximum" impose a maximum across all copies of a card (by title) ». bm023 EST une copie d'Energy : un deck ne peut pas avoir 01088 + bm023. Le plus simple est d'en faire un art alternatif de la carte officielle ; si on garde une carte à part, le constructeur doit au moins la compter par titre (à vérifier). La présentation (tuile à part ou art alternatif) n'est pas une question de règle.

## Pas des questions de règle (couverture de test, à voir en partie réelle)

- bm001c / bm001d (face Lantern) : même texte que bm001a/b (scan bm001c relu : identique sauf nom de capacité « FEAR ME!!! » et trait LANTERN au lieu de BAT FAMILY. JUSTICE LEAGUE.) ; manque un cas de test (harnais `hero_alts`).
- bm004 (plafond 3 non mesuré), bm005 (remélange après paiement), bm011, bm012, bm013 (branche 1), bm019, bm021, bm022 : branches non mesurées par les cas ; rien à trancher.
- bm003, bm006, bm007, bm009, bm010, bm017 : aucune question.

## Bilan

- A confirmé : 1, 3, 6, 10, 8 (« max twice »).
- B (code à changer) : 2 (Trillionaire sur soutiens), 4 (DEF dans Contingency Plan), 5 (Hazard 1 sur Split Decision), 7 (icônes d'une dissuasion défaussée : carte du dessus de la défausse), 8 (Two-Face sur le remélange du livret), 9 (égalité : le premier joueur choisit), 12 (reskins = copies par titre).
- DOUTE RÉEL : 11 (Investigate) — image : `Fusion/marvel-lcg-src/assets/pics/bm020.jpg`.
