# Hellcat (jakxin) : relevé des cartes et arbitrages

**Source** : Drive `1tzW3PJD71-pK6MhQ7MpgNYrd1uWVcZpS`, 41 fichiers, auteur
**jakxin** (« MC Custom Content »). Scans 1500 × 2150. Téléchargés dans le
scratchpad `drive/hellcat/`.

**Préfixe** : `hc` (libre, vérifié). **Pack** : `hellcat`. **Set** :
`172. Custom (Hellcat)`.

## Décisions prises avec l'utilisateur (11/09/2026, une à une)

| Question | Réponse |
|---|---|
| Périmètre | **Pack complet, deck imprimé compris** : identité, 15 signature, obligation, némésis, ET les cartes custom du deck (Firestar, Monica, Green Hell, Hell-Iron, Divas, reskins) |
| Reskins (Energy, Genius, Strength, Chase Them Down) | **Doublons avec l'illustration de jakxin**, copies conformes des officielles |
| Black Cat (listée, absente du dossier) | **Laissée de côté** : le deck fait 24 cartes d'aspect/basiques au lieu de 25 |
| She-Hulk, alliée signature alternative | **Deux decks de départ** : `hellcat` (Iron Man) et `hellcat_she_hulk` |
| Outer Demons, « Hellcat gains villainous » | **Fidèle** : Hellcat reçoit une vraie carte boost à chaque activation de base, icônes ajoutées, effet Boost annulé, soin de 1. Nouveau mécanisme moteur |
| Réponse de Hellcat, « attach that card » | **Événements seulement** (notice de l'auteur). Tooltip FR/EN qui le précise |
| Firestar, « ★ Interrupt » | **Interrupt normal**, l'étoile n'ajoute rien |
| Iron Man, « limit once per turn » | Tranché seul (technique) : **une fois par round** |

## Identité

**hc001a * Hellcat** (Hero) HP 11, ATK 2, THW 2, DEF 2, HS 5. AVENGER. PSIONIC.
> Response: After you play a card with a printed [mental] resource, attach that card to Hellcat (to a maximum of 3). (Limit twice per round.)
> *Empowered* — Resource: Discard 1 attached card from Hellcat → generate a [mental] resource.

**hc001b * Patsy Walker** (AlterEgo) HP 11, REC 3, HS 6. PSIONIC.
> *Mental Potential* — Interrupt: When the villain schemes against you, draw 1 card → if that card has a printed [mental] resource, reduce the amount of threat placed by 1.

## Signature (15 cartes, 11 distinctes)

| id | Carte | Type | Coût | RES | Traits | Texte |
|---|---|---|---|---|---|---|
| hc002 | * Iron Man (Tony Stark) | Ally | 3 | B | AVENGER | THW 2 (1*), ATK 2 (1*), HP 3. Response: After Iron Man uses a basic power, spend a [mental] resource and choose 1 (limit once per turn): • Ready your identity. • Draw 2 cards. |
| hc003 | * Cat Suit | Upgrade | 2 | Y | ARMOR, INFERNAL | You get +3 hit points. Hero Interrupt: When you make a basic thwart, exhaust Cat Suit and spend a [mental] resource → you get +2 THW and ignore the patrol keyword for this thwart. |
| hc004 | * Hellcat's Claws | Upgrade | 2 | R | WEAPON | Hellcat gets +1 ATK. Hero Interrupt: When you make a basic attack, exhaust Hellcat's Claws and spend a [mental] resource → you get +2 ATK and gain piercing for this attack. |
| hc005 ×3 | Helluva Punch | Event | 2 | B | ATTACK | Hero Action (attack): Deal 4 damage to an enemy. If you paid for this using only [mental] resources, deal an additional 2 damage to that enemy, and this attack gains overkill. |
| hc006 ×2 | On the Prowl | Event | 2 | B | TACTIC, THWART | Hero Action (thwart): Remove 4 threat from a scheme. If you paid for this using only [mental] resources, remove an additional 2 threat from that scheme, and this card ignores the crisis icon and patrol keyword. |
| hc007 ×2 | Cat-Like Reflexes | Event | 1 | B | DEFENSE | Hero Interrupt (defense): When Hellcat defends against an attack → you get +2 DEF for this defense. Search your discard pile for a card not named Cat-Like Reflexes with a printed [mental] resource and add it to your hand. |
| hc008 ×2 | Illusion | Event | 1 | B | PSIONIC, TACTIC | Action: Choose one: • Heal a friendly character by 1 for each card attached to your identity. • Remove 1 threat from a scheme for each card attached to your identity. |
| hc009 | * Mental Training | Upgrade | 2 | Y | PSIONIC, SKILL | Hero Interrupt: When you pay for an ATTACK or THWART event using only [mental] resources, that event deals 1 additional damage or removes 1 additional threat. |
| hc010 | * Outer Demons | Upgrade | 2 | G | CONDITION, INFERNAL | Hellcat gains villainous. Interrupt: When a boost card given to Hellcat is turned faceup, cancel its "Boost" ability. Then, heal 1 damage from Hellcat. Forced Response: After you change form, discard this card. |
| hc011 | * Hedy Wolfe | Support | 1 | B | BEST FRENEMY | Alter-Ego Action: Exhaust Hedy Wolfe → search your discard pile for a card with a printed [mental] resource and attach it to your identity. |
| hc012 | * She-Hulk (Jennifer Walters) | Ally | 3 | B | AVENGER, GAMMA | THW 2 (1*), ATK 2 (1*), HP 3. She-Hulk gets +1 hit point for each [mental] resource used to pay for her. Response: After She-Hulk attacks and defeats a minion, search your discard pile for an event with a printed [mental] resource and add it to your hand. *(Alliée signature alternative, deck `hellcat_she_hulk`.)* |

Les exemplaires multiples ont des scans différents seulement par le numéro
de pied de carte (« 5 / 6 MC Custom Content ») : un seul scan par `card_id`.
« Outer Demons full » est une variante plein-art du même texte : non retenue.

## Obligation

**hc013 Mental Episode** (Obligation) Boost 2, GiveTo Patsy Walker.
> Flip to alter-ego form and discard all cards attached to your identity. Deal 1 damage to your identity for each discarded this way. If at least 2 cards were discarded from your identity this way, remove this card from the game. If not, discard this card.

## Set némésis « Hellcat Nemesis » (5 cartes, 4 distinctes)

| id | Carte | Type | Desc | Texte |
|---|---|---|---|---|
| hc014 | Battle for a Soul | SideScheme | StartingThreat 2, Boost 2 | Blackheart gets +X SCH and Daimon Hellstrom gets +X ATK, where X is the number of cards attached to Hellcat. Forced Interrupt: When Blackheart or Daimon Hellstrom activate, they also activate against the player the other is engaged with. |
| hc015 | * Blackheart | Minion | HP 4, SCH 1, ATK 2, Boost 2, Toughness, Villainous, DEMON | Blackheart cannot be in the same play area as Daimon Hellstrom. When Revealed: If Daimon Hellstrom is in your play area, Blackheart engages with the next player in turn order. If he cannot, this card gains surge. |
| hc016 | * Daimon Hellstrom | Minion | HP 4, SCH 3, ATK 1, Boost 2, Stalwart, Villainous, DEMON | Daimon Hellstrom cannot be in the same play area as Blackheart. When Revealed: If Blackheart is in your play area, Daimon Hellstrom engages with the next player in turn order. If he cannot, this card gains surge. |
| hc017 ×2 | Hot as Hell | Treachery | Boost 2, INFERNAL | When Revealed: Discard an upgrade you control. Take damage equal to that card's resource cost. |

Insert de l'auteur, en solo : on engage l'un des deux sbires au choix,
l'autre gagne surge (ne peut pas entrer en jeu). Le texte des cartes le
rend tel quel : « next player in turn order » en solo, c'est soi-même →
« cannot » → surge.

## Cartes custom hors pack, dans le deck imprimé

| id | Carte | Type | Coût | RES | Classe | Texte |
|---|---|---|---|---|---|---|
| hc018 | * Firestar (Angelica Jones) | Ally | 3 | B | Aggression | X-MEN. THW 1 (1*), ATK 1 (1*), HP 3. Firestar enters play with 1 fire counter on her for each [mental] resource used to pay for her. Interrupt: When Firestar attacks, remove 1 fire counter from her → deal 2 damage to an enemy. |
| hc019 | * Captain Marvel (Monica Rambeau) | Ally | 3 | B | Basic | AERIAL. AVENGER. THW 2 (1*), ATK 2 (1*), HP 3. Interrupt: When Captain Marvel uses a basic power, spend 1 resource of any type → search your discard pile for a card with a matching printed resource and shuffle it into your deck. |
| hc020 | Green Hell | Event | 1 | R | Basic | Team-Up (Hellcat and She-Hulk). Max 1 per deck. Hero Action: Ready Hellcat and She-Hulk. They get +2 ATK until the end of the phase. |
| hc021 | Hell-Iron | Event | 1 | Y | Basic | Team-Up (Hellcat and Iron Man). Max 1 per deck. Hero Action: Ready Hellcat and Iron Man. Search your deck and discard pile for an upgrade and add it to your hand. |
| hc022 | Divas | Event | 0 | Y | Basic | Team-Up (any 2 of Black Cat, Firestar, Hellcat, and Monica Rambeau). Max 1 per deck. Hero Action: Search your discard pile for 3 cards, each with a different printed resource. Add 1 to your hand and shuffle the rest into your deck. *(Pas dans le deck imprimé.)* |
| hc023 | Chase Them Down | Event | 0 | B | Aggression | THWART. Response (thwart): After your hero attacks and defeats an enemy, remove 2 threat from a scheme. *(Reskin de 01052.)* |
| hc024 | Energy | Resource | | YY | Basic | Max 1 per deck. *(Reskin de 01088.)* |
| hc025 | Genius | Resource | | BB | Basic | Max 1 per deck. *(Reskin de 01089.)* |
| hc026 | Strength | Resource | | RR | Basic | Max 1 per deck. *(Reskin de 01090.)* |

⚠ Divas : `TeamUp` du moteur attend « A;B » (les deux en jeu). « Any 2 of 4 »
demande une condition maison. Et l'aspect de Divas n'est pas imprimé :
BASIC en bas de carte, comme Green Hell et Hell-Iron.

## Deck de départ imprimé (recopié tel quel, Black Cat en moins)

Aspect Agressivité : Firestar (hc018), * She-Hulk (10013), * Tigra (01051),
Chase Them Down ×3 (hc023), Precision Strike ×3 (35018), Psi-Bow Attack ×3
(41030), Psychic Assault ×2 (34032), Combat Training (01057), Honed Technique
(28017).
Basiques : Captain Marvel Monica (hc019), Green Hell (hc020), Hell-Iron
(hc021), Energy (hc024), Genius (hc025), Strength (hc026), * Quincarrier
(08023), * Psimitar (40029).
Total : 24 cartes (25 avec Black Cat).

Deux fichiers : `deck/starter/hellcat.json` (hero_deck avec hc002 Iron Man)
et `deck/starter/hellcat_she_hulk.json` (hc012 She-Hulk à la place).

## Points d'attention pour le script

- **Mécanique neuve** : un héros qui reçoit une carte boost (Outer Demons).
  À concevoir dans le moteur, avec cas plateau (la carte boost doit se voir).
- **On the Prowl** ignore la Crise **si payée en mental seulement** : même
  cas limite que `15012` Crisis Averted (voir `mots-cles/crisis.md`) :
  `SetIgnoreKeyword('Crisis')` inconditionnel, la résolution tranche.
- **« paid using only mental »** : `effect.GetPaidResources()`, modèle
  `bt005`, `12031`.
- **Cartes attachées à l'identité** : c'est le compteur de tout le pack
  (Illusion, Battle for a Soul, Mental Episode, Empowered).
- Homonymes : 09039 / 23002 Iron Man, 10013 / 62021 She-Hulk, 04032 / 23013 /
  61015 Captain Marvel, 01052 Chase Them Down, 01088-01090 ressources.
