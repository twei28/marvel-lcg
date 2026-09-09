from . import *

# Symbiotic Perseverance — EVENEMENT, cout 1, RES [mental]. SYMBIOTE. TACTIC.
# Hero Response: After you change form, give your hero a tough status card.
#
# CARTE DE REFERENCE
#  - `13033` Perseverance (Protection, pack wsp) : meme cout, meme ressource,
#    meme texte. Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ `canbe_tough=True` sur la cible : sans lui le moteur ecarterait une
#    identite qui porte deja un statut Tough, alors que le texte ne l'interdit
#    pas.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_perseverance(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            symbiotic_perseverance
        ).SetPlay().SetLabel()
        .SetTarget("YourIdentity", canbe_tough=True),
    ]
