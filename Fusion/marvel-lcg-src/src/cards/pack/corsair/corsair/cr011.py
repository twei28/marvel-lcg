from . import *
# Irresponsible Cad. Obligation (donnee au joueur Christopher Summers), boost 2.
#
# Discard a card you control. If the discarded card was Cyclops or Havok, remove this card from the game. Otherwise,
#   this card gains surge, then discard this obligation.
#
# Cartes de reference : 01160 Legal Work (`WhenThisObligationGiveToYou`), hc013 Mental Episode (« une obligation revelee
# ENTRE EN JEU et y reste » : coder `RemoveAllFromGame` ET `DiscardAll`), `GainSurge(1, effect)` (can_surge.py).
# ⚠ « Cyclops or Havok » : le NOM, toutes versions (officielle, Starjammer) ; l'etoile d'unicite et le sous-titre
# entre parentheses sont ecartes par `NomNu`.
# « Discard a card you control » : OBLIGATOIRE, au choix du joueur parmi ses cartes controlees (hors identite). Sans
# aucune carte, l'obligation prend la branche « Otherwise ».
def GetAbilities() -> Sequence['Ability']:
    def cad(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        identite = joueur.GetIdentity()
        candidates = [f for f in joueur.GetControlCards() if f.IsInPlay() and f is not identite and f is not this]
        defaussee = None
        if candidates:
            choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(
                candidates, effect, prompt="Discard a card you control", forced=True)
            if choisie is not None and Faces.DiscardAll([choisie], effect):
                defaussee = choisie
        if defaussee is not None and NomNu(defaussee) in ("Cyclops", "Havok"):
            Faces.RemoveAllFromGame([this], effect)
        else:
            this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.WhenThisObligationGiveToYou(cad),
    ]
