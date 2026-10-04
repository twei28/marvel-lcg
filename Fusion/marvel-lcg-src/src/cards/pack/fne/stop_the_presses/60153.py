from . import *

# * Ben Urich (DAILY BUGLE, PERSONA, soutien de rencontre) — Uses (3 stamina) : base.
# Action: Exhaust Ben Urich and remove 1 stamina counter from him -> look at
#   the top 2 cards of the encounter deck. You may discard 1 of those cards.
#   (Put the rest back in the same order.)
# joueur.LookAtDeck("EncounterDeck", 2) (bc006 Cat Burglary), choix facultatif.

def GetAbilities() -> Sequence['Ability']:

    def enquete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        vues = joueur.LookAtDeck("EncounterDeck", 2, effect)
        if not vues:
            return
        # ⚠ L'INTITULE EST OBLIGATOIRE (signalement Yarro n43, 03/10/2026). Sans
        # `prompt`, l'option du choix reprenait le NOM DE LA CAPACITE (« Ben
        # Urich: look at the top 2 cards... ») : le joueur croyait devoir la
        # relancer et ne voyait jamais qu'il s'agissait de defausser. « Discard
        # one » est l'intitule deja employe par 45036 (Magik).
        choisie = joueur.AskChooseFace(list(vues), effect, forced=False, prompt="Discard one")  # « You may » = forced=False (pas de `may`)
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    a = AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, enquete).SetName("Ben Urich: look at the top 2 cards of the encounter deck")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
