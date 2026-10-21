# Cas test_capacites du set PUNISHER'S ARMORY (pack MC×DC 2026), PU-3. Prefixe `[arm]`.
# Montage : scenario `protection_racket_jigsaw` (Jigsaw, vilain en jeu : l'arme s'y attache faute de Punisher), Spider-Man en HEROS.
SC = "protection_racket_jigsaw"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _a(nom, pourquoi, mise, declencher, attendu, **cle):
    deck = cle.pop("deck", ["01105"] * 4)
    cas = {"nom": "[arm] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck), HEROS, *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


ALLIE = ["Puzzle.PutIntoPlay('01075', under_control=True)"]
CAS = [
    # ---- pu115 Shotgun
    _a("pu115 Shotgun : attache au vilain faute de Punisher, entre avec 2 compteurs ammo (solo)",
       "« Attach to Punisher. Otherwise, attach to the villain. Uses (2[per hero] ammo counters) »",
       ["Puzzle.PutIntoPlay('pu115')"], [], {"accroche_a": [["pu115", "pu056a"]], "compteurs": [["pu115", "ammo", 2]]}),
    _a("pu115 When Revealed : Reveal d'une autre ARMAMENT (Sniper pu116) en jeu -> elle est defaussee",
       "« Discard each other ARMAMENT card in play »",
       ["Puzzle.PutIntoPlay('pu116')"], ["Puzzle.Reveal('pu115')"], {"hors_jeu": ["pu116"], "en_jeu": ["pu115"]}),
    _a("pu115 Forced Response : Jigsaw (arme attachee) attaque le heros -> 1 compteur ammo retire et le heros (cible) etourdi",
       "« remove 1 ammo counter from here and stun the attack's target »",
       ["Puzzle.PutIntoPlay('pu115')"], ["Puzzle.EnemyAttacks('pu056a', '01001a')"],
       {"compteurs": [["pu115", "ammo", 1]], "statuts": [["01001a", "Stunned"]]}, **SANS_DEFENSE),
    # ---- pu116 Sniper
    _a("pu116 Sniper : entre avec 1+1 = 2 compteurs ; l'attaque de Jigsaw gagne piercing (allie Tenace : il meurt)",
       "« Attached character's attacks gain piercing and ranged »",
       ["Puzzle.PutIntoPlay('pu116')", *ALLIE, "Puzzle.Tough('01075')"], ["Puzzle.EnemyAttacks('pu056a', '01075')"],
       {"hors_jeu": ["01075"], "compteurs": [["pu116", "ammo", 1]]}, **SANS_DEFENSE),
    # ---- pu117 SMG
    _a("pu117 SMG : apres l'attaque, chaque joueur inflige 1 degat a un personnage qu'il controle, 1 compteur retire",
       "« each player deals 1 damage to a character they control. Remove 1 ammo counter »",
       ["Puzzle.PutIntoPlay('pu117')", *ALLIE], ["Puzzle.EnemyAttacks('pu056a', '01075')"],
       {"compteurs": [["pu117", "ammo", 1]], "degats_identite": 1}, **SANS_DEFENSE),
    # ---- pu118 Frag Grenade
    _a("pu118 Frag Grenade : sans carte a defausser, 3 degats indirects sur le heros",
       "« Take 3 indirect damage »", [], ["Puzzle.Reveal('pu118')"], {"degats_identite": 3}),
    _a("pu118 Frag Grenade : on defausse un soutien (Aunt May, cout 1) -> 3 - 1 = 2 degats indirects",
       "« discard a card you control to prevent X of this damage, where X is that card's cost »",
       ["Puzzle.PutIntoPlay('01006', under_control=True)"], ["Puzzle.Reveal('pu118')"],
       {"degats_identite": 2, "hors_jeu": ["01006"]}),
    # ---- pu114 Armory
    _a("pu114 Forced Response : debut de la phase du vilain, pas d'arme sur le vilain -> defausse jusqu'a une WEAPON (pu115), revelee et attachee",
       "« discard from the encounter deck until a WEAPON is discarded. Reveal that card »",
       ["Puzzle.PutIntoPlay('pu114')"], ["Puzzle.BeginVillainPhase()"],
       {"en_jeu": ["pu115"], "accroche_a": [["pu115", "pu056a"]]}, deck=["pu115", "01105"]),
    _a("pu114 TEMOIN : une arme DEJA attachee au vilain -> aucune carte defaussee, rien de revele (pu116 reste dans le deck)",
       "« if there is no WEAPON attachment on the villain »",
       ["Puzzle.PutIntoPlay('pu115')", "Puzzle.PutIntoPlay('pu114')"], ["Puzzle.BeginVillainPhase()"],
       {"dans_deck_rencontre": ["pu116"], "hors_jeu": ["01105"]}, deck=["pu116", "01105"]),
    _a("pu114 When Defeated : les WEAPON de la defausse de rencontre (pu115) retournent dans le deck",
       "« Shuffle each WEAPON in the encounter discard pile into the encounter deck »",
       ["Puzzle.CreateEncounterDiscardPile('pu115')", "Puzzle.PutIntoPlay('pu114')", "Puzzle.SetThreat('pu114', 1)"],
       ["Puzzle.Thwart('01001a')"], {"dans_deck_rencontre": ["pu115"]}),
]
