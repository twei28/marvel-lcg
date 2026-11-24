from . import *

# * PAC-RAT II : soutien Leadership, cout 1. VEHICLE. X-FORCE.
# Response: After your turn begins, place 1 time counter on PAC-RAT II.
# Action: Put up to two X-FORCE allies from your hand into play with total printed cost equal to or less than the number of time counters
# on PAC-RAT II. Then, discard PAC-RAT II.
#
# Cartes de reference : `Faces.PlaceCountersOn(..., 'time', ...)`, `FacesCounter.GetPrintedCost` (faces_counter.py:110), `face.PutIntoPlay(joueur, effect,
# under_control=True)`, `joueur.AskChooseFace(..., forced=False)` (cr010).
# ⚠ « total printed cost » : la SOMME des couts imprimes des deux allies <= le nombre de compteurs ; « up to two » : 0, 1 ou 2.
def GetAbilities() -> Sequence['Ability']:
    def compteur(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Support)
        Faces.PlaceCountersOn([this], 1, 'time', effect)

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        joueur = JoueurDe(effect)
        reste = this.GetCounters('time')
        for _ in range(2):
            candidats = [f for f in joueur.hand_cards.GetAll()
                         if Ally.IsType(f) and f.HasTrait("X-FORCE") and FacesCounter.GetPrintedCost([f]) <= reste]
            if not candidats:
                break
            choisi = joueur.AskChooseFace(candidats, effect, prompt="Put an X-FORCE ally into play", forced=False)
            if choisi is None:
                break
            reste -= FacesCounter.GetPrintedCost([choisi])
            choisi.PutIntoPlay(joueur, effect, under_control=True)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterPlayerTurnBegin(AbilityType.Response, "You", compteur),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action),
    ]
