from . import *
# * Cyclops: Scott "Slim" Summers (Leadership, allie 2 [physical], 1*/1*, PV 2). CHAMPION. STARJAMMER.
# [star] Response: After Cyclops uses a basic power, choose another character. That character gets +1 to that basic power until the end of
# the phase.
#
# Cartes de reference : 14001a Quicksilver (`AfterUnitUseBasicPower(Response, "This", op, powers=[..])`) ; 45048 Triage (`SetTarget(Unit2, ..)`) ;
# hc020 / wt006 (`face.GainUntilPhaseEnd(effect, attack=..)`) ; l'etoile d'une Response est une convention d'IMPRESSION (RECETTES §1).
# « ANOTHER character » : pas Cyclops ; « THAT basic power » : celui que Cyclops vient d'utiliser (`message.power` -> ATK / THW / DEF / REC) ;
# « until the end of the phase » : `GainUntilPhaseEnd`.
def GetAbilities() -> Sequence['Ability']:
    def cyclops(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        bonus = BonusAuPouvoir(message.power)
        if not bonus:
            return
        for face in effect.targets:
            face.GainUntilPhaseEnd(effect, **bonus)
    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            cyclops,
            powers=["ATK", "THW", "DEF"],
        ).SetTarget(Friend, check_fn=lambda effect, face: face is not effect.this),
    ]
