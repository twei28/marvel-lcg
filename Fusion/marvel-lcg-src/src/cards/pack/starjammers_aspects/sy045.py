from . import *
# * Tolo Hawk (Protection, allie 2 [physical], 1*/1*, PV 2). STARJAMMER.
# Response: After Tolo Hawk enters play, ready a friendly STARJAMMER character.
#
# Cartes de reference : 54012 Captain America (`AfterCardEnterPlay(Response, "This")` + `SetTarget(trait=..., card_type=Unit2,
# canbe_ready=True)` + `Faces.ReadyAll`) ; ub029 Michelangelo (`Friend` pour « friendly character »).
# « a friendly STARJAMMER character » : identite ou allie ami (de n'importe quel joueur) portant le trait ; `canbe_ready` ecarte les
# personnages deja prets (Tolo Hawk entre en jeu pret : il ne se redresse pas lui-meme).
def GetAbilities() -> Sequence['Ability']:
    def tolo_hawk(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Faces.ReadyAll(effect.targets, effect)
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            tolo_hawk,
        ).SetTarget(Friend, trait="STARJAMMER", canbe_ready=True),
    ]
