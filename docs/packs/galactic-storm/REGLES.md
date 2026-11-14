# Galactic Storm : règles de campagne et de scénario (lot GS-0)

Source : livret 1.2 (24 pages, `sources/z2/Campaigns/.../rulebook 1.2_compressed.pdf`, relu page par page le 20/10/2026),
inserts de scénario (`sources/z1`, `z2`, `z3`) et page 24 du livret (journal de campagne). Texte du livret en anglais, résumé
fidèle ; les numéros de page sont ceux du livret 1.2. Les écarts avec le livret 1.1 sont en fin de document.
Les deux livrets sont des images (aucun texte extractible) : tout a été lu à l'œil.

Numérotation : les cartes portent un numéro imprimé unique à l'échelle du coffret (305 au total d'après le livret p.2). Le
livret s'y réfère (cartes 224 à 236, solutions des cartes intruses 81, 130, 139, 181/182). Voir INVENTAIRE.md.

## 1. Contenu (p.2)

305 cards: 109 player cards, 24 villain cards, 172 encounter cards. Set symbol: a ringed planet. Five scenarios, two
pre-built player decks (Binary / Aggression, Quasar / Protection), two interludes, one epilogue. Credits (p.23) : conception
Kajislav ; développement additionnel : communauté Homebrew de Marvel Champions LCG ; relecture Lord_Havok et Phenexian ;
spécialistes des règles Veral et Nashman88 ; conception graphique Kajislav, Man-3, Merlin, FuManchuToo, CommCody103 ; cartes
couvertures Kajislav et Man-3 ; gabarits Hitch, Man-3 et Kajislav.

## 2. Mots-clés mis en avant (p.3)

Mot-clé nouveau dans cette extension : Honorary (*). Liste du livret (texte 1.2) :

- Assault: when a character makes a basic thwart on a scheme with the assault keyword, that character uses its ATK instead
  of its THW. If that character is an ally, it takes the consequential damage listed under its ATK instead of its THW after
  the thwart.
- Hinder X: when a card with hinder X enters play, place X threat on that card.
- Honorary *: an ally with the honorary keyword has the team trait(s) of your identity (see page 9 for the list of team
  traits [sic : le livret dit « page 9 », la liste est p.7]). An ally with honorary retains these traits in every game area.
- Linked (Card Title): cards with linked cannot be included in a player's deck. Instead they are set aside at the start of
  the game if any player's deck includes the card that brings the linked cards into play. Linked cards do not count toward
  the minimum or maximum deck size.
- Patrol: while any minions with patrol are engaged with a player, that player cannot use cards they control to thwart the
  main scheme.
- Permanent: a card with permanent cannot be defeated, leave play, or have any part of its text box blanked.
- Piercing: an attack with piercing discards any tough status cards from the attacked character before dealing damage.
- Ranged: an attack with ranged ignores the retaliate keyword.
- Requirement (Resources): a card with the requirement keyword cannot be played unless each resource of the specified type
  is spent while paying for that card's cost.
- Setup: a card with setup begins the game in play.
- Steady: a character with steady can have one additional stunned status card and one additional confused status card. That
  character is not stunned unless they have two stunned status cards, and is not confused unless they have two confused
  status cards. After that character's activation is replaced by a status card effect, remove all status cards of that type
  from that character.
- Teamwork (TRAIT): after a minion with teamwork enters play and engages a player, if there is at least one other minion
  that shares the specified trait in play, the minion that just entered play activates against the player it is engaged with.
- Temporary: discarded at the end of the round.
- Victory X: when a card with victory X is defeated, place it in the victory display instead of its owner's discard pile.
- Villainous: when a minion with villainous activates, give it a facedown boost card from the top of the encounter deck. When
  you resolve that minion's activation, turn the boost card faceup, resolve any boost ability on that card, and apply its boost
  icons to the minion's stats for this activation. Discard the boost card after the activation.
- Vulnerable: when a character with vulnerable becomes stunned or confused, that character is immediately discarded. That
  character is not considered defeated, even if it is simultaneously dealt enough damage to defeat it.

Mots-clés avec une fiche existante dans `docs/reference/mots-cles/` selon l'analyse du 06/09 (à revérifier au lot GS-11) ;
Honorary (traits d'équipe), Assault, Linked, Requirement, Vulnerable, Teamwork et Steady sont à contrôler un par un.

## 3. Règles additionnelles (p.4)

- "Find": search each area where the card could be found (play area, set-aside area, player deck, discard pile, encounter
  deck, etc.). Do not search unnecessarily if the location is known. Do NOT look at facedown encounter cards currently dealt
  to players.
- "Tuck": place the tucked card faceup under the other card. The tucked card is not in play. When a card leaves play, any
  cards tucked under it are discarded.
- Amplify icon: when a boost card is turned faceup during an enemy activation, add one additional boost icon to that card for
  each amplify icon in play.
- Attacks against allies: when a villain or minion attacks an ally directly, any undefended damage from that attack is placed
  on the ally that was attacked. Boost abilities that refer to "you" refer to the player who controls the attacked ally ;
  abilities triggering when the attacking enemy "attacks you" do not trigger ; players may defend as normal by declaring a hero
  or an ally as the defender ; if the attack has overkill and defeats an ally, excess damage is dealt to the identity of the
  player who controlled the defeated ally.
- Player side scheme (new card type): played from hand during the player's turn by paying its resource cost, placed next to
  the main scheme with threat equal to its starting threat value. Works like an encounter side scheme but is a player card and
  is subject to the PLAYER SIDE SCHEME LIMIT: at most one in play if one or two players started the game, at most two if three
  or four started. If the limit is exceeded, the first player chooses and discards player side schemes from play to their
  owners' discard piles until under the limit. All player side schemes of this product have victory X (they go to the victory
  display when defeated).
- Victory display: out-of-play area shared by all players ; cards there follow the standard rules for out-of-play cards.

## 4. Mode campagne (p.5 à 7)

- Each scenario can be played individually, or together as one campaign. To complete the campaign the players must win all
  five scenarios in numerical order, from #1 Kree Sentry to #5 Supreme Intelligence.
- Unlike other campaigns, players do NOT choose a single hero. Each player plays a total of THREE different heroes throughout
  the campaign ; the Campaign Instructions say when to change hero between scenarios.
- Each player is free to change aspects and alter their deck between scenarios (deck customization rules of the Marvel
  Champions Rules Reference), plus any restriction specified by the Campaign Instructions.
- To play a scenario in campaign mode: set up as normal, then follow that scenario's setup instructions in the order listed.
  When the game ends, if the players won, follow the victory instructions in order. If they lost, they may reset the scenario
  and try again with no penalty.
- Campaign-specific cards: cards 224 to 236 were created for this campaign. They cannot be in any deck unless playing the
  campaign and instructed to add them. Cards 224 to 226 do not count toward a player's minimum or maximum deck size.
  (Card 224 = Rick Jones, BASIC / CAMPAIGN, 0 cost ally, Honorary, civilian ; vu sur le scan.)
- Campaign log: p.24 of the rulebook (reproduction en `z2/.../OGS rulebook page 24.png`). Colonnes Player #1 à #4 : First /
  Second / Third Identity, chacune avec « Remaining hit points » ; case « Unique Cards (+) » par joueur ; « Recruited Allies »
  (Scenarios #1-4) ; « Time Pressure » (Scenarios #2-4) ; « Odd Cards » (Scenario 1 à 4 : « Card number: »). Le livret renvoie à
  un dossier Google Drive de l'auteur pour une copie imprimable.

### Prohibited cards (p.6)

In scenarios #2-4, during deckbuilding, players cannot include a unique card (+) that "matches" any unique card recorded in the
campaign log (see the unique icon in the Marvel Champions Rules Reference v1.7, p.44). The identity is included in this
evaluation.

### Card replacement (p.6)

In scenarios #2-4, if a player chooses a hero who has a unique card among their identity-specific cards that "matches" a unique
card recorded in the campaign log (identity included), that player must replace that card with a campaign identity-specific card
of their choice from the Galactic Storm set that does not "match" any unique card recorded in the log. Cards from the Galactic
Storm set are considered identity-specific cards. When a card refers to an identity-specific card (even by the hero title), it
also applies to the card from the Galactic Storm set included in that player's deck. Exemple du livret : Doctor Pym, carte
IDENTITY-SPECIFIC / CAMPAIGN, imprimée avec le numéro 230 : « specific to the identity whose deck it was included in ».

### Odd cards (p.6, texte 1.2)

Optional mystery. Each of the first four scenarios contains one card that seems out of place. During a scenario players may
study and discuss any card normally. If the players win, they may no longer study the cards included in the scenario ; they
may still discuss them to determine which was the "Odd card". Entirely optional, no effect on the campaign course, no penalty
for a wrong guess. The victory instructions direct players to record the card number of the group's guessed "Odd card".
During setup of the final scenario, players gain access to one additional ally for each correct guess recorded. These allies
are available only during the Galactic Storm campaign. Solutions (p.19) : 81, 130, 139, 181/182.

### Time pressure (p.6)

In scenarios #2-4, the number of rounds it takes to win matters ; fewer rounds, better starting position in the final
scenario. Players can use the hit point dial to track rounds (« game round dial » placed next to the villain's hit point dial).

### Expert campaign (p.7)

Setup and Victory instructions preceded by "Expert Campaign Only" are ignored unless playing an expert campaign.
- Persistent damage: record remaining hit points in the log after each victory ; this sets the starting hit points of the next
  scenario with the same identity. If the remaining hit points exceed the base hit points, record the base value.
- Elimination and victory: if a player is defeated during a scenario their teammates go on to win, the defeated player does not
  participate in the Victory steps. During the Setup of the next scenario where the defeated identity is chosen, place an
  acceleration token on the main scheme and restore that identity to full hit points.

### Team traits (p.7)

Honorary refers to team traits (those that refer to a team affiliation). List of the livret: Avenger, Agent of Atlas, Champion,
Deadpool Corps, Defender, Dora Milaje, Excalibur, Guardian, Hero for Hire, Hydra, Nova Corps, Posse, S.H.I.E.L.D., Space Knight,
Starjammer, X-Factor, X-Force, X-Men, Web-Warrior, "including any other custom or future-released trait that can be considered
a team trait". (19 traits.)

## 5. Imperial Guard, modulaire (p.8)

Used throughout the campaign. 23 encounter cards ; whenever the set is chosen for a scenario, only nine cards are included :
choose one random environment, six random minions and both treacheries ; put the environment into play ; shuffle the other eight
encounter cards into the encounter deck with the other sets. Elsewhere it can be used like any encounter set. En campagne : la
victoire de chaque scénario où il est utilisé retire de la campagne chaque carte non-traîtrise de l'ensemble utilisée (scénarios 1
et 2 ; l'insert du scénario 4 et le scénario 3 ne le mentionnent pas dans les instructions de victoire).

## 6. Nega-Bomb, modulaire (p.8)

Includes the Nega-Bomb side scheme, which has setup (starts in play). Can be included in any scenario but does not count toward
the number of modular sets required.

## 7. Scénario 1 : Kree Sentry (p.9 à 10)

Villain deck: Kree Sentry (I), (II) ; expert: remove (I), add (III). Main scheme deck: Sentry Awakens, Self-Destruct Protocol.
Encounter deck: Kree Sentry, Imperial Guard, Standard. The Imperial Guard can be removed or added via customization rules ; if
added, follow the extra rules p.8.
- Sentry's Grasp (two copies, attachment): a character with a copy attached cannot scheme or thwart ; may only attack Kree Sentry
  or the Sentry's Grasp attached to it, as if it were a minion. Cards and abilities that target a minion but are not attacks cannot
  be resolved against the Sentry's Grasp. Attached to a minion, that minion cannot activate for a scheme or attack.
- Attacks against minions: effects can make Kree Sentry attack a minion ; the damage is placed on that minion and the attack is
  always undefended. "You" in boost abilities = the player who revealed the card that caused the attack. "Attacks you"
  abilities do not trigger. Players may defend as normal. Overkill that defeats the minion : excess goes to Kree Sentry.
- Campaign setup: each player chooses and records their first identity in the log.
- Victory: record Rick Jones in Recruited Allies and add the matching campaign-specific ally (card 224) to the campaign pool ; if
  Gladiator is in the victory display record him and add his campaign ally (card 225 ; le livret ne le numérote pas ici, voir
  INVENTAIRE) ; remove each non-treachery Imperial Guard card used from the campaign ; record the "Odd card" guess ; expert only:
  record each identity's remaining hit points.
- FAQ (p.22): if Intruder Elimination is revealed and the first player's identity is the target, Kree Sentry attacks Rick Jones
  (his Forced Interrupt changes the target).

## 8. Interlude I : Galactic Storm (p.11)

Story only. Kree Sentry destroyed; the Imperial Guard of the Shi'ar vanish through a stargate with the Universal Energy Core of
the Psyche-Magnitron. Rick Jones explains the Shi'ar have Nega-Bands from the tomb of Captain Marvel on Titan and can build the
Nega-Bomb to wipe out Hala. Captain America splits the heroes in three teams: Shi'ar space (the truth of the Nega-Bomb), Hala
(prevent Kree retaliation), and Earth (guard). "Operation Galactic Storm has begun."

## 9. Scénario 2 : Majestrix's Verdict (p.12 à 13)

Villain deck: Deathbird (I), (II) ; expert: remove (I), add (III). Main scheme deck: Earn the People's Favor, Majestrix's
Verdict. Encounter deck: Majestrix's Verdict, Imperial Guard, Standard.

### Chandilar Prison

Starjammers start the game in prison. The setup on main scheme 1A has the players put the Imprisoned on Chandilar side scheme into
play and tuck each STARJAMMER ally under it. When the last threat is removed from Imprisoned on Chandilar, players choose an ally
tucked under it and put it into play under any player's control ; after a STARJAMMER ally leaves play, it is tucked under
Imprisoned on Chandilar (rebels freed and recaptured when defeated). Whenever the main scheme is completed, players choose a
STARJAMMER ally tucked under Imprisoned on Chandilar (or in play if none tucked) and remove it from the game (execution of the
rebels). **If Lilandra is removed from the game, the players lose the game.**
FAQ: in expert mode, if the main scheme is completed and only one STARJAMMER ally is tucked under Imprisoned on Chandilar, the
"otherwise" effect is NOT resolved: it resolves only if the preceding effect cannot be at least partially resolved, i.e. only if no
STARJAMMER ally is tucked.

### Campaign instructions

Setup: each player chooses two additional identities and records them (three in all) ; for this scenario each chooses one of the
three. Deckbuilding: cannot include a unique card (+) that matches any identity recorded in the log. Place a game round dial next
to the villain's hit point dial. Expert only: a player using a previously used identity sets hit points to the remaining value
recorded ; each player may place one acceleration token on the main scheme to heal their identity to full.
Victory: each player records each unique card (+) included in their deck ; record each basic STARJAMMER ally in play in Recruited
Allies and add them to the campaign pool ; Gladiator in the victory display: record him and add the campaign ally ; remove each
non-treachery Imperial Guard card used ; record the Odd card guess ; record the value on the game round dial in Time Pressure ;
expert only: record remaining hit points.

## 10. Scénario 3 : Hala Ultimatum (p.14 à 15)

Villain deck: Kree Leader (I), (II) ; expert: remove (I), add (III). Main scheme deck: Hidden Might of Hala, Reckoning Begins.
Encounter deck: Hala Ultimatum, Accuser Corps, Standard. Accuser Corps can be removed/added via customization rules.

### Hidden villain

While the villain has the HIDDEN trait, players cannot affect the villain with player cards: no attacks by heroes or allies, no
damage through overkill when a minion is defeated with excess damage, no status card placed on the villain, no upgrades or other
player cards attached to it, no discarding of its tough status cards (piercing or any player card ability). If a card ability
has multiple targets and one is the villain, players may only play that card or initiate that ability if at least one other
valid target exists; if the villain is the only target, the card cannot be played / ability cannot be initiated. Conversely, the
villain cannot attack players while HIDDEN: whenever a player would be attacked by the villain, that player is dealt a facedown
encounter card. After the villain flips to its DISCOVERED side, all attachments, status cards, boost cards, damage and other
elements remain. After a villain stage is defeated, the next stage enters play on the same side as the just-defeated stage ("in
most situations ... DISCOVERED").

### Campaign instructions

Setup: each player chooses one of their three identities, different from the one used in Majestrix's Verdict. Deckbuilding: no
unique card (+) that matches any recorded in the log, identity included. Game round dial. Expert only: previously used identity
resumes at its recorded hit points ; may place one acceleration token on the main scheme to heal fully.
Victory: record unique cards (+) in the deck ; record Lauri-Ell in Recruited Allies and add the matching campaign-specific ally
to the campaign pool ; record the Odd card guess ; if the round dial is higher than the Time Pressure value recorded, replace it
with the dial value ; expert only: record remaining hit points. (Pas de retrait d'Imperial Guard ici : le scénario 3 ne l'emploie
pas.)

## 11. Scénario 4 : Earth Under Siege (p.16 à 17)

Villain deck: Annihilus (I), Attuma (I), Destroyer (I), Doctor Minerva (I), Mole Man (I), Veranke (I) ; expert: remove each (I),
add each (II). Main scheme deck: Earthfall. Encounter deck: Earth Under Siege, Annihilus, Attuma, Destroyer, Doctor Minerva, Mole
Man, Veranke, Imperial Guard, Standard.

### Multiple villains (text 1.2, identical on the insert)

During setup, set Annihilus, Attuma, Destroyer, Doctor Minerva, Mole Man and Veranke encounter sets aside. To create the villain
deck, shuffle a villain card of the same stage from each set-aside encounter set into the villain deck, facedown next to the
encounter deck. If a villain is defeated, remove it from the game ; unlike other scenarios, all tokens, status cards and
attachments on it are discarded instead of carrying over. Whenever a villain is revealed, shuffle the rest of its set-aside
encounter set into the encounter deck. If a villain is revealed while another is in play, place the newly revealed villain as the
rightmost villain, so the longest-present villain is always the leftmost. Encounter cards that refer to "the villain" refer only
to the leftmost villain. Player cards that refer to "the villain" refer only to the villain chosen by the player who controls that
card. If a minion takes any excess damage from an attack with overkill, the attacking player must choose which villain that excess
damage is dealt to. Cards attached to a villain that refer to "the villain" refer only to the attached villain.

### Villains activation (p.17)

During step two of the villain phase, with more than one villain, resolve each villain's activation against each player in player
order, villains from left to right. The leftmost villain activates against the first player, then the villain to its right against
the first player, and so on ; after all villains have activated against the first player, resolve the activations of the minions
engaged with that player ; then the second player in the same order. If the last villain is defeated during the villain phase while
activating, or immediately afterwards (retaliate, a "Hero Response" that triggers after the villain attacks), reveal the top card
of the villain deck ; the just-revealed villain activates against the same player. Exemple (Black Panther / T'Chala, Veranke and a
Moloid): Veranke is defeated by retaliate, Attuma is revealed, activates against Black Panther, then the Moloid activates.
FAQ: damage from Queen Veranke's attacks can be prevented by non-defense card effects (Maria Hill's Life Model Decoy) but not by
defense cards (Spider-Man's Backflip).

### Campaign instructions

Setup: each player chooses one of their three identities, different from those used in Majestrix's Verdict AND Hala Ultimatum.
No unique card (+) matching the log, identity included. Game round dial. Expert only: previously used identity resumes at recorded
hit points ; may place one acceleration token to heal fully.
Victory: Gladiator in the victory display: record him and add the campaign ally ; record the Odd card guess ; round dial higher
than the Time Pressure value: replace it ; expert only: record remaining hit points.

## 12. Interlude II : Nega-Bomb (p.18)

Story: peace obtained on Hala and Chandilar, yet the Nega-Bomb is launched. The Supreme Intelligence manipulated the Skrulls,
seeded infiltrators among the Kree, the Shi'ar and on Earth, guided the Imperial Guard to the Psyche-Magnitron and infiltrated
the launch. The Nega-Bomb is "a weapon of evolution", a culling to leave only the Kree capable of change and dominance.

## 13. Scénario 5 : Supreme Intelligence (p.19)

Villain deck: Supreme Intelligence (I), (II) ; expert: remove (I), add (III). Main scheme deck: Protectors of the Kree Empire, The
Endless Mind. Encounter deck: Supreme Intelligence, Starforce, Seeds of Corruption, Standard. Seeds of Corruption can be removed
or added elsewhere ; Starforce may be used in other scenarios but is REQUIRED when playing Supreme Intelligence.
Starforce modular set: minions mostly with victory and three boost icons ; when they enter the victory display they grant the
villain a bonus.

### Campaign instructions (1.2)

Setup: each player chooses one of their three identities. Put the Nega-Bomb side scheme into play with X threat (per player) in
place of its starting threat value, X = the value recorded in Time Pressure. Shuffle BOTH copies of Green Interference from the
Nega-Bomb set into the encounter deck. Compare the guessed Odd cards in the log to the correct solutions (81, 130, 139, 181/182).
For each correct guess, players as a group may choose one campaign identity-specific ally from the Galactic Storm set and add it to
the campaign pool. Each player may shuffle one ally from the campaign pool that does not "match" any unique card in their deck into
their deck. Each player may choose one identity-specific ally in their deck and replace it with a campaign identity-specific ally
from the Galactic Storm set that does not "match" any unique card in their deck. Expert only: each player sets their identity's hit
points to the remaining value in the log ; each may place one acceleration token on the main scheme to heal fully.
Victory: Supreme Intelligence is defeated, the players win the campaign. Epilogue (p.20): story only, moral question about heroes
deciding who lives and dies without trial.

## 14. Decks de départ (p.21)

- Binary / Aggression. Binary cards: Cosmic Influx (x2), Fuel the Flame [sic, voir transcription : « Fuel the Fire »] (x2), Pursued by
  the Flame (x2), Solar Flare (x2), Energy Torrent, Prophet-Singer, White Hole, Body in Flames, Energy Conversion (x2), Light,
  Radiation, Heat. Aggression: Into the Fray (x2), Moment of Triumph (x2), Spoiling for a Fight (x3 sur la page, à contrôler avec
  l'image), Keep Them Busy, Hall of Heroes, Aggressive Conditioning, Follow Through (x3), Marked (x2). Basic: Directed Force (x2),
  Face the Past, Hope Summers, Specialized Training, Energy, Genius, Strength, Avengers Mansion, Deft Focus, Soaring Acrobatics
  [et Nick Fury]. Nemesis: Rogue, Goin' Rogue, Touched, Energy Transfer (x2). Obligation: Forgotten Life.
- Quasar / Protection. Quasar cards: Quantum Bands, Epoch, Flight of Light (x2), No Holding Back (x2), Righteous Fury (x2),
  Unbreakable Guard (x2), Quantum Energy (x2), Quantum Absorption, Quantum Bubble, Quantum Jump, Quantum Weapon. Protection: Martyr,
  Starhawk, Desperate Defense (x3), Powerful Punch (x3), Change of Fortune, Defensive Conditioning, Electrostatic Armor, Unflappable.
  Basic: Cosmo, Drax, Gamora, Martinex, Multitalented (x3), Energy, Genius, Strength, Honorary Guardian, S.H.I.E.L.D. Deputy,
  Knowhere. Nemesis: Maelstrom, Entropy Ascendant, Avatar of Oblivion, Distant Manipulation (x2). Obligation: Protector of the
  Universe.
  (Les quantités et listes exactes seront contrôlées contre les fiches de transcription au lot GS-1 et GS-2.)
- Quasar: « Quantum Bands » donne une ressource supplémentaire par round ; les améliorations SUPERPOWER sont à maximiser.

## 15. FAQ du livret 1.2 (p.22 à 23)

Binary: Cosmic Influx after Energy Conversion and three non-energy resources drawn: no damage, because the cards are drawn first and
the non-energy resources are counted on them, but being treated as energy resources they cause none. Deckbuilding: identity-specific
cards with e, m and p resources are equal in number, so only aspect and basic cards need balancing. Campaign-specific cards are not
counted for resources and ignore deckbuilding restrictions.
Quasar: paying No Holding Back with two P resources, one generated by Quantum Bands, with Quantum Jump in play: no threat removed
(the unresolved part cannot be increased). With two M resources, one by Quantum Bands: remove 4 threat, Quantum Jump +2, total 6.
Campaign mode (1.2): a unique card in the deck for #3 or #4 recorded in another player's column: NOT allowed (each unique card
included may not match any recorded in any column). Honorary: the ally has the team trait of your identity while in play and in any
other game area (hand, deck, discard pile...). If you flip to alter-ego and your identity only has the team trait in hero form, the
ally loses it.
Scénarios 3 et 5 : « Q. to be added... » (FAQ à venir dans le livret).

## 16. ÉCARTS entre le livret 1.1 et le livret 1.2

Méthode : rendu des 24 pages, comparaison pixel à pixel (pages 1, 2, 4, 5, 7, 8, 10, 11, 13, 15, 17, 18, 20, 21, 24 identiques),
puis lecture des 9 pages qui diffèrent (3, 6, 9, 12, 14, 16, 19, 22, 23).

| Page | 1.1 | 1.2 | Effet en jeu |
|---|---|---|---|
| 3, Honorary | « team trait of your hero (see page 9 for the list) » | « team trait(s) of your identity (see page 9 ...) ; an ally with honorary retains these traits in every game area » | le trait d'équipe suit l'IDENTITÉ (alter-ego compris), et reste dans toutes les zones : voir FAQ p.23 |
| 3, mise en page | Requirement, Setup, Steady, Teamwork très légèrement décalés | texte inchangé | aucun |
| 6, Odd cards | texte différent, avec l'exemple d'une carte de Ronan l'Accusateur « The card number of this card is 214 » (icônes de boost en pied de carte) | texte réécrit (mystère facultatif, « Odd card » sans carte d'exemple), le chiffre 214 disparaît | aucun sur les règles ; la numérotation (214 = Ronan) sert d'indice : voir questions |
| 9, 12, 14, 16, 19 | « Villain deck(s) » au pluriel | « Villain Deck » au singulier | aucun (typographie) |
| 16, Multiple villains | « If a minion takes any amount of excess damage from an attack with overkill, deal that excess damage to the leftmost villain. Whenever a player plays a card or triggers an ability that refers to "the villain", they must choose which villain it refers to. » | « Player cards that refer to "the villain" only refer to the villain chosen by the player who controls that player card. If a minion takes any excess damage from an attack with overkill, the attacking player must choose which villain that excess damage is dealt to. » | l'excès de dégâts va au méchant CHOISI par l'attaquant (1.1 : le plus à gauche) ; un effet joueur désigne un méchant choisi par son contrôleur ; l'insert d'Earth Under Siege suit la version 1.2 |
| 19, Scénario 5 setup | (a) choisir une identité ; (b) chaque joueur peut remplacer un allié propre à l'identité par un allié de campagne ; (c) chaque joueur peut mélanger UN allié de campagne de la réserve dans son deck ; (d) Nega-Bomb : X menace, X = valeur de Time Pressure ; (e) pour chaque Odd card correcte : retirer 1 menace de la Nega-Bomb ; (f) mélanger les DEUX Green Interference, UNE seule si au moins deux Odd cards correctes | (a) choisir une identité ; (b) Nega-Bomb : X menace par joueur, X = Time Pressure ; (c) mélanger les DEUX Green Interference, toujours ; (d) comparer les Odd cards ; (e) pour chaque bonne réponse, le groupe choisit un allié d'identité Galactic Storm qui rejoint la réserve ; (f) chaque joueur peut mélanger un allié de la réserve (qui ne « correspond » à aucune carte unique de son deck) ; (g) remplacement d'un allié d'identité | la récompense des Odd cards change de nature : 1.1 = moins de menace sur la Nega-Bomb et une seule Green Interference ; 1.2 = alliés supplémentaires, deux Green Interference toujours |
| 22, FAQ | scénarios 4 et 5 : « Q. to be added... » | scénario 4 : question sur les dégâts des attaques de Veranke (Life Model Decoy ou non) ; scénario 5 : « Q. to be added... » ; scénario 3 inchangé | précision de règle |
| 23, FAQ campagne | honorary : trait du « hero » « as long as you are in hero form » ; flip en alter-ego : « Yes. It keeps it only as long as you are in hero form. » | trait de l'« identity » dans toute zone ; flip : perte seulement si l'identité n'a le trait qu'en forme héros | cohérent avec p.3 |
| 23, crédits | Expansion Graphic Design : Kajislav, Man-3, Merlin, FuManchuToo, CommCody103 et Supertnt73 ; playtesters finissent à Insanohops | Supertnt73 retiré des graphistes (il reste playtester), « and » remplacé par une virgule ; playtester ajouté : Matchet | crédits seulement |

Les inserts de scénario (Kree Sentry, Majestrix, Hala, Earth Under Siege p.1-2, Supreme Intelligence) sont alignés sur le texte 1.2
(« Villain Deck », surcharge d'overkill 1.2). L'insert d'Earth Under Siege dit « Black Panther / T'Chala » et « Hero Response » comme
le livret 1.2.

Le zip 4 contient en plus une version non compressée du livret 1.2 (336 Mo, 24 pages, même mise en page) : voir INVENTAIRE.md.
