from . import *

# Chaos on the Battlefield — COMPLOT ANNEXE x2 (Secret Invasion). Menace 1, icone ACCELERATION, 3 boosts.
# Incite 2.
# When Revealed: Place X additional threat here, where X is equal to the total SCH of all IMPOSTOR characters in play.
#
# Cartes de reference : **`paibok/sk156`** (`this.PlaceThreatOnSchemes([this], n, effect)`, menace additionnelle a la
# revelation) ; Incite : mot-cle natif (desc `Incite`, fiche mots-cles/incite.md) ; icone Acceleration : desc natif.
#
# ⚠ Mots-pieges : « the TOTAL SCH of ALL IMPOSTOR CHARACTERS in play » : allies CAMOUFLAGED (SCH imprime, lu sur la face
# sbire de la carte) ET sbires REVEALED (SCH courant, modifie par Ssrov par exemple), de tous les joueurs ; la carte se
# revele APRES l'Incite (menace de l'Incite sur le complot principal, X sur ce complot annexe) ; X = 0 : rien.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        x = ScHTotalImpostors(effect)
        if x > 0:
            this.PlaceThreatOnSchemes([this], x, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
