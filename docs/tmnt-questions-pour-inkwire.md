# TMNT content for Marvel Champions: questions and suspected typos, for Inkwire

Hello Inkwire,

Thank you for creating all of the Teenage Mutant Ninja Turtles content for Marvel Champions: the eight hero packs (Leonardo, Michelangelo, Raphael, Donatello, Casey Jones, Jennika, Alopex, Venus), the scenarios (Shredder, Bebop & Rocksteady, Baxter Stockman), the TMNT Standard / Expert status-card sets and the six aspect packs (Aggression, Basic, Justice, Leadership, Protection, Dual-Aspect). We are a small, non-commercial fan project that runs a digital, scripted implementation of Marvel Champions (an open-source engine derived from `irefrixs/marvel-lcg`). Every one of your cards is implemented there as faithfully as we can manage, scan by scan, and we want to get each one exactly as you intended.

While implementing the cards we found (a) a number of printed details that look like typos, and (b) a number of places where the rules text can be read in more than one way. We did not want to guess silently, so this document lists all of them. You do not need to know anything about our engine; each entry quotes what is printed, says what we expected, and says what we currently do.

**What we are asking.** For each entry, a one-line answer is plenty:

- Part A (suspected typos): reply **"typo? yes - it should say: ..."** or **"typo? no - intended"** (with a note if you like).
- Part B (rules questions): reply **"intended: 1"** (or 2, 3...) when one of our readings is right, or **"intended: X"** with your own wording.
- Part C (name conflicts) and Part D (our other assumptions): reply **"OK"** or tell us what to change.

Where we write **[decided by us, please confirm]**, our maintainer already picked a reading (sometimes after hearing your community's FAQ or an insert), but you are the authority, so please correct us if it is not what you meant. **[our provisional reading, not yet decided]** means we implemented the most literal reading in the meantime and it may well change. Our internal card ids (for example `tl006`) are given in parentheses only so we can find the card again; the card name is what matters.

Contents: Part A suspected typos - Part B rules questions (grouped by pack) - Part C cross-card name conflicts - Part D our other assumptions - To verify before sending.

---

# Part A: Suspected typos

Each table row is one suspected typo. Last column: **Typo? (yes / no, and the intended text)**. "Official" means the official Marvel Champions card or wording we compared with.

## A1. Hero packs and scenarios

| # | Card (our id) | Where on the card | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A1.1 | Manipulated, Alopex obligation (`ta012`) | rules text | "charcter" (in "... each charcter you control ...") | "character" | Displayed as "character" (we corrected it silently) | |
| A1.2 | Prey, Alopex upgrade (`ta011`) | rules text, both lines | "Alopex' attacks deal 1 additional damage..." and "Alopex' thwarts remove 1 additional threat..." | "Alopex's" (or an intended possessive without s) | Kept exactly as printed | |
| A1.3 | Welcome to the Jungle, Bebop & Rocksteady side scheme (`tk101`) | italic quote | "...It's time to take this fight to the them." | "to them" (or another word instead of "the them") | English text keeps "to the them" as printed (our French translation is corrected) | |
| A1.4 | Mutagen Bomb, Raphael side scheme (`tr014`) | italic flavour text | "Old Hobb has weaponized mutagen into bombs." | The nemesis card in the same pack is printed "Old Hob" | Kept as printed | |
| A1.5 | Bō Tobu, Donatello event (`td003`) | card title, two copies of the same card | Copy 2/15: "Bō Tobu" (macron). Copy 3/15: "Bo Tobu" (no macron). Same text, cost and icons | One title (we assume "Bō Tobu", like "Chūdan-Ura-Uke" and "Donatello's Bō") | One card named "Bō Tobu" (the 2/15 image) [decided by us, please confirm] | |
| A1.6 | Extermination!, Donatello side scheme (`td014`) | When Defeated line | Per our transcription: "Search the encounter deck and discard pile for a MOUSER or FLYBORG minion" (singular), whereas the minions' trait lines and Baxter Stockman (`td015`) say "MOUSERS" / "FLYBORGS" (plural) | One spelling used everywhere | We treat MOUSER(S) and FLYBORG(S) as the same trait for all searches [decided by us, please confirm] | |
| A1.7 | Flight of Flyborgs, Baxter Stockman minion (`tx012`, `tx013` Superfly) vs Donatello's Flight of Flyborgs (`td017`) | trait line | Baxter's cards: "AERIAL. FLYBORG. SWARM." Donatello's card: "AERIAL. FLYBORGS. SWARM." | Same trait spelling on both | Same trait for searches (see A1.6) [decided by us, please confirm] | |
| A1.8 | Baxter's Laboratory, main scheme 1A (`tx004a`) | Content line | "(Baxter Stockman (II) and Baxter (III) for expert mode.)" | "Baxter Stockman (III)" (the stage III card is named "Baxter Stockman") | We use stages II and III in expert mode; only the wording is odd | |
| A1.9 | Arc Nova, Venus event (`tv003`) | collection number at the foot | "VENUS (2/16)" | Our 15 Venus player-deck scans are numbered 1 to 15 | Ignored (the number has no game effect) | |
| A1.10 | Wyrm, Michelangelo nemesis minion (`tm015`) | trait line | "WORMS!" (with an exclamation mark) | "WORMS" | Stored as the trait WORMS | |
| A1.11 | I'm Here to Help, Michelangelo player side scheme (`tm009`) | cost box, top right | A cost cartouche with no readable digit | Cost 0 (as for official player side schemes)? | Cost 0 | |


## A2. Aggression aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A2.1 | Firepower (`ua018`) | Hero Action | "...for each upgrade exhausted this way, choose an enemy and deal 3 damage to it." | Official Firepower (54014): "for each weapon upgrade exhausted this way" | Treated as identical to the official card (only WEAPON upgrades can be exhausted by the cost anyway) | |
| A2.2 | Chain Reaction (`ua008`) | whole card | Credited "Reskins" on the scan (as we understand it); text: "Deal 2 damage to an enemy. If that enemy is defeated, deal 2 damage to a second enemy. If that enemy is defeated, deal 3 damage to a third enemy." | We could not find an official card with this text | Implemented as a new TMNT-exclusive card. Which official card is it a reskin of? | |
| A2.3 | Combo Move (`ua011`) | whole card | Credited "Reskins" on the scan (as we understand it); text: "Deal 2 damage among enemies in play (3 damage instead if your identity has the MARTIAL ARTIST trait)." | We could not find an official card with this text | Implemented as a new TMNT-exclusive card. Which official card is it a reskin of? | |

## A3. Basic aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A3.1 | Assess the Situation (`ub002`) | trait line | No trait printed | Official Assess the Situation (12033): "TACTIC." (text otherwise identical) | Decided: oversight, TACTIC added (implemented) [decided by us, please confirm] | |
| A3.2 | Sky Wagon (`ub047`, banner "Helicarrier") | trait line | "NYC. VEHICLE." | Official Helicarrier (01092): "LOCATION. S.H.I.E.L.D."; text identical | Decided: we follow the scan exactly (NYC, VEHICLE; not a LOCATION, a flying van is not a place). Implemented as printed [decided by us, please confirm] | |
| A3.3 | Atilla (`ub003`) | ability type | "Forced Response: After you play Atilla from your hand, choose THW or ATK. Atilla gets +2 to the chosen power until the end of the phase." | The text is word for word that of official Spider-Man, Miles Morales (13019), which is a "Response" | Implemented as a Forced Response, as printed [our provisional reading, not yet decided] | |
| A3.4 | Gofu Talisman (`ub017`, reskin of Bloodgem) | first line | "Play only if you have the MYSTIC trait." | Official Bloodgem (45050): "Play only if your identity has the MYSTIC trait." | Same meaning ("you" = your identity), identical to Bloodgem [our provisional reading, not yet decided] | |
| A3.5 | Honorable Blades (`ub019`) | text | "Team-Up (Leonardo and Usagi Yōjimbō). Max 1 per deck. Hero Action: Ready Leonardo and Usagi Yōjimbō. Cloak Leonardo. Place a tough status card on Usagi Yōjimō." | The last line spells the name "Yōjimō" (missing b) | Integrated and playable: Usagi Yōjimbō is your Protection ally (`up041`), and the Team-Up needs Leonardo and that ally in play. The name is spelled "Yōjimbō" on our display [decided by us, please confirm]. Is "Yōjimō" a typo, and is the Team-Up meant to be with that ally? | |
| A3.6 | Team-Building Exercise (`ub055`, reskin of 12024) | Hero Action | "...reducing it's resource cost by 1." | "its" | Printed apostrophe kept | |

## A4. Justice aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A4.1 | Chance Encounter (`uj002`) | first line | "Attach to a scheme. Max 1 per scheme." (the Interrupt below still says "When attached side scheme is defeated") | Official (26034 / 60025): "Attach to a side scheme. Max 1 per scheme." | Decided: typo, side scheme only, exactly like the official card (implemented, text shows "side scheme") [decided by us, please confirm] | |
| A4.2 | Venus, Bonnie (`uj036`, banner "Manifold") | Response | "...That player searches their deck and a discard pile for a player side scheme and adds it to their hand." | Official Manifold (51014): "searches their deck and discard pile" | Decided: typo, the chosen player searches their OWN discard pile, exactly like Manifold [decided by us, please confirm] | |
| A4.3 | Zone of Silence (`uj040`) | Hero Action | "...discard up to 4 card cards from the top of your deck..." | Official (21050): "4 cards" | Displayed as "4 cards" (cosmetic, chosen without asking) [decided by us, please confirm] | |

## A5. Leadership aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A5.1 | Old Hob (`ul019`, banner "White Wolf") | trait line | "CAT. MUTANIMALS." (plural) | Every other card prints "MUTANIMAL"; Splinter Dojo Training says "Attach to a NINJA or MUTANIMAL ally" | Decided: typo, trait MUTANIMAL, so Splinter Dojo Training and Attack Training can attach to Old Hob (implemented) [decided by us, please confirm] | |
| A5.2 | Take a Stand (`ul033`) | trait line | No trait printed | Official Take a Stand (62015): "TACTIC." | Decided: oversight, TACTIC added (implemented) [decided by us, please confirm] | |
| A5.3 | Suit Up (`ul031`) | Alter-Ego Action | "Search your deck and discard pile for an ally and an upgrade that can be attached to AN ally." | Official Suit Up (45017): "...that can be attached to THAT ally" | Decided: literal reading, any upgrade that can attach to some ally, not necessarily the ally found (implemented, against the official wording) [decided by us, please confirm] | |
| A5.4 | Suit Up (`ul031`) | italic quote | "TIme to get back at it." | "Time" | Kept as printed | |
| A5.5 | Unified Stike (`ul038`) | title | "Unified Stike" | "Unified Strike" (official `58020`) | Decided: title corrected to "Unified Strike" (implemented) [decided by us, please confirm] | |
| A5.6 | Unified Stike (`ul038`) | ability type | "Hero Response: When an ally uses a basic power, exhaust your hero -> add your hero's matching power to that ally's power for this use. That ally does not take consequential damage for this use." | Official Unified Strike (58020): "Hero Interrupt: When an ally uses a basic power..." (a Response happens after the use, where "for this use" no longer makes sense) | Decided: Hero Interrupt [decided by us, please confirm] | |
| A5.7 | Shōgun (`ul025`) | Response | "After Shugun enters play, discard an ally from your hand -> give an ally a tough status card." | "Shōgun" (the title is "Shōgun") | Displayed as printed ("Shugun"); the engine targets the card itself | |
| A5.8 | Mushroom (`ul041`) | rules text | "Musroom does not count against your ally limit." | "Mushroom" | Displayed as printed ("Musroom") | |
| A5.9 | "You Got This!" (`ul044`) | resource icon (top corner) | A red fist ([physical]) | Official "You Got This!" (49019) has an [energy] resource; the text is otherwise identical | Follows the scan: [physical] [decided by us, please confirm]. Is the physical icon intended? | |

## A6. Protection aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A6.1 | Redirection Mastery (`up030`) | Hero Response | "After you exactly defend an attack, deal damage to the attacker equal to your DEF for that attack." | "exactly defend" appears on no official card or in the Rules Reference. Possible intended text: "After you defend an attack ..." or "After you defend an attack without taking damage ..." | Decided: "exactly defend" = the attack's value (boosts included) equals your DEF exactly; the script is implemented [decided by us, please confirm] | |
| A6.2 | "I Can Do This All Day" (`up018`) | ability type | "Hero Action (defense): When an enemy attacks, declare your hero as the defender without exhausting them." | Official (56047): "Hero Interrupt (defense): When an enemy attacks..." (an Action cannot have a "When" trigger) | Decided: Hero Interrupt; displayed text corrected [decided by us, please confirm] | |
| A6.3 | Ready for a Fight (`up029`) | ability type | "Intterupt: When an enemy would scheme, discard Ready for a Fight -> change to hero form. That enemy attacks you instead." | "Interrupt" | Treated as an Interrupt (identical to official 52019) | |
| A6.4 | Seymour Gutz (`up034`, banner "Rogue") | Action | "...until the end of the round, Seymor Gutz gains each of that character's Traits..." | "Seymour" | Text shows the typo; no game effect | |
| A6.5 | Jōtarō (`up021`) | cost, resource, wording | Cost 3. "Toughness. Interrupt: When an enemy would deal any amount of damage, spend a [physical] resource -> reduce that amount of damage by 1. (Limit once per round.)" | Closest official card, Protector (26014), costs 4 and says "When Protector would take any amount of damage, spend a [mental] resource -> reduce that amount by 1." Our own working table said Jōtarō costs 2 | We implemented cost 3 and a [physical] resource as printed. Are the cost 3 and the [physical] resource intended? | |
| A6.6 | Nobody (`up024`) | subtitle | Subtitle "Angel Bridge" | Alopex's ally Nobody (`ta002`) has the subtitle "Angel Bridges" (with s) | Both kept as printed. Same person, one spelling? (see also Part C) | |

## A7. Dual-Aspect

| # | Card (our id) | Where | Printed | Expected / official | What we currently do | Typo? |
|---|---|---|---|---|---|---|
| A7.1 | Stealth Fighter (`ud004`) | second ability | "Interrupt: After Stealth Fighter is defeated by consequential damage, cloak a friendly character." | An Interrupt is a "When ..." trigger; an "After ..." trigger is a Response. The same pack's Rōnin, Doomsayer and Sōhei say "Interrupt: When ... is defeated by consequential damage" | Decided: implemented as "Interrupt: When ... is defeated", like the other cards of the pack [decided by us, please confirm] | |

---

# Part B: Rules questions

For each entry: the card, the exact text, what is ambiguous, **our current reading**, and the question. Status tags: **[decided by us, please confirm]** or **[our provisional reading, not yet decided]**. Answer with "intended: 1 / 2 / 3" or your own wording.

## B-L. Leonardo (Leonardo v3)

**B-L1. Karai, Foot Soldiers: "Cloak" (`tl015`, `tl016`)** [decided by us, please confirm]
- Text: Karai "When Revealed: Cloak Karai. When Defeated: Cloak the villain." Foot Soldiers "When Revealed: Cloak Foot Soldiers."
- Ambiguity: "Cloak" is not defined on the cards themselves.
- Our current reading: "Cloak X" means "place a Cloaked status card on X" (using the Cloaked status card from your Shredder scenario). Question: is that what you meant? (The reading of the status card itself is in Part B, section B-G.)

**B-L2. Leonardo's Katana: "gains" (`tl011`; also `tl012`)** [decided by us, please confirm]
- Text: "Each KATANA upgrade you control gains: 'Hero Resource: Exhaust this card -> generate a [wild] resource for an identity-specific card.'"
- Ambiguity: a real "gains" (every KATANA you control, including Other Katana, gets the ability while Leonardo's Katana is in play) or each Katana carrying its own ability.
- Our current reading: a real grant. While Leonardo's Katana is in play, every Katana you control (both of them) can produce the resource; if Leonardo's Katana leaves play the grant disappears. Question: correct?

**B-L3. Yo Ko Giri (`tl006`)** [decided by us, please confirm]
- Text: "Hero Action (attack): Deal 5 damage to an enemy. This attack gains piercing. If you paid for this card with [energy][mental][physical] resources, you may return this card to your hand."
- Ambiguity: does it need at least one resource of each of the three colours, exactly those three, or any of them? (The card costs 3.)
- Our current reading: at least one resource of EACH colour (energy, mental, physical); a [wild] resource counts for one colour at the player's choice. Question: correct?

**B-L4. Iaijutsu (`tl008`)** [decided by us, please confirm]
- Text: "Hero Interrupt: When an enemy initiates an attack, exhaust a KATANA upgrade you control -> you may play an ATTACK event with a 'Hero Action' ability from your hand (paying its cost). If this attack defeats an enemy, draw 1 card."
- Ambiguity: "this attack" is the played event's attack (not the enemy's attack).
- Our current reading: the draw happens only if the attack of the event we played defeats an enemy (minion or villain). Question: correct?

**B-L5. Brainwashed Betrayal, obligation (`tl013`)** [decided by us, please confirm]
- Text: "Give to the Leo player. Flip to hero form and discard an ally you control. You cannot attack the villain. Forced Response: After your turn begins, deal 3 damage to an ally. Alter-Ego Action: Exhaust Leo and take 2 damage -> remove Brainwashed Betrayal from the game."
- Ambiguities: (i) is the flip to hero form mandatory? (ii) which ally is damaged by the Forced Response? (iii) how long does "cannot attack the villain" last?
- Our current reading (literal): the flip is mandatory and one of your allies is discarded (your choice); you cannot attack the villain as long as the obligation is in play (minions can still be attacked); the 3 damage go to ANY ally in play (chosen by the player, including other players' allies). Question: correct? In particular, should the 3 damage be restricted to the Leo player's own allies?

**B-L6. Foot Patrol (`tl014`)** [decided by us, please confirm]
- Text: "When Defeated: Search the encounter deck and discard pile for a FOOT CLAN minion and put it into play engaged with the first player."
- Ambiguity: what if no FOOT CLAN minion is found?
- Our current reading: nothing happens. Question: correct?

**B-L7. "Katana Weapon Rules" insert** [decided by us, please confirm]
- Our current reading: the insert is a rules sheet, not a card; we encoded its bullets in the scripts of the cards concerned (Leo, both Katanas, Iaijutsu) and created no separate card. Question: OK?

**B-L8. Leonardo's Other Katana: "+1 to each of their basic powers" (`tl012`)** [decided by us, please confirm]
- Text: "Hero Action: Choose a friendly character and exhaust 2 KATANA upgrades you control -> that character gets +1 to each of their basic powers until the end of the round." (also gains a [wild] resource when Leonardo's Katana is in play)
- Ambiguity: does "each of their basic powers" include REC (recover)?
- Our current reading: yes, the bonus includes +1 REC (visible on the alter-ego side in the same round). Question: correct?

## B-M. Michelangelo (Michelangelo v3)

**B-M1. Mikey / I'm Here to Help: where the player side scheme comes from at Setup (`tm001b`, `tm009`)** [decided by us, please confirm]
- Text: Mikey "Setup: Put the I'm Here to Help player side scheme into play." The side scheme is printed "MICHELANGELO (12/15)", one of the 15 deck cards.
- Our current reading: at Setup we search the deck for it and put it into play; it stays one of the 15 deck cards (so the starting hand draws 14 others). Question: correct, or should it start set aside?

**B-M2. Majime (`tm006`)** [decided by us, please confirm]
- Text: "Hero Action (attack/thwart): Take X damage (to a maximum of 3) -> remove X threat from a scheme and deal X damage to an enemy."
- Ambiguity: is X the damage you announce, or the damage actually taken (if Toughness or a prevention effect reduces it)?
- Our current reading: X = damage actually taken. Question: correct?

**B-M3. Booyakasha (`tm001a`)** [decided by us, please confirm]
- Text: "Response: After you use a basic power (THW, ATK, or DEF), move up to 3 threat from one scheme to another scheme. You cannot move threat onto a side scheme with 5[per hero] or more threat on it."
- Ambiguity: (i) a side scheme emptied by the move: is it defeated? (ii) does Crisis on a side scheme stop moving threat OFF the main scheme?
- Our current reading: (i) yes, it is defeated; (ii) yes, Crisis prevents moving threat from the main scheme. Question: correct?

**B-M4. Impulsive (`tm004`)** [decided by us, please confirm]
- Text: "Hero Action: Place 2 threat on the main scheme -> ready Michelangelo and a WEAPON you control. Draw 1 card."
- Ambiguity: can the card be played with no WEAPON in play?
- Our current reading: yes (only the cost, 2 threat, must be payable). Question: correct?

**B-M5. I'm Here to Help: the draw (`tm009`)** [decided by us, please confirm]
- Text: "Hero Interrupt: When this scheme is defeated, draw 3 cards (only the Michelangelo player can trigger this ability)." The insert adds "you must be in hero form to draw the 3 cards".
- Our current reading: Michelangelo must be in hero form and must be the OWNER of the card; if another player defeats the scheme, or Michelangelo is in alter-ego form, nobody draws. Question: correct?

**B-M6. Michelangelo's Nunchuck / Other Nunchuck (`tm011`, `tm012`)** [decided by us, please confirm]
- Text: "Each NUNCHUCK upgrade you control gains: ..." (Response: +1 to a basic power / Interrupt: reduce attack damage by 1 and deal 1 damage to the attacker).
- Our current reading (following your insert "either NUNCHUCK (or both)"): each of the two cards gives its ability to every NUNCHUCK you control, itself included, so with both in play each Nunchuck carries both abilities. Question: correct?

**B-M7. Sewer Problems: central icon (`tm014`)** [decided by us, please confirm]
- Text: no keyword in the text box; the central icon matches the Crisis icon of official Crowd Control (01108).
- Our current reading: Crisis 1 (4 threat per hero, 3 boost icons). Question: correct, or is the icon decoration?

**B-M8. "Hero Spin"** [decided by us, please confirm]
- The folder contained a single hero face named "0 Michelangelo Hero Spin" (THW 1 / ATK 1 / DEF 2). Our current reading: it is simply Michelangelo's one hero face; no variant. Question: is there another hero face we should have?

## B-R. Raphael (Raphael v3)

**B-R1. Rage counter cap (`tr001a`, `tr007`, `tr002`, `tr010`, Sai)** [decided by us, please confirm]
- Text: "(to a maximum of 3)" is printed on Yaban Hito (`tr001a`) and Seething Rage (`tr007`) and in the Sai insert; it is NOT printed on Casey Jones ("Place 1 rage counter on Raphael") or Gekido ("Place 1 rage counter on Raphael").
- Our current reading: Raphael never has more than 3 rage counters, whatever the source. Question: correct, or can Casey Jones and Gekido go beyond 3?

**B-R2. "Raphael" when the player is in alter-ego form (`tr002`, `tr007`, heal of `tr010`)** [decided by us, please confirm]
- Text: Casey Jones "deal 1 damage to Raphael and each minion engaged with you. Place 1 rage counter on Raphael."; Seething Rage "heal 2 damage from Raphael and place 1 rage counter on him". These can be played in alter-ego form, where the identity is called "Raph".
- Our current reading: "Raphael" means the player's identity in either form (damage, healing and rage apply to the identity card even when it shows Raph). Question: correct?

**B-R3. Sai insert (`tr011`, `tr012`)** [decided by us, please confirm]
- Text: card: "Hero Action (attack): Exhaust this card and take 1 damage -> deal 1 damage to an enemy." Insert: "Each time you use the Sai to deal 1 damage to yourself and 1 damage to an enemy, it is an attack action. Make sure to place 1 rage counter on Raphael when you use this ability (to a maximum of 3)."
- Our current reading: the insert prevails: each use is an attack and places 1 rage counter. Question: correct?

**B-R4. Out of Control (`tr013`)** [decided by us, please confirm]
- Text: "Give to the Raph player. Flip to hero form and exhaust your identity. You cannot change forms, thwart, or defend. Hero Action: Remove 2 rage counters from Raphael -> flip to alter-ego form and discard Out of Control."
- Our current reading: "you" = the identity only (allies may still thwart and defend). The Hero Action may flip to alter-ego despite "cannot change forms". Question: correct?

**B-R5. Mutagen Bomb: icon under the text (`tr014`)** [decided by us, please confirm]
- Text: "Forced Response: After resolving step one of the villain phase, place 1 timer counter here. Then, if there are 2 or more timer counters here, discard this card and deal each player 1 facedown encounter card." Under the text there is an icon (a cross and an aircraft-like shape).
- Our current reading: Amplify 1 (the same glyph as official Vendetta, 16054, checked by overlaying the silhouettes). Question: correct? (Alternatives we considered: Hazard, Acceleration, decoration.)

**B-R6. Disarm (`tr003`)** [decided by us, please confirm]
- Text: "Remove 4 threat from a scheme. You may discard a SAI upgrade you control to discard an attachment with the text 'Hero Action' or 'Hero Response' from an enemy."
- Our current reading: "attachment" = encounter Attachment cards attached to an enemy only (not player upgrades attached to an enemy). Question: correct?

## B-D. Donatello (Donatello v3)

**B-D1. Improvised Tactics: "Cloak two friendly characters" (`td005`)** [decided by us, please confirm]
- Text: "Hero Action: Exhaust a TECH upgrade you control -> choose two (you cannot choose the same option twice): Cloak two friendly characters. / Stun or confuse an enemy. / Draw 2 cards."
- Our current reading: place a Cloaked status card on two friendly characters (identities and allies of all players). Question: correct?

**B-D2. Donatello's Shell (`td012`)** [decided by us, please confirm]
- Text: "You may play, spend, or discard cards tucked here as if they were in your hand. (Max 1 tucked card.)"
- Our current reading: a tucked card can be played, spent for its resource, and discarded to pay "discard a card from your hand" costs as if it were in hand (we extended our engine so the full text works). Question: correct?

**B-D3. Swarm minions' hit points (`td016`, `td017`, also `tx007`, `tx012`, `tx013`)** [decided by us, please confirm]
- Text: "This minion's SCH, ATK, and hit points are equal to the number of swarm counters here." (printed with a star)
- Our current reading: hit points track the number of swarm counters dynamically; damage removes counters instead ("When this minion takes any amount of damage, remove that many swarm counters from here instead"). Question: correct?

**B-D4. Metalhead (`td002`)**
- Text: "Interrupt: When Donatello defends against an attack, spend a [mental] resource -> play Metalhead from your hand or Donatello's Shell without paying his resource cost."
- Our reading: playable from hand or from the Shell, you pay only the [mental] resource. No doubt about the text; listed for completeness. Question: OK?

## B-C. Casey Jones (Casey Jones v3)

**B-C1. "Casey Jones WEAPON upgrade" (`tc002` Clap Back, `tc006` Anything Goes)** [decided by us, please confirm]
- Text: Clap Back "If a Casey Jones WEAPON upgrade was discarded to pay for this card, confuse an enemy." Anything Goes "Exhaust Anything Goes -> swap a Casey Jones WEAPON upgrade you control with a Casey Jones WEAPON upgrade tucked under Casey's Bag."
- Our current reading: "Casey Jones WEAPON upgrade" = a WEAPON upgrade of the Casey Jones set (his five WEAPON upgrades), not any WEAPON (so Raphael's Sai discarded for Clap Back does not confuse). Question: correct?

**B-C2. Casey's Bag at Setup when it is in the starting hand (`tc001b`, `tc013`)** [decided by us, please confirm]
- Text: "Setup: Search your deck and discard pile for the Casey's Bag upgrade and put it into play. (Shuffle.)" Casey's Bag prints no cost (a dash) and "Permanent".
- Ambiguity: the starting hand is drawn before this Setup, so the Bag is already in the hand roughly 37% of the time.
- Our current reading: we search the deck, the discard pile AND the hand, so the Bag always enters play. Question: correct? (Also: the Bag has no cost, so we treat it as unplayable from hand and usable only as a [mental] resource; confirm?)

**B-C3. Cricket Willow (`tc009`)** [decided by us, please confirm]
- Text: "Hero Response: After you attack an enemy, discard Cricket Willow -> stun that enemy."
- Our current reading: the Response is NOT offered if the attacked enemy was defeated (nothing to stun, so you would not pay the discard). Question: correct?

**B-C4. Anything Goes: the swap (`tc006`)** [decided by us, please confirm]
- Our current reading: the Casey WEAPON in play goes tucked under the Bag, and the tucked one enters play READY (not exhausted), attached to Casey. Question: correct, or should it enter exhausted?

## B-J. Jennika (Jennika v3)

**B-J1. Ninja Senpai: "Limit once per round for each Shinobi" (`tj001a`)** [decided by us, please confirm]
- Text: "Interrupt: When you play a Shinobi card, Jennika gets +1 THW, +1 ATK, and +1 DEF until the end of the round. (Limit once per round for each Shinobi.)"
- Our current reading: once per round for each of the four classes (Bushido, Ninjutsu, Kuji-Kiri, Taijutsu); a dual-class card triggers both. Question: correct?

**B-J2. Which cards are "Shinobi" cards?** [decided by us, please confirm]
- Text: Decisive Strike / Apparition / Moonlighting / Fearless Resolve print "This card is both a Jennika card and a Taijutsu / Kuji-Kiri / Ninjutsu / Bushido card". Composure, Jenny's Crib, Jennika's Bow and the two Tekko-Kagi print no class. The Path card back says "You may add any combination of Shinobi cards (Bushido, Ninjutsu, Kuji-Kiri, or Taijutsu) to your deck."
- Our current reading: only cards that print one of the four classes are Shinobi; the five classless cards are not. Question: correct?

**B-J3. Sōsaiken: card type "PATH" (`tj011`)** [decided by us, please confirm]
- Text: "Permanent. Response: After you play a Shinobi card, exhaust this card -> draw 1 card." Printed type PATH, trait SENPAI. Jenny: "Setup: Put the Sōsaiken Path into play under your control."
- Our current reading: we created a real card type "Path" in our engine; it sits in the support area, but effects that mention "support" do not affect it. Question: correct, or should it behave like a Support?

**B-J4. Sōsaiken: set aside or in the deck? (`tj011`)** [decided by us, please confirm]
- Our current reading: the Path starts set aside (outside the 15-card deck), and Jenny's Setup puts it into play. Question: correct, or is it one of the deck's cards (16 in all) that Setup searches for?

**B-J5. Apparition (`tj003`)** [decided by us, please confirm]
- Text: "Action (thwart): Remove 2 threat from a scheme and confuse an enemy."
- Our current reading: the two halves are independent (if there is no scheme to thwart, the enemy is still confused, and vice versa). Question: correct, or are both targets required?

Smaller readings we settled without asking (please tell us if any is wrong): Phantasm (`tj014`) "Cloak each PHANTOMS minion in play" includes itself; Jennika's Bow (`tj008`) "deal 1 damage to an enemy or remove 1 threat" is one or the other; Personality Adjustment (`tj012`) the flip is optional, then the choice is mandatory, and "Exhaust Jenny" exists only in alter-ego form with Jenny ready.

## B-A. Alopex (Alopex v3)

**B-A1. Matagi: "find Prey" when Prey is already in play (`ta001a`)** [decided by us, please confirm]
- Text: "Matagi - Forced Response: After you attack an enemy or thwart a scheme, find Prey and attach it to that enemy or scheme."
- Our current reading (following the official rule for "find"): if Prey is already in play on another target it is found and MOVED to the new target. Question: correct, or does Prey stay where it is?

**B-A2. Nobody and the last threat (`ta002`)** [decided by us, please confirm]
- Text: "Response: After Nobody attacks an enemy with Prey attached, daze that enemy. Response: After Nobody thwarts a scheme with Prey attached, cloak her."
- Ambiguity: if the thwart empties the scheme, the scheme is defeated and Prey leaves play before the Response window.
- Our current reading: "with Prey attached" is read at the moment of the thwart, so Nobody is still cloaked. Question: correct?

**B-A3. Sniff Out Trouble (`ta006`)** [decided by us, please confirm]
- Text: "Hero Action: Discard cards from the encounter deck until you discard a minion or side scheme. Reveal that card -> draw 2 cards and ready each KAMA upgrade you control."
- Ambiguity: what if the encounter deck runs out without a minion or side scheme?
- Our current reading: nothing is revealed, so nothing is drawn or readied (the discarded cards stay discarded; the deck is not reshuffled). Question: correct?

Smaller readings settled without asking: Prowl's "printed [mental] resource" means a printed mental icon only (a wild resource does not count); "Daze" = place the Dazed status card; Pounce's "1 damage" plus "2 additional damage for each ..." is one hit of 1 + 2n; Alopex's Kama / Alopex's Other Kama (14/15) have one blade illustration across both cards, which we display as a panorama.

## B-V. Venus (Venus v3)

**B-V1. "(to a maximum of 6)" (`tv001a`)** [decided by us, please confirm]
- Text: "Action: Place 1 dredge counter on Venus for each ELEMENT upgrade you control (to a maximum of 6). (Limit once per round.)"
- Our current reading: the maximum applies to the total number of dredge counters on Venus (not only to the number placed per activation). Question: correct?

**B-V2. Hazard icon on Faulty Creation (`tv015`)** [decided by us, please confirm]
- Text: "Give to the Bonnie player. You may flip to alter-ego form. Alter-Ego Action: Exhaust Bonnie -> remove Faulty Creation from the game." The card shows a Hazard icon (tilted card and cross).
- Our current reading: it is a real Hazard 1 (one extra encounter card per villain phase while the obligation is in play). Question: correct, or is it template decoration (the same glyph appears on Jasper Barlow's Lab)?

**B-V3. Eldritch Lance (`tv005`)** [decided by us, please confirm]
- Text: "Hero Action (attack): Deal 5 damage to an enemy. This attack gains overkill. Draw 1 card for each [wild] resource used to pay for this card."
- Ambiguity: all [wild] resources spent, or only those needed to pay the cost of 4?
- Our current reading: only the [wild] resources actually needed to pay the cost (never surplus), so two Evanescence cards (GGG + GGG) draw 4 cards, not 6. Question: correct?

Venus also has the two cards Dragon Scale and Turtle Shell, whose illustrations look continuous; our maintainer decided to show them as two separate cards (no panorama). Question: are they meant to be a panorama pair?

## B-S. Shredder scenario and TMNT Standard / Expert sets

**B-S1. Bladed Armor: "take 1 damage" (`ts006`)** [decided by us, please confirm]
- Text: "Hero Action: If there are no cloaked status cards on Shredder, take 1 damage and spend 1 resource of any type -> discard this card."
- Ambiguity: who takes the damage?
- Our current reading: the identity of the player who pays (a cost, as with "take 1 damage ->" on official cards). Question: correct?

**B-S2. Intense Combatants (`te201`) and "intensify"** [decided by us, please confirm]
- Text: "Permanent. Setup. Forced Interrupt: When a status card would be placed on a character, if that character already has 1 copy of that status card on them, intensify them instead."
- Our reading, based on the Intensified card from your Discord server: "The next time this character would discard a status card, discard this status card instead. This card cannot be given to a character that has no status cards." "Intensify X" = give X an Intensified status card. See B-G below for the details we settled. Question: correct?

**B-S3. Which "Standard" set does Shredder use? (`ts004a`)** [decided by us, please confirm]
- Text: "Content: Shredder, Shadow of the Foot, and Standard sets."
- Ambiguity: your zip contains two Standard sets (the TMNT-specific Standard-Expert set with No Quarter, Outmatched, Pursued by Shadows, Skulk...; and "Normal Standard-Expert Reskins", the ten core cards with TMNT art).
- Our current reading: the TMNT-specific Standard (and Expert) set is the default for every TMNT scenario; the reskins are available as an interchangeable option. Question: correct?

**B-S4. Foot Ninja (`ts010`)** [decided by us, please confirm]
- Text: "Forced Interrupt: When Foot Ninja is defeated, shuffle them into the encounter deck."
- Ambiguity: replacement ("instead of being defeated") or after the defeat?
- Our current reading: Foot Ninja IS defeated (the defeat counts, for instance for "After a FOOT CLAN minion is defeated, place 1 threat") and is then shuffled in instead of being discarded. Question: correct?

**B-S5. Kira no Ken (`ts103`)** [decided by us, please confirm]
- Text: "Attach to Karai. If Karai is not in play, search the encounter deck and discard pile for Karai and reveal her. Then, attach this card to her."
- Ambiguity: what if Karai cannot be found?
- Our current reading: the attachment is discarded. Question: correct?

**B-S6. "Karai" (`ts101` and `tl015`)** [decided by us, please confirm]
- Karai appears as a Shredder minion (`ts101`) and as Leonardo's nemesis minion (`tl015`). Our current reading: they are the same unique character, and every card that says "Karai" (Ocho's boost, Kira no Ken) can find or attach to either. Question: correct?

**B-S7. Kuro Kabuto, boost (`ts007`)** [decided by us, please confirm]
- Text: "Boost: Attach Kuro Kabuto to Shredder."
- Our current reading: it attaches after the activation resolves (not instantly during the boost). Question: correct?

**B-S8. One Cloaked card per character (insert)** [decided by us, please confirm]
- Insert text: "Normally characters can only have one Cloaked status card on them at a time, but the Shredder can have more than one, depending on his villain stage." and "Unless otherwise specified, a character can only have one Cloaked status card placed on them."
- Our current reading: cap of ONE Cloaked per character (Shredder 2 / 3 / 4 by stage), including for cards such as Improvised Tactics (`td005`), Karai and Foot Soldiers; a "Cloak X" on an already cloaked X does nothing (this is what "If you cannot" in Foot Rikugun, `ts020`, refers to). Question: correct?

## B-X. Baxter Stockman scenario

**B-X1. Baxter Blaster: the star in the ATK box (`tx005`)** [decided by us, please confirm]
- Text: "Attach to Baxter Stockman. [star] Forced Response: After Baxter Stockman attacks and damages a friendly character, daze them. Hero Action: Exhaust your hero or spend 2 resources of any type -> discard this card. [star] Boost: Attach Baxter Blaster to Baxter Stockman." The ATK box shows a star and no number.
- Our current reading: the star only flags the starred rules lines; it gives no ATK bonus. Question: correct?

**B-X2. Wrapped Up (`tx016`)** [decided by us, please confirm]
- Text: "When Revealed: Daze a friendly character. If you cannot, this card gains surge."
- Our current reading: the player to whom the card is revealed chooses among ALL friendly characters (all players' identities and allies). Question: correct?

**B-X3. Auto Defense Bots (`tx017`)** [decided by us, please confirm]
- Text: "Enters play with 1 shield counter on them. Forced Interrupt: When this minion would be defeated, heal all damage from this minion, and remove 1 shield counter from here instead."
- Ambiguity: with no shield counter left?
- Our current reading: the Interrupt does not apply, and the minion is defeated normally. Question: correct?

**B-X4. FLYBORG vs FLYBORGS** (see A1.6 and A1.7) [decided by us, please confirm]

**B-X5. all-purpose counter** (`tx004b`, `tx006`): we follow the official FAQ that the card holding the counter defines its type (swarm / ooze / cable / shield). Question: OK?

## B-B. Bebop & Rocksteady

**B-B1. Headfirst: "your identity" (`tk007b`)** [decided by us, please confirm]
- Text: "Special: Deal 1 damage to your identity." (triggered by "After Bebop takes damage, resolve the 'Special' ability on the HOG attachment.")
- Our current reading: the identity of the player who damaged Bebop (the first player if no player did). Question: correct, or the first player always, or every player?

**B-B2. Headfirst / Headstrong: the activation that triggers the flip (`tk007b`, `tk008b`)** [decided by us, please confirm]
- Text: "Forced Interrupt: When Bebop would activate, if Headstrong is in play, flip Bebop and Rocksteady to their K.O. sides and flip both TEMPER attachments to their ROWDY sides."
- Our current reading: that activation becomes a K.O. villain activation: it is replaced by removing 1 knucklehead counter (2 in expert) from the Temper attachment now on its ROWDY side. Question: correct, or is the activation cancelled without removing a counter, or does it happen with K.O. values?

**B-B3. Lay the Beatdown (`tk022`)** [decided by us, please confirm]
- Text: "When Revealed (Hero): Choose: Deal 2 indirect damage to your hero. / Stun your hero."
- Our current reading: 2 indirect damage to the hero only (no spreading to allies). Question: correct, or the usual indirect damage split among hero and allies?

**B-B4. Road to Ruin (`tk102`)** [decided by us, please confirm]
- Text: "When Revealed: Choose: Discard a friendly LOCATION. / Stun your hero."
- Our current reading: "Stun your hero" is available in hero form only (in alter-ego form with no LOCATION, nothing happens). Question: correct?

**B-B5. Hittin' the Town (`tk201`)** [decided by us, please confirm]
- Text: "When Revealed: Discard cards from the top of the villain deck until an attachment or side scheme is discarded and reveal it."
- Our current reading: "villain deck" = the encounter deck. Question: correct?

**B-B6. Power Play (`tk109`)** [decided by us, please confirm]
- Text: "Hero Response: After you remove threat from this scheme, discard 1 card from your hand -> remove 2 threat from this scheme."
- Our current reading: removing the 2 threat is itself "removing threat", so the Response can trigger again as long as you have cards to discard. Question: correct?

**B-B7. Shutter Shades / Aviator Cap: "When Revealed" when the card does not attach (`tk009`, `tk010`)** [decided by us, please confirm]
- Text: "Attach to Bebop if he is ALERT. Otherwise, this card gains surge. ... When Revealed: Place 1 knucklehead counter on the HOG attachment."
- Our current reading: "When Revealed" always resolves (the counter is placed even if the card could not attach, then it gains surge). Question: correct?

**B-B8. Destructive Dunderheads: activation order (`tk006a`)** [decided by us, please confirm]
- Text: "Double Trouble - During step two of the villain phase, both villains activate against each player. Choose either Bebop or Rocksteady as the target for each card that references 'the villain'."
- Our current reading: the FIRST PLAYER chooses, for each player, which of Bebop or Rocksteady activates first (simultaneous effects rule). Question: correct?

## B-AGG. Aggression aspect

**B-AGG1. Flow of Battle: "Prerequisite (MARTIAL ARTIST)" (`ua019`)** [decided by us, please confirm]
- Text: "Prerequisite (MARTIAL ARTIST). Max 1 per player. Hero Response: After you attack and exactly defeat an enemy, discard this card -> draw 3 cards." Only one official card uses "Prerequisite" (Defend Our City, 61029) and nothing implements it.
- Our current reading: the card can only be PLAYED if your identity has the MARTIAL ARTIST trait. Other readings: deck-construction restriction only; both. Question: which?

**B-AGG2. Slash: "take 3 damage" (`ua037`)** [decided by us, please confirm]
- Text: "Forced Response: After Slash enters play, take 3 damage."
- Our current reading: you (your identity) take the 3 damage; Slash stays at 5 HP. The alternative is "Slash takes 3". Question: correct?

**B-AGG3. Pete: "After you deal damage to an enemy" (`ua033`)** [decided by us, please confirm]
- Text: "Response: After you deal damage to an enemy, exhaust Pete and remove 1 pistol counter from him -> deal 1 damage to that enemy."
- Our current reading (same as the engine's reading of official Schadenfreude): damage dealt by your identity and by cards you play (attack events included); an ALLY's attack does not trigger Pete. Question: correct?

## B-BAS. Basic aspect

**B-BAS1. Fugitoid (`ub014`)** [our provisional reading, not yet decided]
- Text: "[star] Response: After Fugitoid uses a basic power, discard 1 card from your hand. If that card's printed resource has: [physical] - Heal 2 damage from a friendly character. [mental] - Remove 2 threat from a scheme. [energy] - Deal 2 damage to an enemy. [wild] - Draw 1 card."
- Our current reading: you choose the card to discard; each icon present on the discarded card triggers its line (a card with two icons triggers two lines); with an empty hand nothing happens. Question: correct?

**B-BAS2. Honorable Blades "Team-Up"** (see A3.5) [decided by us, please confirm]: Team-Up (Leonardo and Usagi Yōjimbō) requires both characters in play (identity or ally); Usagi is the Protection ally `up041`. That is how we implement Team-Up. Question: correct?

## B-LEA. Leadership aspect

**B-LEA1. Shōgun and Mushroom (cosmetic)**: see A5.7 and A5.8.

**B-LEA2. Mushroom / Weasel In: "Linked (Weasel In)" (`ul041`, `ul040`)** [our provisional reading, not yet decided]
- Text: Mushroom "Linked (Weasel In). Musroom does not count against your ally limit. When Revealed: Heal 2 damage from a friendly character and put Mushroom into play under your control. This card gains surge. This effect cannot be canceled."
- Our current reading: Linked (X) as in the official game: Mushroom starts set aside and is only reachable through Weasel In's effects. Question: correct?

## B-PRO. Protection aspect

**B-PRO1. Redirection Mastery**: see A6.1.

## B-DUA. Dual-Aspect

**B-DUA1. Heavy Metal: "place a status card on a character" (`ud003`)** [decided by us, please confirm]
- Text: "Heavy Metal enters play with 2 amp counters on her. Response: After Heavy Metal takes consequential damage, remove 1 amp counter from her -> place a status card on a character."
- Ambiguity: which status cards are allowed? Our game knows seven: Stunned, Confused, Tough, Cloaked, Dazed, Intensified, Exposed (Exposed comes from another custom pack).
- Our current reading (decided): any status card the game knows (all seven), the player's choice, among those the character can receive. Alternatives: only the three official ones; the official three plus your three (Cloaked, Dazed, Intensified). Question: which did you intend?

**B-DUA2. Stealth Fighter**: see A7.1.

**B-DUA3. Sōhei: "your hero gets +2 hand size" (`ud005`)** [decided by us, please confirm]
- Text: "Toughness. Interrupt: When Sōhei is defeated by consequential damage, your hero gets +2 hand size until the end of the round."
- Ambiguity: an ally can be defeated by consequential damage while the player is in alter-ego form.
- Our current reading (decided): "your hero" = your identity in either form, so the bonus also applies when the player is in alter-ego form. Alternatives: hero form only; or the bonus waits until the player flips to hero form before the round ends. Question: which did you intend?


## B-ADD. Further readings settled on 17 October 2026

**B-ADD1. Chance Encounter, Venus (Bonnie), Zone of Silence, I Can Do This All Day:** see A4.1, A4.2, A4.3, A6.2.

**B-ADD2. Slash (Aggression, `ua037`) and Pete (`ua033`):** see B-AGG2 and B-AGG3. Decided exactly as listed there.

**B-ADD3. Prerequisite (MARTIAL ARTIST) on Flow of Battle (`ua019`):** decided: the card can only be played if your identity has the MARTIAL ARTIST trait (see B-AGG1).

## B-G. General mechanics: status cards and keywords

**B-G1. Cloaked status card** [decided by us, please confirm]
- Printed: "The next time this character uses a basic power or activates, increase that value by 2, then discard this status card. The next time this character would take any amount of damage, decrease that value by 2, then discard this status card."
- Our current reading: ONE effect only: whichever comes first (+2 to the next basic power / activation, or -2 to the next damage, minimum 0), then the card is discarded. A basic power includes THW, ATK, DEF and REC. Question: correct, or can the card give both effects (two discards)?

**B-G2. Dazed status card** [decided by us, please confirm]
- Printed: "The next time this character uses a basic power or activates, decrease that value by 2, then discard this status card. The next time this character would take any amount of damage, increase that value by 2, then discard this status card." plus the Dazed Rules insert.
- Our current reading: one Dazed per character; only one effect then the card goes; Tough resolves before Cloaked, and Cloaked and Dazed resolve simultaneously (so 1 damage with both = 1 - 2 + 2 = 1 and both are discarded); a defense: -2 DEF then the card goes before excess damage (no +2); an ally with consequential damage: the ATK/THW drops, the card goes, so consequential damage is not increased; piercing: Tough goes first and then Dazed adds +2. Question: all as you intended?

**B-G3. Intensified status card and "intensify"** (your Discord capture: "The next time this character would discard a status card, discard this status card instead. This card cannot be given to a character that has no status cards.")
- Six readings settled by us [decided by us, please confirm]:
  1. The original status card's EFFECT still happens; only its DISCARD is replaced (a Stunned character still has its attack cancelled, but the Stunned card stays).
  2. If several status cards are discarded at once, each Intensified replaces ONE discard; the others go.
  3. Scope: any discard of a specific status card (consumption, player card effects, piercing); NOT "the character leaves play", NOT "discard each status card", NOT rule-based caps.
  4. Intense Combatants: "already has 1 copy" = at least one copy, for any status card.
  5. Cap: Intensified follows the normal status rules: one per character, two for a Steady character.
  6. Intense Combatants is an optional setup checkbox, off by default, available with TMNT Standard / Expert.
- Question: any of these wrong?

**B-G4. Rampage X** [decided by us, please confirm] (8 cards: Apex Predator, Demolish, Dire Straits, Feral Cunning, Down the Drain, Rubble Rouser, Primal Provisions, Autodefenestration)
- Printed: "[star] Rampage 3. (As an additional cost for this card, take 3 damage and discard 3 cards from the top of your deck.)"
- Our current reading: the star is the Rules Reference "star icon" reminder with no effect of its own; the cost is paid together with the resource cost; if the damage is prevented (Tough) the cost is not paid and the card is not played; if your deck has fewer than X cards you still play the card, discard what is left, reshuffle the discard pile and take one encounter card (no further discards from the new deck). Question: correct?

**B-G5. Discount X (TRAIT)** (`ua030` Nerve Strike): "[star] Discount 1 (MARTIAL ARTIST)" = costs X less if you control any card with the trait (identity, ally or upgrade). Question: OK?

**B-G6. Team-Up** (Honorable Blades): our implementation requires both named characters to be in play (identity or ally). Question: OK?

**B-G7. Linked (X)**: see B-LEA2 and the Bebop & Rocksteady cards Channel 6 News, Eastman Theater, Powder Keg and Power Play (all "Linked (Welcome to the Jungle)"). Question: OK?

**B-G8. Intense Combatants option** (`te201`): see B-S2 and B-G3.

---

# Part C: Cross-card name conflicts (uniqueness)

Marvel Champions allows only one copy of a unique card (same title) in play. Our general reading: **cards with the same title are the same character and cannot be in play together**; **the "✦ original title" banner under a title counts as a second unique title** of the same card (for example "Bo-Wing" with the banner "✦ Winter Soldier" cannot be in play with a card titled Winter Soldier, and vice versa). Please confirm this reading, or tell us which of the following pairs should be allowed to coexist.

| # | Name | Cards | Our current reading |
|---|---|---|---|
| C1 | Nobody | Alopex's ally Nobody, subtitle "Angel Bridges" (`ta002`) vs Protection ally Nobody, subtitle "Angel Bridge" (`up024`) | Same character; they cannot coexist [decided by us, please confirm]. (Spelling of the subtitle: see A6.6) |
| C2 | Alopex | Hero Alopex (`ta001a`/`ta001b`) vs Leadership ally Alopex (`ul001`) | Same character; an Alopex player cannot put the ally into play [decided by us, please confirm] |
| C3 | Venus | Hero Venus (`tv001a`/`b`) vs Justice ally Venus, "Bonnie", banner "Manifold" (`uj036`) vs Leadership ally Venus, "Bonnie" (`ul039`) | Same character; no two can coexist (the two Bonnie allies not either) [decided by us, please confirm] |
| C4 | Splinter | Leonardo's ally Splinter (`tl002`), Leadership ally Splinter (`ul029`), Basic support Splinter with banner "Stick" (`ub053`), Aggression ally Ujigami with subtitle "Splinter" and banner "Shang-Chi" (`ua040`) | Same title = same character; no two Splinters in play together [decided by us, please confirm; the support `ub053` follows the same rule; the subtitle of `ua040` is covered by the sub-title rule in C12] |
| C5 | Slash | Michelangelo's ally Slash (`tm002`), Aggression ally Slash (`ua037`), Basic ally Slash with banner "Hulk" (`ub048`) | Same character; they cannot coexist [decided by us, please confirm] (`ub048` also cannot coexist with a Hulk card because of its banner) |
| C6 | Casey Jones | Hero/alter ego Casey Jones (`tc001a`/`b`), Raphael's ally Casey Jones (`tr002`), Basic ally Casey Jones, no subtitle (`ub005`) | Same character; only one Casey Jones in play (so `ub005` is unplayable in a Casey Jones deck) [decided by us, please confirm]. Alternative: give the two allies different subtitles |
| C7 | Leonardo | Hero (alter ego "Leo") (`tl001a`/`b`) vs Basic ally Leonardo, subtitle "Leo" (`ub025`) | Same character; a Leonardo player cannot play the ally [decided by us, please confirm] |
| C8 | Donatello | Hero (alter ego "Donnie") (`td001a`/`b`) vs Basic ally Donatello, "Donnie" (`ub008`) | Same, as above [decided by us, please confirm] |
| C9 | Michelangelo | Hero (alter ego "Mikey") (`tm001a`/`b`) vs Basic ally Michelangelo, "Mikey" (`ub029`) | Same, as above [decided by us, please confirm] |
| C10 | Raphael | Hero (alter ego "Raph") (`tr001a`/`b`) vs Basic ally Raphael, "Raph" (`ub041`) | Same, as above [decided by us, please confirm] |
| C11 | Jennika | Hero (alter ego "Jenny") (`tj001a`/`b`) vs Basic ally Jennika, "Jenny" (`ub022`) | Same, as above [decided by us, please confirm]. (Note: her Response fetches a Shinobi card, which only a Jennika deck contains) |
| C12 | Sub-titles equal to the turtles' alter-ego names | Dual-Aspect allies: Rōnin "Mikey" (`ud001`), Doomsayer "Donnie" (`ud002`), Heavy Metal "Jenny" (`ud003`), Stealth Fighter "Raph" (`ud004`), Sōhei "Leo" (`ud005`), Nightwatcher "Jenny" (`ud006`); and the single-aspect allies with the same sub-titles: Assassin "Leo" (`ua003`), Bo-Wing "Donnie" (`ua006`), Commando "Raph" (`ua012`), He-Dude "Mikey" (`ua022`), Cowabunga "Mikey" (`uj004`), Hatamoto "Donnie" (`uj012`), Night-Blade "Leo" (`uj023`), Ram-Shell "Raph" (`uj026`), Red Shell "Raph" (`ul021`), Shōgun "Leo" (`ul025`), Turtle Titan "Mikey" (`ul036`), Turtle-At-Arms "Donnie" (`ul037`), Cyber Ninja "Donnie" (`up007`), Honor Blade "Leo" (`up017`), Road Rage "Raph" (`up031`), Wonder Turtle "Mikey" (`up043`) | Two judges disagree in our project: our deck-builder treats a sub-title equal to a hero's alter-ego title (or to another unique card's sub-title) as "the same character" (so Rōnin "Mikey" cannot go in Michelangelo's deck, and Heavy Metal and Nightwatcher "Jenny" cannot be together); our game engine only conflicts when the TITLE and the sub-title are both equal. Our maintainer decided: the sub-title IS the character, so these allies are "versions" of that turtle and are exclusive with it (the game engine now applies this to TMNT cards; official cards of other packs keep their previous behaviour). Is that what you intended? [decided by us, please confirm] |
| C13 | Old Hob | Raphael's nemesis minion Old Hob (`tr015`) vs Leadership ally Old Hob with banner "White Wolf" (`ul019`) | Different card types; we assume the enemy and the ally can be in play together (the ally is not a copy of the enemy). Question: is that right? [our provisional reading, not yet decided] |
| C14 | Karai | Shredder's minion Karai (`ts101`) vs Leonardo's nemesis minion Karai (`tl015`) | Same unique character; "Karai" in any card text can refer to either (see B-S6) [decided by us, please confirm] |
| C15 | Baxter Stockman | Villain Baxter Stockman I / II / III (`tx001` to `tx003`) vs Donatello's nemesis minion Baxter Stockman (`td015`) | Searches by card id so they do not interfere; they can coexist in play. Question: OK? [our provisional reading, not yet decided] |

**"✦ original title" banners.** In our data these 35 cards have a banner that we treat as a second unique title (a card with the banner title cannot be in play together with a card carrying that title, and vice versa): Bo-Wing "Winter Soldier" (`ua006`), Exeen "Angela" (`ua017`), He-Dude "Two-Gun Kid" (`ua022`), Rave "Bug" (`ua035`), Ujigami "Shang-Chi" (`ua040`), April O'Neil "Nick Fury" (`ub001`), Atilla "Spider-Man" (`ub003`), Clyde "Ironheart" (`ub006`), E.P.F. R.N.D. "Weapon X" (`ub012`), Genghis "White Fox" (`ub015`), Herold Lilja's Lab "Cerebro" (`ub018`), Mary "Mockingbird" (`ub028`), Onmyōdō Saikō "The Sorcerer Supreme" (`ub034`), Rupert's Pizzeria "X-Mansion" (`ub043`), Slash "Hulk" (`ub048`), Splinter "Stick" (`ub053`), The Market "X-Bunker" (`ub056`), Night-Blade "Agent Coulson" (`uj023`), Ram-Shell "Spider-Woman" (`uj026`), Screwloose "Dagger" (`uj028`), Venus (Bonnie) "Manifold" (`uj036`), Wingnut "Cloak" (`uj038`), Zebulon "Squirrel Girl" (`uj039`), Napoleon "Squirrel Girl" (`ul017`), Old Hob "White Wolf" (`ul019`), Rasputin "Maria Hill" (`ul020`), Red Shell "Iron Fist" (`ul021`), Turtle-At-Arms "Misty Knight" (`ul037`), Zetian "White Tiger" (`ul046`), Ace Duck "Brother Voodoo" (`up001`), Grotto "Iron Fist" (`up014`), Honor Blade "Patriot" (`up017`), Lindsey Baker "The Night Nurse" (`up022`), Seymour Gutz "Rogue" (`up034`), Wonder Turtle "White Widow" (`up043`). Question: is the banner meant as the card's original identity for uniqueness purposes, as we assume? Note that Napoleon and Zebulon share the banner "Squirrel Girl", as do Red Shell / Grotto ("Iron Fist"); under our reading, each pair cannot be in play together. Is that intended?

---

# Part D: Our other assumptions

These are decisions we made about how to render or interpret your content; none is a question about a particular card, but tell us if any is wrong.

**D1. Intensified status card.** We never received a card scan; we took the card text from a Discord screenshot (Bebop & Rocksteady server) and cropped its art. Can you confirm that text, and that "Intensified" is meant to be a seventh status card with a back like the others?

**D2. Rampage X.** The keyword is not defined in any rulebook, so we defined it from the reminder text printed on your cards (see B-G4), and we treat the star in the cost ("3*") as a reminder only.

**D3. Reskins.** We separate two kinds: (a) a TMNT card that differs from an official card only by its illustration (we count 64 after merging the identical ones, plus 3 double resources kept as cards): in our digital deck-builder it appears as an alternative art of the official card, offered to every hero and used automatically for a TMNT hero; no duplicate card exists; (b) a TMNT card where ANYTHING else differs (name, traits, text, cost, resource icon, uniqueness, banner; we count 84): it is a TMNT-exclusive card with its own entry. Question: is this how you would classify them? In particular, "reskin" cards whose resource icon differs from the official card (for example "You Got This!") are treated as new cards.

**D4. Resource and keyword icons identified by comparison.** Where an icon was ambiguous (resource colour, Crisis, Hazard, Acceleration, Amplify, boost icons), we identified it by overlaying the silhouette on the official icon (for example Sewer Problems = Crisis 1, Mutagen Bomb = Amplify 1, Faulty Creation = Hazard 1). Let us know if any identification is wrong.

**D5. Paired illustrations (cards 14/15).** Where the illustration runs continuously across two cards (Alopex's Kama / Other Kama, Jennika's Tekko-Kagi pair), we display the two cards side by side as a panorama, and a pair with an exhausted card is shown darkened with a marker. We did not do this for Venus's Dragon Scale / Turtle Shell (judged not continuous). Question: are there other pairs?

**D6. Inserts are not cards.** The rule inserts (Katana Weapon Rules, Sai Weapon Rules, Michelangelo Insert, Dazed Rules, Shredder Cloaked Rules, the Path card back) are implemented inside the scripts of the cards they concern; no card is created for them.

**D7. A new "Path" card type** for Sōsaiken (see B-J3), and the Linked / Prerequisite / Discount keywords (see Part B), implemented the way the official game does where an official equivalent exists.

**D8. Cards with a missing referent.** None any more: Honorable Blades (A3.5) is integrated, with Usagi Yōjimbō as the Protection ally `up041`.

**D9. Text we corrected on display.** We display "character" (A1.1), "4 cards" (A4.3), "Unified Strike" (A5.5), "Hero Interrupt" in "I Can Do This All Day" (A6.2) and the French translation of Welcome to the Jungle; every other typo is shown as printed. We would of course correct more if you confirm they are typos.

---

# To verify before sending

(Notes for the sender; delete this section before sending.)

1. **Sender name and signature** are not in our files; add yours at the end.
2. **Quotations.** Most quotes were taken from our card database (`cards.json`) and from the notes written while scanning, not re-read on the scan images for this document. Entries where the printed text comes only from our notes (so please re-check against the scan before sending): A1.1 ("charcter" in `ta012`), A1.3, A1.4, A1.5, A1.6 (the singular "MOUSER or FLYBORG" in `td014`; our database now shows the plural "MOUSERS or FLYBORGS"), A1.9 ("VENUS (2/16)"; we do not know the printed denominator of the other Venus cards, only that the 15 scans are numbered 1 to 15), A1.10/A1.11 (WORMS!, the blank cost in `tm009`), A3.5 (Honorable Blades; not in our database), A4.3 ("4 card cards"; our database already shows "4 cards"), A5.5 ("Unified Stike": our database still has the typo), A6.3 ("Intterupt") and A6.4 ("Seymor").
3. **Part A, rows A1.10 and A1.11** (WORMS! and the blank cost of `tm009`) come from our notes only; re-read both on the scans.
4. **Chain Reaction and Combo Move (A2.2, A2.3).** We were told these two are signed "Reskins" on the scans but have no official counterpart; the exact credit wording on the scan was not found in the files, so check the scans.
5. **Usagi Yōjimbō (A3.5).** Resolved: the ally exists as `up041` and Honorable Blades is integrated. Nothing to adjust.
6. **Status tags.** "Decided by us" means the maintainer ruled on it (up to 17 October 2026). All the aspect-card decisions of 17 October are now applied in the code. Remaining "provisional" entries: A3.3 (Atilla), A3.4 (Gofu Talisman), B-BAS1 (Fugitoid), B-LEA2 (Mushroom / Linked), C13, C15 (never put to the maintainer).
7. **Shredder Q9** (French word for "daze": "hébété") is a translation matter and is deliberately not in this document.
8. **B-G3 wording of the Intensified card** comes from a Discord screenshot in our repo (`.planning/tmnt/intensified-capture.webp`); confirm it before quoting.
9. **Counts quoted in D3** (64 + 3 / 84) and the 35 banners in Part C are measurements from our data on 17 October 2026 (the conversion of the 64 art-only reskins was in progress when this was written: recheck).
10. **Part C, C13 and C15** are our own extensions (not explicitly decided anywhere in the files); remove them if you prefer a shorter document.
11. **Skipped details.** Test-level and engine-level notes (bug fixes to official cards, deck-builder behaviour) were left out on purpose as irrelevant to the creator.

---

Thank you very much for your time, and for the wonderful content. Any answer, even partial, helps us make your cards behave as you intended.

[Your name]
