from . import *

# * Galactus (sbire nemesis de Silver Surfer) — PV 3, SCH 2, ATK 2, Villainous. COSMIC. ELITE.
# Villainous.
# When Revealed: Reveal The World Eater and put it into play engaged with you.
# When Defeated: Remove Galactus from the game.
#
# Cartes de reference :
#  - `04130` The Sleeper (trors) : « When Revealed » + « When Defeated: Remove X from the game »
#    (`WhenThisRevealed(None, op)`, `WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", op)`,
#    `Faces.RemoveAllFromGame`).
#  - `yd015` Sav'rkk (yondu_nemesis) : « reveal / summon X » depuis le deck de rencontre (`Search.SearchForCards`).
#  - `Villainous` : lu directement dans `desc` (fiche mots-cles/villainous.md), rien a coder.
#
# ⚠ Mots-pieges :
#  - « engaged WITH YOU » : engage le joueur a qui Galactus est revele (`message.GetToPlayer()`).
#  - The World Eater fait partie du set nemesis, donc du deck de rencontre : on le cherche dans le deck et la
#    defausse ; s'il est deja en jeu (Galactus est unique), il n'y a rien a reveler.
#  - « Remove Galactus from the game » : jamais defausse, il ne reviendra plus.


def GetAbilities() -> Sequence['Ability']:

    def galactus_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetToPlayer()
        mangeur = ChercherEnRencontre(effect, NOM_MANGEUR, Minion)
        if mangeur is not None and joueur is not None:
            mangeur.PutIntoPlay(joueur, effect)

    def galactus_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            galactus_revele,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            galactus_vaincu,
        ),
    ]
