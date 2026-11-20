# -*- coding: utf-8 -*-
"""Importe les cartes de CAMPAGNE et d'aspect de la campagne « Hellfire Hunt » (Dipsome), prefixe `hf`, pack `hellfire_hunt`.

Source : zip `Hellfire Hunt Campaign-20261025T195712Z-1-001.zip`, dossiers `Hero/Aspect Cards/` (013-027), `Campaign Card/allies/` (16),
`Campaign Card/ally side scheme/` (12 Potential Ally), `Campaign Card/Campaign/` (7 manigances de campagne + `xav`).
Transcription et choix de numerotation : docs/packs/hellfire-hunt/TRANSCRIPTIONS.md.

Numerotation (hf001-hf099 reserves aux fondations de campagne ; les scenarios prennent hf100+) :
  hf001-hf009  cartes d'aspect de Marvel Girl (Leadership / Basic) absentes du jeu ;
  hf010-hf012  Energy / Genius / Strength (reskins de ressources, « Max 1 per deck ») ;
  hf013-hf028  les 16 allies RECRUITED (numeros imprimes 200-214, Oya partage le 206 avec Mirage) ;
  hf029-hf040  les 12 manigances annexes POTENTIAL ALLY (188-199) ;
  hf041-hf047  les 7 manigances annexes de campagne (180-186) ;
  hf048        l'environnement Xavier's Institute (187).
X-Gene, X-Mansion et Mutant Education du zip ont EXACTEMENT le texte des officielles 38019, 32049, 37021 : copies par titre, donc pas
portees (le deck de depart prend les officielles).

Ce script ECRIT la liste `hellfire_hunt` de `data/cards.json` (idempotent : il remplace la liste du pack). Il prend
`flock /tmp/cards_json.lock`. Recalculer le checksum APRES : tools/recalculer_checksums.py.

Usage : python3 tools/importer_cartes_hellfire_hunt.py [--ecrire]
"""
import fcntl
import io
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTES = os.path.join(RACINE, "data", "cards.json")
PACK = "hellfire_hunt"
SET = "Hellfire Hunt"
AUTEUR = "Dipsome"
VERROU = "/tmp/cards_json.lock"
CLASSE_CAMPAGNE = "Campaign;Basic"


def _carte(cid, type_, nom, sous_titre, desc, traits, texte):
    return {"card_id": cid, "type": type_, "name": nom, "subtitle": sous_titre, "desc": desc,
            "traits": traits, "set_name": SET, "text": texte, "custom": AUTEUR}


def _allie(cid, nom, sous_titre, cout, pv, atq, ctr, res, classe, traits, texte, **extra):
    desc = {"Cost": cout, "HP": pv, "ATK": atq, "THW": ctr, "RES": res, "Class": classe}
    desc.update(extra)
    return _carte(cid, "Ally", nom, sous_titre, desc, traits, texte)


def _recrute(cid, nom, sous_titre, cout, pv, atq, ctr, res, texte, **extra):
    """Un allie RECRUITED de campagne (classe imprimee « Basic / Campaign »)."""
    return _allie(cid, nom, sous_titre, cout, pv, atq, ctr, res, CLASSE_CAMPAGNE, ["MUTANT", "RECRUITED"], texte, **extra)


def _pa(cid, nom, boost, menace, texte, **extra):
    """Une manigance annexe POTENTIAL ALLY de la campagne."""
    desc = {"Boost": boost, "StartingThreat": menace, "Victory": "1"}
    desc.update(extra)
    return _carte(cid, "SideScheme", nom, "", desc, ["POTENTIAL ALLY"], texte)


def _sa(allie):
    return (f"<b>When Defeated</b>: The player who defeat this scheme searches {allie} from the set-aside area, "
            f"put it into play under the player's control.")


CARTES_HF = [
    # ----------------------------------------------------------------------------- aspect de Marvel Girl (13-27)
    _allie("hf001", "* Boom Boom", "Tabitha Smith", "4", "2", "1*", "1*", "R", "Leadership", ["X-FORCE"],
           "<b>Response</b>: After your turn begins, place 1 boom counter to Boom Boom (to a maximum of 5). Then, you may discard Boom Boom "
           "to deal 2 damage to the villain for each boom counter"),
    _allie("hf002", "* Captain Britain", "Brian Braddock", "5", "4", "2**", "2**", "G", "Leadership", ["AERIAL", "EXCALIBUR"],
           "<b>Response</b>: After your turn begins, search the top 5 cards of your deck for an ally card and add it to your hand. "
           "Shuffle your deck.\n<i>\"Together, we will guard the gates of reality...how father intended.\"</i>"),
    _carte("hf003", "Support", "* PAC-RAT II", "", {"Cost": "1", "RES": "Y", "Class": "Leadership"}, ["VEHICLE", "X-FORCE"],
           "<b>Response</b>: After your turn begins, place 1 time counter on PAC-RAT II.\n"
           "<b>Action</b>: Put up to two [[X-FORCE]] allies from your hand into play with total printed cost equal to or less than the number "
           "of time counters on PAC-RAT II. Then, discard PAC-RAT II."),
    _carte("hf004", "Event", "Divided We Fall", "", {"Cost": "2", "RES": "R", "Class": "Leadership"}, [],
           "<b>Hero Action</b>: Heal 1 damage from up to 2 friendly characters, If this is the first card you have played this round, "
           "give those characters a tough status card."),
    _carte("hf005", "Event", "First Command", "", {"Cost": "1", "RES": "R", "Class": "Leadership"}, [],
           "Play only during your turn. You cannot play this card if you have played another card this turn.\n"
           "<b>Hero Action</b>: Ready an ally. That ally gets +1 THW and +1 ATK this phrase."),
    _allie("hf006", "* White Phoenix", "Hope Summers", "4", "3", "3*", "1*", "R", "Basic", ["PSIONIC", "X-FORCE"],
           "White Phoenix gains each [[TRAIT]] on your identity.\n"
           "<b>Interrupt</b>: When White Phoenix leaves play, search your discard pile for an event card and add it to your hand."),
    _carte("hf007", "Upgrade", "Jump-Start", "", {"Cost": "3", "RES": "Y", "MaxPerUnit": "1", "Class": "Basic"}, ["SUPERPOWER"],
           "Attach to a friendly character. Max 1 per character.\n"
           "<b>Response</b>: After your turn begins, deal 1 damage to attached character → place 1 power counter here.\n"
           "<b>Interrupt</b>: When attached character makes a basic thwart or basic attack action, remove 1 power counter from here → "
           "that character gets +1 THW and +1 ATK for that action."),
    _carte("hf008", "Support", "Psionic Soulmates", "",
           {"Cost": "2", "RES": "R", "MaxPerDeck": "1", "Class": "Basic"}, [],
           "Team-Up (Betsy Braddock and Rachel Summers). Max 1 per deck.\n"
           "<b>Response</b>: After you play a [[PSIONIC]] card, shuffle that card into your deck and exhaust this card → draw 1 card."),
    _carte("hf009", "Resource", "From The Ashes", "", {"RES": "G", "MaxPerDeck": "2", "Class": "Basic"}, [],
           "Max 2 per deck.\nThis card doubles the number of resources it generates while paying for the first card you play in your turn."),
    _carte("hf010", "Resource", "Energy", "", {"RES": "YY", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),
    _carte("hf011", "Resource", "Genius", "", {"RES": "BB", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),
    _carte("hf012", "Resource", "Strength", "", {"RES": "RR", "MaxPerDeck": "1", "Class": "Basic"}, [], "Max 1 per deck."),
    # ----------------------------------------------------------------------------- les 16 allies RECRUITED (200-214)
    _recrute("hf013", "* Armor", "Hisako Ichiki", "3", "5", "1*", "1*", "G",
             "<b>Response</b>: After Armor defends against an emeny attack, deal 1 damage to her → give her a tough status card.\n"
             "<i>\"Tell you what: You go one day without stabbing me, you get to choose my name.\"</i>"),
    _recrute("hf014", "* Blink", "Clarice Ferguson", "3", "2", "1*", "1*", "R",
             "Any of the players may play Blink from Recruited Mutant discard pile during their own turn (paying it's resource cost).\n"
             "<b>Forced Response</b>: When Blink is defeated, shuffle her into Recruited Mutant deck."),
    _recrute("hf015", "* Dazzler", "Alison Blaire", "2", "2", "1*", "1*", "Y",
             "<b>Response</b>: After Dazzler enters play, confuse up to 2 minions.\n"
             "<i>\"This city is a symphony. And I'm her speaker.\"</i>"),
    _recrute("hf016", "* ForgetMeNot", "Xabi", "4", "4", "4***", "4***", "G",
             "<b>Forced Response</b>: At the end of the round, if ForgetMeNot is still in play, discard him.\n"
             "<i>\"It's better to do something that matters and not be noticed than the other way around.\"</i>"),
    _recrute("hf017", "* Marrow", "Sarah Rushman", "1", "2", "1*", "1*", "R",
             "<b>Response</b>: After Marrow attacks an enemy, spend a [physical] resource → stun that enemy.\n"
             "<i>\"Oooh, Oooh, QUESTION! Who do we go creatively murder first? Also: Dibs on the hit.\"</i>"),
    _recrute("hf018", "* Glob Herman", "Robert Herman", "0", "2", "1*", "1*", "B",
             "Toughness.\n<i>\"Hey, nice chatting with you! Let's hang again sometime.\"</i>", Toughness="1"),
    _recrute("hf019", "* Mirage", "Danielle Moonstar", "2", "3", "2*", "1*", "B",
             "[star] Mirage's basic attack gains ranged.\n<i>\"I am Cheyenne -- and today is a good day to die!\"</i>"),
    _recrute("hf020", "* Oya", "Idie Okonkwo", "4", "2", "2*", "1*", "Y",
             "<b>Response</b>: After Oya enters play, choose one: deal 4 damage to an enemy, or stun an enemy.\n"
             "<i>\"Tell you what: You go one day without stabbing me, you get to choose my name.\"</i>"),
    _recrute("hf021", "* Polaris", "Lorna Dane", "2", "2", "2*", "2*", "Y",
             "<b>Action</b>: Spend a [energy] resource → heal 2 damage from Polaris.\n<i>\"I am a big gun. Or have you forgotten?\"</i>"),
    _recrute("hf022", "* Sage", "Tessa", "1", "3", "1*", "1*", "G",
             "[star] <b>Response</b>: After Sage thwarts, discard the top card of the encounter deck. Stun a minion if that card has a star "
             "icon ([star]) in the boost area.\n<i>\"I want children to be safe. Because then the future will be defined by hope.\"</i>"),
    _recrute("hf023", "* Wiz-Kid", "Takeshi Matsuya", "2", "3", "1*", "1*", "B",
             "Wiz-Kid gets +1 THW for each side scheme in play.\n"
             "<i>\"I'm a mutant...Like Artie and Leech! I can make my chair take me anywhere!\"</i>"),
    _recrute("hf024", "* Wolfsbane", "Rahne Sinclair", "1", "2", "1*", "1*", "R",
             "[star] <b>Response</b>: After Wolfsbane enters play, she gets +2 ATK until the end of the round.\n<i>\"We got you.\"</i>"),
    _recrute("hf025", "* Emma Frost", "", "4", "3", "1*", "2*", "R",
             "Armored 1.\n<b>Response</b>: After Emma Frost defends against an attack, discard 1 card from your deck, you may play it if it "
             "is an event, ignoring it's resource cost."),
    _recrute("hf026", "* Charles Xavier", "", "3", "2", "0*", "3*", "G",
             "<b>Response</b>: After Charles Xavier enters play, choose one: draw 2 cards, stun an enemy, or ready your identity. "
             "At the end of the round, if Charles Xavier is still in play, discard him."),
    _recrute("hf027", "* Sebastian Shaw", "", "3", "6", "2**", "1*", "Y",
             "<b>Response</b>: After Sebastian Shaw is damaged, place an equal amount of energy counter here.\n"
             "[star] <b>Interrupt</b>: When Sebastian Shaw thwarts, remove each energy counter from him → for each counter discarded "
             "this way, he gets +1 THW for this thwart."),
    _allie("hf028", "* Selene", "Selene Gallio", "4", "2", "3*", "1*", "R", CLASSE_CAMPAGNE, ["MUTANT", "RECRUITED"],
           "[star] <b>Response</b>: After Selene attacks and defeats a minion, heal 2 damage from her."),
    # ----------------------------------------------------------------------------- les 12 POTENTIAL ALLY (188-199)
    _pa("hf029", "Shattered Confidence", "1", "3", _sa("Armor"), Amplify="1"),
    _pa("hf030", "Portal Trouble", "1", "4",
        "<b>Forced Response</b>: When the villain phase begins, each player discard 1 card from hand in random.\n" + _sa("Blink")),
    _pa("hf031", "Battle of the Bands", "1", "5", _sa("Dazzler"), Crisis="1"),
    _pa("hf032", "Secret Identity", "2", "3", "Victory 1. Surge.\n" + _sa("ForgetMeNot"), Surge="1"),
    _pa("hf033", "Morlock Rescue Mission", "1", "3",
        "<b>When Revealed</b>: Place 1 threat here for each ally in play.\n" + _sa("Marrow")),
    _pa("hf034", "Xavier's School Under Siege", "1", "3",
        "<b>When Revealed</b>: The first player searches the encounter deck and discard pile for a minion and puts it into play engaged "
        "with them.\n" + _sa("Glob Herman")),
    _pa("hf035", "Astral Plane Showdown", "2", "5", _sa("Mirage"), Acceleration="1"),
    _pa("hf036", "Crisis of Faith", "2", "3",
        "Threat cannot be removed from other side scheme in play from thwarting.\n" + _sa("Oya")),
    _pa("hf037", "Break The Prison", "1**", "10",
        "Victory 1. Assault.\n" + _sa("Polaris") + "\n[star] <b>Boost</b>: After this activation, reveal this card.", Assault="1"),
    _pa("hf038", "Covert Intelligence Operation", "3", "2", "Each minion gains incite 1.\n" + _sa("Sage")),
    _pa("hf039", "Tech Glitch", "1", "4", _sa("Wiz-Kid"), Hazard="1"),
    _pa("hf040", "Muir Island Crisis", "3", "5",
        "<b>Forced Response</b>: After the villain phase ends, deal 1 damage to each hero in player order.\n" + _sa("Wolfsbane")),
    # ----------------------------------------------------------------------------- manigances de campagne (180-186) + environnement (187)
    _carte("hf041", "SideScheme", "Cerebro Insights", "",
           {"Boost": "3", "StartingThreat": "2", "Hinder": "1*", "Victory": "1"}, [],
           "<i>The heroes discover traces of other mutants in Cerebro's recent logs. This information proves crucial in tracking down "
           "possible allies.</i>\nVictory 1. Hinder 1[per_hero].\n"
           "<b>Forced Response</b>: After White Queen flips, discard this side scheme.\n"
           "<b>When Defeated</b>: The player who defeats this side scheme searches the encounter deck and discard pile for a "
           "[[POTENTIAL ALLY]] side scheme and put it into play. They choose a [[POTENTIAL ALLY]] side scheme in play, then defeat it."),
    _carte("hf042", "SideScheme", "Emma Frost's Redemption", "",
           {"Boost": "3", "StartingThreat": "4*", "Victory": "1", "Amplify": "1"}, [],
           "<i>Emma Frost has begun questioning the Hellfire Club's methods, secretly observing the unfolding events.</i>\nVictory 1.\n"
           "<b>When Defeated</b>: The player who defeated this scheme searches the Emma Frost ally from the set-aside area and put it into play."),
    _carte("hf043", "SideScheme", "Cryptic Threatening Message", "",
           {"Boost": "3", "StartingThreat": "4*", "Victory": "1"}, [],
           "<i>A mysterious psychic message warns of danger within the X-Mansion itself. Is this a genuine attempt to help, or a ploy to "
           "sow discord among the heroes?</i>\nVictory 1.\n"
           "Treat the printed text box of each [[LOCATION]] support as if it were blank (except for [[TRAITS]]). The \"Action\" ability of "
           "Xavier's Institute environment cannot be triggered.\n"
           "<b>When Defeated</b>: The player who defeated this scheme searches the Charles Xavier ally from the set-aside area and put it into play."),
    _carte("hf044", "SideScheme", "Psychic Minefield", "",
           {"Boost": "3", "StartingThreat": "1", "Victory": "1", "Acceleration": "1"}, [],
           "<i>Emma Frost has erected powerful mental barriers. Breaking through these defenses is crucial to freeing Emma and uncovering "
           "Cassandra's true plans.</i>\nVictory 1.\nThreat cannot be removed from here while there is only 1 threat here.\n"
           "<b>When Defeated</b>: Deal 5[per_hero] damage to Emma Frost. Each player draws 1 card."),
    _carte("hf045", "SideScheme", "Rally the Survivors", "",
           {"Boost": "3", "StartingThreat": "5", "Victory": "1", "Hazard": "1"}, [],
           "<i>With Cassandra Nova's attack in full swing, you must protect surviving mutants while fending off the assault. Every ally "
           "could mean the difference between victory and extinction.</i>\nVictory 1. While this side scheme is in the victory display, "
           "each campaign ally gains +1 THW, +1 ATK, and +1 hit-point.\n"
           "<b>When Defeated</b>: The player who defeated this scheme takes a card from the Recruited Mutants deck and put it into play "
           "under their control. Then, if there still has card in the Recruited Mutants deck, place 5 threat here."),
    _carte("hf046", "SideScheme", "Tactical Help", "",
           {"Boost": "2**", "StartingThreat": "3", "Acceleration": "1"}, [],
           "<b>When Defeated</b>: The player who defeat this scheme searches Sebastian Shaw from the set-aside area, put it into play "
           "under the player's control. Remove this card from the campaign.\n"
           "[star] <b>Boost</b>: Reveal this card. Place 2 additional threat here."),
    _carte("hf047", "SideScheme", "Enemy Of Enemy", "",
           {"Boost": "1**", "StartingThreat": "5", "Crisis": "1"}, [],
           "<b>When Defeated</b>: The player who defeat this scheme searches Selene from the set-aside area, put it into play under "
           "the player's control. Remove this from the campaign.\n[star] <b>Boost</b>: Reveal this card. You are confused."),
    _carte("hf048", "Environment", "* Xavier's Institute", "", {}, [],
           "<b>Forced Response</b>: After a [[RECRUITED]] ally is discarded, place it into the Recruited Mutants discard pile instead.\n"
           "<b>Action</b>: Spend 1 resource of any type → draw 1 card from the Recruited Mutants deck. (Max once per phase per player.)"),
]


def verifier():
    ids = [c["card_id"] for c in CARTES_HF]
    assert len(ids) == len(set(ids)), "doublon d'identifiant"
    attendus = [f"hf{n:03d}" for n in range(1, 49)]
    assert ids == attendus, f"suite d'identifiants attendue hf001-hf048, obtenu {ids}"
    for c in CARTES_HF:
        for cle in ("card_id", "type", "name", "desc", "traits", "set_name", "text", "custom"):
            assert cle in c, (c["card_id"], cle)
        assert c["set_name"] == SET


def main():
    verifier()
    if "--ecrire" not in sys.argv:
        print(f"{len(CARTES_HF)} cartes valides (hf001-hf048). Ajouter --ecrire pour ecrire data/cards.json.")
        return 0
    with open(VERROU, "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        texte = io.open(CARTES, encoding="utf-8", newline="").read()
        donnees = json.loads(texte)
        avant = donnees.get(PACK)
        donnees[PACK] = CARTES_HF
        sortie = json.dumps(donnees, ensure_ascii=False, indent=1)
        tmp = CARTES + ".tmp-hf"
        io.open(tmp, "w", encoding="utf-8", newline="").write(sortie)
        os.replace(tmp, CARTES)
        print(f"data/cards.json : {PACK} {'remplace' if avant else 'cree'} ({len(CARTES_HF)} cartes). "
              f"Recalculer le checksum : tools/recalculer_checksums.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
