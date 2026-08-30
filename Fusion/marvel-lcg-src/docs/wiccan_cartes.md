# Pack Wiccan — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md`. **25 card_id** au
total (`wc001a` à `wc023`, les faces `a`/`b` de Wiccan et de New Vessel comptant
chacune pour deux identifiants distincts). Source : pack fan-made **CptScorp**
(« Marvel Champions Custom Project », Cycle 2) — même auteur qu'`iron_lad` et
`scarlet_spider`. 2 faces héros, 15 cartes signature, 1 Team-Up de classe Basic,
1 obligation et 6 cartes némésis (dont le verso de New Vessel). Set 129, préfixe
`wc`. Personnage : Billy Kaplan, sorcier adolescent des Young Avengers.

Les étapes 1 et 3-6 de PROCESSUS-HEROS (cards.json, deck de départ, nemesis
json, sets_info.json, préfixe déclaré, traits `YOUNG AVENGER` / `KREE` /
`FAMILY` / `WIZARD` ajoutés au moteur, images) ont été faites lors d'une session
antérieure et validées par l'utilisateur. Cette session a couvert l'étape 2
(scripts) et les étapes 7 à 10 (biographie, texte FR, validation carte par
carte, autoplay, gate finale), plus **une correction de données** rendue
obligatoire par le moteur (voir bug n°1).

## Mécanique centrale

Tout le kit **compte les icônes de bonus de la carte du dessus du deck de
rencontre**. Wiccan joue même avec cette carte **face visible**
(« Clairvoyance », imprimée sur ses DEUX faces).

Neuf cartes en dépendent : `wc002` Hulkling, `wc003`/`wc004` Impenetrable
Barrier, `wc005`/`wc006`/`wc007` Magic Bolt, `wc008` Magic Manipulation,
`wc009`/`wc010` Magic Portal, `wc011`/`wc012` Teleport, `wc014` Warping Reality.
`wc016` Wiccan's Cloak les rejoue ; `wc018` Avoiding the Demiurge les éteint
toutes d'un coup.

Deux briques du moteur suffisent, réunies dans le helper unique
`IconesBoostDuDessus` (`src/cards/pack/wiccan/wiccan/__init__.py`) :

| Besoin | Brique |
|---|---|
| regarder le dessus du deck de rencontre sans y toucher | `player.LookAtDeck("EncounterDeck", 1, effect)` (`player_action.py:945`) |
| compter les icônes | `FacesCounter.CountTotalBoostIcons(faces)` (`faces_counter.py:142`) |
| jouer avec cette carte face visible | `AbilityFactory.PlayWithTopCardOfDeckFaceup(..., only_during_player_phase=True)` (`factory/deck.py:84`) |

Précédents du dépôt, tous relus avant d'écrire une ligne :
`drs/doctor_strange/09003.py` (Astral Projection, base fixe + icônes),
`agent_13/agent_13/ag004.py` (Infiltrate, avec la distinction REGARDER /
DÉFAUSSER), `scw/scarlet_witch/15004.py` (Hex Bolt, paliers d'icônes),
`gambit/gambit/37001b.py` (Remy LeBeau, « regarder 2, défausser 1 ») et
`falcon/falcon/53001a.py` (Falcon, la seule autre carte du dépôt qui imprime
« play with the top card of the encounter deck face up »).

**L'interrupteur de l'obligation** (`wc018`) est un drapeau nommé sur
`effect.world` (`_wiccan_boosts_eteints`), levé par `EteindreLesBoosts` et
rabaissé par une capacité temporaire `WhenPlayerPhaseEnd` posée sur
**l'identité** — jamais sur l'obligation, qui part à la défausse dans la foulée.
Le helper `IconesBoostDuDessus` le consulte, donc les neuf cartes s'éteignent
ensemble sans qu'aucune n'ait à le savoir. Voie recommandée par le §3.1 du guide
(« état persistant maison ») et déjà employée par `gwenpool`.

## Trois arbitrages tranchés par l'utilisateur le 30/08/2026 (documentés, non rediscutés)

1. **`wc019a` New Vessel, trois valeurs imprimées** : **4 = menace de DÉPART**,
   **0 = accélération**, **8 = seuil qui COMPLÈTE** la manigance. Seul
   `StartingThreat: "4"` figure dans le `desc`. Le moteur ne lit `TargetThreat`
   et `EscalationThreat` que sur les complots **principaux**
   (`game/card/face/card_type/scheme_main.py`) : le seuil de 8 est donc **câblé
   à la main** dans `wc019a.py` (constante `MENACE_CIBLE`, écart assumé
   commenté), sur le modèle exact de `madame_web/the_grim_hunt_nemesis/mw018.py`
   (The Grim Hunt). L'accélération de 0 ne demande aucun code.
2. **`wc017` Royal Couple** : le « Team-Up (Hulkling and Wiccan) » imprimé est
   rendu comme une **condition « Hulkling en jeu », allié OU héros**. Ni la clé
   `desc.TeamUp` ni `.SetTarget("TeamUp")` : une simple condition sur
   `WhenInYourPlayTurn`, comme `il023` Sudden Plan Change (même auteur) et
   `jj022` Power Couple. C'est aussi ce que prescrit
   `docs/reference/mots-cles/teamup.md` quand l'un des deux noms est un allié.
3. **Aspect Justice** pour le deck de départ (aucune decklist fournie par
   l'auteur). Voir `metadata.aspect_note` de `deck/starter/wiccan.json`.

## Trois choix tranchés par Claude, faute d'interlocuteur (session en arrière-plan)

1. **`wc014` Warping Reality — « this round »** : le moteur ne connaît que
   `in_this="Phase"` et `in_this="Turn"` pour une réduction de coût
   (`Worlds.UpdateNextCardPlayCost`, `worlds.py:815`), **jamais `Round`** (même
   leçon que le pack Dazzler). **`Phase` est retenu**, la plus large des deux :
   elle couvre toute la phase des joueurs, tours des autres joueurs compris. Ce
   qui reste hors de portée, c'est la phase du **vilain** du même round — une
   carte jouée en réaction pendant la phase du vilain ne bénéficiera pas de la
   réduction alors que le texte imprimé le permettrait. **Écart plus sévère que
   la carte, jamais plus permissif.**
2. **`wc005` Magic Bolt — « This attack gains ranged »** : la phrase désigne le
   **SECOND** bloc de dégâts, pas les 3 premiers. Le texte séquence
   explicitement (« Deal 3 damage… **Then**, if the top card… ») : les 3
   premiers dégâts sont déjà résolus — et une éventuelle riposte déjà subie —
   quand on lit les icônes. La phrase suit immédiatement le second « deal 3
   damage to an enemy » dans la même puce : c'est son antécédent le plus proche.
3. **`wc020` Moridun — portée de « when Wiccan would remove threat »** : rendue
   comme « Wiccan lui-même, ou une carte **non personnage** que le joueur de
   Billy Kaplan possède » — donc ses sorts, mais pas ses alliés. Un allié qui
   contre n'est pas Wiccan. Détail du pourquoi technique dans le bug n°3.

## Deux écarts d'auteur assumés, non corrigés

1. **`wc020` Moridun est typée `Attachment`** alors que son texte se termine par
   « *(Wiccan's Nemesis Minion.)* ». Le **type imprimé fait foi** : la carte n'a
   ni PV, ni ATQ, ni MNG, et son premier mot est « Attach to… ». La parenthèse
   est une coquille de l'auteur. Documentée dans
   `wiccan_nemesis/__init__.py` et dans la fiche de la carte.
2. **`wc019b` The Demiurge n'est jamais tirée** : c'est le **verso** de
   `wc019a`, atteint uniquement par retournement. Elle compte donc pour un
   `card_id` de plus, mais le `nemesis_set` n'a bien que **cinq cartes
   physiques**.

## Outils exécutés depuis `.game-src`

- `tools/test_cards.py` : **4638 ok / 0 err** (25 modules `wc*` ajoutés ;
  référence relevée avant ce pack, dans ce même worktree : **4613 ok / 0 err**
  — aucune régression).
- `tools/verifier_prefixes.py` : OK — **5193 cartes, 27 préfixes déclarés,
  859 cartes fan-made**, aucun doublon, aucun préfixe non déclaré, aucun numéro
  emprunté.
- `tools/verifier_coherence_cartes.py` : **0 carte joueur sans classe d'aspect,
  0 obligation sans destinataire, 0 image manquante** (25 images `assets/pics/
  wc*.png`). Aucune collision de nom impliquant Wiccan n'apparaît dans le
  rapport — mais une collision réelle existe et a été traitée en amont :
  « **Hulkling** » (`wc002`, allié) porte le même nom que le **héros officiel**
  `56029a` du pack `cw`. C'est une collision **de noms**, jamais de `card_id` ;
  la seule carte du pack qui cherche « Hulkling » par son nom est `wc017`, et
  elle passe par `HulklingEnJeu`, qui **énumère** les alliés et les identités
  des joueurs au lieu de balayer `get_InPlay` (leçon `wolverine_x23`).
- Deck de départ (`tools/verifier_tous_les_decks.py`, `DECK_NOM=wiccan`) :
  partie montée avec succès, identité `wc001a`. **Ce test a trouvé le bug
  moteur n°1** : avant correctif, il échouait sur
  `AssertionError: self=[(01,wc001b) Billy Kaplan] face_type=Hero`.
- Script anti-fuite « jamais une carte signature d'un autre héros dans un
  deck » (PROCESSUS-HEROS §10) : **0 résultat**, sur les **94 decks de départ**
  du dépôt, `wiccan` inclus.
- `tools/test_capacites.py` : **34 cas dédiés au pack `wiccan`, 34/34 verts**
  (indices 617 à 650), rejoués **d'un bloc** après le dernier correctif. Un cas
  par capacité distincte, un cas partagé pour chaque lot de cartes physiquement
  dupliquées (Impenetrable Barrier ×2, Magic Bolt ×3, Magic Portal ×2,
  Teleport ×2, Inescapable Horror ×2), et deux ou trois cas pour chaque carte à
  branche conditionnelle (`wc005`, `wc009`, `wc011`, `wc017`, `wc018`, `wc019a`,
  `wc020`, `wc021`, `wc023`).
  **Preuve par substitution faite module par module**, 19 modules retirés puis
  remis, 35 relances : **33 cas rouges sans leur module**. Le seul qui reste
  vert est `wc017 … SANS Hulkling` (579), et c'est attendu — c'est une
  contre-épreuve de la condition (sans script, la carte ne fait rien non plus) ;
  la preuve de présence du module, c'est le cas 578, qui est bien rouge. Deux
  faux verts ont été attrapés au passage et corrigés (voir bugs n°4 et n°6).
- `tools/autoplay.py` : **8 parties contre `rhino`, profil `equilibre`**
  (détail et comparaison au témoin ci-dessous).

> ⚠ **Indices décalés de +56 depuis la fusion dans `master` (30/08/2026).**
> Les numéros de cas cités DANS LE CORPS de cette fiche sont ceux de la
> branche `worktree-okoye`, avant l'arrivée des packs `dazzler`,
> `wolverine_x23`, `superior_iron_man` et `kate_bishop` qui les précèdent
> désormais dans `CAS`. Pour retrouver un cas, ajouter 56 à l'indice écrit.

## Autoplay : 8 parties, témoin `okoye`

**Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError`
sur les 8 journaux : 0 partout.** Grep élargi `traceback|exception` : **0
partout aussi**. **0 partie bloquée** (`incidents: 0` dans le rapport).

| | `wiccan` | `okoye` (témoin) |
|---|---|---|
| parties | 8 | 8 |
| victoires | 0 | 0 |
| parties bloquées | 0 | 0 |
| rounds tenus (moyenne) | 4,4 | 4,1 |
| fin par complot achevé | 6/8 | 6/8 |
| fin par élimination | 2/8 | 2/8 |
| tracebacks | 0 | 0 |

**Lecture de l'écart : il n'y en a pas.** Les deux héros perdent leurs 8
parties, aucun n'en bloque une, aucun ne produit de traceback, et les deux
meurent des mêmes causes dans les mêmes proportions (6 complots achevés,
2 éliminations). Wiccan tient 4,4 rounds contre 4,1 au témoin : un quart de
round d'écart sur 8 parties, c'est du bruit, pas un signal. Le profil
`equilibre` ne gagne contre Rhino avec aucun des deux decks, ce qui est déjà
le cas du témoin depuis son audit : cela mesure le pilote, pas le pack.

**Couverture des cartes du pack dans les journaux** (présence du `card_id`) :
`wc001a` et `wc001b` **8/8**, `wc018` **8/8**, `wc010` 7/8, `wc012` et `wc013`
et `wc017` 6/8, `wc002`/`wc005`/`wc008`/`wc009` 5/8, `wc011`/`wc014`/`wc015`/
`wc016` 4/8, `wc003` 3/8, `wc006`/`wc007` 2/8, `wc004` 1/8 ; les 5 cartes du set
némésis (`wc019a`, `wc020`, `wc021`, `wc022`, `wc023`) 2/8 (aléa du tirage de
l'obligation). **`wc019b` The Demiurge : 0/8** — normal, elle n'est atteinte
qu'en laissant New Vessel monter à 8 menaces, ce qu'aucune des 8 parties n'a
fait ; elle a son cas dédié dans `test_capacites` (indice 584).

**Lecture ligne à ligne d'un journal** (partie 1, la plus lisible) : le cycle
complet de la mécanique centrale y est visible tel qu'écrit sur les cartes —

```
>  34: [(59,01104) Hard to Keep Down] was flipped ([(01,wc001b) Billy Kaplan])
>  78: [(59,01104) Hard to Keep Down] was discarded to EncounterDiscardPile<1> ([(01,wc001a) Wiccan])
> 128: [(66,01107) Breakin' & Takin'] was flipped ([(01,wc001a) Wiccan])
> 158: [(66,01107) Breakin' & Takin'] was discarded to EncounterDiscardPile<5> ([(08,wc002) Hulkling])
> 159: [(61,01105) "I'm Tough"] was flipped ([(01,wc001b) Billy Kaplan])
```

Ligne 34 : Clairvoyance de **Billy Kaplan** retourne la carte du dessus au début
de la phase des joueurs. Ligne 78 : le Forced Interrupt de **Wiccan** la
défausse au début de la phase du vilain. Ligne 128 : Clairvoyance retourne la
suivante, cette fois portée par la face héros. Ligne 158 : **Hulkling** défausse
la carte qu'il vient de compter. Ligne 159 : Clairvoyance retourne la nouvelle
carte du dessus. Les deux faces, les deux déclencheurs et l'interaction avec
`wc002` sont exercés dans une seule partie.

## Bugs réels trouvés et corrigés (preuve par substitution rouge/vert)

### 1. Bug MOTEUR : `PlayWithTopCardOfDeckFaceup` ne pouvait pas être portée par une face alter-ego

**Symptôme** : `tools/verifier_tous_les_decks.py DECK_NOM=wiccan` refusait de
monter la partie :

```
setup : AssertionError: self=[(01,wc001b) Billy Kaplan] face_type=Hero
  .../game/ability/factory/deck.py, line 99, in magik
    this = effect.this.CastTo(Hero)
```

**Cause** : la fabrique partagée castait `effect.this` en `Hero`. Ses deux seuls
usages antérieurs — Magik (`45030a`) et Falcon (`53001a`) — sont des **faces
héros** et ne voyaient donc pas le problème. Wiccan imprime sa Clairvoyance sur
ses **deux** faces : `wc001b` Billy Kaplan plantait le montage de partie dès la
première phase des joueurs.

**Correctif** : `CastTo(Hero)` → `CastTo(Identity)`, la classe mère commune de
`Hero` et `AlterEgo` (`game/card/face/card_type/identity.py:10`). `this` n'est
de toute façon **jamais utilisé** (un `Unused(this)` suit immédiatement) : le
cast ne servait que d'assertion, qui reste posée, simplement élargie. Aucune
autre carte du dépôt n'est affectée : Magik et Falcon restent des `Hero`, donc
des `Identity`.

**Rouge/vert** : rouge = `AssertionError` au montage de la partie **et** cas
`wc001b … Clairvoyance` rouge ; vert = deck monté (`{"deck": "wiccan", "ok":
true, "message": "identite wc001a, …"}`) et les deux cas Clairvoyance verts.
`test_cards` reste à **4638 ok / 0 err**.

### 2. `wc016` Wiccan's Cloak — « resolve that event again » plantait le moteur

**Symptôme** : `AssertionError` et 3 dégâts au lieu de 6 :

```
> 68: [(11,wc005) Magic Bolt] activates, targets [[(49,01094) Rhino]]
Traceback (most recent call last):
  File ".../game/effect/effect_invoke.py", line 197, in ResolveSelfInternal
    assert ability.when in [
AssertionError
```

**Cause** : la voie évidente était `played_face.ResolveAbility(joueur,
play_effect.ability.type, effect)` (`card_face.py:793`), la brique qu'emploie
`ResolveEachWhenRevealedAbilityAdditionalTime`. Elle passe par
`Effect.ResolveToPlayer`, qui appelle `ResolveSelfInternal` **sans message** ;
cette fonction porte alors une **liste blanche** de déclencheurs re-résolubles
(`effect_invoke.py:195-205`) — `WhenCardRevealed`, `WhenUnitBeDefeated`,
`WhenCardBecomeBoost`… — mais **pas `WhenPlayerInTurn`**, le déclencheur de
toute capacité « Play ». Un événement joué ne peut donc pas être re-résolu par
cette voie.

**Correctif** : on re-résout l'effet de jeu lui-même en lui **repassant son
message d'origine** — `play_effect.ResolveSelf(play_effect.bind_message,
effect, to_player=…, skip_cost=True)` — ce qui remet la résolution sur le chemin
normal (`isinstance(message, ability.when)` vrai, `effect_invoke.py:189-192`).
`skip_cost=True` rend exactement ce que dit le texte : l'événement est **rejoué
sans être repayé**. Les cibles sont **rechoisies** (rafraîchissement par
`play_effect.checker.UpdateLegalTargets()` puis `AskChooseFaces` dans la plage
imprimée), pour qu'un Magic Bolt rejoué ne se perde pas sur un ennemi que la
première salve vient de vaincre.

**Rouge/vert** : rouge = `degats sur 01094 = 3 (attendu au moins 6)` +
`AssertionError` au journal ; vert = 6 dégâts et cape inclinée.

### 3. `wc020` Moridun — l'interruption sur le retrait de menace ne partait jamais depuis un sort

**Symptôme** : cas rouge, `menace sur wc019a = 4 (attendu au moins 5)` après un
Magic Portal joué par Wiccan.

**Cause** : `WhenSchemeWouldRemoveThreat(..., who_make_thwart=CardFinder(
name="Wiccan"))` compare `message.by_effect.this` (`scheme.py:65-66`). Pour un
contre de base, c'est bien Wiccan ; pour un **sort**, c'est **l'événement**.
Asymétrie du moteur, vérifiée au journal : côté **dégâts**, le moteur attribue
déjà la source à l'identité même quand ils viennent d'un événement
(« `[Wiccan] would deal 3 damage to [Rhino] ([Magic Bolt])` »), donc la branche
« deal damage » couvrait déjà Magic Bolt ; côté **menace**, non.

**Correctif** : condition écrite à la main — Wiccan lui-même, ou une carte
**non personnage** (`Unit2.IsType` faux) possédée par le joueur de Billy Kaplan.
Un allié qui contre n'est donc pas Wiccan, ce qui est la lecture stricte du
texte imprimé.

**Rouge/vert** : rouge = New Vessel reste à 4 menaces ; vert = 5.

### 4. Défaut de CAS de test trouvé par la substitution elle-même (`wc014`)

La preuve par substitution a attrapé un **faux vert** : sans son module, le cas
`wc014` restait vert. Warping Reality porte elle-même une ressource **[wild]** ;
n'étant plus jouable, le pilote la **dépensait** pour financer Magic Portal
(0 + 2 + 1 = 3, le coût plein), et le cas passait sans que la réduction ait
jamais joué. Corrigé par `ne_pas_depenser: ["wc014"]`, qui interdit à la carte
de servir de ressource. **Rouge/vert après correction** : rouge =
`menace sur 01097b = 6 (attendu 1)` (Magic Portal injouable à 2 ressources pour
un coût de 3) ; vert = menace à 1. C'est exactement le genre de cas vert
mensonger que l'étape 7 de PROCESSUS-CARTE existe pour attraper.

### 5. Piège de nommage évité avant qu'il ne morde : le `*` d'unicité

`cards/paper.py:45-46` retire le préfixe `"* "` d'un nom unique
(`is_unique = name.startswith("* ")` puis `name = name.lstrip("* ")`). Un
`CardFinder(name="* Wiccan")` n'aurait **jamais** rien trouvé, en silence — et
cinq cartes du pack en dépendent (`wc017` via `HulklingEnJeu`, `wc019a` et
`wc020` et `wc021` et `wc023` via `NOM_WICCAN` / `NOM_MORIDUN` /
`NOM_NEW_VESSEL` / `NOM_DEMIURGE`). Les constantes du `__init__.py` du set sont
écrites **sans l'étoile** dès la première ligne.

### 6. Correction de DONNÉES rendue obligatoire : la leçon Dazzler sur `wc019a`

`CardFactory.GenerateCard` crée **une face par identifiant séparé par une
virgule** (`game/card/factory.py:63-67`). Déclarer `"wc019a"` seul donne une
carte dont `card.back_faces` est **vide** ; `CardFace.FlipTo` se contente alors
de la coucher face cachée (`card_face.py:987-989`) et la manigance **quitte le
jeu** au lieu de devenir The Demiurge. `deck/starter/wiccan.json` et
`data/nemesis/wiccan_nemesis.json` déclarent donc désormais
**`"wc019a,wc019b"`**. Le `nemesis_set` compte toujours cinq cartes physiques.

**Rouge/vert** : le cas `wc019a … When Completed` (582) a été rejoué à
l'identique avec `Puzzle.PutIntoPlay('wc019a')` (une seule face) au lieu de
`Puzzle.PutIntoPlay('wc019a,wc019b')`. Résultat rouge, et le journal montre
exactement le mécanisme du piège :

```
>  43: [(81,wc019a) New Vessel] activates
>  44: [[(81,wc019a) New Vessel]] moved to revealing area
>  47: [(81,wc019a) New Vessel] is entering play ([(81,wc019a) New Vessel])
RESULTAT: wc019b n'est pas en jeu ; wc019a est encore en jeu
```

La carte est couchée puis **re-révélée sur sa propre face** : The Demiurge
n'existe jamais. Avec la forme à deux faces, le cas est vert (`wc019b` en jeu,
`wc019a` hors jeu).

## Trois limites du harnais, documentées et non masquées

1. **Trois déclencheurs sont hors de portée de l'API Puzzle** : le début de la
   phase du vilain (`wc001a`), la fin de la phase des joueurs (`wc018`) et
   l'épuisement d'un deck de joueur (`wc019b`). Aucune commande `Puzzle.*` ne
   les produit, et vider vraiment le deck déclenche en plus la pénalité standard
   (une carte rencontre distribuée), qui fausserait le relevé. Les trois cas
   emploient donc une **sonde in-process** : la vérification renvoie dans le
   monde exactement le message que le moteur émet au même instant
   (`Message.WhenPhaseBegin("Villain", monde)`, `Message.WhenPhaseEnd(...,
   "Player", monde)`, `Message.AfterDeckRunOut(player.player_deck)`). Ce qui est
   court-circuité, c'est l'attente du tour de jeu, jamais la logique de la
   carte : les trois cas sont rouges sans leur module.
2. **`surpayer` compte des CARTES, pas des ressources.** La clé fixe
   `besoin = len(candidates)` (`test_capacites.py`, fonction `payer`) : avec
   deux cartes qui fournissent 2 ressources chacune, elle croit qu'il faut
   « 2 » et s'arrête après la première, qui en couvre 2. Magic Portal (coût 3)
   restait donc impayée et le cas paraissait rouge alors que la carte était
   correcte (journal : `Wiccan gains resource YY from Energy` puis
   `WhenPlayerInTurn failed`). Constaté, contourné en **retirant** `surpayer` :
   le calcul par défaut (`besoin = int(cout)`, avec les poids par carte) compose
   correctement 2 + 2 pour un coût de 3. La clé n'a **pas** été modifiée, pour
   ne pas changer silencieusement le comportement des cas qui l'emploient déjà
   (`mw008` et les cartes à coût X).
3. **Le pilote prend toujours la première option d'un `ChooseAbilities`**
   (convention `il017`/`ok019`/`ss011`). La seconde branche de l'obligation
   `wc018` — celle qui éteint le comptage des icônes pour tout le pack — était
   donc **intestable**. Une clé de cas **`preferer_option`** a été ajoutée au
   harnais : elle choisit l'option dont le **libellé** contient un fragment
   donné, au lieu d'un rang. Deux détails qui comptent : elle n'agit que pendant
   la phase « cas » (jamais pendant le setup), et elle **normalise les
   soulignés** — le moteur remplace les espaces des noms d'option par des `_`
   (`+1_ATK_until_the_end_of_the_round`), donc un fragment à plusieurs mots ne
   pouvait sinon jamais correspondre.

Deux points supplémentaires, qui ne sont pas des limites mais des observations
utiles au prochain pack :

- **Le pilote accepte volontiers un `MayChooseOneText`.** Sur `wc011` Teleport,
  il changeait systématiquement la forme du joueur ciblé, si bien que le
  « +1 ATQ » atterrissait sur une face alter-ego qui n'a pas d'ATQ, et le cas
  paraissait mort. Prouvé par `TRACE_OPTIONS=1` (ASK 4 = `Billy_Kaplan` /
  `Cancel`, ASK 5 = les quatre pouvoirs de base, tous sans `failure_reason`).
  Deux cas distincts en sortent : un avec `preferer_option: "Cancel"` pour
  mesurer le bonus, un sans pour exercer la bascule de forme.
- **`.SetHasNoTargetEffect()` a été retiré des `ForChoiceAbility` de `wc011`**
  par alignement sur `ok019`/`il017`, qui ne l'emploient pas. Rien ne prouve
  qu'il était en cause dans le cas rouge — la cause réelle était la bascule de
  forme ci-dessus, établie par la trace : c'est un alignement de style, pas un
  bug corrigé.

---

### wc001a : * Wiccan (face héros)

- [x] Étape 2 : cartes de référence :
      **Clairvoyance** → `falcon/falcon/53001a.py`, seule autre carte du dépôt
      qui imprime « play with the top card of the encounter deck face up » ;
      même `*AbilityFactory.PlayWithTopCardOfDeckFaceup(lambda effect:
      Worlds.GetEncounterDecks(effect), only_during_player_phase=True)`.
      `45030a` Magik emploie la même fabrique mais sur le deck JOUEUR et sans
      restriction de phase : ce n'est donc pas elle le modèle.
      **Forced Interrupt** → `AbilityFactory.WhenVillainPhaseBegin`
      (`turn_phase.py:176`) + `Worlds.DiscardEncounterTopCard` (`worlds.py:577`),
      la brique qu'emploie déjà Falcon dans sa Response « Eagle-Eyed ».
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : **`During the player
      phase`** (`only_during_player_phase=True`, qui ajoute un
      `WhenPlayerPhaseBegin` ET filtre les autres déclencheurs sur
      `IsPlayerPhase("AnyPlayer")`) ; **`the top card`** (une seule, pas toutes) ;
      **Forced Interrupt vs Forced Response** (`WhenVillainPhaseBegin`, donc
      AVANT le début de la phase, comme imprimé) ; **`encounter deck`** au
      pluriel côté moteur (`GetEncounterDecks`, comme Falcon, pour les scénarios
      à plusieurs decks). La capacité est portée par la face HÉROS seule : en
      identité civile c'est `wc001b` qui la porte, et le texte l'imprime aussi
      là-bas. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 9, ATQ 1, CTR 2, DEF 1, MNG 5 (`desc`
      et carte identiques) ; « the top card » → 1 carte défaussée.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par capacité :
      - `wc001a … Clairvoyance` (561) : deck de rencontre truqué à 01106, sonde
        `WhenPhaseBegin("Player")` → carte du dessus **face visible**. Rouge sans
        module (« encore FACE CACHEE »), vert avec.
      - `wc001a … Forced Interrupt` (563) : défausse de rencontre vérifiée vide
        au départ, sonde `WhenPhaseBegin("Villain")` → 01106 s'y retrouve. Rouge
        sans module (« aucune carte de rencontre defaussee »), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc001a` présente dans **8/8** parties ; le
      journal montre le cycle complet retournement → défausse → retournement
      (extrait cité plus haut) ; 0 traceback.

Carte terminée : OUI

### wc001b : * Billy Kaplan (face alter-ego)

- [x] Étape 2 : cartes de référence :
      **Clairvoyance** → même fabrique et même modèle que `wc001a` (Falcon
      `53001a`). La capacité est **dupliquée**, pas héritée : elle est imprimée
      sur les deux faces.
      **Action** → `AbilityType.Action` + `.LimitOncePerRound()` sur une face
      alter-ego, comme `10001b` Bruce Banner, `01029b` Tony Stark et `ag001b`
      Sharon Carter (« Action: » nu, jamais « Alter-Ego Action: »).
      **regarder 2 / défausser 1** → `gambit/gambit/37001b.py` Remy LeBeau,
      qui imprime exactement « look at the top 2 cards of the encounter deck,
      discard 1 of those cards » via `CostFunc.LookAtDeck("EncounterDeck", 2,
      discard=1)`.
- [x] Étape 5 : mots-pièges : **`you MAY discard one of them`** — la fabrique de
      Remy LeBeau n'est PAS réutilisable telle quelle, elle impose une plage
      `(discard, discard)` donc une défausse **forcée** ; ici la plage est
      `(0, 1)`, écrite à la main via `player.AskDiscardFaces` ;
      **`the top 2 cards`** (nombre fixe) ; **`one of them`** (une seule, prise
      parmi les 2 regardées, pas dans tout le deck) ; **`Limit once per round`**
      (`.LimitOncePerRound()`). Aucun `SetName` : le nom italique
      « Clairvoyance » appartient à la capacité du dessus, pas à l'Action.
      Résultat : conforme.
- [x] Étape 6 : nombres : PV 9, REC 3, MNG 6 ; 2 regardées, 0 ou 1 défaussée.
      Résultat : conforme.
- [x] Étape 7 : deux cas :
      - `wc001b … Clairvoyance` (562) : identique au cas de `wc001a` mais en
        forme civile (la partie démarre en alter-ego, aucun `ChangeToFace`).
        Rouge sans module, vert avec. **C'est ce cas qui a trouvé le bug moteur
        n°1.**
      - `wc001b … Action` (564) : `accepter_choix: True` pour exercer le
        « you may » ; la défausse de rencontre, vide au départ, contient 01106
        à la fin. Rouge sans module (`n'offre aucune action en jeu`), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc001b` présente dans **8/8** parties, le
      retournement de Clairvoyance lui est attribué à chaque début de phase des
      joueurs dans le journal ; 0 traceback.

Carte terminée : OUI

### wc002 : * Hulkling (allié signature)

- [x] Étape 2 : cartes de référence :
      **Interrupt sur attaque** → `AbilityFactory.WhenUnitWouldAttackUnit`
      (`do_attack.py:175`) + `message.GainAttackForThisAttack`
      (`sender_damage.py:436`), les deux seules cartes du dépôt qui augmentent
      l'ATQ d'une attaque en cours étant `cyclops/33033.py` Befuddle et
      `iceman/46015.py` Surprise Move.
      **comptage** → helper de pack `IconesBoostDuDessus` (modèle 09003).
      **défausse du dessus** → `Worlds.DiscardEncounterTopCard`, comme
      `ag008` Agent 13's Pistol.
- [x] Étape 5 : mots-pièges : **`When Hulkling attacks`** — `is_basic_attack`
      laissé à `None` (défaut), à la différence de Befuddle et Surprise Move qui
      impriment « makes a **basic** attack » et passent `True` ; le texte de
      Hulkling ne restreint pas ; **`for each boost icon`** (le nombre d'icônes
      EST le bonus, pas un palier) ; **`Then, discard that card`** — phrase
      séparée par un point, **inconditionnelle** : la défausse a lieu même à
      0 icône, et même quand l'obligation `wc018` a éteint le comptage (le texte
      dit « cannot be **counted** », pas « la carte n'est plus défaussée ») ;
      **`that card`** = bien celle qui vient d'être comptée, c'est-à-dire le
      dessus du deck. Le joueur consulté est le **contrôleur de l'allié**
      (`GetControlByPlayer`), pas `effect.GetInitiator()` : une interruption
      déclenchée en phase du vilain n'a pas forcément d'initiateur joueur
      (leçon `il020`). Résultat : conforme.
- [x] Étape 6 : nombres : coût 3, PV 3, ATQ 1\*, CTR 1\* (`desc`) ; +1 ATQ par
      icône ; 1 carte défaussée. `1*` = par joueur, lu nativement.
      Résultat : conforme.
- [x] Étape 7 : cas `wc002 Hulkling — Interrupt` (565) : deck truqué à 01111
      Explosion (**2 icônes**), attente ≥ 3 dégâts (1 ATQ + 2 icônes) **et**
      01111 dans la défausse de rencontre. Un montage à 0 icône ne prouverait
      rien. Rouge sans module (`degats sur Rhino = 1`), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc002` présent dans **5/8** parties ; journal
      de la partie 1 : « `Breakin' & Takin' was discarded to
      EncounterDiscardPile<5> ([(08,wc002) Hulkling])` » ; 0 traceback.

Carte terminée : OUI

### wc003 : Impenetrable Barrier (exemplaire 1/2)

- [x] Étape 2 : cartes de référence :
      **statut Tough** → `Faces.GiveStatus(faces, "Tough", effect)`
      (`faces.py:169`), brique standard.
      **« up to X » à nombre calculé** → `player.AskChooseFaces(candidats,
      (0, X), effect, not_move=True)` avec le choix imbriqué DANS le handler,
      comme `ag001b` et `15004` Hex Bolt — indispensable puisque le nombre de
      cibles n'est connu qu'à la résolution.
      **portée « friendly characters »** → `Worlds.GetOnFieldFriendlyCharacters`
      (`worlds.py:289`).
- [x] Étape 5 : mots-pièges : **`your hero`** (inconditionnel, ne consomme aucun
      des X — piège `your`) ; **`up to X`** (plage à minimum ZÉRO : le pilote la
      décline par défaut, d'où `accepter_choix` dans le cas) ; **`friendly
      characters`** NU (identités ET alliés de **tous** les joueurs — le texte
      n'écrit pas « you control », contrairement à la capacité Boost de `wc021`,
      qui le précise, elle) ; filtre `CardFinder(canbe_status="Tough")`
      (`checker.py:244`) pour ne pas proposer une cible déjà Tenace.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 2 ; 1 Tough au héros ; X = icônes de bonus.
      Résultat : conforme.
- [x] Étape 7 : cas `wc003 Impenetrable Barrier — Hero Action` (566) : allié
      `wc002` en jeu, deck truqué à 01111 (2 icônes), `accepter_choix` ;
      vérification `statuts: [[wc001a, Tough], [wc002, Tough]]`. Rouge sans
      module (aucun des deux n'a le statut), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc003` présente dans **3/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc004 : Impenetrable Barrier (exemplaire 2/2)

- [x] Étape 2 : identique à `wc003` (même texte imprimé, deux `card_id`).
      Code dupliqué à l'identique, commentaire complet sur `wc003`, pointeur
      bref sur `wc004` — convention `ok004`/`ok005`, `il021`/`il022`.
- [x] Étape 5 : mêmes mots-pièges que `wc003`, vérifiés sur le même texte.
      Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par le cas de `wc003` (code strictement identique,
      diff vide hors en-tête de commentaire).
- [x] Étape 8 : autoplay ciblé : `wc004` présente dans **1/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc005 : Magic Bolt (exemplaire 1/3)

- [x] Étape 2 : cartes de référence :
      **paliers d'icônes** → `scw/scarlet_witch/15004.py` Hex Bolt, seul
      événement officiel du dépôt qui branche sur le NOMBRE d'icônes de bonus.
      **second bloc de dégâts** → `initiator.ChooseAbilities` imbriqué avec son
      propre `.SetTarget(Enemy)`, **jamais `.SetTarget2`** : leçon `hd009`
      (Quack and Burn), `effect.targets2` n'est pas alimenté par le pilote
      générique et la moitié de la carte n'était jamais exercée.
      **ranged** → `property=AttackProperty(ranged=True)` passé à `DealDamage`
      (`ag003`, `ag005`, `45004`).
- [x] Étape 5 : mots-pièges : **`Then, if…`** (séquencement strict : les
      3 premiers dégâts sont résolus AVANT la lecture des icônes) ;
      **`0 or 1` / `2 or more`** (`icones <= 1` puis `else`, pas de trou) ;
      **`an enemy`** deux fois = **deux ciblages distincts**, pas la même cible
      reconduite ; **`This attack gains ranged`** → arbitrage documenté
      ci-dessus, la phrase porte sur le SECOND bloc. Deck de rencontre vide ou
      obligation `wc018` active → 0 icône → branche du haut, on pioche : lecture
      fidèle. Résultat : conforme.
- [x] Étape 6 : nombres : coût 2 ; 3 dégâts ; seuils 0/1 et 2+ ; 1 carte piochée ;
      3 dégâts au second bloc. Résultat : conforme.
- [x] Étape 7 : deux cas, un par palier :
      - `wc005 … palier « 0 ou 1 icône »` (567) : deck truqué à 01106 (1 icône),
        main vidée puis rechargée → **3 dégâts exactement** et **1 carte en
        main** (elle ne peut venir que de la pioche). Rouge sans module
        (0 dégât, 2 cartes en main), vert avec.
      - `wc005 … palier « 2 icônes ou plus »` (568) : deck truqué à 01111
        (2 icônes), cible M.O.D.O.K. (`01184`, 8 PV, Retaliate 2 imprimé) qui
        survit aux 6 dégâts → **6 dégâts exactement**. Rouge sans module
        (0 dégât), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc005` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc006 : Magic Bolt (exemplaire 2/3)

- [x] Étape 2 : identique à `wc005`, code dupliqué à l'identique.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les deux cas de `wc005`.
- [x] Étape 8 : autoplay ciblé : `wc006` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc007 : Magic Bolt (exemplaire 3/3)

- [x] Étape 2 : identique à `wc005`, code dupliqué à l'identique.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les deux cas de `wc005`.
- [x] Étape 8 : autoplay ciblé : `wc007` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc008 : Magic Manipulation

- [x] Étape 2 : cartes de référence :
      **« Alter-Ego Action: » sur une carte JOUEUR** → `AbilityType.AlterEgoAction`
      comme `21033` Soul World — et non `AbilityType.Action`, réservé aux faces
      d'identité elles-mêmes (distinction rappelée dans `ag001b`).
      **remélanger de la défausse vers le deck** → `Faces.ShuffleAllTo(faces,
      initiator.player_deck, effect)` (`faces.py:48`), comme `ok001b`
      Marshalling Forces et `ok011` Upanga.
      **pioche** → `initiator.DrawUp(1, effect)`.
- [x] Étape 5 : mots-pièges : **`for each boost icon`** (X = nombre d'icônes,
      pas un palier) ; **`1 card … for each`** — plage **fermée** `(n, n)`, le
      texte n'imprime pas « up to » : le remélange est obligatoire dès que des
      cartes sont disponibles ; **`your discard pile`** / **`your deck`** (le
      joueur qui joue, jamais un autre) ; **`Then, draw 1 card`**
      inconditionnelle (elle a lieu à 0 icône, sur une défausse vide, et sous
      l'obligation `wc018`). n est **borné** par la taille de la défausse : on ne
      peut pas remonter plus de cartes qu'il n'y en a. Résultat : conforme.
- [x] Étape 6 : nombres : coût 0 ; 1 carte par icône ; 1 carte piochée.
      Résultat : conforme.
- [x] Étape 7 : cas `wc008 Magic Manipulation — Alter-Ego Action` (569) :
      **2 cartes semées** dans la défausse du joueur (`01086`, `01087`) et deck
      de rencontre truqué à 01111 (**2 icônes**) → les deux doivent avoir quitté
      la défausse. Rouge sans module (les deux y sont encore), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc008` présente dans **5/8** parties ; le
      journal de la partie 1 montre l'action `Shuffle_back_into_your_deck` ;
      0 traceback.

Carte terminée : OUI

### wc009 : Magic Portal (exemplaire 1/2)

- [x] Étape 2 : cartes de référence : même squelette à paliers que `wc005`
      (modèle `15004` Hex Bolt) ; premier retrait par `.SetTarget(Scheme2)` +
      `.SetLabel('thwart')` comme `09003` Astral Projection et `ag004`
      Infiltrate ; « each scheme in play » par `Worlds.GetOnFieldSchemes`
      (`worlds.py:145`, complots principaux **+** manigances annexes).
- [x] Étape 5 : mots-pièges : **`a scheme`** → `Scheme2` et non `MainScheme`
      (n'importe quelle manigance — piège déjà documenté sur `hd001a`) ;
      **`each scheme in play`** → effet de zone, **aucun ciblage**, la liste
      passe directement à `RemoveThreatFromSchemes` (piège `each`) ;
      **`Then, if…`** (séquencement) ; **`0 or 1` / `2 or more`** (pas de trou).
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 3 ; 5 menaces retirées ; 1 carte piochée ;
      2 menaces par manigance. Résultat : conforme.
- [x] Étape 7 : deux cas, un par palier :
      - `wc009 … palier « 0 ou 1 icône »` (570) : complot principal posé à 6
        (sous son seuil, sinon il s'accomplit et l'événement n'a plus de cible),
        deck truqué à 01106 → menace exactement à **1**. Rouge sans module
        (menace inchangée à 6), vert avec.
      - `wc009 … palier « 2 icônes ou plus »` (571) : manigance annexe `01107`
        posée à **3** menaces à côté, jamais choisie comme cible → elle doit
        descendre à **1**, ce qui prouve la portée « each scheme in play ».
        Rouge sans module (reste à 3), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc009` présente dans **5/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc010 : Magic Portal (exemplaire 2/2)

- [x] Étape 2 : identique à `wc009`, code dupliqué à l'identique.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les deux cas de `wc009`.
- [x] Étape 8 : autoplay ciblé : `wc010` présente dans **7/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc011 : Teleport (exemplaire 1/2)

- [x] Étape 2 : cartes de référence :
      **« choose a player »** → `core/01092.py` Helicarrier, même
      `AbilityType.Action` et même `.SetTarget("Players")`, avec le même
      `target.GetControlByPlayer()` pour remonter au joueur.
      **redresser** → `Faces.ReadyAll` (`il015` / `ok014` / `hd001a`).
      **changer de forme, optionnellement** → aide partagée `YouMayChangeForm`
      de `cards/pack/__init__.py`.
      **bonus temporaire** → `identite.TemporaryGain(effect, None,
      Message.WhenRoundEnd, <pouvoir>=1, ignore_flip=True, render_ui=True)`.
- [x] Étape 5 : mots-pièges : **`that player`** (trois fois : redressement,
      changement de forme, bonus — tous sur le joueur CHOISI, jamais sur celui
      qui joue la carte) ; **`may change their form`** (optionnel) ;
      **`2 or more boost icons`** (seuil, le bonus ne part pas en dessous) ;
      **`until the end of the round`** (`Message.WhenRoundEnd`, pas
      `WhenPhaseEnd`) ; **`a basic power of their choice`** → quatre branches,
      ATQ / CTR / DEF / **REC**.
      **Choix technique assumé** : `TemporaryGain` plutôt que
      `GainUntilRoundEnd`. Les deux font la même chose — c'est le corps littéral
      de `GainUntilRoundEnd` (`face_action.py:410-437`) — mais la version courte
      n'expose pas `recover` (`TemporaryGain` l'accepte, ligne 49). Passer par la
      version longue est le seul moyen d'offrir les **quatre** pouvoirs de base.
      `29016` Patriot, qui n'en donne que trois, s'en tient à `GainUntilRoundEnd`
      parce qu'il vise un personnage quelconque, allié compris, qui n'a pas de
      REC. `ignore_flip=True` : le bonus survit au changement de forme, ce qui
      compte ici puisque la carte propose justement d'en changer juste avant —
      l'identité est donc **relue** après la bascule. Résultat : conforme.
- [x] Étape 6 : nombres : coût 1 ; seuil 2 icônes ; +1 sur un pouvoir ;
      jusqu'à la fin du round. Résultat : conforme.
- [x] Étape 7 : deux cas, un par moitié de la phrase :
      - `wc011 Teleport — Action` (572) : identité **inclinée** au départ, deck
        truqué à 01111 (2 icônes), `preferer_option: "Cancel"` pour refuser la
        bascule de forme et pouvoir mesurer le bonus → identité redressée **et**
        un pouvoir de base au-dessus de sa valeur imprimée. Rouge sans module
        (« encore inclinée »), vert avec (`+1 sur ['attack']`).
      - `wc011 Teleport — bascule optionnelle` (573) : sans `preferer_option`,
        le pilote accepte → partie en forme **AlterEgo**, `wc001b` prêt. Rouge
        sans module (« forme Hero »), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc011` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc012 : Teleport (exemplaire 2/2)

- [x] Étape 2 : identique à `wc011`, code dupliqué à l'identique.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les deux cas de `wc011`.
- [x] Étape 8 : autoplay ciblé : `wc012` présente dans **6/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc013 : Transmutation

- [x] Étape 2 : cartes de référence :
      **fouiller le deck de rencontre** → `Search.SearchForCard(effect,
      initiator, include_encounter_deck=True, not_move=True)` (`search.py:196`).
      On appelle `SearchForCard` **directement**, et non le raccourci
      `Search.EncounterCard`, parce que ce dernier ne transmet pas `not_move`
      (`search.py:47-77`) : sans lui, la carte trouvée est déplacée hors du deck
      par le sélecteur, alors que le texte veut qu'elle y reste et remonte.
      **remonter sur le dessus** → `Faces.MoveAllToDeck([face], deck, "Top",
      effect)` (`faces.py:60`), comme `ag001b` Sharon Carter.
- [x] Étape 5 : mots-pièges : **`Then, shuffle the encounter deck AND put that
      card on top of it`** — le mélange n'est PAS une ligne de code : tout
      `Select.From(..., not_shuffle=False, by_search=True)` du moteur remélange
      le deck fouillé (`search_internal.py:60-66`) ; la remontée a donc bien lieu
      **après** le mélange, dans l'ordre imprimé ; **`that card`** = celle qu'on
      vient de chercher ; **`Draw 1 card`** inconditionnelle (aucun « if »
      imprimé : la pioche a lieu même si rien n'a été trouvé). Seule carte SPELL
      du pack qui ne compte **aucune** icône : elle est volontairement absente de
      `EVENEMENTS_QUI_COMPTENT_LES_BOOSTS`, donc `wc016` ne la rejoue jamais.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 0 ; 1 carte cherchée ; 1 carte piochée.
      Résultat : conforme.
- [x] Étape 7 : cas `wc013 Transmutation — Action` (574) : `01111` posée sur le
      dessus et `01143` juste dessous, `cibles: ["01143"]` pour forcer la
      recherche ; vérification que **01143 est sur le dessus** après le mélange.
      Rouge sans module (le dessus reste 01111), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc013` présente dans **6/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc014 : Warping Reality

- [x] Étape 2 : cartes de référence : `Worlds.UpdateNextCardPlayCost`
      (`worlds.py:808`), brique unique du dépôt pour « reduce the cost of the
      next card played » ; modèles `core/01092.py` Helicarrier (« the next card
      that player plays this phase ») et `jessica_jones/on_the_job/jj015.py`
      Pore Over the Evidence (même brique sur un joueur nommé).
- [x] Étape 5 : mots-pièges : **`this round`** → écart assumé, documenté
      ci-dessus (le moteur ne connaît que `Phase` et `Turn`) ; **`1+X`** — la
      réduction vaut **au moins 1**, même à 0 icône, même deck vide, même sous
      l'obligation `wc018` : le « 1 » est imprimé en dur, seul X dépend des
      icônes ; **`the next card played`** (une seule carte, pas toutes) ; valeur
      **négative** attendue par la brique (Helicarrier passe `-1`).
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 0 ; réduction 1 + X. Résultat : conforme.
- [x] Étape 7 : cas `wc014 Warping Reality — Action` (575), **preuve par
      insuffisance** : Magic Portal (`wc009`) coûte 3 et la main ne contient
      qu'Energy (`01088`, 2 ressources) ; sans la réduction elle est injouable.
      Avec 1 icône (01106), la réduction vaut 1+1 = 2, le coût tombe à 1 et la
      carte part. `ne_pas_depenser: ["wc014"]` empêche le pilote de dépenser
      Warping Reality **elle-même** comme ressource [wild] — sans quoi le cas
      restait vert sans module (voir bug n°4). Rouge sans module
      (`menace sur 01097b = 6`), vert avec (menace à 1).
- [x] Étape 8 : autoplay ciblé : `wc014` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc015 : Mother's Protection

- [x] Étape 2 : cartes de référence : `bkw/04004.py` Mockingbird, même couple
      « payer un coût → prévenir des dégâts » (`.SetCostFunc(...)` +
      `message.PreventDamage` dans le handler) ; déclencheur
      `WhenUnitWouldTakeDamage(AbilityType.Interrupt, "YourIdentity", …)`,
      fabrique standard du guide §3.1.
- [x] Étape 5 : mots-pièges : **`your identity`** et non « your hero » — la
      protection joue **aussi en forme civile**, d'où la cible `"YourIdentity"` ;
      **`any amount of damage`** — aucun filtre `is_from_attack`, donc les dégâts
      de trahison et les dégâts indirects sont couverts ; **`shuffle … back into
      your deck →`** — la flèche fait de ce déplacement un **coût**, payé par le
      moteur AVANT le handler (`Effect.ProcessSelfCost`), donc la carte a bien
      quitté le jeu quand la prévention s'applique ; **`prevent 3`** (valeur
      exacte, pas `"All"` comme Mockingbird). Aucune `CostFunc` du moteur ne
      remélange une carte dans le deck (liste complète : `cost_func.py:106-1156`)
      → `CostFunc.Custom(None, …)`, le point d'extension prévu, déjà employé par
      huit cartes du dépôt. `CanPlayThisSupportCard()` est posée explicitement
      bien que `Support.GetAbilities` en ajoute une d'office
      (`support.py:17-23`) : même objet, écrit à la main pour que le fichier dise
      tout. Résultat : conforme.
- [x] Étape 6 : nombres : coût 1 ; 3 dégâts prévenus. Résultat : conforme.
- [x] Étape 7 : cas `wc015 Mother's Protection — Interrupt` (576) : 5 dégâts
      infligés à l'identité → **2 encaissés** et la carte **plus en jeu**. Rouge
      sans module (5 dégâts, carte encore en jeu), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc015` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc016 : * Wiccan's Cloak

- [x] Étape 2 : cartes de référence :
      **déclencheur** → `AbilityFactory.AfterPlayerPlayedCard(Response, "You",
      <finder>, …)` (`play.py:275`).
      **coût d'inclinaison** → `CostFunc.Exhaust("This")`, comme `ag008`.
      **défausse du dessus du deck de rencontre en coût** → aucune `CostFunc`
      du moteur ne le fait → `CostFunc.Custom(None, …)` +
      `Worlds.DiscardEncounterTopCard`.
      **re-résolution** → voir bug n°2 : `play_effect.ResolveSelf(bind_message,
      …, skip_cost=True)`.
      Aucune capacité « Play » déclarée : `Upgrade.GetAbilities` en pose une
      d'office (`upgrade.py:12-19`), comme pour `ag008`.
- [x] Étape 5 : mots-pièges : **`a [[SPELL]] event THAT COUNTS the amount of
      boost icons`** — un filtre par simple trait serait **faux** : `wc013`
      Transmutation est un événement SPELL du pack qui ne compte aucune icône et
      la cape la rejouerait à tort. Le filtre porte donc sur une liste explicite
      de `card_id` (`EVENEMENTS_QUI_COMPTENT_LES_BOOSTS`), doublée d'un contrôle
      `HasTrait("SPELL")` ; **`you play`** borné à `"You"`, jamais `"AnyPlayer"` ;
      **`exhaust … AND discard …`** — coût à **deux parties**, les deux payées
      (piège `and remove`) ; le coût `Custom` rend `False` quand le deck de
      rencontre est vide, la Response ne part alors pas — lecture stricte ;
      **`resolve that event AGAIN`** et non « play it again » → aucun coût
      repayé. La re-résolution ne redéclenche pas la cape (`ResolveSelf`
      n'émet aucun `AfterPlayerPlayedCard`), et la cape est de toute façon
      inclinée par son propre coût. Résultat : conforme.
- [x] Étape 6 : nombres : coût 3 ; 1 carte de rencontre défaussée ; 1
      re-résolution. Résultat : conforme.
- [x] Étape 7 : cas `wc016 Wiccan's Cloak — Response` (577) : Magic Bolt jouée
      avec la cape en jeu et le deck truqué à 01106 → **≥ 6 dégâts** (3 + 3) et
      **cape inclinée**. Rouge sans module (3 dégâts, cape non inclinée), vert
      avec. **C'est ce cas qui a trouvé le bug n°2.**
- [x] Étape 8 : autoplay ciblé : `wc016` présente dans **4/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc017 : Royal Couple (classe Basic)

- [x] Étape 2 : cartes de référence :
      **Team-Up rendu comme condition** → `il023` Sudden Plan Change (même
      auteur, Team-Up Stature and Iron Lad) et `jj022` Power Couple ; la
      condition passe par `conditions=[...]` sur `WhenInYourPlayTurn`, **jamais**
      par `SetPlay(only_if_you_control_face=...)`, qui cherche dans
      `GetInventoryDeck()` (les améliorations équipées) et ne voit pas les alliés
      — correctif déjà payé sur `il023`.
      **défausse de rencontre → dessus du deck** → `ag001b` Sharon Carter, même
      triplet `GetEncounterDiscardPileCards` + `AskChooseFace` +
      `MoveAllToDeck(..., "Top", ...)`.
      **redresser** → `Faces.ReadyAll`.
- [x] Étape 5 : mots-pièges : **collision de nom « Hulkling »** — `wc002` est un
      ALLIÉ, `56029a` est un HÉROS OFFICIEL du même nom ; la recherche
      **énumère** les alliés et les identités des joueurs
      (`HulklingEnJeu`), elle ne passe jamais par un
      `Worlds.FindCardsOnField(name="Hulkling")` nu, qui balaierait tout
      `get_InPlay`, cartes de rencontre comprises (leçon `wolverine_x23`) ;
      **`Choose ONE card`** (une seule) ; **`Ready your hero`** — seconde phrase,
      **inconditionnelle** : elle a lieu même si la défausse de rencontre était
      vide ; **`Hero Action`** (injouable en forme civile) ; **`Max 1 per
      deck`** = `desc.MaxPerDeck`, contrainte de construction de deck, aucun
      code. Le nom est écrit **sans** l'étoile d'unicité.
      Résultat : conforme.
- [x] Étape 6 : nombres : coût 1 ; `MaxPerDeck` 1 ; 1 carte remontée.
      Résultat : conforme.
- [x] Étape 7 : deux cas, dont une contre-épreuve :
      - `wc017 … AVEC Hulkling` (578) : allié en jeu, héros incliné, défausse de
        rencontre truquée à 01106 → héros **redressé** et 01106 **sur le dessus**
        du deck. Rouge sans module, vert avec.
      - `wc017 … SANS Hulkling` (579) : même montage sans l'allié → héros
        **toujours incliné**, rien ne remonte. Ce cas reste vert sans le module
        (sans script, la carte ne fait rien non plus) : c'est une **contre-
        épreuve de la condition**, pas une preuve de présence du module — la
        preuve de présence, c'est le cas 578.
- [x] Étape 8 : autoplay ciblé : `wc017` présente dans **6/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc018 : Avoiding the Demiurge (obligation)

- [x] Étape 2 : cartes de référence :
      **structure** → `ok019` Funeral Rites et `il017` Shadow of the Future
      (même auteur), même triplet `WhenThisObligationGiveToYou` +
      `YouMayFlipToYourAlterEgoForm` + `player.ChooseAbilities` à deux branches.
      **capacité Boost « Reveal this card »** → `AbilityFactory.WhenCardBecomeBoost
      ("This", RevealThisCard)`, idiome unique du dépôt (`16140` Sound the
      Alarms, `56144` Cap's Helmet).
      **interrupteur global** → voir « Mécanique centrale ».
- [x] Étape 5 : mots-pièges : **`your identity`** et non « your alter ego »
      (on incline la face COURANTE : `player.GetIdentity()`, pas
      `.GetAlterEgoFace()` comme `ok019`) ; **portée de « Discard this
      obligation »** — la phrase appartient à la **seconde** puce seulement, la
      première se terminant déjà par « remove … from the game », qui est
      exclusif d'une défausse (même lecture que `ok019` et `il017`) ;
      **`until the end of the NEXT player phase`** — l'obligation se révèle en
      phase du vilain, la prochaine fin de phase **joueur** est donc bien celle
      visée ; **`for any Wiccan card effects`** — interrupteur **global**, il vit
      dans le `__init__.py` du set et non dans `wc018.py` ; **un second
      mot-clé annoncé** (`[star] Boost`) — il a bien son module.
      `desc.GiveTo = "Billy Kaplan"` : `Obligation.CheckPrintedValue` exige ce
      champ sur toute obligation (correctif déjà payé sur `il020`).
      Résultat : conforme.
- [x] Étape 6 : nombres : aucun nombre imprimé hors les deux branches.
      Résultat : conforme.
- [x] Étape 7 : deux cas, un par branche :
      - `wc018 … branche 1` (580) : le pilote prend spontanément la première
        option → obligation **hors du jeu** et identité **inclinée**. Rouge sans
        module (« encore en jeu »), vert avec.
      - `wc018 … branche 2` (581) : atteinte grâce à la clé `preferer_option`
        ajoutée au harnais. Le vérificateur contrôle l'interrupteur **dans les
        deux sens** : drapeau levé **et** `IconesBoostDuDessus` à 0 juste après,
        puis drapeau **rabaissé** quand la sonde renvoie
        `WhenPhaseEnd("Player")`. Rouge sans module, vert avec.
      - La capacité **Boost** n'a pas de cas séparé : `Puzzle.Boost('wc018')`
        révèle la carte, donc résout l'obligation, et le résultat observable est
        exactement celui du cas 580. Elle est en revanche exercée en partie
        réelle : `wc018` apparaît dans **8/8** journaux d'autoplay, et le journal
        de la partie 1 montre l'action
        `Exhaust_your_identity_→_remove_Avoiding_the_Demiurge_from_the_game`.
- [x] Étape 8 : autoplay ciblé : `wc018` présente dans **8/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc019a : New Vessel (manigance annexe némésis, recto)

- [x] Étape 2 : cartes de référence :
      **seuil câblé à la main** → `madame_web/the_grim_hunt_nemesis/mw018.py`
      The Grim Hunt, même écart assumé, même constante.
      **« Only the <joueur> can remove threat »** →
      `gam/gamora_nemesis/18025.py` Sibling Rivalry, même phrase imprimée, même
      `PlayersCannotRemoveThreatFrom(PlayerFinder(non_name=…), "This")`.
      **When Defeated** → `AbilityFactory.WhenSchemeBeDefeated` (`jj015`,
      `27068`, `40194a`).
      **retournement en environnement** → `next_evol/.../40194a.py` Practice
      Maneuvers, même triplet `card.Flip` / `card.face` /
      `CastTo(Environment).Reveal(...)`.
      **détection de l'accomplissement** → `AbilityFactory.AfterSchemePlaceThreat
      (..., has_at_least_threat=MENACE_CIBLE)` (`scheme.py:89-111`), plus fin que
      le sondage de fin de phase de `mw018` : la menace de New Vessel est posée
      par `wc020` à chaque fois que Wiccan frappe ou contre, donc en pleine phase
      des joueurs.
- [x] Étape 5 : mots-pièges : **`Only the Billy Kaplan player`** — `Player.IsName`
      compare avec `check_all_face=True` (`player.py:251-262`), le joueur de
      Wiccan est donc reconnu dans les deux formes ; **`Then, set aside New
      Vessel AND Moridun`** — coût à deux parties, les **deux** cartes sont mises
      de côté (piège `and remove`) ; **`set aside`** et non « discard » — c'est
      ce qui permet à `wc020` de re-révéler « your SET-ASIDE New Vessel side
      scheme » ; **`the main scheme`** (`GetMainSchemes`, pas n'importe quelle
      manigance) ; **When Defeated vs When Completed** — deux fabriques
      distinctes, jamais un `if`. Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ `desc` ↔ code : **4** = `desc.StartingThreat`
      (lu nativement) ; **0** = accélération, absente du `desc`, aucun code ;
      **8** = `MENACE_CIBLE`, entier **nu** (la valeur imprimée ne porte pas
      l'icône par joueur, contrairement au `"5*"` de `mw018`, et la menace de
      départ imprimée ne la porte pas non plus) ; **2** menaces retirées du
      complot principal. Résultat : conforme.
- [x] Étape 7 : trois cas, un par capacité :
      - `wc019a … When Completed` (582) : `Puzzle.PutIntoPlay('wc019a,wc019b')`
        puis 4 menaces posées (4 + 4 = 8) → `wc019b` **en jeu**, `wc019a`
        **hors jeu**. Rouge sans module, vert avec.
      - `wc019a … When Defeated` (583) : complot principal posé à 5, menace de
        New Vessel ramenée à 0 → complot principal à **3** et les deux faces
        hors jeu (mises de côté). Rouge sans module (complot reste à 5), vert
        avec.
      - `wc019a … seul le joueur Billy Kaplan peut retirer de la menace` (594) :
        **vraie partie à deux joueurs** (`heros2: "okoye"`). La vérification
        monte les deux effets à la main (`GameRule(identite)`, dont l'initiateur
        vaut le contrôleur de la face, `rule.py:10-22`) et compare : menace
        **inchangée** pour Okoye, **4 → 2** pour Wiccan. Rouge sans module
        (« le second joueur (Okoye) a retiré de la menace : 4 → 2 »), vert avec.
        C'est la manigance qui porte l'appel, pas l'identité :
        `CanThwart.OnRemoveSchemeThreat` lit `by_effect.ability`
        (`can_thwart.py:62`), attribut qu'un effet de règle n'a pas.
- [x] Étape 8 : autoplay ciblé : `wc019a` présente dans **2/8** parties (aléa du
      tirage de l'obligation) ; 0 traceback.

Carte terminée : OUI

### wc019b : The Demiurge (environnement, verso de wc019a)

- [x] Étape 2 : cartes de référence : `mts/adam_warlock/21033.py` Soul World,
      **seule autre carte du dépôt** sur le déclencheur `AfterDeckRunOut`.
      **Écart voulu** : Soul World passe `lambda effect:
      effect.GetInitiator().player_deck` (le deck de SON joueur) ; ici le texte
      dit « **A** player deck », donc n'importe lequel — et un environnement
      n'appartient à aucun joueur, `effect.GetInitiator()` n'aurait pas de sens.
      La fabrique `AfterDeckRunOut` n'accepte qu'un `deck(effect)` comparé par
      égalité (`deck.py:40-41`), sans accès au message : elle ne sait pas
      exprimer « n'importe quel deck de joueur ». L'`Ability` est donc construite
      à la main, comme le font déjà une dizaine de cartes du dépôt (`cd008`,
      `dt077`, `lj004`, `mk021`, `60007`…), avec pour seule condition
      `message.deck.flags.is_player_deck` — le drapeau qu'emploie déjà
      `AfterDeckReset` pour cette même distinction (`deck.py:67-71`).
- [x] Étape 5 : mots-pièges : **`a player deck`** (n'importe quel joueur, jamais
      le deck de rencontre — d'où le filtre sur `is_player_deck`) ;
      **`Forced Response`** et non Interrupt (`After a player deck runs out`) ;
      **`the main scheme`** (`GetMainSchemes`) ; **`Permanent`** = mot-clé
      automatique lu dans `desc.Permanent`, **aucun code** (voir
      `docs/reference/mots-cles/permanent.md`, qui interdit explicitement de le
      recoder). Résultat : conforme.
- [x] Étape 6 : nombres : 1 menace posée. `desc.Permanent = "1"`.
      Résultat : conforme.
- [x] Étape 7 : cas `wc019b The Demiurge — Forced Response` (584) : New Vessel
      accomplie au montage pour poser l'environnement, complot principal remis à
      0, puis **sonde in-process** `Message.AfterDeckRunOut(player.player_deck)`
      (vider vraiment le deck déclencherait aussi la pénalité standard, qui
      distribue une carte rencontre et fausserait le relevé) → menace du complot
      principal **0 → 1**. Rouge sans module (0 → 0), vert avec.
- [x] Étape 8 : autoplay ciblé : `wc019b` **0/8** — normal et attendu : elle
      n'est atteinte qu'en laissant New Vessel monter à 8 menaces, ce qu'aucune
      des 8 parties n'a fait. Sa capacité est prouvée par le cas 584 ;
      0 traceback.

Carte terminée : OUI

### wc020 : * Moridun (attachement némésis)

- [x] Étape 2 : cartes de référence :
      **attacher à l'identité** → `hood/24007.py` Established Dominance, même
      `AttachToFaceWhenPutIntoPlay("YourIdentity")`.
      **révéler une carte mise de côté** → `mw018` The Grim Hunt, même
      `Worlds.GetSetAsideAreaCards(effect, CardFinder(name=…))`.
      **interruption sur les dégâts** → `AbilityFactory.WhenFaceWouldDealDamage`
      (`damage.py:495`).
      **interruption sur le retrait de menace** →
      `AbilityFactory.WhenSchemeWouldRemoveThreat` (`scheme.py:53`), dont la
      condition interne exige déjà `message.value > 0`.
- [x] Étape 5 : mots-pièges : **`the Billy Kaplan player's identity`** →
      `"YourIdentity"` et **non** `CardFinder(name="Billy Kaplan")` : la carte
      doit s'attacher aussi quand le joueur est en forme héros, où le nom de sa
      face courante est « Wiccan » ; **`deal damage to an enemy OR remove threat
      from a scheme`** → **deux** fabriques distinctes, jamais un `if` ;
      **`Wiccan`** (le nom de la face HÉROS, pas « votre identité » : en forme
      civile Billy Kaplan n'inflige pas de dégâts et ne contre pas), écrit
      **sans** l'étoile d'unicité ; **Forced Interrupt** et non Forced Response
      (la menace se pose AVANT que les dégâts ou le retrait ne s'appliquent) ;
      **`(Wiccan's Nemesis Minion.)`** = écart d'auteur assumé, le type imprimé
      Attachment fait foi. Portée du retrait de menace : voir bug n°3 et
      l'arbitrage n°3 de Claude. Garde : si New Vessel n'est pas en jeu (vaincue
      et mise de côté), rien ne se passe — le texte ne prévoit pas de repli.
      Résultat : conforme.
- [x] Étape 6 : nombres : 1 menace posée par déclenchement. Aucun autre nombre
      imprimé. Résultat : conforme.
- [x] Étape 7 : trois cas, un par capacité :
      - `wc020 … When Revealed` (585) : `wc019a` est **déjà** dans la zone de
        réserve du joueur au montage (le set némésis y vit, `worlds.py:384`) :
        la carte révélée est donc bien celle du deck, pas une copie fabriquée par
        le harnais → `wc020` **et** `wc019a` en jeu. Rouge sans module, vert avec.
      - `wc020 … Forced Interrupt (dégâts)` (586) : attaque de base de Wiccan →
        New Vessel passe de 4 à **≥ 5**. Rouge sans module, vert avec.
      - `wc020 … Forced Interrupt (retrait de menace)` (587) : Magic Portal joué
        par Wiccan, cible forcée sur le complot principal pour ne pas viser New
        Vessel elle-même → New Vessel **≥ 5**. Rouge sans module, vert avec.
        **C'est ce cas qui a trouvé le bug n°3.**
- [x] Étape 8 : autoplay ciblé : `wc020` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc021 : Inescapable Horror (exemplaire 1/2)

- [x] Étape 2 : cartes de référence :
      **When Revealed** → `AbilityFactory.WhenThisRevealed(None, …)`, fabrique
      standard.
      **statut sur le joueur qui révèle** → `cw/spider_woman/56177.py` Venom
      Blast, même `message.GetToPlayer().GetIdentity()` + `Faces.GiveStatus`.
      **capacité Boost** → `AbilityFactory.WhenCardBecomeBoost("This", …)`,
      même carte modèle.
- [x] Étape 5 : mots-pièges : **DEUX PORTÉES DIFFÉRENTES**, à ne surtout pas
      confondre (pièges `each` et `you control`) —
      « each friendly character » **nu** dans le When Revealed
      (`Worlds.GetOnFieldFriendlyCharacters`, identités **et** alliés de **tous**
      les joueurs) contre « each friendly character **you control** » dans la
      capacité Boost (le seul joueur qui révèle). L'auteur a explicitement écrit
      « you control » sur la seule capacité Boost : la différence est voulue.
      **`If Moridun is in play`** (branche conditionnelle, testée par un cas
      dédié dans chaque sens) ; **`you are stunned`** = le joueur qui révèle,
      jamais le premier joueur ni tous ; les dégâts ne sont **pas** une attaque
      (aucun `property=`), donc aucune riposte, aucun ranged.
      Résultat : conforme.
- [x] Étape 6 : nombres : 1 dégât par personnage, dans les deux capacités.
      Résultat : conforme.
- [x] Étape 7 : trois cas :
      - `wc021 … SANS Moridun` (588) : identité **et** allié à 1 dégât chacun,
        **aucun** étourdissement. Rouge sans module (0 dégât), vert avec.
      - `wc021 … AVEC Moridun` (589) : identité **Sonnée** en plus. Rouge sans
        module, vert avec.
      - `wc021 … capacité Boost` (590) : l'allié contrôlé prend ≥ 1 dégât.
        Rouge sans module, vert avec.
- [x] Étape 8 : autoplay ciblé : `wc021` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc022 : Inescapable Horror (exemplaire 2/2)

- [x] Étape 2 : identique à `wc021`, code dupliqué à l'identique.
- [x] Étape 5 : mêmes mots-pièges, dont les deux portées. Résultat : conforme.
- [x] Étape 6 : mêmes nombres. Résultat : conforme.
- [x] Étape 7 : couverte par les trois cas de `wc021`.
- [x] Étape 8 : autoplay ciblé : `wc022` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

### wc023 : Master Magus Returns

- [x] Étape 2 : cartes de référence : `mw018` (recherche en zone de réserve),
      `wc020` lui-même (qui va chercher New Vessel de la même façon), `il017`
      (`Faces.RemoveAllFromGame([this], effect)`), `56177` Venom Blast (statut
      sur le joueur qui révèle et capacité Boost).
- [x] Étape 5 : mots-pièges : **`If The Demiurge environment is NOT in play`**
      (garde négative : une fois New Vessel accomplie et retournée, cette
      trahison ne ramène plus Moridun) ; **`the SET-ASIDE Moridun attachment`**
      (la zone de réserve, pas la défausse de rencontre — Moridun n'y arrive que
      par le `Faces.SetAside` de `wc019a`) ; **`then remove … from the game`** —
      la phrase est **dans** la branche conditionnelle (« reveal …, **then**
      remove ») : quand The Demiurge est en jeu, la carte part à la défausse de
      rencontre normalement ; **`If Moridun was not revealed THIS WAY`** — hors
      branche, la phrase s'applique aussi bien quand The Demiurge bloquait que
      quand Moridun n'était pas de côté ; « this way » désigne la révélation de
      CETTE carte-ci, donc un Moridun déjà **en jeu** ne compte pas et le joueur
      est bien désorienté ; **`you`** = le joueur qui révèle.
      Résultat : conforme.
- [x] Étape 6 : nombres : aucun nombre imprimé. Résultat : conforme.
- [x] Étape 7 : trois cas :
      - `wc023 … When Revealed` (591) : `wc020` est dans la zone de réserve au
        montage → `wc020` **en jeu**, `wc023` **hors jeu**. Rouge sans module,
        vert avec.
      - `wc023 … avec The Demiurge en jeu` (592) : New Vessel accomplie au
        montage → **aucune** révélation de Moridun, identité **Désorientée**.
        Rouge sans module, vert avec.
      - `wc023 … capacité Boost` (593) : identité Désorientée. Rouge sans
        module, vert avec.
- [x] Étape 8 : autoplay ciblé : `wc023` présente dans **2/8** parties ;
      0 traceback.

Carte terminée : OUI

---

## Gate finale (PROCESSUS-HEROS)

- [x] **Étapes 1 à 8 complètes** : cards.json (25 cartes), scripts (25 modules
      + 3 `__init__.py`), deck de départ, `data/nemesis/wiccan_nemesis.json`,
      `data/sets_info.json` (129), 25 images, **biographie** (`wc001a` dans
      `public/js/prepare/heros-info.js`), **texte français** (25 entrées dans
      `ui-app/src/board/textes-fr-fanmade.ts`).
- [x] **Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour chaque
      carte du pack** : `wc001a`, `wc001b`, `wc002`, `wc003`, `wc004`, `wc005`,
      `wc006`, `wc007`, `wc008`, `wc009`, `wc010`, `wc011`, `wc012`, `wc013`,
      `wc014`, `wc015`, `wc016`, `wc017`, `wc018`, `wc019a`, `wc019b`, `wc020`,
      `wc021`, `wc022`, `wc023` — **25/25**.
- [ ] **Une partie complète jouée avec le héros** : **NON**, et ce n'est pas une
      omission qu'on peut combler ici. Une partie humaine dans le navigateur est
      hors de portée de cette session : elle demande d'ouvrir
      `http://127.0.0.1:2345/`, de cliquer et de juger. **Je ne l'ai pas jouée et
      je ne peux pas la jouer.** Ce qui a été fait à la place : 8 parties
      d'autoplay complètes (0 bloquée, 0 traceback), 34 cas de comportement
      verts avec preuve rouge/vert, et le montage de partie vérifié.

**Ce que ces outils ne peuvent pas voir** — à vérifier lors de la première
partie humaine, précisément :

1. **La biographie au survol.** PROCESSUS-HEROS §7 exige une preuve visuelle :
   survoler Wiccan dans le wizard et constater que le panneau affiche bien le
   texte, pas seulement le grand visuel. L'entrée est indexée par `wc001a` comme
   prescrit, mais **la preuve visuelle n'a pas été faite**.
2. **Les tooltips français.** Les 25 entrées sont écrites, mais rien n'apparaît
   dans le jeu tant que **`ui-app/deployer.sh` n'a pas tourné** (§11.1 du guide).
   **Il n'a pas été lancé dans cette session.**
3. **Le confort de Clairvoyance.** Jouer avec la carte du dessus du deck de
   rencontre face visible change l'affichage du plateau à chaque phase. Le
   journal d'autoplay montre que le retournement a bien lieu ; **il ne dit rien
   de ce que le joueur voit**.
4. **`wc019b` The Demiurge en partie réelle.** Aucune des 8 parties d'autoplay
   n'a laissé New Vessel monter à 8 menaces : le retournement est prouvé par le
   cas 582 et l'environnement par le cas 584, mais **jamais dans une partie
   entière jouée jusqu'au bout**.
