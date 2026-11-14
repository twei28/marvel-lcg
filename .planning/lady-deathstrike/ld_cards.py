# Definitions des cartes LADY DEATHSTRIKE (Mysteltainn, scenario custom « MC Custom Content By: Mysteltainn »), 25/10/2026.
# Relues une a une contre les scans (zip « LadyDeathstrike », 31 images dont 4 Bleeding Out identiques).
# Icones identifiees par COMPARAISON AVEC LES GLYPHES de public/fonts/ChampionsIcons.ttf (mots-cles/hazard.md) :
#   Bide Time = Crisis (C), Stalking Prey = Hazard (H), Chop-Shop Cybernetics = Amplify (F).
# Doublons du zip (verifies au pixel pres, hors pied de carte) : Bleeding Out 5-8, Nanoskeleton 9-10, Tracker 13-15,
# Bide Time 17-18, Lash Out 20-21, Mutant Hunter 22-23, Inhibitor Collar 3-4 : UNE carte, plusieurs exemplaires.
# Inseres dans data/cards.json par inserer_lady_deathstrike.py (idempotent).

K = "Mysteltainn"
SET = "Lady Deathstrike"
MOD = "Reaver Resources"
SPECIAL = '"<b>Special</b>"'

CARDS = [
    {"card_id": "ld001", "type": "Villain", "name": "* Lady Deathstrike", "subtitle": "",
     "desc": {"HP": "16*", "ATK": "2", "SCH": "1", "Stage": "1"}, "traits": ["REAVER"], "set_name": SET,
     "text": f"<b>Forced Response</b>: After Lady Deathstrike attacks and damages you, resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity.\n"
             "<i>\"Your arrogance will cost you your life!\"</i>", "custom": K},
    {"card_id": "ld002", "type": "Villain", "name": "* Lady Deathstrike", "subtitle": "",
     "desc": {"HP": "18*", "ATK": "3", "SCH": "1", "Stage": "2"}, "traits": ["REAVER"], "set_name": SET,
     "text": f"<b>When Revealed</b>: Find Reinforced Adamantium Claws and reveal it. If you cannot, resolve the {SPECIAL} ability on each copy of Bleeding Out in play.\n"
             f"<b>Forced Response</b>: After Lady Deathstrike attacks and damages you, resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity.", "custom": K},
    {"card_id": "ld003", "type": "Villain", "name": "* Lady Deathstrike", "subtitle": "",
     "desc": {"HP": "19*", "ATK": "3", "SCH": "1", "Stage": "3"}, "traits": ["REAVER"], "set_name": SET,
     "text": f"<b>When Revealed</b>: Resolve the {SPECIAL} ability on each copy of Bleeding Out in play. Find Reaver Commander and reveal it.\n"
             f"<b>Forced Response</b>: After a [[REAVER]] attacks and damages you, resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity.", "custom": K},
    {"card_id": "ld004a", "type": "MainScheme", "name": "Mutant Hunting Season", "subtitle": "",
     "desc": {"Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<b>Contents</b>: Lady Deathstrike (I) and Lady Deathstrike (II) <i>(Lady Deathstrike (II) and Lady Deathstrike (III) for expert mode)</i>. Lady Deathstrike, Reavers and Standard encounter sets. One modular set <i>(Military Grade or Reaver Resources)</i>.\n"
             "<b>Setup</b>: Attach a copy of Bleeding Out to each player, then set each remaining copy aside. Place 3 bleed counters on each copy of Bleeding Out.", "custom": K},
    {"card_id": "ld004b", "type": "MainScheme", "name": "Mutant Hunting Season", "subtitle": "",
     "desc": {"StartingThreat": "1*", "TargetThreat": "9*", "EscalationThreat": "1*", "Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<i>With the stage set, Lady Deathstrike declares open season on the wounded heroes!</i>\n"
             "<b>Forced Response</b>: After a player deck empties, place an acceleration token here.\n"
             "<b>If this scheme is completed, the players lose the game.</b>", "custom": K},
    {"card_id": "ld005", "type": "Attachment", "name": "Bleeding Out", "subtitle": "",
     "desc": {"Permanent": "1"}, "traits": ["CONDITION"], "set_name": SET,
     "text": f"Permanent. Attach to your identity.\n<b>Special</b>: Place 1 bleed counter here. Discard cards from the top of your deck equal to the number of bleed counters here. If you discard an identity-specific card this way, take 1 damage.\n"
             "<b>Alter-Ego Action</b>: Discard a card from your hand → remove 2 bleed counters from here.", "custom": K},
    {"card_id": "ld006", "type": "Attachment", "name": "Adamantium Nanoskeleton", "subtitle": "",
     "desc": {"Boost": "2"}, "traits": ["ARMOR"], "set_name": SET,
     "text": f"Attach to Lady Deathstrike.\n<b>Forced Interrupt</b>: When a player attacks Lady Deathstrike, prevent all damage that would be dealt to her and resolve the {SPECIAL} ability on the copy of Bleeding Out attached to that player's identity instead. Then, discard this card. <i>(Max once per attack.)</i>", "custom": K},
    {"card_id": "ld007", "type": "Attachment", "name": "Reaver Commander", "subtitle": "",
     "desc": {}, "traits": ["TITLE"], "set_name": SET,
     "text": "Attach to Lady Deathstrike.\nLady Deathstrike gains steady.\n<b>Forced Response</b>: After an ally is defeated by a [[REAVER]], place 1 threat on the main scheme.\n"
             "<b>Hero Action</b>: Spend [mental][mental] resources → discard this card.\n[star] <b>Boost</b>: Reveal this card.", "custom": K},
    {"card_id": "ld008", "type": "Attachment", "name": "Reinforced Adamantium Claws", "subtitle": "",
     "desc": {"ATK+": "1*"}, "traits": ["WEAPON"], "set_name": SET,
     "text": f"Attach to Lady Deathstrike.\n[star] Lady Deathstrike's attacks gain piercing.\n<b>Hero Response</b>: After you attack Lady Deathstrike, resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity → discard this card.\n[star] <b>Boost</b>: Reveal this card.", "custom": K},
    {"card_id": "ld009", "type": "Minion", "name": "Reaver Tracker", "subtitle": "",
     "desc": {"HP": "3", "ATK": "2", "SCH": "1", "Boost": "1"}, "traits": ["REAVER"], "set_name": SET,
     "text": f"<b>When Revealed</b>: Resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity. If you did not discard an identity-specific card this way, place 1 threat on the main scheme.\n"
             "<i>\"Now that's a problem. If we don't see the mutant, you die.\"</i>", "custom": K},
    {"card_id": "ld010", "type": "Obligation", "name": "Deep Wound", "subtitle": "",
     "desc": {"Boost": "2", "GiveTo": ""}, "traits": [], "set_name": SET,
     "text": "Your hero gets -1 ATK, -1 THW and -1 DEF.\n"
             "<b>Response</b>: After you resolve the \"<b>Alter-Ego Action</b>\" on the copy of Bleeding Out attached to your identity, discard a card from your hand → discard this card.\n"
             "<i>\"Believe me, it feels worse than it looks.\"</i>", "custom": K},
    {"card_id": "ld011", "type": "SideScheme", "name": "Bide Time", "subtitle": "",
     "desc": {"Boost": "3", "Crisis": "1", "StartingThreat": "2"}, "traits": [], "set_name": SET,
     "text": "<i>Sometimes it is best to conserve energy, and pursue once the quarry is exhausted...</i>\n"
             f"<b>When Defeated</b>: The player who defeated this scheme resolves the {SPECIAL} ability on the copy of Bleeding Out attached to their identity.", "custom": K},
    {"card_id": "ld012", "type": "SideScheme", "name": "Stalking Prey", "subtitle": "",
     "desc": {"Boost": "2", "Hazard": "1", "StartingThreat": "3"}, "traits": [], "set_name": SET,
     "text": "<i>A brief moment of respite isn't what it seems - Lady Deathstrike is merely waiting for the perfect moment to strike!</i>\n"
             "<b>When Revealed</b>: Place additional threat here equal to the number of bleed counters on the copy of Bleeding Out attached to your identity.", "custom": K},
    {"card_id": "ld013", "type": "Treachery", "name": "Lash Out", "subtitle": "",
     "desc": {"Boost": "1"}, "traits": ["SKILL"], "set_name": SET,
     "text": "<b>When Revealed</b>: Lady Deathstrike attacks you <i>(even if you are in alter-ego)</i>. Do not give her a boost card for this attack. If this attack deals any amount of damage, give Lady Deathstrike a tough status card.\n"
             "[star] <b>Boost</b>: Give Lady Deathstrike a tough status card.", "custom": K},
    {"card_id": "ld014", "type": "Treachery", "name": "Mutant Hunter", "subtitle": "",
     "desc": {"Boost": "1"}, "traits": ["SKILL"], "set_name": SET,
     "text": f"<b>When Revealed (Alter-Ego)</b>: Resolve the {SPECIAL} ability on the copy of Bleeding Out attached to your identity. This card gains surge.\n"
             "<b>When Revealed (Hero)</b>: Place 1 bleed counter on the copy of Bleeding Out attached to your identity. Lady Deathstrike attacks you.", "custom": K},
    {"card_id": "ld015", "type": "Attachment", "name": "Integrated Augmentations", "subtitle": "",
     "desc": {"Boost": "2", "ATK+": "1*"}, "traits": ["TECH", "WEAPON"], "set_name": MOD,
     "text": "Attach to the enemy with the highest printed ATK.\nAttached enemy gains retaliate 1.\n[star] Attached enemy's attacks gain ranged.\n"
             "<b>Hero Response</b>: After you attack the attached enemy, spend [energy][mental] resources → discard this card.", "custom": K},
    {"card_id": "ld016", "type": "Attachment", "name": "Titanium Exoskeleton", "subtitle": "",
     "desc": {"Boost": "2"}, "traits": ["ARMOR", "TECH"], "set_name": MOD,
     "text": "Attach to the enemy with the fewest remaining hit points.\nAttached enemy cannot take more than 2 damage from a single attack.\n"
             "<b>Hero Action</b>: Choose to either spend 3 resources of any type or remove a confused or stunned status card from attached enemy → discard this card.", "custom": K},
    {"card_id": "ld017", "type": "Attachment", "name": "Inhibitor Collar", "subtitle": "",
     "desc": {"Boost": "1", "ATK+": "-1"}, "traits": ["TECH"], "set_name": MOD,
     "text": "Attach to your identity.\nTreat your identity's printed text box as if it were blank <i>(except for traits)</i>.\n"
             "<b>Action</b>: Choose to either exhaust a character you control or take 3 damage → discard this card. <i>(Any player can do this.)</i>", "custom": K},
    {"card_id": "ld018", "type": "SideScheme", "name": "Chop-Shop Cybernetics", "subtitle": "",
     "desc": {"Boost": "3", "Amplify": "1", "StartingThreat": "3", "Hinder": "1*"}, "traits": [], "set_name": MOD,
     "text": "<i>Black market cybernetics aren't pretty, but they perform even in adverse conditions.</i>\nHinder 1[per_hero].\n"
             "<b>Forced Response</b>: After a [[TECH]] attachment enters play, give the villain and the attached enemy a tough status card.", "custom": K},
]
