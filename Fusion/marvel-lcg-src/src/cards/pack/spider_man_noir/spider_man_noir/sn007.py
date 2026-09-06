from . import *

# Dual Pistols — AMELIORATION, cout 2, [physical]. WEAPON.
# Restricted.
# Hero Action (attack): Exhaust Dual Pistols and discard a card tucked under
#   your hero -> deal 3 damage to an enemy. This attack gains ranged.
#
# ⚠ PAS UNIQUE. Le nom n'est pas precede de l'etoile sur le scan, contrairement
# a `sn001a`, `sn001b` et `sn006` : deux exemplaires peuvent donc etre en jeu,
# dans la limite des deux cartes Restreintes.
#
# MOT-CLE : RESTRICTED — fiche `docs/reference/mots-cles/restricted.md`. Base
# automatique : `desc.Restricted = "1"`, le moteur la lit seul. AUCUN SCRIPT.
# MOT-CLE : RANGED — fiche `docs/reference/mots-cles/ranged.md`. Rendu par
# `AttackProperty(ranged=True)` passe a `DealDamage`, comme overkill.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir / `br010` : le squelette d'une amelioration d'arme.
#  - `27078` / `43009` : une attaque qui gagne un mot-cle.
#  - `sn002` Guns Blazing : la carte qui REDRESSE ces pistolets, et donc la
#    raison pour laquelle leur inclinaison est un vrai cout.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX COUTS devant la fleche : incliner ET defausser une carte glissee.
#    Le second est ce qui relie l'arme au moteur du pack — sans pile, les
#    pistolets ne tirent pas.
#  « This attack gains RANGED » -> les attaques a distance ignorent Riposte.
#    C'est la difference avec `sn002`, qui frappe plus fort mais s'expose.
#  « deal 3 damage to AN ENEMY » -> une seule cible.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def pistolets(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect,
                        property=AttackProperty(ranged=True))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pistolets,
            conditions=[PileNonVide],
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee))
        .SetTarget(Enemy),
    ]
