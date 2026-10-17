from . import *

# Chance Encounter — AMELIORATION 0 [energy], aspect Justice (TMNT Aspects, Inkwire). CONDITION.
# Attach to a scheme. Max 1 per scheme.
# Interrupt: When attached side scheme is defeated, search your deck and discard pile for an ally and add it
#   to your hand. Shuffle your deck.
#
# MODIFIEE par rapport a `26034` / `60025` Chance Encounter : « Attach to a SCHEME » au lieu de « Attach to a
# SIDE scheme » ; l'Interruption parle toujours de « attached SIDE scheme ». Pas d'`ability_link` : script
# propre, copie de 26034 dont seule la cible de jeu change.
# ⚠ QUESTION OUVERTE Q-uj002 (.planning/tmnt/aspects-justice-questions.md) : coquille probable de l'auteur ?
#   Lecture CODEE en attendant (recommandee, fidele au scan) : jouable sur n'importe quelle manigance, y
#   compris la principale ; sur la principale, l'Interruption ne peut jamais partir.
#
# CARTES DE REFERENCE
#  - `26034` (officielle) : `CanPlayThisUpgradeCard(SchemeSide2)` + `WhenSchemeBeDefeated(Interrupt,
#    "AttachedSideScheme", op)`, `Search.PlayerCard(..., include_player_deck, include_discard_pile,
#    card_type=Ally)` puis `GainCard` (la recherche melange le deck).
#  - `30019` Overwatch : « Attach to a scheme » = `CanPlayThisUpgradeCard(Scheme2)`.
#  « Max 1 per scheme » : `desc.MaxPerUnit "1"` (lu par le moteur).
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « a scheme » : principale OU annexe (Scheme2).
#  ⚠ « attached SIDE scheme is defeated » : seulement une manigance ANNEXE, au moment ou elle est vaincue.
#  ⚠ « YOUR deck and discard pile » ; « Shuffle your deck » (fait par la recherche).


def GetAbilities() -> Sequence['Ability']:

    def chance_encounter(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Ally,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Scheme2),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.Interrupt,
            "AttachedSideScheme",
            chance_encounter,
        ),
    ]
