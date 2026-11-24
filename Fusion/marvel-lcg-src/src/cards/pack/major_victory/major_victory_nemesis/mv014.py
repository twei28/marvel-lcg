from . import *

# Korvac's Future — COMPLOT ANNEXE nemesis. Permanent. Menace 4, boost 3.
# While there is 4 or more threat here, each hero identity gets -1 hand size.
# Forced Response: After threat is placed here, if there is at least 14 threat here, the players lose the game.
#
# CARTES DE REFERENCE
#  - `st005b` Legs / `04165` : `GiveKeywordToInPlayWhenApplyThis(.., hand_size=-1)` pour le malus de main ; son parametre
#    `condition` porte le seuil de menace.
#  - `ra029` / `wt018` : `AfterSchemePlaceThreat(.., has_at_least_threat=N)` + `Worlds.SetGameOver(False, effect)`.
#
# TEXTE CONTRE CODE
#  « Permanent » -> `desc.Permanent` (base automatique). « 4 or more threat here » -> seuil >= 4 (PAS > 4).
#  « each hero identity » -> `Identity`. « -1 hand size » -> `hand_size=-1`. « at least 14 » -> `has_at_least_threat=14`.
#  « After threat is placed here » -> `AfterSchemePlaceThreat` sur "This" (et non « when »), en Forced Response.
#  Chiffres : 4, -1, 14.


def GetAbilities() -> Sequence['Ability']:

    def quatre_menaces_ou_plus(effect: 'Effect') -> bool:
        return effect.this.CastTo(Scheme2).threat >= 4

    def perdre(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        Unused(message)
        Worlds.SetGameOver(False, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            hand_size=-1,
            condition=quatre_menaces_ou_plus,
            # ⚠ SANS `change_on_event`, le malus n'etait calcule qu'a l'entree en jeu : retirer la menace sous 4 ne rendait
            # JAMAIS la main (temoin « sous 4 menaces », rouge le 30/10/2026). Modele : `sk138` (`OnEvent.Threat("This")`).
            change_on_event=OnEvent.Threat("This"),
        ),
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.ForcedResponse,
            "This",
            perdre,
            has_at_least_threat=14,
        ),
    ]
