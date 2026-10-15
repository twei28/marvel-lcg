from . import *

# Villain's Versatility — TRAITRISE x2 (Super-Skrull). 2 icones Y.
# When Revealed: If Super-Skrull has the following SUPERPOWER attachment attached:
#   Pyrokinesis   - Take 3 indirect damage.
#   Rock Mimicry  - Give Super-Skrull a tough status card.
#   Flexibility   - Discard 1 card from your hand.
#   Invisibility  - Place 2 threat on the main scheme.
#
# Cartes de reference :
#  - **`next_evol/40110`** Dizzying Deeds : « If the following enemies are in play: •
#    A — … • B — … » = une branche par ennemi present, resolues DANS L'ORDRE de la
#    liste (`TakeIndirectDamage` sur l'identite, statut, etc.).
#  - **`hunting_season/vulture` DefausserUneCarteDeLaMain** :
#    `joueur.DiscardHandCards((1, 1), effect)` ; `sk100`/`sk073` :
#    `PlaceThreatOnSchemes("MainScheme", n, effect)`.
#
# ⚠ Mots-pieges : chaque ligne est INDEPENDANTE (un mechant a deux pouvoirs
# declenche les deux, dans l'ordre imprime) ; « indirect damage » (reparti par le
# joueur entre ses personnages, pas une attaque) ; « 1 card from YOUR hand »
# (choisie par le joueur) ; « 2 threat on the MAIN scheme » ; aucun pouvoir
# attache : la carte ne fait rien (pas de surge imprime).


def GetAbilities() -> Sequence['Ability']:

    def versatilite(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        mechant = MechantSuperSkrull(effect)
        if mechant is None:
            return
        presents = [a for a in SuperpouvoirsAttaches(effect)]

        def a_le_pouvoir(nom: str) -> bool:
            return any(a.IsName(nom) for a in presents)

        if a_le_pouvoir("Pyrokinesis"):
            joueur.GetIdentity().TakeIndirectDamage(this, 3, effect)
        if a_le_pouvoir("Rock Mimicry"):
            Faces.GiveStatus([mechant], "Tough", effect)
        if a_le_pouvoir("Flexibility"):
            joueur.DiscardHandCards((1, 1), effect)
        if a_le_pouvoir("Invisibility"):
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, versatilite),
    ]
