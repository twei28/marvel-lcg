from . import *

# Cyclonic Suction — AMELIORATION, cout 2, [physical]. SUPERPOWER.
# Hero Response: After you use one of Texas Twister's basic powers (THW, ATK,
#   or DEF), exhaust Cyclonic Suction -> draw 1 card.
#
# CARTE DE REFERENCE
#  - `04032` Captain Marvel : `AfterUnitUseBasicPower` + `DrawUp(1, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ LA CARTE N'EST PAS UNIQUE (pas d'etoile sur le scan) : deux exemplaires
#    en jeu piochent deux cartes par pouvoir de base. C'est volontaire.
#  « exhaust Cyclonic Suction » est un COUT (fleche), donc `SetCostFunc` : la
#    Reponse ne part pas si la carte est deja inclinee, ce qui la limite
#    naturellement a une fois par round sans `LimitOncePerRound`.
#  « TEXAS TWISTER's basic powers » -> `"You"`, l'identite du joueur, et non
#    n'importe quel personnage : un allie qui attaque ne fait rien piocher.


def GetAbilities() -> Sequence['Ability']:

    def aspiration(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            aspiration,
            powers=POUVOIRS_DE_BASE,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
