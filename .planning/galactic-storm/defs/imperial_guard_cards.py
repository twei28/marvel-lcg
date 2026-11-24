# Entrees cards.json du modulaire IMPERIAL GUARD de Galactic Storm (gs091-gs113), lot GS-4 (20/10/2026).
# Texte = docs/packs/galactic-storm/transcriptions/imperial-guard.md, RELU SUR LES SCANS le 20/10/2026.
# card_id = gs + numero IMPRIME (91 a 113), UN card_id par numero (23 cartes, une copie chacune). Hobgoblin est
# imprime « 99 » : `gs099` (Maelstrom de Quasar est `gs099q`).
#
# Lectures faites sur les scans (preuves de decoupe dans le gabarit, IMPERIAL-GUARD-GABARITS.md) :
#  - icones de RESSOURCE dans le texte des sbires, comparees par decoupe aux icones de sk148 / sk152 (mental +
#    physique, energie + physique, ressource declaree) : Electron = eclair = [energy] (Y) ; Nightside = « noeuds
#    relies » = [mental] (B) ; Pulsar = poing = [physical] (R) ; Fang = etoile = [wild] (G, comme l'etoile du coin
#    de sk010, RES=G).
#  - pastille orange = PV ; chevrons rouges en bas a droite = icones de boost (1 a 3) ; etoile de nom (carre a
#    quatre branches) = carte unique (+), nom precede de « * » comme dans les lots precedents.
#  - environnements : aucun cout, `Setup` (la carte entre en jeu a la mise en place).
IG = "Imperial Guard"
WHEN_SPECIAL = ('resolve the "<b>Special</b>" ability on the [[SETTING]] environment.')
SINON = "If you cannot, " + WHEN_SPECIAL
TRAITS_IG = ["IMPERIAL GUARD"]


def c(cid, typ, name, desc, traits, text):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": IG, "text": text, "custom": "Kajislav"}


def sbire(cid, nom, pv, sch, atk, boost, traits, quand_revele, citation, **desc_en_plus):
    desc = {"HP": str(pv), "SCH": str(sch), "ATK": str(atk), "Boost": str(boost)}
    desc.update(desc_en_plus)
    return c(cid, "Minion", "* " + nom, desc, traits, "<b>When Revealed</b>: " + quand_revele + "\n<i>" + citation + "</i>")


APRES_REVELE = "<b>When Revealed</b>: Discard each other [[SETTING]] environment in play."

CARDS = [
    # --- Environnements ------------------------------------------------------------------------------------
    c("gs091", "Environment", "Disciplined Training", {"Setup": "1"}, ["CONDITION", "SETTING"],
      "Setup.\nEach [[IMPERIAL GUARD]] minion gains toughness.\n<b>Special</b>: Deal 1 damage to your identity.\n"
      + APRES_REVELE),
    c("gs092", "Environment", "Loyal Devotion", {"Setup": "1"}, ["CONDITION", "SETTING"],
      "Setup.\nEach [[IMPERIAL GUARD]] minion gains teamwork ([[IMPERIAL GUARD]]).\n"
      "<b>Special</b>: Place 1 threat on the main scheme.\n" + APRES_REVELE),
    c("gs093", "Environment", "Noble Bearing", {"Setup": "1"}, ["CONDITION", "SETTING"],
      "Setup.\nEach [[IMPERIAL GUARD]] minion gains guard and the [[ELITE]] trait.\n"
      "<b>Special</b>: Discard the top 3 cards of the encounter deck.\n" + APRES_REVELE),
    # --- Sbires ---------------------------------------------------------------------------------------------
    sbire("gs094", "Astra", 4, 2, 1, 1, TRAITS_IG,
          "Discard an identity-specific card you control. " + SINON,
          "You will cause no more trouble, mutant, once I reach through you intangibly--then materialize my arm ever so "
          "slightly-just enough to shock your system to its foundations!\""),
    sbire("gs095", "Earthquake", 5, 1, 2, 2, TRAITS_IG,
          "Exhaust your identity. If you were already exhausted, " + WHEN_SPECIAL,
          "I am called Earthquake, mammals...behold the reason why!\""),
    sbire("gs096", "Electron", 5, 1, 2, 2, TRAITS_IG + ["SHI'AR"],
          "Discard a [energy] resource from your hand. " + SINON,
          "Metal projectiles are useless against Electron, cretins...a man who controls magnetic force!\""),
    sbire("gs097", "Fang", 5, 1, 2, 2, TRAITS_IG,
          "Discard a card you control with a printed [wild] resource. " + SINON,
          "In our culture, the warrior title of Fang is won in nigh-mortal combat.\""),
    sbire("gs098", "Gladiator", 8, 1, 3, 3, ["ELITE", "IMPERIAL GUARD"],
          "Defeat a non-scenario specific ally you control. If no ally was defeated this way, " + WHEN_SPECIAL,
          "I would gladly sacrifice your entire galaxy to save the life of a single Shi'ar!\"", Victory="0"),
    sbire("gs099", "Hobgoblin", 4, 3, 1, 2, TRAITS_IG,
          "Resolve a \"<b>When Revealed</b>\" ability of another [[IMPERIAL GUARD]] minion in play. If no ability was "
          "resolved this way, " + WHEN_SPECIAL,
          "I've a bitter lesson for you, my praetor, things are not always what they seem.\""),
    sbire("gs100", "Hussar", 5, 1, 2, 2, TRAITS_IG,
          "Discard an upgrade you control. " + SINON,
          "Ah! Another Terran to humble! I forget your name, but that hardly matters.\""),
    sbire("gs101", "Magique", 4, 2, 2, 1, TRAITS_IG + ["SHI'AR"],
          "Give the villain a tough status card. " + SINON,
          "My spells will keep them from ensnaring me...\""),
    sbire("gs102", "Manta", 4, 2, 2, 2, TRAITS_IG,
          "You are stunned. If you were already stunned, " + WHEN_SPECIAL,
          "You are to be held until a proper trial is scheduled for you.\""),
    sbire("gs103", "Mentor", 4, 3, 1, 1, TRAITS_IG,
          "Discard a player side scheme from play. " + SINON,
          "The Imperial Guard will not allow this travesty to proceed any further.\""),
    sbire("gs104", "Neutron", 5, 1, 2, 2, TRAITS_IG,
          "Discard a support you control. " + SINON,
          "I've a bitter lesson for you, my praetor, things are not always what they seem.\""),
    sbire("gs105", "Nightside", 4, 2, 2, 1, TRAITS_IG,
          "Discard a [mental] resource from your hand. " + SINON,
          "My name, in your primitive tongue, would be... Nightside. Does that give you a hint what my special "
          "power is?\""),
    sbire("gs106", "Oracle", 4, 3, 1, 1, TRAITS_IG,
          "You are confused. If you were already confused, " + WHEN_SPECIAL,
          "If I cannot read your lips, youth...I shall instead read your mind!\""),
    sbire("gs107", "Pulsar", 5, 1, 2, 1, TRAITS_IG,
          "Discard a [physical] resource from your hand. " + SINON,
          "I will kill you extremely slowly for your insolence!\""),
    sbire("gs108", "Smasher", 5, 1, 2, 1, TRAITS_IG,
          "Discard an event from your hand. " + SINON,
          "I am recalling you to serve, Superguardian.\" —Gladiator"),
    sbire("gs109", "Starbolt", 5, 2, 2, 1, TRAITS_IG,
          "Remove 1 all-purpose counter from a card you control. " + SINON,
          "My body was converted to energy. Its physical weaknesses, its... attributes... are no more.\""),
    sbire("gs110", "Titan", 6, 0, 2, 1, TRAITS_IG,
          "Discard a resource card from your hand. " + SINON,
          "Let's see you survive a foot-stomp, little mammal!\""),
    sbire("gs111", "Warstar", 5, 1, 2, 2, TRAITS_IG + ["ROBOT"],
          "Discard the top card of the encounter deck. If that card is an [[IMPERIAL GUARD]] minion, reveal it. "
          "Otherwise, " + WHEN_SPECIAL,
          "Do not struggle, Terran. It merely forces us to increase the force of our grip.\""),
    # --- Traitrises ---------------------------------------------------------------------------------------------
    c("gs112", "Treachery", "Guard Assembles", {"Boost": "1"}, [],
      "<b>When Revealed</b>: Discard cards from the encounter deck until you discard an [[IMPERIAL GUARD]] minion and "
      "reveal it.\n<i>\"I am recalling you to serve, Superguardian. Ready your family and report to the flagship, "
      "Lilandra. I will be waiting for you there.\" —Gladiator</i>"),
    c("gs113", "Treachery", "Imperial Formation", {}, [],
      "<b>When Revealed</b>: Resolve the \"<b>When Revealed</b>\" ability of each [[IMPERIAL GUARD]] minion in play. If "
      "you cannot, search the encounter deck and discard pile for an [[IMPERIAL GUARD]] minion and reveal it.\n"
      "<i>\"You are here to answer for your crimes.\" —Gladiator</i>"),
]

for _carte in CARDS:
    if _carte["card_id"] == "gs098":  # « Victory 0. » est imprime en premiere ligne du texte
        _carte["text"] = "Victory 0.\n" + _carte["text"]

# Citations : les guillemets ouvrants ont ete oublies par `sbire` ; on les rend ici une fois pour toutes.
for _carte in CARDS:
    if _carte["type"] == "Minion":
        _carte["text"] = _carte["text"].replace("\n<i>", "\n<i>\"", 1)

ENVIRONNEMENTS = ["gs091", "gs092", "gs093"]
SBIRES = ["gs094", "gs095", "gs096", "gs097", "gs098", "gs099", "gs100", "gs101", "gs102", "gs103", "gs104", "gs105",
          "gs106", "gs107", "gs108", "gs109", "gs110", "gs111"]
TRAITRISES = ["gs112", "gs113"]
# Le set « Imperial Guard » : 23 cartes ; une fois choisi pour un scenario on n'en garde que NEUF (livret p.8 :
# « one random environment, six random minions, and both treacheries »). Le moteur applique `random_pick` au
# moment de former le deck rencontre (src/game/card/factory.py, `LoadEncounterSet(.., world)`).
ENCOUNTER_SET = {
    "gs_imperial_guard": ("Imperial Guard", ENVIRONNEMENTS + SBIRES + TRAITRISES,
                          [{"from": ENVIRONNEMENTS, "count": 1}, {"from": SBIRES, "count": 6}]),
}
