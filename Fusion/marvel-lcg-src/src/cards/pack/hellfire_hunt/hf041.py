from . import *

# Cerebro Insights (manigance annexe de campagne, scenario 1). Victory 1. Hinder 1[per_hero] (desc).
# Forced Response: After White Queen flips, discard this side scheme.
# When Defeated: The player who defeats this side scheme searches the encounter deck and discard pile for a POTENTIAL ALLY side scheme and put it into play.
# They choose a POTENTIAL ALLY side scheme in play, then defeat it.
#
# Cartes de reference : `AbilityFactory.AfterCardFlipToThisSide` (state.py, adapte : « after WHITE QUEEN flips » = apres le RETOURNEMENT du vilain),
# `Faces.DefeatUnits` (faces.py:207), `Search.EncounterCard(..., include_discard_pile=True)`.
# ⚠ « they choose a POTENTIAL ALLY side scheme in play » : n'importe laquelle en jeu (y compris celle qu'on vient de mettre en jeu).
def GetAbilities() -> Sequence['Ability']:
    def cerebro_defaite(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            card_type=EncounterSideScheme,
            trait="POTENTIAL ALLY",
        )
        if face:
            face.PutIntoPlay(joueur, effect)
        choix = Worlds.FindCardsOnField(effect, trait="POTENTIAL ALLY", card_type=EncounterSideScheme)
        if choix:
            cible = choix[0] if len(choix) == 1 else joueur.AskChooseFace(
                choix, effect, prompt="Choose a POTENTIAL ALLY side scheme", forced=True)
            if cible is not None:
                this = effect.this.CastTo(EncounterSideScheme)
                this.RemoveThreatFromSchemes([cible], cible.threat, effect)

    def cerebro_flip(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            cerebro_defaite,
            has_defeating_player=True,
        ),
        # « After WHITE QUEEN flips » : le retournement d'une AUTRE carte (le vilain) ; `AfterCardFlipToThisSide` ne vise que la carte elle-meme.
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterCardFlip,
            [
                lambda effect, message:
                    effect.this.card.IsOnField() and
                    message.to_face is not None and
                    message.to_face.card.IsOnField() and
                    message.to_face.IsName("White Queen"),
            ],
            cerebro_flip,
        ),
    ]
