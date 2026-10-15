from . import *

# * Raphael's Sai — AMELIORATION, cout 1, [physical]. NINJA. SAI. WEAPON.
# UNIQUE. Restricted.
# Each [[SAI]] upgrade you control gains: "Hero Action (attack): Exhaust this
#   card and take 1 damage -> deal 1 damage to an enemy."
#
# PHASE A : construit, jamais execute.
#
# MOTS-CLES (fiches lues) : RESTRICTED — `docs/reference/mots-cles/restricted.md`
# (`desc.Restricted = "1"`, limite de 2 cartes Restricted gerees par le moteur,
# AUCUN script) ; voir aussi `tr012`.
#
# CARTES DE REFERENCE
#  - `ho010` Powered Gauntlets : AMELIORATION a Hero Action (attack) =
#    `CanPlayThisUpgradeCard()` + `WhenInYourPlayTurn(HeroAction).SetLabel(
#    'attack').SetTarget(Enemy).SetCostFunc(Exhaust("This"))`.
#  - `hulk_rainy/90107`, `dr001a` : « take N damage » EN COUT =
#    `CostFunc.TakeDamage(N, "YourIdentity")`.
#  - AUCUN modele pour « each X upgrade you control GAINS an ability » sur des
#    cartes joueur (`GiveAbilityToInPlayWhenApplyThis` n'est employe que par des
#    cartes de RENCONTRE : 50070, 50074, 21139a). Voir l'en-tete du __init__ :
#    les deux Sai portent les deux capacites, chacune conditionnee a la carte
#    donneuse (`SaiEnJeu`).
#
# TEXTE CONTRE CODE
#  ⚠ « EACH SAI upgrade YOU CONTROL gains » : les deux Sai, elle-meme comprise
#    (`CapaciteAttaqueSai` est aussi sur `tr012`, sous la condition « `tr011`
#    en jeu »).
#  ⚠ « Exhaust this card AND take 1 damage -> » : deux COUTS ; les degats sont
#    infliges a l'IDENTITE du joueur (la Sai est attachee au heros).
#  ⚠ « deal 1 damage to AN enemy » : vilain ou sbire, au choix.
#  ⚠ Encart de regles : action d'ATTAQUE + pose de 1 rage (max 3). TODO-QUESTION Q3.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        CapaciteAttaqueSai(),
        CapaciteReponseSai(),
    ]
