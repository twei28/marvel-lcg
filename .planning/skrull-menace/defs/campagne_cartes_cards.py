# Entrees cards.json des 26 CARTES DE CAMPAGNE de Skrull Menace (sk263-sk288) + le rappel
# « Cooperation Progress Reminder » (sk289a / sk289b) + trois cartes TECHNIQUES.
# Texte = transcriptions/campagne.md, RELU SUR LES SCANS (15/10/2026) ; decisions utilisateur
# marquees VERIFIE dans la transcription (noms, badge orange = PV, side scheme : coin haut droit
# = cout / boite noire bas gauche = menace de depart, icones de Pool-O-Vision).
# card_id = sk + numero IMPRIME en pied de carte.
#
# Lectures faites en relisant les scans (voir defs/campagne_cartes_questions.md) :
#  - Class « Campaign;<aspect> » : modele web_of_deceit wd123-wd127 (carte de campagne d'un aspect).
#  - THW/ATK d'un allie : les pastilles « mains » sous la valeur = DEGATS CONSEQUENTS, une etoile
#    `*` par pastille (« 2** » = valeur 2, 2 degats consequents). L'etoile en exposant a cote du
#    chiffre (Paibok, Super-Skrull, War Skrull) n'est qu'un renvoi au texte (decision NOTES.md).
#  - sk270 Buddy Training Program et sk280 Princess Anelle : cout « X » IMPRIME mais calcule par le
#    texte (stade du mechant ; joueurs + ennemis SKRULL) : `Cost` = 0 dans le desc, la valeur est
#    ajoutee par le script (`IncreaseResourceCostToPlay`).
#  - sk271 Cloning Faux Pas porte l'icone ACCELERATION (decision utilisateur du 15/10/2026).
#  - sk285 Ultimate Nullifier : l'icone « personnage » devant « hazard icon » = [per_hero].
CP = "Skrull Menace Campaign"


def c(cid, typ, name, desc, traits, text, subtitle="", set_name=CP):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}


CARDS = [
    # --- Allies -----------------------------------------------------------------------------
    c("sk263", "Ally", "* Crusader",
      {"Cost": "2", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "R", "Class": "Campaign;Aggression"},
      ["INITIATIVE", "SKRULL"],
      "<b>Response</b>: After Crusader enters play, choose a player → deal 1 damage to the villain and each minion "
      "engaged with that player. Draw 1 card for each enemy defeated this way."),
    c("sk264", "Ally", "* Jazinda",
      {"Cost": "3", "HP": "4", "THW": "3**", "ATK": "1*", "RES": "B", "Class": "Campaign;Justice"},
      ["SKRULL"],
      "Jazinda does not count against your ally limit.\nWhile Jazinda is exhausted, your hero gets +1 THW."),
    c("sk265", "Ally", "* Paibok",
      {"Cost": "3", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "R", "Toughness": "1", "Class": "Campaign;Basic"},
      ["S.W.O.R.D.", "SKRULL"],
      "Toughness.\n[star] Paibok gets +1 THW and +1 ATK for each treachery card attached to him.\n"
      "<b>Response</b>: After a treachery card is discarded, take 1 damage → attach it facedown here "
      "(to a maximum of 2)."),
    c("sk266", "Ally", "* Skymax",
      {"Cost": "3", "HP": "5", "THW": "2**", "ATK": "3**", "RES": "R", "Class": "Campaign;Leadership"},
      ["SKRULL", "SQUADRON SUPREME"],
      "<b>Response</b>: When Skymax enters play, shuffle all allies from your discard pile into your deck."),
    c("sk267", "Ally", "* Super-Skrull",
      {"Cost": "3", "HP": "4", "THW": "2**", "ATK": "2**", "RES": "Y", "Class": "Campaign;Basic"},
      ["GUARDIAN", "SKRULL"],
      "[star] Super-Skrull gets +1 THW and +1 ATK for each different [[SUPERPOWER]] card attached to him.\n"
      "<b>Response</b>: After a [[SUPERPOWER]] card is placed into a discard pile, attach it facedown here "
      "(to a maximum of 4).", subtitle="Kl'rt"),
    c("sk268", "Ally", "* Chilly McHotpants",
      {"Cost": "0", "HP": "5", "THW": "2", "ATK": "2", "RES": "R", "Class": "Campaign;'Pool"},
      ["SKRULL"],
      "<i>*Treat this ally as a minion engaged with you.</i>\n"
      "[star] <b>Response</b>: After \"Chilly McHotpants\" attacks you, draw 1 cards. If you take no damage from "
      "that attack, draw 1 card."),
    c("sk269", "Ally", "* Xavin",
      {"Cost": "3", "HP": "5", "THW": "2**", "ATK": "3**", "RES": "B", "Class": "Campaign;Protection"},
      ["RUNAWAYS", "SKRULL"],
      "<b>Interrupt</b>: When Xavin enters play, discard cards from your deck until you discard an event with a "
      "\"<b>Hero Action</b>\" ability. You may resolve that event's \"<b>Hero Action</b>\" ability."),
    # --- Complots annexes de JOUEUR -------------------------------------------------------------
    c("sk270", "PlayerSideScheme", "* Buddy Training Program",
      {"Cost": "0", "RES": "R", "StartingThreat": "2", "Victory": "0", "Class": "Campaign;Protection"},
      [],
      "Victory 0.\nX is equal to the villain's stage number.\n"
      "<b>When Defeated</b>: The player who defeated this scheme may give up to X friendly characters a tough "
      "status card."),
    c("sk271", "PlayerSideScheme", "* Cloning Faux Pas",
      {"Cost": "0", "RES": "Y", "StartingThreat": "3", "Acceleration": "1", "Victory": "0",
       "Class": "Campaign;'Pool"},
      [],
      "Victory 0.\n<b>When Defeated</b>: The player who defeated this scheme may deal up to 3 damage to each "
      "[[SKRULL]] minion engaged with them."),
    c("sk272", "PlayerSideScheme", "* Fickle Alliance",
      {"Cost": "0", "RES": "G", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Leadership"},
      [],
      "Victory 0.\n<b>When Defeated</b>: The player who defeated this scheme may search the encounter deck for a "
      "non-[[ELITE]] minion and put it into play under their control. <i>(Shuffle.)</i> Treat that minion as an "
      "ally with a blank text box <i>(except for</i> [[TRAITS]]<i>)</i>. Its THW is equal to its printed SCH and "
      "it takes 1 consequential damage after it thwarts or attacks."),
    c("sk273", "PlayerSideScheme", "* Newbie Training",
      {"Cost": "0", "RES": "R", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Aggression"},
      [],
      "Victory 0.\n<b>When Defeated</b>: The player who defeated this scheme may defeat a non-[[ELITE]] "
      "[[SKRULL]] minion and draw 1 card."),
    c("sk274", "PlayerSideScheme", "* Searching for Powers",
      {"Cost": "0", "RES": "Y", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Basic"},
      [],
      "Victory 0.\n<b>When Defeated</b>: The player who defeated this scheme may search their deck and discard "
      "pile for a card with the [[SUPERPOWER]] trait and play it, ignoring its resource cost. <i>(Shuffle.)</i>"),
    c("sk275", "PlayerSideScheme", "* Skrull Military Training",
      {"Cost": "0", "RES": "R", "StartingThreat": "3", "Victory": "0", "Class": "Campaign;Basic"},
      [],
      "Victory 0.\nThreat cannot be removed from this scheme unless it is being thwarted by a [[SKRULL]] ally.\n"
      "While this card is in the victory display, its owner's hero gets +1 THW, +1 ATK, and +1 DEF."),
    c("sk276", "PlayerSideScheme", "* Stealing For Good",
      {"Cost": "0", "RES": "R", "StartingThreat": "2", "Victory": "0", "Class": "Campaign;Justice"},
      [],
      "Victory 0.\n<b>When Defeated</b>: The player who defeated this scheme may search their deck and discard "
      "pile for an upgrade and add it to their hand. <i>(Shuffle.)</i> Then, they remove threat from a scheme "
      "equal to that upgrade's printed cost."),
    # --- Soutiens ------------------------------------------------------------------------------
    c("sk277", "Support", "* Antalya",
      {"Cost": "2", "RES": "B", "Class": "Campaign;Protection"},
      ["PERSONA", "SKRULL"],
      "<b>Action</b>: Exhaust Antalya → heal 1 damage from a friendly character."),
    c("sk278", "Support", "* Cadre K",
      {"Cost": "2", "RES": "G", "Class": "Campaign;Justice"},
      ["SKRULL"],
      "<b>Action</b>: Exhaust Cadre K → remove 1 threat from a scheme."),
    c("sk279", "Support", "* Pool-O-Vision",
      {"Cost": "0", "RES": "Y", "Class": "Campaign;'Pool"},
      ["METAGAME"],
      "<b>Hero Response</b>: After a [[SKRULL]] minion is defeated, exhaust Pool-O-Vision → draw 1 card (to a "
      "maximum of 3) for each [crisis], [acceleration], [amplify], and [hazard] in play."),
    c("sk280", "Support", "* Princess Anelle",
      {"Cost": "0", "RES": "G", "Class": "Campaign;Basic"},
      ["PERSONA", "SKRULL"],
      "Alliance.\nX is equal to the total number of players and [[SKRULL]] enemies in play.\n"
      "<b>Response</b>: After the player phase ends, remove Princess Anelle from the game → skip the villain "
      "phase."),
    c("sk281", "Support", "Skrull Battleship",
      {"Cost": "2", "RES": "G", "Class": "Campaign;Leadership"},
      ["SKRULL", "VEHICLE"],
      "Play only if you control a [[SKRULL]] ally.\n<b>Hero Resource</b>: Exhaust Skrull Battleship → generate "
      "a [wild] resource for any player."),
    c("sk282", "Support", "* Skrull Kill Krew",
      {"Cost": "2", "RES": "R", "Class": "Campaign;Aggression"},
      ["CREW"],
      "<b>Hero Action</b>: Exhaust Skrull Kill Krew → deal 1 damage to a [[SKRULL]] minion. If that minion is "
      "defeated this way, ready Skrull Kill Krew."),
    # --- Ameliorations ---------------------------------------------------------------------------
    c("sk283", "Upgrade", "* 3-D Man's Goggles",
      {"Cost": "2", "RES": "B", "Class": "Campaign;Leadership"},
      ["ITEM", "TECH"],
      "Attach to a non-[[SKRULL]] ally.\n<b>Interrupt</b>: When attached ally attacks a [[SKRULL]] enemy, that "
      "ally does not take consequential damage."),
    c("sk284", "Upgrade", "* Inhibitor Mask",
      {"Cost": "1", "RES": "R", "Temporary": "1", "Class": "Campaign;Basic"},
      ["ITEM"],
      "Attach to a [[SKRULL]] enemy.\nTemporary.\nTreat attached enemy's printed text box as if it were blank."),
    c("sk285", "Upgrade", "* Ultimate Nullifier",
      {"Cost": "0", "RES": "R", "Temporary": "1", "Class": "Campaign;'Pool"},
      ["ITEM", "TECH"],
      "Attach to a [[SKRULL]] enemy.\nTemporary.\nAttached enemy cannot activate.\nWhile Nullifier is attached to "
      "the villain, it gains 1[per_hero] hazard icon ([hazard])."),
    c("sk286", "Upgrade", "Reverting Device",
      {"Cost": "0", "RES": "Y", "Class": "Campaign;Justice"},
      ["ITEM", "TECH"],
      "Play under any player's control.\nEach [[SKRULL]] minion engaged with you gets -1 SCH."),
    c("sk287", "Upgrade", "Skrull Shapeshifter",
      {"Cost": "1", "RES": "G", "Class": "Campaign;Protection"},
      ["CONDITION"],
      "Play under any player's control.\nYour identity gains the [[SKRULL]] trait.\n<b>Interrupt</b>: When you "
      "would be defeated, set your hit point dial to 1 instead. Then, discard this card."),
    c("sk288", "Upgrade", "* Sy-Torak Gem",
      {"Cost": "2", "RES": "Y", "Class": "Campaign;Aggression"},
      ["ARTIFACT"],
      "Play under any player's control.\nYou get +3 hit points.\nYour hero gets +1 ATK.\n<b>Forced Interrupt</b>: "
      "When your deck empties, spend [energy] resource. If you cannot, discard Sy-Torak Gem."),
    # --- Rappel (carte sans numero, deux faces, type « Insert » comme rule_a / rule_b) -----------------
    c("sk289a", "Insert", "Cooperation Progress Reminder", {}, [],
      "<i>Campaign Mode Only.</i>\n<b>Interrupt</b>: When a player defeats a minion or a side scheme, that player "
      "may discard the top card of their deck to place that minion or side scheme in the victory display instead "
      "of the encounter discard pile."),
    c("sk289b", "Insert", "Cooperation Progress Reminder", {}, [],
      "<b><i>Do not flip this unless you intend to build cooperation.</i></b>"),
    # --- Cartes TECHNIQUES (gabarits de conversion, jamais dans un deck) -----------------------------
    # War Skrull / Chilly McHotpants : la forme SBIRE de l'allie (TreatAsMinion). Le texte imprime reste
    # actif (Response : pioche) ; le nom, l'image, l'ATQ et le MNG sont repris de l'allie par le script.
    {"card_id": "skrull_war_minion", "pic_id": "player", "type": "Minion", "name": "Chilly McHotpants Minion",
     "subtitle": "", "desc": {"HP": "5"}, "traits": ["SKRULL"], "set_name": CP,
     "text": "[star] <b>Response</b>: After \"Chilly McHotpants\" attacks you, draw 1 cards. If you take no damage "
             "from that attack, draw 1 card.", "custom": "Kajislav"},
    # Fickle Alliance : la forme ALLIE du sbire (Faces.TreatAsAlly). Texte blanc ; 1 degat consequent apres un
    # contre ou une attaque (une etoile par pastille, comme fne_black_cat_ally).
    {"card_id": "skrull_fickle_ally", "pic_id": "encounter", "type": "Ally", "name": "Fickle Ally",
     "subtitle": "", "desc": {"HP": "0", "ATK": "0*", "THW": "0*", "Class": "Encounter"}, "traits": [],
     "set_name": CP, "text": "", "custom": "Kajislav"},
]
