from . import *

# * Rend : EVENEMENT (ATTACK.), cout 3, [physical]. Classe Hero. (x2)
# Hero Action (attack): Deal 6 damage to an enemy. This attack gains overkill. Deal 2 additional damage for each [physical] you overpaid for this card (to a maximum of [physical][physical][physical]).
#
# CARTES DE REFERENCE
#  - Evenement d'attaque a libelle + mot-cle : `uw004` (`this.DealDamage(.., property=AttackProperty(..))`, `.SetPlay().SetLabel('attack').SetTarget(Enemy)`) ; fiche mots-cles/overkill.md.
#  - Surpaiement d'un EVENEMENT : `sk008` / `yd006` : `effect.GetCostX()` = ressources payees - cout (effect.py:519) ; `effect.GetPaidResources().GetColor("R")` pour le nombre de ressources [physical] payees (le wild compte).
#
# TEXTE CONTRE CODE
#  « Deal 6 damage ... This attack gains OVERKILL » : UNE attaque de 6 avec `AttackProperty(overkill=True)`. « 2 ADDITIONAL damage for EACH [physical] you OVERPAID » : seules les ressources [physical] AU-DELA du cout comptent ;
#    lecture du joueur (FAQ du jeu : le joueur choisit lesquelles de ses ressources sont le surplus) = min(surpaiement total, ressources [physical] payees). « to a MAXIMUM of three » : plafond 3 (soit +6). Les ressources d'une autre couleur surpayees ne rapportent rien.
#  Chiffres : cout 3, 6 degats, +2 par [physical], plafond 3.


def GetAbilities() -> Sequence['Ability']:

    def rend(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        surpaye = max(0, effect.GetCostX())
        physiques = effect.GetPaidResources().GetColor("R")
        bonus = min(3, surpaye, physiques)
        this.DealDamage(
            effect.targets,
            6 + 2 * bonus,
            effect,
            property=AttackProperty(overkill=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rend,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
