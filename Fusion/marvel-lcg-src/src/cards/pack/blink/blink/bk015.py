from . import *

# * Earth-295 — SOUTIEN BASIC, cout 2, [wild]. MULTIVERSE. LOCATION.
# Action: Exhaust Earth-295 and spend 1 resource of any type -> ready a unique
#   ([star]) ally, support or upgrade in play.
#
# TEXTE CONTRE CODE
#  « and spend 1 resource » -> DEUX couts cumules : l'inclinaison ET une
#    ressource. Mot-piege « coût à plusieurs parties » du PROCESSUS-CARTE :
#    ne jamais en oublier une.
#  « of ANY type » -> `Cost("1")` generique, aucune couleur imposee.
#  « a UNIQUE ([star]) ally, support or upgrade » -> le filtre porte sur
#    l'unicite, pas sur le controle : on peut redresser la carte d'un voisin.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            redresser,
        ).SetCost(Cost("1"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(CardFinder(card_type=Ally | Support | Upgrade, is_unique=True)),
    ]
