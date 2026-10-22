# Shadowland : ce que le moteur devra savoir faire

Etabli le 22/10/2026 depuis les textes transcrits (`cartes.md`) et les decisions de `QUESTIONS.md`. **Rien n'est code** (l'utilisateur ne veut pas qu'on touche au moteur pour l'instant). Liste a completer a la relecture fine de chaque carte ; l'ordre est celui de Shadows in the Night, premier scenario.

## Donnees et affichage

| Besoin | Cartes | Etat |
|---|---|---|
| **PV infinis** (« HIT POINTS ∞ » : affiches « ∞ », jamais vaincu, degats comptes) | sl037 | decision Q1 ; valeur « infinie » dans `desc` + rendu a creer |
| **TargetThreat ∞** d'un complot principal | sl038b | meme principe que Q1 ; a creer |
| **★ affiche apres une valeur** (ATK, SCH, escalade) | sl037, sl012-sl017, sl031, sl034, sl057-sl059, sl061b... | decisions Q2/Q3 ; rendu a creer (la valeur reste celle du `desc`) |
| **Case de cout vide** (upgrade sans `Cost`) | sl072a/b | rien a faire : le scan l'affiche |
| **Traits absents du `Literal`** `TRAITS` (`card_face.py:73`, typage seul) | OVERPOWERING, POSSESSED | a ajouter ; « overpowering » est un TRAIT (cf. sl061a, sl077, sl078 « has the OVERPOWERING trait »), pas un mot-cle |
| Mots-cles : fiches `docs/reference/mots-cles/` | Steady, Toughness, Guard, Villainous, Surge, Peril, Patrol, Retaliate, Stalwart, Quickstrike, Assault, Linked, Overkill, Piercing, Ranged, Setup, Permanent... | **toutes presentes** (verifie le 22/10/2026) ; relire `linked.md` pour la forme « Linked (A, B, or C) » avant de coder |

## Mecaniques nouvelles (Shadows in the Night)

1. **Positions** (sl003 villain, sl004 hero) : deux cartes Environnement recto-verso mises en jeu ensemble, « change the villain's position » = retourner sl003, action du premier joueur = effet au choix puis retourner sl004 (decision Q4). Effets continus selon que les positions sont egales (+1 ATK a chaque personnage) ou differentes (-1 degat par attaque a chaque personnage, menace non retirable du complot principal). Recto-verso d'ENVIRONNEMENT : a verifier dans le moteur.
2. **Vilain tire au hasard** parmi les 6 Dark Proteges du set (decision Q5) ; ses 5 cartes liees (Linked) melangees dans le deck de rencontre, les autres mises de cote.
3. **Complot principal a deux etapes** : « Forced Interrupt: when the villain would be defeated on side A, instead flip it to side B, reset its hit points, change the villain's position, deal each player 1 facedown encounter card » ; vaincu face B = victoire ; etape 2B terminee = defaite. Mode expert : +1 SCH et +3 PV par joueur (applique uniquement en expert).
4. **Recherche dans le deck et la defausse de rencontre** d'un sbire, chaque joueur, puis melange (sl002a).
5. A relire : effets « Boost » en etoile, cartes « Surround the Fortress », « Strategic Positioning » (l'icone acceleration/hazard accordee selon la position du vilain).

## Shadow Labyrinth et Heart of Shadow (apercu, non etudie)

- Pile de **trap deck** et son defausse, cartes TRAP! (Avoid / Disarm / Trip, choix du joueur avec depense de ressources).
- **Compteurs de passage** sur Shifting Corridors, remplacement des degats par du retrait de menace (sl038b).
- **Corruption** : Creeping Corruption (upgrade permanente, Setup, 1 par joueur, compteurs, se retourne a 5, face B « vous etes vaincu » a 5), vilains Krahllak I-III, set Black Flower.
