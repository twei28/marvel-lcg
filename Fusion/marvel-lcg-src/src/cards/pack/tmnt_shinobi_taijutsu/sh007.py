from . import *

# Trading Blows — EVENEMENT 1 [physical], Taijutsu (TMNT Shinobi, Inkwire). ATTACK. DEFENSE.
# Hero Response (attack/defense): After you take damage from an enemy attack, deal 2 damage to that enemy. If you
#   paid for this card with a DEFENSE event, stun or confuse that enemy.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « After you take damage from an enemy attack, ... that enemy » : `08030` Counterattack
#    (`AfterUnitTookDamage(HeroResponse, "You", op, is_from_attack=True, who_dealt_damage=Enemy)` + `SetTarget("Attacker")`) ;
#  - « stun or confuse » : `ma015` Break Through (deux branches `ForChoiceAbility`) ;
#  - « if you paid for this card with a DEFENSE event » : `jennika/tj004` (`PayeAvecUnEvenement`).
#
# TEXTE CONTRE CODE
#  ⚠ « After you TAKE damage » : seulement si des degats ont ete REELLEMENT subis (une attaque entierement prevenue
#    ne declenche pas la Reponse) ; « from an ENEMY attack » : `is_from_attack=True` + `who_dealt_damage=Enemy`.
#  ⚠ « THAT enemy » : l'attaquant (`SetTarget("Attacker")`), encore en jeu apres les 2 degats pour l'etourdir.
#  ⚠ « stun OR confuse » : un choix du joueur ; une option impossible (deja etourdi / deja desoriente) n'est pas
#    offerte ; si l'ennemi a deja les deux, rien n'est donne.
#  ⚠ Libelle `(attack/defense)`.


def GetAbilities() -> Sequence['Ability']:

    def trading_blows(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)

        if joueur is None or not PayeAvecUnEvenement(effect, "DEFENSE"):
            return
        vivants = [e for e in effect.targets if not e.IsDefeated()]
        if not vivants:
            return
        cible = vivants[0]
        peut_etourdir = cible.CanbeStunned()
        peut_desorienter = cible.CanbeConfused()
        if peut_etourdir and peut_desorienter:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun that enemy",
                    lambda cibles: Faces.GiveStatus(vivants, "Stunned", effect),
                ),
                AbilityFactory.ForChoiceAbility(
                    "Confuse that enemy",
                    lambda cibles: Faces.GiveStatus(vivants, "Confused", effect),
                ),
            )
        elif peut_etourdir:
            Faces.GiveStatus(vivants, "Stunned", effect)
        elif peut_desorienter:
            Faces.GiveStatus(vivants, "Confused", effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            trading_blows,
            is_from_attack=True,
            who_dealt_damage=Enemy,
        ).SetPlay().SetLabel('attack', 'defense')
        .SetTarget("Attacker"),
    ]
