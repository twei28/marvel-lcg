from . import *

# Targeted by Hellfire (x2, hf218-hf219). Attachement CONDITION. « Attach to your identity if a copy of Targeted by Hellfire is not attached to you.
# Otherwise, this card gains surge. Forced Response : After you change to hero form, Sebastian Shaw and each HELLFIRE minion engaged with you attacks
# you. Discard this card. »
# Cartes de reference : 04119 Neurological Implants (`AttachToFaceWhenPutIntoPlay("YourIdentity", without_another_copy=True, if_cannot_gain_surge=True)`),
# 90110 (`AfterUnitChangeForm(..., "You", ...)`), hf-fondations `DoAttackYou` (02030 I See You).
# ⚠ Mots-pieges : « Sebastian Shaw AND each HELLFIRE minion ENGAGED WITH YOU » : Shaw (vilain, meme non engage) + les sbires HELLFIRE engages avec CE joueur ;
# « to HERO form » : `to_form=Hero` ; la carte se defausse APRES les attaques.


def GetAbilities() -> Sequence['Ability']:
    def attaques(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this
        joueur = message.trigger.GetControlBy()
        if not Player.IsType(joueur):
            return
        attaquants = list(Worlds.GetVillains(effect, CardFinder(name=NOM_SHAW)))
        attaquants += [m for m in joueur.GetEngagedMinions() if m.HasTrait("HELLFIRE")]
        for attaquant in attaquants:
            if attaquant.IsInPlay():
                attaquant.DoAttackYou(joueur, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity", without_another_copy=True, if_cannot_gain_surge=True),
        AbilityFactory.AfterUnitChangeForm(AbilityType.ForcedResponse, "AttachedCharacter", attaques, to_form=Hero),
    ]
