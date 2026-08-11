from . import *
from cards.pack.aos.campaign import CampaignSetup

# Zemo's Manipulations

def GetAbilities() -> Sequence['Ability']:

    def zemos_manipulations(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        # Prepare the evidence <i>(see rulebook p. 18)</i>.

        # During setup, when you are instructed to prepare the
        # evidence:
        # » If you are not playing in campaign mode, follow the
        # steps under “Preparing the Evidence” on page 5.
        # » If you are playing in campaign mode, simply place the
        # A.I.M. and S.H.I.E.L.D. envelopes within reach.

        # CORRECTIF, divergence volontaire du bytecode d'origine. L'assert qui
        # etait ici interdisait purement et simplement le mode campagne : la
        # boite n'en avait pas. Le commentaire ci-dessus dit deja quoi faire,
        # et c'est ce qu'on fait maintenant. En campagne, les enveloppes et les
        # membres du Conseil viennent du scenario precedent, et CampaignSetup(5)
        # a deja pose les membres avec leurs compteurs secrets ; preparer les
        # preuves ici les reposerait a neuf, avec deux secrets chacun.
        if Worlds.IsCampaign(effect):
            return

        # Put each [[Board Member]] environment into play.
        # If not playing campaign mode, place 2 secret counters on each [[Board Member]] environment.

        PreparingTheEvidence(effect)

    return [
        *CampaignSetup(5),
        AbilityFactory.WhenCardSetup(
            "This",
            zemos_manipulations
        ),
    ]

