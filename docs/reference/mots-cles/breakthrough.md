# Breakthrough

**Texte imprimé / définition** : « This thwart gains breakthrough. »
Mot-clé MAISON, imprimé dans le pack `viv_vision` (Rainy) sur `vv003` Just a
Phase et **sur aucune autre carte du pack** : le zip ne contient aucun insert
de règles.

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026) :

> « Excess threat removed from this side scheme is removed from **the main
> scheme**. »

⚠ **Ce qui a changé le 29/09/2026.** La fiche suivait jusque-là la « Marvel
Champions Home Brew Master List » transmise par l'utilisateur le 02/09/2026
(« another eligible target », au choix du joueur), jamais recoupée depuis le
dépôt. MC4DB, seul glossaire public consulté qui définit le mot, impose la
manigance PRINCIPALE. Le script `vv003` ne propose donc plus de choix : l'excès
part sur `Worlds.GetMainSchemes(effect)[0]`. Si la menée visait la principale
elle-même, l'excès est perdu (rien d'autre n'est nommé). La lecture « l'excès
va toujours sur la principale », écartée le 02/09, est donc celle qui vaut.

Exemple : Viv (THW 1) joue Just a Phase, monte à 4 THW et vise une manigance
annexe qui ne porte que 2 menaces. Les 2 menaces partent, la manigance tombe,
et les **2 restantes** partent sur la manigance principale, même si une autre
annexe est en jeu (cas « avec DEUX annexes », rouge avec l'ancien script).

⚠ MC4DB ne parle que de MENACE : le volet « dégâts » de l'ancienne définition
(« this attack gains breakthrough ») n'a de source que la masterlist. Aucune
carte du dépôt ne l'imprime ; s'il en arrive une, la question se repose.

**Mécanisme moteur — volet ATTAQUE** : c'est `overkill`, tel quel. Le moteur
sait déjà le faire, et sa fiche `overkill.md` donne les deux chemins
(`overkill=True` sur la fabrique d'attaque, ou `message.GainOverKill(effect)`
en cours d'attaque pour les textes « this attack gains… »). Une carte qui
imprimerait « this attack gains breakthrough » n'a donc **rien à coder à la
main** : elle se rend par `GainOverKill`. Aucune carte du dépôt n'est dans ce
cas au 02/09/2026 ; `vv003` n'imprime que le volet menée.

**Mécanisme moteur — volet MENÉE** : rien de natif, contrairement à `overkill`.
Le report se calcule à la main sur le message
`Message.AfterUnitThwartScheme`, envoyé juste après `RemoveThreatInternal`
(`src/game/card/face/attribute/can_thwart.py:148-150`), donc **pendant** que
les bonus de menée de la carte sont encore actifs :

- valeur voulue : `message.would_thw_scheme_message.property.GetThwart(unit)`
  (`ThwartProperty.GetThwart`, `can_thwart.py:4`) ;
- valeur réellement retirée : `message.remove_threat` (plafonnée par la menace
  présente sur la manigance) ;
- excès = voulu − retiré, reporté par
  `RemoveThreatFromSchemes` sur une cible choisie via `ChooseAbilities` +
  `ForChoiceAbility(...).SetTarget(Scheme2, exclude=[...], has_threat=True)`.

L'abonnement se pose en `RegisterTemp` depuis l'Interruption de la carte, sur
le modèle de `20013` Making an Entrance qui pose exactement le même genre
d'effet de suite (`AfterUnitThwartAndRemoveLastThreat` + condition
`message in thw_message.would_thw_messages`).

**Carte exemple** : `vv003` (Just a Phase), pack `viv_vision`.

**Pièges connus** :

- **Seule une vraie MENÉE reporte.** Comme `overkill` ne reporte que des dégâts
  d'attaque, le volet menée de `breakthrough` ne reporte que ce qui a été
  retiré PAR une menée (« removed from this side scheme »). Un « remove N threat » qui n'est pas une menée (le Hero
  Action de `vv005` Solar Beam, par exemple) ne reporte jamais rien, même si la
  manigance tombe.
- **Lire l'excès sur `AfterUnitThwartScheme`, pas sur `AfterUnitThwartEnd`.**
  Le bonus de +3 THW est posé par `GainTHWForThisThwart`, qui passe par
  `GainForThisActive` : à la fin de la menée il peut déjà avoir expiré, et
  `property.GetThwart(unit)` rendrait alors la valeur de base. Le message par
  manigance est envoyé DANS la boucle, avant toute expiration.
- **Menée répartie** (`property.is_divided`) : la valeur par manigance vaut 1,
  et le multiplicateur `schemes_dict[target]` ne se lit pas depuis le message.
  Le cas ne se présente pas sur `vv003` (Interruption sur une menée DE BASE,
  donc une seule manigance), mais toute réutilisation du mot-clé sur une carte
  à cibles multiples devra revoir le calcul.
- **Une manigance vaincue disparaît.** Si la menée abat la manigance visée,
  l'excès existe toujours : ne pas conditionner le report à la survie de la
  cible.
- **Pas de choix à proposer.** La cible du report est la principale, imposée :
  un `ChooseAbilities` (ancien montage) ouvrait une question que le glossaire
  ne pose pas.

**Variantes maison** : aucune autre dans le dépôt pour l'instant. La définition
communautaire prévient elle-même que certains auteurs la retouchent pour un
héros donné : si un pack imprime sa propre formulation, c'est elle qui gagne
sur cette fiche, et la fiche se corrige en conséquence.
