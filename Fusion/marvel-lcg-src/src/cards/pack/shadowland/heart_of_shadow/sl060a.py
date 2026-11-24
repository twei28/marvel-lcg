from . import *
from cards.pack.shadowland.campaign import CampaignSetup

# Dark Invitation (1A) — MANIGANCE PRINCIPALE, stade 1.
# Contents : Krahllak (I) and Krahllak (II). (Krahllak (II) and Krahllak (III) instead for expert mode.) Heart of Shadow, Black Flower, and Standard encounter sets. One
#   modular encounter set (Ninja Swarm).
# Setup : Each player puts a Creeping Corruption upgrade into play. Set the rest aside.
#
# Cartes de reference : sl001a (Setup d'une face 1A : `WhenCardSetup("This")` + `SetupCards.PutIntoPlay`, les cartes de depart sont DEJA mises de cote par le scenario),
# fne/kingpin/60161b (`SetupCards.PutIntoPlay(effect, joueur, name=...)` pour un joueur donne), galactic_storm/kree_sentry/gs079a (`under_control=True`).
# ⚠ Mots-pieges : « EACH player puts A Creeping Corruption » : UNE par joueur, SOUS SON controle (sinon « your Creeping Corruption » ne designerait personne) ; `PutIntoPlay` n'en
#  met qu'une par appel ; « set the rest aside » : les autres exemplaires (4 en tout) restent de cote, c'est deja leur etat de depart ; « Contents » : composition, portee par
#  data/scenarios/heart_of_shadow*.json (vilains Krahllak I-II ou II-III, sets Heart of Shadow + Black Flower + Standard).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)

        def une_pour_chacun(joueur: 'Player') -> None:
            SetupCards.PutIntoPlay(effect, joueur, True, name='Creeping Corruption', card_type=Upgrade)

        Players.ForEachPlayer(effect, une_pour_chacun)

    return [
        AbilityFactory.WhenCardSetup('This', mise_en_place),
        # Campagne (livret FR) : le niveau est le numero du scenario dans `data/campagnes/shadowland.json`.
        *CampaignSetup(3),
    ]
