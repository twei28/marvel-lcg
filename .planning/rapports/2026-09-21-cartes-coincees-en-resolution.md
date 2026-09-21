# Cartes coincées en zone de résolution : une recherche qui ne se referme pas

Signalement d'Aghenatak, le 20/09/2026, deux messages à une minute
d'intervalle. Branche `mode-manuel`.

> « Squirrel Girl a été jouée comme un support. Impossible de l'activer
> d'aucune manière, ni de la défausser. »
>
> « Piecing all together a été joué comme un support. Impossible de le
> contrer. »

Deux symptômes, un seul défaut, établi avant cette session : les deux rapports
viennent de la même partie (Jessica Jones contre *Dark Beast's Bogus Journey*,
round 13) et portent le même état de table, où `61007` Piecing It All Together
et `61017` Squirrel Girl sont toutes deux « en résolution », c'est-à-dire dans
la **zone de traitement** (`area_processing`).

## Ce que la reproduction montre

Montée avec `tools/test_capacites.py`, héros `jessica_jones` (le pack officiel
`jj`, 61xxx), scénario `rhino`, graine 42.

**Ce n'est pas la mise en jeu qui échoue. C'est la RECHERCHE qui ne se referme
jamais.**

Une recherche (`Search.SearchForCards`, `src/game/operate/search.py`) ne se
contente pas de lire le deck. Elle **sort la carte trouvée du deck et la pose
dans la zone de traitement**, pour la montrer au joueur : c'est
`SelectorEnd.DoMove` (`src/game/selector/selector_end.py:47`) qui appelle
`Faces.MoveAllToProcessingArea`. Le deck est remélangé dans la foulée. À partir
de là, c'est à l'opération appelante de faire quelque chose de la carte :
l'ajouter à la main, la jouer, la défausser.

Quand elle ne le fait pas, **rien** ne ramène la carte.

Les deux cartes du signalement sont exactement les deux proies de ce trou dans
le paquet Jessica Jones :

| carte du deck | ce qui la sort du deck | texte |
| --- | --- | --- |
| `61017` Squirrel Girl (Ally) | `61008` Calling in Favors | « search your deck for an ally and **play it** as if it were in your hand » |
| `61007` Piecing It All Together (PlayerSideScheme) | `61019` Strategy Session | « search their deck for a player side scheme and **add it to their hand** » |

Les deux scripts font la même chose : la recherche sort la carte, puis un
`ForChoiceAbility(...).SetTarget(faces, range=(0, 1))` demande au joueur s'il
veut vraiment la jouer / la prendre. **`range=(0, 1)` : il a le droit de
refuser.** S'il refuse (ou, en jeu réel, s'il ferme la fenêtre, ou si la modale
de paiement ne lui convient pas), l'opération ne fait rien, et la carte reste
dans le sas.

Trace du pilote, moteur d'origine, sur Calling in Favors :

```
> 55: Jessica Jones's PlayerDeck<33> (All) : [(0,61003) Luke Cage], ...
ASK 3  | "Alter-Ego_Action" | all_legal_targets: [9, 26, 40, 24, 25] | [1,1] | is_search: true
> 56: [[(09,61003) Luke Cage]] placée(s) sur la table
> 57: Jessica Jones's PlayerDeck<32> va être mélangé
ASK 4  | "Choose_an_ally_to_play,_reducing_its_cost_by_2" | [9] | target_num_range: [0, 1]
RESULTAT: 61003 -> Jessica Jones's ProcessingArea<1>
```

Et sur Strategy Session, même figure, avec `61020` Run Them to Ground à la
place (c'est la manigance que la graine 42 place en tête) :
`61020 -> Jessica Jones's ProcessingArea<1>`.

Une carte qui reste là n'est **ni en jeu, ni en défausse, ni dans le deck**.
Aucune action ne la touche, aucune capacité ne part, et le plateau la dessine
posée sur la table : le joueur la lit comme un soutien. La description
d'Aghenatak est exacte, mot pour mot.

Les faits négatifs du signalement se recollent d'eux-mêmes :

- **aucune exception serveur**, parce qu'il n'y a pas de plantage : la séquence
  se termine normalement, elle oublie simplement de refermer le sas ;
- **le journal ne remonte pas au round d'entrée**, parce que l'entrée en sas ne
  produit qu'une ligne « placée sur la table », plusieurs rounds plus tôt ;
- **`R6 {c41} Squirrel Girl défaussé / P1` sans effet** : la défausse ne peut
  pas mordre sur une carte qui n'est dans aucune zone défaussable.

## Générique, ou propre à ces deux cartes ? GÉNÉRIQUE

Trois arguments, dont le troisième est mesuré.

1. **Le mécanisme est moteur, pas carte.** `SelectorEnd.DoMove` sort la carte
   du deck pour *toute* recherche, sans se soucier de qui la consommera, et
   personne, nulle part, ne referme ce transit. Le contrat « la zone de
   traitement est un sas » n'était écrit nulle part et gardé par rien.

2. **Il y a déjà des filets ailleurs, et ils prouvent que le trou était connu
   sans être bouché.** `PlayCardsLikeInTurn` et `PlayOneCardLikeInTurn`
   (`player_action.py:897` et `:1007`) font tous deux, chacun de leur côté,
   `if face.IsInProcessingArea(): Faces.DiscardAll(...)`. Deux rustines locales
   pour le chemin « jouer », rien pour le chemin « chercher ».

3. **Une troisième carte, dans un pack sans aucun rapport, tombe dans le même
   trou.** `62022` Dynamic Duo (pack `luke_cage`) fait une recherche **sans
   filtre** (`Search.SearchForCards(effect, player, include_player_deck=True,
   include_player_discard_pile=True)`), puis ne garde que les cartes dont le
   texte porte `Team-Up (`. Toute carte tirée qui n'est pas une Team-Up reste
   dans le sas. Témoin rouge constaté : `carte(s) restée(s) en zone de
   traitement : ['62017']`.

   Trois cartes, deux packs, deux familles de textes différentes. Et
   **223 fichiers de cartes appellent `Search.*`** (dont 54 `SearchForCards`) :
   chacun qui ne consomme sa trouvaille que sur une branche est exposé. Tout
   `Search.*` passe par un unique goulot, `SearchForCardsInternal`, appelé
   d'un seul endroit (`search.py:358`) : c'est ce qui rend le filet possible
   en un point.

⚠ **MAIS LE FILET, LUI, N'EST PAS AUSSI GÉNÉRIQUE QUE LE TROU, ET IL FAUT LE
DIRE.** `SelectorEnd` sert **tous** les sélecteurs, pas seulement les
recherches, et `not_move` vaut `False` par défaut : n'importe quel sélecteur
qui vise une carte face cachée dans un deck la déplace vers le sas. Seul le
chemin `Search.*` est couvert ici, parce que c'est le seul qui passe par
`SearchForCardsInternal` et donc le seul où l'on connaisse l'effet propriétaire.
L'exposition réelle paraît quasi nulle (les `from_where` qui visent un deck
sont presque tous des `...DeckTop`, qui forcent `not_move=True`), mais elle
n'est pas nulle par construction : c'est une zone non gardée, pas une zone
prouvée vide.

## Le correctif : le sas de recherche se referme tout seul

Même motif que le correctif de paiement du 20/09 (`ab0b6e7e`, signalement
Yarro n°18) **un cran plus loin**, et volontairement sur le même principe :
une opération qui n'aboutit pas remet les choses où elles étaient. Les deux
mécanismes ne se recouvrent pas et n'ont pas été dupliqués :

| correctif | ce qui est défait | où |
| --- | --- | --- |
| 20/09 (Yarro) | un **paiement** incomplet : ressources dépensées, coûts payés, carte jouée | `SpendResource` / `CostFunc.RollbackCost` |
| 21/09 (ici) | une **recherche** non consommée : la carte sortie du deck | `EffectInvoker.CloseSearchTransit` |

Trois fichiers moteur :

| fichier | rôle |
| --- | --- |
| `src/game/operate/search_internal.py` | relève la zone de chaque candidate **avant** la sélection, puis note sur `by_effect` les cartes qui se retrouvent dans le sas, avec leur deck d'origine |
| `src/game/effect/effect_context.py` | `search_transit` : la liste de ces paires, portée par l'effet de la carte qui cherche |
| `src/game/effect/effect_invoke.py` | `CloseSearchTransit` : à la fin de la résolution, toute carte du sas que personne n'a réclamée rentre dans son deck, puis le deck est remélangé |

(`src/game/selector/selector_end.py` ne porte qu'un commentaire : c'est là que
la carte sort du deck, mais ce n'est pas là qu'on peut le noter, voir plus
bas.)

### Le piège qui a coûté une passe : SUR QUEL EFFET poser le sas

Première version : le sas était noté dans `SelectorEnd.DoMove`, juste après le
`MoveAllToProcessingArea`. C'était le geste évident, et il est faux.

`SelectorEnd` n'est pas appelé avec l'effet de la carte qui cherche. Il est
appelé avec **un effet jetable**, que `Player.AskChooseSelect`
(`player_ask.py:222`) fabrique à la volée (`ForChoiceAbility`) rien que pour
poser la question au joueur. Cet effet-là se termine **dès que le joueur a
répondu**, c'est-à-dire bien avant que l'opération appelante ait pu consommer
la carte. Le sas se refermait donc immédiatement et reprenait la carte.

Le symptôme n'apparaît que sur une carte qui enchaîne **deux recherches** :
`ze014` The Mother of Night (pack `zeus`, « each player search their deck and
discard pile for **2 cards** with printed [energy] icons ») les appelle deux
fois de suite et ne pose les cartes qu'après. La première carte rentrait au
deck entre les deux, la seconde recherche retombait dessus, et une seule carte
finissait posée : `1 carte(s) posée(s) sous ze014 (attendu 2)`.

C'est la session voisine qui a vu le rouge en premier, dans sa propre passe, et
qui a proposé la cause. **Je ne l'ai pas prise pour acquise, je l'ai mesurée**,
sur un moteur de référence monté exprès (`.game-src-ref`, dont le seul
`src/game` est une copie où mes quatre fichiers sont remis à leur version
`HEAD`, tout le reste de l'arbre de travail étant conservé) :

| moteur | `ze014` ×2 |
| --- | --- |
| sans mon correctif (mes 4 fichiers à `HEAD`) | **vert** |
| avec la 1re version du sas (noté dans `SelectorEnd`) | **rouge** : `1 carte(s) posée(s) sous ze014 (attendu 2)` |
| avec la version corrigée (noté dans `SearchForCardsInternal`) | **vert** |

C'était donc bien ma régression, et non un rouge antérieur. La trace
intermédiaire (une sonde temporaire dans `CloseSearchTransit`, retirée depuis)
montrait le sas se refermer sur un effet
`(ChooseAbility) WhenPlayerChooseAbility` entre les deux recherches, ce qui
nomme la cause sans ambiguïté.

Les deux cas `ze014` sont donc devenus, et restent, le **garde-fou du double
appel** ; leur `pourquoi` le dit désormais.

Correction : la paire `(carte, deck d'origine)` est notée dans
`SearchInternal.SearchForCardsInternal`, sur le `by_effect` que la carte a
passé à `Search.*`. C'est le seul endroit qui connaisse à la fois le vrai
propriétaire de la recherche et la zone d'origine des candidates.

Trois points de conception valent d'être dits :

- **La fermeture est HORS du `if can_action`.** Une recherche peut avoir lieu
  pendant le choix des cibles, donc avant que le coût soit payé : un effet
  abandonné faute de paiement doit rendre lui aussi ce qu'il a sorti du deck.
- **On remélange, et ça fait plus que respecter le « (Shuffle.) » imprimé.**
  La carte repart à sa place et sa position n'est pas connue, c'est l'évident.
  Le moins évident, relevé à la relecture : `Deck.Shuffle` appelle
  `CleanAllCardsStatuesInternal`, qui vide `visible_players`. Or cette
  visibilité est **collante** : la recherche l'a posée (`LookAt_Text`) et rien
  d'autre ne l'efface. Sans le remélange, la carte rendue **resterait visible
  au joueur à l'intérieur de son propre deck** pour le reste de la partie.
  Le remélange ferme donc aussi une fuite d'information ; le passage par
  `Faces.ShuffleAllTo`, la recette du dépôt, l'annonce en plus au journal.
  Il n'a lieu que s'il y a eu un retour : le chemin normal, où la carte est
  consommée, ne déclenche aucun mélange supplémentaire et ne déplace donc
  aucun tirage.
- **La zone de RÉVÉLATION est explicitement exclue.** `RevealingArea` porte
  elle aussi `is_processing` (`deck/deck_type.py`) : une carte que l'appelant a
  envoyée à la révélation **a bien été réclamée**, et sans cette garde toute
  recherche suivie d'un `Reveal` aurait vu sa carte arrachée en pleine
  résolution. **Elle est défensive, et mesurée comme telle** : le témoin
  `01095` reste vert avec la garde neutralisée, parce que sur le seul chemin
  connu la révélation se termine à l'intérieur de l'opération et que la carte
  est déjà en jeu quand le sas se referme. Elle est gardée parce qu'elle ne
  coûte rien et qu'elle protège la seule façon dont ce correctif pourrait
  mordre trop fort.
- **La fermeture est dans un `finally`.** `ResolveSelfInternal` a un retour
  anticipé, quand `WhenEffectWouldResolve` est remplacé
  (`resolve_message.is_be_instead`) : une recherche menée pendant le paiement
  ou le choix des cibles, suivie d'un effet remplacé, sortait sans refermer le
  sas. C'est exactement le défaut d'origine, sur une branche que le correctif
  prétend couvrir. Le `finally` couvre aussi l'exception : une carte sortie du
  deck n'a pas à payer le plantage d'un script.
- **Le retour est journalisé** (`Log.Debug`, « recherche non consommée : X
  rendue à Y ») : on ne fait pas disparaître le symptôme en silence.

## Deux mécanismes de retour en arrière : faut-il les mettre en commun ?

Question posée par le coordinateur pendant le travail, réponse donnée pendant
que le sujet est frais.

**Ma réponse : séparés aujourd'hui, unifiables plus tard, et pas ici.** Ils
partagent une *intention* (« ce qui n'aboutit pas remet les choses où elles
étaient ») mais pas une *mécanique*.

| | paiement (`ab0b6e7e`, `d4d1fc43`) | recherche (ici) |
| --- | --- | --- |
| ce qui est défait | plusieurs cartes ET des coûts hétérogènes (inclinaison, jetons, compteurs) | une carte, et rien d'autre |
| quand on sait qu'il faut défaire | à un **point de non-retour identifiable** : juste avant `AfterCardsBeSpendAsResource` | jamais explicitement ; **c'est l'absence d'action** qui est le signal |
| comment on referme | par un appel, au moment de l'abandon | par un **balayage** en fin de résolution |
| ce qui bloque la fusion | `RollbackCost` doit interroger chaque `CostFunc`, et le rapport du 20/09 liste tout ce qui ne sait pas se défaire | il n'y a aucun coût à défaire : rendre la carte suffit toujours |

Le seul morceau vraiment commun est le relevé « d'où vient cette carte », et il
tient en une ligne des deux côtés (un dictionnaire de zones pris avant le
geste ; la session voisine l'appelle `zones_avant`, moi aussi, par hasard, ce
qui dit bien que c'est le geste naturel et pas une abstraction à extraire).
Factoriser ça produirait un module de trois lignes et deux appelants, au prix
d'un couplage entre le paiement et la recherche qui n'existe pas aujourd'hui.

**DETTE À INSCRIRE, À NE PAS ENTREPRENDRE MAINTENANT.** Le relecteur de l'autre
chantier a tranché dans ce sens et sa conclusion est reprise ici telle quelle :
la bonne base serait **la forme adoptée ici**, un registre porté par
`effect.context`, fermé par l'invocateur, avec le test « la carte a-t-elle été
réclamée depuis ». Leur `zones_avant` est un dictionnaire local à une fonction
et devrait devenir une **politique de fermeture** de ce registre, pas un second
registre. L'unification attend que ce chantier-ci ait atterri ; elle n'est pas
faite ici.

En revanche **le vocabulaire, lui, doit converger**, et c'est le vrai risque à
six mois : deux mots pour la même idée dans un moteur que personne ne relit en
entier. Les deux correctifs parlent déjà de « rendre la carte d'où elle vient »
et relèvent tous les deux un `zones_avant`. Ce qui manque est une entrée unique
dans `RECETTES-MOTEUR.md` qui dise « toute zone de transit doit se refermer,
voici les deux qui existent et où elles se referment ». C'est ce que vaudrait
un chantier à froid : une page de doc et, éventuellement, une gate de test
générique (« aucune carte ne reste en zone de traitement à la fin d'un cas »,
qui est exactement la clé `aucune_en_resolution` posée ici, généralisée à toute
la batterie). Pas une fusion de code.

## Les témoins

Harnais choisi : **`tools/test_capacites.py`**. C'est le seul qui monte une
position réelle, fait jouer des cartes et déclenche des actions
(`Puzzle.Action`, clés `jouer` / `main_exclusive` / `accepter_choix`) ;
`test_cards.py` ne fait que construire les capacités et n'aurait rien vu, et le
paquet `jj` n'avait jusqu'ici aucun fichier de test dédié dans `tools/`. Les
cas de cartes vivent tous là, le moule était donc déjà écrit.

Clé de vérification **ajoutée** : `aucune_en_resolution`. Aucune clé existante
ne savait voir le défaut : `hors_jeu` est *vrai* pour une carte coincée, et
`dans_deck_joueur` ne regarde que le deck. Elle balaie
`world.area_processing` **et** le `area_processing` de chaque joueur.

| témoin | avant correctif | après |
| --- | --- | --- |
| `61008` Calling in Favors, recherche **refusée** | ROUGE : `carte(s) restée(s) en zone de traitement : ['61003']` | vert |
| `61019` Strategy Session, recherche **refusée** | ROUGE : `['61020']` | vert |
| `62022` Dynamic Duo, carte tirée qui n'est pas Team-Up | ROUGE : `['62017']` | vert |
| `61008`, recherche **acceptée** (contre-cas) | vert | vert |
| `61019`, recherche **acceptée** (contre-cas) | vert | vert |
| `01095` Rhino (II), recherche puis **révélation** (contre-cas) | vert | vert |
| `ze014` The Mother of Night ×2 (garde-fou du **double** appel) | vert | vert (rouge sur la 1re version du sas) |

Les contre-cas sont obligatoires : sans eux, un correctif qui renverrait au
deck **toute** carte cherchée resterait vert sur les trois cas d'échec tout en
cassant les cartes. Ils vérifient que l'allié entre bien en jeu
(`en_jeu: ["61003"]`), que la manigance arrive bien en main
(`en_main: ["61020"]`), et que la carte cherchée **puis révélée** finit bien en
jeu (`01095`, `en_jeu: ["01107"]`).

Les trois cas de recherche qui existaient déjà (`si008` Stark Island, `ar003`
To Battle!, `st001b`) sont restés verts avant comme après. Passe des huit cas
« recherche » après la ronde de relecture : **8/8**.

## Verdict de la batterie

`tools/test_capacites.py` EN ENTIER, `PARALLELES=6`, sur un dossier de jeu
jetable (`.game-src-jjc`, supprimé après la passe ; ni `.game` ni `.game-src`
n'ont été touchés), après la ronde de relecture :

**2346 / 2351 cas passés.**

Les cinq rouges, **rejoués un par un en séquentiel** :

| cas | rejoué seul | sans mon correctif (`.game-src-ref`) | verdict |
| --- | --- | --- | --- |
| `vr009` Lethal Protector | **vert** | — | **artefact de passe parallèle** (« aucun résultat, processus mort ») |
| `sg009` Squirrel Girl's Costume | rouge | **rouge, message identique** | antérieur |
| `sg013` Call the Squirrels | rouge | **rouge, message identique** | antérieur |
| `sg007` The Gatherer | rouge | **rouge, message identique** | antérieur |
| `sg006` The Forager | rouge | **rouge, message identique** | antérieur |

Ce sont, **nommément**, les cinq mêmes cas que le rapport du 20/09 relevait
déjà : `sg009`, `sg013`, `sg007`, `sg006` et un artefact de passe parallèle
(`ma015` chez lui, `vr009` ici, l'artefact ne tombant pas sur le même cas d'une
passe à l'autre). Les **totaux**, eux, ne se comparent pas : 2344 le 20/09,
2349 pour la session voisine, 2351 ici, sur un arbre partagé où plusieurs
sessions ajoutent des cas. Ce sont les noms qui font foi.

Les quatre `sg0xx` sont établis comme antérieurs **par mesure**, sur le moteur
de référence, et non repris sur parole.

Les huit cas qui touchent au sas sont verts dans la passe complète : `ze014`
×2 (1809, 1810) et les six témoins (2345 à 2350).

### Une passe entière perdue sur un piège de ports, et ce qu'il en reste

La première passe de la ronde 2 a rendu **2282/2351**, avec **soixante-cinq**
faux rouges « aucun résultat (processus mort) ». Aucun n'était une régression :
tous mouraient sur `AssertionError: ip='127.0.0.1', port=<n>` **avant d'avoir
démarré la partie**. La base de ports choisie était 49000, donc une plage
49000-51350, et **49152 est le début de la plage dynamique de Windows** ; WSL2
partage la pile réseau de l'hôte, une bonne partie de ces ports est réservée
sans que rien ne le dise. Relancée sur la base 36000 : zéro.

Le motif « rouges en masse = artefact avant régression » a donc payé une
seconde fois. Il est maintenant **un garde-fou de code et plus seulement de
prose** : `main()` de `tools/test_capacites.py` refuse de démarrer si la plage
atteint 49152, avec la raison ; et le §8 de `GUIDE-CREATION-CONTENU.md` le dit
aussi, à côté de l'avertissement sur les plages qui se recouvrent.

**Réserve de méthode.** La passe retenue reste une passe parallèle : les cinq
rouges ont été rejoués en séquentiel un par un, pas les 2346 verts.

## Ce qui reste, et mes inquiétudes

- **La carte CHOISIE mais impayable est toujours DÉFAUSSÉE, pas rendue au
  deck.** Si le joueur accepte de jouer l'allié trouvé par Calling in Favors et
  n'arrive pas à payer, `PlayCardsLikeInTurn` le défausse
  (`player_action.py:1007`, `if not played ... DiscardAll`). Mon filet ne voit
  rien : la carte n'est plus dans le sas. C'est un second défaut, plus petit,
  de la même famille que le correctif de paiement du 20/09, et il n'est pas
  traité ici : une carte cherchée qu'on n'arrive pas à jouer devrait retourner
  au deck, pas à la défausse. Aucun témoin ne le couvre. **Inscrit au backlog
  en point D** de `.planning/todos/2026-09-20-trois-signalements.md`, avec le
  témoin à écrire.

- **Le sas n'est refermé qu'à la fin de la résolution d'un effet.** Une carte
  sortie d'un deck par un chemin qui ne passe pas par
  `EffectInvoker.ResolveSelfInternal` (triche, mise en place, commande Puzzle)
  n'est pas couverte. Aucun de ces chemins n'est joué par un joueur.

- **Je n'ai pas prouvé le geste EXACT d'Aghenatak.** J'ai prouvé que la
  recherche laisse la carte dans le sas quand le choix qui suit n'est pas pris,
  avec un pilote qui refuse ce choix. En partie réelle, refuser ce choix peut
  vouloir dire « j'ai cliqué sur passer », « je n'ai pas pu payer » ou « j'ai
  fermé la fenêtre » ; le résultat est le même et les trois mènent au même
  état, mais je n'ai pas relu le client pour dire lequel des trois il a fait.

- **Le paquet `jj` reste sans couverture par ailleurs.** Les quatre témoins
  `61008` / `61019` sont les quatre premiers cas du pack officiel Jessica Jones
  dans `test_capacites.py` (les cas `jj0xx` existants portent sur
  `jessica_jones_custom`, un pack fan-made homonyme). Le reste du pack n'est
  toujours pas testé.

- **La garde `is_revealing` n'a aucun cas qui la fasse mordre.** Le témoin
  `01095` reste vert avec la garde neutralisée : sur le seul chemin connu, la
  révélation se termine dans l'opération. Je la garde parce qu'elle ne coûte
  rien, mais je ne peux pas prouver qu'elle sert, ni qu'elle est inatteignable.
  Le témoin tient la séquence « chercher puis révéler », pas la garde.

- **L'écran ne dit rien.** Le joueur qui refuse voit la carte disparaître de
  la table sans un mot. Une ligne « la carte cherchée retourne dans votre
  deck » serait à sa place côté client ; elle n'existe que dans le journal de
  débogage.

- **J'ai pollué la passe de la session voisine.** Nos deux batteries lisent le
  même `src/` vivant : la sienne, lancée à 00:13, a vu arriver ma première
  version du sas vers 00:33. Ses deux `ze014` rouges en viennent. Son verdict
  (2342/2349) est donc à relire avec cette réserve ; elle l'a écrit sans
  pouvoir le savoir. Il n'y a pas de parade tant que les sessions partagent
  l'arbre : seule une copie gelée de `src/` par passe l'éviterait.

- **Une heure et demie de machine brûlée sur un piège de ports.** Voir le
  verdict de batterie : base 49000, plage mordant sur 49152, soixante-cinq faux
  « processus mort ». Le garde-fou est posé, mais c'est la deuxième fois que
  ce motif coûte une passe complète à ce dépôt.
