# Cas test_capacites de gs168 Portal to the Negative Zone (Earth Under Siege, ensemble Annihilus, lot
# GS-7). Filtre `[eus] gs168`. Voir .planning/galactic-storm/EARTH-UNDER-SIEGE-GABARITS.md pour pourquoi
# gs166/gs167/gs169 (meme ensemble) n'ont pas de cas equivalent.

CAS = [
    {
        "nom": "[eus] gs168 vaincue : chaque joueur avec une carte identitaire en defausse peut la "
               "remelanger dans son deck",
        "pourquoi": ("« When Defeated: Each player may shuffle 1 identity-specific card from their "
                     "discard pile into their deck » : WhenSchemeBeDefeated(ForcedInterrupt, ..) + "
                     "AskChooseFace + ShuffleAllTo. 01005 Webbed Up (Hero = identitaire) est deja en "
                     "defausse via le mulligan de depart, pas besoin de le mettre a la main"),
        "scenario": "rhino", "heros": "spider_man",
        "mise_en_place": ["Puzzle.RemoveVillain('01094')", "Puzzle.SetVillainRule('Leftmost', 'PlayerChooses')",
                           "Puzzle.PutIntoPlay('gs166')", "Puzzle.PutIntoPlay('gs168')"],
        "declencher": ["Puzzle.SetThreat('gs168', 0)"],
        "verifier": "etat_attendu",
        "attendu": {"dans_deck_joueur": ["01005"]},
    },
]
