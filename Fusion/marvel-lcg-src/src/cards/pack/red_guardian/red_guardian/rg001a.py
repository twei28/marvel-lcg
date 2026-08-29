from . import *

# * Red Guardian
# Shield Launch — Action (attack/thwart): Attach Red Guardian's Shield from
#   your hand to an enemy or a scheme -> deal 2 damage to that enemy or remove
#   2 threat from that scheme.
#
# La capacite fait DEUX choses d'un coup : elle sort le bouclier de la main
# pour l'attacher a la cible choisie, puis frappe cette meme cible. La nature
# de la cible decide de l'effet — 2 degats a un ennemi, 2 menace retiree a une
# manigance.
#
# Le cout n'est pas une ressource : c'est d'avoir le bouclier en main. La
# condition le verifie, et le bouclier quitte la main dans l'operation.


def GetAbilities() -> Sequence['Ability']:

    def shield_launch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        joueur = effect.GetInitiator()
        cibles = list(effect.targets)
        if joueur is None or not cibles:
            return

        bouclier = BouclierEnMain(joueur)
        if bouclier is None:
            return

        cible = cibles[0]

        # 1) le bouclier quitte la main et se plante sur la cible
        bouclier.CastTo(Upgrade).PutIntoPlay(joueur, effect, under_control=True)
        bouclier.CastTo(Upgrade).AttachTo2(cible, effect)

        # 2) l'effet depend de ce qu'on a touche
        if Enemy.IsType(cible):
            this.DealDamage([cible], 2, effect)
        elif Scheme2.IsType(cible):
            this.RemoveThreatFromSchemes([cible], 2, effect)

    return [
        (AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            shield_launch,
            conditions=[BouclierEstEnMain],
        )
            .SetName("Shield Launch")
            # deux libelles distincts, pas la chaine « attack/thwart » : le
            # moteur valide chaque libelle contre ['attack', 'thwart']
            # (ability.py check_sub_type). Modele dt028.
            .SetLabel("attack", "thwart")
            .SetTarget(Enemy | Scheme2, range=(1, 1))),
    ]
