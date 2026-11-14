from . import *

# Relentless Pursuit. Attachement CONDITION. « Attach to your identity. Forced Interrupt : When Selene would scheme against you, she attacks you
# instead. Hero Action : Spend a [physical] resource and remove 1 time counter from Beneath the Sun -> discard this card. »
# Cartes de reference : 60182 Cop (`WhenUnitWouldScheme` + `message.SetBeInstead` « instead », RECETTES §2), hf120 (`villain.DoAttackYou`),
# hf413 (cout en compteur de temps). Icone [physical] = poing (so002, comme hf110).


def GetAbilities() -> Sequence['Ability']:
    def l_identite_porteuse(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> bool:
        hote = effect.this.GetBindFace()
        return hote is not None and message.against_player is not None and message.against_player is hote.GetControlByOrOwner()

    def elle_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        selene = Selene(effect)
        joueur = message.against_player
        message.SetBeInstead(effect)
        if selene is not None and joueur is not None:
            selene.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, ChercheurSelene(), elle_attaque, conditions=[l_identite_porteuse]),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("R")).SetCostFunc(CoutTempsDuJour()),
    ]
