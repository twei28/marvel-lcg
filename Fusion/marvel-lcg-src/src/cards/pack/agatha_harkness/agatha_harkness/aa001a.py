from . import *

# * Agatha Harkness (face heros)
# MYSTIC.  THW 1 / ATK 1 / DEF 1 — HS 5 / PV 9
# Power Absorption - Response: After Agatha Harkness takes any amount of
#   damage from an attack, discard an equal number of cards from the top of
#   your deck. Add 1 SPELL card discarded this way to your hand.
#   (Limit once per phase.)
#
# Cartes de reference (RECETTES-MOTEUR §1/§2) :
#  - declencheur : 27078 « Now We're Angry! », meme
#    `AfterUnitTookDamage(..., is_from_attack=True)` — le montant subi est
#    `message.took_damage` (sender_damage.py:892) ;
#  - la defausse : an011 Hel's Retribution,
#    `player.DiscardDeckTopCards(n, effect)` qui REND la liste des cartes
#    defaussees ;
#  - la remontee : 01034 Stark Tower, `Faces.ReturnToHand`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « takes any amount of damage from an ATTACK » : les degats indirects ou
#    d'effets directs ne declenchent RIEN (`is_from_attack=True`) ;
#  - « an EQUAL number » : on defausse autant que les degats REELLEMENT
#    subis (`took_damage`, pas les degats annonces) ;
#  - « discarded THIS WAY » : seul le lot tout juste defausse est eligible,
#    jamais le reste de la defausse ;
#  - « Add 1 SPELL card » : UNE seule, au choix du joueur s'il y en a
#    plusieurs ; aa011 Runic Magician leve la contrainte SPELL (son
#    Hero Interrupt), rendu par un choix supplementaire quand elle est en jeu.

def GetAbilities() -> Sequence['Ability']:

    def power_absorption(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        n = message.took_damage
        if n <= 0:
            return
        defaussees = initiator.DiscardDeckTopCards(n, effect)
        if not defaussees:
            return

        sorts = [f for f in defaussees if f.HasTrait("SPELL")]
        eligibles = sorts
        if RunicMagicianEnJeu(effect) and defaussees:
            # aa011 : « ignore the SPELL trait requirement »
            eligibles = list(defaussees)
        if not eligibles:
            return

        choisies = initiator.AskChooseFaces(eligibles, (1, 1), effect)
        if choisies:
            Faces.ReturnToHand(list(choisies), initiator, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            power_absorption,
            is_from_attack=True,
        ).SetName("Power Absorption")
        .LimitOncePerPhase(),
    ]
