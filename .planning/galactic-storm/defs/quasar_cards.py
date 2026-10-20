# Entrees cards.json du heros QUASAR (Galactic Storm, Kajislav). Lot GS-2.
# Texte = docs/packs/galactic-storm/transcriptions/quasar.md, RELU contre chaque image le 20/10/2026
# (planche de decoupes des icones de ressource : scratchpad, voir le gabarit de chaque carte).
#
# Numerotation (decision de l'utilisateur du 20/10/2026, Q1) :
#  - les 16 cartes de heros portent toutes « 4 » imprime : card_id = gs + (300 + n) ou n vient du pied
#    « QUASAR (n/16) » ; Quantum Bubble (14/16) porte le numero imprime 49 : gs349 ;
#  - un card_id par carte DISTINCTE avec le nombre d'exemplaires (decision c) : la copie prend le
#    PREMIER n/16 (Flight of Light 3/16 et 4/16 -> gs303 x2 ; gs304, gs306, gs308, gs310, gs312 et gs314
#    restent libres) ;
#  - l'identite n'a pas de n/16 (pied « HAND SIZE ... ») : gs300a (Quasar) / gs300b (Wendell Vaughn),
#    choix technique sans effet en jeu ;
#  - obligation : numero imprime 65 -> gs065 (le 65 des reskins est un art alternatif, sans card_id) ;
#  - nemesis en collision avec Binary : suffixe q (gs237q, gs239q, gs240q) ; Maelstrom imprime 99, deja
#    pris par Hobgoblin (Imperial Guard) : gs099q en attendant la reponse a
#    .planning/todos/2026-10-20-gs2-questions.md (Q-GS2-1).
H = "Quasar"
N = "Quasar Nemesis"


def c(cid, typ, name, desc, traits, text, set_name=H, subtitle=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}


CARDS = [
 c("gs300a", "Hero", "* Quasar", {"HP": "11", "ATK": "2", "THW": "2", "DEF": "2", "HS": "5"}, ["GUARDIAN"],
   "<i>Channel the Bands</i> — <b>Action</b>: Exhaust Quasar → ready Quantum Bands."),
 c("gs300b", "AlterEgo", "* Wendell Vaughn", {"HP": "11", "REC": "3", "HS": "6"}, ["S.H.I.E.L.D"],
   "<i>Chosen as the Protector</i> — <b>Setup</b>: Put Quantum Bands into play."),
 c("gs301", "Upgrade", "* Quantum Bands", {"RES": "G", "Permanent": "1", "Class": "Hero"}, ["ITEM"],
   "Permanent.\nQuasar gains the [[AERIAL]] trait.\n<b>Hero Resource</b>: Exhaust Quantum Bands → generate a [wild] resource."),
 c("gs302", "Ally", "* Epoch", {"Cost": "4", "HP": "4", "THW": "1*", "ATK": "3***", "RES": "G", "Class": "Hero"},
   ["COSMIC ENTITY"],
   "[star] <b>Response</b>: After Epoch uses one of her basic powers, ready Quantum Bands."),
 c("gs303", "Event", "Flight of Light", {"Cost": "2", "RES": "R", "Class": "Hero"}, ["THWART"],
   "<b>Hero Action</b> <i>(thwart)</i>: Remove 3 threat from a scheme. If this removes the last threat from that scheme, remove 2 threat from a scheme."),
 c("gs305", "Event", "No Holding Back", {"Cost": "2", "RES": "R", "Class": "Hero"}, ["ATTACK", "THWART"],
   "<b>Hero Action</b> <i>(attack/thwart)</i>: Deal 3 damage to an enemy for each [physical] resource you used to pay for this card. Remove 2 threat from a scheme for each [mental] resource you used to pay for this card."),
 c("gs307", "Event", "Righteous Fury", {"Cost": "3", "RES": "Y", "Class": "Hero"}, ["ATTACK"],
   "<b>Hero Action</b> <i>(attack)</i>: Deal 6 damage to an enemy. If this attack defeats that enemy, ready Quasar."),
 c("gs309", "Event", "Unbreakable Guard", {"Cost": "1", "RES": "B", "Class": "Hero"}, ["DEFENSE"],
   "<b>Hero Interrupt</b> <i>(defense)</i>: When a friendly character would take any amount of damage, prevent all of that damage. If you paid for this card with Quantum Bands give that friendly character a tough status card."),
 c("gs311", "Resource", "Quantum Energy", {"RES": "G", "Class": "Hero"}, [],
   "<b>Response</b>: After you spend this card, ready Quantum Bands."),
 c("gs313", "Upgrade", "Quantum Absorption", {"Cost": "1", "RES": "G", "Class": "Hero"}, ["SUPERPOWER"],
   "<b>Hero Interrupt</b>: When you pay for a [[DEFENSE]] event with Quantum Bands, heal 2 damage from Quasar."),
 c("gs315", "Upgrade", "Quantum Jump", {"Cost": "2", "RES": "G", "Class": "Hero"}, ["SUPERPOWER"],
   "<b>Hero Interrupt</b>: When you pay for a [[THWART]] event with Quantum Bands, that thwart removes 2 additional threat and ignores the crisis icon ([crisis]) and the patrol keyword."),
 c("gs316", "Upgrade", "Quantum Weapon", {"Cost": "2", "RES": "G", "Class": "Hero"}, ["SUPERPOWER"],
   "<b>Hero Interrupt</b>: When you pay for an [[ATTACK]] event with Quantum Bands, that attack deals 1 additional damage and gains piercing and overkill."),
 c("gs349", "Upgrade", "Quantum Bubble", {"Cost": "2", "RES": "G", "Class": "Hero"}, ["SUPERPOWER"],
   "<b>Hero Response</b>: After you pay for an ally with Quantum Bands, give that ally a tough status card."),
 c("gs065", "Obligation", "Protector of the Universe", {"Boost": "2", "GiveTo": "Wendell Vaughn", "Uses": "3,duty"}, [],
   "<b><i>Give to the Wendell Vaughn player.</i></b>\nUses (3 duty counters).\nYou cannot flip to alter-ego form.\n<b>Hero Response</b>: After you defeat an enemy or a scheme, or defend against an attack and take no damage, remove 1 duty counter from here."),
 c("gs099q", "Minion", "* Maelstrom", {"HP": "5", "SCH": "1", "ATK": "2", "Boost": "2", "Nemesis": "Wendell Vaughn"},
   ["DEVIANT", "INHUMAN"],
   "<b>When Revealed</b>: Tuck Quantum Bands under Maelstrom.\n<b>Forced Response</b>: After Maelstrom leaves play, put Quantum Bands into play under the Quasar player's control.\n<i>(Quasar's nemesis minion.)</i>",
   set_name=N),
 c("gs239q", "SideScheme", "Entropy Ascendant", {"StartingThreat": "3", "Hinder": "1*", "Boost": "3"}, [],
   "Hinder 1 [per_player].\nEach event card gains requirement ([energy]).", set_name=N),
 c("gs237q", "Attachment", "Avatar of Oblivion", {"ATK+": "1"}, ["TITLE"],
   "Attach to the minion with the highest ATK. If you cannot, this card gains surge.\nAttached minion gains the [[ELITE]] trait.\n<b>Forced Interrupt</b>: When attached minion would be defeated, heal all damage from it instead, then discard this card.",
   set_name=N),
 c("gs240q", "Treachery", "Distant Manipulation", {"Boost": "1"}, [],
   "<b>When Revealed</b>: Choose to either exhaust each card with a \"<b>Resource</b>\" ability you control or discard each resource card from your hand. If you cannot, this card gains surge.",
   set_name=N),
]
