from . import *

# Bad Publicity — custom « Rainy » (obligation de Peter Parker)
# Give to the Peter Parker player. Uses (3 menace counters).
# Hero Response: After you defeat an enemy or scheme, remove 1 menace counter
#   from here. (La regle des Uses defausse la carte quand le dernier compteur
#   part.)

def GetAbilities() -> Sequence['Ability']:

    def entre_en_jeu(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        this.PutIntoPlay(player, effect)

    def retirer_menace(effect: 'Effect', message: 'Message.WhenUnitBeDefeated|Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Obligation)
        if message.GetDefeatingPlayer() == effect.this.GetControlBy():
            Faces.RemoveCountersOn([this], 1, 'menace', effect)

    def vaincu_par_moi(effect: 'Effect', message: 'Message2') -> bool:
        return message.GetDefeatingPlayer() == effect.this.GetControlBy()

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            entre_en_jeu
        ),

        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.HeroResponse,
            Enemy,
            retirer_menace,
            has_defeating_player=True,
            conditions=[vaincu_par_moi],
        ),

        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.HeroResponse,
            Scheme2,
            retirer_menace,
            has_defeating_player=True,
            conditions=[vaincu_par_moi],
        ),
    ]
