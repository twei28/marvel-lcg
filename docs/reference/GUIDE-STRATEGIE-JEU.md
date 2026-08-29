# Marvel Champions LCG : cadre de décision tour par tour

> Document de référence stratégique, conservé dans sa version d'origine.
> Il sert deux usages : jouer mieux, et servir de spécification à la politique
> de jeu du simulateur `tools/autoplay.py` (voir la section « Traduction dans le
> bot » en fin de fichier).

---

## The Core Principle

A game of Marvel Champions usually follows four strategic phases:

> **Stabilize → Build → Take Control → Close the Game**

The most common mistake is attacking the villain while the board is still unstable.

Damage dealt to the villain usually does not reduce what the encounter deck can do during the next villain phase. Defeating a minion, clearing a side scheme, removing a dangerous attachment, or applying a status card often does.

In general:

> **Villain damage is your lowest priority until it contributes to a controlled stage transition or wins the game.**

---

# The Decision Tree

Use the following questions during each player phase.

## 1. Can We Win This Turn?

Before doing anything else, calculate your available damage.

Account for:

* **Guard**
* **Tough**
* **Retaliate**
* Interrupts and responses
* The villain's remaining hit points
* The next villain stage
* Any **When Revealed** ability on the next stage
* Additional enemies or encounter cards created by the stage transition
* Resources required to complete the attack sequence

If you have reliable lethal damage, win the game.

You do not need to clear threat or defeat unrelated minions unless they directly prevent the win.

If you cannot win, continue to the next question.

---

## 2. Can We Lose During the Next Villain Phase?

Check threat and damage separately.

### Threat Risk

Estimate the likely threat after the next villain phase:

```text
Current threat
+ threat placed during step one
+ villain schemes
+ minion schemes
+ possible additional activations
+ encounter card effects
```

The basic villain phase sequence is:

1. Place threat on the main scheme.
2. The villain and minions activate.
3. Deal encounter cards.
4. Reveal and resolve encounter cards.

This means the main scheme can be completed before you receive an opportunity to solve the problem during the next player phase.

Pay particular attention to:

* **Advance**
* Additional villain activations
* Minions with high **SCH**
* Side schemes with an **acceleration icon**
* Effects that place threat directly
* Effects that prevent threat removal
* Main schemes with multiple stages

In true solo, tracking whether **Advance** is still in the encounter deck is especially valuable.

Do not calculate only the most likely outcome. Maintain enough margin to survive a moderately bad encounter card.

### Damage Risk

Estimate the incoming damage:

```text
Villain ATK
+ boost icons
+ boost abilities
+ minion attacks
+ additional activations
+ indirect damage
```

Then assign a defensive answer to each expected attack:

* Defend with your identity
* Defend with another player's identity
* Block with an ally
* Use **Tough**
* Apply **Stunned** to the villain
* Prevent or reduce damage
* Cancel the attack
* Recover before the villain phase
* Defeat the attacking minion
* Flip to alter-ego, when threat permits it

Do not rely on drawing a low boost card unless you have no better option.

A weak defensive plan usually sounds like:

> "It should probably be fine."

It is rarely fine.

---

## 3. What Is Making the Board Worse?

Prioritize encounter cards that will continue creating problems.

A useful default priority order is:

1. Immediate loss conditions
2. Side schemes with dangerous icons
3. High-impact minions
4. Encounter card attachments and environments
5. Ordinary minions
6. Non-urgent threat
7. Villain damage

This order is not absolute. Evaluate the actual effect of each card.

### Dangerous Side Scheme Icons

#### Crisis Icon

While a crisis icon is in play, threat cannot be removed from the main scheme.

Clear it quickly when the main scheme is becoming dangerous.

#### Hazard Icon

A hazard icon causes an additional encounter card to be dealt during the villain phase.

Hazard becomes increasingly dangerous in multiplayer because the extra card affects the entire team's encounter-card economy.

#### Acceleration Icon

An acceleration icon increases the amount of threat placed on the main scheme during step one of the villain phase.

Leaving it in play creates a recurring threat penalty every round.

#### Amplify Icon

An amplify icon adds an additional boost icon to boost cards during enemy activations.

It increases the volatility of both attacks and schemes.

### Dangerous Minion Keywords

#### Guard

While you are engaged with a minion with **Guard**, you cannot attack the villain.

Defeat it if it interferes with a stage transition or lethal damage.

#### Patrol

While you are engaged with a minion with **Patrol**, you cannot thwart the main scheme.

Patrol can become more dangerous than Guard when the main scheme is close to completion.

### Evaluate Minions by Future Impact

A minion with 1 hit point and 4 ATK is not a minor problem.

Ask:

* How much damage or threat will it generate next round?
* Does it have a forced response?
* Does it gain attachments?
* Does it protect the villain?
* Does defeating it trigger another effect?
* Can an ally defeat it efficiently?
* Can I leave it alive without spending another card later?

The goal is not merely to remove cards from the table.

The goal is to remove the cards that create the greatest future cost.

---

## 4. Can I Safely Build My Engine?

Once the next villain phase is under control, invest in cards that improve future turns.

Typical engine pieces include:

* Resource generators
* Card draw
* Supports
* Upgrades
* Permanent cost reductions
* Readying effects
* Hero-specific setup cards
* Allies intended to remain in play
* Player side schemes that unlock important rewards

A resource generator played early may be used five or six times.

The same card played shortly before the game ends may never recover its initial cost.

Do not ask only:

> "Is this card powerful?"

Ask:

> "How many times am I likely to use this card before the game ends?"

### A Simple Setup Rule

Play an engine card when:

```text
The next villain phase is already covered
AND
the card will probably be used multiple times
AND
playing it does not create a new emergency
```

If playing a support means leaving a dangerous minion alive, the support may be too slow for the current board state.

---

## 5. Can I Safely Change Form?

Changing to alter-ego form is an economic decision, not merely a healing decision.

Alter-ego form may provide:

* A larger hand size
* Recovery
* Alter-ego actions
* Access to specific supports
* Identity-specific setup
* Safer card sequencing
* Protection from villain attacks

However, the villain will normally scheme instead of attacking.

Consider changing to alter-ego when:

* The villain is **Confused**
* The main scheme has a large threat margin
* **Advance** has already been discarded
* You can remove the expected threat next turn
* Your alter-ego abilities provide significant value
* Another player can control the threat
* Remaining in hero form creates a serious risk of defeat

### Multiplayer Form Management

Avoid having every player change to alter-ego form simultaneously unless the main scheme is completely safe.

A strong multiplayer rhythm is often:

* One player changes to alter-ego
* The other players remain in hero form
* The team manages the resulting threat
* Another player changes form on a later round

This allows players to recover and use alter-ego abilities without giving the villain several scheme activations at once.

---

## 6. What Should I Do With My Remaining Resources?

After survival, board control, and engine development are covered:

* Prepare your defense
* Use remaining identity abilities
* Clear low-priority encounter cards
* Set up future combinations
* Deal damage to the villain

This is when villain damage becomes efficient.

Damage is not unimportant. It is simply the part of the turn that should usually come after the board has been secured.

---

# Five Habits That Improve Your Win Rate

## 1. Mulligan Aggressively

Your opening hand should usually search for cards that improve several future turns.

Prioritize:

* Hero-specific setup cards
* Resource generators
* Card draw
* Essential supports
* Important upgrades
* Cheap allies
* Immediate answers to setup encounter cards

Frequently discard:

* Expensive attack events
* Situational defense cards
* Late-game damage cards
* Cards that cannot currently be played efficiently
* Duplicate setup pieces

An attack event discarded during the mulligan can return after your deck is reshuffled.

A resource generator that you fail to play early can never recover the turns during which it could have generated value.

### Opening Hand Question

Ask:

> "Which cards in this hand will still matter three rounds from now?"

Those are usually your best mulligan targets.

---

## 2. Do Not Hoard Cards Without a Specific Reason

At the end of the player phase, you may discard cards before drawing up to your hand size.

Keeping a card means seeing one fewer new card.

Keep a card only when it has a specific purpose, such as:

* Defending during the villain phase
* Completing a likely combination next turn
* Paying for an essential card
* Countering a known encounter effect
* Preserving a unique hero card
* Preparing a controlled villain stage transition

"This card might be useful later" is usually not a sufficient reason.

Cycling through your deck is often more valuable than protecting a merely decent card.

---

## 3. Calculate the Full Value of Allies

An ally's value is not limited to its ATK or THW.

An ally may provide:

* A **Response** or **Interrupt** when played
* One or more attacks
* One or more thwarts
* A block against an entire enemy attack
* A defeat response
* Trait synergy
* Card draw
* Resource generation
* Status effects
* Readying or healing effects

A cheap ally might:

1. Trigger an ability when played.
2. Thwart once or twice.
3. Block a villain attack.
4. Trigger another effect when defeated.

That is often exceptional value from a single card.

However, check for:

* **Overkill**
* Villain abilities that punish defeated allies
* Minions that cannot be blocked normally
* Effects that deal indirect damage
* Effects that attack multiple characters
* Allies that are more valuable when kept in play

Do not automatically sacrifice every ally.

Use ally blocks when the prevented attack is worth more than the ally's future activations.

---

## 4. Track the Important Encounter Cards

You do not need to memorize the entire encounter deck.

Track the cards that can radically change the villain phase:

* **Advance**
* Additional attacks
* Additional schemes
* Encounter cards with **Surge**
* Cards that deal additional encounter cards
* Villain-specific signature treacheries
* **Shadows of the Past**
* Your nemesis set
* Cards that place large amounts of threat
* Cards that remove status cards
* Cards that punish changing form

Also track your own player deck:

* Are your essential hero cards already in the discard pile?
* How close are you to reshuffling?
* Which attack events remain in your deck?
* Which defensive cards remain?
* Can you prepare a large damage turn?
* Will emptying your deck give you an additional encounter card?

Likewise, when the encounter deck empties, it is reshuffled and an acceleration token is placed on the main scheme.

Deck position is therefore part of threat and risk management, not just card counting.

---

## 5. Control Villain Stage Transitions

Do not defeat a villain stage merely because you can.

Before dealing the final damage to the current stage, check:

* The next stage's **When Revealed** ability
* Its ATK and SCH values
* Additional hit points
* New minions
* New attachments
* Status cards that may be discarded
* Encounter cards that may be dealt
* Side schemes that may enter play
* Whether the villain will activate before your next turn
* Whether the team can immediately answer the new board state

It is often correct to leave the villain at 1 hit point on the current stage.

Use the remaining time to:

* Clear side schemes
* Defeat minions
* Play supports and upgrades
* Heal
* Prepare allies
* Apply status cards
* Build a burst-damage hand

Then change the villain's stage when you are ready to handle its new effects.

### Exception

Do not delay the transition when:

* The current stage has a dangerous recurring ability
* The current stage becomes stronger over time
* The next stage is easier for your deck
* You are close to losing anyway
* The transition enables immediate lethal damage
* The scenario specifically rewards fast stage progression

---

# Default Target Priority

When several targets compete for your resources, use this general order:

| Priority | Target                                                                  |
| -------: | ----------------------------------------------------------------------- |
|        1 | An effect that can immediately lose the game                            |
|        2 | A side scheme with a crisis, hazard, acceleration, or amplify icon      |
|        3 | A minion with high ATK, high SCH, Guard, Patrol, or a dangerous ability |
|        4 | A harmful attachment or environment                                     |
|        5 | A player side scheme with a crucial reward                              |
|        6 | An ordinary minion                                                      |
|        7 | Non-urgent threat                                                       |
|        8 | The villain                                                             |

Change this order whenever the scenario, hero, or board state demands it.

---

# End-of-Turn Checklist

Before ending your turn, ask:

1. **Can we win right now?**
2. **Can the main scheme complete next round?**
3. **Can every player survive the expected attacks?**
4. **Have we dealt with the cards that generate recurring problems?**
5. **Can I play an engine card without creating an emergency?**
6. **Is changing to alter-ego form safe?**
7. **Am I keeping cards for a specific reason?**
8. **Am I triggering the next villain stage at the right time?**
9. **Have I prepared for the most dangerous encounter cards still in the deck?**
10. **Can my remaining resources be converted into villain damage?**

---

# Condensed Decision Tree

```text
Can we win this turn?
├── Yes → Confirm Guard, Tough, Retaliate, and the next villain stage.
│         Then deal lethal damage.
└── No
    │
    ├── Can the main scheme complete next round?
    │   ├── Yes → Remove threat, defeat scheming minions, or apply Confused.
    │   └── No
    │
    ├── Can a player be defeated next round?
    │   ├── Yes → Prepare a defense, ally block, Tough, Stunned, healing,
    │   │         damage prevention, or defeat the attacking enemy.
    │   └── No
    │
    ├── Are encounter cards generating recurring problems?
    │   ├── Yes → Clear dangerous side schemes, minions, attachments,
    │   │         and environments.
    │   └── No
    │
    ├── Can we safely improve our engine?
    │   ├── Yes → Play resource generators, supports, upgrades, and allies.
    │   └── No
    │
    ├── Is changing form safe and valuable?
    │   ├── Yes → Change form and use alter-ego abilities.
    │   └── No → Remain in hero form.
    │
    └── Spend remaining resources on setup or villain damage.
```

---

# The Strategic Summary

Marvel Champions is not primarily a damage race.

It is a game of controlling how many problems the encounter deck can create.

A strong player repeatedly asks:

> **What will make the next round harder, and can I remove it now?**

Once the board stops getting worse, your engine begins producing more resources than the villain can efficiently answer.

That is the moment when you stop surviving and start winning.

---

# Traduction dans le bot (`tools/autoplay.py`)

Ce que le simulateur applique aujourd'hui, et ce qui reste à faire. Cette
section est la seule partie maison du document ; le reste est la référence
d'origine.

| Règle du cadre | État dans le bot |
|---|---|
| Priorité des cibles : manigances secondaires à icône avant le vilain | fait |
| L'icône Crise interdit de retirer de la menace du plan principal | fait |
| Juger un sbire sur son ATK et son SCH, pas sur ses PV | fait |
| Le vilain à portée de tomber passe devant tout le reste | fait |
| Deux horloges : défaite contre victoire | fait |
| Le repli fait maniganer tous les ennemis, pas seulement le vilain | fait |
| Bloquer avec un allié plutôt qu'encaisser du héros | fait |
| Ne pas épuiser l'identité pour un gain mineur | fait |
| Mulligan : jeter les cartes chères, garder le moteur | partiel, jette au-dessus de 4 de coût |
| Contrôler le passage de stade du vilain | à faire |
| Ne pas garder de cartes sans raison précise | à faire |
| Compter les dégâts entrants pour dimensionner la défense | à faire |
| Suivre les cartes de rencontre dangereuses restantes | à faire |

Repère mesuré le 4 août 2026 : contre Rhino en solo, il faut infliger 29 dégâts
au total (stade I à 14 PV, stade II à 15 PV) pendant que le plan principal se
remplit à 7 points, plus 1 par round d'escalade. Le bot en infligeait alors 5 à
8, ce qui situe l'écart à combler.
