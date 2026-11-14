# Entrees cards.json du lot GS-8 de Galactic Storm (Kajislav) : scenario 5 « Supreme Intelligence »
# (gs195-gs208) et les sets modulaires du meme bloc : Starforce (gs209-gs217), Seeds of Corruption
# (gs218-gs221), Nega-Bomb (gs222a/gs222b, gs223).
#
# card_id = « gs » + numero IMPRIME en pied de carte (decision utilisateur du 20/10/2026) ; UN card_id
# par numero imprime, les exemplaires sont comptes dans le scenario / le set (comme Skrull Menace).
# Texte = transcriptions/supreme-intelligence.md et modular-sets.md, RELU SUR CHAQUE SCAN (20/10/2026).
#
# Lectures faites en relisant les scans (voir .planning/todos/2026-10-20-gs8-questions.md) :
#  - Icone « croix + pointe + barre » (gs203 Ren-Varr, gs205 Loyalty to Supremor) = ACCELERATION :
#    meme dessin que sk229 Cosmic Cube Creation (convention validee le 15/10/2026).
#  - Icone « carte penchee nue + croix » (gs207 Supremor Seed) = HAZARD, meme dessin que sk234.
#  - Icone « croix + avion » (gs206 Selective Breeding) = AMPLIFY.
#  - Icone de RESSOURCE « trois noeuds relies » (gs218, gs219, gs220) = MENTALE (B) : decoupe comparee au
#    coin de sk003 Wiccan (RES=B, meme maquette Kajislav) ; ni le poing (R, sk004), ni l'eclair (Y, sk008),
#    ni l'etoile (G, sk010).
#  - Etoile accolee a un nombre (PV 3 de Supremor, ATK 1 d'Ultimus / Shatterax, objectif 6 de gs198b) =
#    renvoi aux effets ★ du texte, sans valeur chiffree (convention validee le 15/10/2026). Le « * » de
#    `desc` reste donc reserve aux silhouettes « par joueur » (HP, menaces) ; ATK "1*" = convention
#    Skrull Menace (sk245 War Skrull), sans effet sur un sbire.
#  - gs198b : objectif 6 SANS silhouette, escalade +2 SANS silhouette, depart 0 (lu sur le scan, carte
#    pivotee) ; gs199b : depart 1, escalade +1 et objectif 11, tous trois PAR JOUEUR (la transcription
#    avait oublie l'objectif 11).
#  - « Y » rouge = 1 icone de boost ; etoile rouge du coin = carte a « ★ Boost » (aucune cle Boost).
#  - gs199b imprime « If this stage is completes » : coquille (question Q4 du lot GS-0, recommandation
#    « traiter comme la forme officielle ») ; le texte de jeu porte la forme officielle « completed ».
SI = "Supreme Intelligence"
SF = "Starforce"
SC = "Seeds of Corruption"
NB = "Nega-Bomb"


def c(cid, typ, name, desc, traits, text, set_name, **extra):
    carte = {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
             "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}
    carte.update(extra)
    return carte


CITATION_SI = ("<i>\"...I am the living embodiment of power...for I am the Supreme Intelligence of the majestic race of "
               "the Kree!\"</i>")
REPONSE_I_II = ("<b>Forced Response</b>: After a [[KREE]] minion is defeated, heal 1 damage from the villain. If that "
                "minion has the [[ELITE]] trait, give the villain a facedown boost card.")
STARFORCE_TRAITS = ["ELITE", "KREE", "STARFORCE"]


def starforce(cid, nom, sch, atk, texte, citation, **desc_en_plus):
    desc = {"HP": "8", "SCH": sch, "ATK": atk, "Villainous": "1", "Victory": "1", "Boost": "3"}
    desc.update(desc_en_plus)
    return c(cid, "Minion", "* " + nom, desc, STARFORCE_TRAITS, texte + "\n<i>" + citation + "</i>", SF)


CARDS = [
    # ===================================================================== Supreme Intelligence (195-208)
    c("gs195", "Villain", "* Supreme Intelligence", {"HP": "13*", "SCH": "2", "ATK": "1", "Stage": "1"}, ["KREE"],
      REPONSE_I_II + "\n" + CITATION_SI, SI),
    c("gs196", "Villain", "* Supreme Intelligence", {"HP": "14*", "SCH": "2", "ATK": "2", "Stage": "2", "Toughness": "1"},
      ["KREE"], "Toughness.\n" + REPONSE_I_II + "\n" + CITATION_SI, SI),
    c("gs197", "Villain", "* Supreme Intelligence", {"HP": "15*", "SCH": "3", "ATK": "2", "Stage": "3", "Toughness": "1"},
      ["KREE"],
      "Toughness.\n<b>Forced Response</b>: After a [[KREE]] minion is defeated, heal 1 damage from the villain and give it "
      "a facedown boost card.\n" + CITATION_SI, SI),
    c("gs198a", "MainScheme", "Protectors of the Kree Empire", {"Stage": "1"}, [],
      "<b>Contents</b>: Supreme Intelligence (I) and (II) <i>(Supreme Intelligence (II) and (III) instead for expert "
      "mode)</i>. Supreme Intelligence, Starforce, and Standard sets. One modular encounter set <i>(Seeds of "
      "Corruption)</i>.\n<b>Setup</b>: Set each [[STARFORCE]] minion aside and put 1 of them at random into play engaged "
      "with the first player. Attach Holding Tank to the villain.", SI),
    c("gs198b", "MainScheme", "Protectors of the Kree Empire",
      {"Stage": "1", "TargetThreat": "6", "EscalationThreat": "2", "StartingThreat": "0"}, [],
      "The target threat value of this scheme cannot be changed.\n[star] <b>Forced Interrupt</b>: When this scheme would "
      "be completed, remove all threat from here instead and put a random set aside [[STARFORCE]] minion into play "
      "engaged with the first player. Then, if there are 5 or less set aside [[STARFORCE]] minions, advance to stage 2A.",
      SI),
    c("gs199a", "MainScheme", "The Endless Mind", {"Stage": "2"}, [],
      "<i>\"The Supreme Intelligence. It killed every person who it admired or who opposed it, and added their minds, dead "
      "and screaming, to its own.\" —Carol Danvers</i>\n<b>When Revealed</b>: Shuffle each set aside [[STARFORCE]] minion "
      "into the encounter deck.", SI),
    c("gs199b", "MainScheme", "The Endless Mind",
      {"Stage": "2", "TargetThreat": "11*", "EscalationThreat": "1*", "StartingThreat": "1*"}, [],
      "<i>The Supreme Intelligence is the collective of the greatest Kree minds in history removed upon their deaths and "
      "assimilated by the supercomputer in a process called \"Supremorization\".</i>\n<b>If this stage is completed, the "
      "players lose the game.</b>", SI),
    c("gs200", "Attachment", "Holding Tank", {"Uses": "7*,integrity", "Victory": "0"}, [],
      "Uses (7[per_hero] integrity counters). Victory 0.\nReduce the amount of damage the villain takes from each attack by "
      "2.\n<b>Forced Response</b>: After an enemy takes any amount of damage, remove 1 integrity counter from here.", SI),
    c("gs201", "Attachment", "Genetic Augmentation", {"ATK+": "1", "Boost": "1"}, ["CONDITION"],
      "Attach to the [[KREE]] minion with the most remaining hit points. Otherwise, this card gains surge.\nAttached minion "
      "gets +2 hit points and gains the [[ELITE]] trait.\n<i>\"I used the crystal's power on my Kree subjects...effecting "
      "countless millennia of evolution in mere moments.\" —Supreme Intelligence</i>", SI),
    c("gs202", "Minion", "Kree Infantry", {"HP": "5", "SCH": "1", "ATK": "2", "Guard": "1", "Patrol": "1", "Boost": "1"},
      ["KREE"],
      "Guard. Patrol.\n<b>When Defeated</b>: Place 2 threat on the main scheme.\n<i>\"The Kree ascension is now and those "
      "who stand in its way will fall.\" —Minister Marvel</i>", SI),
    c("gs203", "Minion", "* Ren-Varr", {"HP": "5", "SCH": "2", "ATK": "1", "Vulnerable": "1", "Acceleration": "1",
                                        "Boost": "2"}, ["GENIUS", "KREE"],
      "Vulnerable.\n<b>When Defeated</b>: Give the villain a tough status card.\n<i>\"I have the power to undo the "
      "annihilation of the Kree race!\"</i>", SI),
    c("gs204", "Minion", "Supremor", {"HP": "3", "SCH": "1", "ATK": "1", "Villainous": "1", "Boost": "2"},
      ["ELITE", "KREE", "STARFORCE"],
      "Villainous.\n[star] Supremor gets +1 hit point for each [[KREE]] minion in the victory display.\n<i>\"The Kree will "
      "erase your misbegotten race from existence!\"</i>", SI),
    c("gs205", "SideScheme", "Loyalty to Supremor", {"StartingThreat": "3*", "Acceleration": "1", "Boost": "1"}, [],
      "<i>\"Revenge. Yes! That is something something a Kree can understand!\" —Doctor Minerva</i>\nEach minion gains "
      "guard.", SI),
    c("gs206", "SideScheme", "Selective Breeding", {"StartingThreat": "6", "Amplify": "1", "Boost": "3"}, [],
      "<b>When Revealed</b>: Shuffle each [[KREE]] minion from the encounter discard pile into the encounter deck.", SI),
    c("gs207", "SideScheme", "Supremor Seed", {"StartingThreat": "4*", "Hazard": "1", "Boost": "2"}, [],
      "<b>When Defeated</b>: The defeating player may place 1 [[KREE]] minion from the victory display in the encounter "
      "discard pile.", SI),
    c("gs208", "Treachery", "Summon Reinforcements", {"Boost": "2"}, [],
      "<b>When Revealed</b>: If there is at least 1 [[STARFORCE]] minion set aside, the villain schemes. Otherwise, discard "
      "cards from the top of the encounter deck until a minion is discarded and reveal it.\n<i>\"The Supreme Intelligence "
      "of the Kree calls you. I know who you are.\" —Supreme Intelligence</i>", SI),
    # ===================================================================== Starforce (209-217)
    starforce("gs209", "Cadmi-M the Pursuer", "1", "1",
              "Retaliate 1. Villainous. Victory 1.\nWhile Cadmi-M the Pursuer is in the victory display, the villain "
              "gains retaliate 1.", "\"Oh well...improvisation works well too.\"", Retaliate="1"),
    starforce("gs210", "Doctor Minerva", "2", "1",
              "Villainous. Victory 1.\nWhile Doctor Minerva is in the victory display, the villain gets +1 SCH.",
              "\"Don't hurt your primitive human brain. Let me.\""),
    starforce("gs211", "Inndig-O the Accuser", "1", "2",
              "Villainous. Victory 1.\nWhile Inndig-O the Accuser is in the victory display, the villain gets +1 ATK.",
              "\"...I know an accusation when I hear one!\""),
    starforce("gs212", "Korath the Pursuer", "1", "1",
              "Retaliate 1. Villainous. Victory 1.\nWhile Korath the Pursuer is in the victory display, the villain gains "
              "retaliate 1.", "\"One touch of my beta-baton will wipe your smirk from all existence...\"", Retaliate="1"),
    starforce("gs213", "Protector", "1", "1",
              "Steady. Villainous. Victory 1.\nWhile Protector is in the victory display, the villain gains steady.",
              "\"Each of us in this unit has a job.\"", Steady="1"),
    starforce("gs214", "Ronan the Accuser", "1", "2",
              "Villainous. Victory 1.\nWhile Ronan the Accuser is in the victory display, the villain gets +1 ATK.",
              "\"...this is the highes crime of all, to be un-Kree...\""),
    starforce("gs215", "Shatterax", "1", "1*",
              "Villainous. Victory 1.\n[star] Shatterax's attacks gain piercing.\nWhile Shatterax is in the victory "
              "display, the villain's attacks gain piercing.",
              "\"Agent Shatterax to Hala Command and Control. Action against alien intrusion on Outpost SIK/SIGMA now in "
              "progress.\""),
    starforce("gs216", "Ultimus", "1", "1*",
              "Villainous. Victory 1.\n[star] Ultimus's attacks gain overkill.\nWhile Ultimus is in the victory display, "
              "the villain's attacks gain overkill.", "\"Such a fool deserves death!\""),
    c("gs217", "Treachery", "Starformation", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Give each [[STARFORCE]] minion a tough status card and a facedown boost card. Otherwise, give "
      "the villain a tough status card and a facedown boost card.\n<i>\"We have been gathered by the Supreme Intelligence "
      "for a reason, for this is a turning point in our history, and we are needed!\" —Ultimus</i>", SF),
    # ===================================================================== Seeds of Corruption (218-221)
    c("gs218", "Attachment", "Manipulated Memories", {"Boost": "1"}, ["CONDITION"],
      "Attach to your identity.\nEach event card in your hand gains requirement ([mental]).\n<b>Hero Action</b>: Spend 2 "
      "resources of the same type → discard this card.\n<hr />\n[star] <b>Boost</b>: If this activation is a scheme, you "
      "are confused. Otherwise, you are stunned.", SC),
    c("gs219", "SideScheme", "Psychic Shackles", {"StartingThreat": "3", "Hinder": "1*", "Boost": "2"}, [],
      "<i>\"Now that you are truly helpless, I will assimilate your intellect, conquering your mind as well as your "
      "body!\" —Supreme Intelligence</i>\nHinder 1[per_hero].\nPlayers cannot play cards with a printed [mental] "
      "resource.", SC),
    c("gs220", "Treachery", "Mental Torture", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Discard 1 random card from your hand. If a [mental] resource was discarded this way, stun "
      "your identity.\n<i>\"While you writhe in abject helplessness, I have probed your primitive brains! And now... I am "
      "done!\" —Supreme Intelligence</i>", SC),
    c("gs221", "Treachery", "Whisper in the Mind", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Find a copy of your obligation and reveal it. If your obligation was not revealed this way, "
      "this card gains surge.\n<hr />\n[star] <b>Boost</b>: If your obligation is in the victory display or if it was "
      "removed from the game, shuffle it into the encounter deck.", SC),
    # ===================================================================== Nega-Bomb (222A/222B, 223)
    c("gs222a", "SideScheme", "Nega-Bomb", {"StartingThreat": "8*", "Setup": "1", "Victory": "0"}, [],
      "<i>\"The Nega-Bomb is the most abominable devices the Shi'ar people have ever created.\"</i>\nSetup. Victory 0.\n"
      "Enters play with 4 time counters on it.\n<b>Forced Response</b>: After resolving step one of the villain phase, "
      "remove 1 time counter from here. If there is no time counter here, flip this card and reveal Detonation.", NB),
    c("gs222b", "Environment", "Detonation", {}, [],
      "<b>When Revealed</b>: Deal X damage to each friendly character and minion in play ignoring any tough status card, "
      "where X is equal to the amount of threat here divided by the total number of friendly characters and minions in "
      "play (rounded up). Remove this card from the game.", NB),
    c("gs223", "Treachery", "Green Interference", {"Boost": "2"}, [],
      "<b>When Revealed</b>: Remove 1 all-purpose counter from each card in play. If no counter was removed this way, this "
      "card gains surge.\n<hr />\n[star] <b>Boost</b>: Remove 1 all-purpose counter from a card in play.", NB),
]

# Exemplaires (un card_id par numero imprime, decision du 20/10/2026).
EXEMPLAIRES = {"gs201": 2, "gs202": 4, "gs204": 2, "gs207": 2, "gs208": 2, "gs218": 2, "gs220": 2, "gs221": 2, "gs223": 2}


def x(cid):
    return [cid] * EXEMPLAIRES.get(cid, 1)


# Paquet rencontre propre au scenario (Holding Tank est MIS DE COTE : le Setup de 1A l'attache).
ENCOUNTERS_SCENARIO = [i for cid in ["gs201", "gs202", "gs203", "gs204", "gs205", "gs206", "gs207", "gs208"] for i in x(cid)]
# Starforce est OBLIGATOIRE pour ce scenario (insert) : ses cartes sont listees avec celles du scenario
# (et non dans `modular_sets`, qu'un joueur peut retirer) ; le Setup de 1A met de cote les sbires STARFORCE.
STARFORCE = ["gs209", "gs210", "gs211", "gs212", "gs213", "gs214", "gs215", "gs216", "gs217"]

ENCOUNTERS = {
    "gs_starforce": ("Starforce", STARFORCE),
    "gs_seeds_of_corruption": ("Seeds of Corruption", [i for cid in ["gs218", "gs219", "gs220", "gs221"] for i in x(cid)]),
    # Nega-Bomb : le complot annexe double face (222A / 222B) + les deux Green Interference.
    "gs_nega_bomb": ("Nega-Bomb", ["gs222a,gs222b", "gs223", "gs223"]),
}
