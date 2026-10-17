from . import *

# Migatte — EVENEMENT DUAL Bushido/Taijutsu, cout 1, [physical]. DEFENSE.
# Classe : « Bushido;Taijutsu ».
# Hero Interrupt (defense): When your hero defends against an attack, it gets +2 DEF for that attack.
#   If you paid for this card with a Shinobi card, ready your hero.
#
# Mots-cles (fiches lues AVANT le code) : Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « When your hero defends against an attack, it gets +N DEF for that attack » : `cap/03033` Expert Defense
#    (`WhenUnitDefendAgainstAttack(HeroInterrupt, "YourHero", fn).SetPlay().SetLabel('defense')`,
#    `message.GainDEFForThisAttack(n, effect)`) ;
#  - « If you paid for this card with <un type de carte> » : `jennika/tj004` Decisive Strike (lit
#    `effect.context.paid_this_res_effects`, dont `.this` est la carte qui a paye), ici avec le helper
#    `EstShinobi` au lieu d'un evenement ATTACK ;
#  - « ready your hero » : `Faces.ReadyAll([heros], effect)` (`tj006`).
#
# TEXTE CONTRE CODE
#  ⚠ « paid for this card with a SHINOBI CARD » : une AUTRE carte (pas Migatte elle-meme), n'importe quel type de carte
#    (evenement, amelioration, allie...) portant l'une des quatre classes Shinobi, defaussee pour sa ressource. Une Dual en est
#    une pour ses deux classes. Une carte non Shinobi (ni aspect, ni Basic) ne compte pas ; un PATH n'est pas une carte
#    Shinobi (`EstShinobi`).
#  ⚠ « +2 DEF FOR THAT ATTACK » : inconditionnel (les deux phrases sont independantes) ; « ready your hero » ne depend que
#    du paiement.
#  ⚠ « When your hero defends » : forme heros seulement (HeroInterrupt, `"YourHero"`).


def GetAbilities() -> Sequence['Ability']:

    def paye_avec_une_carte_shinobi(effect: 'Effect') -> bool:
        this = effect.this
        return any(
            e.this != this and EstShinobi(e.this)
            for e in effect.context.paid_this_res_effects
        )

    def migatte(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GainDEFForThisAttack(2, effect)
        if paye_avec_une_carte_shinobi(effect):
            joueur = effect.GetInitiator()
            if joueur is not None and joueur.IsHero():
                Faces.ReadyAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            migatte,
        ).SetPlay().SetLabel('defense'),
    ]
