# Entrees cards.json du scenario Super-Skrull (sk117-135) et du set modulaire Kree-Skrull War (sk136-140).
# Textes = transcriptions/super-skrull.md et modular-sets.md, RELUS contre les images (15/10/2026).
# card_id = sk + numero IMPRIME en pied de carte (« MC Custom Content By Kajislav <n> »).
# Corrections de lecture par rapport a la transcription (images) :
#  - Lord Kl'rt (sk127) : l'icone au centre de la boite de texte est l'AMPLIFICATION (croix + avion,
#    convention NOTES.md), pas une « icone de heros » : desc Amplify 1.
#  - Rock Mimicry (sk125) : badge ATK a etoile seule = marqueur sans valeur (decision utilisateur du
#    15/10/2026) : aucune cle ATK+.
SS = "Super-Skrull"; KW = "Kree-Skrull War"
SP = "[[SUPERPOWER]]"
def c(cid, typ, name, desc, traits, text, set_name):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}

VILLAIN_TEXT = ("<b>Forced Response</b>: After resolving step two of the villain phase, shuffle each " + SP +
                " attachment from play into the " + SP + " deck and reveal the top %s of the " + SP + " deck.")
V = [
 c("sk117", "Villain", "* Super-Skrull", {"HP": "14*", "ATK": "2", "SCH": "1", "Stage": "1"}, ["SKRULL"], VILLAIN_TEXT % "card", SS),
 c("sk118", "Villain", "* Super-Skrull", {"HP": "16*", "ATK": "2", "SCH": "1", "Stage": "2"}, ["SKRULL"], VILLAIN_TEXT % "2 cards", SS),
 c("sk119", "Villain", "* Super-Skrull", {"HP": "19*", "ATK": "2", "SCH": "2", "Stage": "3"}, ["SKRULL"], VILLAIN_TEXT % "2 cards", SS),
]
MS = [
 c("sk120a", "MainScheme", "Searching for the Heir", {"Stage": "1"}, [],
   "<b>Contents</b>: Super-Skrull I and Super-Skrull II <i>(Super-Skrull III for expert mode)</i>. Super-Skrull and Standard encounter sets. Two modular encounter sets <i>(Army of Skrulls and Kree-Skrull War)</i>.\n"
   "<b>Setup</b>: Shuffle each " + SP + " attachment into the " + SP + " deck and set it next to the encounter deck.", SS),
 c("sk120b", "MainScheme", "Searching for the Heir", {"Stage": "1", "TargetThreat": "6*", "EscalationThreat": "1*", "StartingThreat": "0"}, [],
   "<i>Learning that Princess Anelle had a child with his old foe, the original Captain Marvel, and that the Skrull Empire was seeking out this heir, named Dorrek VIII, the Super-Skrull made it his mission to be the first to find the boy, hidden on planet Earth.</i>\n"
   "<b>When Revealed</b>: Reveal the top card of the " + SP + " deck.", SS),
 c("sk121a", "MainScheme", "Heir to the Throne", {"Stage": "2"}, [],
   "<i>The Super-Skrull broadcasted to all Skrull worlds that he had located Dorrek VIII, who turned out to be Hulkling, a member of the recently formed Young Avengers team.</i>\n"
   "<b>When Revealed</b>: If Lord Kl'rt is in play, deal each player a facedown encounter card. Otherwise, search the encounter deck and discard pile for Lord Kl'rt and attach it to Super-Skrull. Shuffle the encounter deck.", SS),
 c("sk121b", "MainScheme", "Heir to the Throne", {"Stage": "2", "TargetThreat": "12*", "EscalationThreat": "2*", "StartingThreat": "2*"}, [],
   "<i>Kl'rt, the Super-Skrull, revealed Hulkling the truth about his past. He insisted that he must return to his people so that they could reunite the Skrull Empire.</i>\n"
   "<b>When Revealed</b>: Reveal the top card of the " + SP + " deck.\n<b>If this stage is completed, the players lose the game.</b>", SS),
]
ATTACH = "Attach to Super-Skrull.\n"
PW = [
 c("sk122", "Attachment", "Flexibility", {"SCH+": "1"}, ["SUPERPOWER"],
   ATTACH + "Super-Skrull gains stalwart and his attacks gain ranged.", SS),
 c("sk123", "Attachment", "Invisibility", {"SCH+": "1"}, ["SUPERPOWER"],
   ATTACH + "As an additional cost to attack Super-Skrull, you must spend 1 resource of any type.", SS),
 c("sk124", "Attachment", "Pyrokinesis", {"ATK+": "1"}, ["SUPERPOWER"],
   ATTACH + "<b>Forced Response</b>: After a friendly character thwarts the main scheme, deal 1 damage to it.\n[star] Super-Skrull's attacks gain piercing.", SS),
 c("sk125", "Attachment", "Rock Mimicry", {}, ["SUPERPOWER"],
   ATTACH + "[star] <b>Forced Interrupt</b>: When Super-Skrull attacks, give him 1 additional boost card for this activation.\n[star] Super-Skrull's attacks gain overkill.", SS),
]
ENC = [
 c("sk126", "Attachment", "Invisible Forcefield", {}, [],
   "Attach to the enemy with the highest printed hit points and without another Invisible Forcefield attached. If you cannot, this card gains surge.\n"
   "<b>Forced Interrupt</b>: When any amount of damage would be dealt to attached character, place it here instead. Then, if there is at least 5 damage here, discard this card.", SS),
 c("sk127", "Attachment", "Lord Kl'rt", {"Amplify": "1"}, ["TITLE"],
   ATTACH + "<b>Hero Action</b>: Reveal the top card of the " + SP + " deck → discard this card.\n<hr />\n[star] <b>Boost</b>: Reveal this card.", SS),
 c("sk128", "Minion", "* Mt'nox", {"HP": "4", "SCH": "2", "ATK": "2*", "Boost": "1"}, ["ELITE", "MYSTIC", "SKRULL"],
   "[star] <b>Forced Response</b>: After Mt'nox makes an undefended attack against you, discard the top card of your deck. If that card's printed resource has:\n"
   "[physical] - Give the villain a tough status card.\n[energy] - You are stunned.\n[mental] - You are confused.\n[wild] - All of the above.", SS),
 c("sk129", "Minion", "* Praxagora", {"HP": "5", "SCH": "1", "ATK": "3*", "Boost": "1"}, ["ELITE", "ROBOT"],
   "[star] Praxagora's attacks gain overkill.", SS),
 c("sk130", "Minion", "* R'kin", {"HP": "2", "SCH": "2", "ATK": "1", "Boost": "2"}, ["GENIUS", "SKRULL"],
   "<b>When Defeated</b>: Discard cards from the top of the encounter deck until an attachment is discarded. Reveal that card.", SS),
 c("sk131", "SideScheme", "Galactic Council Membership", {"StartingThreat": "3*"}, [],
   "<i>The Galactic Council is an intergalactic organization which was created to deal with important matters in the universe. Represented are the races of eight galaxies and other dimensions.</i>\n"
   "<b>Forced Response</b>: After a player attacks Super-Skrull, place 1 threat on the main scheme.", SS),
 c("sk132", "SideScheme", "Skrull Warlords", {"StartingThreat": "2*", "Boost": "3"}, [],
   "<i>The Super-Skrull became one of many Warlords seeking to re-unite the divided Skrull territories. He became one of the six most powerful Warlords who united themselves against this common foe.</i>\n"
   "<b>Forced Response</b>: After a card enters play under any player's control, give the villain a facedown boost card.", SS),
 c("sk133", "Treachery", "Hypnotic Gaze", {"Boost": "1"}, [],
   "<b>When Revealed</b>: Discard the top 2 cards of your deck. For each [physical] resource discarded this way stun a character you control, for each [mental] resource discarded this way confuse a character you control.", SS),
 c("sk134", "Treachery", "Power Multiplying", {}, [],
   "<b>When Revealed</b>: Reveal the top card of the " + SP + " deck. If you cannot, this card gains surge.\n<hr />\n"
   "[star] <b>Boost</b>: This card gets +1 boost icon ([boost]) for each " + SP + " attachment attached to Super-Skrull.", SS),
 c("sk135", "Treachery", "Villain's Versatility", {"Boost": "2"}, [],
   "<b>When Revealed</b>: If Super-Skrull has the following " + SP + " attachment attached:\n"
   "• Pyrokinesis - Take 3 indirect damage.\n• Rock Mimicry - Give Super-Skrull a tough status card.\n"
   "• Flexibility - Discard 1 card from your hand.\n• Invisibility - Place 2 threat on the main scheme.", SS),
]
KREE = [
 c("sk136", "Minion", "* Bel-Dann", {"HP": "4", "SCH": "1", "ATK": "3", "Boost": "2"}, ["ELITE", "KREE"],
   "<b>When Revealed</b>: Search the encounter deck and discard pile for Raksor and put him into play engaged with you.", KW),
 c("sk137", "Minion", "* Raksor", {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"}, ["ELITE", "SKRULL"],
   "<b>When Revealed</b>: Search the encounter deck and discard pile for Bel-Dann and put him into play engaged with you.", KW),
 c("sk138", "SideScheme", "Earth Involvement", {"StartingThreat": "1*", "Permanent": "1", "Setup": "1"}, [],
   "<i>Both the Kree and Skrulls are involving Earth in their plans in this intergalactic war.</i>\n"
   "Permanent. Setup.\nWhile there is at least 1 threat here, this card gains a crisis icon ([crisis]).\n"
   "<b>Forced Response</b>: After a card that belongs to the Kree-Skrull War encounter set is revealed, place 2 threat here.", KW),
 c("sk139", "Treachery", "Imperial Kree Army", {"Boost": "1"}, [],
   "<b>When Revealed</b>: Discard the top card of the encounter deck. Deal 1 damage to each character you control for each boost icon ([boost]) discarded this way.\n<hr />\n"
   "[star] <b>Boost</b>: Place 2 threat on Earth Involvement.", KW),
 c("sk140", "Treachery", "Skrull Imperial Fleet", {"Boost": "1"}, [],
   "<b>When Revealed</b>: Discard the top card of the encounter deck. Place 1 threat on each scheme in play for each boost icon ([boost]) discarded this way.\n<hr />\n"
   "[star] <b>Boost</b>: Place 2 threat on Earth Involvement.", KW),
]
CARDS = V + MS + PW + ENC + KREE
