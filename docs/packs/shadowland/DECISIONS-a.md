# Shadowland : decisions de l'agent « a » (set Dark Protege, sl012a/b a sl027)

Pas de livret officiel en ligne et personne a qui poser la question : chaque arbitrage ci-dessous est tranche selon la Rules Reference habituelle de Marvel Champions, avec son raisonnement. Les scripts sont dans `Fusion/marvel-lcg-src/src/cards/pack/shadowland/dark_protege/` (un constructeur par vilain et par carte liee dans `__init__.py`, les fichiers `slNNN.py` ne font que l'appeler), les cas dans `Fusion/marvel-lcg-src/tools/cas/shadowland_a.py`.

## Structure

- Recto A et verso B d'un vilain portent le MEME texte (le verso ajoute Steady + Toughness, lus dans `desc`) : un constructeur par vilain. White Tiger est la seule difference de texte : A « again **with +1 ATK** », B « again » (parametre `plus_un_atq`).
- L'etoile devant « Forced Response/Interrupt » est un marqueur (convention deja retenue par Skrull Menace et Rainy) : capacite obligatoire ordinaire, sans mecanique propre.
- « Linked (A, B, or C) » : lue dans le texte imprime par `VilainsLies` (shadowland/__init__.py, deja code par sl001a) ; aucune cle `desc.Linked` sur ces cartes.

## Arbitrages

1. **Archpriestess (sl012) : « give a minion a tough status card »** : n'importe quel SBIRE en jeu (celui d'un autre joueur compris), choisi par le joueur attaque, y compris un sbire qui a deja un Tough (rien n'est alors pose et la branche « if no tough status card was placed » joue). Raison : le texte ne restreint pas le choix ; c'est « aucune carte posee » qui declenche la seconde phrase, pas « aucun sbire ». Quand plusieurs sbires sont possibles, le joueur choisit ; un seul : automatique.
2. **Archpriestess : « deal 1 minion discarded this way »** : le joueur attaque choisit parmi les SBIRES defausses ; les traitrises restent defaussees ; aucun sbire defausse = aucune carte donnee.
3. **Daredevil (sl013) : limite « once per round per player »** : une fois par round pour chaque joueur, comptee sur le joueur qui a attaque (identite ou allie), partagee entre les faces A et B. `LimitOncePerRoundPerPlayer` plante sur ce message (assert `TriggerNonePlayerMessage`) : registre maison `LimiteParJoueurEtParRound` (copie de celui de hunting_season, cle propre a chaque vilain).
4. **Daredevil : « choose: Either discard 1 random card ... or Daredevil attacks you »** : si la main est vide, la branche « discard » n'est pas offerte (un choix sans aucun effet ne se choisit pas) ; Daredevil attaque.
5. **Elektra (sl014) : cout imprime** : seul le cout IMPRIME compte. Carte sans cout imprime (ressource) ou deck vide (rien de defausse) : ni pair ni impair, donc branche « otherwise » (overkill + piercing). Le Forced Interrupt agit AVANT l'attaque (la carte est defaussee d'abord).
6. **Gorgon (sl015) : « Spend a [physical] resource »** : une ressource physique (`Cost("R")`, une carte wild en vaut une) ; la branche n'est offerte que si elle est payable (le moteur reduirait sinon un choix payant impayable au plus gros morceau payable, `player_action.py:855`). « Stun your identity » : l'identite du joueur attaque, meme deja etourdie (la branche reste choisissable, rien n'est pose).
7. **Lady Bullseye vilain (sl016) : « undefended »** : aucun defenseur n'a ete declare (un allie qui defend, meme vaincu, rend l'attaque defendue). Deux capacites distinctes (non defendue / defendue), une seule part par attaque.
8. **White Tiger (sl017) : « attacks you again »** : une NOUVELLE attaque (nouvelle carte de boost) ; la limite est consommee AVANT la 2e attaque pour qu'elle ne se redeclenche pas ; limite partagee entre les deux faces (cle `sl017`).
9. **Art of the Kill (sl018) : « If that attack defeats a character »** : tout personnage vaincu par cette attaque (le sien ou un allie), lu apres l'attaque (`has_defeated_target`) ; « When an enemy attacks you » : seulement les attaques dirigees contre l'identite du porteur. Alter-Ego Action : `Cost("YBR")` (energie, mentale, physique : eclair, reseau de noeuds, poing, compares a Genius 01089 / Strength 01090 / Energy 01088).
10. **Krahllak's Blessing (sl019) : « from a character »** : toute source `Unit2` (heros, allie, sbire) sauf le vilain porteur lui-meme (il ne s'attaque pas lui-meme) ; si la source est l'identite d'un joueur, le vilain attaque CE joueur (il peut defendre, boost normal) ; si c'est un allie, `Enemy.AttackCharacter` ; la carte est defaussee dans tous les cas, meme si les degats retombent a 0 ; reduction jamais sous 0.
11. **Archpriestess sbire (sl020) : « If no attack was made this way »** : aucune attaque n'a eu lieu (aucun autre sbire engage, ou tous etourdis), pas « une seule attaque ratee ». Les attaques se resolvent l'une apres l'autre.
12. **Lady Bullseye sbire (sl022) : ex aequo sur le cout imprime** : le joueur choisit entre les allies ex aequo. Sans allie : l'attaque reste sur l'identite (« if able »), mais elle gagne quand meme ranged. L'attaque redirigee vers l'allie reste une attaque du joueur (meme modele que Deathbird, galactic_storm/gs114) : pas de `not_against_player`.
13. **Rite of Offering (sl024)** : le joueur qui a vaincu la manigance retire de la partie un allie qu'il controle (a son choix) ; sans allie, 3 degats DIRECTS sur son identite.
14. **Shadowy Plot (sl025)** : les trois cartes du dessus (moins s'il en reste moins) ; le joueur qui a vaincu en choisit une, qui est revelee (ses When Revealed partent) ; les deux autres sont defaussees. Deck de rencontre de moins de 3 cartes : on prend ce qu'il y a (pas de remelange de la defausse pendant l'examen).
15. **Darkness Within (sl026) : « Change to hero form »** : sans effet si le joueur est deja en forme heros ; l'attaque du vilain a lieu APRES le changement.
16. **Embraced by Darkness (sl027)** : « 2 or less threat was placed on the main scheme this way » : la menace posee par CETTE manigance, boost compris (`AfterUnitSchemeEnd.placed_threat`) ; 0 compte (manigance etourdie, par exemple).

## Cartes recto-verso et positions

Les vilains etant des cartes recto-verso retournees par sl001b/sl002b (`AbilitesComplotAvecVilainRetourne`), leurs capacites sont enregistrees par la face visible : verifie par les cas A et B de chaque vilain.

## Gabarit PROCESSUS-CARTE (resume par groupe de cartes)

Les seize cartes (22 faces) partagent les memes etapes ; le detail par capacite (carte de reference, mots-pieges, nombres) est en tete du constructeur correspondant dans `dark_protégé/__init__.py`.

- Etape 1 (cards.json) : les 22 entrees ont ete relues sur les scans (`assets/pics/sl012a` a `sl027`) : SCH/ATQ/PV, icones de boost, PV des sbires (5, rond en bas a droite), traits, texte. Aucune correction necessaire ; l'etoile apres l'ATQ n'est pas dans `desc` (marqueur renvoyant au texte, convention du pack).
- Etape 2 (references) : listees dans le docstring de chaque constructeur.
- Etape 3 (mots-cles) : fiches `docs/reference/mots-cles/` lues avant le code : villainous, guard, steady, toughness, linked, overkill, piercing, ranged. Steady/Toughness/Guard/Villainous = bases automatiques lues dans `desc` (aucun script) ; Linked a trois noms lu dans le texte (`VilainsLies`, deja code par sl001a).
- Etape 5/6 (texte contre code, nombres) : dans les docstrings (mots-pieges) ; nombres : 3 PV de reduction (sl019), 3 cartes defaussees (sl012, sl020, sl027), 2 indirects (sl015, sl023), 1 indirect (sl016), +1 ATQ (sl014, sl017a, sl018), 3 degats (sl024), 2 menaces (sl027), seuil « 2 or less » (sl027), 3 cartes regardees (sl025), cout `YBR` (sl018).
- Etape 7 (cas + substitution) : `tools/cas/shadowland_a.py`, 79 cas `[sla]`, tous verts. Preuve par substitution (module remplace par `GetAbilities -> []`) : chaque carte a au moins un cas qui passe au ROUGE et revient au vert ; les cas qui restent verts sous stub sont des temoins d'absence ou de tirage (liste dans le rapport). Ressource mixte `YBR` : le pilote du harnais ne la paie qu'avec `surpayer` et six cartes en main (voir le cas sl018).
- Etape 7 bis (limite imprimee) : Daredevil (sl013a/b) et White Tiger (sl017a/b) ont un temoin d'epuisement (deux declenchements dans le meme round, chiffre mesure au second : degats identite 3 au lieu de 6 pour Daredevil, 4 au lieu de 6 pour White Tiger A, 6 au lieu de 8 pour B).
- Etape 8 (autoplay) : voir le rapport de fin (parties par vilain, standard et expert).
- Etape 8 bis (plateau) : sl018 et sl019 s'attachent (identite / vilain), sl015 etourdit, sl012 pose un Tough : mecanismes deja affiches par le plateau ; **aucun cas plateau `.ts` ecrit** (non fait). Une partie reelle dans le navigateur reste le seul juge.

Carte terminee : OUI pour le moteur (cas + substitution) ; NON pour la verification plateau et la partie humaine.
