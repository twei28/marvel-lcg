from . import *

# Magic Portal (1/2) — custom « CptScorp »
# Cout 3, [mental], classe Hero, traits SPELL / SUPERPOWER / THWART.
# Hero Action (thwart): Remove 5 threat from a scheme. Then, if the top card
#   of the encounter deck has:
#   • 0 or 1 boost icons -> draw 1 card.
#   • 2 or more boost icons -> remove 2 threat from each scheme in play.
#
# Exemplaire physique 1 de 2 (wc009, wc010). Commentaire complet ici,
# pointeur bref sur wc010.
#
# Meme squelette a paliers que wc005 Magic Bolt, meme modele : Hex Bolt
# (15004). Le premier retrait passe par `.SetTarget(Scheme2)` +
# `.SetLabel('thwart')`, forme standard d'un evenement de manigance (modele
# 09003 Astral Projection, ag004 Infiltrate).
#
# `Scheme2` (et non `MainScheme`) : « a scheme » vise n'importe quelle
# manigance, principale OU annexe — c'est le piege `a scheme` deja documente
# sur hd001a.
#
# « each scheme in play » -> `Worlds.GetOnFieldSchemes(effect)` (worlds.py:145
# = complots principaux + manigances annexes). Aucune cible a choisir : c'est
# un effet de zone, pas un ciblage. `this.RemoveThreatFromSchemes(faces, 2,
# effect)` accepte directement la liste.
#
# Deck de rencontre vide, ou obligation wc018 active -> 0 icone, donc branche
# « 0 ou 1 » : on pioche.

def GetAbilities() -> Sequence['Ability']:

    def magic_portal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 5, effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if initiator is None:
            return

        if icones <= 1:
            initiator.DrawUp(1, effect)
        else:
            manigances = Worlds.GetOnFieldSchemes(effect)
            if manigances:
                this.RemoveThreatFromSchemes(manigances, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            magic_portal,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
