"""Insere (ou REMPLACE) les 13 cartes de campagne de Galactic Storm (gs224-gs236 : 3 alliees
BASIC/CAMPAIGN + 10 alliees IDENTITY-SPECIFIC/CAMPAIGN) dans data/cards.json (cle `galactic_storm`)
puis recalcule les checksums. Recette : inserer_binary.py (meme pack).

IDEMPOTENT : une carte deja presente est remplacee a sa place (meme card_id), une carte absente
est ajoutee ; la liste du pack est triee par card_id.
Usage :  .venv-linux/bin/python3.10 .planning/galactic-storm/defs/inserer_campagne_alliees.py [racine_du_depot]
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
PYTHON = os.environ.get("PYTHON_DU_DEPOT", sys.executable)
PACK = "galactic_storm"
SET_NAME = "Galactic Storm Campaign"

CARDS = [
    {
        "card_id": "gs224", "type": "Ally", "name": "* Rick Jones", "subtitle": "",
        "desc": {"Cost": "0", "HP": "2", "THW": "1", "ATK": "2**", "RES": "B", "Class": "Campaign;Basic"},
        "traits": ["CIVILIAN"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Forced Interrupt</b>: When the villain attacks you, it attacks Rick Jones instead.\n<i>\"I guess I'll never be a super-hero.\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs225", "type": "Ally", "name": "* Gladiator", "subtitle": "KALLARK",
        "desc": {"Cost": "4", "HP": "4", "THW": "1*", "ATK": "3**", "RES": "G", "Class": "Campaign;Basic"},
        "traits": ["AERIAL"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Response</b>: After you play Gladiator from your hand, defeat a minion.\n<i>\"Gladiator claims victory!\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs226", "type": "Ally", "name": "* Lauri-Ell", "subtitle": "",
        "desc": {"Cost": "3", "HP": "5", "THW": "1*", "ATK": "2**", "RES": "R", "Toughness": "1", "Class": "Campaign;Basic"},
        "traits": ["KREE"], "set_name": SET_NAME,
        "text": "Honorary. Toughness.\n[star] <b>Response</b>: After Lauri-Ell attacks and damages an enemy, discard each boost card on that enemy.\n<i>\"I will make certain that everyone is safely evacuated off-world. Of that, you have my word.\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs227", "type": "Ally", "name": "* Binary", "subtitle": "CAROL DANVERS",
        "desc": {"Cost": "3", "HP": "3", "THW": "2", "ATK": "0*", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["AERIAL"], "set_name": SET_NAME,
        "text": "Honorary.\nX is the number of [energy] resource in your hand.\n<i>\"To save a star, someone with the power of a star is needed and that someone is me.\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs228", "type": "Ally", "name": "* Captain Marvel", "subtitle": "MONICA RAMBEAU",
        "desc": {"Cost": "3", "HP": "3", "THW": "2", "ATK": "2", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["AERIAL"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Resource</b>: Discard Captain Marvel → generate [energy][energy] resources.\n<i>\"You have like fifteen alternate code names, anyway, Monica-Photon-Pulsar-Captain-Marvel-Rambeau!\"</i> —Carol Danvers",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs229", "type": "Ally", "name": "* Crystal", "subtitle": "CRYSTALIA AMAQUELIN",
        "desc": {"Cost": "3", "HP": "4", "THW": "2", "ATK": "2", "RES": "G", "Requirement": "YBR", "Class": "Campaign;IdentitySpecific"},
        "traits": ["INHUMAN"], "set_name": SET_NAME,
        "text": "Honorary. Requirement ([energy][mental][physical]).\n<b>When Defeated</b>: Spend 3 resources of any type → put Crystal into play under your control.\n<i>\"Elements are what I do.\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs230", "type": "Ally", "name": "* Doctor Pym", "subtitle": "HANK PYM",
        "desc": {"Cost": "2", "HP": "2", "THW": "1*", "ATK": "1*", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["GENIUS", "SCIENTIST"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Alter-Ego Action</b>: Exhaust Doctor Pym → your identity gets +1 to each of its basic powers until the end of the round.\n<i>\"I know what I did wrong now. I know what I have to do.\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs231", "type": "Ally", "name": "* Goliath", "subtitle": "CLINT BARTON",
        "desc": {"Cost": "4", "HP": "4", "THW": "1", "ATK": "2", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["GIANT"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Response</b>: After Goliath uses a basic power, discard the top card of your deck. If a [physical] resource was discarded this way, deal 1 damage to each enemy.",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs232", "type": "Ally", "name": "* Her", "subtitle": "",
        "desc": {"Cost": "3", "HP": "3", "THW": "2", "ATK": "2", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["AERIAL"], "set_name": SET_NAME,
        "text": "Honorary.\n[star] <b>Response</b>: After Her enters play, ready an upgrade you control.\n<i>\"For the great resourcefulness you have demonstrated in our interactions, you have earned yourself the privilege...of being one of my mates!\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs233", "type": "Ally", "name": "* Living Lightning", "subtitle": "MIGUEL SANTOS",
        "desc": {"Cost": "2", "HP": "2", "THW": "2", "ATK": "2", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["AERIAL"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Response</b>: After Living Lightning leaves play, discard the top 2 cards of your deck. For each printed [energy] resource discarded this way, ready a card you control.",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs234", "type": "Ally", "name": "* Sersi", "subtitle": "",
        "desc": {"Cost": "2", "HP": "3", "THW": "1", "ATK": "1", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["ETERNAL"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Action</b>: Exhaust Sersi, deal 1 damage to her, and spend a [mental] resource → choose a status card in play. Replace that status card with a different status card.",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs235", "type": "Ally", "name": "* Spider-Woman", "subtitle": "JULIA CARPENTER",
        "desc": {"Cost": "3", "HP": "3", "THW": "2", "ATK": "1", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": [], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Response</b>: After Spider-Woman is discarded from the top of your deck, stun up to 2 enemies.\n<i>\"I'll buy you some time with my psi-webs!\"</i>",
        "custom": "Kajislav",
    },
    {
        "card_id": "gs236", "type": "Ally", "name": "* Thor", "subtitle": "ERIC MASTERSON",
        "desc": {"Cost": "4", "HP": "3", "THW": "1*", "ATK": "3*", "RES": "G", "Class": "Campaign;IdentitySpecific"},
        "traits": ["ASGARD"], "set_name": SET_NAME,
        "text": "Honorary.\n<b>Response</b>: After you play Thor from your hand, deal 1 damage to each minion engaged with you for each [energy] resource you used to pay for him.\n<i>\"It's time for some serious butt pounding!\"</i>",
        "custom": "Kajislav",
    },
]


def avant_checksum(d: dict, cle: str, valeur) -> dict:
    out = {}
    for k, v in d.items():
        if k == "checksum":
            out[cle] = valeur
        out[k] = v
    if cle not in out:
        out[cle] = valeur
    return out


chemin_cartes = os.path.join(MOTEUR, "data", "cards.json")
cartes = json.load(open(chemin_cartes, encoding="utf-8"))
if PACK not in cartes:
    cartes = avant_checksum(cartes, PACK, [])
liste = cartes[PACK]
index = {c.get("card_id"): i for i, c in enumerate(liste) if isinstance(c, dict)}
ajoutees = remplacees = 0
for carte in CARDS:
    if carte["card_id"] in index:
        liste[index[carte["card_id"]]] = carte
        remplacees += 1
    else:
        liste.append(carte)
        index[carte["card_id"]] = len(liste) - 1
        ajoutees += 1
liste.sort(key=lambda c: c.get("card_id", ""))
with open(chemin_cartes, "w", encoding="utf-8") as f:
    json.dump(cartes, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json"], cwd=MOTEUR, env=env, check=True)
print(f"Alliees de campagne : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
