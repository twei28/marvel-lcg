from . import *

# * Dawn Greenwood — Allie, cout 0, PV 1, ATK 1*, THW 1*, ressource [mental]. ADVENTURER.
# Interrupt: When Dawn Greenwood is defeated, deal 2 damage to your identity -> return Dawn Greenwood to your hand.
#
# Cartes de reference :
#  - `05002` * Red Dagger (msm) : « Interrupt: When Red Dagger is defeated, <cout> -> ... return to hand »,
#    meme fabrique `WhenUnitBeDefeated(Interrupt, "This", op)` et `Faces.ReturnToHand([this], initiator, effect)`.
#  - `01027` Focused Rage : cout en degats a l'identite (`CostFunc.TakeDamage`).
#
# ⚠ Mots-pieges :
#  - « deal 2 damage to YOUR IDENTITY » : les deux formes (heros ET alter-ego), `"YourIdentity"`.
#  - la fleche en fait un COUT : si l'identite ne peut pas payer, Dawn est simplement vaincue.
#  - « return Dawn Greenwood to your hand » : elle QUITTE le jeu au lieu d'etre defaussee (Interruption).
#  - le [star] des icones ATK/THW de l'allie est une icone de degats consecutifs (`1*`), pas un texte.


def GetAbilities() -> Sequence['Ability']:

    def dawn(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        Faces.ReturnToHand([this], initiator, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            dawn,
        ).SetCostFunc(CostFunc.DealDamage(2, "YourIdentity")),
    ]
