from . import *

# Exploding Their Head (OBLIGATION, x2 : hf608, hf609). « Each encounter card you revealed gains peril. Forced Response : After your turn ends,
# discard cards you control that the total resource cost of cards is at least 2. Take 1 damage for each card you discarded. Then, discard this
# card. Otherwise, deal yourself 1 facedown encounter card. »
# Cartes de reference : bf023 / 39064 (`GiveKeywordToInPlayWhenApplyThis(EncounterCard, peril=1)`), 32099 (`AfterPlayerTurnEnd(ForcedResponse,
# "AttachedPlayer")` d'une obligation), `Player.AskChooseFace`, `Faces.DiscardAll`.
# ⚠ LECTURE (QUESTIONS.md n°1) : « cards you control » = allies, ameliorations et soutiens ; « resource cost » = cout IMPRIME ; le joueur choisit
# les cartes une a une jusqu'a atteindre 2 (il peut en defausser plus, a ses frais : 1 degat chacune) ; SI le total de tout ce qu'il controle est
# inferieur a 2, « Otherwise » : 1 carte de rencontre face cachee et l'obligation RESTE.


def GetAbilities() -> Sequence['Ability']:
    return ObligationExploding()
