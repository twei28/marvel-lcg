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
