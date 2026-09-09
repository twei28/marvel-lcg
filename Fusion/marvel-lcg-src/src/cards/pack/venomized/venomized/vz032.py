from . import *

# Klyntar Tendrils — AMELIORATION, cout 3, RES [physical]. SYMBIOTE. WEAPON.
# Uses (3 klyntar counters).
# Hero Action: Exhaust this card and remove 1 klyntar counter from it -> choose
#   to either deal 1 damage to an enemy or remove 1 threat from a scheme. Then,
#   heal 1 damage from your identity.
#
# MOT-CLE
#  - `Uses` (mots-cles/uses.md) : BASE NATIVE, `desc.Uses = "3,klyntar"`.
#    Le moteur pose les pions et defausse la carte au dernier retire.
#
# CARTES DE REFERENCE
#  - `01080` Med Team : les deux couts chaines (inclinaison + pion).
#  - `32009` Bulletproof Protector : le « choose » a deux branches, par deux
#    `ForChoiceAbility` passees a `ChooseAbilities`.
#  - `su006` * Anna Maria Marconi (maison) : le meme « choose to EITHER ... or
#    ... » sur une carte du depot.
#
# TEXTE CONTRE CODE
#  ⚠ « THEN, heal 1 damage » : le soin est HORS du choix, il tombe dans les
#    deux branches. Ecrit dans une seule branche, la moitie des usages
#    perdrait le soin.
#  ⚠ Le soin tombe MEME si la branche choisie n'a rien pu faire (aucune
#    menace a retirer, par exemple) : le texte enchaine par « Then », sans
#    condition.
#  ⚠ « from YOUR IDENTITY » : l'identite, pas le heros nomme.
def GetAbilities() -> Sequence['Ability']:

    def klyntar_tendrils(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = effect.GetInitiator()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 1, effect)
            ).SetLabel('attack').SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect)
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

        # « Then, heal 1 damage from your identity. » — hors du choix.
        this.HealthUnits([joueur.GetIdentity()], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            klyntar_tendrils
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'klyntar')),
    ]
