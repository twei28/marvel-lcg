from . import *


def GetAbilities() -> Sequence['Ability']:

    def forceful(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        tough_count = len(effect.targets)
        Faces.DiscardAll(effect.targets, effect)
        villain = Worlds.FindVillain(effect)
        if villain and tough_count:
            this.DealDamage([villain], 3 * tough_count, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            forceful,
        ).SetPlay(only_if_your_identity_has_trait="PSIONIC")
        .SetLabel("attack")
        # CORRECTIF (4/8/2026) : `from_where=["YouControlCards"]` rendait la
        # carte INJOUABLE. Les cartes de statut ne figurent jamais dans cette
        # liste (qui contient identite, allies, ameliorations, soutiens) :
        # l'intersection etait toujours vide. `bind_to` est le mecanisme prevu
        # pour restreindre un statut au personnage qui le porte.
        .SetTarget(StatusCard, name="Tough", bind_to=CardFinder(card_type=Friend),
                   range=(1, "All"))
        .SetName("Forceful"),
    ]
