from cards.pack import *

################################################################################
# Pack Jessica Jones — custom « ekAugust ».
#
# Toute la boite a outils du heros tourne autour des manigances secondaires :
# plusieurs cartes demandent « si tu as vaincu une manigance secondaire ce
# round ». Le moteur ne tient pas ce compteur (`player_stat.py` ne suit que les
# cartes jouees/revelees), on l'enregistre donc nous-memes sur `effect.world`,
# comme le recommande le guide pour l'etat persistant maison.
#
# Le marqueur est pose par une capacite silencieuse (Temp0, invisible dans
# l'UI) portee par les DEUX faces d'identite : Crack the Case est une simple
# « Action », jouable donc aussi en alter-ego.
################################################################################

DEFEAT_ROUNDS_ATTR = "jessica_jones_side_scheme_defeat_rounds"


def _defeat_rounds(world: Any) -> Any:
    table = getattr(world, DEFEAT_ROUNDS_ATTR, None)
    if table is None:
        table = {}
        setattr(world, DEFEAT_ROUNDS_ATTR, table)
    return table


def RecordSideSchemeDefeat() -> 'Ability':
    """Capacite silencieuse a poser sur une face d'identite."""

    def record(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        world = effect.world
        _defeat_rounds(world)[id(effect.GetInitiator())] = world.round_id

    return AbilityFactory.AfterUnitDefeatedScheme(
        AbilityType.Temp0,
        "You",
        SchemeSide2,
        record,
    )


def HasDefeatedSideSchemeThisRound(effect: 'Effect') -> bool:
    world = effect.world
    initiator = effect.GetInitiator()
    if initiator is None:
        return False
    return _defeat_rounds(world).get(id(initiator)) == world.round_id


def IsSideSchemeInPlay(effect: 'Effect', message: Any=None) -> bool:
    return len(Worlds.GetSideSchemes(effect)) > 0
