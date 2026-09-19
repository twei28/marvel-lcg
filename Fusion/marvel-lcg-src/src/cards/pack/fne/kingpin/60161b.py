from . import *

# The King's Gambit (1B) — 3[per_hero] depart, 11[per_hero] cible, +1[per_hero].
# When Revealed: Put Public Support into play, LOW side faceup.
# Hero Action: Remove 5 threat from here (4 threat instead in expert mode).
#   Shuffle the encounter discard pile into the encounter deck, then discard
#   cards from the top of the encounter deck until a minion is discarded and
#   reveal that minion.
# If this stage is completed, the players lose the game.
# Modeles : 56096b (When Revealed d'une face 1B), 16073b (Hero Action sur un
# complot principal + IfThisSchemeStageIsCompletedPlayersLoseTheGame), 60095
# (DiscardEncounterCardsUntil + Reveal). Le cout « Remove N threat from here »
# depend du mode : CostFunc.Custom + condition (RECETTES §5).

def GetAbilities() -> Sequence['Ability']:

    def seuil(effect: 'Effect') -> int:
        return 4 if Worlds.IsExpert(effect) else 5

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = SetupCards.PutIntoPlay(effect, joueur, name="Public Support", card_type=Environment)
        if face is not None and face.card.face is not face.card.printed_faces[0]:
            face.card.Flip(effect, call_reveal=False)

    def assez_de_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.threat >= seuil(effect)

    def retirer_la_menace(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(MainScheme)
        n = seuil(effect)
        if this.threat < n:
            return False
        retire = this.RemoveThreatFromSchemes([this], n, effect)
        return retire is not None and retire >= n

    def gambit(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if defausse:
            Faces.ShuffleAllTo(defausse, "EncounterDeck", effect)
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, gambit, conditions=[assez_de_menace])
            .SetName("Remove threat from here: shuffle the discard pile in and reveal a minion")
            .SetCostFunc(CostFunc.Custom(None, retirer_la_menace)),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
