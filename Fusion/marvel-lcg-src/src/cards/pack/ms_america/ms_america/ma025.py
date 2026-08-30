from . import *

# Power Stomp — EVENEMENT d'ASPECT (Aggression), custom « jakxin »
# Cout 2, [physical], traits ATTACK + SUPERPOWER.
#
# Play only if your hero has at least 3 ATK.
# Hero Action (attack): Deal X damage to the villain and each minion engaged
#   with you, where X equals your ATK.
#
# ⚠ C'est la SEULE carte d'aspect du catalogue a porter le trait SUPERPOWER
# en dehors des deux cartes Protection officielles : elle declenche donc
# Star-Gaze (branche [physical] : 1 degat a un ennemi).
#
# ---------------------------------------------------------------------------
# LA CONDITION DE JEU — AUCUN KWARG NE SAIT LA DIRE
#
# `Ability.SetPlay` (ability.py:596-629) n'expose AUCUN filtre sur une valeur
# d'attribut COURANTE : le seul voisin est
# `only_if_your_identity_has_at_least_printed_hp`, qui porte sur des PV
# IMPRIMES. On passe donc par une `conditions=[...]` puis `.SetPlay()`.
# Modele exact : `dt012` Gone in a Flash, qui compare des PV courants dans une
# `conditions=` et enchaine sur `.SetPlay()`.
#
# « your HERO has at least 3 ATK » : valeur COURANTE, donc Star Flight (+1
# CTR) n'y change rien mais Combat Training (+1 ATQ) ou America's Anger
# comptent. Ms. America imprime ATQ 2 : la carte est INJOUABLE sans un bonus
# d'attaque en jeu. C'est voulu.
#
# ⚠ `GetHero()` leve un `assert False` en forme alter-ego (player_get.py:203)
# : on passe par `GetIdentity()` + `Hero.IsType(...)`. Une Hero Action n'est
# de toute facon proposee qu'en forme heros, mais la condition est evaluee
# plus tot et plus souvent que la capacite.
#
# ---------------------------------------------------------------------------
# « THE VILLAIN AND EACH MINION ENGAGED WITH YOU »
#
# Le moteur n'expose AUCUNE notion d'engagement pour le vilain : le patron
# canonique est `Worlds.FindVillain(effect)` + `player.GetEngagedMinions()`,
# reunis dans une seule liste. Modeles : `01046` Energy Daggers (officielle),
# `01158` et `lj010`.
#
# « engaged with YOU » -> les sbires du joueur qui joue la carte, jamais ceux
# des autres (mot-piege `against you` du PROCESSUS-CARTE §5).
#
# « X equals YOUR ATK » -> `hero.attack`, la valeur COURANTE (property,
# can_attack.py:56-60), lue au moment de la resolution.


def GetAbilities() -> Sequence['Ability']:

    def atk_du_heros(effect: 'Effect') -> int:
        player = effect.GetInitiator()
        if player is None:
            return 0
        identite = player.GetIdentity()
        if identite is None or not Hero.IsType(identite):
            return 0
        return identite.attack

    def power_stomp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        player = effect.GetInitiator()
        if player is None:
            return

        valeur = atk_du_heros(effect)
        if valeur <= 0:
            return

        vilain = Worlds.FindVillain(effect)
        ennemis: List['CardFace'] = ([vilain] if vilain else [])
        ennemis += player.GetEngagedMinions()
        ennemis = [x for x in ennemis if not x.IsDefeated()]
        if ennemis:
            this.DealDamage(ennemis, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            power_stomp,
            conditions=[
                lambda effect, message:
                    atk_du_heros(effect) >= ATK_MINIMUM_POWER_STOMP,
            ],
        ).SetPlay().SetLabel('attack'),
    ]
