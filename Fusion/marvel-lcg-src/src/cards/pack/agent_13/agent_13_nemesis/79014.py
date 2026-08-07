from . import *

# Hypnotic Suggestion — custom « Rainy » (nemesis d'Agent 13 / Sharon Carter)
# When Revealed (Alter-Ego): You are confused. This card gains surge.
# When Revealed (Hero): Confuse your hero and place threat on the main scheme
#   equal to your THW.
#
# Modele : Leaping Kick (aos/batroc/50096.py), qui separe deja les deux
# branches par `AbilityFactory.WhenThisRevealed("Alter-Ego", ...)` puis
# `"Hero"`. La confusion passe par `Faces.GiveStatus([identite], "Confused",
# effect)`, enveloppe de `GainStatus("Confused", by_effect)`
# (can_status.py:67) -- meme montage que Purple Man (73019, Jessica Jones) et
# Smoke and Mirrors (71017, Spider-Man Rainy). Le gain de deferlante reprend
# l'aide globale `ThisCardGainSurge` (Worldwide Crisis 45165, Family
# Emergency 45165), equivalente a `this.GainSurge(1, effect)`. La menace de la
# branche heros lit `identite.thwart`, la valeur de THW COURANTE (deja
# modifiee par toute capacite en jeu), exactement ce que dit « equal to your
# THW ».

def GetAbilities() -> Sequence['Ability']:

    def hypnotic_suggestion_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()

        Faces.GiveStatus([player.GetIdentity()], "Confused", effect)
        ThisCardGainSurge(effect)

    def hypnotic_suggestion_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        hero = player.GetIdentity()
        Faces.GiveStatus([hero], "Confused", effect)
        this.PlaceThreatOnSchemes("MainScheme", hero.thwart, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            hypnotic_suggestion_alter_ego,
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            hypnotic_suggestion_hero,
        ),
    ]
