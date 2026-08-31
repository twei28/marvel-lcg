from . import *

# Shocking Entrance — complot annexe. Boost 2. Hazard 1. Menace de depart 2[per_hero].
# When Revealed: Deal 3 indirect damage to the first player.
# (Hazard Icon: Deal +1 encounter card during the villain phase.)
# [star] Boost: Deal 1 indirect damage to the first player.
#
# Cartes de reference : 42025 * Harpoon (pack angel) pour
# `player.GetIdentity().TakeIndirectDamage(this, n, effect)`, et 01107
# Breakin' & Takin' pour l'icone hazard, qui est lue directement dans `desc`
# (aucun module a ecrire pour l'icone elle-meme).
#
# ⚠ L'ICONE A ETE IDENTIFIEE PAR COMPARAISON D'IMAGE, PAS A VUE (leçon
# Lockjaw, PROCESSUS-CARTE etape 3). Le pictogramme du scan a ete decoupe et
# superpose a ceux de 01107 (hazard : « + » sur une CARTE inclinee) et 01109
# (acceleration : « + » sur une MAISON soulignee) : c'est le premier.
#
# « the first player », pas « the player who revealed it » : on passe par
# `Worlds.GetFirstPlayer`, jamais par `message.GetToPlayer()`.

def GetAbilities() -> Sequence['Ability']:

    def degats_au_premier_joueur(effect: 'Effect', valeur: int) -> None:
        this = effect.this
        premier = Worlds.GetFirstPlayer(effect)
        if premier is None:
            return
        identite = premier.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, valeur, effect)

    def shocking_entrance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        degats_au_premier_joueur(effect, 3)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        degats_au_premier_joueur(effect, 1)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            shocking_entrance,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
