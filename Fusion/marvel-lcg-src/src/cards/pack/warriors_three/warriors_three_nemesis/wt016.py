from . import *


def GetAbilities() -> Sequence['Ability']:
    def questing(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        paquet = Worlds.GetEncounterDeck(effect)
        sbires = [f for f in paquet.GetAll() if Minion.IsType(f)]
        if not sbires:
            ThisCardGainSurge(effect)
        else:
            sbire = sbires[-1]          # « bottommost » : la derniere carte du deck

            def attacher() -> None:
                this.AttachTo2(sbire, effect)

            # « Reveal it, then attach this card to it » : le sbire entre en jeu, puis la carte s'attache a LUI (inventaire du sbire :
            # elle le suit, et disparait avec lui). Les trois bonus viennent de `GiveKeywordToAttached`, plus de pose directe.
            sbire.Reveal(joueur, effect, if_entered_play=attacher)
        paquet.Shuffle(effect)

    return [
        # « The attached minion gets +5 hit points and gains steady and the ELITE trait ».
        *AbilityFactory.GiveKeywordToAttached(Minion, health=5, steady=1, trait="ELITE"),
        AbilityFactory.WhenThisObligationGiveToYou(questing),
    ]
