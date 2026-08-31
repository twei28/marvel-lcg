from . import *

# Psyche Warp — traitrise nemesis. Boost 3.
# When Revealed: You take X damage where X is equal to the ATK of the ally
#   with the highest printed ATK. Discard that ally. If no damage was taken
#   this way, this card gains surge.
#
# Cartes de reference : 42025 * Harpoon (pack angel) pour « le joueur qui
# recoit la carte subit des degats calcules sur une carte », et 01104 (pack
# core) pour « If no damage was ... this way, this card gains surge ».
#
# ARBITRAGE UTILISATEUR DU 31/08/2026 : « the ally » designe UNIQUEMENT les
# allies du joueur qui revele la carte, jamais ceux de ses coequipiers. La
# phrase commence par « YOU take X damage » : la carte reste dans le perimetre
# d'un seul joueur. En solo la question ne se pose pas ; en multi, Psyche Warp
# ne peut donc pas defausser l'allie d'un voisin.
#
# ⚠ « highest PRINTED ATK » : on lit `printed_attack`, pas `attack` — un allie
# dope par une amelioration ne doit pas remonter dans le classement.
# ⚠ « If no damage was taken this way » : aucun allie = 0 degat = surge. Un
# allie a ATK 0 imprime declenche AUSSI le surge (0 degat inflige), mais il
# est quand meme defausse : les deux phrases sont independantes.

def GetAbilities() -> Sequence['Ability']:

    def psyche_warp(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            ThisCardGainSurge(effect)
            return

        allies = [f for f in joueur.allies.Get() if f.IsInPlay()]
        if not allies:
            ThisCardGainSurge(effect)
            return

        cible = max(allies, key=lambda f: f.printed_attack)
        degats = cible.printed_attack

        identite = joueur.GetIdentity()
        if degats > 0 and identite is not None:
            identite.TakeDamage(this, degats, effect)
        else:
            ThisCardGainSurge(effect)

        Faces.DiscardAll([cible], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            psyche_warp,
        ),
    ]
