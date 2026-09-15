# La mise en place se tait, et la manigance prend son temps

Conception validée le 15/09/2026, question par question, avant toute ligne de
code. Ce document fait foi : ce qui n'y est pas n'est pas décidé.

## Le problème

Constat de l'utilisateur, 15/09/2026 : « il y a toute la mise en place qui est
visible, avec les cartes qui se placent etc. c'est trop, trop de bruit, trop de
mouvement. Tout doit être en place, sauf la manigance principale, on doit voir
la face A de la première manigance, puis on fait ok, puis elle se place sur la
face B et met directement la menace s'il y en a de base dessus. »

Deux demandes dans une seule phrase, et elles vont ensemble : **vider
l'ouverture de tout mouvement**, et **rendre au retournement de la manigance le
seul moment qui en mérite un**.

La cause du bruit est connue : le moteur n'envoie pas un état final, il envoie
ses trames au fil de la mise en place (`WaitSync`, un accusé de réception par
trame), et le plateau les dessine toutes. On voit donc la table se remplir,
alors que personne ne regarde une vraie table se monter toute seule.

## Ce qui existe déjà, et qu'on ne refait pas

- **La face A est réelle, pas une invention d'affichage.** Chaque étape de
  manigance a ses deux faces dans les données : `01097a` (titre, étape, aucun
  seuil) et `01097b` (`StartingThreat`, `TargetThreat`, `EscalationThreat`).
  Le moteur met la face A en jeu, puis la retourne.
- **Un seul point de retournement pour tous les cas.**
  `World.AdvanceMainScheme` (`src/game/world/world.py:896`) : sa première
  branche ne traite que « la manigance est sur sa face imprimée n°1, on la
  retourne ». La mise en place y passe (étape 12 de `Initialize`), et une
  étape suivante y repasse par `MainScheme.OnAfterCardRevealedEnd`, qui appelle
  `Advance` dès qu'une face A sans seuil imprimé est révélée.
- **La question à une seule option.** `PlayerAsk.AskChooseOneText`
  (`src/game/player/model/player_ask.py:56`) construit une capacité de choix que
  le plateau sait déjà afficher et router.
- **Le plateau ne valide pas tout seul.** `interaction.ts` n'auto-valide une
  option unique que sous prédicat explicite (`optionDemarreAuto`, qui sert au
  mulligan). Notre question ne le portera pas.
- **Les drapeaux de règle.** `world_rule.py` tient déjà
  `disable_resolve_mulligans` et `disable_setup_draw_cards`, chacun un
  `VariableBool` nommé, activable par la liste de règles de la partie.
- **Les briques d'animation.** `CoucheAnimations.tsx` (deux couches : la
  translation d'un côté, le geste de l'autre) et `CoucheRevelation.tsx` (la
  présentation en grand au centre).

## Décisions

### Le déroulé d'une partie neuve

1. Le voile de chargement tient tant que la question de la manigance n'est pas
   arrivée. **On ne voit jamais la table se remplir.**
2. La table apparaît d'un bloc, complète et figée, avec **la manigance 1A en
   grand au centre** et un bouton OK.
3. Au clic : la carte **se retourne sur sa face B**, sa **menace de départ est
   déjà à sa valeur** sur le compteur, et elle **rejoint sa place** sur la
   table.
4. La main apparaît, l'écran de mulligan s'ouvre, et plus rien ne bouge.

### La main est vide au moment de la face A, et c'est assumé

Le moteur retourne la manigance à l'étape 12 de `Initialize` et ne distribue les
mains qu'à l'étape 14. Au moment du panneau, la main est donc vide.

⚠ **On ne déplace pas le retournement après la pioche.** Les effets « Une fois
révélée » de la manigance doivent se résoudre avant que les joueurs piochent
(Klaw met un sbire en jeu de cette façon). Déplacer le retournement changerait
le jeu, ce que ce projet refuse.

Choix retenu parmi trois : **main vide assumée**. Pas de zone masquée, pas de
pioche animée après le OK.

### Rien d'autre ne bouge

Choix retenu : **rien du tout**. Aucune carte ne vole, aucune présentation au
centre, aucun cartouche, aucun son pendant la mise en place. Le retournement de
la manigance est le seul mouvement de toute l'ouverture.

Les deux autres pistes ont été écartées explicitement : laisser entrer en
mouvement ce que la manigance déclenche, et distribuer la main après le OK.

### La menace de départ

Choix retenu : **le compteur porte sa valeur dès le retournement**. Pas de jeton
volant, pas de compteur qui monte. C'est le sens de « met directement la
menace ».

### Le OK arrête vraiment la partie

Choix retenu, en connaissance du coût : **le moteur attend**. Ce n'est pas un
récit d'affichage comme `JetonMenaceVolant`, c'est une vraie question posée
pendant la mise en place, au même titre que le mulligan.

### Qui répond

Choix retenu : **le premier joueur seul**. C'est lui qui tient le jeton et qui,
sur une vraie table, retourne la carte. Les autres voient la face A puis la
voient se retourner, sans avoir à cliquer.

### Où le moment se rejoue

Choix retenu : **à l'ouverture, et à chaque nouvelle étape de manigance**. Quand
1B est complétée, on voit 2A en grand, OK, elle se retourne sur 2B et sa menace
de départ se pose.

Une reprise de sauvegarde ne rejoue pas le moment : la partie reprend sur sa
table en place.

## Le montage

### Moteur

Une question posée dans `World.AdvanceMainScheme`, **juste avant le
`card.Flip(...)` de la première branche**. Ce seul crochet sert la mise en place
et les changements d'étape, puisque les deux y passent.

⚠ **À vérifier par une trace avant d'écrire la question, pas à supposer** : la
mise en place appelle `scheme.Advance(None, game_start_effect)` explicitement à
l'étape 12, avec le commentaire « Has already reveal here ». Il faut voir, sur
une vraie partie, par quel chemin la face A de l'étape 1 est retournée, et
confirmer que la branche visée est bien celle qui s'exécute. Si ce n'est pas le
cas, le crochet se pose dans `MainScheme.OnAfterCardRevealedEnd`, l'autre porte
du même retournement.

### Le drapeau, et pourquoi il n'est pas optionnel

Les rejeux sont une liste d'opérations relues dans l'ordre avec contrôle CRC
(`engine/controller/module/replay.py`). **Une question de plus pendant la mise
en place décale cette liste.** Sans précaution, toutes les sauvegardes en cours,
toutes les campagnes et tous les cas `su0` enregistrés avant le changement
partiraient en désynchronisation.

D'où un `VariableBool` dans `world_rule.py`, à côté de
`disable_resolve_mulligans`, **par défaut à faux** :

- une partie neuve lancée depuis le plateau porte la règle, donc pose la
  question ;
- une sauvegarde ancienne ne la porte pas, donc se rejoue à l'identique ;
- les puzzles et les cas de test ne la portent pas non plus.

### Plateau

Trois morceaux, tous dans `ui-app/src/board/` :

- **le voile tenu** jusqu'à l'arrivée de la question, pour que la table
  n'apparaisse jamais en train de se remplir ;
- **un panneau** qui reconnaît cette question et affiche la carte en grand au
  centre avec son OK, au lieu du bouton de choix ordinaire. Le routage passe par
  `ou-va-la-question.ts` ;
- **le retournement et le vol** vers sa place, sur la mécanique à deux couches
  de `CoucheAnimations`.

⚠ Aucun texte en dur. Tout passe par `langue.ts` et `dico-en.ts` : la gate de
langue posée le 15/09/2026 refuse le reste.

## Les cas limites, tranchés

- **Deux manigances principales en jeu en même temps** (`21098a`) : un panneau
  par manigance, l'un après l'autre.
- **Une face A qui porte un seuil de menace imprimé** ne se retourne pas dans le
  jeu réel (`OnAfterCardRevealedEnd` ne l'avance pas) : aucun panneau, aucune
  question.
- **Partie sans manigance principale** (cas de test, puzzle) : rien ne change,
  le drapeau n'est pas posé.
- **Reprise de sauvegarde en cours de partie** : pas de panneau.

## Comment on le prouvera

- **Moteur** : un cas rouge d'abord, qui montre que la partie s'arrête sur la
  face A et n'avance qu'après la réponse. Et un cas qui prouve le REFUS du
  changement d'état tant que la réponse n'est pas donnée, pas seulement le
  passage après.
- **Rejeux** : un cas qui rejoue une sauvegarde antérieure au changement et la
  voit arriver au même CRC. C'est la garde qui protège les campagnes en cours.
- **Plateau** : l'étape 8 bis de `PROCESSUS-CARTE.md`. Un cas sur
  `plateau-de-test.ts` qui prouve que c'est bien la face A qui est DESSINÉE au
  moment du panneau, pas seulement celle que le moteur tient.
- **Silence de l'ouverture** : un cas qui prouve qu'aucun vol n'est émis entre
  l'entrée sur le plateau et la réponse au panneau.
- **Pilote d'autoplay et specs `ui-check`** : ils jouent de vraies parties et
  rencontreront la question. Ils doivent y répondre, et c'est la preuve que le
  moment existe.

## Ce qui n'est pas dans cette spec

- Les cinq autres causes de mollesse des animations
  (`.planning/todos/2026-09-14-animations-molles.md`) : la durée et le geste
  sont déjà faits et sous drapeau d'essai, le reste n'est pas engagé ici.
- Les sons de l'ouverture : sujet à cadrer séparément
  (`.planning/todos/2026-09-14-revoir-les-sons.md`).
- Le mode manuel, les couleurs du halo.

---

## Avenant du 15/09/2026 : les manigances ANNEXES aussi

**Demande de l'utilisateur, en cours de chantier** : « s'il y a une sidescheme
qui commence en partie je veux qu'on la voit aussi comme la principale, idem
quand une sidescheme arrive en jeu après, par exemple que le méchant change de
forme ».

### Ce que ça ajoute

Le même panneau de présentation, pour une manigance annexe :

1. **à la mise en place**, quand le scénario en pose une d'entrée ;
2. **en cours de partie**, quand une manigance annexe ENTRE EN JEU, quelle
   qu'en soit la cause (changement de stade du vilain, carte rencontre, effet).

### Ce qui est différent de la principale, et qu'il faut trancher

⚠ **Une manigance annexe n'a pas de face A.** La principale a deux faces
imprimées (`01097a` / `01097b`) et le moteur RETOURNE la carte, ce qui donne le
moment naturel « on lit, on valide, elle se retourne ». Une annexe entre en jeu
directement, d'une seule face. Le panneau ne peut donc pas être « avant le
retournement » : ce sera « au moment de l'entrée en jeu ».

⚠ **Elles peuvent arriver par paquets** (un « Une fois révélée » qui en pose
deux, un changement de stade qui en pose plusieurs). Un panneau par carte, à la
suite, ou un seul panneau qui les montre ensemble : à décider.

⚠ **Le crochet moteur n'est pas le même.** `AdvanceMainScheme` ne sert que la
principale. Pour une annexe il faut se brancher sur son entrée en jeu
(`OnPutIntoPlay` / `OnWhenCardRevealed` du type `EncounterSideScheme`, à
vérifier par une trace comme pour la principale).

⚠ **Le risque de lassitude est réel** : une annexe par tour dans certains
scénarios. Le panneau doit-il attendre un OK à chaque fois, ou seulement se
montrer ?

### Les décisions, prises le 15/09/2026

| Question | Décision |
|---|---|
| **Le jeu s'arrête-t-il ?** | **Oui, un OK**, exactement comme la principale. Le moteur attend. |
| **Plusieurs d'un coup ?** | **Une à la fois, un OK chacune.** On lit chaque carte pour elle-même, même si un effet en pose deux ou trois. |
| **Celles que le joueur pose lui-même ?** | **Aucun panneau.** Il vient de la lire et de la choisir : le panneau ne lui apprendrait rien et lui coûterait un clic. Le panneau est réservé à ce que le SCÉNARIO impose. |
| **Qui valide en multijoueur ?** | **Le premier joueur**, comme la principale. Une seule règle pour les deux panneaux. |

### Ce qui reste à établir par une trace, pas à supposer

⚠ **Par où passe l'entrée en jeu d'une manigance annexe ?** La principale avait
UNE porte (`AdvanceMainScheme`), trouvée par trace. Il faut la même mesure ici :
`OnPutIntoPlay`, `OnWhenCardRevealed`, ou les deux selon l'origine (mise en
place, changement de stade du vilain, carte rencontre, effet d'une carte).

⚠ **Comment distinguer ce que le scénario impose de ce que le joueur pose ?**
C'est la décision n°3, et elle n'a de sens que si le moteur sait le dire. À
vérifier : une `PlayerSideScheme` jouée depuis la main passe-t-elle par un
chemin distinct d'une `EncounterSideScheme` mise en jeu par le scénario ?

⚠ **Le doublon avec `CoucheRevelation`.** Une manigance annexe RÉVÉLÉE est déjà
montrée en grand au centre aujourd'hui, avec disparition automatique. Si le
panneau s'ajoute sans que la présentation existante se taise, on aura deux
présentations de la même carte, l'une par-dessus l'autre. C'était le défaut n°2
du 14/09/2026, il ne faut pas le refaire.

### Ce que la trace a répondu, le 15/09/2026

**La porte est unique, et c'est `SchemeSide2.OnPutIntoPlay`** : les deux types
de manigance annexe en héritent. Chemin complet relevé sur une vraie partie de
Klaw, dont la mise en place pose « Defense Network » (`01125`) :

```
01116a.py (face A de la manigance principale)
  -> SetupCards.Reveal   -> face.Reveal   -> OnWhenCardRevealed
  -> PutIntoPlay         -> SchemeSide2.OnPutIntoPlay
```

**Distinguer le scénario du joueur** : la classe concrète suffit.
`EncounterSideScheme` est ce que le scénario impose, `PlayerSideScheme` est ce
que le joueur joue depuis sa main. Le moteur ne pose la question que pour la
première.

⚠ **Le doublon avec `CoucheRevelation` était RÉEL** : la carte passe par
`Reveal`, donc la couche des révélations la montrait aussi en grand, par-dessus
le panneau. La couche se tait désormais tant que le panneau tient la question.

### Statut

**Fait le 15/09/2026.** Drapeau `confirm_side_scheme` (séparé de celui de la
principale, pour qu'une sauvegarde écrite entre les deux se rejoue sans lui),
crochet dans la porte unique, panneau partagé SANS retournement (une annexe n'a
qu'une face), et sept cas verts au harnais moteur.
