# Entrees cards.json du modulaire ACCUSER CORPS de Galactic Storm (gs156-gs160), lot GS-6 (20/10/2026).
# Texte = docs/packs/galactic-storm/transcriptions/modular-sets.md, RELU SUR LES SCANS le 20/10/2026.
ACCUSER = "Accuser Corps"


def c(cid, typ, name, desc, traits, text, subtitle=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": ACCUSER, "text": text, "custom": "Kajislav"}


CARDS = [
    c("gs156", "Attachment", "* The Accused", {"Boost": "1"}, ["CONDITION"],
      "Attach to your identity.\n<b>Forced Interrupt</b>: When an enemy initiates an attack against the "
      "attached identity, that enemy gets +1 ATK for that attack.\n<b>Forced Response</b>: After an "
      "ACCUSER CORPS enemy is defeated, discard this card.\n<hr />\n[star] <b>Boost</b>: Attach to your "
      "identity."),
    c("gs157", "Attachment", "Universal Weapon", {"SCH+": "1", "ATK+": "1"}, ["WEAPON"],
      "Attach to the villain.\nAttached character gains steady and the ACCUSER CORPS trait.\n<b>Hero "
      "Action</b>: Take 2 damage and deal yourself 1 facedown encounter card → shuffle this card into "
      "the encounter deck.\n<hr />\n[star] <b>Boost</b>: Attach to an enemy."),
    c("gs158", "Attachment", "Unwavering", {"ATK+": "3"}, ["CONDITION"],
      "Attach to an enemy.\n[star] <b>Forced Response</b>: After attached enemy attacks and damages a "
      "character, discard this card.\n[star] <b>Boost</b>: Attach to an enemy.\n<i>\"I have passed "
      "judgment, nothing more, nothing less. It is justice...that has been done.\" —Ronan</i>"),
    c("gs159", "Minion", "Kree Accuser", {"SCH": "1", "ATK": "2", "HP": "6", "Toughness": "1", "Villainous": "1"},
      ["ACCUSER CORPS", "KREE"],
      "Toughness. Villainous.\n<i>\"Will you need me to employ physical force?\" —Lauri-Ell</i>"),
    c("gs160", "Treachery", "Judgement Day", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Each ACCUSER CORPS enemy activates against you. If no enemy activated this "
      "way, search the encounter deck and discard pile for a Kree Accuser and reveal it.\n<i>\"Accusers... "
      "restrain the prisoners!\" —Ronan</i>"),
]

# Set modulaire complet : pas de random_pick (aucune regle « N cartes sur M » n'est imprimee pour Accuser
# Corps, contrairement a Imperial Guard, livret p.14).
ENCOUNTERS = ["gs156", "gs157", "gs158", "gs158", "gs159", "gs159", "gs160"]
SET_ASIDE: list = []
