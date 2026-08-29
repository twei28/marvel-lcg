# Squirrel Girl — Cartes du set custom

*Extrait le 28/08/2026 directement de `data/cards.json` (source de vérité en jeu, pas la spec de conception initiale — le texte a évolué pendant l'implémentation sur plusieurs cartes, et « Call the Squirrels » a été rééquilibré le 28/08/2026, voir §15 de `squirrel_girl_complete_custom_hero_pack_and_starter_deck.md`).*

23 cartes de set (identité, Squirrel deck, deck signature, obligation, set némésis) + le deck de départ recommandé.

---

## Identité

### Squirrel Girl — Hero
`sg001a` · ATK 1 · THW 1 · DEF 2 · PV 10 · Main 5 · Traits : AVENGER

*Unbeatable Army* — **Hero Response** : après avoir dépensé un Écureuil, soit inflige 1 dégât à un ennemi, soit retire 1 menace d'une manigance. (Limite une fois par phase.)
*Squirrel Aid* — **Resource** : défausse un allié [[SQUIRREL]] que tu contrôles → génère 1 ressource [wild]. À dépenser uniquement pour payer une carte Squirrel Girl. (Limite 1 écureuil par carte jouée.)

### Doreen Green — AlterEgo
`sg001b` · REC 3 · PV 10 · Main 6 · Traits : CIVILIAN, STUDENT

Doreen Green commence la partie avec un deck Écureuil. *(Mets de côté les 6 alliés [[SQUIRREL]], mélangés. Quand un effet appelle un écureuil, révèle le dessus du deck Écureuil et mets-le en jeu épuisé, sous ton contrôle. Si le deck Écureuil est vide, mélange sa défausse pour en former un nouveau.)*
*Squirrel Speech* — **Alter-Ego Action** : épuise Doreen Green → appelle 1 écureuil. (Limite une fois par round.)
*Squirrel Aid* — **Resource** : défausse un allié [[SQUIRREL]] que tu contrôles → génère 1 ressource [wild]. À dépenser uniquement pour payer une carte Squirrel Girl. (Limite 1 écureuil par carte jouée.)

---

## Le Squirrel deck (6 alliés, mis de côté au setup)

Un allié SQUIRREL ne compte pas dans la limite d'alliés, ne peut pas défendre, ne peut recevoir aucune amélioration, ne peut être ciblé/renforcé que par des cartes du set Squirrel Girl, et rejoint la défausse Écureuil quand il quitte le jeu.

| Carte | ATK | THW | PV | Capacité |
|---|---:|---:|---:|---|
| * Tippy-Toe (`sg002`) | 1* | 1* | 2 | Response : à son entrée en jeu, regarde les 2 dessus du deck Écureuil, remets-les dans l'ordre voulu |
| * Monkey Joe (`sg003`) | 1* | – | 1 | Response : après avoir vaincu un minion, appelle 1 écureuil |
| The Lookout (`sg004`) | – | 1* | 1 | Aucune capacité imprimée |
| The Bruiser (`sg005`) | – | – | 2 | Interrupt : quand un autre SQUIRREL subirait des dégâts conséquents, épuise The Bruiser → 1 de ces dégâts lui est infligé à la place |
| The Forager (`sg006`) | – | – | 1 | Response : quand tu le dépenses, regarde les 2 dessus de ton deck, défausses-en 1 ou remets-les dans l'ordre voulu |
| The Gatherer (`sg007`) | – | – | 1 | Response : quand tu le dépenses, soigne 1 dégât de Squirrel Girl |

*(`*` = valeur qui ne peut être augmentée par une carte hors du set Squirrel Girl.)*

---

## Deck signature (15 cartes)

| Carte | Type | Qté | Coût | Ressource |
|---|---|---:|---:|---|
| Nancy Whitehead | Ally | 1 | 3 | Mental |
| Squirrel Girl's Costume | Upgrade | 1 | 3 | Physical |
| Prehensile Tail | Upgrade | 1 | 2 | Energy |
| Central Park | Support | 1 | 3 | Mental |
| Network of Trees | Support | 1 | 2 | Wild |
| Call the Squirrels | Event | 2 | 2 | Mental |
| Squirrel Swarm | Event | 3 | 2 | Physical |
| Recon Team | Event | 2 | 2 | Mental |
| Unbeatable! | Event | 2 | 2 | Energy |
| Nuts! | Resource | 1 | – | 2 Physical |

**Total : 15 cartes**

### * Nancy Whitehead — Ally
`sg008` · Coût 3 (Mental) · ATK 1* · THW 1* · PV 2 · Traits : CIVILIAN

**Response** : après l'entrée en jeu de Nancy Whitehead, appelle 1 écureuil.

### * Squirrel Girl's Costume — Upgrade
`sg009` · Coût 3 (Physical) · Traits : ITEM, SUIT

Squirrel Girl obtient +1 ATK.
**Hero Response** : après qu'un minion est vaincu, appelle 1 écureuil. (Limite une fois par round.)

### * Prehensile Tail — Upgrade
`sg010` · Coût 2 (Energy) · Traits : SKILL

**Resource** : épuise Prehensile Tail → génère 1 ressource [wild]. À dépenser uniquement pour payer une carte Squirrel Girl.

### * Central Park — Support
`sg011` · Coût 3 (Mental) · Traits : LOCATION

**Action** : épuise Central Park → si tu contrôles moins de 3 alliés SQUIRREL, appelle 1 écureuil.

### * Network of Trees — Support
`sg012` · Coût 2 (Wild) · Traits : NETWORK

**Interrupt** : quand tu appellerais un écureuil, épuise Network of Trees → regarde les 2 dessus du deck Écureuil, appelle l'un des deux et place l'autre au fond du deck Écureuil.

### Call the Squirrels — Event ×2
`sg013` · Coût 2 (Mental) · Traits : TACTIC

**Action** : appelle 2 écureuils. 1 des deux entre en jeu prêt.
*(rééquilibré le 28/08/2026 : les 2 entraient prêts à l'origine — aucune carte officielle ne fait entrer un allié invoqué directement prêt, voir le journal d'équilibrage.)*

### Squirrel Swarm — Event ×3
`sg014` · Coût 2 (Physical) · Traits : ATTACK

**Hero Action (attack)** : inflige 3 dégâts à un ennemi. Si tu as dépensé un écureuil pour jouer cette carte, inflige 3 dégâts supplémentaires à cet ennemi.

### Recon Team — Event ×2
`sg015` · Coût 2 (Mental) · Traits : THWART

**Hero Action (thwart)** : retire 3 menace d'une manigance. Si tu as dépensé un écureuil pour jouer cette carte, retire 1 menace d'une manigance différente.

### Unbeatable! — Event ×2
`sg016` · Coût 2 (Energy) · Traits : DEFENSE

**Hero Interrupt (defense)** : quand Squirrel Girl défend contre une attaque, elle obtient +2 DEF pour cette attaque (+3 si tu as dépensé un écureuil pour jouer cette carte). Si cette attaque n'inflige aucun dégât à Squirrel Girl, elle est readied.

### Nuts! — Resource ×1

`sg017` · Génère 2 ressources Physical

**Response** : quand tu dépenses cette carte pour payer une carte Squirrel Girl, appelle 1 écureuil.

---

## Obligation

### Surprise Exam
`sg018` · Boost 2 · Donnée au joueur de Doreen Green

Tu peux passer en forme alter-ego. Choisis :
- Épuise Doreen Green et défausse une carte à ressource [mental] imprimée de ta main → retire Surprise Exam du jeu.
- Défausse 1 allié [[SQUIRREL]] que tu contrôles. Si tu ne peux pas, défausse 1 carte aléatoire de ta main. Défausse cette obligation.

---

## Set némésis (5 cartes)

| Carte | Type | Qté |
|---|---|---:|
| Ratatoskr | Minion | 1 |
| Discord in the Branches | SideScheme | 1 |
| Poisoned Rumors | Treachery | 2 |
| Ratatoskr's Whispers | Attachment | 1 |

### * Ratatoskr — Minion
`sg019` · SCH 2 · ATK 2 · PV 5 · Boost 2 · Traits : ASGARDIAN, CREATURE

**Forced Interrupt** : quand Ratatoskr s'active contre toi, défausse 1 allié [[SQUIRREL]] que tu contrôles. Si tu ne peux pas, Ratatoskr obtient 1 carte boost supplémentaire pour cette activation.

### Discord in the Branches — SideScheme
`sg020` · Menace de départ 2/joueur · Icône Crise (le vilain ne peut pas voir sa manigance réduite tant que ce side scheme est en jeu)

Tant que ce side scheme est en jeu, les capacités imprimées des alliés SQUIRREL sont blanches. Leurs THW, ATK et PV restent inchangés.
**Forced Response** : après l'entrée en jeu d'un allié [[SQUIRREL]], place 1 menace ici. (Limite une fois par round.)

### Poisoned Rumors — Treachery ×2
`sg021` · Boost 1

**When Revealed** : défausse 2 alliés [[SQUIRREL]] que tu contrôles. Si tu ne peux pas, place 2 menace sur Discord in the Branches (ou sur la manigance principale si ce side scheme n'est pas en jeu).
[star] **Boost** : après cette activation, épuise 1 allié [[SQUIRREL]] que tu contrôles.

### Ratatoskr's Whispers — Attachment
`sg022` · Boost 1 · Traits : CONDITION

S'attache à ta carte identité. Tu ne peux pas dépenser d'alliés [[SQUIRREL]].
**Alter-Ego Action** : épuise Doreen Green et défausse une carte à ressource [mental] imprimée de ta main → défausse Ratatoskr's Whispers.
[star] **Boost** : défausse 1 allié [[SQUIRREL]] que tu contrôles. Si tu ne peux pas, cette activation obtient +1 ATK et +1 SCH.

---

## Deck de départ recommandé — Aggression (25 cartes hors signature)

Tel que réellement configuré dans `deck/starter/squirrel_girl.json`.

### Alliés — 5

| Qté | Carte | Coût |
|---:|---|---:|
| 1 | * Angela (`18011`) | 0 |
| 1 | * Wasp (`13012`) | 0 |
| 1 | * Spider-Girl (`04040`) | 2 |
| 1 | * Tigra (`01051`) | 3 |
| 1 | * Brawn (`10011`) | 3 |

### Événements — 9

| Qté | Carte | Coût |
|---:|---|---:|
| 2 | Looking for Trouble (`16043`) | 0 |
| 2 | Spoiling for a Fight (`54016`) | 0 |
| 2 | Skilled Strike (`09037`) | 0 |
| 2 | One by One (`28014`) | 1 |
| 1 | "Bring It!" (`19030`) | 0 |

### Améliorations et soutiens — 6

| Qté | Carte | Coût |
|---:|---|---:|
| 1 | Martial Prowess (`10018`) | 2 |
| 1 | Combat Training (`01057`) | 2 |
| 1 | Aggressive Conditioning (`56013`) | 3 |
| 2 | Battle Fury (`06018`) | 1 |
| 1 | * Hall of Heroes (`06017`) | 2 |

### Ressources — 5

| Qté | Carte |
|---:|---|
| 2 | The Power of Aggression (`01055`) |
| 1 | Energy (`01088`) |
| 1 | Genius (`01089`) |
| 1 | Strength (`01090`) |

---

## Récapitulatif du deck complet (40 cartes)

| Catégorie | Cartes |
|---|---:|
| Cartes signature Squirrel Girl | 15 |
| Alliés Aggression | 5 |
| Événements Aggression | 9 |
| Améliorations et soutiens Aggression | 6 |
| Ressources | 5 |
| **Total deck joueur** | **40** |

Le Squirrel deck (6 cartes) est séparé et ne compte pas dans les 40 cartes minimum.
