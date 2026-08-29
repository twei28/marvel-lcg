from . import *

# Song of Leadership
# SONG.
# Max 2 per deck.
# Hero Action: Exhaust an ally -> heal damage from that ally equal to the
#   amount of SONG cards in your discard pile (to a maximum of 4).
#
# L'allie epuise EST l'allie soigne. Le lien se fait par le COUT, pas par une
# cible : `CostFunc.Exhaust("YourAlly")` choisit l'allie, et l'operation relit
# `return_exhausted_cards` pour le soigner. C'est l'idiome officiel, celui de
# Teamwork (Cyclope 33017, Thor 06032).
#
# ATTENTION, piege paye en partie reelle : `CostFunc.Exhaust("Targets")` avec
# un `SetTarget` a cote ne marche PAS. Le selecteur « Targets » lit
# `effect.bind_message.targets`, or le cout est evalue AVANT que la cible soit
# choisie, sur un `WhenPlayerInTurn` qui n'est pas un `TargetsMessage` :
# `assert isinstance(effect.bind_message, TargetsMessage)` pete des la
# verification de jouabilite (selector_target_helper.py:122), donc la carte
# n'etait meme pas proposable.


def GetAbilities() -> Sequence['Ability']:

    def chant_de_commandement(effect: 'Effect',
                              message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        epuises = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        valeur = SongsDansLaDefausseBornee(effect)
        if epuises and valeur > 0:
            this.HealthUnits(epuises, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chant_de_commandement,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust("YourAlly")),
    ]
