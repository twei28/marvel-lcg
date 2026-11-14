# Definitions des cartes THE VAULT (Kajislav, « MC Custom Content By: Kajislav »), 25/10/2026.
# Relues une a une contre les scans (zip « The Vault (Sealed) », 51 images dont 13 doublons de la rencontre).
# Transcriptions : docs/packs/vault/TRANSCRIPTIONS.md. Icones identifiees par COMPARAISON AVEC LES GLYPHES de
# public/fonts/ChampionsIcons.ttf (mots-cles/hazard.md) : Burglary = Crisis (C), Scheming from Within et
# Contingency Measures = Hazard (H), ressource de Inspection of the Vault = mentale (M, noeuds relies).
# Doublons du zip : Craven Escape 20-21, Corrupted Guardsman 22-25, Burglary 26-27, Rampage in Public 30-33,
# Riot in the Vault 34-36 : UNE carte, plusieurs exemplaires (numero imprime le plus bas).
# Inseres dans data/cards.json par inserer_vault.py (idempotent).

K = "Kajislav"
SET = "The Vault"


def ordre(n):
    return f"<b>Activation Order {n}</b>\n"


CONSEQ = ("<b>Forced Response</b>: After you attack {nom} with a card you control, choose to either {choix} "
          "or place 1 threat on the main scheme.")


def vilain(cid, nom, stade, hp, atk, sch, n, avant, choix, citation, extra=None, **mots):
    desc = {"HP": f"{hp}*", "ATK": str(atk), "SCH": str(sch), "Stage": str(stade), "ActivationOrder": str(n)}
    desc.update(mots)
    texte = ordre(n)
    if mots.get("Stalwart") or mots.get("Toughness"):
        texte += "Stalwart. Toughness.\n"
    if avant:
        texte += avant + "\n"
    texte += CONSEQ.format(nom=nom, choix=choix)
    if citation:
        texte += f"\n<i>\"{citation}\"</i>"
    return {"card_id": cid, "type": "Villain", "name": f"* {nom}", "subtitle": "", "desc": desc, "traits": [],
            "set_name": SET, "text": texte, "custom": K}


CARDS = [
    vilain("vt001", "Batroc", 1, 7, 2, 1, 1, "", "discard the top 3 cards of the encounter deck",
           "Sacre Bleu! You are fastaire than ever Avengaire."),
    vilain("vt002", "Batroc", 2, 8, 3, 1, 1, "<b>When Revealed</b>: Each player discards the top 5 cards of their deck.",
           "discard the top 3 cards of the encounter deck", "Sacre Bleu! You are fastaire than ever Avengaire."),
    vilain("vt003", "Mentallo", 1, 7, 1, 2, 2, "", "exhaust your identity",
           "Funny how hallucinations can sometimes seem so real."),
    vilain("vt004", "Mentallo", 2, 8, 2, 2, 2, "<b>When Revealed</b>: Each player exhausts a character they control.",
           "exhaust your identity", "Funny how hallucinations can sometimes seem so real."),
    vilain("vt005", "Grey Gargoyle", 1, 7, 2, 1, 3, "", "stun the attacker", "Forgive me for not shaking hands, sir..."),
    vilain("vt006", "Grey Gargoyle", 2, 8, 3, 1, 3, "<b>When Revealed</b>: Each player stuns a character they control.",
           "stun the attacker", "Forgive me for not shaking hands, sir..."),
    vilain("vt007", "Hydro-Man", 1, 7, 2, 1, 4, "", "deal 1 damage to each character you control",
           "...all I gotta do is 'tsunami' that stupid wallcrawler..."),
    vilain("vt008", "Hydro-Man", 2, 8, 2, 2, 4, "<b>When Revealed</b>: Deal 1 damage to each friendly character.",
           "deal 1 damage to each character you control", None),
    vilain("vt009", "Mad Thinker", 1, 7, 0, 3, 5, "", "place 1 threat on each side scheme", "I plan for every eventuality!"),
    vilain("vt010", "Mad Thinker", 2, 8, 1, 3, 5,
           "<b>When Revealed</b>: Place 1 threat on the main scheme for each enemy in play.",
           "place 1 threat on each side scheme", None),
    vilain("vt011", "Nekra", 1, 7, 2, 1, 6, "", "give Nekra 1 facedown boost card", "Nekra needs no one's help!!"),
    vilain("vt012", "Nekra", 2, 8, 3, 1, 6, "<b>When Revealed</b>: Give each villain 1 facedown boost card.",
           "give Nekra 1 facedown boost card", None),
    vilain("vt013", "Vapor", 1, 7, 1, 2, 7, "", "confuse the attacker", "...you cannot strike one whose form you cannot touch!"),
    vilain("vt014", "Vapor", 2, 8, 2, 2, 7, "<b>When Revealed</b>: Each player confuses a character they control.",
           "confuse the attacker", "...you cannot strike one whose form you cannot touch!"),
    vilain("vt015", "Venom", 1, 7, 2, 1, 8, "", "heal 1 damage from him",
           "The Vault can't hold us, punk! We've broken out of here twice already!"),
    vilain("vt016", "Venom", 2, 8, 2, 2, 8, "", "heal 1 damage from him",
           "The Vault can't hold us, punk! We've broken out of here twice already!", Stalwart="1", Toughness="1"),

    {"card_id": "vt017a", "type": "MainScheme", "name": "The Vault Breakout", "subtitle": "",
     "desc": {"Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<b>Contents</b>: All villains (I) <i>(stages (II) instead for expert mode)</i>. The Vault and Standard encounter sets. One modular encounter set <i>(Sinister Syndicate)</i>.\n"
             "<b>Setup</b>: Create the Villain deck <i>(see insert)</i>. Put The Vault environment into play. Then, place the top 4 villain cards and each player's nemesis ([unique]) minion beneath it facedown. "
             "Set the Inspection of the Vault obligation aside, out of play.", "custom": K},
    {"card_id": "vt017b", "type": "MainScheme", "name": "The Vault Breakout", "subtitle": "",
     "desc": {"StartingThreat": "1*", "TargetThreat": "6*", "EscalationThreat": "1*", "Stage": "1"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Reveal the top card of the villain deck.\n"
             "[star] <b>Forced Interrupt</b>: When this scheme would be completed, instead do each of the following:\n"
             "1. Remove all but 1[per_hero] threat from here.\n2. Reveal 1 random villain beneath The Vault.\n3. Reveal Inspection of the Vault.", "custom": K},
    {"card_id": "vt018", "type": "Environment", "name": "* The Vault", "subtitle": "",
     "desc": {}, "traits": ["LOCATION"], "set_name": SET,
     "text": "<b>Forced Response</b>: After a unique minion ([unique]) is defeated, place it beneath The Vault facedown.\n"
             "<b>If no villain is beneath The Vault, the players lose the game.</b>\n"
             "<b>If all the villains are either beneath The Vault or defeated, the players win the game.</b>", "custom": K},
    {"card_id": "vt019", "type": "Obligation", "name": "Inspection of the Vault", "subtitle": "",
     "desc": {"GiveTo": ""}, "traits": [], "set_name": SET,
     "text": "<b><i>Give to the first player.</i></b>\n<b>Alter-Ego Action</b>: Exhaust your identity and spend a [mental] resource → set this card aside, out of play.\n"
             "<i>\"You've got security measures in here that they've given me a stack of books to help me understand.\"</i> —Warden", "custom": K},

    {"card_id": "vt020", "type": "Attachment", "name": "Craven Escape", "subtitle": "",
     "desc": {"Boost": "2"}, "traits": [], "set_name": SET,
     "text": "Attach to the villain with the fewest remaining hit points and without another Craven Escape attached. If you cannot, this card gains surge.\n"
             "<b>Forced Response</b>: After the player phase ends, shuffle attached villain into the villain deck.\n"
             "<i>\"How you survived isn't important! That you survived is!\"</i> —Venom", "custom": K},
    {"card_id": "vt022", "type": "Minion", "name": "Corrupted Guardsman", "subtitle": "",
     "desc": {"HP": "4", "ATK": "3", "SCH": "1", "Boost": "1", "Incite": "1"}, "traits": ["TRAITOR"], "set_name": SET,
     "text": "Incite 1.\n<b>When Revealed</b>: If Inspection of the Vault is in play, reveal 1 random minion beneath The Vault. If you cannot, this card gains surge.\n"
             "[star] <b>Boost</b>: Shuffle 1 minion beneath The Vault into the encounter deck.", "custom": K},
    {"card_id": "vt026", "type": "SideScheme", "name": "Burglary", "subtitle": "",
     "desc": {"Boost": "2", "Crisis": "1", "StartingThreat": "2*"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: If Inspection of the Vault is in play, place 1[per_hero] additional threat here.\n"
             "<b>When Defeated</b>: Reveal the top card of the villain deck.", "custom": K},
    {"card_id": "vt028", "type": "SideScheme", "name": "Contingency Measures", "subtitle": "",
     "desc": {"Boost": "3", "StartingThreat": "2*"}, "traits": [], "set_name": SET,
     "text": "<i>\"Since I can't bend you to my will... I'm afraid I will have to break you!\"</i> —Senso\n"
             "<b>Forced Interrupt</b>: When a villain would be defeated, shuffle it into the villain deck instead.\n"
             "While Inspection of the Vault is in play, this card gains a hazard icon ([hazard]).", "custom": K},
    {"card_id": "vt029", "type": "SideScheme", "name": "Scheming from Within", "subtitle": "",
     "desc": {"Boost": "1", "Hazard": "1", "StartingThreat": "2*"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: Place 1 additional threat here for each villain beneath The Vault.\n"
             "[star] <b>Boost</b>: If Inspection of the Vault is in play, this card gets +1 boost icon ([boost]) for each villain beneath The Vault.", "custom": K},
    {"card_id": "vt030", "type": "Treachery", "name": "Rampage in Public", "subtitle": "",
     "desc": {"Boost": "2"}, "traits": [], "set_name": SET,
     "text": "<b>When Revealed</b>: If the number of villains in play is less than the number of players, this card gains surge. "
             "Reveal the top card of the villain deck. If you cannot, the villain with the highest activation order value activates against you.", "custom": K},
    {"card_id": "vt034", "type": "Treachery", "name": "Riot in the Vault", "subtitle": "",
     "desc": {"Boost": "1", "Surge": "1"}, "traits": [], "set_name": SET,
     "text": "Surge.\n<b>When Revealed</b>: If Inspection of the Vault is not in play, reveal it. Otherwise, place 1 threat on the main scheme for each villain beneath The Vault.\n"
             "<i>\"No prison can hold a mind such as mine.\"</i> —Mad Thinker", "custom": K},
]
