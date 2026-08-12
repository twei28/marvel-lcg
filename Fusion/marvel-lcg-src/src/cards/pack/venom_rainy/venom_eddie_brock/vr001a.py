from . import *

# * Venom (Eddie Brock) — custom « Rainy »
# Hunger — Response: After you defeat an enemy, heal 1 damage from Venom.
#
# L'avertissement « DEFAUT CONNU : Hunger ne repond jamais », porte ici du
# 5/8/2026 au 10/8/2026, etait FAUX. Hunger repond. Prouve par le cas
# « vr001a Venom — Hunger : soigne 1 apres avoir vaincu un ennemi » de
# tools/test_capacites.py : le journal donne « was defeated by Venom » puis
# « Venom gains 1 ♡ », et les degats de l'identite passent de 4 a 3.
#
# Ce qui manquait au constat de l'epoque n'etait pas dans la carte mais dans la
# facon de la mettre a l'epreuve. Venom frappe a 2 : contre un sbire de 3 PV son
# attaque de base ne tue pas, donc rien ne se declenche, et le journal montre
# quand meme une attaque. Le cas lui donne Sharp Teeth (vr011) pour monter a 3.
# Deux autres pieges rencontres en l'ecrivant, notes dans le cas lui-meme :
# `Puzzle.Damage` sur un sbire ne fait RIEN et sans message, et `Puzzle.Attack`
# fait attaquer la carte visee, donc `Puzzle.Attack('01101')` fait frapper le
# SBIRE. Ne pas remettre d'avertissement ici sans un cas rouge a l'appui.
# Symbiotic Bond — Resource: Take 1 damage -> generate a [wild] resource.
#   (Limit once per phase.)

def GetAbilities() -> Sequence['Ability']:

    def hunger(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Hero)
        this.HealthUnits([this], 1, effect)

    def vaincu_par_moi(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return message.GetDefeatingPlayer() == effect.this.GetControlBy()

    def symbiotic_bond_cost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this
        this.TakeDamage(this, 1, effect)
        return True

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Response,
            Enemy,
            hunger,
            has_defeating_player=True,
            conditions=[vaincu_par_moi],
        ).SetName("Hunger"),

        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
        ).SetName("Symbiotic Bond")
        .SetCostFunc(CostFunc.Custom(None, symbiotic_bond_cost))
        .LimitOncePerPhase(),
    ]
