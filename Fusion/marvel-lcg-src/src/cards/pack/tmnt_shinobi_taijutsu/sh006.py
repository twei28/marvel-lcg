from . import *

# Flying Kick — EVENEMENT 2 [mental], Taijutsu (TMNT Shinobi, Inkwire). ATTACK.
# Hero Action (attack): Deal 4 damage to an enemy. Draw 1 card for each THWART event used to pay for this event.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - `jennika/tj004` Decisive Strike : lecture des evenements qui ont paye (`effect.context.paid_this_res_effects`,
#    `.this` = la carte depensee) ; ici on les COMPTE au lieu de tester « au moins un » ;
#  - `05015` Tackle : `Hero Action (attack)` + `SetTarget(Enemy)` ; `bt023` / `05005` : `DrawUp`.
#
# TEXTE CONTRE CODE
#  ⚠ « FOR EACH THWART event used to pay » : un nombre, pas un booleen ; chaque evenement THWART depense compte
#    UNE fois (un evenement ATTACK/DEFENSE, ou une ressource, ne compte pas ; Flying Kick elle-meme n'est pas THWART).
#  ⚠ « Deal 4 damage » et « Draw » : deux phrases sans fleche, la pioche a lieu meme si l'ennemi est vaincu.


def GetAbilities() -> Sequence['Ability']:

    def flying_kick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 4, effect)

        if joueur is None:
            return
        comptes: List['CardFace'] = []
        for paye in effect.context.paid_this_res_effects:
            carte = paye.this
            if Event.IsType(carte) and carte != this and carte.HasTrait("THWART") and carte not in comptes:
                comptes.append(carte)
        if comptes:
            joueur.DrawUp(len(comptes), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            flying_kick,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
