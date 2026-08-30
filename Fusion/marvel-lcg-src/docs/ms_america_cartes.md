# Pack Ms. America — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. **30 card_id** au
total (`ma001a` à `ma029`, les faces `a`/`b` de Ms. America comptant pour deux
identifiants distincts). Source : pack fan-made **jakxin**. 2 faces héros,
15 cartes signature, 1 obligation, 4 cartes némésis, 4 cartes d'aspect/basiques
et 4 re-skins `full_link`. **Set 137, préfixe `ma`.** Personnage : America
Chavez, la Starling venue d'un autre univers.

Les étapes 1 et 3-6 de PROCESSUS-HEROS (cards.json, deck de départ,
`data/nemesis/ms_america_nemesis.json`, `data/sets_info.json`, préfixe déclaré,
30 images) ont été faites lors d'une session antérieure, **avec vérification
des 23 icônes de ressource par découpe d'image en planche** et de l'icône de
mot-clé de `ma019` contre trois cartes-témoins (recette reproductible :
`tools/importer_images_ms_america.py`, `assets/pics/` étant gitignoré). Le
moteur a reçu deux ajouts, tous deux commentés `# CORRECTIF` dans
`game/card/face/card_face.py` : le **trait `STARLING`** et le **compteur
`star`**.

Cette session a couvert l'**étape 2** (les 26 scripts) et les **étapes 7 à 10**
(biographie, texte FR, règle de deck-building, validation carte par carte,
autoplay, gate finale).

---

## Le pack en une phrase : modifier ses stats, et jouer des cartes SUPERPOWER

L'insert de l'auteur le dit mot pour mot : « **America wants to do two things:
modify her stats and play SUPERPOWER cards.** » Tout tourne autour de
**Star-Gaze** (`ma001a`), la Response de la face héros qui se déclenche APRÈS
avoir joué une carte `[[SUPERPOWER]]` et qui branche sur la **ressource
IMPRIMÉE** de cette carte : `[physical]` 1 dégât, `[energy]` soigner 1,
`[mental]` retirer 1 menace, `[wild]` la redresser.

⚠ **Fait mesuré le 30/08/2026, à ne pas redécouvrir** : le trait `SUPERPOWER`
n'existe **que sur des cartes de héros** dans tout le catalogue — **0** carte
Agression, **0** Justice, **0** Leadership, **2** Protection. Star-Gaze ne se
déclenche donc quasiment que sur les cartes signature de ce pack, sur `ma025`
Power Stomp, et sur ce que `ma006` Star Flight **convertit**. Une couverture
faible en autoplay est **normale**, ce n'est pas un défaut. C'est aussi
pourquoi l'aspect retenu (JUSTICE, tranché par l'utilisateur) ne change
presque rien au déclenchement de la capacité d'identité : le choix porte sur le
reste du deck (CTR 1 est le pire pouvoir d'America, Justice comble le trou).

Trois cartes rendent Star-Gaze pilotable, et c'est le cœur du pack :
- **`ma005` Star Light** change la ressource imprimée de la carte payée en
  `[wild]`, donc « redresser Ms. America », le plus fort des quatre effets ;
- **`ma006` Star Flight** donne le trait `SUPERPOWER` à un événement joué,
  seul moyen du catalogue de faire mordre Star-Gaze sur une carte d'aspect ;
- **`ma008` Energy Infusion** rejoue Star-Gaze une seconde fois, sur la même
  couleur.

## La règle de la flèche, appliquée à neuf cartes

`→` sépare un **COÛT** (à gauche) d'un **EFFET** (à droite), et la capacité ne
se déclenche **que si le coût est intégralement payable**. Règle officielle,
appliquée sans exception. Elle vaut **aussi pour une capacité FORCÉE**
(`11014`, `11031`, `16074`) ; quand une carte veut deux **conséquences**, elle
les relie par « and » **sans** flèche (`02021` Pumpkin Bombs).

| Carte | Coût (gauche de la flèche) | Rendu par |
|---|---|---|
| `ma001b` | défausser une carte de ta main | `CostFunc.Discard("YourHandCards")` |
| `ma004` | incliner Santana Family | `CostFunc.Exhaust("This")` |
| `ma005` | incliner Star Light | `CostFunc.Exhaust("This")` |
| `ma006` | incliner Star Flight | `CostFunc.Exhaust("This")` |
| `ma007` | incliner **et** retirer 4 compteurs `star` | `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 4, 'star')` |
| `ma009`/`ma010` | choisir CTR ou ATQ **et redresser ton identité** | `CostFunc.Ready("YourIdentity")` |
| `ma013`/`ma014` | trouver un allié dans une défausse et le poser incliné | `conditions=` (voir écarts) |
| `ma017` | subir 2 (ou 4) dégâts | `CostFunc.TakeDamage(N, "YourIdentity")` |
| `ma024` | incliner Noh-Varr's Ship | `CostFunc.Exhaust("This")` |

Le point commun : **le coût est porté par la capacité elle-même**, pas recodé à
la main dans le corps. Le moteur ne propose alors pas la capacité quand le coût
n'a aucune cible légale (`CostFunc.Base.HasTargets`, `cost_func.py:49`). C'est
la seule construction qui rende « coût impayable = rien ne se passe » sans
l'écrire.

## Arbitrages tranchés par l'utilisateur (documentés, non rediscutés)

1. **`ma009`/`ma010` America's Anger : l'exception est REFUSÉE** (30/08/2026).
   Le coût est « choisir CTR ou ATQ **et redresser ton identité** ».
   **Conséquence assumée et voulue : si l'identité est déjà prête, le coût
   n'est pas payable et la carte est INJOUABLE.** Il faut s'être incliné
   d'abord (avoir attaqué, contré ou défendu). Ce n'est pas un défaut, il ne
   faut ni le « corriger » ni le contourner. Le cas 736 est là pour que
   personne ne le change sans le voir tomber.
2. **`ma018` Catalina Chavez : lecture LITTÉRALE de « each stat modifier in
   your play area »** (30/08/2026) — **tout** ce qui est dans la zone de jeu du
   joueur, y compris les améliorations posées sur ses **alliés** (Inspired,
   Laser Blaster, Danger Room Training…), pas seulement celles attachées à
   l'identité. C'est la lecture la plus punitive, et c'est celle qui est
   demandée.
3. **`ma019` porte `Hazard`, et rien d'autre.** L'icône a été vérifiée **par
   découpe d'image** contre `ag011` (qui déclare `Crisis` ET `Acceleration`),
   avec `hd022` (Hazard, carte-plus **nue**) et `hd026` (Acceleration,
   carte-plus **soulignée**) en contrôles : c'est la version **nue**. À vue on
   aurait dit Acceleration. Point clos, à ne pas rouvrir.
4. **`ma018` : `HP: "4"` SANS étoile, délibérément.** `FormatPlayerNumValue`
   (`has_attribute.py:17`) transforme un `HP: "4*"` en 4 × nb_joueurs, alors
   qu'un `ATK: "1*"` vaut « 1 dégât consécutif » (`can_attack.py:47`). Sur ce
   pack l'étoile imprimée renvoie à la **capacité ★**, pas à un par-joueur — le
   marqueur par-joueur du pack est l'icône **personnage**, visible sur `ma019`.
5. **Aspect JUSTICE** pour le deck de départ (voir `metadata.aspect_note`).
   Les trois cartes AGRESSION du pack (`ma022`, `ma025`, `ma026`) entrent au
   catalogue et restent deckables, mais ne peuvent pas figurer dans ce deck.

## Écarts assumés, non corrigés

| Sujet | Écart | Pourquoi, et pourquoi il n'est jamais plus permissif |
|---|---|---|
| `ma005`, « change the printed resource » | rendu par un **DRAPEAU** sur `effect.world`, lu par Star-Gaze, plutôt que par une vraie mutation | le moteur SAIT muter une ressource imprimée (`Message.WhenCountingResourcesOnCards` + `SetReturnValue`, employé par `29038` Haywire et `40037a` Domino), mais cette voie changerait AUSSI ce que la carte vaut si elle était ensuite **dépensée** comme ressource, et pour toute la durée de vie de la capacité. On ne change que ce que Star-Gaze LIT, une fois, pour la carte qui vient d'être payée. Le guide autorise explicitement ce repli. Effacé à la fin de la phase (`RunAt.TheEndOfThePhase`). |
| Star-Gaze, carte à **plusieurs** icônes imprimées | on résout **une fois chaque COULEUR présente** | le texte dit « was » (singulier) et **aucune** carte SUPERPOWER du catalogue n'imprime deux couleurs différentes : le cas est théorique. Quand il se présentera, on suit l'idiome déjà établi du dépôt pour cette lecture (`av007` Unlikely Allies et `wd154`, tous deux « printed resource area **includes** »). Deux icônes de la MÊME couleur (`ma008` « GG ») ne déclenchent qu'une fois : on lit des couleurs, pas des icônes. |
| `ma013`/`ma014`, la flèche-coût | rendue par une `conditions=` et non par une `CostFunc` | aucune `CostFunc` du moteur ne sait dire « trouver un allié dans une défausse et le poser incliné » : `CostFunc.SearchForCard` (`cost_func.py:979-1040`) ne fouille que les zones de **Rencontre**, ne sait pas poser incliné et ne sait pas viser un autre joueur. La `conditions=` rend la carte **injouable** sans allié (cas 739), ce qui est le comportement voulu ; le corps re-vérifie avant d'agir. Précédent : `pt017` branche 1. |
| `ma009`/`ma010`, « choose THW or ATK » | la moitié « choisir » du coût est résolue **dans le corps** | un choix entre deux options toujours disponibles ne peut jamais échouer : le placer avant ou après le paiement ne change aucune partie. Aucune `CostFunc` du moteur ne sait « choisir un mot ». **Aucun effet en jeu.** |
| `ma018`, mesure des modificateurs | lus sur les **personnages amis** (`face.attack - face.printed_attack`) | le moteur n'expose nulle part « la liste des modificateurs posés par une carte ». Mesure refaite le 31/08/2026, par type de carte : ces clés portent sur **170 Attachements** de rencontre (Charge, Enhanced Ivory Horn) et **une seule Amélioration** dans tout le catalogue — autrement dit elles sont, à une carte près, absentes du côté joueur — Combat Training, Heroic Intuition et Inspired expriment leur bonus **en code** (`GiveKeywordToAttached`). On lit donc le résultat là où il est visible. Tout modificateur posé par une carte de la zone de jeu s'y retrouve, sur l'identité comme sur les alliés. |
| `ma019`, menace de départ | **X, câblée à la main** dans le `When Revealed` | `desc.StartingThreat` ne sait porter qu'un nombre : il ne peut pas dire « la somme du coût des cartes attachées ». La manigance entre à 0 et son `When Revealed` pose la valeur calculée. Précédents EXACTS du dépôt, avec le même commentaire : `mw018` The Grim Hunt et `wc019a` New Vessel. |
| `ma007`, portée de l'annulation | `"AnyPlayer"` et non `"You"` | le texte dit « When **an encounter card is revealed** », sans « you » ni « against you ». `mw009` Foresight dit « When **YOU** reveal an encounter card » et emploie `"You"` : deux textes différents, deux portées différentes. En solo la différence est nulle ; en multijoueur Ms. America peut protéger un coéquipier, ce que le texte autorise. |
| `ma008`, « the played **event** » | on suit « a SUPERPOWER **card** », la première moitié de la phrase | l'auteur écrit « card » dans la condition de déclenchement et « event » dans la clause de couleur. Lire « event » au sens strict rendrait la clause de couleur INAPPLICABLE quand une amélioration SUPERPOWER est payée, alors que la Response, elle, serait partie : la capacité n'aurait aucun effet, ce qui n'est écrit nulle part. |
| `ma006`, portée du trait donné | `GainUntilPhaseEnd` | la portée n'est pas imprimée sur la carte. Le trait sert à Star-Gaze, qui résout dans la même fenêtre. `GainUntilRoundEnd` aurait laissé le trait sur la carte défaussée jusqu'à la fin du round — **plus permissif**, donc écarté. |
| `gwenpool` / « Gwenpool » | **rien n'est corrigé côté `gp`** | le jeu contient déjà un pack complet `gwenpool` (préfixe `gp`, identité « Gwenpool »). `ma022` est un ALLIÉ homonyme : deux cartes distinctes, aucune collision moteur, et `ma022` ne fait aucune recherche par nom. |
| `04011` / `kb001a` / `ma003` « Hawkeye » | **aucune recherche par nom** | trois cartes portent ce nom (l'allié officiel `04011`, le héros du pack `kate_bishop`, et `ma003`). Les deux capacités de `ma003` ne parlent que d'elle-même (`"This"`). Rien n'est corrigé ailleurs. |

## Une clé ajoutée au harnais : `declencher_apres`

`tools/test_capacites.py` exécute ses étapes dans cet ordre : `mise_en_place`,
`main`/`main_exclusive`, `declencher`, `jouer`. Deux cartes de ce pack ne sont
donc pas testables en l'état :

- **`ma009`** — « double all modifiers … **on its next use this turn** » : il
  faut ATTAQUER après avoir joué la carte ;
- **`ma003`** — « **if you have resolved "Star-Gaze" this turn** » : il faut
  avoir JOUÉ une carte SUPERPOWER avant que l'attaque ne la tue.

`declencher_apres` exécute des commandes `Puzzle.*` **après** `jouer`. Clé
**additive** : aucun cas existant ne la définit, aucun n'est modifié. Même
esprit que `preferer_option` (pack `wiccan`) et `choisir_option` (pack
`kate_bishop`), ajoutées de la même façon pour les mêmes raisons.

## Deux pièges de banc payés sur ce pack, à ne pas repayer

1. **`Puzzle.SetThreat('01097b', N)` ne fait RIEN.** Les commandes `Puzzle.*`
   cherchent par **NOM** (`FindOrCreateFace`), pas par `card_id` : avec un
   identifiant, elles fabriquent une carte orpheline et la menace n'arrive
   jamais sur le vrai complot. Écrire `Puzzle.SetThreat('The Break-In!', N)`.
   Piège déjà écrit au §10 du guide, repayé quand même.
2. **`01061` Great Responsibility, dans la main de départ, AVALE toute pose de
   menace.** « Hero Interrupt: When any amount of threat would be placed on a
   scheme, you may take X damage instead. » Le pilote la joue, la menace part
   en dégâts sur l'identité, et le complot reste à 0. Or `main_exclusive`, qui
   vide la main, tourne **après** `mise_en_place` : toute commande
   `Puzzle.SetThreat` doit donc aller dans **`declencher`**, pas dans
   `mise_en_place`. Six cas rouges pour ce seul motif.
3. **`Puzzle.Attack('01094', defender='ma001a')` ne suffit pas pour tester une
   interruption de défense.** Avec DEF 2 contre ATQ 2, les dégâts tombent à
   **0** et `WhenUnitWouldTakeDamage` (qui exige `at_least_damage=1`) n'est
   jamais envoyé. Il faut au contraire **incliner l'identité** pour qu'elle ne
   défende pas : le déclencheur de `ma011` est bien les dégâts, pas la fenêtre
   de défense.
4. **Un `sed -i` GLOBAL sur `tools/test_capacites.py` touche les autres
   packs.** En corrigeant le piège n°1 ci-dessus, un `sed` sans borne a
   remplacé `Puzzle.SetThreat('01097b'` par `Puzzle.SetThreat('The Break-In!'`
   dans **64 lignes appartenant à d'autres packs** — ce qui n'est pas une
   réécriture cosmétique : elle transforme un no-op (face orpheline) en une
   vraie pose de menace, donc elle change le comportement de cas qui n'étaient
   pas les miens. Le fichier a été **reconstruit** depuis la version d'origine
   plus les seuls ajouts `ms_america`, et le diff final est **816 insertions,
   0 suppression** ; les 41 cas ont été relancés après reconstruction
   (**41/41**). À retenir : sur ce fichier, borner toute réécriture au bloc du
   pack en cours, et contrôler le diff par `git diff --stat` avant de conclure.

## Outils exécutés depuis `.game-src`

| Outil | Résultat |
|---|---|
| `python3.10 -m compileall -q src` | **propre** |
| `tools/test_cards.py` (port 24521) | **4895 ok / 0 err** (référence relevée AVANT les modules : **4869 / 0**), 0 `failures` — soit exactement **+26**, le nombre de modules écrits |
| `tools/verifier_prefixes.py` | **OK** — 5460 cartes, 46 préfixes, 1045 fan-made, aucun doublon |
| `tools/verifier_desc_mots_cles.py ms_america` | **OK** — « les 30 cartes de ms_america ont un desc conforme à leur texte » |
| `tools/verifier_coherence_cartes.py` | **0** carte joueur sans classe, **0** obligation sans destinataire, **0** image manquante. Seul avertissement : `dt134`, antérieur au pack |
| `tools/verifier_noms_modules.py … ms_america` | **OK** — aucun nom inconnu |
| `tools/verifier_cartes_en_jeu.py … ms_america` | **OK** — « les 30 cartes de ms_america portent ce que leur texte annonce » |
| `tools/verifier_api_cartes.py` (port 29100) | 5465 fichiers, **4 en faute — aucune dans `ms_america`** (`sp018`, `underling/__init__`, `wd159`, `wd160`, tous antérieurs) |
| `DECK_NOM=ms_america tools/verifier_tous_les_decks.py` | **`ok: true`** — « identite ma001a, main 4, deck 33 » |
| `DECK_NOM=kate_bishop` (non-régression) | **`ok: true`** — « identite kb001a, main 2, deck 33 » |
| `DECK_NOM=superior_iron_man` (non-régression) | **`ok: true`** — « identite si001a, main 6, deck 34 » |
| Script anti-fuite de PROCESSUS-HEROS §10 | **0 résultat** |
| `tools/test_capacites.py`, 41 cas `ma*` | **41/41** (indices **716 à 756**) |
| `tools/autoplay.py --deck ms_america --vilains rhino --profils equilibre --parties 8` | **0 partie bloquée**, 0 traceback |
| `node --check public/js/deckbuilder/app.js` | **propre** |
| `launch.json` de `$W` après campagne | `['127.0.0.1:2345']` ✔ |

### Preuve par substitution, module par module

Chaque module retiré (et son `__pycache__` purgé), les cas dont le **nom**
commence par son `card_id` sont relancés et doivent tous être **ROUGES** ; le
module est ensuite remis.

| Module | Cas concernés | Résultat sans le module |
|---|---|---|
| `ma001a` | 716, 717, 718, 719, **720** | ROUGE ; **720 reste VERT — contre-épreuve** |
| `ma001b` | 721 | ROUGE |
| `ma002` | 722, **723** | ROUGE ; **723 VERT — contre-épreuve** |
| `ma003` | 724, 725, **726** | ROUGE ; **726 VERT — contre-épreuve** |
| `ma004` | 727 | ROUGE |
| `ma005` | 728 | ROUGE |
| `ma006` | 729, 730 | ROUGE |
| `ma007` | 731, 732, **733** | ROUGE ; **733 VERT — contre-épreuve** |
| `ma008` | 734 | ROUGE |
| `ma009` | 735, **736** | ROUGE ; **736 VERT — contre-épreuve** |
| `ma011` | 737 | ROUGE |
| `ma013` | 738, **739** | ROUGE ; **739 VERT — contre-épreuve** |
| `ma015` | 740, 741 | ROUGE (les deux) |
| `ma017` | 742, 743, 744 | ROUGE |
| `ma018` | 745, **746** | ROUGE ; **746 VERT — contre-épreuve** |
| `ma019` | 747, 748 | ROUGE (les deux) |
| `ma020` | 749, **750** | ROUGE ; **750 VERT — contre-épreuve** |
| `ma022` | 751 | ROUGE |
| `ma023` | 752 | ROUGE |
| `ma024` | 753, 754 | ROUGE (les deux) |
| `ma025` | 755, **756** | ROUGE ; **756 VERT — contre-épreuve** |

`ma010`, `ma012`, `ma014`, `ma016` et `ma021` n'ont pas de cas dédié : ce sont
des **doublons de code** de `ma009`, `ma011`, `ma013`, `ma015` et `ma020`,
comptés comme tels (même convention que `pt004`/`pt006`, `sd004`/`sd007`,
`wc006`).

**Les neuf verts légitimes** (720, 723, 726, 733, 736, 739, 746, 750, 756) sont
tous des **contre-épreuves** : ils affirment que **rien** ne se passe, donc
retirer le module ne peut pas les faire tomber. Chacun a son jumeau positif,
qui est bien rouge — 720/716-719, 723/722, 726/725, 733/732, 736/735, 739/738,
746/745, 750/749, 756/755. Un vert isolé de ce type ne prouve rien ; le couple
en est une preuve.

⚠ **Deux contre-épreuves sont, elles, de vraies preuves rouges** : 754
(`ma024` injouable hors YOUNG AVENGER) et 748 (`ma019` sans allié) rougissent
sans leur module, parce que le moteur pose une capacité de jeu par défaut sur
un Soutien et que la manigance n'aurait alors aucune menace du tout.

## Autoplay : 8 parties, témoin `okoye`, même fournée

| Deck | Parties | Victoires | Rounds moyens | **Bloquées** | Causes de fin |
|---|---|---|---|---|---|
| **ms_america** | 8 | 0 | **5,5** | **0** | 7 × complot principal, 1 × tous les joueurs éliminés |
| `okoye` (témoin) | 8 | 0 | 4,1 | **0** | 6 × complot principal, 2 × tous les joueurs éliminés |

Le taux de blocage absolu ne veut rien dire (le pilote se coince aussi tout
seul) : c'est l'**écart au témoin** qui compte, et il est **nul sur le
blocage**, légèrement **favorable à Ms. America** sur la survie (5,5 rounds
contre 4,1, 1 élimination contre 2).

⚠ **Lecture honnête de l'écart** : `01093` Tenacity, seul bloqueur d'autoplay
officiel connu du projet, est **dans le deck d'okoye et pas dans celui de
Ms. America** (`metadata.tenacity_note`). L'écart joue donc en faveur du héros
custom et doit être lu comme tel. Cela dit, **aucune des 8 parties d'okoye n'a
été bloquée non plus** : le piège ne s'est pas déclenché, et la comparaison
reste exploitable.

Grep exhaustif sur les **16 journaux** :

```
NameError|AttributeError|TypeError|KeyError|AssertionError  ->  0 partout
traceback|exception (insensible a la casse)                 ->  0 partout
```

**Couverture des `card_id` en partie réelle : 27/30.** `ma001a` et `ma001b`
8/8, `ma010` et `ma013` et `ma017` 7/8, `ma011` 6/8, `ma002`/`ma005`/`ma028`
5/8, `ma003`/`ma023`/`ma029` 4/8, `ma006`/`ma007`/`ma008`/`ma009`/`ma012` 3/8,
`ma004`/`ma014`/`ma015`/`ma016`/`ma018`/`ma019`/`ma020`/`ma021`/`ma027` 2/8,
`ma024` 1/8. **Les trois absentes sont AGRESSION** — `ma022` Gwenpool, `ma025`
Power Stomp et `ma026` (re-skin de Moment of Triumph) — donc absentes du deck
de départ Justice **par construction** (`metadata.cartes_du_pack_note`), pas
par accident. Elles sont couvertes par les cas 751, 755 et 756.

### Lecture ligne à ligne — le cycle flèche-coût → carte jouée → Star-Gaze

`/tmp/autoplay_ms_america_rhino_normal_equilibre_2.log`, lignes 73 à 92 :

```
 73: [[ma009 America's Anger]] were placed on table
 74: Ms. America gains resource Y from [ma024 Noh-Varr's Ship], total Y   <- la ressource du vaisseau
 75: [[ma024 Noh-Varr's Ship]] were discarded
 76: [[ma001a Ms. America]] readied ([ma009 America's Anger])             <- LE COUT DE LA FLECHE
 77: Ms. America would play [ma009 America's Anger] with (Y)
 78: [ma009 America's Anger] activates
 79: [[ma009 America's Anger]] were discarded
 80: [ma001a Ms. America] activates, targets [[ma001a Ms. America]]       <- STAR-GAZE
 81: [ma001a Ms. America] would deal 1 damage to [01094 Rhino]            <- branche [physical]
 84: [01094 Rhino] perd 1♡
 86: [[ma001a Ms. America]] exhausted
 87: [ma001a Ms. America] va attaquer [[01094 Rhino]] (+0)
 89: [ma001a Ms. America] would deal 2 damage to [01094 Rhino]
 92: [01094 Rhino] perd 2♡
```

Tout y est, dans l'ordre : le **coût** est payé AVANT l'effet (ligne 76,
l'identité est redressée), la carte se joue (77-79), **Star-Gaze part** sur la
ressource IMPRIMÉE de la carte jouée (80-84, `ma009` est `[physical]` → 1 dégât),
puis le héros s'incline pour attaquer (86-92). Le journal de round confirme que
le pilote a choisi la branche **CTR** (`Double_all_modifiers_applied_to_your_THW`)
et non ATQ, ce qui explique que l'attaque suivante vaille bien 2 et non 4 :
sans modificateur d'ATQ en jeu, doubler des modificateurs nuls ne fait rien.
C'est le texte.

### Lecture ligne à ligne — Bulletproof Chica en défense réelle

Même journal, lignes 348 à 356 :

```
348: [[ma011 Bulletproof Chica]] were placed on table
351: Ms. America would play [ma011 Bulletproof Chica] with (B)
352: [ma011 Bulletproof Chica] activates
353: Prevented 2 of this damage ([ma011 Bulletproof Chica])   <- « prevent ALL of that damage »
355: [ma001a Ms. America] gained Tough ([ma011 Bulletproof Chica])
356: [[ma011 Bulletproof Chica]] were discarded
```

Les DEUX conséquences partent ensemble (la prévention **et** le statut) : elles
sont reliées par un point, sans flèche, donc aucune n'est conditionnelle.

## Limites du harnais, explicites et non masquées

1. **La branche « surge » de `ma020`/`ma021`.** « If no attack is made this
   way, this card gains surge » n'a **pas** de cas dédié : le surge d'une
   traîtrise distribue une carte de rencontre supplémentaire, et le harnais
   n'expose aucune clé pour observer cette distribution de façon déterministe
   (`ThisCardGainSurge` n'est lisible ni dans `etat_attendu`, ni via un
   compteur). Ce qui EST prouvé : la branche « no attack » est bien la seule
   qui parte quand Catalina est absente (cas 750, ni dégât ni Sonné). Ce qui ne
   l'est pas : la bascule du surge elle-même. Elle est correcte par lecture
   (`ThisCardGainSurge`, `cards/pack/__init__.py:100`, l'idiome de `il021`,
   `il022`, `22031` et `pt017`), **jamais observée**. Même limite que `pt017`.
2. **La seconde capacité de `ma004`** (« Events attached to Santana Family may
   be played **as if they were in your hand** »). Ce qui EST prouvé : l'action
   d'identité civile attache bien l'événement, face cachée, sous le soutien, et
   incline la carte (cas 727). Ce qui ne l'est pas : le fait de le **jouer**
   depuis cette zone. Le harnais ne sait pas enchaîner « action d'alter-ego,
   puis bascule en forme héros, puis jeu d'une carte hors de la main » dans un
   seul cas : `Puzzle.ChangeToFace` doit vivre dans `mise_en_place` (sinon la
   nouvelle forme n'est pas active pour les commandes suivantes, GUIDE §10),
   or l'action d'attachement, elle, exige la forme civile. **L'outil qui manque
   est nommé : une commande `Puzzle.ChangeForm` utilisable en cours de
   `declencher`.** La construction, elle, est copiée mot pour mot de `27007`
   George Stacy et `dz014` Lightbringr, toutes deux vérifiées en jeu.
3. **La branche `[wild]` de Star-Gaze quand l'identité est déjà prête** n'a
   aucun effet observable : le cas 719 l'incline d'abord, exprès.
4. **La règle de deck-building de `ma001b`** vit dans le deck-builder, pas dans
   le moteur (GUIDE §5.2) : elle n'est pas testable par `test_capacites`. Elle
   est contrôlée hors navigateur par un chargement direct de
   `exemptDeLaLimiteAspect` (résultats plus bas), et `node --check` est propre.
5. **La biographie au survol** et **les tooltips français** : voir la gate
   finale.

## La règle de deck-building, vérifiée hors navigateur

`public/js/deckbuilder/app.js`, `exemptDeLaLimiteAspect` — **troisième cas**
après Madame Web (*Arachnophilia*) et Patriot (*Leader*).

**Comment « qui modifient tes pouvoirs de base » a été tranché.** Ce n'est pas
un trait. Deux voies ont été mesurées le 30/08/2026 sur `data/cards.json` :

- **les clés `desc`** `ATK+` / `THW+` / `SCH+` existent bien (140, 4 et 64
  cartes) mais **uniquement sur des ATTACHEMENTS de rencontre** (Charge,
  Enhanced Ivory Horn, Program Transmitter). **Aucune amélioration d'aspect ne
  les porte** : Combat Training, Heroic Intuition et Armored Vest expriment
  leur bonus **en code** (`GiveKeywordToAttached`). Cette voie est donc presque
  vide — une seule amélioration du catalogue, `52009` Organic Webbing, porte un
  `THW+`.
- **le TEXTE**, dont la formule est stable dans tout le catalogue : « **Your
  hero gets +1 ATK** », « **Your alter-ego gets +1 REC** », « **you get +3
  DEF** ».

**Les deux voies sont gardées** (le `desc` d'abord, le texte ensuite), mais
c'est la seconde qui fait le travail. Le filtre exige aussi `type === "Upgrade"`,
parce que le texte imprimé dit « **upgrade** cards ».

Résultats mesurés (chargement direct de la fonction, hors navigateur) :

```
--- ancrage du nom ---
* Ms. America   true     Iron Patriot    false
Ms. America     true     America Chavez  false
Ms America      true     Miss Americana  false
                         Patriot         false
--- exemptées, attendu OUI ---
01057 Combat Training  01065 Heroic Intuition  01081 Armored Vest
56013 Aggressive Cond. 56046 Defensive Cond.   58021 Heroic Conditioning
60038 Innate Reflexes  61034 Innate Aggression 61036 Innate Perception   -> toutes true
--- NON exemptées, attendu NON ---
01074 Inspired  17019 Laser Blaster  33015 Danger Room Training
34016 Mission Training  03031 Enraged  22032 Energy Spear
01059 Jessica Jones (allié)  ma005/ma006 (signature)                     -> toutes false
--- total ---
64 cartes exemptées : Aggression 8, Justice 4, Protection 5, Leadership 1,
Basic 6, Hero 15, Campagne 21, Determination 3, 'Pool 1
```

⚠ **Le test du nom est ANCRÉ** (`/^\*?\s*ms\.?\s*america$/i`), comme celui de
Patriot : « Iron Patriot » attend d'être porté dans `A créer/`, et le catalogue
contient déjà « America Chavez ». Un `/america/i` lâche aurait attrapé les
deux. L'étoile d'unicité est tolérée parce que `cards/paper.py` la retire côté
moteur, mais pas partout côté client.

Les alliés qui reçoivent des améliorations (Inspired, Laser Blaster, Danger
Room Training) sont **écartés** : « **your** basic powers », ce ne sont pas les
tiennes. C'est la lecture la plus stricte des deux possibles.

---

# Fiches PROCESSUS-CARTE, une par card_id

### ma001a : * Ms. America (face héros)

PV 14 / ATQ 2 / CTR 1 / DEF 2 / MNG 4, traits STARLING + YOUNG AVENGER.

- [x] Étape 2 : cartes de référence : **Star-Gaze** → `av007` Unlikely Allies
      (pack `agent_anti_venom`), même structure « selon la ressource IMPRIMÉE
      de la carte, telle branche », même lecture `carte.printed_resource` avec
      un compteur par couleur, même rendu par une `ForChoiceAbility` par
      branche passée à `player.ChooseAbilities` ; `53018` Redwing fait de même.
      Le DÉCLENCHEUR vient de `60037a` Echo (« After you play an aspect
      event ») : `AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response,
      "You", <filtre>, …)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`After`** (→ `AfterPlayerPlayedCard`, pas `WhenPlayerPlayCard` : c'est
      ce qui laisse `ma006` poser le trait SUPERPOWER entre les deux) ;
      **`you`** (→ `"You"`, jamais `"AnyPlayer"`) ; **`card`** et non
      « event » (les trois améliorations SUPERPOWER du pack déclenchent en
      entrant en jeu) ; **`printed resource`** (→ `printed_resource`, PAS
      `using_res=`, qui aurait rendu « payé avec ») ; **`Response`** nu (la
      capacité est imprimée sur la face héros, elle n'existe donc pas en forme
      civile — le moteur s'en charge).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 14, ATQ 2, CTR 1, DEF 2, MNG 4
      (`desc` et scan identiques, lus nativement) ; **1** dégât, **1** soin,
      **1** menace ; aucune autre valeur.
      Résultat : conforme.
- [x] Étape 7 : cinq cas, un par branche plus une contre-épreuve :
      716 ([physical]), 717 ([energy]), 718 ([mental]), 719 ([wild]),
      **720** (contre-épreuve : carte non-SUPERPOWER). Sans le module :
      716-719 **ROUGES**, 720 reste vert (il affirme que rien ne se passe).
      Résultat : conforme.
- [x] Étape 8 : autoplay ciblé : 8 parties, témoin `okoye`, grep tracebacks :
      **0** ; `ma001a` vue 8/8 ; cycle Star-Gaze lu ligne à ligne ci-dessus.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma001b : * America Chavez (face alter-ego)

STARLING. PV 14 / REC 5 / main 6.

- [x] Étape 2 : cartes de référence : **Thinking With Portals** → `sd001b`
      Thomas Shepherd / Accelerated Perception (pack `speed`), même fabrique
      `WhenInYourPlayTurn(AbilityType.Action, …)` sur une face ALTER-EGO, même
      `.LimitOncePerRound()`, même couple `Search.PlayerCard(
      include_discard_pile=True)` + `Faces.ShuffleAllTo(…, player.player_deck,
      …)`. Modèles d'origine : `ok011` Upanga et `60014` Karen Page. Le coût
      « défausser une carte de ta main » : `01015`, `03001a`, `45014`, tous en
      `CostFunc.Discard("YourHandCards")`.
      **La première phrase n'a AUCUNE carte de référence : ce n'est pas une
      capacité de jeu**, c'est une règle de deck-building (§14.1 du guide).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Action` nu** sur une face alter-ego → `AbilityType.Action`, comme
      `sd001b`, `wc001b`, `ss001b`, `10001b`, `01029b` (et non
      `AlterEgoAction`, réservé aux cartes JOUEUR) ; **la flèche** est un coût
      porté par la capacité, donc pas d'action proposée main vide ;
      **`a card`** sans filtre de type, contrairement à `sd001b` qui dit
      « an event » — on ne recopie pas une carte sur l'autre ;
      **`(Limit once per round.)`** → `.LimitOncePerRound()` ;
      **mot-clé cité mais pas imprimé** : aucune capacité fantôme pour la règle
      de deck-building.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 14, REC 5, main 6 (lus nativement) ;
      **1** carte défaussée, **1** carte remontée, **1** fois par round.
      Résultat : conforme.
- [x] Étape 7 : cas 721, vérificateur sur mesure
      `ma001b_carte_remontee_dans_le_deck` (`etat_attendu` ne sait pas regarder
      le deck du joueur : « hors_jeu » serait satisfait par une carte restée à
      la défausse). Il contrôle les **trois** faits : la carte cherchée est
      dans le deck, elle n'est plus dans la défausse, et la carte qui a PAYÉ y
      est bien. Sans le module : **ROUGE**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma001b` vue 8/8, « Thinking_With_Portals » apparaît
      dans le journal de 4 rounds sur 6 de la partie 2. 0 traceback.
      Résultat : conforme.

**Écart documenté, sans correction** : le coût étant payé AVANT le corps
(`Effect.ProcessSelfCost`, `effect.py:135`), la carte défaussée pour payer est
déjà dans la pile quand la recherche s'ouvre — elle peut donc être celle qu'on
remonte. C'est la lecture littérale, et c'est ce qui fait de cette action un
outil de **filtrage**.

**Carte terminée : OUI.**

### ma002 : * Alloy (Ramone Watts, allié signature)

Coût 3, PV 3, ATQ 2*, CTR 1*, `[wild]`, `Toughness 1`, traits AERIAL + MUTATE.

- [x] Étape 2 : carte de référence : le DÉCLENCHEUR → `sr007` Great Power
      (pack `spider_man_rainy`) et `av006` Anti-Venom Goo, tous deux montés sur
      `AbilityFactory.AfterCardResolveAbility(…)`. On emploie sa forme
      **nommée**, `ability_name=NOM_STAR_GAZE` (`resolve.py:137-141`), qui
      compare `message.effect.ability.name` à la chaîne posée par `.SetName()`
      sur `ma001a` : c'est le seul lien entre les deux cartes. L'EFFET →
      `12009` Pym Particles, seul usage réel de `GainUntilTurnEnd` du dépôt.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Toughness`** lu NATIVEMENT dans `desc` (`HasToughness`), aucun module
      — fiche `mots-cles/toughness.md`, « base automatique » du guide ;
      **`After you RESOLVE "Star-Gaze"`** et non « après avoir joué une carte
      SUPERPOWER » : deux choses différentes, prouvées distinctes par le
      couple 722/723 ; **`Hero Response`** → sous-type dédié
      `AbilityType.HeroResponse` ; **`until the end of the TURN`** →
      `GainUntilTurnEnd` (`face_action.py:466`), PAS `GainUntilPhaseEnd` ni
      `GainUntilRoundEnd` — trois portées différentes, le texte en nomme une.
      ⚠ `GainAttack` seul accorde le bonus **PERMANENT** (correctif `62015`
      du 29/08/2026) : il n'est pas employé.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3, PV 3, ATQ 2*, CTR 1*,
      `Toughness 1` (lus nativement) ; **+1** ATQ.
      Résultat : conforme.
- [x] Étape 7 : cas 722 (positif) et **723** (contre-épreuve : `01087`
      Haymaker, joué au lieu d'une carte SUPERPOWER, ne donne rien). Sans le
      module : 722 **ROUGE**, 723 vert (jumeau négatif).
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma002` vue 5/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma003 : * Hawkeye (Kate Bishop, allié signature)

Coût 2, PV 2, ATQ 2*, CTR 1*, `[wild]`, trait YOUNG AVENGER.

- [x] Étape 2 : cartes de référence : **[star] piercing + ranged** → `dt024`
      Elektra et `dt026` The Punisher, dont le texte imprimé est mot pour mot
      « <X>'s attacks gain piercing and ranged » et qui s'écrivent
      `AbilityFactory.UnitAttackGainKeyword("This", piercing=True,
      ranged=True)` (`do_attack.py:827-838`). **Le remplacement de la défaite**
      → `kb002` Hawkeye / Clint Barton (pack `kate_bishop`), texte IDENTIQUE à
      la clause près, même `WhenUnitWouldBeDefeated(AbilityType.Interrupt,
      "This", …, by_consequential_damage=True)`, même
      `message.SetBeInstead(effect)`, même `Faces.ShuffleAllTo([this],
      player.player_deck, effect)`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`instead`** (leçon The Spot) → `SetBeInstead` AVANT le déplacement : la
      défaite n'a PAS lieu, la carte PART dans le deck ; sans lui elle irait à
      la défausse ET dans le deck ; **`by CONSEQUENTIAL damage`** →
      `by_consequential_damage=True` (`defeated.py:11`), sans quoi la capacité
      partirait sur n'importe quelle défaite ; **`into your DECK`** →
      `player.player_deck`, pas la défausse ; **`if you have RESOLVED
      "Star-Gaze" this turn`** → le drapeau du set, posé par `ResoudreStarGaze`
      et vidé par `RunAt.TurnEnd`, porté par une `conditions=` (la capacité
      n'est pas proposée quand elle est fausse) ; **`Interrupt` nu**, sans
      libellé.
      ⚠ Rappel indépendant : **`ranged` ignore la RIPOSTE, pas le Garde**
      (`can_retaliate.py:38` est le seul lecteur d'`IsRanged()`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2, PV 2, ATQ 2*, CTR 1* (lus
      nativement) ; aucune valeur codée en dur.
      Résultat : conforme.
- [x] Étape 7 : trois cas. **724** prouve `piercing` : Rhino reçoit un jeton
      Robuste, Hawkeye attaque, le Robuste saute et les 2 dégâts passent —
      sans le mot-clé le relevé montrerait 0. **725** prouve l'interruption
      (module + `declencher_apres`, seule façon de jouer une carte SUPERPOWER
      AVANT l'attaque qui la tue) avec un vérificateur sur mesure qui distingue
      deck et défausse. **726** est la contre-épreuve : sans Star-Gaze résolue,
      elle est bel et bien vaincue. Sans le module : 724 et 725 **ROUGES**,
      726 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma003` vue 4/8. 0 traceback.
      Résultat : conforme.

**Limite déclarée** : `ranged` n'est pas observable ici — aucun ennemi du
scénario `rhino` n'a Riposte.

**Carte terminée : OUI.**

### ma004 : * Santana Family (soutien signature)

Coût 1, `[mental]`, trait PERSONA.

- [x] Étape 2 : cartes de référence : `27007` George Stacy (Ghost-Spider) et
      `dz014` Lightbringr (pack `dazzler`, trait PERSONA lui aussi), tous deux
      montés sur `*AbilityFactory.AttachedCardCanPlayLikeInHand(
      CardFinder(card_type=Event))` + une action qui glisse une carte SOUS le
      soutien avec `conditions=[… GetPlacedCardArea().GetSize() < N]` et
      `CostFunc.Exhaust("This")`. Pour la moitié « chercher dans la DÉFAUSSE »
      (George Stacy prend dans la main) : `dt079` Borrowed Gear, qui fouille
      `discard_pile` puis appelle `TuckCardUnderHere`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Events attached`** → `CardFinder(card_type=Event)`, le filtre est
      écrit parce que le texte l'écrit ; **`FACEDOWN`** →
      `TuckCardUnderHere(face, effect)` sans `peek=` (`PlaceCardHere(faces,
      False, effect)`), et non le `peek=True` de `53021` Resource Reserve ;
      **`(to a maximum of 2)`** → `conditions=` qui rend l'action indisponible
      dès que la zone est pleine (le moteur n'a aucun mécanisme dédié : idiome
      de `27007`, `dz014`, `60030`) ; **`ALTER-EGO Action`** → sous-type dédié
      `AbilityType.AlterEgoAction` : la carte se **remplit** en identité civile
      et se **dépense** en forme héros.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 1 ; **2** événements au maximum
      (`MAX_EVENEMENTS_SANTANA`).
      Résultat : conforme.
- [x] Étape 7 : cas 727, vérificateur sur mesure `ma004_evenement_attache`
      (l'événement est dans `GetPlacedCardArea()`, et le soutien est incliné —
      les deux moitiés, le coût compris). Sans le module : **ROUGE**.
      La seconde capacité n'a pas de cas : voir « limites du harnais » n°2.
      Résultat : conforme, avec une limite déclarée.
- [x] Étape 8 : autoplay : `ma004` vue 2/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI**, avec une limite du harnais nommée (la lecture
« jouable comme si elle était en main » n'est pas exercée ; la construction est
copiée mot pour mot de deux cartes vérifiées).

### ma005 : * Star Light (amélioration signature)

Coût 2, `[energy]`, trait SUPERPOWER.

- [x] Étape 2 : carte de référence : `kb013` Kate's Quiver (pack
      `kate_bishop`), même structure « Resource: Exhaust X → generate a [wild]
      resource ET un second effet », même montage
      `CanGenerateResources(…, Resources("G"), ex_operation=…)` +
      `.SetCostFunc(CostFunc.Exhaust("This"))`. Le second effet passe
      OBLIGATOIREMENT par `ex_operation=` : son oubli **côté moteur** avait
      rendu Sue Storm et Reed Richards à moitié muets (GUIDE §8).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Hero Resource`** → `AbilityType.HeroResource` ; **la flèche** est un
      coût ; **`the PLAYED card`** → `message.paying_card`
      (`sender_player.py:281-285`), avec garde quand elle est absente ;
      **`You MAY`** → `player.MayChooseOneAbility` (le joueur peut refuser) ;
      **une seule `CanGenerateResources` par carte** (assert
      `card_player.py:50`) : les deux phrases tiennent dans une seule fabrique.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; **1** ressource `[wild]`.
      Résultat : conforme.
- [x] Étape 7 : cas 728. Preuve indirecte mais sans ambiguïté : `ma006` Star
      Flight imprime `[energy]` ; sans le changement, Star-Gaze soignerait
      (l'identité est intacte, donc rien de visible) et l'identité resterait
      **inclinée**. Avec, la branche `[wild]` la **redresse**. La main ne
      contient qu'un seul icône (`ma009` = `[physical]`) : Star Light est donc
      OBLIGÉE de financer le second point du coût, ce que le relevé confirme
      par son inclinaison. Sans le module : **ROUGE**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma005` vue 5/8, financement observé. 0 traceback.
      Résultat : conforme.

**Écart assumé** : voir le tableau des écarts (drapeau plutôt que mutation).

**Carte terminée : OUI.**

### ma006 : * Star Flight (amélioration signature)

Coût 2, `[energy]`, trait SUPERPOWER.

- [x] Étape 2 : cartes de référence : **le bonus continu** → `01065` Heroic
      Intuition (« Your hero gets +1 THW »), écrite
      `*AbilityFactory.GiveKeywordToAttached(Hero, thwart=1)` ; le **trait
      accordé** par la même fabrique → `dt079` Borrowed Gear (`trait=`). **Le
      Hero Interrupt** → `WhenPlayerPlayCard` (`play.py:225`) ; le don de trait
      → `01039` et `30011` (`GainUntilPhaseEnd(effect, trait="AERIAL")`).
      **Aucune capacité « Play » déclarée** : `Upgrade.GetAbilities`
      (`upgrade.py:12-19`) en pose une d'office, qui attache la carte à
      l'identité — comme `wc016` Wiccan's Cloak et `ag008`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **deux choses distinctes dans la même phrase** (un bonus de stat ET un
      trait), les deux codées ; **`Ms. America gets`** → `Hero` et non
      `Identity` : en identité civile le bonus ne s'applique pas ;
      **`WHEN you play`** → `WhenPlayerPlayCard`, qui résout AVANT — c'est
      indispensable, Star-Gaze est un `AfterPlayerPlayedCard` ;
      **`an EVENT card`** → `CardFinder(card_type=Event)` ; **`Hero
      Interrupt`** → sous-type dédié, **sans `.SetLabel(...)`** (la carte
      n'imprime aucun libellé, et `ability.py:196` n'autorise de toute façon
      que 'defense' et 'thwart' — piège payé sur `pt015`) ; **la flèche** est
      un coût.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; **+1** CTR.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **729** contrôle les DEUX moitiés du bonus continu
      (`attributs: {thwart: 1}` ET `traits: ["AERIAL"]`). **730** prouve
      l'interruption : `01087` Haymaker est un événement BASIC `[energy]` SANS
      le trait SUPERPOWER ; sans Star Flight, Star-Gaze ne part pas et
      l'identité garde ses 3 dégâts ; avec, la branche `[energy]` en soigne 1.
      Le relevé contrôle aussi les 3 dégâts de Haymaker sur Rhino (preuve que
      l'événement a bien été **joué** et non simplement défaussé) et
      l'inclinaison, qui est le coût. Sans le module : **ROUGES** tous les deux.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma006` vue 3/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma007 : * Hyper-Cosmic Awareness (amélioration signature)

Coût 2, `[mental]`, trait SUPERPOWER.

- [x] Étape 2 : cartes de référence : **accumuler + dépenser sur la même
      carte** → `mk005` Different Folks (pack `moon_knight`), squelette exact
      (une Response qui pose 1 compteur ici, une capacité qui en dépense N),
      même `Faces.PlaceCountersOn([this], 1, <nom>, effect)`. **L'annulation**
      → `40048` Lucky Break et `mw009` Foresight, toutes deux
      `WhenPlayerRevealCard(<type>, <joueur>, <carte>, "All", fn)` puis
      `message.CancelAllEffectsAndDiscardIt(effect)`. **Le coût double** →
      `06017` (exhaust + 3 compteurs 'glory') et `pt008`, deux `.SetCostFunc`
      chaînés.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`cancel ALL of its effects`** → niveau `"All"` (`reveal.py:41`), leçon
      Dazzler n°5 : l'annulation totale englobe les mots-clés et le **surge** ;
      `"WhenRevealed"` n'aurait annulé que la capacité « Une fois révélée » ;
      **`and remove`** (coût à plusieurs parties) : les DEUX parties sont
      payées, `CostFunc.Exhaust` **et** `CostFunc.Counter` ;
      **`an encounter card is revealed`** sans « you » → `"AnyPlayer"` (voir
      écarts) ; **`Hero Response`** et **`Hero Interrupt`** → sous-types
      dédiés ; **pas de `.SetPlay()` ni de `.SetLabel()`**, contrairement à
      `mw009` qui est un ÉVÉNEMENT joué depuis la main.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; **1** compteur posé ; **4**
      compteurs retirés (`COMPTEURS_POUR_ANNULER`).
      Résultat : conforme.
- [x] Étape 7 : trois cas. **731** (la Response pose exactement 1 compteur, pas
      2, alors que la carte est elle-même SUPERPOWER), **732** (les deux
      moitiés du coût **et** l'annulation : `01107` est une manigance annexe,
      annulée elle n'entre PAS en jeu, ce qui est directement observable),
      **733** (contre-épreuve : à 3 compteurs, la capacité n'est même pas
      proposée — `CostFunc.Counter` filtre lui-même). Sans le module : 731 et
      732 **ROUGES**, 733 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma007` vue 3/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma008 : Energy Infusion (ressource signature)

`desc.RES = "GG"` : **deux icônes `[wild]` imprimées**, relevé par découpe
d'image en planche. Aucun coût : c'est un type `Resource`, elle se dépense.

- [x] Étape 2 : carte de référence : `12006` Pym Particles (pack `ant`), même
      fabrique `AbilityFactory.AfterYouSpendThisCard(AbilityType.HeroResponse,
      …)`, même situation (la carte est DÉJÀ à la défausse quand la Response
      part — la fabrique porte `.NoOutOfPlayLimit()` d'office,
      `resources.py:547`, c'est ce qui la rend atteignable). `dz018` (pack
      `dazzler`) est le même montage avec un filtre de carte payée.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`After you SPEND THIS CARD`** → condition interne `effect.this in
      message.faces` (`resources.py:517`) : la Response ne part que si c'est
      bien CETTE carte qui a payé ; **`to pay for a SUPERPOWER CARD`** →
      kwarg dédié `to_pay_card=CardFinder(trait=…)`, et le mot imprimé est
      « card », donc payer une AMÉLIORATION SUPERPOWER déclenche aussi ;
      **`an ADDITIONAL time`** → on rappelle `ResoudreStarGaze`, la MÊME
      résolution ; **`as the same printed resource as the played event`** → la
      couleur n'est PAS celle d'Energy Infusion (qui serait `[wild]` deux fois)
      mais celle de la carte PAYÉE, Star Light comprise si elle l'a changée ;
      **aucune icône à coder** : `desc.RES = "GG"` est lu nativement, une
      `CanGenerateResources` ici serait une capacité fantôme.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `RES "GG"` (2 icônes) ; **1** résolution
      supplémentaire.
      Résultat : conforme.
- [x] Étape 7 : cas 734. `ma009` imprime `[physical]` : Star-Gaze inflige
      1 dégât et Energy Infusion la rejoue sur la MÊME couleur → **2** dégâts.
      La main ne contient QUE `ma009` et `ma008` : Energy Infusion est donc
      obligée de payer, et ses deux icônes `[wild]` ne dictent PAS la branche
      (sinon Ms. America serait redressée au lieu de frapper). Sans le module :
      **ROUGE** (1 dégât).
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma008` vue 3/8, dépensée comme ressource dans le
      journal 2. 0 traceback.
      Résultat : conforme.

**Écart de vocabulaire de l'auteur, non corrigé** : voir le tableau des écarts.

**Carte terminée : OUI.**

### ma009 / ma010 : America's Anger (événement signature, ×2)

Coût 1, `[physical]`, traits SKILL + SUPERPOWER. `ma010` est le doublon de code
de `ma009`.

- [x] Étape 2 : cartes de référence : le coût → `CostFunc.Ready`
      (`cost_func.py:327-356`), qui pose `canbe_ready=True` sur son sélecteur ;
      le déclenchement du doublement → `AbilityFactory.WhenUnitUseBasicPower`
      (`friend.py:339-370`) puis `message.GainValue(n, effect)`
      (`sender_unit.py:21-34`), qui route vers `GainTHWForThisThwart` ou
      `GainATKForThisAttack` selon le pouvoir — la brique exacte du moteur pour
      « cette utilisation-ci vaut N de plus » ; la durée →
      `RegisterTemp(…, unregister_after_exec=True, until_turn_end=True)`
      (`face_effect.py:97-124`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **la flèche** est un coût, arbitrage EXPLICITE de l'utilisateur (voir
      plus haut) ; **`double all MODIFIERS`** et non la valeur de base : on
      AJOUTE une seconde fois le total des modificateurs, puisque la valeur
      courante en contient déjà un exemplaire — CTR 1 imprimée + Star Flight
      (+1) = 1 + (1 × 2) = **3**, jamais 4 ; **`on its NEXT use`** →
      `unregister_after_exec=True` (la capacité part à la première
      utilisation) ; **`THIS TURN`** → `until_turn_end=True` (elle expire si le
      pouvoir n'est pas utilisé) — les DEUX bornes sont écrites, pas une seule ;
      **`Hero Action`** sans libellé imprimé → `.SetPlay()` sans `.SetLabel()`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 1 ; **×2** sur les modificateurs ;
      aucune autre valeur.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **735** : `01057` Combat Training donne +1 ATQ
      (Ms. America passe de 2 à 3) ; après la carte, l'attaque suivante vaut
      2 + (1 × 2) = **4**, plus le dégât de Star-Gaze `[physical]` = **5** sur
      Rhino. Il exige DEUX clés du harnais : `preferer_option` (le pilote prend
      toujours la première branche, ici CTR) et `declencher_apres` (attaquer
      APRÈS le jeu de la carte). **736** est la contre-épreuve de l'arbitrage :
      identité déjà prête, la carte reste en main et Rhino ne prend rien. Sans
      le module : 735 **ROUGE**, 736 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma009` 3/8, `ma010` 7/8 ; le cycle complet
      (coût-flèche → jeu → Star-Gaze) est lu ligne à ligne plus haut, et le
      journal de round montre bien
      `Double_all_modifiers_applied_to_your_THW_on_its_next_use`. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI** (`ma009` et `ma010`).

### ma011 / ma012 : Bulletproof Chica (événement signature, ×2)

Coût 1, `[mental]`, traits DEFENSE + SUPERPOWER. `ma012` est le doublon de code
de `ma011`.

- [x] Étape 2 : carte de référence : `rg004` Shield Block (pack
      `red_guardian`) et son original officiel `03005` (Captain America), même
      phrase imprimée « When you would take ANY AMOUNT OF DAMAGE, prevent all
      of that damage », même montage `WhenUnitWouldTakeDamage(<type>, "You",
      fn).SetPlay().SetLabel('defense')` + `message.PreventDamage("All",
      effect)` (`sender_damage.py:808-820`). Le statut → `hd011` et `38008`
      (`Faces.GiveStatus([identite], "Tough", effect)`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`ANY AMOUNT OF DAMAGE`** → **AUCUN `is_from_attack=`**. Le texte ne
      restreint PAS aux dégâts d'une attaque, contrairement à Backflip
      (`01003`) et `dz010`, qui disent « from an attack » et portent
      `is_from_attack=True`. Une traîtrise, un dégât consécutif ou un dégât
      direct sont prévenus tout autant. Le commentaire de `rg004` formule déjà
      cette lecture mot pour mot ; **deux CONSÉQUENCES sans flèche** : la
      prévention ET le statut partent toujours ensemble ; **`your
      IDENTITY`** → `player.GetIdentity()`, pas `"YourHero"` ; **`Tough`** avec
      la majuscule (`CardFace.STATUS`, `card_face.py:221`) ; **le libellé
      `(defense)`** est LÉGAL sur une interruption (`ability.py:196`) —
      c'est `attack` qui fait planter le montage ; **`.SetPlay()` AVANT
      `.SetLabel()`** (`assert self.selectors == []`, `ability.py:486`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 1 ; **tous** les dégâts prévenus
      (`"All"`) ; **1** carte de statut Robuste.
      Résultat : conforme.
- [x] Étape 7 : cas 737, qui contrôle les TROIS faits (0 dégât, statut Robuste,
      carte défaussée donc réellement jouée). Sans le module : **ROUGE**.
      ⚠ Piège de banc payé ici : avec `defender='ma001a'`, la DEF 2 ramenait
      l'attaque de Rhino à 0 dégât et l'interruption n'était jamais proposée.
      L'identité est donc **inclinée** pour ne pas défendre.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma011` 6/8, `ma012` 3/8 ; prévention observée en
      partie réelle (lecture ligne à ligne plus haut). 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI** (`ma011` et `ma012`).

### ma013 / ma014 : Star Portal (événement signature, ×2)

Coût 2, `[wild]`, trait SUPERPOWER. `ma014` est le doublon de code de `ma013`.

- [x] Étape 2 : cartes de référence : « n'importe quel joueur » comme cible →
      `01092` Helicarrier et `51014` Manifold (`.SetTarget("Players")` puis
      `effect.targets[0].GetControlByPlayer()`) ; « poser en jeu **incliné**
      chez un autre joueur » → `50088b` (pack `aos`), **seule carte du dépôt**
      qui emploie `PutIntoPlay(…, under_control=True, exhaust=True)`
      (`face_on_event.py:170` et 189-202) ; le choix d'un allié parmi une liste
      → `dt079` Borrowed Gear (`MayChooseOneText`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`ANY PLAYER'S`** deux fois, ni « your » ni « you control » : on ne
      restreint rien (en solo la différence est nulle, en multijoueur elle est
      majeure) ; **`EXHAUSTED`** → `exhaust=True`, le point le plus facile à
      rater, contrôlé par le cas ; **`that ally's THW`** / **`that ally's
      ATK`** → valeurs COURANTES, lues APRÈS l'entrée en jeu, et c'est bien LE
      MÊME allié dans les deux moitiés (mot-piège `that <nom>`) ; **`and`**
      relie deux CONSÉQUENCES, sans flèche : les deux se résolvent toujours ;
      **la flèche** est un coût, rendu par une `conditions=` (voir écarts) ;
      **`Hero Action`** sans libellé imprimé.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; aucune valeur en dur (menace et
      dégâts viennent de l'allié).
      Résultat : conforme.
- [x] Étape 7 : deux cas. **738** : `01059` Jessica Jones imprime CTR 1* et
      ATQ 2* → 1 menace retirée et 2 dégâts, l'allié arrive **incliné**.
      **739** : contre-épreuve, aucun allié dans aucune défausse → la carte
      reste en main et la menace ne bouge pas. Sans le module : 738 **ROUGE**,
      739 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma013` 7/8, `ma014` 2/8 ; le journal 2 montre
      `01058 Daredevil` remonté de la défausse et mis en jeu par Star Portal,
      suivi des 2 dégâts sur Rhino. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI** (`ma013` et `ma014`).

### ma015 / ma016 : Break Through (événement signature, ×2)

Coût 2, `[energy]`, traits ATTACK + SUPERPOWER + THWART. `ma016` est le doublon
de code de `ma015`.

- [x] Étape 2 : cartes de référence : le **double libellé** → `dt028` Pay It
      Forward, `dt095`, `dt115`, `60050` In Harm's Way, `60055`, tous en
      `.SetLabel('attack', 'thwart')` (`Ability.SetLabel` est variadique,
      `ability.py:375-382`) ; **« si cela met K.O. »** → deux briques
      distinctes, `DealDamage(…, if_this_attack_defeats=fn)`
      (`card_face.py:558-563`, modèles `ag006`, `ab004`, `50037`) et
      `RemoveThreatFromSchemes(…, if_this_remove_last_threat=fn)`
      (`card_face.py:692`, modèles `56009` Feline Senses, `37009`, `56039`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`defeated` vs `damaged`** : c'est bien la DÉFAITE ; **`an enemy OR
      scheme`** : deux déclencheurs, les deux codés ; **`AN enemy`** au
      singulier → un DRAPEAU local garantit que le bonus ne part **qu'une
      fois** même si les deux défaites arrivent (deux résolutions seraient plus
      permissives) ; **`stun OR confuse`** → choix du joueur entre deux
      `ForChoiceAbility`, avec `canbe_stunned` / `canbe_confused` pour filtrer
      les cibles ; les deux premières phrases sont deux **conséquences**
      séparées par un point, sans flèche ; **`.SetPlay()` AVANT `.SetLabel()`**
      (`assert self.selectors == []`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; **4** dégâts ; **3** menaces.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **740** : la menace est posée à **3** exactement, les
      3 retirées enlèvent la DERNIÈRE, `if_this_remove_last_threat` part, Rhino
      est Étourdi. **741** : contre-épreuve à 5 menaces — il en reste 2, Rhino
      (14 PV) survit à 4 dégâts, et le vérificateur sur mesure
      `ma015_aucun_etourdi` contrôle qu'**aucun statut** n'a été posé (la
      troisième phrase est CONDITIONNELLE : sans ce témoin, un Étourdi
      inconditionnel passerait). Sans le module : **ROUGES tous les deux**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma015` 2/8, `ma016` 2/8 ; le journal 2 montre les
      4 dégâts, les 3 menaces retirées et `Rhino gained Stunned` par
      Break Through. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI** (`ma015` et `ma016`).

### ma017 : Edges Syndrome (obligation)

`desc.Boost = "1"`, `desc.GiveTo = "America Chavez"`.

- [x] Étape 2 : carte de référence : `04166` Anti-Hero Propaganda — même
      famille exacte (une obligation qui RESTE EN JEU, impose un malus continu
      aux pouvoirs de base et offre une Action pour s'en débarrasser),
      `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero, thwart=-1,
      attack=-1, defense=-1)` +
      `PlayerActionToDiscardThis(…).SetCostFunc(CostFunc.TakeDamage(2,
      "YourIdentity"))`. `28021` Weight of the World confirme qu'une obligation
      reste en jeu quand elle porte un effet continu, et fournit le modèle de
      `PlayerActionToRemoveThisFromGame`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`your IDENTITY`** et non « your hero » → filtre `Identity`, le malus
      vaut sur LES DEUX faces (`04166` dit « your HERO gets » et emploie
      `Hero` : deux textes différents, on ne recopie pas) ; **`EACH of its
      basic powers`** → les quatre, ATQ/CTR/DEF/REC ; `unit.Gain` n'applique un
      attribut que si la face le POSSÈDE (`face_gain.py:120-125`), donc la face
      héros perd ATQ/CTR/DEF et la face civile perd REC, rien à trier ;
      **`YOUR identity`** → `control_by="You"`
      (`environment_helper.py:177-179`), sans quoi le malus frapperait TOUTES
      les identités en jeu en multijoueur — `04166` ne le pose pas, on ne
      recopie pas son omission ; **`Action` nu** et non « Alter-Ego Action » →
      `AbilityType.Action`, disponible dans les deux formes ; **les deux
      flèches** sont des coûts ; **`Boost`** lu nativement, aucune capacité
      fantôme.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `Boost 1` ; **-1** à chaque pouvoir ;
      **2** dégâts pour défausser ; **4** dégâts pour retirer du jeu.
      Résultat : conforme.
- [x] Étape 7 : trois cas. **742** (les trois pouvoirs de la face héros d'un
      coup), **743** (Action 1 : 2 dégâts ET la carte part), **744** (Action 2 :
      branche inatteignable sans le 3ᵉ argument de `Puzzle.Action`, avec un
      vérificateur sur mesure `ma017_retiree_du_jeu` qui distingue « retirée du
      jeu » de « défaussée », ce qu'`etat_attendu` ne sait pas faire). Sans le
      module : **ROUGES tous les trois**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma017` vue 7/8, mise en jeu et subie. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma018 : * Catalina Chavez (sbire némésis)

PV 4, ATQ 1*, MNG 1*, `Boost 2`, `Quickstrike 1`, `Nemesis "America Chavez"`,
trait STARLING.

- [x] Étape 2 : carte de référence : `08026` Taskmaster (pack `bkw`), sbire
      NÉMÉSIS lui aussi, dont le texte imprimé est « Taskmaster gets +1 ATK and
      +1 SCH for each upgrade in your play area » et qui s'écrit
      `ThisGainKeyword(lambda …: len(effect.this.CastTo(Minion)
      .GetEngagedPlayer().GetControlUpgrade()), scheme=1, attack=1,
      change_on_event=OnEvent.PlayAreaCard("YouControlCards"))`. Même fabrique,
      même déclencheur de réévaluation, même lecture de « ta zone de jeu ».
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Quickstrike`, `Boost`, `Nemesis`** lus NATIVEMENT dans `desc` (fiche
      `mots-cles/quickstrike.md`) : coder l'attaque d'engagement à la main
      serait une capacité fantôme ; **`each stat modifier`** → arbitrage de
      l'utilisateur, lecture littérale (voir plus haut) ; **`in YOUR play
      area`** → `GetEngagedPlayer()`, avec garde si le sbire n'est engagé avec
      personne ; **`(replacing THW with SCH)`** → **deux** `ThisGainKeyword`
      distincts (Taskmaster ajoute la MÊME valeur aux deux stats, Catalina non
      : son ATQ suit les modificateurs d'ATQ et son MNG ceux de CTR), et la
      conversion est nécessaire — un sbire n'a pas de CTR, `unit.Gain(thwart=…)`
      ne s'applique que si `HasThwart.IsType` et le bonus serait silencieusement
      perdu ; **`HP: "4"` sans étoile** (voir arbitrages).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 4, ATQ 1*, MNG 1*, `Boost 2`,
      `Quickstrike 1` (lus nativement) ; aucune valeur en dur.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **745** : `01057` Combat Training (+1 ATQ) et `ma006`
      Star Flight (+1 CTR) sont posés ; Catalina doit gagner **+1 ATQ et
      +1 MNG**, pas +1 CTR. **746** : contre-épreuve, zone de jeu vide, ATQ et
      MNG restent imprimés — il reste vert sans le module, c'est le couple qui
      prouve que la capacité lit vraiment la zone de jeu et n'ajoute pas un
      bonus fixe. Sans le module : 745 **ROUGE**, 746 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma018` vue 2/8. 0 traceback.
      Résultat : conforme.

**Conséquence en jeu, assumée** : Star Flight (+1 CTR à Ms. America) donne
+1 MNG à sa sœur, et Edges Syndrome (-1 à chaque pouvoir de base) lui donne
-1 ATQ et -1 MNG. Les deux sens comptent.

**Carte terminée : OUI.**

### ma019 : Search for the Cure (manigance annexe némésis)

Carte PAYSAGE. `Boost 3`, `Hazard 1`. **Aucune** menace de départ imprimée dans
`desc` : elle est calculée.

- [x] Étape 2 : cartes de référence : **la menace câblée** → `mw018` The Grim
      Hunt et `wc019a` New Vessel, mêmes écarts assumés, même commentaire.
      **« each player searches their discard pile »** → `59022` (pack
      `hercules`) et `lj027`, tous deux une boucle sur `Worlds.GetPlayers` avec
      un `Search.PlayerCard(…, may=True)` par joueur — seul montage possible,
      `Search.PlayerCard` n'ayant pas d'option « n'importe quel joueur »
      (`search_internal.py:77`). **L'attachement face visible** → `04003`
      Hawkeye's Quiver (`PlaceCardHere(face, True, effect)`). **Le coût
      cumulé** → `FacesCounter.GetPrintedCost` (`faces_counter.py:109-114`,
      modèles `42025`, `50006`, `50119`). **`2[per_hero]`** →
      `Worlds.ConvertPerPlayerIconToInt` (`worlds.py:666-670`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`Hazard`** lu NATIVEMENT (fiche `mots-cles/hazard.md`), icône vérifiée
      par découpe — aucun module pour lui ; **`SideScheme` en JSON =
      `EncounterSideScheme` dans le script** (piège du GUIDE §10) ;
      **`EACH player`** et **`THEIR discard pile`** → une boucle, chacun
      fouillant SA pile ; **`FACEDOWN` absent** : la carte ne le dit pas,
      contrairement à `ma004` — et il FAUT qu'elle soit visible, on lit son
      coût juste après ; **`did not attach`** → on compte les JOUEURS qui n'ont
      rien posé (un joueur sans allié et un joueur qui refuse comptent pareil) ;
      **`an ADDITIONAL 2[per_hero]`** → s'ajoute au coût cumulé, il ne le
      remplace pas.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `Boost 3`, `Hazard 1` (lus nativement) ;
      **2**`[per_hero]` par joueur sans allié. En solo : 2 × 1 = 2. À quatre
      joueurs, si personne ne pose d'allié : 4 × (2 × 4) = 32.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **747** : `01059` coûte 3 → **3** menaces, et PAS le
      repli à 2 — vérificateur sur mesure `ma019_allie_attache_et_menace`, qui
      contrôle aussi que l'allié est bien attaché. `accepter_choix` y est
      indispensable : la recherche est un `may`, et le pilote décline par
      défaut. **748** : la défausse ne contient qu'une ressource, aucun allié à
      attacher → le repli s'applique, 2 menaces. Sans le module : **ROUGES
      tous les deux**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma019` vue 2/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma020 / ma021 : Star Lightning (traîtrise némésis, ×2)

`Boost 2`, trait SUPERPOWER. `ma021` est le doublon de code de `ma020`.

- [x] Étape 2 : carte de référence : `pt021` Bulldozing Charge (pack
      `patriot`), même structure imprimée (« <sbire némésis> attacks you. If no
      attack was made this way, … ») et même brique de moteur
      (`Worlds.FindCardOnField` puis `enemy.DoAttackYou(player, effect, …)`,
      sinon le repli directement). Originaux officiels : `02040` Tail Sweep et
      `22031` Old Rivals. La clause « deals damage » →
      `if_this_attack_deals_damage=` (`enemy.py:80`), crochet dédié du moteur.
      Le surge conditionnel → `ThisCardGainSurge`
      (`cards/pack/__init__.py:100`), idiome de `il021`, `il022`, `22031`,
      `pt017`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`ATTACKS YOU`** → `message.GetToPlayer()` ; **`If this attack DEALS
      DAMAGE`** (mot-piège `defeated` vs `damaged`) : ce n'est ni « vainc », ni
      « if undefended » — une attaque bloquée qui passe quand même 1 dégât
      étourdit ; **`your IDENTITY`** → `player.GetIdentity()` ; **`If NO ATTACK
      IS MADE this way`** → `if_no_attack_was_made=`, et le repli part AUSSI
      quand Catalina n'est pas en jeu du tout (cas nominal, traité par un
      `else`) ; **les deux clauses s'excluent** : soit l'attaque a lieu, soit
      elle n'a pas lieu, aucun cas ne déclenche les deux ; **`Boost`** lu
      nativement.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : `Boost 2` (lu nativement) ; aucune autre
      valeur (le surge est **gagné**, pas imprimé : `desc.Surge` est
      volontairement absent).
      Résultat : conforme.
- [x] Étape 7 : deux cas, tous deux avec un vérificateur sur mesure. **749** :
      l'identité est inclinée pour qu'elle ne défende pas (seul moyen fiable de
      faire arriver une attaque jusqu'à elle, GUIDE §8) ; on contrôle les
      dégâts ET le statut, parce que la clause est « if this attack DEALS
      DAMAGE ». **750** : contre-épreuve, Catalina absente, ni dégât ni Sonné.
      Sans le module : 749 **ROUGE**, 750 vert.
      Résultat : conforme, avec une limite déclarée (le surge).
- [x] Étape 8 : autoplay : `ma020` 2/8, `ma021` 2/8. 0 traceback.
      Résultat : conforme.

**Limite du harnais, déclarée** : la bascule du surge n'est pas observable de
façon déterministe. Voir « limites du harnais » n°1.

**Carte terminée : OUI** (`ma020` et `ma021`).

### ma022 : * Gwenpool (Gwendolyn Poole, allié Agression)

Coût 3, PV 3, ATQ 1*, CTR 1*, `[wild]`, trait AVENGER.

- [x] Étape 2 : carte de référence : `08026` Taskmaster, même montage exact
      pour « X pour chaque carte de ta zone de jeu »,
      `ThisGainKeyword(<compte>, attack=1,
      change_on_event=OnEvent.PlayAreaCard("YouControlCards"))` ; `dt065`
      Colleen Wing et `12013` Ronin emploient la même fabrique avec un autre
      déclencheur de réévaluation. La classe `IdentitySpecific` :
      `59026` Ancient Rivalry (`CardFinder(card_type=Upgrade,
      card_class='IdentitySpecific')`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`IDENTITY-SPECIFIC upgrade`** → `card_class='IdentitySpecific'`, classe
      de carte à part entière du moteur (`card_player.py:33-41` et 69) donnée à
      toute carte joueur dont le `desc.Class` vaut « Hero ». Ce n'est PAS « une
      amélioration quelconque », ni « une amélioration attachée à ton
      identité » : une amélioration signature posée sur un ALLIÉ compte tout
      autant ; **`YOU CONTROL`** → `player.GetControlUpgrade(finder)`, la zone
      de jeu du CONTRÔLEUR de Gwenpool ; **`to a MAXIMUM of +2 ATK`** →
      `min(BONUS_ATK_MAX_GWENPOOL, …)`, sans quoi un deck signature bien posé
      donnerait +4.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3, PV 3, ATQ 1*, CTR 1* (lus
      nativement) ; **+1** par amélioration ; plafond **+2**.
      Résultat : conforme.
- [x] Étape 7 : cas 751, qui pose **trois** améliorations signature (`ma005`,
      `ma006`, `ma007`) : le plafond doit ramener le bonus à +2. Sans le
      module : **ROUGE**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : **0/8**, et c'est attendu — la carte est AGRESSION,
      donc absente du deck de départ Justice par construction
      (`metadata.cartes_du_pack_note`). Le cas 751 la couvre. 0 traceback.
      Résultat : conforme, avec la couverture d'autoplay expliquée.

**Collision de noms documentée** : le jeu contient déjà un pack complet
`gwenpool` (préfixe `gp`). Rien n'est corrigé côté `gp`, et `ma022` ne fait
aucune recherche par nom.

**Carte terminée : OUI.**

### ma023 : * Marvel Boy (Noh-Varr, allié Basic)

Coût 3, PV 3, ATQ 2*, CTR 1*, `[energy]`, traits KREE + YOUNG AVENGER.

- [x] Étape 2 : cartes de référence : le déclencheur → `30021` SP//dr, même
      `WhenUnitBeDefeated(AbilityType.…, "This", …, by_consequential=True)` ;
      l'effet → `31022` Spider-Man (Otto), dont le texte imprimé dit « ready an
      upgrade you control » et qui s'écrit `Faces.ReadyAll(effect.targets,
      effect)` avec `.SetTarget(Upgrade, canbe_ready=True,
      from_where=["YouControlCards"])` — la ligne exacte.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`IS defeated`** et non « would be defeated » : rien n'est remplacé,
      l'allié meurt. On emploie donc `WhenUnitBeDefeated`
      (`defeated.py:110-122`) et surtout **PAS** de `SetBeInstead` — comparer
      avec `ma003`, qui dit bien « would be » ; **`CONSEQUENTIAL damage`** →
      `by_consequential=True` ; **`an upgrade YOU CONTROL`** →
      `from_where=["YouControlCards"]` et `canbe_ready=True`, qui écarte les
      améliorations déjà prêtes (sans amélioration inclinée, la capacité n'a
      aucune cible légale et ne se déclenche pas) ; **`Interrupt` nu**, sans
      libellé.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3, PV 3, ATQ 2*, CTR 1* (lus
      nativement) ; **1** amélioration redressée.
      Résultat : conforme.
- [x] Étape 7 : cas 752. Star Light est inclinée au départ (sinon `canbe_ready`
      l'écarte), Marvel Boy est amené à 1 PV pour que son unique dégât
      consécutif le tue. Sans le module : **ROUGE**.
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma023` vue 4/8. 0 traceback.
      Résultat : conforme.

**Carte terminée : OUI.**

### ma024 : * Noh-Varr's Ship (soutien Basic)

Coût 3, `[energy]`, traits KREE + VEHICLE + YOUNG AVENGER.

- [x] Étape 2 : cartes de référence : la condition de jeu →
      `AbilityFactory.CanPlayThisSupportCard().SetPlay(
      only_if_your_identity_has_trait=…)`, kwarg dédié de `Ability.SetPlay`
      (`ability.py:596-629`), modèles `12014` (`"AVENGER"`) et `45042`
      (`"X-MEN"`) ; `53020` Flight Squadron montre le même couple sur un
      SOUTIEN. La capacité Resource → `kb013` Kate's Quiver, même phrase
      imprimée.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`your IDENTITY`** et non « your hero » : le kwarg
      `only_if_your_hero_has_trait` existe aussi et exigerait la forme héros,
      ce que le texte ne dit pas ; **`Resource` NU** (ni « Hero », ni
      « Alter-Ego ») → `AbilityType.Resource`, la carte finance dans les deux
      formes ; **la flèche** est un coût ; **une seule
      `CanGenerateResources`** par carte (assert `card_player.py:50`) ;
      **`.SetPlay(...)` AVANT tout `.SetTarget`** (`assert self.selectors ==
      []`, `ability.py:486`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3 ; **1** ressource `[wild]`.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **753** : la main ne contient qu'un seul icône
      (`ma009` = `[physical]`) pour un coût de 2 — le vaisseau est OBLIGÉ de
      fournir le second, et le relevé contrôle son inclinaison. **754** :
      contre-épreuve montée avec un AUTRE héros, `okoye`, qui n'est pas YOUNG
      AVENGER : la carte reste en main. Sans le module : **ROUGES tous les
      deux** (sans `ma024.py`, le moteur pose une capacité de jeu par défaut
      sur le Soutien et la condition disparaît).
      Résultat : conforme.
- [x] Étape 8 : autoplay : `ma024` vue 1/8, financement observé ligne 74 du
      journal 2. 0 traceback.
      Résultat : conforme.

**Vraie synergie inter-packs** : six identités custom portent YOUNG AVENGER
(Wiccan, Speed, Iron Lad, Patriot, Kate Bishop, Ms. America). C'est le seul
soutien BASIC du catalogue réservé à cette équipe.

**Carte terminée : OUI.**

### ma025 : Power Stomp (événement Agression)

Coût 2, `[physical]`, traits ATTACK + SUPERPOWER.

- [x] Étape 2 : cartes de référence : la **condition sur une valeur courante**
      → `dt012` Gone in a Flash, qui compare des PV courants dans une
      `conditions=` et enchaîne sur `.SetPlay()` — **aucun kwarg de
      `Ability.SetPlay` ne sait exprimer un seuil d'attribut courant**, le seul
      voisin (`only_if_your_identity_has_at_least_printed_hp`) porte sur des PV
      IMPRIMÉS. **« le vilain et chaque sbire engagé »** → `01046` Energy
      Daggers (officielle), `01158` et `lj010`, tous montés sur
      `Worlds.FindVillain(effect)` + `player.GetEngagedMinions()` réunis dans
      une seule liste : le moteur n'expose **aucune** notion d'engagement pour
      le vilain.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés :
      **`at least 3 ATK`** : valeur COURANTE, `hero.attack` (property,
      `can_attack.py:56-60`) ; **`GetHero()` lève un `assert False` en forme
      alter-ego** (`player_get.py:203`) → on passe par `GetIdentity()` +
      `Hero.IsType(...)` ; **`engaged with YOU`** → les sbires du joueur qui
      joue la carte, jamais ceux des autres ; **`X equals YOUR ATK`** → lu au
      moment de la résolution ; **`Hero Action (attack)`** →
      `.SetPlay().SetLabel('attack')`.
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2 ; seuil **3** ATQ
      (`ATK_MINIMUM_POWER_STOMP`) ; X = ATQ, aucune valeur en dur.
      Résultat : conforme.
- [x] Étape 7 : deux cas. **755** : `01057` Combat Training porte Ms. America à
      ATQ 3, ce qui rend la carte jouable ET fixe X ; `01103` Shocker (3 PV)
      est engagé, il tombe exactement, et Rhino encaisse 3 + 1 (Star-Gaze
      `[physical]`, la carte étant SUPERPOWER) = 4. **756** : contre-épreuve à
      ATQ 2, la carte reste en main. Sans le module : 755 **ROUGE**, 756 vert.
      Résultat : conforme.
- [x] Étape 8 : autoplay : **0/8**, attendu — la carte est AGRESSION, absente
      du deck de départ Justice par construction. Les cas 755 et 756 la
      couvrent. 0 traceback.
      Résultat : conforme, avec la couverture d'autoplay expliquée.

**Carte terminée : OUI.**

### ma026 : re-skin de `12030` Moment of Triumph — `full_link`

Réimpression `{"card_id": "ma026", "full_link": "12030"}`. **Aucun module,
aucun cas de test** : le moteur résout la carte liée, qui a déjà les siens.
Vérifié : même coût, même ressource, même aspect (AGRESSION), même texte, et
`CardStatistics.createCardObjects` recopie le champ `custom` depuis la carte
source (GUIDE §14). Elle se construit (`test_cards` : 4895 ok / 0 err) et le
catalogue l'accepte (`verifier_prefixes`, `verifier_desc_mots_cles`,
`verifier_cartes_en_jeu` propres sur les **30** cartes).

⚠ Elle est AGRESSION : elle n'est pas dans le deck de départ Justice, par
construction. **Carte terminée : OUI.**

### ma027 : re-skin de `01088` Energy — `full_link`

Réimpression `{"card_id": "ma027", "full_link": "01088"}`. Aucun module, aucun
cas. La ressource `RES "YY"` et la clé `MaxPerDeck 1` sont héritées de la carte
source. **On met la RE-SKIN et jamais l'originale** : `full_link` clone le nom
et la limite par nom, donc avoir les deux violerait `MaxPerDeck`
(`metadata.reskins_note` du deck). Vue 2/8 en autoplay. **Carte terminée : OUI.**

### ma028 : re-skin de `01089` Genius — `full_link`

Réimpression `{"card_id": "ma028", "full_link": "01089"}`. Aucun module, aucun
cas. Même remarque `MaxPerDeck` que `ma027`. Vue 5/8 en autoplay.
**Carte terminée : OUI.**

### ma029 : re-skin de `01090` Strength — `full_link`

Réimpression `{"card_id": "ma029", "full_link": "01090"}`. Aucun module, aucun
cas. Même remarque `MaxPerDeck` que `ma027`. Vue 4/8 en autoplay, dépensée
comme ressource ligne 536 du journal 2. **Carte terminée : OUI.**

---

## Gate finale (PROCESSUS-HEROS)

- [x] **Étapes 1 à 8 complètes** : `cards.json` (30 cartes), scripts
      (**26 modules + 3 `__init__.py`**), deck de départ,
      `data/nemesis/ms_america_nemesis.json`, `data/sets_info.json` (137),
      `tools/prefixes_fanmade.json`, 30 images (+ recette
      `tools/importer_images_ms_america.py`), **biographie** (`ma001a` dans
      `public/js/prepare/heros-info.js`), **texte français** (30 entrées dans
      `ui-app/src/board/textes-fr-fanmade.ts`), **règle de deck-building**
      (`public/js/deckbuilder/app.js`, `exemptDeLaLimiteAspect`, 3ᵉ cas).
- [x] **Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour chaque
      carte du pack** : `ma001a`, `ma001b`, `ma002`, `ma003`, `ma004`, `ma005`,
      `ma006`, `ma007`, `ma008`, `ma009`, `ma010`, `ma011`, `ma012`, `ma013`,
      `ma014`, `ma015`, `ma016`, `ma017`, `ma018`, `ma019`, `ma020`, `ma021`,
      `ma022`, `ma023`, `ma024`, `ma025`, `ma026`, `ma027`, `ma028`, `ma029` —
      **30/30**.
- [ ] **Une partie complète jouée avec le héros** : **NON**, et ce n'est pas
      une omission qu'on peut combler ici. Une partie humaine dans le
      navigateur demande d'ouvrir `http://127.0.0.1:2345/`, de cliquer et de
      juger. **Elle n'a pas été jouée.** Ce qui a été fait à la place :
      8 parties d'autoplay complètes (0 bloquée, 0 traceback, 27/30 cartes vues
      en jeu, les 3 manquantes étant Agression donc hors deck Justice),
      41 cas de comportement verts avec preuve rouge/vert module par module, et
      le montage de partie vérifié (`ok: true`).

**Ce que ces outils ne peuvent pas voir** — à vérifier lors de la première
partie humaine, précisément :

1. **Les tooltips français.** Les 30 entrées sont écrites, mais rien
   n'apparaît dans le jeu tant que **`ui-app/deployer.sh` n'a pas tourné**
   (§11.1 du guide). ⚠ Attention au piège du §10 : `deployer.sh` recopie
   `public/js` **depuis le vestige WSL vers la copie Windows avec
   `--delete`**, et écrase donc `public/js/prepare/` — c'est-à-dire la
   biographie `ma001a` et la règle de deck-building qui viennent d'être
   écrites. **Vérifier `js/prepare/` après tout déploiement.** Le déploiement
   n'a volontairement pas été lancé ici, comme pour `patriot`.
2. **La biographie au survol.** L'entrée `ma001a` est en place et le module se
   charge (contrôlé hors navigateur), mais la preuve exigée par
   PROCESSUS-HEROS étape 7 est un **survol dans le wizard** : elle n'a pas été
   faite.
3. **La règle de deck-building en situation.** La fonction a été chargée
   directement et testée sur le catalogue (résultats plus haut), mais aucun
   deck n'a été construit dans le navigateur.
4. **« Est-ce que le pack est agréable ? »** Star-Gaze demande d'enchaîner des
   cartes SUPERPOWER et de choisir sa couleur : c'est un rythme qui ne se juge
   qu'à la main.

## Questions ouvertes

**Aucune.** Les trois points qui auraient pu en être (la flèche de `ma009`, la
lecture de « each stat modifier » sur `ma018`, l'icône de `ma019`) ont été
tranchés par l'utilisateur le 30/08/2026 et sont documentés plus haut. Les
autres choix listés dans « écarts assumés » sont **techniques** : ils se
documentent, ils ne se discutent pas (PROCESSUS-CARTE §3).
