from . import *

# Timebreakers (x3) — TRAITRISE NEMESIS. 1 boost.
# When Revealed: Search the encounter deck and discard pile for Timebroker and
#   reveal him. (Shuffle.) If Timebroker does not enter play this way, this
#   card gains surge.
#
# CARTES DE REFERENCE : `yd017` Hard to Kill, `yd018` Savage Destruction,
# `dr012` et `dr014` — meme motif « chercher deck ET defausse puis reveler ».
#
# TEXTE CONTRE CODE
#  « the encounter deck AND DISCARD PILE » -> LES DEUX zones. N'en fouiller
#    qu'une rendrait la carte inerte des que Timebroker a ete defausse une
#    fois, or c'est exactement le cas qu'elle existe pour couvrir.
#  « If Timebroker DOES NOT ENTER PLAY this way » -> le Renfort tombe aussi
#    quand il etait DEJA en jeu, pas seulement quand la fouille echoue.


def GetAbilities() -> Sequence['Ability']:

    def timebreakers(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        if TimebrokerEnJeu(effect) is not None:
            ThisCardGainSurge(effect)
            return
        trouve = ChercherTimebroker(effect)
        if trouve is None:
            ThisCardGainSurge(effect)
            return
        trouve.Reveal(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            timebreakers,
        ),
    ]
