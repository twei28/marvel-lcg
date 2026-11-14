from . import *

# The Ultimate Hunt (1A) — COMPLOT PRINCIPAL, stade 1.
# Contents: Alien Queen (A) and Predator Warlord (A) (B instead in expert mode). Alien vs. Predator, Xenomorph deck, Apex Standard and one
#   modular encounter set (Clan Yautja).
# Setup: Put Skulls for the Taking and Expanding Hive into play. Place the Xenomorph deck next to Alien Queen and place the active counter
#   on her.
#
# Cartes de reference :
#  - « Contents » : data/scenarios/alien_vs_predator(_expert).json (aucun code) ; les deux mechants sont mis de cote (`villain: []`) et
#    mis en jeu ICI, comme Bebop & Rocksteady (tk005a) et Sinister Six (27100a) ;
#  - « the active counter » : `Villains.SetRule(.., the_villain="Active")` (brique 16.3, fiche mechants-multiples.md) puis
#    `Villains.SetActive` ; seul le mechant actif s'active (arbitrage 1 du 25/10/2026 : `GettingVillain` rend le mechant actif) ;
#  - « Put ... into play » : `SetupCards.PutIntoPlay(name=, card_type=)` (gs161a, vt017a) ;
#  - « Place the Xenomorph deck next to Alien Queen » : les 16 Alien Scout (mis de cote) sont GLISSES SOUS la Reine, face cachee
#    (`TuckCardUnderHere`, fiche tuck.md) : le plateau montre la pile et son nombre.
#
# ⚠ Mots-pieges :
#  - « place the active counter on HER » : la Reine commence ;
#  - « Player cards that refer to "the villain" » : rien d'imprime -> regle par defaut des scenarios a compteur (Sinister Six) : le
#    mechant actif, pour les cartes de rencontre comme pour les cartes joueur.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        Villains.SetRule(effect, Villains.Rule(the_villain="Active", player_cards="TheVillain"))
        joueur = Worlds.GetFirstPlayer(effect)
        de_cote = Worlds.GetSetAsideAreaCards(effect)

        mechants = [f for f in de_cote if Villain.IsType(f) and NomDuMechant(f)]
        mechants.sort(key=lambda f: 0 if f.IsName(REINE) else 1)
        for mechant in mechants:
            mechant.PutIntoPlay(joueur, effect)

        for nom in (SKULLS, HIVE):
            SetupCards.PutIntoPlay(effect, "FirstPlayer", False, name=nom, card_type=EncounterSideScheme)

        reine = MechantNomme(effect, REINE)
        if reine is not None:
            scouts = [f for f in Worlds.GetSetAsideAreaCards(effect) if f.paper.card_id in IDS_SCOUTS]
            if scouts:
                reine.TuckCardUnderHere(scouts, effect)
            Villains.SetActive(reine, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
