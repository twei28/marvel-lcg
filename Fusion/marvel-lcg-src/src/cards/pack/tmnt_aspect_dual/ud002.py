from . import *

# * Doomsayer (Donnie) — ALLIE double aspect Aggression/Leadership (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 1 / ATK 2 (1 degat consecutif chacun), ressource [energy].
#
# Response: After Doomsayer enters play, draw X cards (to a maximum of 3), where X is equal
#   to the villain's stage number.
# Interrupt: When Doomsayer is defeated by consequential damage ([consequential]), draw 1 card
#   for each minion engaged with you.
#
# Cartes de reference :
#  - « draw X cards (to a maximum of 3), where X is equal to the villain's stage number » :
#    21013 White Tiger (`Worlds.GetVillainStage`, `Math.MinMax`). ⚠ White Tiger a une clause
#    « If the villain has no stage number, draw 1 card » (d'ou son minimum a 1) : Doomsayer NE
#    l'imprime PAS, son minimum est donc 0 ;
#  - « After X enters play » : `AfterCardEnterPlay(Response, "This", ...)` (et non
#    `AfterYouPlayThisFromHand` de White Tiger : « enters play » vaut aussi pour une mise en jeu) ;
#  - « draw 1 card for each minion engaged with you » : 19030 "Bring It!"
#    (`len(initiator.GetEngagedMinions())`) ;
#  - « When X is defeated by consequential damage » : 30021 SP//dr (`by_consequential=True`).
#
# Mots-pieges : « to a MAXIMUM of 3 » ; « engaged with YOU » (pas tous les sbires en jeu).


def GetAbilities() -> Sequence['Ability']:

    def presage(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        x = Math.MinMax(Worlds.GetVillainStage(effect), 0, 3)
        if x > 0:
            effect.GetInitiator().DrawUp(x, effect)

    def par_sbire(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        n = len(joueur.GetEngagedMinions())
        if n > 0:
            joueur.DrawUp(n, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            presage,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            par_sbire,
            by_consequential=True,
        ),
    ]
