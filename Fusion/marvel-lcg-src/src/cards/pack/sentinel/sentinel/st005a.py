from . import *

# * Legs (Intact) — COMPONENT. INTACT. TECH.
# Permanent. Setup.
# Hero Action: Exhaust Legs (Intact) → reduce the cost of the next card you
#   play by 1.
#
# Cartes de reference :
#  - `05008` Nakia Bahadir et `54019` Man on the Wall : le meme effet, rendu
#    par `Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Phase")`.
#  - `av009` pour l'action de heros a inclinaison.
#
# ⚠ ARBITRAGE. Les deux cartes officielles disent « the next card you play
# **this phase** ». T-Wrecks ecrit « the next card you play », sans duree. Le
# moteur EXIGE une duree (`in_this` est obligatoire : "Phase" ou "Turn") et
# n'offre rien d'illimite. On retient "Phase", la duree officielle de cet
# effet : c'est la lecture la plus proche du texte imprime, et la seule qui
# n'invente pas une reduction qui survivrait a la phase du vilain.


def GetAbilities() -> Sequence['Ability']:

    def survolter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Worlds.UpdateNextCardPlayCost(
            effect.GetInitiator(),
            -1,
            effect,
            in_this="Phase",
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            survolter,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
