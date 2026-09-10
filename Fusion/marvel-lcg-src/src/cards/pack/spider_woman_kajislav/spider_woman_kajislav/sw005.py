from . import *

# Swing and Kick — EVENEMENT, cout 2, RES [physical], x2. AERIAL. ATTACK.
# Hero Action (attack): Deal 5 damage to an enemy. Place 1 psionic web counter
#   on Spider-Woman for each [mental] resource you used to pay for this card
#   (to a maximum of 10).
#
# ⚠ 5 DEGATS POUR 2, c'est enorme — et c'est le marche du pack : payer en
# [mental] pour recharger, ou payer en n'importe quoi pour frapper vite.
#
# CARTE DE REFERENCE
#  - la brique « provenance du paiement », deja rodee sur Throg, Beta Ray Bill,
#    Hulk, Lady Sif, Spider-Man 2099 et Venomized :
#    `effect.cost_func.Get(CostFunc.Spend).return_res` rend les ressources
#    REELLEMENT depensees. Elle est enfermee ici dans
#    `ToilesParRessourceMentale` (voir `__init__.py`), que quatre cartes du
#    pack partagent.
#
# TEXTE CONTRE CODE
#  ⚠ « for each [MENTAL] resource » : la couleur compte, pas le nombre de
#    cartes. Une carte a deux icones [mental] en vaut deux.
#  ⚠ Un joker [wild] depense en [mental] COMPTE : c'est `GetColor("B")` qui
#    tranche, et le moteur convertit les jokers a la depense.
#  ⚠ « (to a maximum of 10) » : le plafond du stock, applique par
#    `PoserDesToiles`.
#  ⚠ Les degats tombent MEME si l'on n'a paye aucun [mental] : les deux
#    phrases sont independantes.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_pied(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 5, effect)
        PoserDesToiles(effect.GetInitiator(),
                       ToilesParRessourceMentale(effect, 1), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            coup_de_pied,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
