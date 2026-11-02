from . import *

# Throne of the Hellfire Club (1A). « Setup : Put Under the Moonlight environment into the play. Set the Darkhold module aside. Shuffle the
# set-aside Darkhold Dwarf into the encounter deck. »
# Cartes de reference : 50087a (Batroc : `SetupCards.PutIntoPlay(name=..., card_type=Environment)` pour un environnement mis de cote par le
# scenario, `*CampaignSetup(n)` pour la campagne), skrull_menace/shaper_of_worlds (`Faces.SetAside` d'un ensemble modulaire).
# Le scenario liste l'environnement recto-verso dans `set_aside` ; le module Darkhold (hf_darkhold) est charge DANS le deck de rencontre avec
# les autres sets : la mise en place en met de cote tout SAUF le Darkhold Dwarf, qui reste dans le deck (« shuffle the set-aside Darkhold
# Dwarf into the encounter deck » : le sbire est donc simplement laisse, le deck est melange apres la mise en place).
# Campagne : `CampaignSetup(3)` (cards.pack.hellfire_hunt.campaign) : allies Recruited, Potential Ally, Emma Frost's Redemption ou
# Cryptic Threatening Message + Emma Frost dans Recruited Mutants, PV experts ; releve du carnet a la victoire.


def GetAbilities() -> Sequence['Ability']:
    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        SetupCards.PutIntoPlay(effect, name=NOM_NUIT, card_type=Environment)
        a_ecarter = [f for f in Worlds.GetEncounterDeckCards(effect)
                     if f.paper.set_name == ENSEMBLE_DARKHOLD and not f.IsName(NOM_DWARF)]
        if a_ecarter:
            Faces.SetAside(a_ecarter, effect)

    return [
        *CampaignSetup(3),
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
