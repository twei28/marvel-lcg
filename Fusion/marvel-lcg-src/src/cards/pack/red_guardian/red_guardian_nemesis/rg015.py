from . import *

# "I Can't Do It All Day" — traitrise nemesis de Red Guardian
# When Revealed: Choose to either exhaust your identity or discard 1 random
#   card from your hand.
#
# Gabarit : Spider-Woman (madame_web/madame_web_nemesis/mw013), du meme auteur
# custom, meme forme « Choose to either X or exhaust your identity », et Energy
# Drain (spdr/spdr_nemesis/31028) pour la version officielle.
#
# L'epuisement passe par `.SetTarget("YourIdentity", canbe_exhaust=True)` et
# non par un `CostFunc` : c'est un EFFET de l'option, pas un cout. Le filtre
# `canbe_exhaust` fait aussi le tri d'eligibilite — identite deja epuisee, pas
# de cible legale, `ChooseEffects` retire l'option de la liste. Le joueur doit
# alors prendre la seconde, ce qui est la regle officielle du choix (« you must
# choose an option that you can fulfill »).


def GetAbilities() -> Sequence['Ability']:

    def i_cant_do_it_all_day(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity",
                lambda targets:
                    Faces.ExhaustAll(targets, effect),
            ).SetTarget("YourIdentity", canbe_exhaust=True),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 random card from your hand",
                lambda targets:
                    joueur.DiscardRandomHandCards(1, effect),
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            i_cant_do_it_all_day,
        ),
    ]
