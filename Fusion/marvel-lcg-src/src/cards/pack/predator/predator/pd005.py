from . import *

# Spine Rip — EVENEMENT, cout 3, [physical]. ATTACK. x2.
# Hero Action (attack): Deal 7 damage to an enemy. If that enemy has Infralocked attached, this attack gains overkill.
#
# Cartes de reference :
#  - `core/01053` Relentless Assault : `hero.DealDamage(effect.targets, N, effect, property=AttackProperty(overkill=...))`
#    (fiche mots-cles/overkill.md : l'outrepassement se donne a l'ATTAQUE) ; `.SetPlay().SetLabel('attack')`.
#  - `Hote` / `GetAttachedUpgrades` (ares, yd012) : lire les ameliorations posees sur la cible.
#
# ⚠ Mots-pieges :
#  - « an ENEMY » : sbire ou vilain (`Enemy`), pas seulement un sbire ; Infralocked ne s'attache qu'a un sbire.
#  - « THAT enemy has Infralocked attached » : la carte nommee, lue sur la CIBLE avant les degats.
#  - « this attack GAINS overkill » : le debordement va sur le vilain/le heros selon le mot-cle, pas des degats en plus.


def GetAbilities() -> Sequence['Ability']:

    def eventrer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not effect.targets:
            return
        cible = effect.targets[0]
        marque = any(u.paper.card_id == ID_INFRALOCKED for u in cible.GetAttachedUpgrades())
        joueur.GetHero().DealDamage(effect.targets, 7, effect, property=AttackProperty(overkill=marque))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            eventrer,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
