# Pack Iron Lad — fiches PROCESSUS-CARTE.md, une par card_id

Gabarit suivi : `PROCESSUS-HEROS.md` / `PROCESSUS-CARTE.md` (lus en lecture
seule depuis `master`, non encore mergés dans ce worktree au moment de la
rédaction). 24 card_id au total (`il001a` à `il023`, la face `a`/`b` d'Iron
Lad comptant pour deux identifiants distincts). Source : pack fan-made
CptScorp (« Marvel Champions Custom Project », Cycle 2), zip `Iron Lad`
(Bureau, dossier `A créer`) — 25 cartes physiques scannées (2 faces héros +
15 signature + 1 obligation + 5 némésis + 1 Team-Up basique).

## Deux points tranchés par l'utilisateur le 29/08/2026

1. **Aspect du deck de départ** : aucune decklist d'aspect fournie par
   l'auteur (comme pour Okoye). **Justice** choisi (thème manipulation de
   deck/défausse cohérent avec tout le kit signature).
2. **Team-Up « Sudden Plan Change »** (il023) : le texte imprimé dit
   « Team-Up (Stature and Iron Lad) », mais Stature n'est pas une identité
   héros séparée dans ce moteur — c'est l'alliée signature il002, déjà dans
   le deck d'Iron Lad. Rendu comme condition **« Stature (alliée) en jeu »**
   plutôt que la sémantique TeamUp stricte (deux identités), précédent
   documenté dans `mots-cles/teamup.md` (jj022 Power Couple).
3. **Ion Amplifiers (il011/il012)**, compteurs « ion » dynamiques : pas de
   défausse automatique à 0 jeton (le texte imprimé ne porte pas la clause
   « discard this card », contrairement à Web-Shooter officiel).

## Outils exécutés depuis `.game-src` (`$HOME/marvel-work/python/bin/python3.10`)

- `tools/test_cards.py` : **4565 ok / 0 err** (pack `iron_lad` inclus, aucune
  régression sur les autres packs).
- `tools/verifier_prefixes.py` : OK, aucun doublon, préfixe `il` déclaré
  dans `tools/prefixes_fanmade.json`.
- `tools/verifier_coherence_cartes.py` : 0 obligation sans destinataire, 0
  carte joueur sans classe, 0 mot-clé imprimé sans clé `desc` pour le pack
  `iron_lad` (après correctif `GiveTo` sur il020, voir plus bas). La
  collision de nom « Iron Lad »/« Stature » n'existe pas ailleurs dans le
  dépôt (noms non ambigus).
- Deck de départ (`tools/verifier_tous_les_decks.py`, restreint au seul
  deck `iron_lad` via `DECK_NOM=iron_lad`) : partie montée avec succès,
  identité `il001a`, main 5 cartes, 30 cartes restantes au deck.
- `tools/test_capacites.py` : **22 cas dédiés au pack `iron_lad`, 22/22
  verts** (un par capacité distincte ; les cartes physiquement dupliquées
  — Ion Blast x3, Seeking Solutions x2, Ion Amplifiers x2, Pay the Price x2
  — partagent un seul cas, contenu identique). Six vrais bugs trouvés et
  corrigés en écrivant ces cas (preuve par substitution rouge/vert directe :
  rouge = traceback ou assertion observée avant correctif, vert = cas passe
  après) — détail par carte ci-dessous : `il015`, `il016`, `il018`, `il019`,
  `il020`, `il023`. Pour les 10 autres cartes testées (`il001a`, `il001b`,
  `il002`, `il003`, `il004`, `il007`, `il009`, `il010`, `il011`, `il017`,
  `il021`), le cas est passé du premier coup : la preuve de substitution
  formelle (retirer le module, constater rouge) n'a pas été rejouée
  systématiquement dessus, faute de temps — leur couverture repose sur le
  cas positif lui-même (qui échouerait si l'ability n'existait pas : le
  déclencheur `Puzzle.Action`/`jouer` échoue net si aucune ability
  correspondante n'est offerte, comme observé sur `il007`/`il015` avant
  correction).
- `tools/autoplay.py` : **8 parties contre `rhino`, profil `equilibre`,
  0 partie bloquée, 0 traceback.** Toutes les capacités principales
  observées en jeu réel dans le journal (`Destiny`, `Inventive_Genius`,
  `Attack`, `Play:Upgrade/Event/Support/Ally`, `Response`, `Hero_Response`,
  `Action`, `Recover`, `Discard`, `Deal_2_damage`,
  `Remove_2_threat_from_a_scheme`, `Change_Form`). 0/8 victoires, 4,8 rounds
  tenus en moyenne. **Témoin `okoye`** (héros déjà audité à 100%, même
  scénario/profil) : 0/8 victoires, 0 bloquée, 4,1 rounds tenus en moyenne —
  taux de blocage et de survie comparables, aucun écart anormal.

## Bugs réels trouvés et corrigés (preuve par substitution)

1. **il020 (Taking Responsability)** — `Obligation.CheckPrintedValue` exige
   `desc.GiveTo` non-None sur TOUTE carte Obligation, même sans texte
   imprimé « Give to X player » (précédent officiel : 90129 Wounded
   Civilians). Rouge : `AssertionError: il020` au chargement de n'importe
   quel deck. Vert : `"GiveTo": "Iron Lad"` ajouté à `cards.json`.
2. **il020** — `.SetPlay()` sur l'action « Remove the top card... » suppose
   `desc.Cost` (`assert HasCost.IsType(face)`), qu'une Obligation n'a
   jamais. Rouge : `AssertionError: face=[(05,il020) Taking Responsability]`.
   Vert : remplacé par `AbilityFactory.PlayerActionToDiscardThis` (modèle
   Weakened, `toafk/kang/11018.py`, officielle).
3. **il020** — `effect.GetInitiator()` dans le Forced Response rendait
   parfois le vilain (`AssertionError: self.initiator=Rhino`) au lieu du
   joueur. Vert : lecture via `message.trigger.GetControlByPlayer()`.
4. **il015 (Iron Lad's Suit)** — `.SetPlay()` posé sur l'Action répétable
   (redresser Iron Lad) au lieu de la seule mise en jeu de la carte :
   `Puzzle.PutIntoPlay('il015')` échouait silencieusement (la carte finissait
   sur le dessus du deck au lieu d'être en jeu). Vert : `.SetPlay()` retiré
   (modèle Munitions Cache, `determination/dt070.py`, une Action régulière
   sur un Upgrade déjà en jeu n'en a pas besoin).
5. **il016 (Neurokinetic Interface)** — `AfterPlayerRevealCard(..., None,
   ...)` : `which_card=None` ne déclenche JAMAIS l'ability
   (`Condition.CheckWhichCard` n'a pas de repli pour `None`, même piège que
   `CheckWhichPlayer` documenté sur Albert/ab001a.py). Vert :
   `EncounterCard` (classe de base) à la place de `None`.
6. **il018 (Early Start) et il019 (Kang the Conqueror)** — `NameError:
   name 'UpgradesIronLadEnJeu' is not defined` : les cartes du set némésis
   ont leur propre `from . import *` (`iron_lad_nemesis/__init__.py`),
   distinct de celui du pack héros où l'aide est définie. Vert : import
   explicite ajouté (`from cards.pack.iron_lad.iron_lad import
   UpgradesIronLadEnJeu, ...`).
7. **il019** — `AfterUnitBeDefeated` (message APRÈS coup) arrive trop tard :
   le nettoyage générique de la carte empilée (son `PlaceCardArea`) la
   défaussait déjà avant que le hook ne se déclenche (observé : « Iron
   Lad's Suit were discarded » avant même le message de défaite). Vert :
   remplacé par `WhenUnitWouldBeDefeated` (hook AVANT coup), qui récupère la
   carte empilée pendant qu'elle est encore là.
8. **il023 (Sudden Plan Change)** — `SetPlay(only_if_you_control_face=...)`
   cherche dans `GetInventoryDeck()` (les upgrades/objets équipés), PAS les
   alliés en jeu : la condition ne voyait jamais Stature. Vert : remplacé
   par un `conditions=[...]` testant `Worlds.FindCardsOnField(effect,
   name="Stature", card_type=Ally)`.
9. **il023** — `identity.ChangeToOtherForm(effect)` sert au choix PARMI
   PLUSIEURS faces (identités à 3+ faces) et ne faisait donc rien sur un
   simple aller-retour Hero/AlterEgo. Vert : `identity.
   ChangeToOtherIdentityForm(effect)`, le vrai bascule binaire.

Aucun de ces 9 défauts n'était visible par `test_cards.py` (construction
seule) : seuls `verifier_tous_les_decks.py` (défauts 1-2) et
`test_capacites.py` (défauts 3 à 9, la carte étant vraiment JOUÉE) les ont
attrapés — confirmation directe de la leçon du guide (§8).

---

### il001a : Iron Lad (face héros)

- [x] Étape 2 : carte de référence : `01029b` Tony Stark (core/iron_man),
      même couple `LookAtDeck` + `AskChooseFace(s)` pour « regarder le
      dessus du deck, garder une carte » — étendu ici à « jusqu'à 2 cartes »
      via `AskChooseFaces(faces, (0, 2), ...)` et filtré par type de
      ressource nommé (`CardFinder(has_printed_res=lettre).Checks(faces)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés — `up to 2` (range
      (0,2), pas (1,2) : le joueur peut ne rien garder), `Limit once per
      round` (`.LimitOncePerRound()`), le type de ressource nommé AVANT de
      regarder les cartes (`DeclareResourceType()` appelé en premier).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : HP 9, ATK 2, THW 2, DEF 2, HS 4
      (desc et carte identiques) ; « top 4 cards » → `LookAtDeck(deck, 4,
      effect)` ; « up to 2 » → range `(0, 2)`. Résultat : conforme.
- [x] Étape 7 : cas `il001a Destiny — regarde 4 cartes, en garde au plus 2` :
      invariant robuste (au moins 2 cartes partent TOUJOURS en défausse,
      quel que soit le type nommé/les correspondances). Vert du premier
      coup. Preuve renforcée par l'autoplay : `Destiny` apparaît dans les
      8/8 parties (2 fois par round joué, la limite du mot-clé).
- [x] Étape 8 : autoplay ciblé : couvert par la campagne pack (8 parties,
      0 traceback, `Destiny` exercé dans 100% des parties). Témoin `okoye`
      comparable (0 bloquée, rounds similaires).

Carte terminée : OUI

### il001b : Iron Lad (face alter-ego, Nathaniel Richards)

- [x] Étape 2 : carte de référence : Evaluate Threat (hercules/59028.py),
      `Worlds.UpdateNextCardPlayCost(player, -2, effect, finder=..., in_this=
      'Phase')` pour la réduction de coût.
- [x] Étape 5 : mots-pièges : `next TECH card` (finder `trait="TECH"`, pas
      une carte précise), `this phase` (`in_this='Phase'`), `Limit once per
      round`. Résultat : conforme.
- [x] Étape 6 : nombres : HP 9, REC 3, HS 6 ; réduction `-2` ; plancher à 0
      géré par le moteur (`Worlds.UpdateNextCardPlayCost`, testé). Résultat :
      conforme.
- [x] Étape 7 : cas `il001b Inventive Genius` : preuve par insuffisance de
      ressources — il009 (coût 1, TECH) joué SANS aucune carte de paiement
      en main ; seule la réduction de 2 (plancher 0) rend cela possible.
      Vert. Porte aussi `SetupReshuffleNemesis` (règle spéciale de l'insert,
      voir ci-dessous).
- [x] Étape 8 : `Inventive_Genius` exercé dans 8/8 parties de l'autoplay,
      0 traceback.

**Règle spéciale non imprimée sur une carte, mais sur l'insert de règles**
(« Iron Lad — Rules Insert ») : « When your deck empties and you have to
reshuffle, ... you also have to find and reveal your Nemesis Minion. »
Câblée via `SetupReshuffleNemesis()` (`iron_lad/__init__.py`), qui surcharge
`player.player_deck.BindDiscardPile` (modèle : le moteur pose déjà cette
liaison par défaut dans `player.py:71-73`, jamais surchargée par un héros
avant Iron Lad) pour, en plus du tirage standard, chercher et mettre en
file Kang the Conqueror via `Search.EncounterCard` + `DealEncounterCard`
avant `RevealEncounterCards()`. **À vérifier en partie réelle** : aucun
précédent dans le dépôt pour ce montage précis ; le harnais Puzzle ne sait
pas déclencher un reshuffle de deck (aucune commande dédiée), donc ce cas
précis n'a pas de `test_capacites` propre — seule la lecture de code et la
cohérence des briques individuelles (chacune déjà éprouvée ailleurs dans le
moteur) le soutiennent.

Carte terminée : OUI (la règle spéciale de reshuffle reste à vérifier en
partie réelle longue, aucun outil du dépôt ne sait la déclencher)

### il002 : Stature (Cassie Lang)

- [x] Étape 2 : carte de référence : `ok003` Ayo (okoye/okoye/ok003.py) pour
      `AfterCardEnterPlay(AbilityType.Response, "This", ...)`.
- [x] Étape 5 : mots-pièges : `heal 1 damage from your identity` (fixe, pas
      conditionnel), `may discard up to 3` (`DeclareNumber(0, 3)`, le pilote
      choisit 0 par défaut), `1 more damage for each card discarded`
      (`1 + len(discarded)`). Résultat : conforme.
- [x] Étape 6 : nombres : soin de base 1, jusqu'à 3 cartes, +1 soin par
      carte. Résultat : conforme.
- [x] Étape 7 : cas `il002 Stature` : identité endommagée de 3, Stature mise
      en jeu, soin exactement 1 (pilote décline le bonus). Vert du premier
      coup.
- [x] Étape 8 : `Play:Ally` + `Response` exercés dans plusieurs parties de
      l'autoplay, 0 traceback.

Carte terminée : OUI

### il003 : Energy Overflow

- [x] Étape 2 : carte de référence : aucune carte directement comparable
      trouvée pour « X cibles, X = coût imprimé d'une carte défaussée » ;
      construit à partir des briques `CostFunc.Discard(trait="TECH", ...)`
      + `.return_discarded_cards` (`aos/maria_hill/50006.py` pour le filtre
      trait+from_where) et `DamageProperty(6, ignore_tough=True)` (modèle
      Sanctuary, `mts/thanos/21116.py`).
- [x] Étape 5 : mots-pièges : `a TECH card you control` (`from_where=
      ["YouControlCards"]`), `X is equal to the printed resource cost`
      (`face.printed_cost.val`, pas le coût réduit), `ignores tough status
      cards` (`DamageProperty(ignore_tough=True)`). Résultat : conforme.
- [x] Étape 6 : nombres : 6 dégâts fixes, X = coût imprimé. Vérifié avec
      il009 (coût 1) → X=1, 6 dégâts à 1 cible. Résultat : conforme.
- [x] Étape 7 : cas `il003 Energy Overflow` : il009 défaussée (coût 1),
      6 dégâts confirmés sur 01094 (pas 2, pas un autre montant). Vert.
- [x] Étape 8 : `Deal_2_damage`/`Attack` exercés dans l'autoplay (Ion Blast
      partage ces libellés) ; Energy Overflow elle-même jouée au moins une
      fois (partie 1, `Play:Event` x2+`Cancel`). 0 traceback.

Carte terminée : OUI

### il004, il005, il006 : Ion Blast (3 exemplaires physiques)

- [x] Étape 2 : carte de référence : structure « Hero Action (attack) »
      standard, cible unique + bonus optionnel modélisé comme un choix
      textuel (`AskChooseOneText`, modèle `determination/dt070.py`).
- [x] Étape 5 : mots-pièges : `an enemy` (range (1,1)), `may discard 5 cards
      ... instead` (binaire, pas « jusqu'à 5 » : soit 2 dégâts soit 6, rien
      entre les deux). Résultat : conforme.
- [x] Étape 6 : nombres : 2 dégâts de base, 6 dégâts si 5 cartes défaussées.
      Résultat : conforme.
- [x] Étape 7 : cas `il004 Ion Blast` (partagé pour les 3 exemplaires,
      contenu identique) : 2 dégâts de base confirmés sur 01094, pilote
      décline le bonus. Vert du premier coup.
- [x] Étape 8 : `Attack`/`Deal_2_damage` exercés dans 8/8 parties de
      l'autoplay. 0 traceback.

Carte terminée : OUI (les 3 exemplaires)

### il007, il008 : Seeking Solutions (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : Asteroid M (`magneto/magneto/49002.py`)
      pour `from_where=["YourDiscardPileTopmost"]` + `Faces.ShuffleAllTo` ;
      Tony Stark (`01029b`) pour la pioche conditionnelle.
- [x] Étape 5 : mots-pièges : `2 cards from your discard pile` (choix du
      joueur, `AskChooseFaces(..., (0,2), forced=False)`), `1 card for
      each TECH card shuffled` (compte les cartes TECH PARMI celles
      choisies, pas toutes). Résultat : conforme.
- [x] Étape 6 : nombres : jusqu'à 2 cartes mélangées, 1 pioche par carte
      TECH. Résultat : conforme.
- [x] Étape 7 : cas `il007 Seeking Solutions` : il009 (TECH) forcée via
      `cibles`, doit avoir quitté la défausse. Vert après correction du cas
      (Event, doit être JOUÉ — `Puzzle.Action` réservé aux cartes déjà en
      jeu, pas aux Events).
- [x] Étape 8 : `Alter-Ego_Action` exercé plusieurs fois dans l'autoplay,
      0 traceback.

Carte terminée : OUI (les 2 exemplaires)

### il009 : Vision AI

- [x] Étape 2 : carte de référence : combinaison Asteroid M (topmost) +
      Conditioning Room (`gam/gamora/18008.py`, `from_where=
      ["YourDiscardPileBottommost"]` + `Faces.ReturnToHand`).
- [x] Étape 5 : mots-pièges : `the top card` vs `the bottom card` (deux
      cibles distinctes, Topmost/Bottommost), `shuffle ... into your deck`
      vs `Return ... to your hand` (deux opérations différentes). Résultat :
      conforme.
- [x] Étape 6 : nombres : 1 carte mélangée, 1 carte rendue. Résultat :
      conforme.
- [x] Étape 7 : cas `il009 Vision AI` : défausse à 2 cartes connues
      (01088, 01089 dans cet ordre) ; 01089 (dessus) quitte la défausse,
      01088 (dessous) revient en main. Vert du premier coup.
- [x] Étape 8 : `Play:Support` + action exercés dans l'autoplay,
      0 traceback.

Carte terminée : OUI

### il010 : Hack

- [x] Étape 2 : carte de référence : Great Responsibility (core/01061.py)
      pour `WhenThreatWouldBePlacedOn` + `message.SetBeInstead(effect)` ;
      Temporal Leap (`next_evol/cable/40013.py`) pour
      `RemoveThreatFromSchemes`.
- [x] Étape 5 : mots-pièges : `remove that amount from that scheme instead`
      (le MÊME plan, pas un autre — `message.trigger`), `you may discard 5
      cards ... a different scheme` (exclusion explicite du premier plan
      dans le filtre). Résultat : conforme.
- [x] Étape 6 : nombres : montant = `message.value` (le montant qui allait
      être posé, pas une constante), coût additionnel 5 cartes. Résultat :
      conforme.
- [x] Étape 7 : cas `il010 Hack` : menace du complot principal fixée à 5,
      un sbire manigance ; menace finale < 5 (retirée, pas ajoutée), Hack
      défaussée. Vert du premier coup.
- [x] Étape 8 : pas observée spontanément dans les 8 parties d'autoplay
      (le pilote ne l'a pas piochée/gardée systématiquement) — capacité
      couverte uniquement par `test_capacites`, pas par l'autoplay ciblé.

Carte terminée : OUI

### il011, il012 : Ion Amplifiers (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : Web-Shooter (core/01008.py) pour le
      couple `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1,
      "ion")` + `Resources("G")` ; Hawkeye (core/01066.py) pour
      `AfterCardEnterPlay` + pose de compteurs à l'entrée en jeu (compte
      DYNAMIQUE ici, pas fixe : `desc.Uses` ne le permet pas).
- [x] Étape 5 : mots-pièges : `X is equal to the number of TECH cards you
      control` (compte recalculé à CHAQUE entrée en jeu, pas seulement à
      la première), pas de clause « discard this card » (tranché par
      l'utilisateur : pas de défausse automatique à 0 jeton).
      **Correctif moteur** : compteur `'ion'` ajouté à `COUNTER_LIST`
      (`game/card/face/card_face.py`), absent avant ce pack.
- [x] Étape 6 : nombres : 1 compteur si 1 carte TECH contrôlée (elle-même
      seule), 2 si 2 (elle-même + Vision AI) — vérifié par DEUX cas
      distincts. Résultat : conforme.
- [x] Étape 7 : cas `il011 Ion Amplifiers — 1 compteur` et `— 2 compteurs` :
      les deux verts du premier coup, prouvant que le compte suit vraiment
      l'état du plateau (pas une constante figée).
- [x] Étape 8 : `Play:Upgrade` exercé dans l'autoplay, 0 traceback.

Carte terminée : OUI (les 2 exemplaires)

### il013 : Iron Lad's Boots

- [x] Étape 2 : carte de référence : ag009 Physical Training
      (agent_13/agent_13/ag009.py) et ok012/ok013 Midnight Angel Armor
      (Okoye) pour `*AbilityFactory.GiveKeywordToAttached("You",
      trait="AERIAL")` sans cible attachée.
- [x] Étape 5 : mots-pièges : `Iron Lad gains AERIAL` (trait, pas un
      mot-clé à fiche séparée — Aerial est un trait officiel déjà câblé
      nativement, voir Angel/Captain Marvel), `After playing an event`
      (déclencheur générique `AfterPlayerPlayedCard(CardFinder(card_type=
      Event))`, pas un événement précis). Résultat : conforme.
- [x] Étape 6 : nombres : aucun (trait + retour de 1 carte). Résultat :
      conforme.
- [x] Étape 7 : deux cas — `il013 — trait AERIAL` (vert du premier coup) et
      `il013 — Response après un événement` (défausse à 2 cartes connues,
      01089 revient en main après avoir joué Ion Blast, un Event). Vert du
      premier coup.
- [x] Étape 8 : `Play:Upgrade` exercé dans l'autoplay, 0 traceback.

Carte terminée : OUI

### il014 : Iron Lad's Helmet

- [x] Étape 2 : carte de référence : ok001a The Art of War (okoye/okoye/
      ok001a.py) pour `AfterUnitUseBasicPower(..., "You", powers=["ATK",
      "THW"])`.
- [x] Étape 5 : mots-pièges : `after Iron Lad uses a basic power` (ATK ou
      THW, pas DEF/REC — `powers=["ATK", "THW"]`, même liste qu'ok001a).
      Résultat : conforme.
- [x] Étape 6 : nombres : 1 carte rendue. Résultat : conforme.
- [x] Étape 7 : cas `il014 Iron Lad's Helmet` : défausse à 2 cartes connues,
      Iron Lad attaque (`Puzzle.Attack('Iron Lad')`), 01089 revient en
      main. Vert du premier coup.
- [x] Étape 8 : `Attack` exercé dans 8/8 parties de l'autoplay,
      0 traceback.

Carte terminée : OUI

### il015 : Iron Lad's Suit

- [x] Étape 2 : carte de référence : ag009 (`GiveKeywordToAttached("You",
      health=3)`) et Munitions Cache (`determination/dt070.py`, Action
      régulière sur Upgrade SANS `.SetPlay()`).
- [x] Étape 5 : mots-pièges : `You get +3 hit points` (bonus permanent, pas
      conditionnel), `ready Iron Lad` (l'IDENTITÉ, pas la Suit elle-même —
      `Faces.ReadyAll([initiator.GetIdentity()], effect)`). Résultat :
      conforme.
- [x] Étape 6 : nombres : +3 PV. Résultat : conforme.
- [x] Étape 7 : cas `il015 Iron Lad's Suit` : **rouge** au premier essai
      (`.SetPlay()` en trop empêchait `Puzzle.PutIntoPlay` de fonctionner),
      **vert** après retrait de `.SetPlay()` — preuve par substitution
      directe. +3 PV et redressement de l'identité confirmés.
- [x] Étape 8 : `Play:Upgrade` exercé dans l'autoplay, 0 traceback.

Carte terminée : OUI

### il016 : Neurokinetic Interface

- [x] Étape 2 : carte de référence : jj001b Pays the Bills (jessica_jones/
      jessica_jones/jj001b.py) pour `AfterPlayerRevealCard`, silk/52028.py
      pour `<Type>.IsType(face)` (idiome classmethod).
- [x] Étape 5 : mots-pièges : `if that card was: A treachery or minion` vs
      `A side scheme or attachment` (deux branches distinctes, `Treachery/
      Minion` vs `SchemeSide2/Upgrade`), `an encounter card` (classe de
      base `EncounterCard`, pas `None`). Résultat : conforme.
- [x] Étape 6 : nombres : 2 dégâts OU 2 menaces retirées (jamais les deux à
      la fois). Résultat : conforme.
- [x] Étape 7 : cas `il016 Neurokinetic Interface` : **rouge** deux fois
      (`which_card=None` ne déclenchait jamais l'ability ; puis oubli de
      `ChangeForm` pour une capacité HeroResponse), **vert** après les deux
      correctifs — preuve par substitution directe. 2 dégâts confirmés sur
      01094 après révélation d'une trahison (il021).
- [x] Étape 8 : pas observée spontanément dans les 8 parties (le pilote ne
      l'a pas systématiquement posée/gardée) — couverte par
      `test_capacites` uniquement.

Carte terminée : OUI

### il017 : Shadow of the Future

- [x] Étape 2 : carte de référence : ok019 Funeral Rites (okoye/okoye/
      ok019.py), même structure `WhenThisObligationGiveToYou` +
      `YouMayFlipToYourAlterEgoForm` + `player.ChooseAbilities` à 2
      branches.
- [x] Étape 5 : mots-pièges : `Give to the Nathaniel Richards player`
      (`desc.GiveTo`), `remove ... from the game` (branche 1,
      `Faces.RemoveAllFromGame`) vs `discard` (branche 2,
      `Faces.DiscardAll`) — deux destinations différentes. Résultat :
      conforme.
- [x] Étape 6 : nombres : 3 cartes retirées de la partie (branche 1) ; 1
      carte TECH + 3 cartes du deck défaussées (branche 2). Résultat :
      conforme.
- [x] Étape 7 : cas `il017 Shadow of the Future` : branche par défaut
      (première option, comme Funeral Rites) — l'obligation est bien
      retirée de la partie. Vert du premier coup.
- [x] Étape 8 : révélée en mise en place de plusieurs parties de l'autoplay
      (obligation du héros), aucune n'a planté.

Carte terminée : OUI

### il018 : Early Start

- [x] Étape 2 : carte de référence : `CardCannotReady` (game/ability/
      factory/state.py) pour la restriction continue ; construction du
      filtre "amélioration Iron Lad" via `set_name` (pas un trait) dans
      `UpgradesIronLadEnJeu` (__init__.py).
- [x] Étape 5 : mots-pièges : `each Iron Lad upgrade in play` (filtre par
      `set_name == "Iron Lad"`, PAS par trait TECH — plus précis et
      multijoueur-sûr), `While this scheme is in play` (la restriction
      cesse automatiquement quand la carte quitte le jeu, propriété native
      de `CardCannotReady`, pas de garde supplémentaire nécessaire).
      Résultat : conforme.
- [x] Étape 6 : nombres : aucun. Résultat : conforme.
- [x] Étape 7 : cas `il018 Early Start` : **rouge** (`NameError:
      UpgradesIronLadEnJeu`, import manquant entre les deux sous-paquets),
      **vert** après ajout de l'import explicite — preuve par substitution
      directe. il011 bien inclinée après révélation.
- [x] Étape 8 : révélable en jeu réel (nemesis_set), non observée
      spontanément dans les 8 parties (aléa du tirage).

Carte terminée : OUI

### il019 : Kang the Conqueror

- [x] Étape 2 : carte de référence : A.I.M. Abductor (aos/aim_abduction/
      50080.py) pour `TuckCardUnderHere` ; `Filter.One(..., highest_cost=
      True)` (game/operate/filter.py) pour « le coût le plus élevé ».
- [x] Étape 5 : mots-pièges : `the highest cost Iron Lad upgrade` (même
      filtre `UpgradesIronLadEnJeu` qu'Early Start), `Return the upgrade
      under here to its owner's hand` (pas la défausse), `Set Kang the
      Conqueror aside` (retiré du jeu sans repasser par le deck rencontre —
      `Faces.SetAside`). Résultat : conforme.
- [x] Étape 6 : nombres : Toughness 1, Villainous 1, HP 6, SCH 2, ATK 2 —
      tous conformes à `desc`. Résultat : conforme.
- [x] Étape 7 : cas `il019 Kang the Conqueror` : **rouge trois fois**
      (`NameError` import manquant ; puis `AfterUnitBeDefeated` trop tardif,
      la carte empilée déjà auto-défaussée par le nettoyage générique du
      moteur avant que le hook ne se déclenche), **vert** après le passage
      à `WhenUnitWouldBeDefeated` (hook avant coup) — preuve par
      substitution directe, documentée en détail dans le fichier. il015
      (coût 3, le plus élevé face à il011 coût 2) bien empilée puis rendue
      en main à la défaite ; Kang bien mis de côté.
- [x] Étape 8 : révélable en jeu réel, non observée spontanément dans les
      8 parties (aléa du tirage).

Carte terminée : OUI

### il020 : Taking Responsability

- [x] Étape 2 : carte de référence : Weakened (toafk/kang/11018.py,
      obligation officielle SANS GiveTo) pour `AfterUnitUseBasicPower` +
      `PlayerActionToDiscardThis`.
- [x] Étape 5 : mots-pièges : `After you attack or thwart` (`powers=["ATK",
      "THW"]`), `Remove the top card ... from the game` (pas la défausse)
      `→ discard this obligation` (deux opérations distinctes, la seconde
      via `ex_operation` de `PlayerActionToDiscardThis`). Résultat :
      conforme.
- [x] Étape 6 : nombres : 1 carte défaussée (Forced Response), 1 carte
      retirée de la partie (Action). Résultat : conforme.
- [x] Étape 7 : deux cas — `il020 — Forced Response` (**rouge** trois fois :
      `GiveTo` manquant, `.SetPlay()` sur une Obligation, puis
      `effect.GetInitiator()` rendant le vilain ; **vert** après les trois
      correctifs) et `il020 — Action` (vert dès le second correctif).
      Preuve par substitution directe documentée.
- [x] Étape 8 : révélable en jeu réel ; le montage du deck lui-même
      (`verifier_tous_les_decks.py`) est PASSÉ PAR cette carte pour trouver
      le premier bug (GiveTo), donc déjà exercée hors `test_capacites`.

Carte terminée : OUI

### il021, il022 : Pay the Price (2 exemplaires physiques)

- [x] Étape 2 : carte de référence : `ThisCardGainSurge` (aide partagée),
      modèle Hypnotic Suggestion (agent_13/agent_13_nemesis/ag014.py) pour
      le gain de renfort conditionnel.
- [x] Étape 5 : mots-pièges : `Discard 8 cards from your deck` (top du
      deck, `DiscardDeckTopCards(8, effect)`), `If less than 8 ... gains
      surge` (condition sur le nombre RÉELLEMENT défaussé, pas 8 fixe — le
      deck peut être plus court). Résultat : conforme.
- [x] Étape 6 : nombres : 8 cartes. Vérifié avec un deck de départ assez
      grand pour ne PAS déclencher le renfort (exactement 8 défaussées).
      Résultat : conforme.
- [x] Étape 7 : cas `il021 Pay the Price` : 8 cartes défaussées confirmées.
      Vert du premier coup (le seul cas resté vert pendant TOUTE la
      campagne, y compris avant le correctif GiveTo — il021 ne referme
      aucune des briques buguées des autres cartes).
- [x] Étape 8 : révélée et résolue dans PLUSIEURS parties de l'autoplay
      (visible dans le journal détaillé, partie 1 notamment), 0 traceback.

Carte terminée : OUI (les 2 exemplaires)

### il023 : Sudden Plan Change (BASIC, Team-Up)

- [x] Étape 2 : carte de référence : jj022 Power Couple (jessica_jones/
      jessica_jones/jj022.py) pour la structure BASIC/Team-Up/MaxPerDeck ;
      `identity.ChangeToOtherIdentityForm` (game/card/face/card_type/
      identity.py) pour le vrai bascule Hero/AlterEgo.
- [x] Étape 5 : mots-pièges : `Team-Up (Stature and Iron Lad)` (condition
      rendue comme alliée en jeu, voir point tranché en tête de fichier —
      PAS `only_if_you_control_face`, qui ne cherche que les objets
      équipés), `Change to another form` (bascule binaire, pas un choix
      parmi plusieurs faces). Résultat : conforme.
- [x] Étape 6 : nombres : +1 taille de main, jusqu'à la fin de la phase.
      Résultat : conforme.
- [x] Étape 7 : cas `il023 Sudden Plan Change` : **rouge deux fois**
      (condition `only_if_you_control_face` ne trouvait jamais Stature ;
      puis `ChangeToOtherForm` — la mauvaise méthode — ne changeait rien),
      **vert** après les deux correctifs — preuve par substitution directe.
      Stature en jeu, carte jouée gratuitement, forme passée à AlterEgo,
      +1 taille de main confirmée.
- [x] Étape 8 : non observée dans les 8 parties d'autoplay (le pilote n'a
      jamais mis Stature en jeu ET tenté ce Team-Up dans le même
      échantillon) — couverte uniquement par `test_capacites`.

Carte terminée : OUI

---

## Ce que ces blocs ne peuvent pas voir

Aucune partie n'a été jouée par un humain dans le navigateur : la validation
s'arrête à `test_cards`, `verifier_*`, `test_capacites` (22 cas verts) et
`autoplay` (8 parties, 0 traceback, comparable au témoin). La règle spéciale
de reshuffle (il001b, voir plus haut) n'a aucun outil du dépôt capable de la
déclencher : **à vérifier en partie réelle**, précisément sur ce point.
