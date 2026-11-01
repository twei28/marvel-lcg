from . import *

# Cassandra Domination (environnement). « Forced Response : After a Cassandra Controls counter is placed on your identity card, if there is at
# least 3 Cassandra Controls counter, remove 3 Cassandra Controls counter from it -> you choose one : place 2 threat on each scheme, stun and
# confuse your identity, or deal 3 indirect damage to another friendly character. »
# Cartes de reference : hg `limite_atteinte` (`AfterCounterPlacedOn(... 'infection', at_least=...)` sur une identite), `Player.ChooseAbilities` +
# `ForChoiceAbility(condition=)` (options dynamiques, modele mt011 Psychic Tremor), `Player.AssignDamage` (degats indirects).
# FAQ du livret p.22 : une option IMPOSSIBLE disparait (cible trop fragile, identite deja etourdie ou desorientee) ; la menace reste en dernier.


def GetAbilities() -> Sequence['Ability']:
    def declenchee(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        joueur = message.trigger.GetControlByOrOwner()
        if Player.IsType(joueur):
            Domination(effect, joueur)

    return [
        AbilityFactory.AfterCounterPlacedOn(AbilityType.ForcedResponse, CardFinder(check_face_fn=EstUneIdentite), CTR, declenchee, at_least=3),
    ]
