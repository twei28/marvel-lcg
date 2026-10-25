from . import *

# Riot in the Vault — TRAITRISE x3. 1 icone de boost. Surge.
# When Revealed: If Inspection of the Vault is not in play, reveal it. Otherwise, place 1 threat on the main scheme for each
#   Villain beneath The Vault.
#
# Cartes de reference :
#  - Surge : natif (desc.Surge, fiche surge.md) ; « reveal it » : `SetupCards.Reveal(..., only_set_aside=True)` (Obligation, donnee
#    au premier joueur par son `GiveTo`) ; menace : `this.PlaceThreatOnSchemes("MainScheme", n, effect)` (modele 60148).
#
# ⚠ Mots-pieges : « OTHERWISE » = deux branches exclusives (l'Inspection arrive OU la menace tombe, jamais les deux) ; « Villain
# beneath » ne compte que les vilains ; Inspection de cote dans la reserve : la carte la retrouve meme apres qu'un joueur l'a
# mise de cote.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        if not InspectionEnJeu(effect):
            SetupCards.Reveal(effect, Worlds.GetFirstPlayer(effect), name=NOM_INSPECTION, card_type=Obligation, only_set_aside=True)
            return
        n = len(MechantsSousLeVault(effect))
        if n > 0:
            this.PlaceThreatOnSchemes("MainScheme", n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
