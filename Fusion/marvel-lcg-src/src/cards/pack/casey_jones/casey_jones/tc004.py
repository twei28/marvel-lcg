from . import *

# Face-Off — EVENEMENT, cout 2, [physical]. ATTACK. x2.
# Hero Action (attack): Ready your hero and deal 3 damage to an enemy. That
#   enemy attacks you.
#
# CARTES DE REFERENCE
#  - `10015` Toe to Toe : « That enemy attacks you » = `cible.DoAttackYou(
#    joueur, effect)` sur l'ennemi choisi ; montage `SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)`.
#  - `raphael/tr004` Headbutt : les degats sont infliges par le HEROS
#    (`heros.DealDamage`), pour que Casey soit l'auteur.
#  - `Faces.ReadyAll` : recette §2.
#
# TEXTE CONTRE CODE
#  ⚠ ORDRE IMPRIME : « Ready your hero » PUIS « deal 3 damage » PUIS « That enemy
#    attacks you » (Toe to Toe fait l'inverse : ne pas copier son ordre).
#  ⚠ « THAT enemy » = la cible des 3 degats ; si elle est vaincue, il n'y a plus
#    d'attaque (la carte hors jeu ne frappe pas).
#  ⚠ « attacks YOU » : le joueur qui joue la carte (son identite), qui peut
#    defendre normalement ; une attaque d'ennemi pioche sa carte de boost.


def GetAbilities() -> Sequence['Ability']:

    def face_off(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        heros = joueur.GetHero()
        cibles = [t for t in effect.targets if t is not None]
        if heros is None:
            return
        Faces.ReadyAll([heros], effect)
        if not cibles:
            return
        heros.DealDamage(cibles, 3, effect)
        for cible in cibles:
            if cible.IsInPlay():
                cible.CastTo(Minion | Villain).DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            face_off,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
