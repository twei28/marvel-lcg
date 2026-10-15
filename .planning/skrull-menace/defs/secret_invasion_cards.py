# Entrees cards.json du scenario 5 SECRET INVASION (sk189-sk227).
# Texte = transcriptions/secret-invasion.md, RELU SUR LES SCANS (15/10/2026) : les 6 faces de mechant, les 4 complots,
# l'environnement, l'attachement Impostor, les 3 Super-Skrull Enhancement, les 8 cartes de rencontre et plusieurs
# paires Impostor (27, 28, 29, 30, 31, 32, 33, 38, 42) ont ete ouvertes une a une ; les autres paires ne portent que
# des chiffres et des textes transcrits tels quels.
# card_id = sk + numero IMPRIME en pied de carte (« MC Custom Content By Kajislav <n> »), suffixe a / b pour les deux
# faces d'une meme carte (mechants, complots, paquet Impostor : allie = a, sbire = b).
#
# Lectures faites en relisant les scans (voir defs/secret_invasion_questions.md) :
#  - L'icone au milieu de la boite de texte des complots annexes (sk199, sk200, sk201) est ACCELERATION (croix sur forme
#    a pointe + barre), comparee a sk156 (Galactic Ambassador) ; les triangles rouges en haut a gauche sont des icones
#    de boost ordinaires (3 pour Chaos, 2 pour Fulfill et Mistrust).
#  - Etoile rouge de boost = pas d'icone chiffree (aucune cle Boost) ; « Y » rose = 1 icone de boost.
#  - Badge orange a droite de la boite de texte des cartes Impostor = POINTS DE VIE (decision NOTES.md : badge orange des
#    allies de campagne = PV), identique sur les deux faces.
#  - Allie Impostor : stat « SCH » (jamais THW) + pastilles creuses = degats consequentiels : ATK « 2** » pour deux
#    pastilles. Le SCH de l'allie (valeur + 1 pastille) n'a pas de cle desc (la classe Ally n'a pas de SCH) : il se lit sur
#    la face sbire de la meme carte (`secret_invasion/__init__.py`, `SchAllie`).
SI = "Secret Invasion"


def c(cid, typ, name, desc, traits, text, set_name=SI):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}


# --------------------------------------------------------------------------------------------------------------------
# Mechant : Spider-Woman (Veranke) = face A (CAMOUFLAGED) / Queen Veranke = face B (REVEALED)
# --------------------------------------------------------------------------------------------------------------------
SW_TEXTE = ("Spider-Woman cannot take damage.\n"
            "[star] <b>Forced Response</b>: After Spider-Woman attacks you, place 1 suspicion counter on \"Who Do You Trust?\".\n"
            "<i>You are a Skrull!</i> — <b>Hero Action</b>: Exhaust a hero and spend 1[per_hero] resources of any type → flip "
            "Spider-Woman. <i>(The players can pay this ability's costs as a group.)</i>")
QV_FLAVOR = ("<i>\"I will be among those on Earth infiltration assignment. I will take a role in this strategy.\"</i>")
QV_BASE = ("<b>Forced Response</b>: After the villain phase ends, if any player is in alter-ego form, flip Queen Veranke.")
QV_VAINCUE = "<b>When Defeated</b>: Remove all suspicion counters from \"Who Do You Trust?\"."
QV_III = (" Otherwise, discard the top card of the encounter deck, if it is a treachery, flip Queen Veranke.")

VILLAINS = [
    c("sk189a", "Villain", "* Spider-Woman (Veranke)", {"HP": "14*", "ATK": "2*", "SCH": "2", "Stage": "1"},
      ["CAMOUFLAGED", "SKRULL"], SW_TEXTE),
    c("sk189b", "Villain", "* Queen Veranke", {"HP": "14*", "ATK": "2", "SCH": "2", "Stage": "1"},
      ["REVEALED", "SKRULL"], QV_BASE + "\n" + QV_VAINCUE + "\n" + QV_FLAVOR),
    c("sk190a", "Villain", "* Spider-Woman (Veranke)", {"HP": "18*", "ATK": "2*", "SCH": "3", "Stage": "2"},
      ["CAMOUFLAGED", "SKRULL"], SW_TEXTE),
    c("sk190b", "Villain", "* Queen Veranke", {"HP": "18*", "ATK": "3", "SCH": "2", "Stage": "2"},
      ["REVEALED", "SKRULL"], QV_BASE + "\n" + QV_VAINCUE + "\n" + QV_FLAVOR),
    c("sk191a", "Villain", "* Spider-Woman (Veranke)", {"HP": "21*", "ATK": "3*", "SCH": "3", "Stage": "3"},
      ["CAMOUFLAGED", "SKRULL"], SW_TEXTE),
    c("sk191b", "Villain", "* Queen Veranke", {"HP": "21*", "ATK": "4", "SCH": "2", "Stage": "3"},
      ["REVEALED", "SKRULL"], QV_BASE + QV_III + "\n" + QV_FLAVOR),
]

# --------------------------------------------------------------------------------------------------------------------
# Complots principaux
# --------------------------------------------------------------------------------------------------------------------
SCHEMES = [
    c("sk192a", "MainScheme", "The Infiltration Has Begun", {"Stage": "1"}, [],
      "<b>Contents</b>: Spider-Woman I and Spider-Woman II <i>(Spider-Woman II and Spider-Woman III instead for expert mode)</i>. "
      "Secret Invasion and Standard encounter sets. One modular encounter set <i>(Army of Skrulls)</i>.\n"
      "<b>Setup</b>: Create the [[IMPOSTOR]] deck and set it next to the encounter deck <i>(see insert)</i>. Put the "
      "\"Who Do You Trust?\" environment into play."),
    c("sk192b", "MainScheme", "The Infiltration Has Begun",
      {"Stage": "1", "TargetThreat": "8*", "EscalationThreat": "1*", "StartingThreat": "2*"}, [],
      "[star] Place 1 additional threat here for each [[SKRULL]] enemy in play and each [[IMPOSTOR]] ally in play.\n"
      "<b>Forced Response</b>: After your turn ends, if there are less than 2[per_hero] suspicion counters on "
      "\"Who Do You Trust?\", put a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck into play under your control."),
    c("sk193a", "MainScheme", "The Skrull Invasion", {"Stage": "2"}, [],
      "<i>The Skrulls, a ruthless group of alien shapeshifters, have secretly replaced many heroes on Earth with impostors "
      "and now they are about to strike.</i>\n"
      "<b>When Revealed</b>: If Mistrust and Paranoia is in play, remove 2[per_hero] suspicion counters from "
      "\"Who Do You Trust?\". Otherwise, find Mistrust and Paranoia and reveal it."),
    c("sk193b", "MainScheme", "The Skrull Invasion",
      {"Stage": "2", "TargetThreat": "14*", "EscalationThreat": "0", "StartingThreat": "1*"}, [],
      "X is equal to twice the number of [[SKRULL]] enemies in play.\n"
      "<b>Forced Response</b>: After your turn ends, if there are less than 2[per_hero] suspicion counters on "
      "\"Who Do You Trust?\", put a [[REVEALED]] minion at random from the [[IMPOSTOR]] deck into play engaged with you.\n"
      "<b>If this stage is completed, the players lose the game.</b>"),
]

# --------------------------------------------------------------------------------------------------------------------
# Environnement
# --------------------------------------------------------------------------------------------------------------------
ENV = [
    c("sk194", "Environment", "\"Who Do You Trust?\"", {}, [],
      "<b>Forced Interrupt</b>: When any amount of threat is placed on the main scheme, remove an equal amount of suspicion "
      "counters from here.\n"
      "<b>Forced Interrupt</b>: When any amount of threat is removed from the main scheme, place an equal amount of "
      "suspicion counters here."),
]

# --------------------------------------------------------------------------------------------------------------------
# Cartes de rencontre
# --------------------------------------------------------------------------------------------------------------------
ENHANCE_ATTACHE = ("Attach to the [[SKRULL]] minion with the most remaining hit points without another Super-Skrull "
                   "Enhancement attached. If you cannot, choose a [[CAMOUFLAGED]] ally, flip that ally and attach this "
                   "card to it. Otherwise, this card gains surge.")
ENHANCE_BOOST = "[star] <b>Boost</b>: Reveal this card, after this activation ends."
ENC = [
    c("sk195", "Attachment", "Impostor", {"Boost": "1"}, ["CONDITION"],
      "Treat attached ally as a [[SKRULL]] minion with a blank text box. Attached minion's SCH is equal to its printed THW "
      "and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the non-[[SKRULL]] ally with the most "
      "remaining hit points without Impostor attached. Attached ally engages its controller. Otherwise, the villain schemes."),
    c("sk196", "Attachment", "Super-Skrull Enhancement", {"ATK+": "2"}, ["CONDITION"],
      ENHANCE_ATTACHE + "\nAttached minion gets +2 hit points.\n" + ENHANCE_BOOST),
    c("sk197", "Attachment", "Super-Skrull Enhancement", {"ATK+": "3"}, ["CONDITION"],
      ENHANCE_ATTACHE + "\n" + ENHANCE_BOOST),
    c("sk198", "Attachment", "Super-Skrull Enhancement", {"ATK+": "2"}, ["CONDITION"],
      ENHANCE_ATTACHE + "\nAttached minion gains retaliate 1.\n" + ENHANCE_BOOST),
    c("sk199", "SideScheme", "Chaos on the Battlefield", {"StartingThreat": "1", "Acceleration": "1", "Boost": "3", "Incite": "2"}, [],
      "<i>\"All I know is, if there's only one way to figure out who's a Skrull... Then I'm more than happy to do it!\"</i> "
      "—Wolverine\nIncite 2.\n<b>When Revealed</b>: Place X additional threat here, where X is equal to the total SCH of all "
      "[[IMPOSTOR]] characters in play."),
    c("sk200", "SideScheme", "Fulfill the Prophecy", {"StartingThreat": "3", "Hinder": "1*", "Acceleration": "1", "Boost": "2"}, [],
      "<i>The holy text of the Book of Worlds was the main reason the Skrulls turned the invasion of Earth into a holy war. "
      "They believed it rightfully theirs.</i>\nHinder 1[per_hero].\nEach [[SKRULL]] minion gains guard and patrol."),
    c("sk201", "SideScheme", "Mistrust and Paranoia", {"StartingThreat": "2", "Acceleration": "1", "Boost": "2"}, [],
      "Players cannot attack minions engaged with other players or defend against them. Players cannot pay any card's or "
      "ability's costs as a group.\n<b>When Revealed</b>: Place 1 additional threat here for each friendly character in play."),
    c("sk202", "Treachery", "Arrival of Impostors", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Each player puts a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck into play under "
      "their control.\n[star] <b>Boost</b>: Put a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck into play under "
      "your control."),
    c("sk203", "Treachery", "Camouflage", {"Boost": "1"}, [],
      "<b>When Revealed</b> (Queen Veranke): Flip Queen Veranke. Remove 3 suspicion counter from \"Who Do You Trust?\".\n"
      "<b>When Revealed</b> (Spider-Woman): Spider-Woman schemes.\n"
      "[star] <b>Boost</b>: Flip Queen Veranke, after this activation ends."),
    c("sk204", "Treachery", "Glory to the Skrull Empire", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Give the villain and each [[SKRULL]] minion engaged with you a tough status card. If the villain "
      "already has a tough status card, this card gains surge.\n[star] <b>Boost</b>: Give the villain a tough status card."),
    c("sk205", "Treachery", "Infiltration Ritual", {}, [],
      "<b>When Revealed</b>: Put a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck into play under any player's "
      "control. If you cannot, this card gains surge.\n[star] <b>Boost</b>: Remove 3 suspicion counters from "
      "\"Who Do You Trust?\"."),
    c("sk206", "Treachery", "Invasion Fleet", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Each player puts a [[REVEALED]] minion at random from the [[IMPOSTOR]] deck into play engaged "
      "with them.\n[star] <b>Boost</b>: Put a [[REVEALED]] minion at random from the [[IMPOSTOR]] deck into play engaged with you."),
    c("sk207", "Treachery", "Revelation", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Flip the [[CAMOUFLAGED]] ally with the most remaining hit points. If you cannot, put a "
      "[[REVEALED]] minion at random from the [[IMPOSTOR]] deck into play engaged with you.\n"
      "[star] <b>Boost</b>: Flip 1 [[CAMOUFLAGED]] ally you control, after this activation ends."),
]

# --------------------------------------------------------------------------------------------------------------------
# Paquet IMPOSTOR : 20 cartes double face. Allie (a) : CAMOUFLAGED, IMPOSTOR, SKRULL ; sbire (b) : IMPOSTOR, REVEALED, SKRULL.
# (numero du set, numero imprime, nom de l'allie, nom du sbire, PV, SCH, ATK, pastilles ATK, texte du sbire (regles), flavor, pronom)
# --------------------------------------------------------------------------------------------------------------------
INTERRUPTION = "<b>Forced Interrupt</b>: When {nom} would leave play, flip {lui} instead."


def revele(nom, lui):
    return f"<b>When Revealed</b>: Heal all damage from {nom} and put {lui} into play engaged with you."


# (n, numero, nom allie, nom court, nom sbire, pronom, PV, SCH, ATK, pastilles ATK, desc sbire, regles sbire avant "When Revealed",
#  regles sbire apres "When Revealed", flavor allie)
IMP = [
    (27, 208, "Captain America (Pitt'o Nili)", "Captain America", "Pitt'o Nili", "him", 4, 1, 2, 2, {"Guard": "1"},
     "Guard. <i>(While this minion is engaged with you, you cannot attack the villain.)</i>\n", "",
     "\"Your death will bring this world's heroes to their knees. Your death will bring the writings to life.\" —Queen Veranke"),
    (28, 209, "Captain Marvel (Khn'nr)", "Captain Marvel", "Khn'nr", "him", 3, 1, 2, 1, {}, "",
     "\n<b>When Defeated</b>: Remove all suspicion counters from \"Who Do You Trust?\".",
     "\"I Speak Skrull perfectly well.\""),
    (29, 210, "Captain Marvel (M'lanz)", "Captain Marvel", "M'lanz", "her", 4, 1, 2, 2, {}, "",
     "\n[star] <b>Forced Interrupt</b>: When M'lanz attacks you, also resolve her attack against each other hero.",
     "\"It was written a world of blue would be the home for all that believed.\" —Queen Veranke"),
    (30, 211, "Carnage (Zr'x)", "Carnage", "Zr'x", "him", 3, 1, 2, 2, {"Toughness": "1"},
     "Toughness. <i>(This character enters play with a tough status card.)</i>\n", "",
     "\"It was written and it has come true.\" —Queen Veranke"),
    (31, 212, "Daredevil (Trl'k)", "Daredevil", "Trl'k", "him", 2, 2, 1, 1, {},
     "While the engaged player is engaged with another [[SKRULL]] minion Trl'k cannot take damage.\n", "",
     "\"As the prophets wrote down to our ancestors.\" —Queen Veranke"),
    (32, 213, "Deathlok (Fry'lu)", "Deathlok", "Fry'lu", "her", 3, 1, 2, 2, {}, "",
     "\n<b>When Defeated</b>: Deal the player who defeated Fry'lu a facedown encounter card.",
     "\"This will not be easy. Most of us will die before this is over.\" —Queen Veranke"),
    (33, 214, "Dum Dum Dugan (Sn'Tlo)", "Dum Dum Dugan", "Sn'Tlo", "him", 4, 2, 1, 1, {},
     "Reduce the amount of damage Sn'Tlo takes from each attack by 1.\n", "",
     "\"You don't reveal your true self in the open.\""),
    (34, 215, "Elektra (Siri)", "Elektra", "Siri", "her", 4, 1, 2, 2, {"Patrol": "1"},
     "Patrol. <i>(While this minion is engaged with you, you cannot thwart the main scheme.)</i>\n", "",
     "\"My identity was not detected.\""),
    (35, 216, "Giant-Man (D'lutz)", "Giant-Man", "D'lutz", "him", 4, 1, 2, 2, {"Retaliate": "1"}, "Retaliate 1.\n", "",
     "\"It was written in our Book of Worlds.\" —Queen Veranke"),
    (36, 217, "Invisible Woman (De'Lila)", "Invisible Woman", "De'Lila", "her", 3, 2, 1, 1, {},
     "As an additional cost to attack De'Lila, you must spend 1 resource of any type.\n", "",
     "\"It's true! I'm not Susan Richards; I am a Skrull!\""),
    (37, 218, "Iron Fist (Grrix)", "Iron Fist", "Grrix", "him", 3, 2, 1, 1, {}, "",
     "\n<b>When Defeated</b>: The villain attacks the player who defeated Grrix <i>(even if that player is in alter-ego form)</i>.",
     "\"He loves me... He loves me... He loves me...\" —Queen Veranke"),
    (38, 219, "Iron Man (Ssrov)", "Iron Man", "Ssrov", "him", 4, 1, 2, 2, {},
     "[star] While the villain has the [[REVEALED]] trait, Ssrov gets +1 SCH and +1 ATK.\n", "",
     "\"In spite of all that you've done to our empire, he loves you.\" —Queen Veranke"),
    (39, 220, "Moon Knight (Hs'fld)", "Moon Knight", "Hs'fld", "him", 3, 1, 2, 2, {}, "",
     "\n<b>When Defeated</b>: The player who defeated Hs'fld puts a [[CAMOUFLAGED]] ally at random from the [[IMPOSTOR]] deck "
     "into play under their control.",
     "\"A billion Skrulls died to prove the words true.\" —Queen Veranke"),
    (40, 221, "Nick Fury (H'kurrek)", "Nick Fury", "H'kurrek", "him", 2, 1, 2, 1, {},
     "[star] H'kurrek's attacks gain overkill, piercing, and ranged.\n", "",
     "\"It was written a wave would come.\" —Queen Veranke"),
    (41, 222, "Phoenix (Korya)", "Phoenix", "Korya", "her", 3, 1, 2, 2, {}, "",
     "\n[star] <b>Forced Response</b>: After Korya attacks you, discard the top card of each player's deck.",
     "\"You will kill her. After we'll switch you out.\" —Queen Veranke"),
    (42, 223, "Spider-Man (Ch'Gra)", "Spider-Man", "Ch'Gra", "him", 2, 1, 2, 1, {}, "",
     "\n<b>When Defeated</b>: Flip Queen Veranke.",
     "\"Well, I do hate myself, but I don't know if I feel like smacking myself around.\""),
    (43, 224, "Thor (Hagar)", "Thor", "Hagar", "him", 4, 1, 2, 2, {},
     "[star] Hagar's attacks deal indirect damage.\n", "",
     "\"He even loves you.\" —Criti Noll"),
    (44, 225, "Venom (Dharr)", "Venom", "Dharr", "him", 3, 2, 1, 1, {"Villainous": "1"},
     "Villainous. <i>(When this minion activates, give it a boost card.)</i>\n", "",
     "\"We now know the words as written are truth!\" —Queen Veranke"),
    (45, 226, "Wolverine (V'lrym)", "Wolverine", "V'lrym", "him", 3, 1, 2, 1, {"Quickstrike": "1"}, "Quickstrike.\n", "",
     "\"This is as it is written. And no Skrull or man can change that.\" —Commander Chrell"),
    (46, 227, "Yellowjacket (Criti Noll)", "Yellowjacket", "Criti Noll", "him", 3, 3, 1, 1, {"Incite": "3"},
     "Incite 3. <i>(When this card is revealed, place 3 threat on the main scheme.)</i>\n", "",
     "\"It won't be long until we have a Skrull in every state!\""),
]
# Le sbire d'Iron Man (n 38) et celui de Spider-Man (Ch'Gra, n 42) : voir defs/secret_invasion_questions.md
# (badges a etoile du SCH/ATK de Ssrov, « Hagar » imprime a la place de « Ch'Gra »).
STAR_SCH_ATK = {"sk219b": {"SCH": "1*", "ATK": "2*"}}          # Ssrov : etoile sur les deux badges
STAR_ATK = {"sk222b", "sk221b", "sk224b", "sk210b"}            # Korya, H'kurrek, Hagar, M'lanz : etoile sur le badge ATK

IMPOSTORS = []
for (n, num, nom, court, sbire, lui, pv, sch, atk, pastilles, desc_sbire, avant, apres, flavor) in IMP:
    a = f"sk{num}a"
    b = f"sk{num}b"
    pronom = lui
    possessif = {"him": "him", "her": "her"}[lui]
    interruption = INTERRUPTION.format(nom=court, lui=lui if lui in ("him", "her") else "him")
    IMPOSTORS.append(c(a, "Ally", "* " + nom, {"HP": str(pv), "ATK": f"{atk}" + "*" * pastilles},
                       ["CAMOUFLAGED", "IMPOSTOR", "SKRULL"], interruption + "\n<i>" + flavor + "</i>"))
    nom_revele = sbire
    if num == 223:      # « Hagar » est imprime a la place de « Ch'Gra » (voir les questions)
        nom_revele = "Hagar"
    desc = {"HP": str(pv), "ATK": str(atk), "SCH": str(sch)}
    desc.update(desc_sbire)
    if b in STAR_SCH_ATK:
        desc.update(STAR_SCH_ATK[b])
    elif b in STAR_ATK:
        desc["ATK"] = f"{atk}*"
    texte = avant + revele(nom_revele, possessif) + apres
    IMPOSTORS.append(c(b, "Minion", "* " + sbire, desc, ["IMPOSTOR", "REVEALED", "SKRULL"], texte))

CARDS = VILLAINS + SCHEMES + ENV + ENC + IMPOSTORS

# Deck rencontre du set SECRET INVASION (une entree par exemplaire), ordre du livret.
ENCOUNTERS_SI = ["sk195", "sk196", "sk197", "sk198", "sk199", "sk199", "sk200", "sk201", "sk202",
                 "sk203", "sk203", "sk203", "sk204", "sk204", "sk205", "sk205", "sk206", "sk207", "sk207", "sk207"]
# Mis de cote : l'environnement + les 20 cartes Impostor (a,b).
SET_ASIDE = ["sk194"] + [f"sk{num}a,sk{num}b" for (_, num, *_r) in IMP]
