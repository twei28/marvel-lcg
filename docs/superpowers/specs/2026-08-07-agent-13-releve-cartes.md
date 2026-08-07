# Agent 13, relevé des cartes depuis les scans

Auteur : Rainy, Marvel Champions Custom Project, Cycle 2.
Tranche retenue : **79xxx**, libre (vérifié dans `cards.json` et dans `src/cards/pack/`).

## Identité, deux faces

| id | Face | Chiffres | Traits |
|---|---|---|---|
| 79001a | Agent 13 (Hero) | THW 2, ATK 1, DEF 2, main 5, 9 PV | S.H.I.E.L.D. SPY |
| 79001b | Sharon Carter (AlterEgo) | REC 3, main 6, 9 PV | S.H.I.E.L.D. SPY |

**Agent 13** — *Hand-to-Hand Specialist* — **Response** : After Agent 13 uses a
basic hero power, ready Agent 13 and make a basic attack against an enemy.
(Limit once per round).

**Sharon Carter** — *Super Spy* — **Action** : Choose a card in the encounter
discard pile and place it on top of the encounter deck. Then, remove threat
from a scheme equal to the number of boost icons on that card. (Limit once per
round.)

## Les 15 cartes signature, soit 9 distinctes

Les exemplaires multiples sont des copies identiques, vérifié en comparant les
scans 2 et 3 de Burst Fire.

| id | Nom | Ex. | Type | Coût | Ressource | Traits |
|---|---|---|---|---|---|---|
| 79002 | Captain America (Steve Rogers) | 1 | Ally | 3 | physique | AVENGER. S.H.I.E.L.D. SOLDIER |
| 79003 | Burst Fire | 3 | Event | 2 | physique | ATTACK. TACTIC |
| 79004 | Infiltrate | 3 | Event | 2 | mentale | TACTIC. THWART |
| 79005 | Parting Shots | 2 | Event | 1 | énergie | ATTACK. TACTIC |
| 79006 | Takedown | 2 | Event | 0 | physique | ATTACK. TACTIC |
| 79007 | Briefing Room | 1 | Support | 2 | joker | LOCATION |
| 79008 | Agent 13's Pistol | 1 | Upgrade | 2 | physique | WEAPON |
| 79009 | Physical Training | 1 | Upgrade | 2 | physique | CONDITION. SKILL |
| 79010 | Secret Agent | 1 | Upgrade | 2 | mentale | SKILL. TITLE |

Textes imprimés :

- **Captain America** (unique, 2** THW / 2** ATK / 5 PV — deux étoiles sous
  chaque icône THW et ATK, soit 2 dégâts consécutifs par attaque/contre) :
  Retaliate 1. **Interrupt** :
  When Captain America defends against an attack and would take damage, reduce
  that damage by 2 (to a minimum of 1).
- **Burst Fire** : **Hero Action** : Make the following two attacks :
  (attack) Deal 2 damage to an enemy. This attack gains ranged.
  (attack) Deal 2 damage to an enemy. This attack gains ranged.
- **Infiltrate** : **Hero Action** *(thwart)* : Remove 3 threat from a scheme.
  Look at the top card of the encounter deck and remove 1 additional threat for
  each boost icon on that card. Then, you may discard that encounter card.
- **Parting Shots** : **Hero Interrupt** *(attack)* : When an enemy would
  initiate an attack against you, deal 2 damage to that enemy. This attack
  gains ranged. You may flip to alter-ego form → that enemy schemes instead.
- **Takedown** : **Hero Response** *(attack)* : After you attack an enemy, deal
  2 damage to an enemy. If that enemy is defeated by this attack, draw 1 card.
- **Briefing Room** : **Hero Response** : After a minion or side scheme is
  revealed, exhaust Briefing Room → each player in hero form draws 1 card.
- **Agent 13's Pistol** : Restricted. **Hero Response** : After Agent 13
  attacks, exhaust Agent 13's Pistol and discard the top card of the encounter
  deck → deal 1 damage to an enemy for each boost icon discarded this way.
- **Physical Training** : You get +2 hit points. Agent 13 gets +1 ATK.
- **Secret Agent** : **Hero Resource** : Exhaust Secret Agent → generate a
  joker resource.

## Set némésis et obligation, relevés

Quatre cartes distinctes en cinq exemplaires, plus l'obligation. Vérifié que
`Hypnotic Suggestion` 4/5 et 5/5 sont la même carte, seul le numéro de pied
change.

| id | Nom | Ex. | Type | Bonus |
|---|---|---|---|---|
| 79011 | Assassination Plot | 1 | Side Scheme, 2 menaces par joueur | 3 |
| 79012 | Doctor Faustus | 1 | Minion, SCH 3, ATK 1, 3 PV | 2 |
| 79013 | Hallucination | 1 | Attachment, CONDITION | 1 |
| 79014 | Hypnotic Suggestion | 2 | Treachery | 2 |
| 79015 | Sleeper Agent | 1 | Obligation, donnée à Sharon Carter | 3 |

- **Assassination Plot** : **When Revealed** : Discard the ally you control with
  the highest remaining hit points. If you cannot, place 2 threat on this
  scheme. Porte deux icônes en pied : à gauche l'éclat avec point
  d'exclamation, à droite le fanion à croix blanche. Comparaison avec les
  scans FR officiels `assets/pics-fr/fr_01107.jpg` (Breakin' & Takin',
  Hazard seul → fanion à croix), `fr_01108.jpg` (Crowd Control, Crisis seul →
  éclat avec point d'exclamation) et `fr_27155.jpg` (Paradis des Fous, les
  deux ensemble) : l'éclat est bien **Crisis**, le fanion à croix est bien
  **Hazard**. C'est l'inverse de ce que la relecture globale avait conclu.
- **Doctor Faustus** (GENIUS. HYDRA. PSYCHIATRIST.) : Doctor Faustus cannot take
  damage while you are engaged with another minion. ★ **Forced Interrupt** :
  When Doctor Faustus would attack you while you control an ally, that ally
  deals damage to you equal to its ATK instead.
- **Hallucination** : **When Revealed** : Discard cards from the encounter deck
  until a minion is discarded. Reveal that minion and attach this card to it. If
  you cannot, this card gains surge. **Forced Interrupt** : When attached minion
  would take any amount of damage, discard it and place 3 threat on the main
  scheme.
- **Hypnotic Suggestion** : **When Revealed (Alter Ego)** : You are confused.
  This card gains surge. **When Revealed (Hero)** : Confuse your hero and place
  threat on the main scheme equal to your THW.
- **Sleeper Agent** : *Give to the Sharon Carter player.* You may flip to
  alter-ego form. Choose : Remove the Captain America ally from the game →
  remove Sleeper Agent from the game. Ou : Discard 1 card from hand and place 2
  threat on the main scheme. Discard this obligation.

## La mécanique du pack

**Compter les icônes de bonus d'une carte de rencontre**, présente sur trois
cartes : Sharon Carter, Infiltrate et le Pistolet. Le moteur sait le faire :
`FacesCounter.CountTotalBoostIcons`, et `HasBoostIcon.CountBoostIconsInternal`
dans `src/game/card/face/attribute/has_boost_icon.py`. Précédent officiel à
copier : Scarlet Witch `src/cards/pack/scw/scarlet_witch/15004.py`, qui regarde
la carte du dessus du deck de rencontre et compte ses icônes.
