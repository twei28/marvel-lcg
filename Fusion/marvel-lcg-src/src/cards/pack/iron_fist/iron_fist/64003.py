from . import *

# Dragon Punch — EVENEMENT, cout 2, [energy]. ATTACK. SUPERPOWER. x1 (Iron Fist 4/15).
# Hero Action (attack): Deal 2 damage to an enemy. You may remove up to 5 chi counters from your
#   identity to deal 2 additional damage for each chi counter removed this way. If you removed at
#   least 3 counters, also stun that enemy.
#
# CARTES DE REFERENCE
#  - « Remove X counters (X choisi, zero compris) » puis degats : `venus/tv003` Arc Nova
#    (`joueur.DeclareNumber(0, n)` puis `Faces.RemoveCountersOn([identite], x, ...)`).
#  - evenement d'attaque a cible : `cw/56008` Tooth and Claw (`SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)`, `this.DealDamage(effect.targets, n, effect)`).
#  - etourdir : `Faces.GiveStatus([ennemi], "Stunned", effect)` (RECETTES §2, 05015).
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY remove UP TO 5 » : X choisi de 0 a min(5, compteurs de l'identite) ; 0 est legal.
#  ⚠ « from your IDENTITY » : le stock de l'identite (forme heros de fait : Hero Action).
#  ⚠ « 2 ADDITIONAL damage for EACH » : une seule attaque de 2 + 2X degats (X choisi AVANT).
#  ⚠ « If you removed AT LEAST 3 » : X >= 3 (3 compris) ; « also stun THAT enemy » = la cible
#    de l'attaque, seulement si elle est encore en jeu.


def GetAbilities() -> Sequence['Ability']:

    def dragon_punch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        cibles = [t for t in effect.targets if t is not None]
        retires = 0
        disponibles = min(5, Chi(identite))
        if joueur is not None and identite is not None and disponibles > 0:
            retires = joueur.DeclareNumber(0, disponibles)
            if retires > 0:
                Faces.RemoveCountersOn([identite], retires, CHI, effect)
        this.DealDamage(cibles, 2 + 2 * retires, effect)
        if retires >= 3:
            encore = [c for c in cibles if c.IsInPlay()]
            if encore:
                Faces.GiveStatus(encore, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dragon_punch,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
