from . import *

# Mutagen Bomb — COMPLOT ANNEXE nemesis (1/5). 2 icones de boost, menace de
# depart 2 par joueur (« 2 » + silhouette).
# Old Hobb has weaponized mutagen into bombs.
# Forced Response: After resolving step one of the villain phase, place 1
#   timer counter here. Then, if there are 2 or more timer counters here,
#   discard this card and deal each player 1 facedown encounter card.
#
# PHASE A : construit, jamais execute.
#
# ICONE : « croix + avion » sous le texte = AMPLIFY 1 (decision du 15/10/2026 :
#   meme glyphe que 16054 Vendetta, verifie par decoupe). `desc.Amplify = "1"`
#   dans cards.json : le moteur l'applique seul, aucun script (fiche
#   docs/reference/mots-cles/amplify.md).
#
# CARTES DE REFERENCE
#  - `04112b` The Island of Dr. Zola / `04113b` (zola/__init__.py) :
#    « After resolving step one of the villain phase, place 1 test counter here.
#    Then, if there are N or more ... » = `AfterResolveVillainPhaseStep(
#    ForcedResponse, 1, op)`, `Faces.PlaceCountersOn([this], 1, nom, effect)`
#    puis `this.GetCounters(nom) >= N`.
#  - `24029` Cruel Intentions / `32064a` : « deal each player 1 facedown
#    encounter card » = `Players.ForEachPlayer(effect, lambda p:
#    p.DealEncounterCards(1, effect))`.
#  - `gb005b` (gorr) : le compteur `timer` existe deja dans l'enum.
#
# TEXTE CONTRE CODE
#  ⚠ « After resolving STEP ONE of the villain phase » -> `step=1`, pas la
#    simple ouverture de la phase du vilain.
#  ⚠ « place 1 timer counter HERE » (sur cette carte) PUIS « if 2 or MORE » :
#    le test est APRES la pose, donc se declenche au 2e passage (1er : 1
#    compteur, rien ; 2e : 2 compteurs, bombe). Le seuil est `>= 2`.
#  ⚠ « discard this card AND deal each player 1 facedown encounter card » : la
#    defausse d'abord, puis la distribution a CHAQUE joueur (piege `each`).
#  ⚠ « timer » (et non `time`) : meme compteur que `gb005b`.
#  Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def la_bombe_avance(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, 'timer', effect)
        if this.GetCounters('timer') < 2:
            return

        Faces.DiscardAll([this], effect)

        def distribuer(joueur: 'Player') -> None:
            joueur.DealEncounterCards(1, effect)

        Players.ForEachPlayer(effect, distribuer)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            la_bombe_avance,
        ),
    ]
