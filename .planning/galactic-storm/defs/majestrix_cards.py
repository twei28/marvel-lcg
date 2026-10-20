# Entrees cards.json du scenario 2 MAJESTRIX'S VERDICT de Galactic Storm (gs114-gs137), lot GS-5 (20/10/2026).
# Texte = docs/packs/galactic-storm/transcriptions/majestrix-verdict.md, RELU SUR LES 34 SCANS le 20/10/2026.
# card_id = gs + numero IMPRIME en pied de carte (« MC Custom Content By: Kajislav <n> »), 3 chiffres (+ a/b) ;
# UN card_id par numero imprime, les copies sont des exemplaires du paquet (decisions utilisateur du 20/10/2026).
#
# Lectures faites sur les scans (preuves de decoupe dans le gabarit, MAJESTRIX-GABARITS.md) :
#  - icones de ressource, comparees par decoupe aux cartes Kajislav de Skrull Menace dont la fiche declare la
#    ressource (sk003 Wiccan B, sk004 R, sk008 Y, et les icones de texte de sk148 [mental][physical]) :
#    carre bleu « noeuds relies » = B (Ch'od, Raza, Shi'ar Crest, Shi'ar Throne) ; carre jaune « eclair » = Y
#    (Corsair, Korvus, Royal Cape) ; carre rouge « poing » = R (Hepzibah, Shi'ar Javelin).
#  - icones de manigance, comparees a sk100 Emperor's Throne (Hazard + Acceleration) et sk115 (Crisis) /
#    sk252 (Amplify) : Private Audience = ACCELERATION (croix, pointe, barre) ; Shi'ar Throne (face manigance)
#    = HAZARD (carte penchee + croix) ; Tapping the M'kraan Force = AMPLIFY (avion + croix) ET HAZARD ;
#    Tortured Prisoners = CRISIS (« ! » dans une explosion).
#  - silhouette apres un nombre = « par joueur » (`*` dans desc) ; etoile pleine devant une capacite ou en
#    exposant d'une stat = renvoi au texte (convention Skrull Menace validee) ; Y rouge = 1 icone de boost.
#  - pastilles orange des allies et sbires = PV ; etoiles a contour sous THW/ATK d'un allie = degats consecutifs
#    (une `*` par etoile, comme sk023 Talos « 3** »).
GS = "Majestrix's Verdict"


def c(cid, typ, name, desc, traits, text, subtitle=""):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": subtitle, "desc": desc,
            "traits": traits, "set_name": GS, "text": text, "custom": "Kajislav"}


INTERRUPT_STARJAMMER = ("[star] <b>Forced interrupt</b>: When Deathbird initiates an attack against you, if you control a "
                        "[[STARJAMMER]] ally, she attacks that ally instead")
INVAINCUE = "Deathbird cannot be defeated, if players do not control Lilandra and the Shi'ar Throne support."
SUR_LILANDRA = "<b>Response</b>: After Lilandra attacks Deathbird, spend a {res} resource → attach this card to Lilandra."
APRES_ETAPE_1 = ("[star] <b>Forced Response</b>: After resolving step one of the villain phase, place 2 threat on Imprisoned "
                 "on Chandilar for each player in alter-ego form.")

CARDS = [
    # --- Mechant ------------------------------------------------------------------------------------------
    c("gs114", "Villain", "* Deathbird", {"HP": "16*", "ATK": "2", "SCH": "2", "Stage": "1"}, ["SHI'AR"],
      INTERRUPT_STARJAMMER + " with +1 ATK."),
    c("gs115", "Villain", "* Deathbird", {"HP": "19*", "ATK": "3", "SCH": "2", "Stage": "2"}, ["SHI'AR"],
      INVAINCUE + "\n" + INTERRUPT_STARJAMMER + " with +1 ATK."),
    c("gs116", "Villain", "* Deathbird", {"HP": "21*", "ATK": "3", "SCH": "2", "Stage": "3"}, ["SHI'AR"],
      INVAINCUE + "\n" + INTERRUPT_STARJAMMER + ". Give her 1 additional boost card for that activation."),
    # --- Manigances principales ---------------------------------------------------------------------------
    c("gs117a", "MainScheme", "Earn the People's Favor", {"Stage": "1"}, [],
      "<b>Contents</b>: Deathbird (I) and Deathbird (II) <i>(Deathbird (II) and Deathbird (III) instead for expert "
      "mode)</i>. Majestrix's Verdict, and Standard encounter sets. One modular encounter set <i>(Imperial Guard)</i>.\n"
      "<b>Setup</b>: Set the Shi'ar Throne side scheme aside. Put the Imprisoned on Chandilar side scheme into play and "
      "tuck each [[STARJAMMER]] ally under it."),
    c("gs117b", "MainScheme", "Earn the People's Favor",
      {"Stage": "1", "TargetThreat": "3*", "EscalationThreat": "1*", "StartingThreat": "0"}, [],
      "<b>When Revealed</b>: Place 1[per_hero] threat on Imprisoned on Chandilar.\n" + APRES_ETAPE_1),
    c("gs118a", "MainScheme", "Majestrix's Verdict", {"Stage": "2"}, [],
      "<b>When Revealed</b>: The players as a group choose 1 [[STARJAMMER]] ally tucked under Imprisoned on Chandilar "
      "and remove it from the game <i>(2 [[STARJAMMER]] allies instead in expert mode)</i>. Otherwise, the players as a "
      "group choose 1 [[STARJAMMER]] ally in play and remove it from the game. Advance to stage 2B."),
    c("gs118b", "MainScheme", "Majestrix's Verdict",
      {"Stage": "2", "TargetThreat": "5*", "EscalationThreat": "2*", "StartingThreat": "0"}, [],
      "<b>When Revealed</b>: Place 1[per_hero] threat on Imprisoned on Chandilar.\n"
      "<b>Forced Interrupt</b>: When this stage would be completed, flip this card and reveal it instead.\n" + APRES_ETAPE_1),
    # --- Prison et trone -----------------------------------------------------------------------------------
    c("gs119", "SideScheme", "Imprisoned on Chandilar", {"StartingThreat": "6", "Assault": "1", "Permanent": "1"}, [],
      "Assault. Permanent.\n<b>Forced Response</b>: After a [[STARJAMMER]] ally leaves play, tuck it under here.\n"
      "<b>Forced Interrupt</b>: When the last threat is removed from here, the players as a group choose a "
      "[[STARJAMMER]] ally tucked under here, put that ally into play under any player's control and place 6 threat here."),
    c("gs120a", "SideScheme", "Shi'ar Throne", {"StartingThreat": "3*", "Hazard": "1"}, [],
      "<b>When Defeated</b>: The defeating player flips this card and takes control of it."),
    c("gs120b", "Support", "* Shi'ar Throne", {}, ["LOCATION", "SHI'AR"],
      "<b>Resource</b>: Exhaust Shi'ar Throne → generate a [mental] resource for any player.\n"
      "<b>Forced Response</b>: After Shi'ar Throne or Lilandra leaves play, flip this card and reveal it."),
    # --- Starjammers ---------------------------------------------------------------------------------------
    c("gs121", "Ally", "* Lilandra", {"HP": "4", "THW": "1", "ATK": "2*", "Class": "Encounter"}, ["SHI'AR", "STARJAMMER"],
      "Does not count against your ally limit.\n<b>Forced Response</b>: After Lilandra enters play, reveal the set aside "
      "Shi'ar Throne side scheme.\n<b>If Lilandra is removed from the game, the players lose the game.</b>",
      subtitle="Lilandra Neramani"),
    c("gs122", "Ally", "* Ch'od", {"Cost": "3", "HP": "6", "THW": "1*", "ATK": "3**", "RES": "B", "Retaliate": "2",
                                   "Class": "Campaign;Basic"}, ["STARJAMMER"],
      "Retaliate 2."),
    c("gs123", "Ally", "* Corsair", {"Cost": "3", "HP": "4", "THW": "2*", "ATK": "2*", "RES": "Y",
                                     "Class": "Campaign;Basic"}, ["STARJAMMER"],
      "[star] Corsair's attacks gain ranged.", subtitle="Christopher Summers"),
    c("gs124", "Ally", "* Hepzibah", {"Cost": "3", "HP": "3", "THW": "2*", "ATK": "3*", "RES": "R",
                                      "Class": "Campaign;Basic"}, ["STARJAMMER"],
      "[star] Hepzibah's attacks gain piercing."),
    c("gs125", "Ally", "* Korvus", {"Cost": "3", "HP": "5", "THW": "1*", "ATK": "3**", "RES": "Y",
                                    "Class": "Campaign;Basic"}, ["SHI'AR", "STARJAMMER"],
      "[star] Korvus's attacks gain overkill.", subtitle="Korvus Rook'shir"),
    c("gs126", "Ally", "* Raza", {"Cost": "3", "HP": "3", "THW": "2*", "ATK": "2*", "RES": "B", "Toughness": "1",
                                  "Class": "Campaign;Basic"}, ["CYBORG", "STARJAMMER"],
      "Toughness.", subtitle="Raza Longknife"),
    # --- Attachements ----------------------------------------------------------------------------------------
    c("gs127", "Attachment", "Royal Cape of the Shi'ar", {"Boost": "2"}, ["ARMOR"],
      "Attach to Deathbird.\nAttached character gets +2 hit points and gains retaliate 1.\n"
      + SUR_LILANDRA.format(res="[energy]")),
    c("gs128", "Attachment", "Shi'ar Crest", {"Boost": "1", "SCH+": "1", "THW+": "1"}, ["ITEM"],
      "Attach to Deathbird.\nAttached character gains steady.\n" + SUR_LILANDRA.format(res="[mental]")
      + "\n<hr />\n[star] <b>Boost</b>: Give the activating enemy a tough status card."),
    c("gs129", "Attachment", "Shi'ar Javelin", {"Boost": "1", "ATK+": "1"}, ["WEAPON"],
      "Attach to Deathbird.\n[star] Attached character's attacks gain piercing and overkill.\n"
      + SUR_LILANDRA.format(res="[physical]")
      + "\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, it gains piercing and overkill."),
    # --- Sbires ----------------------------------------------------------------------------------------------
    c("gs130", "Minion", "* Araki", {"HP": "4", "SCH": "3", "ATK": "1", "Patrol": "1", "Vulnerable": "1"}, ["SHI'AR"],
      "Patrol. Vulnerable.\n<b>When Defeated</b>: Place 2 threat on each scheme in play.\n<hr />\n"
      "[star] <b>Boost</b>: Place 1 threat on each scheme in play."),
    c("gs131", "Minion", "Jailor of Chandilar", {"HP": "6", "SCH": "1", "ATK": "2", "Retaliate": "1", "Boost": "1"}, ["SHI'AR"],
      "Retaliate 1.\n<b>When Defeated</b>: Remove 2 threat from Imprisoned on Chandilar.\n<hr />\n"
      "[star] <b>Boost</b>: Place 1 threat on Imprisoned on Chandilar."),
    # --- Manigances annexes ----------------------------------------------------------------------------------
    c("gs132", "SideScheme", "Private Audience", {"StartingThreat": "3*", "Acceleration": "1"}, [],
      "Allies cannot attack the villain or thwart the main scheme."),
    c("gs133", "SideScheme", "Tapping the M'kraan Force",
      {"StartingThreat": "2", "Hinder": "2*", "Amplify": "1", "Hazard": "1", "Boost": "3"}, [],
      "Hinder 2[per_hero].\n<b>When Defeated</b>: Heal 1 damage from each [[STARJAMMER]] ally in play."),
    c("gs134", "SideScheme", "Tortured Prisoners", {"StartingThreat": "1*", "Crisis": "1", "Boost": "2"}, [],
      "<b>When Revealed</b>: Place 1 additional threat here for each [[STARJAMMER]] ally tucked under Imprisoned on Chandilar."),
    # --- Traitrises ------------------------------------------------------------------------------------------
    c("gs135", "Treachery", "Birthright to the Throne", {"Boost": "1"}, [],
      "<b>When Revealed</b>: If the Shi'ar Throne support is in play, Deathbird attacks the player who controls it "
      "<i>(even if that player is in alter ego form)</i>. Otherwise, Deathbird schemes.\n<hr />\n"
      "[star] <b>Boost</b>: Give Deathbird a tough status card."),
    c("gs136", "Treachery", "Exemplar Punishment", {"Boost": "1"}, [],
      "<b>When Revealed</b>: For each [[STARJAMMER]] ally tucked under Imprisoned on Chandilar choose to either take 1 "
      "indirect damage or place 1 threat on the main scheme. If there is no ally tucked under Imprisoned on Chandilar, "
      "place 2 threat on it."),
    c("gs137", "Treachery", "Sister's Deception", {"Boost": "2"}, [],
      "<b>When Revealed</b>: If Lilandra is in play, she attacks you <i>(resolve her ATK against you without exhausting "
      "her, but with taking consequential damage)</i>. Otherwise, place 3 threat on Imprisoned on Chandilar."),
]

# Paquet rencontre du scenario (18 cartes, numeros 14 a 31 de « MAJESTRIX'S VERDICT (n/31) »).
ENCOUNTERS = (["gs127", "gs128", "gs129", "gs129", "gs130"] + ["gs131"] * 4
              + ["gs132", "gs133", "gs134", "gs135", "gs135", "gs136", "gs136", "gs137", "gs137"])
# Cartes mises de cote : la prison (mise en jeu par 1A), le trone (deux faces), les six STARJAMMER (glisses par 1A).
SET_ASIDE = ["gs119", "gs120a,gs120b", "gs121", "gs122", "gs123", "gs124", "gs125", "gs126"]
