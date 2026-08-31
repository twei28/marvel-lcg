from . import *

# Occult Knowledge — carte Ressource signature ([wild][mental]). x1
# Response: After this card is discarded from the top of your deck, add it
#   to your hand.
#
# Carte de reference : 40060 Digging Deep (pack officiel Cable), texte MOT
# POUR MOT identique — `AfterCardDiscardInternal(Response, "This", ...,
# from_where="PlayerDeckTop")` + `GainCard`. La double icone « GB » est
# portee par `desc.RES` (comme Energy « YY »), rien a scripter pour elle.
#
# ⚠ Synergie voulue avec tout le pack : Power Absorption (aa001a), Wake Thy
# Power (aa004) et Soul Harvest (aa006) defaussent le dessus du deck — la
# carte revient en main a chaque fois qu'elle tombe ainsi.

def GetAbilities() -> Sequence['Ability']:

    def occult_knowledge(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is not None:
            initiator.GainCard(effect.this, effect)

    return [
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.Response,
            "This",
            occult_knowledge,
            from_where="PlayerDeckTop",
        )
    ]
