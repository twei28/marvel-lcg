# Definitions des cartes SHANG-CHI (DesignHacker, « SEALED »), 24/10/2026.
# Relues une a une contre les scans (zip « SHANG-CHI (SEALED) »).
# Icones de ressource (verifiees le 24/10 en decoupant les scans, MEME pack) : eclair jaune = energie (Y),
# poing = physique (R), noeuds bleus = mental (B), etoile verte = wild (G). Dans le texte du Flow, l'icone
# noire « etoile » de Throat Punch est la meme forme que l'etoile verte du coin : wild.
# ⚠ Les « copy » du zip ne sont PAS des doublons : meme dessin, ICONE DE RESSOURCE IMPRIMEE DIFFERENTE
# (numeros 1..15 du bas de carte). Flow lit cette icone : chaque impression est un card_id distinct.
# Inseres dans data/cards.json par inserer_shang_chi.py (idempotent).

K = "DesignHacker"
SET = "Shang-Chi"
NEM = "Shang-Chi Nemesis"


def ev(cid, nom, cout, res, texte):
    return {"card_id": cid, "type": "Event", "name": nom, "subtitle": "",
            "desc": {"Cost": str(cout), "RES": res, "Class": "Hero"},
            "traits": ["ATTACK"], "set_name": SET, "text": texte, "custom": K}


TP = ('<b>Hero Action</b> <i>(attack)</i>: Deal 1 damage to the villain. Draw a card.\n'
      '<b>Flow</b>: [wild] → draw 2 additional cards.\n<i>"From Yuan Jing, I draw boldness."</i>')
RK = ('<b>Hero Action</b> <i>(attack)</i>: Deal 1 damage to an enemy.\n'
      '<b>Flow</b> <i>(attack)</i>: [physical] → deal 2 damage to an enemy.\n<i>"From Tang Minzhe, I draw power."</i>')
SD = ('<b>Hero Action</b> <i>(attack)</i>: Deal 3 damage to an enemy. If this is the first event you have played this phase, confuse an enemy.\n'
      '<b>Flow</b>: [mental] → if this attack defeats an enemy, play the next [[ATTACK]] event from your hand at no cost.')
DS = ('<b>Hero Action</b> <i>(attack)</i>: Deal 5 damage to an enemy.\n'
      '<b>Flow</b>: [energy] → this attack gains piercing, ranged, and overkill.\n<i>"Another weapon. With it--I will take his eyes."</i>')
CJ = ('<b>Hero Action</b> <i>(attack)</i>: Choose up to 3 different enemies. Deal 1 damage to each of them.\n'
      '<b>Flow</b> <i>(attack)</i>: [physical] → deal 2 damage to the villain.\n<i>"From Kho Danghai, I draw resilience."</i>')
AB = ('<b>Hero Action</b> <i>(attack)</i>: Deal 1 damage to a minion. Place 1 additional counter on an upgrade with any type of counters on it.\n'
      '<b>Flow</b>: [energy] → choose up to 2 upgrades with any type of counter on them. Place 2 additional counters on each of them.')

CARDS = [
    {"card_id": "shc001a", "type": "Hero", "name": "* Shang-Chi", "subtitle": "",
     "desc": {"HP": "9", "ATK": "1", "THW": "1", "DEF": "1", "HS": "5"},
     "traits": ["AVENGER", "MARTIAL ARTIST"], "set_name": SET,
     "text": '<i>Chi Mastery</i> — <b>Response</b>: After you resolve a "<b>Flow</b>" ability, ready Shang-Chi.\n'
             '<i>"Every pilgrim\'s journey begins with but a single step. This, then, was mine. Countless more await me over the horizon...yet walk them I will."</i>',
     "custom": K},
    {"card_id": "shc001b", "type": "AlterEgo", "name": "* Shang-Chi", "subtitle": "",
     "desc": {"HP": "9", "REC": "4", "HS": "6"},
     "traits": ["MARTIAL ARTIST"], "set_name": SET,
     "text": '<i>Multiple Forms</i> — You may include up to 3 copies of 1 [[ATTACK]] event from each aspect other than your chosen aspect.\n'
             '<i>Meditate</i> — <b>Response</b>: After you change to this form, shuffle a card from State of Flow into your deck.',
     "custom": K},
    {"card_id": "shc002", "type": "Support", "name": "State of Flow", "subtitle": "",
     "desc": {"Permanent": "1", "Setup": "1", "Class": "Hero"},
     "traits": [], "set_name": SET,
     "text": 'Permanent. Setup.\n'
             '<b>Forced Response</b>: After you play an [[ATTACK]] event, place it faceup on top here, forming a pile. After the player deck runs out, shuffle each card placed here back into the player deck.\n'
             '<i>Keyword</i> - <b>Flow</b>: Look at the top card here. If a printed resource on that card matches the resource required by the "<b>Flow</b>" ability, you may also resolve its effects.',
     "custom": K},
    ev("shc003", "Throat Punch", 0, "RB", TP),
    ev("shc004", "Throat Punch", 0, "B", TP),
    ev("shc005", "Roundhouse Kick", 0, "Y", RK),
    ev("shc006", "Roundhouse Kick", 0, "RY", RK),
    ev("shc007", "Special Delivery", 2, "G", SD),
    ev("shc008", "Special Delivery", 2, "B", SD),
    ev("shc009", "Dragon Strike", 2, "G", DS),
    ev("shc010", "Dragon Strike", 2, "Y", DS),
    ev("shc011", "Chi Jabs", 1, "G", CJ),
    ev("shc012", "Chi Jabs", 1, "R", CJ),
    ev("shc013", "Augmented Blow", 1, "YB", AB),
    ev("shc014", "Augmented Blow", 1, "R", AB),
    {"card_id": "shc015", "type": "Upgrade", "name": "Stark Nunchaku", "subtitle": "",
     "desc": {"Cost": "3", "RES": "Y", "Class": "Hero", "Restricted": "1"},
     "traits": ["WEAPON"], "set_name": SET,
     "text": 'Restricted. Enters play with 3 charge counters on it.\n'
             '<b>Hero Action</b>: Exhaust Stark Nunchaku and remove 2 charge counters from it → stun an enemy.\n<i>Bzzt.</i>',
     "custom": K},
    {"card_id": "shc016", "type": "Upgrade", "name": "Metal Bracers", "subtitle": "",
     "desc": {"Cost": "3", "RES": "R", "Class": "Hero"},
     "traits": ["ARMOR"], "set_name": SET,
     "text": 'Shang-Chi gets +1 DEF. Enters play with 2 reflection counters on it.\n'
             '<b>Hero Action</b>: Exhaust Metal Bracers and remove 2 reflection counters from it → give Shang-Chi a tough status card.',
     "custom": K},
    {"card_id": "shc017", "type": "Upgrade", "name": "Martial Mastery", "subtitle": "",
     "desc": {"Cost": "2", "RES": "G", "Class": "Hero", "Uses": "3,chi"},
     "traits": ["SKILL"], "set_name": SET,
     "text": 'Uses (3 chi counters).\n'
             '<b>Hero Interrupt</b>: When you use one of your hero\'s basic powers <i>(THW, ATK, or DEF)</i>, exhaust Martial Mastery and remove 1 chi counter from it → your hero gets +1 to that power for this use.',
     "custom": K},
    {"card_id": "shc018", "type": "Obligation", "name": "Family Ties", "subtitle": "",
     "desc": {"Boost": "2", "GiveTo": "Shang-Chi"},
     "traits": [], "set_name": SET,
     "text": '<b><i>Give to the Shang-Chi player.</i></b>\nYou may flip to alter-ego form. Choose:\n'
             '• Deal 2 damage to Shang-Chi → remove Family Ties from the game.\n'
             '• Deal 2 damage to each ally. Discard this obligation.',
     "custom": K},
    {"card_id": "shc019", "type": "Minion", "name": "* Zheng Zu", "subtitle": "",
     "desc": {"HP": "6", "SCH": "2", "ATK": "1*", "Boost": "2", "Nemesis": "Shang-Chi"},
     "traits": ["ELITE", "MYSTIC"], "set_name": NEM,
     "text": '<b>Forced Response</b>: After Zheng Zu schemes, place 1 mystic counter here.\n'
             '[star] Zheng Zu gets +1 ATK for each mystic counter here.\n<i>(Shang-Chi\'s nemesis minion.)</i>\n'
             '<i>"Save your pity for yourself...you\'ll get none from me."</i>',
     "custom": K},
    {"card_id": "shc020", "type": "SideScheme", "name": "The Life Stealer", "subtitle": "",
     "desc": {"StartingThreat": "0", "Victory": "1"},
     "traits": [], "set_name": NEM,
     "text": 'Victory 1.\n'
             '<b>Forced Response</b>: After resolving step one of the villain phase, place 1 mystic counter here. After a third mystic counter is placed here, deal 3 indirect damage to each hero and ally in play and remove The Life Stealer from the game.\n'
             '<i>Zheng Zu is casting a ritual to restore himself to full power. Don\'t let it happen!</i>',
     "custom": K},
    {"card_id": "shc021", "type": "Treachery", "name": "Downtown Attack", "subtitle": "",
     "desc": {"Boost": "1"},
     "traits": [], "set_name": NEM,
     "text": '<b>When Revealed</b>: Remove an ally or [[PERSONA]] card in play from the game. If no card was removed from the game this way, take 3 indirect damage or discard 3 cards from your hand. Then, remove this card from the game.\n'
             '<i>"My father has always been a terrorist." —Shang-Chi</i>',
     "custom": K},
]
