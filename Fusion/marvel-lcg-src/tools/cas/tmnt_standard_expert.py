# Cas test_capacites des ensembles TMNT STANDARD / EXPERT (pack `tmnt_standard_expert`, prefixe `te`) :
# prefixe « [tmnt-se] ». Heros de test : Spider-Man (01001), dont le set nemesis est Vulture 01167 (sbire,
# Coup Rapide), Highway Robbery 01166 (complot annexe), Sweeping Swoop 01168 x2 et The Vulture's Plans 01169.
# Scenario `shredder` (le deck rencontre est vide ou pose a la main).
#
# ⚠ te001, te002, te103 « DAZE » : la carte d'etat Dazed est livree par le pack du vilain Baxter Stockman
# (autre agent) ; les cas `[tmnt-se-dazed]` ne peuvent passer qu'APRES la fusion (voir le gabarit).
HEROS = "Puzzle.ChangeForm('01001b')"
INCLINE = "Puzzle.Exhaust('01001a')"
BASE = ["Puzzle.RemoveMinionsInPlay()", "Puzzle.EmptyEncounterDeck()"]
SANS_CLOAK = "Puzzle.Cloak('ts001')"
SC = "shredder"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[tmnt-se] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "shredder_etat"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ---------------------------------------------------------------- TMNT Standard
    _c("te004 Pursued by Shadows : le sbire nemesis est cherche, revele et CAMOUFLE (pas de Renfort)",
       "« Search ... for your nemesis minion and reveal it. Cloak your nemesis minion »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('te004')"],
       {"en_jeu": ["01167"], "cloaked": [["01167", 1]], "dans_deck_rencontre": ["01105"]}),
    _c("te004 Pursued by Shadows : nemesis DEJA en jeu -> il est camoufle et la carte gagne Renfort",
       "« If your nemesis minion did not enter play this way, this card gains surge »",
       BASE + [SANS_CLOAK, "Puzzle.RemoveNemesisAside()", "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.PutIntoPlay(Puzzle.CreateCard('01167'))", "Puzzle.Reveal('te004')"],
       {"cloaked": [["01167", 1]], "carte_du_surge": "01105"}),
    _c("te005 Shadow of the Past : sbire ET complot annexe nemesis reveles, le reste du set melange au deck",
       "texte identique au core 01190",
       BASE + [SANS_CLOAK], ["Puzzle.Reveal('te005')"],
       {"en_jeu": ["01167", "01166"], "dans_deck_rencontre": ["01168", "01169"]}),
    _c("te005 Shadow of the Past, sans sbire nemesis : la carte gagne Renfort",
       "« If your nemesis minion does not enter the game this way, this card gains surge »",
       BASE + [SANS_CLOAK, "Puzzle.RemoveNemesisAside()", "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Reveal('te005')"], {"carte_du_surge": "01105"}),
    _c("te006 Skulk : 2 degats indirects au joueur ET le vilain est camoufle",
       "« Take 2 indirect damage and cloak the villain »",
       BASE + [SANS_CLOAK, HEROS], ["Puzzle.Reveal('te006')"],
       {"degats_identite": 2, "cloaked": [["ts001", 1]]}, cibles=["01001a", "01001a"]),
    _c("te006 Skulk Boost : la carte est donnee face cachee au premier joueur",
       "« Deal this card to the first player as a facedown encounter card »",
       BASE + [SANS_CLOAK], ["Puzzle.Boost('te006')"], {"distribuees": [[0, ["te006"]]]}, main_exclusive=["01088"]),
    # ---------------------------------------------------------------- TMNT Expert
    _c("te101 Annihilation : le vilain attaque et l'attaque gagne OVERKILL (Maria Hill HP 2, 1 degat : excedent sur le heros)",
       "« The villain attacks you. That attack gains overkill »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')",
               "Puzzle.PutIntoPlay('01067', under_control=True)", "Puzzle.Damage('01067', 1)"],
       ["Puzzle.Reveal('te101')"], {"degats_identite": 1, "hors_jeu": ["01067"]}, main_exclusive=["01088"]),
    _c("te101 Annihilation Boost : si le vilain attaque, l'attaque gagne OVERKILL (3 contre Maria Hill HP 2)",
       "« If the villain is attacking, this attack gains overkill » ; ATQ 2 + 2 icones = 4, excedent 2",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.PutIntoPlay('01067', under_control=True)",
               "Puzzle.CreateEncounterDeck('te101')"],
       ["Puzzle.Attack('ts001', defender='01067')"], {"degats_identite": 2, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("te101 Annihilation Boost, TEMOIN : un boost sans overkill (Foot Soldiers) : pas d'excedent",
       "contre-cas", BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.PutIntoPlay('01067', under_control=True)",
                              "Puzzle.CreateEncounterDeck('ts303')"],
       ["Puzzle.Attack('ts001', defender='01067')"], {"degats_identite": 0, "hors_jeu": ["01067"]},
       main_exclusive=["01088"]),
    _c("te102 Haunted by the Past : le sbire nemesis est cherche et mis en jeu engage avec le joueur",
       "« ...put it into play engaged with you »",
       BASE + [SANS_CLOAK, HEROS], ["Puzzle.Reveal('te102')"], {"en_jeu": ["01167"], "engages": [[0, 1]]},
       main_exclusive=["01088"]),
    _c("te102 Haunted by the Past, sans sbire nemesis : identite epuisee ET Renfort",
       "« exhaust your identity and this card gains surge »",
       BASE + [SANS_CLOAK, "Puzzle.RemoveNemesisAside()", "Puzzle.CreateEncounterDeck('01105')"],
       ["Puzzle.Reveal('te102')"], {"exhausted": ["01001b"], "carte_du_surge": "01105"}),
    # ---------------------------------------------------------------- Habillages (ability_link vers le core)
    _c("te021 Advance (habillage de 01186) : le vilain manigance (1 menace de plus sur 1B)",
       "meme texte, memes capacites (`ability_link`)",
       BASE + [SANS_CLOAK, "Puzzle.SetThreat('ts004b', 0)"], ["Puzzle.Reveal('te021')"],
       {"menace": [["ts004b", 1]]}, main_exclusive=["01088"]),
    _c("te023 Assault (habillage de 01187), forme heros : le vilain attaque",
       "« When Revealed (Hero): The villain attacks you »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('te023')"],
       {"degats_identite": 2}, main_exclusive=["01088"]),
    _c("te023 Assault, alter-ego : la carte gagne Renfort",
       "« When Revealed (Alter-Ego): This card gains surge »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('te023')"],
       {"carte_du_surge": "01105"}, main_exclusive=["01088"]),
    _c("te025 Caught Off Guard (habillage de 01188) : une amelioration controlee est defaussee",
       "« Discard an upgrade or support you control »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('04002', under_control=True)"], ["Puzzle.Reveal('te025')"],
       {"hors_jeu": ["04002"]}, main_exclusive=["01088"]),
    _c("te026 Gang-Up (habillage de 01189), forme heros : le vilain ET chaque sbire engage attaquent (2 + 1 = 3)",
       "« The villain and each minion engaged with you attacks you »",
       BASE + [SANS_CLOAK, HEROS, INCLINE, "Puzzle.CreateEncounterDeck('01105', '01105')",
               "Puzzle.PutIntoPlay('01101')"], ["Puzzle.Reveal('te026')"],
       {"degats_identite": 3}, main_exclusive=["01088"]),
    _c("te027 Shadow of the Past (habillage de 01190) : sbire ET complot annexe nemesis",
       "meme texte que te005", BASE + [SANS_CLOAK], ["Puzzle.Reveal('te027')"],
       {"en_jeu": ["01167", "01166"]}),
    _c("te121 Exhaustion (habillage de 01191) : identite epuisee + Renfort",
       "« Surge. When Revealed: Exhaust your identity card »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105')"], ["Puzzle.Reveal('te121')"],
       {"exhausted": ["01001b"], "carte_du_surge": "01105"}),
    _c("te122 Masterplan (habillage de 01192) : 4 menaces sur chaque complot annexe",
       "« Place 4 threat on each side scheme »",
       BASE + [SANS_CLOAK, "Puzzle.PutIntoPlay('ts305')", "Puzzle.SetThreat('ts305', 0)"], ["Puzzle.Reveal('te122')"],
       {"menace": [["ts305", 4]]}),
    _c("te123 Under Fire (habillage de 01193) : Renfort + revele la carte du dessus du deck",
       "« Surge. When Revealed: Reveal the top card of the encounter deck »",
       BASE + [SANS_CLOAK, "Puzzle.CreateEncounterDeck('01105', '01105', '01105')"], ["Puzzle.Reveal('te123')"],
       {"taille_deck_rencontre": 1}),
    # ---------------------------------------------------------------- DAZED : bloques jusqu'a la fusion
    _c("te001 [dazed] No Quarter : sans amelioration ni soutien, l'identite est hebetee (Dazed)",
       "« If no cards were discarded this way, daze your identity »",
       BASE + [SANS_CLOAK], ["Puzzle.Reveal('te001')"], {"statuts": [["01001b", "Dazed"]]}),
    _c("te002 [dazed] Outmatched : l'identite est hebetee",
       "« When Revealed: Daze your identity »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('te002')"],
       {"statuts": [["01001b", "Dazed"]]}),
    _c("te103 [dazed] Sinister Plan : complot annexe nemesis revele ET identite hebetee",
       "« reveal it. Daze your identity »", BASE + [SANS_CLOAK], ["Puzzle.Reveal('te103')"],
       {"en_jeu": ["01166"], "statuts": [["01001b", "Dazed"]]}),
]
