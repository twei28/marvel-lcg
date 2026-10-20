from . import *

# Fuel the Fire — EVENEMENT, cout 0, [mental]. DEFENSE. SUPERPOWER. x2 (Binary 3/15, 4/15).
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, for each [energy] resource in your hand prevent 1 of that damage
#   and heal 1 damage from Binary.
#
# Cartes de reference :
#  - **`sk021`** Deflect the Blow (meme auteur) : « Hero Interrupt (defense):
#    When you would take any amount of damage from an attack, ... prevent » =
#    `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op, is_from_attack=True)
#    .SetLabel('defense')` ; ici sur un EVENEMENT, donc `.SetPlay()`.
#  - `message.PreventDamage(n, effect)` (`sm/27044`) ; soin
#    `this.HealthUnits([identite], n, effect)` (`ant/12006`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « WHEN YOU would take damage FROM AN ATTACK » : l'identite, attaque
#    seulement (`is_from_attack=True`) ; un degat de traitrise ne l'ouvre pas.
#  - « for EACH [energy] resource in your hand » : compte au moment de la
#    resolution (la carte jouee a deja quitte la main ; elle porte [mental],
#    elle ne compterait pas de toute facon). Helper `EnergieEnMain`.
#  - « prevent 1 of THAT damage AND heal 1 » : les deux, N fois. Le soin vaut
#    N meme si l'attaque fait moins de N degats (lecture litterale de « for
#    each ... and », notee au gabarit) ; il part avant que le reste des degats
#    ne soit subi (Interruption).
#  - « heal 1 damage from BINARY » : le nom de la face heros, qui est celle
#    qui joue une Hero Interrupt.
#  - Sans aucune [energy] en main, la carte ne changerait rien : elle n'est pas
#    proposee (condition), comme le veut la regle de l'etat de jeu.


def GetAbilities() -> Sequence['Ability']:

    def a_de_l_energie(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        return EnergieDuJoueur(effect) > 0

    def attiser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        joueur = JoueurDeCetteCarte(effect)
        n = EnergieEnMain(joueur)
        if n <= 0 or joueur is None:
            return
        message.PreventDamage(n, effect)
        this.HealthUnits([joueur.GetIdentity()], n, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            attiser,
            is_from_attack=True,
            conditions=[a_de_l_energie],
        ).SetPlay()
        .SetLabel('defense'),
    ]
