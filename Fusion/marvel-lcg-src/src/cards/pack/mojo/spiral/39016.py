from . import *

# The Search for Spiral
#
# ERRATA RRG 1.8 (Annexe V, Mojo Mania #16) : « Hero Action: Take 2 damage → remove 3 threat from here. » (ajout de la flèche de coût).
#   ANCIEN comportement du script : les 2 dégâts étaient un EFFET (`identity.TakeDamage(...)` puis le retrait de menace, toujours résolu, même si
#   les dégâts étaient empêchés). NOUVEAU : « Take 2 damage » est un COÛT (`CostFunc.TakeDamage(2, "YourIdentity")`, modèle `16123` Obedience Potion) :
#   si TOUS les dégâts ne sont pas subis (empêchés par une carte d'état Tenace, par exemple), le coût n'est pas payé et AUCUNE menace n'est retirée.
#   Le texte de la fiche (`cards.json`) ne portait que « Permanent. » : la capacité et la Réponse forcée sont ajoutées par l'agent des errata.

def GetAbilities() -> Sequence['Ability']:

    def the_search_for_spiral_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        # Les 2 degats sont le COUT (CostFunc.TakeDamage ci-dessous) : ici, seulement l'effet.
        this.RemoveThreatFromSchemes([this], 3, effect)

    def the_search_for_spiral(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        player = message.GetByPlayer()

        if player:
            face = GetShowDeck(effect).GetTopCard()
            if face:
                face.Reveal(player, effect)

        this.PlaceThreatOnSchemes([this], "3*", effect)


    return [
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.ForcedResponse,
            "This",
            the_search_for_spiral,
            last_threat=True
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            the_search_for_spiral_action,
        ).SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity")),
    ]

