from . import *

# * Kitsune — SBIRE nemesis (2/5). FOOT CLAN. PANTHEON. WITCH.
# MNG 2 / ATQ 2 / PV 2 / Boost 2.
# When Revealed: Cloak Kitsune and exhaust your identity.
# (Alopex's nemesis minion.)
#
# Cartes de reference :
#  - `leonardo/leonardo_nemesis/tl016` : `WhenThisRevealed(None, op)` + « Cloak
#    <la carte elle-meme> » = `Faces.GiveStatus([this], "Cloaked", effect)`
#    (fiche mots-cles/cloak.md) ;
#  - « exhaust your identity » : `Faces.ExhaustAll([joueur.GetIdentity()], effect)` ;
#    le joueur est `message.GetToPlayer()` (celui a qui la carte est revelee).
#
# ⚠ BASES AUTOMATIQUES (desc) : `Nemesis` = « Alopex », `Boost 2`.
#
# Mots-pieges :
#  - « Cloak KITSUNE » : la carte elle-meme (pas le vilain) ;
#  - « exhaust YOUR identity » : l'identite du joueur a qui Kitsune est
#    revelee (heros ou alter-ego), pas forcement Alopex ;
#  - deux effets, dans cet ordre, sans choix.


def GetAbilities() -> Sequence['Ability']:

    def kitsune(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        Faces.GiveStatus([this], "Cloaked", effect)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ExhaustAll([identite], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            kitsune,
        ),
    ]
