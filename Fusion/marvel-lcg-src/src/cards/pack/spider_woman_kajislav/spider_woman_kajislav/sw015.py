from . import *

# Blinded Sight — EVENEMENT d'aspect PROTECTION, cout 1, RES [energy], x2.
# TACTIC.
# Hero Interrupt: When an enemy initiates an attack, that enemy gets -2 ATK for
#   that attack. If that attack deals no damage, confuse the attacking enemy.
#
# CARTES DE REFERENCE
#  - `09037` Skilled Strike : `target.GainForThisActive(effect, message,
#    attack=N)` — le bonus ne dure QUE cette attaque. Ici en negatif.
#  - `message.IfThisAttackDealDamage` (sender_damage.py:187) : sa NEGATION est
#    ce qu'il nous faut, on la construit avec un temoin.
#
# TEXTE CONTRE CODE
#  ⚠ « an enemy initiates AN ATTACK », sans « against you » : la carte protege
#    aussi les VOISINS en multijoueur. C'est ce qui la distingue de `sw014`.
#  ⚠ « If that attack DEALS NO DAMAGE » : zero degat inflige, pas « aucun degat
#    a vous ». Une attaque bloquee par un allie qui encaisse a bien inflige des
#    degats. On regarde donc les degats de L'ATTAQUE, pas du joueur.
#  ⚠ -2 ATK peut ne pas suffire : un ennemi a ATQ 3 frappe encore a 1, et rien
#    n'est desoriente. Les deux moities sont liees par « if », pas par « and ».


def GetAbilities() -> Sequence['Ability']:

    def vue_aveuglee(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        attaquant = message.attacker
        if attaquant is None:
            return
        attaquant.CastTo(Unit2).GainForThisActive(effect, message, attack=-2)

        a_blesse = [False]

        def note_les_degats(cible: 'Unit2') -> None:
            Unused(cible)
            a_blesse[0] = True

        message.IfThisAttackDealDamage(note_les_degats, effect)

        def desorienter_si_rien() -> None:
            if not a_blesse[0] and attaquant.IsInPlay():
                Faces.GiveStatus([attaquant], "Confused", effect)

        RunAt.AfterEnemyActivationEnd(effect, message, desorienter_si_rien)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            vue_aveuglee,
        ).SetPlay(),
    ]
