from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# The Raft Breakout 1A
# Setup: Attach Master Key to the villain. Each player discards cards from
#   the encounter deck until they discard a PRISONER minion and reveal that
#   minion.
# Master Key est dans la mise de cote du scenario (Find.FindAndAttachTo).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        vilain = Worlds.FindVillain(effect)
        premier = Worlds.GetFirstPlayer(effect)
        if vilain is not None:
            Find.FindAndAttachTo(effect, vilain, who_perform=premier, name="Master Key", card_type=Attachment)

        def evasion(player: 'Player') -> None:
            face = Worlds.DiscardEncounterCardsUntil(effect, trait="PRISONER", card_type=Minion)
            if face is not None:
                face.Reveal(player, effect)

        Players.ForEachPlayer(effect, evasion)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("the_raft_breakout"),
    ]
