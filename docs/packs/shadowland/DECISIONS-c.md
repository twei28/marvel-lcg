# Shadowland, scenario 3 « Heart of Shadow » (agent c) : decisions

Cartes : sl057 a sl071 (set HEART OF SHADOW), scenarios `heart_of_shadow` et `heart_of_shadow_expert`. Code : `Fusion/marvel-lcg-src/src/cards/pack/shadowland/heart_of_shadow/`. Cas : `tools/cas/shadowland_c.py` (prefixe `[slc]`). Aucun livret officiel en ligne : quand la regle est muette, tranche selon la Rules Reference 1.8.

## 1. Corrections de `data/cards.json` (verifiees sur les scans)

| Carte | Avant | Apres | Pourquoi |
|---|---|---|---|
| sl059 Krahllak III | `Retaliate 1` seul | + `Steady 1`, `Toughness 1` | le scan imprime « Retaliate 1. Steady. Toughness. » ; sans les mots-cles du `desc` le moteur ne les lit pas |
| sl061b | `Acceleration 1` | supprime | invention du generateur : le scan n'imprime AUCUNE icone d'acceleration ; l'etoile de l'escalade « +1 par joueur ★ » renvoie au texte « ★ Forced Response » (decision Q3), elle ne donne pas de menace en plus |
| sl062 Dark Shroud | `ATK 1` | `ATK+ 1` | la cle des modificateurs d'une carte attachee est `ATK+` (lue par `HasModify`) ; `ATK` ne fait rien |
| sl064 Mark of the Wicked | `ATK 2` | `ATK+ 2` | idem |
| sl065 Pull of Power | rien | `THW+ 2` | la valeur `+2★ THW` du scan manquait |
| sl066 Fist | `Retaliate 1` | `Retaliate 2` | le scan imprime « Retaliate 2 » |
| sl070 Veil of Nightmares | `Boost 2` seul | + `StartingThreat 5*`, `Hazard 1` | menace de depart « 5 par joueur » et icone Hazard du scan (comparee a sl024) |

Le dossier `.planning/shadowland/brouillons/cards_65028_65078.json` (sortie du generateur) n'a PAS ete remis a jour : la source de verite est `data/cards.json`.

## 2. Decisions de regle

1. **« attacks you » quand l'ennemi attaque un ALLIE.** Selon la RR 1.8 p.10 (« Attacks Against Allies ») le controleur de l'allie est le joueur attaque : l'Interruption de Krahllak / Retainer part donc aussi quand ils attaquent un allie (le moteur le fait deja, `Enemy.AttackCharacter`, `ally_attack_is_against_player=True` par defaut). La variante « ne part pas » de Galactic Storm reste une question ouverte du projet ; on suit le defaut du moteur. Cas `[slc] sl057 attaque un ALLIE`.
2. **« you may place 1 corruption counter ... If you do, -3 ATK »** (sl057-sl059, sl068) : question posee au joueur attaque (`MayChooseOneAbility`, bouton Annuler), seulement s'il a une Creeping Corruption en jeu. Le moins 3 ATK ne s'applique que si le jeton est vraiment pose.
3. **Choix « each player chooses » (sl060b, sl061b) et « Choose: Either ... or ... » (sl071)** : une branche qui pose un jeton n'est offerte que si le joueur a une Creeping Corruption en jeu (sinon elle ne change rien a l'etat du jeu). Les autres branches sont toujours offertes.
4. **sl071, branche « remove 1 corruption counter ... and Krahllak attacks you »** : toujours offerte, meme sans jeton a retirer (l'attaque, elle, a lieu ; « as much as possible », RR 1.8). Le vilain vise est Krahllak par son nom, pas « le vilain ».
5. **sl061a, « each other player discards a card they control from play »** : le joueur choisit parmi ses allies, ameliorations et soutiens ; la **Creeping Corruption n'est jamais proposee** : elle est Permanent (fiche `mots-cles/permanent.md`, un effet d'un autre set ne la defausse pas) et c'est de plus une carte posee a la mise en place. S'il n'a rien d'autre en jeu, il ne defausse rien.
6. **sl061a en mode expert** : « deal each player 1 facedown encounter card » concerne tous les joueurs, ceux qui viennent de defausser comme les autres.
7. **sl060b, « After Krahllak is defeated, advance this scheme to stage 2A »** : branche sur `AfterVillainAdvanced` (le vilain suivant est deja en jeu), seulement tant que la face 1B est la, et seulement s'il reste un stade 2 dans la pile des complots (modele `ComplotEn2A` du defi MC×DC). Dernier stade de Krahllak vaincu = victoire par le moteur (la pile des vilains est vide), sans second `Advance`.
8. **sl060b, « instead remove all threat »** : le stade n'est jamais accompli ; le vilain II / III, pas ce stade, fait avancer la partie.
9. **sl067 Hellbride, « the defeating player »** : le controleur de ce qui a vaincu Hellbride (`message.defeating_player`). Sans joueur vainqueur, rien n'est fait. Ordre : jetons PUIS soin (le seuil de 5 jetons peut tomber avant le soin).
10. **sl067, Hero Action** : « If Hellbride has 2 or fewer remaining hit points » est une CONDITION D'OFFRE (PV restants, pas degats subis), le cout est « exhaust your hero », puis defausse (pas une defaite : pas de When Defeated), puis retrait d'un jeton.
11. **Couts « Place N corruption counters on your Creeping Corruption → ... »** (sl063, sl066, sl070) : le jeton est pose PAR LE COUT, et le cout est impayable sans Creeping Corruption (sinon l'action resoudrait a vide et le pilote la rejouerait a l'infini : lecon de `iron_man_model_42` `CoutDuReacteur`).
12. **sl062 Dark Shroud** : « you or an ally you control » = l'identite ou un allie du joueur qui repond (`YouControlCharacter`) ; le seuil de 4 se lit sur les degats de l'attaque ; une capacite etiquetee « (attack) » comme Swinging Web Kick est une attaque (RR). Les trois effets (prevenir, jeton, defausse) partent ensemble.
13. **sl064 / sl065, « You may attach this card to your identity. If you do not ... »** : refus = 4 degats, identite etourdie (sl064) ou confuse (sl065), 1 jeton retire de la Creeping Corruption (s'il y en a), defausse. L'effet « attached hero » ne vise que l'identite en forme de HEROS (attaque ou contre de BASE), pas un allie.
14. **sl069 Snakeroot Elders** : « If you do not » couvre le refus ET l'impossibilite (pas de Creeping Corruption) : le jeton va alors sur le sbire. Guard et patrol suivent le nombre de jetons du SBIRE (`ThisGainKeyword` + `OnEvent.Counter`).
15. **sl061b, escalade ★** : aucune mecanique de plus ; le ★ renvoie a la Forced Response de la meme face.
16. **Mode expert** : la face 1A impose seulement Krahllak (II) et (III) a la place de (I) et (II) (fichier de scenario `heart_of_shadow_expert.json`) ; aucun bonus de SCH / PV imprime, donc aucun code. L'expert se lit aussi dans sl061a (cartes face cachee).

## 3. Scenarios

- `data/scenarios/heart_of_shadow.json` : vilains `sl057`, `sl058`, complots `sl060a,sl060b` et `sl061a,sl061b`, 4 `sl072a,sl072b` MIS DE COTE (le Setup de sl060a en met un en jeu par joueur), jeu de rencontre = cartes HEART OF SHADOW (sl062-sl071) + cartes BLACK FLOWER hors Creeping Corruption (sl073-sl078), jeu `standard`.
- `data/scenarios/heart_of_shadow_expert.json` : idem avec `sl058`, `sl059`, `expert: true`, jeux `standard` et `expert`.
- **Pas encore branches** (integration apres fusion avec les branches de l'agent d) : le set modulaire **Ninja Swarm** (`modular_sets` est `[]`, comme pour `shadows_in_the_night`) et les jeux de rencontre nommes (`data/encounter_sets/`), les cartes BLACK FLOWER etant ici listees en cartes dans `encounters`. La Creeping Corruption (sl072a/b) n'a AUCUN script dans cette branche : elle est une carte porteuse de jetons `corruption`, sans retournement a 5 jetons, sans defaite, sans action (a l'agent d).

## 4. Doutes restants

- La Creeping Corruption est supposee « Permanent » apres fusion (le `desc` de sl072a n'a pas la cle ici) ; les cas ne la defaussent jamais, ils ne dependent pas de ce point.
- « Place 2 corruption counters » qui franchit le seuil de 5 (retournement ou defaite de sl072) : ordre des fenetres a prouver avec le code de l'agent d (aucun cas ici : sans script de sl072 le jeton se pose sans retournement).
- Une Interruption (non forcee) de Dark Shroud pour un ALLIE qui inflige 4 degats ou plus n'est pas prouvee au harnais (aucun allie du depot n'a 4 d'ATQ) : seule l'identite (Swinging Web Kick, 8 degats) l'est.

## 5. Gabarits PROCESSUS-CARTE (une ligne par etape, resume pour les 17 cartes)

Methode commune. **Etape 2** (references) : en tete de chaque script (`heart_of_shadow/slNNN.py`), carte modele + pourquoi + pieges. **Etape 5** (mots-pieges) : « ⚠ Mots-pieges » dans l'en-tete de chaque script (each / you / unless / if you do / instead / defeated / Forced / Interrupt / basic / attached...). **Etape 6** (nombres) : valeurs de chaque scan relues contre `cards.json` (sl057-sl071 : 7 corrections, voir §1), et dans le script (3 / 4 / 5 jetons, 2 / 3 / 4 / 5 / 6 / 9 menace, -3 ATK, 4 degats, 6 soin, 2 PV restants). **Etape 7** (cas + substitution) : `tools/cas/shadowland_c.py`, 91 cas `[slc]`, tous verts ; preuve par substitution (module remplace par `GetAbilities -> []`, `/tmp/claude-29999/slc_mut/mut.sh`) puis 18 mutations semantiques (`mut2.py`, une valeur ou une condition changee a la fois) et 7 mutations de donnees (`mut3.py`, `cards.json` remis dans son etat d'avant). **Etape 7 bis** : aucune limite « once per ... » imprimee sur le set, donc aucun temoin d'epuisement. **Etape 8** (autoplay) : 8 parties standard + 16 expert (equilibre et agressif), 0 traceback, 0 `NameError`...; un blocage (voir §6). **Etape 8 bis** (plateau) : `ui-app/src/board/shadowland-heart-of-shadow-plateau.test.ts`, 6 tests, rouges sous mutation de l'etat pose.

| Carte | Cas (preuve par substitution : rouges / total) | Reste vert sous substitution, et pourquoi |
|---|---|---|
| sl057 | 5 (3 rouges sur 5) | temoin sans Creeping Corruption, valeurs de desc (Steady) |
| sl058 | 4 (2/4) | desc seul : Toughness, Steady, temoin de refus |
| sl059 | 5 (3/5) | desc seul : Retaliate, Tough d'entree (les cartes de reference sont natives) |
| sl060a | 4 (2/4) | vilain tire par le scenario (donnees) |
| sl060b | 10 (6/10) | temoins d'absence + victoire native (pile des vilains vide) |
| sl061a | 6 (5/6) | temoin « rien a defausser » : rouge sous mutation de `CartesControleesDefaussables` |
| sl061b | 4 (3/4) | condition d'accomplissement : la perte est portee par `IfThisSchemeStageIsCompletedPlayersLoseTheGame` (testee par mutation de donnees) |
| sl062 | 5 (4/5) | temoin sans carte |
| sl063 | 6 (5/6) | temoin sans carte |
| sl064 | 5 (5/5) | |
| sl065 | 3 (3/3) | |
| sl066 | 6 (2/6) | Retaliate 2, Patrol, absence : lus dans `desc` (rouge sous mutation de donnees) |
| sl067 | 6 (5/6) | temoin « 3 PV restants » |
| sl068 | 4 (2/4) | temoins de refus / sans Creeping Corruption |
| sl069 | 8 (6/8) | deux temoins sans jeton |
| sl070 | 5 (2/5) | valeurs de desc (menace, Hazard, boost) : rouges sous mutation de donnees ; temoin sans Creeping Corruption |
| sl071 | 6 (6/6) | |

Carte terminee : OUI pour les 17 cartes, **sous les reserves du §4 et du §6** (aucune partie jouee par un humain dans le navigateur ; Creeping Corruption sl072 non codee ici).

## 6. Ce qui n'a pas ete prouve

- **Aucune partie jouee par un humain dans le navigateur.** Outil manquant : un navigateur pilote (le plateau, la fenetre « Interrupt » de Krahllak, le choix « each player chooses »). Les cas du harnais et l'autoplay ne voient pas ce que le joueur lit.
- **Autoplay** (`tools/autoplay.py`, deck `spider_man`, pilote heuristique) : 0 victoire sur 8 standard et sur 16 expert, mais 0 victoire aussi sur 16 parties contre Rhino (temoin) : ce pilote ne gagne pas avec le deck de depart. Un blocage sur 40 parties (expert, graine 7) : Hero Action de `01093 Tenacity` (carte OFFICIELLE du deck, pas une carte du set) reproposee a l'identique. Le mode « expert » d'`autoplay.py` retire le premier vilain de la liste et pose `expert` a faux pour `normal` : l'expert a donc ete joue avec `heart_of_shadow_expert` + difficulte `normal`, ce qui n'active pas `Worlds.IsExpert` (la clause expert de sl061a n'est prouvee que par le harnais, cas `[slc] sl061a (EXPERT)`).
- **Mini-campagne** et **mode campagne** : rien (livret absent).
- **Interaction avec la Creeping Corruption reelle** (retournement a 5 jetons, defaite de l'identite) : cas a ecrire apres la fusion avec la branche de l'agent d.
