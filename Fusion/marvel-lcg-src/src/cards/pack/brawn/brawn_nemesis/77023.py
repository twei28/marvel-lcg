from . import *

# Tidal Surge (2e exemplaire, traitrise nemesis) — custom « Rainy »
# Surge.
# When Revealed: Place 1 acceleration token on Rising Tide. If Namor is in play,
#   give him a tough status card.
# [star] Boost: Give the activating enemy 1 additional boost card.
#
# « Place 1 acceleration token ON RISING TIDE » : si la manigance n'est pas en
# jeu, il n'y a rien a faire — le jeton ne se reporte pas ailleurs. Seule la
# moitie « tough » peut alors s'appliquer.

def GetAbilities() -> Sequence['Ability']:

    def tidal_surge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        rising_tide = Worlds.FindCardOnField(effect, name="Rising Tide")
        if rising_tide is not None:
            rising_tide.CastTo(EncounterSideScheme).PlaceAccelerationToken(1, effect)

        namor = Worlds.FindCardOnField(effect, name="Namor", card_type=Enemy)
        if namor is not None:
            Faces.GiveStatus([namor], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        # Modele de Titania's Fury 01164. La carte imprime « the activating
        # enemy » et non « the villain » : on ne restreint donc pas le type,
        # un sbire qui s'active compte aussi.
        message.GiveBoostCardForThisActivation(Enemy, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            tidal_surge,
        ),

        # ⚠ `WhenCardBecomeBoost` est bien la fabrique des « [star] Boost: » :
        # 170 traitrises OFFICIELLES l'emploient. Elle ne part simplement pas
        # sous `Puzzle.Boost`, qui pose la carte au sommet du deck Rencontre et
        # active le vilain sans passer par la distribution normale — limite du
        # harnais, pas de la carte. Branche a verifier en partie reelle.
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
