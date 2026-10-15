# Entrees cards.json du scenario 4 SKRULL PANTHEON (sk170-183) et du set modulaire DARD'VAN SECT (sk184-188).
# Texte = transcriptions/skrull-pantheon.md et transcriptions/modular-sets.md, RELU SUR LES SCANS (15/10/2026).
# card_id = sk + numero IMPRIME en pied de carte (« MC Custom Content By Kajislav <n>[A|B] »).
#
# Numerotation relue sur les images (pied de carte) :
#   170A/B Kly'bn / Sl'gur't (I)   171A/B (II)   172A/B (III)   173A/B Protect the Pantheon (1A/1B)
#   174A/B Slaying the False Gods (2A/2B)   175A/B Skrull Pantheon (Stronghold / Destroyed)
#   176 Blessed by Kly'bn   177 Blessed by Sl'gur't   178 Nogor   179 Shapeless Wastes   180 Strengthen the Faith
#   181 Prayer to Kly'bn   182 Prayer to Sl'gur't   183 Talisman of the Skrulls
#   184 Dard'van Fanatic   185 Dard'van Priest   186 Dard'van Sect   187 Collective Prayers   188 Sectarian Practices
# Le meme numero imprime porte les DEUX faces d'une carte double face (A / B) : card_id `sk170a` / `sk170b`.
#
# Lectures faites en relisant les scans (voir defs/pantheon_questions.md) :
#  - Les mechants Kly'bn / Sl'gur't sont UNE carte double face (insert p.14) : sk170a = face Kly'bn, sk170b = face
#    Sl'gur't (idem 171, 172). PV partages (meme compteur de degats : c'est la meme carte).
#  - sk186 Dard'van Sect : l'icone noire « boite avec un plus » est l'icone HAZARD (carte penchee, croix evidee, rien
#    dessous : meme glyphe `H` de ChampionsIcons.ttf, tourne de 90 degres sur une carte paysage). La transcription disait
#    « black box-with-plus symbol » sans la nommer.
#  - Une etoile ★ a cote d'un chiffre (SCH / ATK / PV de Nogor) renvoie au texte ; on garde le chiffre imprime dans desc.
#    ★ a la place de l'ATK de Dard'van Priest : `ATK 0*` (convention de sk099 Intelligentsia / sk109 Skrull Telepath).
#  - Etoile rouge de boost = pas d'icone chiffree (aucune cle Boost) ; « Y » rose = 1 icone de boost.
SP = "Skrull Pantheon"
DS = "Dard'van Sect"


def c(cid, typ, name, desc, traits, text, set_name):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}


def dieu(nom, pronom, stade, sch, atk, pv, traitrises):
    """Une face de mechant : memes textes aux trois stades, sauf le stade III (carte d'etat Robuste)."""
    revele = f"<b>When Revealed</b>: Place 1 faith counter on {nom}" + (f" and give {pronom} a tough status card." if stade == 3 else ".")
    quoi = "treachery" if traitrises else "non-treachery"
    suite = (f"<b>Forced Response</b>: After resolving step one of the villain phase, discard the top card of the encounter "
             f"deck for each faith counter on {nom}. Deal the players each {quoi} card discarded this way as a facedown "
             f"encounter card in player order.")
    base = {1: 170, 2: 171, 3: 172}[stade]
    cid = f"sk{base}{'b' if traitrises else 'a'}"
    return c(cid, "Villain", "* " + nom, {"HP": f"{pv}*", "ATK": str(atk), "SCH": str(sch), "Stage": str(stade)},
             ["GOD", "SKRULL"], revele + "\n" + suite, SP)


# Stades : (SCH, ATK, PV par joueur) ; Kly'bn I/II/III puis Sl'gur't I/II/III.
KLYBN = {1: (2, 1, 15), 2: (3, 1, 18), 3: (3, 2, 20)}
SLGURT = {1: (1, 2, 15), 2: (1, 3, 18), 3: (2, 3, 20)}

CARDS = []
for stade in (1, 2, 3):
    CARDS.append(dieu("Kly'bn", "him", stade, KLYBN[stade][0], KLYBN[stade][1], KLYBN[stade][2], False))
    CARDS.append(dieu("Sl'gur't", "her", stade, SLGURT[stade][0], SLGURT[stade][1], SLGURT[stade][2], True))

CARDS += [
    # --- Complots principaux ------------------------------------------------------------------
    c("sk173a", "MainScheme", "Protect the Pantheon", {"Stage": "1"}, [],
      "<b>Contents</b>: Kly'bn I and Kly'bn II <i>(Kly'bn II and Kly'bn III instead for expert mode)</i>. Skrull Pantheon, "
      "Dard'van Sect and Standard encounter sets. One modular encounter set <i>(Skrull Society)</i>.\n"
      "<b>Setup</b>: Set the Skrull Pantheon environment aside, out of play.", SP),
    c("sk173b", "MainScheme", "Protect the Pantheon",
      {"Stage": "1", "TargetThreat": "9*", "EscalationThreat": "1*", "StartingThreat": "6*"}, [],
      "<b>Forced Interrupt</b>: When the last threat is removed from this scheme, put the set-aside Skrull Pantheon "
      "environment into play, <b><i>DESTROYED</i></b> side faceup. Advance to stage 2B.\n"
      "<b>When Completed</b>: Put the set-aside Skrull Pantheon environment into play, <b><i>STRONGHOLD</i></b> side faceup. "
      "Advance to stage 2A.", SP),
    c("sk174a", "MainScheme", "Slaying the False Gods", {"Stage": "2"}, [],
      "<i>Kly'bn, the Eternal Skrull, and Sl'gur't of the Infinite Names are presented as the emperor and the empress of "
      "the Skrull Pantheon.</i>\n<b>When Revealed</b>: Search the encounter deck and discard pile for Strengthen the Faith "
      "side scheme, reveal it and place 2[per_hero] additional threat on it.", SP),
    c("sk174b", "MainScheme", "Slaying the False Gods",
      {"Stage": "2", "TargetThreat": "12*", "EscalationThreat": "1*", "StartingThreat": "0"}, [],
      "<i>Kly'bn and Sl'gur't indirectly supported the creation and expansion of the Skrull Empire. They conquered and "
      "enslaved the pantheons of the conquered races, numbering nearly 1000 pantheons. Now the duo is after the gods of "
      "Earth.</i>\n<b>When Revealed</b>: Flip the villain.\n<b>If this stage is completed, the players lose the game.</b>", SP),
    # --- Environnement double face -------------------------------------------------------------
    c("sk175a", "Environment", "Skrull Pantheon", {}, ["STRONGHOLD"],
      "<b>Hero Action</b>: Spend 2 resources of the same type → remove 1 faith counter from the villain.\n"
      "<i>Kly'bn and Sl'gur't joined together and ascended to godhood becoming the leaders of the Skrull Pantheon.</i>", SP),
    c("sk175b", "Environment", "Skrull Pantheon", {}, ["DESTROYED"],
      "<b>Hero Action</b>: Spend 2 resources of any type → remove 1 faith counter from the villain.\n"
      "<i>Skrull Pantheon was successfully destroyed and the Skrull Deity became really angry.</i>", SP),
    # --- Rencontre : attachements ------------------------------------------------------------------
    c("sk176", "Attachment", "Blessed by Kly'bn", {"Boost": "1"}, ["CONDITION"],
      "Attach to the minion with the lowest SCH. If you cannot, this card gains surge.\n"
      "X is equal to the number of faith counters on the villain.\n<hr />\n"
      "[star] <b>Boost</b>: If this activation is a scheme, this card gets +2 boost icons ([boost][boost]) for this activation.", SP),
    c("sk177", "Attachment", "Blessed by Sl'gur't", {"Boost": "1"}, ["CONDITION"],
      "Attach to the minion with the lowest ATK. If you cannot, this card gains surge.\n"
      "X is equal to the number of faith counters on the villain.\n<hr />\n"
      "[star] <b>Boost</b>: If this activation is an attack, this card gets +2 boost icons ([boost][boost]) for this activation.", SP),
    # --- Rencontre : sbire, complots annexes, traitrises -----------------------------------------------
    c("sk178", "Minion", "* Nogor", {"HP": "4", "SCH": "1", "ATK": "1", "Boost": "2"}, ["ELITE", "SKRULL"],
      "[star] Nogor gets +1 SCH, +1 ATK and +1 hit point for each faith counter on the villain.\n"
      "<b>When Revealed</b>: Flip the villain.\n<hr />\n[star] <b>Boost</b>: Flip the villain.\n"
      "<i>\"I am the living harness of the power of the gods.\"</i>", SP),
    c("sk179", "SideScheme", "Shapeless Wastes", {"StartingThreat": "2", "Hinder": "2*", "Boost": "3"}, [],
      "<i>The Skrullian equivalent of Hell is known as the Shapeless Wastes.</i>\nHinder 2[per_hero].\n"
      "<b>Forced Response</b>: After an ally or a minion is defeated, if that character has the [[SKRULL]] trait, flip the "
      "villain. Otherwise, place 1 faith counter on the villain.", SP),
    c("sk180", "SideScheme", "Strengthen the Faith", {"StartingThreat": "2*", "Boost": "1"}, [],
      "<i>Most Skrulls worship Kly'bn, the Eternal Skrull, and Sl'gur't of the Infinite Names. They are the only true gods "
      "of the Skrull Empire.</i>\n<b>Forced Response</b>: After a [[SKRULL]] minion enters play, place 1 faith counter on the "
      "villain.\n<hr />\n[star] <b>Boost</b>: Place 1 faith counter on the villain.", SP),
    c("sk181", "Treachery", "Prayer to Kly'bn", {"Boost": "1"}, [],
      "<b>When Revealed</b>: If Kly'bn is in play, he activates against you. Otherwise, flip the villain.\n<hr />\n"
      "[star] <b>Boost</b>: If Kly'bn is not in play, flip the villain.\n"
      "<i>\"For I am Kly'bn. I am the Eternal Skrull. And I love you.\" —Kly'bn</i>", SP),
    c("sk182", "Treachery", "Prayer to Sl'gur't", {"Boost": "1"}, [],
      "<b>When Revealed</b>: If Sl'gur't is in play, she activates against you. Otherwise, flip the villain.\n<hr />\n"
      "[star] <b>Boost</b>: If Sl'gur't is not in play, flip the villain.\n"
      "<i>\"What do they call you? I pray you, tell us...\" —Sl'gur't</i>", SP),
    c("sk183", "Treachery", "Talisman of the Skrulls", {"Boost": "3"}, [],
      "<b>When Revealed</b>: Search the encounter deck and discard pile for Nogor and reveal him. If Nogor did not enter play "
      "this way, this card gains surge.\n"
      "<i>\"The Talisman is the representation of the gods, and his presence is required to ensure the gods' blessing on our "
      "endeavors\" —Jazinda</i>", SP),
    # --- DARD'VAN SECT -----------------------------------------------------------------------------
    c("sk184", "Minion", "Dard'van Fanatic", {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"}, ["SKRULL"],
      "<b>When Revealed</b>: Choose to either deal 1 damage to each character you control or place 1 threat on each scheme "
      "in play.\n<i>\"I belong to the Dard'van sect. It's considered extreme by some.\" —Grrix</i>", DS),
    c("sk185", "Minion", "Dard'van Priest", {"HP": "3", "SCH": "2", "ATK": "0*", "Boost": "2"}, ["MYSTIC", "SKRULL"],
      "<b>When Revealed</b>: Dard'van Priest schemes.\n[star] <b>Forced Interrupt</b>: When Dard'van Priest would attack, "
      "instead choose a card in play with a \"<b>When Revealed</b>\" ability and resolve that ability.\n<i>\"He loves you.\"</i>", DS),
    c("sk186", "SideScheme", "Dard'van Sect", {"StartingThreat": "2*", "Hazard": "1", "Boost": "3"}, [],
      "<i>A zealous sect of the Skrull Empire which follows prophecies foretelling that Earth will become the new home for "
      "the Skrull race.</i>\n<b>When Revealed</b>: Give the villain 1 facedown boost card.", DS),
    c("sk187", "Treachery", "Collective Prayers", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Discard the top card of the encounter deck for each character in play. Reveal each card "
      "discarded this way that belongs to the Dard'van Sect encounter set.\n"
      "<i>\"...the first one loves us all alike.\" —Grrix</i>", DS),
    c("sk188", "Treachery", "Sectarian Practices", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Choose a card in play with a \"<b>When Revealed</b>\" ability and resolve that ability. If you "
      "cannot, this card gains surge.\n"
      "<i>\"Trust. What do humans know of trust? You can't even agree on one god.\" —Nogor</i>", DS),
]

# Composition (copies incluses). Une seule entree cards.json par card_id.
ENCOUNTERS_PANTHEON = ["sk176", "sk176", "sk177", "sk177", "sk178", "sk179", "sk180", "sk180",
                       "sk181", "sk181", "sk181", "sk182", "sk182", "sk182", "sk183"]
ENCOUNTERS_DARDVAN = ["sk184", "sk184", "sk185", "sk186", "sk187", "sk188", "sk188", "sk188"]
