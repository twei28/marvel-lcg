# Mockingbird (Kajislav) — relevé du matériel, avant toute ligne de code

**Relevé le 10/09/2026**, depuis le Drive de l'auteur (dossier *Hero Packs /
Mockingbird (Released)*), pas depuis un zip local : **ce pack n'est dans aucun
des zips déposés sur le poste**. Il n'était donc dans aucun plan.

Même auteur que Spider-Woman : *MC Custom Content By: Kajislav*.

## Ce que contient le dossier

**17 images, 15 cartes numérotées 1/15 à 15/15, plus les deux faces
d'identité.** Cinq cartes sont livrées en double, chaque exemplaire portant son
propre numéro dans la série. Il y a donc **10 cartes distinctes**.

| Fichier | Carte | Type | Numéro |
|---|---|---|---|
| `00 mockingbird - hero` | * Mockingbird | Hero | — |
| `0 bobbi morse` | * Bobbi Morse | AlterEgo | — |
| `01 hawkeye` | * Hawkeye (Clint Barton) | Ally | 1/15 |
| `02 agent 19` | * Agent 19 | Upgrade | 2/15 |
| `03 shield medical clinic` | S.H.I.E.L.D. Medical Clinic | Support | 3/15 |
| `04 battle staves` | Battle Staves | Upgrade | 4/15 |
| `05` + `06 quick job` | Quick Job | Event | 5/15, 6/15 |
| `07` + `08 mocking kick` | Mocking Kick | Event | 7/15, 8/15 |
| `09` + `10 acrobatic maneuver` | Acrobatic Maneuver | Event | 9/15, 10/15 |
| `11` + `12 spy's secret strike` | Spy's Secret Strike | Event | 11/15, 12/15 |
| `13` + `14 unexpected assault` | Unexpected Assault | Event | 13/15, 14/15 |
| `15 skrull impostor` | Skrull Impostor | Upgrade | 15/15 |

## ⚠⚠ CE QUI MANQUE, ET QUI BLOQUE LE MONTAGE D'UN DECK

**Ni obligation, ni set némésis.** La carte 15/15 est une AMÉLIORATION
(*Skrull Impostor*), pas une obligation. Or `deck/starter/<héros>.json` exige
les deux champs `obligations` et `nemesis_set`, et
`verifier_tous_les_decks.py` monte une vraie partie qui les réclame.

Les autres packs de cet auteur en fournissent : Spider-Woman livre son
obligation dans le set héros **et** deux sets némésis complets. Ici, rien.

**C'est la seule question qui bloque, et elle est pour l'utilisateur.**

## Les deux mécaniques du pack

### 1. « If you paid for this card using a Mockingbird card »

**Cinq cartes sur dix** en dépendent : Mocking Kick, Acrobatic Maneuver,
Spy's Secret Strike, Unexpected Assault, et en creux Agent 19 qui fabrique la
ressource. C'est le cœur du pack.

⚠ **Cette formulation n'existe NULLE PART dans le catalogue.** Relevé : les 58
cartes officielles qui disent « if you paid for this card using a … » parlent
toutes d'une **icône de ressource** ([energy], [mental], [physical]), jamais
d'une carte nommée. Zéro précédent.

**Mais ce n'est PAS un blocage** : le moteur connaît déjà les cartes dépensées.
`Player.SpendResource` (`player_action.py:1075`) construit `paid_faces` et
envoie `Message.AfterCardsBeSpendAsResource(paid_faces, for_effect, player)`.
Ce que le contexte de l'effet retient, en revanche, ce sont seulement les
COULEURS (`paid_this_resources`). Deux routes, à trancher au moment d'écrire :

- écouter `AfterCardsBeSpendAsResource` depuis la carte jouée ;
- ou ranger `paid_faces` dans `effect.context` à côté de `paid_this_resources`,
  petit ajout moteur du même ordre que `CancelBoostIcons` pour Spider-Woman.

### 2. Une ressource restreinte à une carte du set

*Agent 19* : « Resource: Exhaust Agent 19 → generate a resource for a
Mockingbird card. »

✅ **La brique existe** : `AbilityFactory.CanGenerateResources` prend un
paramètre `for_card: CardFinder|None` (`factory/resources.py:279`). Rien à
concevoir.

## Les dix textes, tels que relevés

⚠ **Textes obtenus par OCR du scan**, pas par lecture visuelle. Les mots sont
fiables, **les CHIFFRES DE STATISTIQUES ne le sont pas** : l'OCR a rendu
« √2 / THY / ATK 2 / DEF » sur la face héros. **Toutes les stats sont à
reconfirmer à l'œil sur les scans** avant la moindre entrée dans
`data/cards.json`.

- **`* Mockingbird`** (Hero) — AVENGER. SPY. HAND SIZE 5 / HIT POINTS 9.
  *Spy Mastery* — **Response** : after Mockingbird removes 3 or more threat
  from a scheme (or schemes) by a single thwart, draw 1 card.
- **`* Bobbi Morse`** (AlterEgo) — S.H.I.E.L.D. SPY. REC 3. HAND SIZE 6 /
  HIT POINTS 9. *S.H.I.E.L.D.'s Database Access* — **Action** : look at the top
  card of any deck. *(Limit once per phase.)* **Response** : after you make a
  basic recovery, discard the top card of any deck.
- **`* Hawkeye`** (Ally, coût 3, ATK 3, THW 1) — AVENGER. Hawkeye's attacks
  gain ranged. **Forced Interrupt** : when Hawkeye attacks, discard the top card
  of the encounter deck. For each boost icon on that card, Hawkeye gets +1 ATK
  for this attack.
- **`* Agent 19`** (Upgrade, coût 2) — S.H.I.E.L.D. TITLE. Mockingbird gets
  +1 THW. **Resource** : exhaust Agent 19 → generate a resource for a
  Mockingbird card.
- **`S.H.I.E.L.D. Medical Clinic`** (Support, coût 1) — LOCATION. S.H.I.E.L.D.
  Bobbi Morse gets +1 REC. **Alter-Ego Action** : exhaust this card and discard
  a Mockingbird card from your hand → ready Bobbi Morse.
- **`Battle Staves`** (Upgrade, coût 1) — Restricted. WEAPON. Mockingbird gets
  +1 DEF *(chiffre à confirmer)*. **Response** : after your hero defends against
  an enemy attack, discard a Mockingbird card from your hand → confuse or stun
  that enemy.
- **`Quick Job`** (Event, coût 1, ×2) — SKILL. **Hero Response** : after you
  make a basic thwart (using your THW), ready Mockingbird.
- **`Mocking Kick`** (Event, coût 1, ×2) — ATTACK. THWART. **Hero Action**
  *(attack/thwart)* : deal 3 damage to an enemy. That enemy attacks you. If you
  paid for this card using a Mockingbird card, remove 3 threat from the main
  scheme.
- **`Acrobatic Maneuver`** (Event, coût 1, ×2) — DEFENSE. SKILL. THWART.
  **Hero Interrupt** *(defense/thwart)* : when you would take any amount of
  damage from an attack, prevent all of that damage and remove 1 threat from a
  scheme (3 threat instead if you paid for this card using a Mockingbird card).
- **`Spy's Secret Strike`** (Event, coût 2, ×2) — ATTACK. SKILL. THWART.
  **Hero Action** *(attack/thwart)* : deal 4 damage to an enemy. If that enemy
  is defeated by this attack, remove 2 threat from a scheme (3 threat from among
  schemes in play instead, if you paid for this card using a Mockingbird card).
- **`Unexpected Assault`** (Event, coût 3, ×2) — ATTACK. THWART. **Hero
  Action** *(attack/thwart)* : deal 5 damage to an enemy. This attack gains
  piercing. If you paid for this card using a Mockingbird card, remove 2 threat
  from each scheme in play.
- **`Skrull Impostor`** (Upgrade, coût 1) — CONDITION. Your identity gains the
  SKRULL trait. **Interrupt** : when Mockingbird would be defeated, set her hit
  point dial to 1 instead. Then, discard this card.

## Pièges de nommage, déjà vérifiés

- **`* Mockingbird` existe déjà, et c'est un ALLIÉ OFFICIEL** : `01083` (core)
  et `04004` (pack Hawkeye). Le héros fan-made porte le même nom. Même famille
  de piège que `spider_woman` et `hulk`, mais ici c'est le NOM DE CARTE qui
  entre en collision, pas le nom de deck.
- `deck/starter/mockingbird.json` **n'existe pas** : le nom de deck est libre.
- Préfixe **`mb` libre** (pris : `ma`, `mf`, `mk`, `mw`).
- Prochain numéro de set : **170** (169 = Spider-Woman).
- Une coquille imprimée de l'auteur : **« TWHART »** sur Spy's Secret Strike.
  Le trait imprimé garde ce qui est imprimé, comme *Arachnne* et *Misdiiirection*
  chez Spider-Woman.

## Mots-clés rencontrés, fiches à ouvrir avant d'écrire

`ranged`, `piercing`, `restricted`, `confused`, `stunned`. Les cinq ont déjà
leur fiche dans `docs/reference/mots-cles/`. Aucun mot-clé maison.

## Ce qu'il faut avant de commencer

1. **Trancher l'obligation et le set némésis** (voir plus haut). Bloquant.
2. **Les images en local.** Le connecteur Drive ne sait rendre que du texte ;
   les 17 PNG doivent être déposés sur le poste comme les autres packs, pour
   `assets/pics/` et pour la relecture visuelle des statistiques.

## Clos le 15/09/2026

Décision de l'utilisateur : **ce pack sort du backlog.** Le relevé reste ici
pour le jour où l'on y reviendrait ; les deux questions bloquantes
(l'obligation, le set némésis) ne sont pas tranchées et les images ne sont pas
en local.
