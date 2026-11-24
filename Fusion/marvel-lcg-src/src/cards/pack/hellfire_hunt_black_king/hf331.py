from . import *

# Sebastian Shaw (sbire ELITE HELLFIRE, module « Sebastian Shaw », Villainous natif). « Forced Response : After Sebastian Shaw takes any amount of
# damage, place that amount of threat on the main scheme. [star] Boost : Give the villain a facedown boost card. »
# Cartes de reference : sk151 (`AfterUnitTookDamage(ForcedResponse, ..., "This")`, `message.took_damage`), hf110 (WQ : `Faces.GiveFacedownBoostCards`).
# ⚠ « any amount of damage » : tout degat (attaque OU non, contrairement a l'Absorb du vilain) ; ce sbire n'entre jamais en jeu dans « Black King »
# (retire au Setup de 1A) : il sert aux autres scenarios (Torn).


def GetAbilities() -> Sequence['Ability']:
    def degats(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        MenaceSurLeComplotPrincipal(effect, message.took_damage)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        villain = Worlds.FindVillain(effect)
        if villain is not None:
            Faces.GiveFacedownBoostCards([villain], 1, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, "This", degats),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
