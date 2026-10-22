# Shadowland : questions a poser a l'utilisateur

Regle du projet (`PROCESSUS-CARTE.md` etape 3) : **une question a la fois, en choix multiple, en montrant le scan**. Ce fichier est la file d'attente ; rien n'est tranche seul. Les scans sont dans `.planning/shadowland/scans-marvelsimulator/<id>.webp` (versions PNG de travail dans le scratchpad de la session).

Deja tranche sans question (preuve par comparaison a des cartes officielles) : icones Boost, Crisis, Hazard, Acceleration, voir `cartes.md`.

## A. Lectures de chiffres et de symboles (avec le scan)

1. **sl037 Shifting Corridors** : « SCH 0★ / ATK 0★ / HP ∞ ». Que veut dire l'etoile apres 0 (valeur definie par le texte) et que faut-il faire du « ∞ » ?
2. ~~sl038b Into the Labyrinth~~ : RESOLU sans question (voir journal : TargetThreat ∞, StartingThreat 25 par joueur).
3. ~~sl039b Chamber of Vile Secrets~~ : RESOLU (rond en haut a gauche = TargetThreat, bas droite = StartingThreat, par comparaison a 01097b).
4. ~~sl060b, sl061b~~ : RESOLU pour les nombres ; RESTE la petite etoile de l'escalade de sl061b (« +1★ »).
5. ~~sl001b, sl002b~~ : RESOLU (cible 7 et 8 par joueur, depart 2 par joueur).
6. ~~Villains et sbires avec « ATK 1★ / 2★ / 3★ / 4★ »~~ : RESOLU par principe (Q2/Q3 : on affiche le ★ comme sur le scan ; sur Krahllak sl057 il annonce l'Interruption ★ « gets –3 ATK »). **Villains et sbires avec « ATK 1★ / 2★ / 3★ / 4★ »** (sl012, sl013, sl014... sl057-059) : l'etoile renvoie-t-elle a un effet du texte qui modifie l'ATK ?
7. ~~sl072a/b Creeping Corruption~~ : RESOLU (rectangle blanc = case de cout vide, pas de `Cost` dans `desc` ; OVERPOWERING = trait imprime, a AJOUTER au `Literal` TRAITS du moteur). Ancienne question : **sl072a/b Creeping Corruption** : le petit rectangle blanc en haut a gauche (cout vide ?) et la ligne « OVERPOWERING » (trait ? mot-cle ?).
8. ~~« TRAP! »~~ : RESOLU (trait « TRAP! » : l'enumeration TRAITS contient `TRAP!` et non `TRAP` ; les cartes citent « a TRAP! card »). Ancienne question : **sl040, sl046, sl050-sl056 : « TRAP! »** en police speciale au centre du texte : est-ce un trait ou un mot-cle de type ?
9. ~~Icones de ressource dans le texte~~ : RESOLU par comparaison a 01088/01089/01090 (eclair = energie `Y`, petit reseau de noeuds = mentale `B` comme sur Genius 01089, poing = physique `R`) ; sequences a relire carte par carte a l'ecriture des scripts. Ancienne question : **Icones de ressource dans le texte** (sl004a, sl004b, sl015, sl018, sl054, sl055, sl063) : poing = physique, eclair = energie, silhouette = mentale ? A confirmer contre une carte officielle (jamais a vue).
10. **sl011 / sl010 / etc.** : les doublons de numerotation sont des exemplaires multiples (quantite deduite). Confirmer les quantites par carte quand le livret sera la.

## B. Choix de modelisation (impact en jeu)

11. **Positions** (sl003, sl004) : deux cartes recto-verso mises en jeu ensemble. Les modeliser comme deux cartes qu'on retourne, ou comme un etat porte par le complot ?
12. **Vilain tire au hasard** : le jeu doit-il laisser l'utilisateur CHOISIR un Dark Protege a la mise en place (en plus du hasard) ?
13. **Mode expert** de Shadows in the Night : « +1 SCH and +3 PV par joueur » : applique-t-on sur le vilain a chaque etape, comme les autres scenarios du jeu ?

## C. Absences

14. **Livret officiel du pack** (PDF FFG, mc65 rulebook) : pas encore dans le depot. Il donne la mise en place, les difficultes, la mini-campagne.
15. **Textes francais** : pas de source VF pour l'instant.

## Decisions prises (journal)

- **Q1, 22/10/2026 : sl037 Shifting Corridors, « HIT POINTS ∞ »** -> vrai « ∞ » affiche, la carte ne peut jamais etre vaincue par les degats (degats comptes mais jamais letaux). Demande une extension du moteur (a faire plus tard : valeur de PV « infinie » dans `desc`, rendu « ∞ » sur la carte).
- **Q2, 22/10/2026 : sl037, « SCH 0★ / ATK 0★ »** -> valeur 0 avec le ★ affiche comme sur le scan.
- **Sans question (22/10/2026)** : roles des nombres des complots principaux, par comparaison a 01097b (voir `cartes.md`). **sl038b TargetThreat ∞** : meme principe que Q1 (∞ reel affiche, extension du moteur plus tard) ; a rappeler a l'utilisateur au moment du cadrage moteur.
- **Q3, 22/10/2026 : sl061b, « +1 par joueur ★ » (escalade)** -> escalade +1 par joueur avec le ★ affiche.
- **Sans question (22/10/2026)** : ★ apres un ATK/SCH (principe de Q2), case de cout vide de sl072a/b (pas de `Cost`), « TRAP! » = trait (CORRECTION 22/10 : le moteur ecrit `TRAP!` avec « ! », pas `TRAP` ; Hunting Season ecrit `TRAP`, a unifier), icones de ressource (poing/eclair/reseau). Traits absents du `Literal` TRAITS du moteur (`src/game/card/face/card_face.py:73`, typage seul, aucun controle a l'execution) : **OVERPOWERING, POSSESSED**. A ajouter le moment venu.
- **Q4, 22/10/2026 : positions sl003/sl004** -> deux vraies cartes Environnement recto-verso, visibles sur le plateau, qu'on retourne (texte actif different de chaque cote).
- **Q5, 22/10/2026 : vilain de Shadows in the Night** -> tirage au hasard parmi les 6 Dark Proteges, comme imprime (sl001a) ; pas de choix a la main.
- **Sans question** : « In expert mode » des complots 1B/2B (+1 SCH, +3 PV par joueur) = appliques uniquement en mode expert, comme les autres scenarios du jeu.
- **Restent ouvertes (documents manquants)** : Q10 quantites par carte (livret ou MarvelCDB), Q14 livret officiel, Q15 textes francais.
- **Relecture complete, 22/10/2026** : les 93 faces ont ete relues par un second regard independant (5 lots croises). 23 corrections appliquees (nombres cible/depart de 65001B, 65002B, 65038B, 65039B, 65060B, 65061B ; icones de 65024, 65025, 65044-65049, 65070, 65076 ; ligne de traits retiree du texte de 65046 et 65050-65056 ; HP de 65047). Doutes restants, sans effet sur le jeu : pied de carte de 65017B coupe sur le scan (credits d'illustrateur incomplets), gras des deux-points et des guillemets de 65010 et 65038B.
- **Decision, 22/10/2026 : trait des pieges** -> Shadowland utilise `TRAP!` (imprime) ; Hunting Season garde `TRAP` (mecanique differente : pieges distribues a chaque joueur) ; on ne partage que la plomberie du `TrapDeck`. Verifie dans le code le 22/10 : 16 cartes `TRAP` (Hunting Season) contre 5 cartes `TRAP!` (Jubilee x3, Sinister Six, Web of Deceit).
