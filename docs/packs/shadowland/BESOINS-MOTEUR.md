# Shadowland : ce que le moteur devra savoir faire

Etabli le 22/10/2026 a partir des textes transcrits (`cartes.md`), des decisions de `QUESTIONS.md` et de l'etape 2 du processus carte (`references/ref_part1-3.md` : **264 capacites examinees, 231 avec une carte de reference (scripts ouverts et verifies), 33 sans reference**). **Rien n'est code** : l'utilisateur ne veut pas qu'on touche au moteur pour l'instant. Les fichiers `references/` donnent, pour chaque capacite, la carte comparable, le fichier verifie et le piege connu.

## 1. Donnees et typage (petits ajouts, a faire en premier)

| Besoin | Cartes | Detail |
|---|---|---|
| **Compteur `corruption`** | tout le set Black Flower / Heart of Shadow | a ajouter au `Literal` `CardFace.COUNTER` (`card_face.py:277`) |
| **Compteur `passage`** | sl037, sl038b, sl042 | idem |
| **Traits `OVERPOWERING`, `POSSESSED`** | sl072b, sl061a, sl077, sl078 ; sl013, sl014... | a ajouter au `Literal` `CardFace.TRAITS` (typage seul) |
| **Orthographe du trait des pieges** | sl040, sl046-sl056 | **CORRECTION (22/10)** : l'enumeration du moteur contient `"TRAP!"` (avec « ! », utilise par les cartes Jubilee), pas `TRAP` ; Hunting Season ecrit `TRAP` sans « ! ». Le scan imprime « TRAP! » : utiliser `TRAP!` et verifier que le `TrapDeck` de Hunting Season ne s'en trouve pas casse |
| **PV infinis, menace cible infinie (∞)** | sl037, sl038b | decision Q1 ; valeur « infinie » dans `desc` + rendu « ∞ » |
| **★ apres une valeur** (ATQ, SCH, escalade) | sl012-sl017, sl031, sl034, sl037, sl057-sl059, sl061b... | decisions Q2/Q3 ; rendu a creer, la valeur reste celle du `desc` |

## 2. Mecaniques sans reference (33 capacites)

**Shadows in the Night (24 + 1)**
1. **Positions** (sl003 villain, sl004 hero) : deux Environnements recto-verso, memes noms de faces (« The Streets Below » / « Atop the Tenshu »), a discriminer par `card_id` ; predicats « position du vilain = Atop ? » et « positions identiques ? » ; retournement par « Change the villain's position » (9 cartes) avec drapeau « deja change cette phase » reinitialise a chaque phase.
2. **Effets continus qui dependent de deux cartes** (+1 ATQ a chaque personnage, -1 aux degats, menace non retirable, icones Acceleration/Hazard de sl008), recalcules au retournement (`Message.AfterCardFlip` existe, aucune carte lue ne s'en sert pour cela).
3. **Linked a trois noms** (« Linked (A, B, or C) », sl018-sl027, 10 cartes) : `desc.Linked` n'accepte qu'un nom ; il faut lier chaque carte a 3 vilains et ne melanger dans le deck de rencontre que celles du vilain TIRE.
4. **Complot a deux etapes, vilain retourne au lieu d'etre vaincu** (face A -> B, PV remis, position changee, 1 carte rencontre face cachee par joueur ; vaincu face B = victoire).
5. Voir aussi les modeles partiels : tirage au hasard parmi 6 vilains (21165a, 27101a), melange des cartes liees (60121a) ; **le vilain tire doit etre memorise jusqu'a l'etape 2A** (rien de lu ne garde un tirage d'un stade a l'autre).

**Shadow Labyrinth (8)**
6. **Hook « quand vous choisissez l'effet nomme Avoid / Disarm / Trip »** (sl046, sl047, sl048, sl049) : le moteur n'envoie rien apres le choix d'une branche nommee ; le plus proche est `Message.WhenPlayerChooseAbility` (envoye AVANT). Et **interdire une branche nommee** (sl047 Iron Monk).
7. **Deck Piege** : le moteur a deja un `TrapDeck` avec defausse liee (Hunting Season, `hunting_season/trap/__init__.py`), mais il distribue les pieges aux joueurs et ne lit que les cartes TRAP ; ici on le cree au Setup (sl038a), on y melange des cartes du deck de rencontre qui ne sont PAS des pieges (sl041, sl045), on revele la carte du dessus, on remelange la defausse.
8. **Vider un vilain, le mettre de cote et reveler la face A ou B selon le mode expert** (sl039a, etape 2).
9. **Vilain traite comme sbire ELITE a 6 PV** (sl040) : `TreatAttachedCardAsMinion` n'accepte que Hero et Ally.
10. PV infinis et menace cible infinie (voir §1).

**Heart of Shadow / Black Flower (1)**
11. **Defaite d'un joueur par texte de carte** (sl072b, « you are defeated » a 5 jetons) : aucune reference ; choisir entre `Faces.DefeatUnits` sur l'identite et `Player.Eliminate` direct.

## 3. Assemblages a prouver au harnais (reference partielle ou ordre des fenetres)

- **La Creeping Corruption DU joueur X** : chaque joueur a la sienne ; il faut un assistant partage et un cas a **deux heros** pour toute capacite qui pose, retire ou lit un jeton.
- **Seuil de 5 jetons atteint par pose de 2 d'un coup** (sl060b, sl067, sl074, sl076 vers sl072a) : le retournement retire TOUS les jetons (comme 55007a), cas 4 -> 6.
- **Ordre des fenetres** quand un cout pose le 5e jeton (sl063, sl066, sl070, sl072a/b) : retournement ou defaite AVANT l'effet imprime ; a prouver, pas a supposer.
- **Interruption facultative d'un ennemi qui attaque « vous »**, effet conditionnel au paiement (sl057-sl059, sl068 : -3 ATQ ; sl073 : annuler) ; cout « poser N jetons sur une AUTRE carte » (sl063, sl066, sl070) ; interruption « vous ou un allie » (sl062).
- **Limite « une fois par round et par joueur »** sur declencheurs d'attaque non-joueur (Daredevil, White Tiger, sl039b) : `LimitOncePerRoundPerPlayer` plante sur un message sans joueur cible ; helper maison de hs104 / hs108b a reutiliser.
- **Boost « un allie defend contre cette attaque »** (sl028, sl029) ; attaque supplementaire d'un vilain avec +1 ATQ et limite consommee avant la 2e attaque (White Tiger) ; tri de cible par « cout imprime le plus haut » (Lady Bullseye) ; reduction de degats + contre-attaque + auto-defausse dans une meme interruption (Krahllak's Blessing) ; « if no ... this way » avec decompte reel (sl020, sl027) ; defausse « sbire OU manigance annexe » (sl043) non prouvee.
- **Choix des cartes rencontre** : une option payee en ressources mais impayable en entier reste choisissable et est reduite au plus gros morceau payable (`player_action.py:855`) ; les options a cout de defausse disparaissent si impayables.

## 4. Mots-cles

Fiches `docs/reference/mots-cles/` : **toutes presentes** (Steady, Toughness, Guard, Villainous, Surge, Peril, Patrol, Retaliate, Stalwart, Quickstrike, Assault, Linked, Overkill, Piercing, Ranged, Setup, Permanent...). Relire `linked.md` pour la forme a plusieurs noms.

## 5. Limites de cette etape 2

Deux scripts de reference (21099b pour sl001b/sl002b, 36037 pour sl006) ont ete cites depuis un resultat de recherche sans etre ouverts en entier ; la reference de Assault est la fiche `mots-cles/assault.md`, pas un script. Aucune de ces references n'a ete executee : elles disent ce qui EXISTE, pas que ca marche.
