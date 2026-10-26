from . import *
# * Oracle — SOUTIEN cout 2 [mental]. BAT FAMILY. PERSONA. Action : exhaust Oracle -> search the encounter deck for a deterrence card. Then, reveal the
# chosen deterrence card and shuffle the encounter deck.
# Reference : hercules 59001b (`face.Reveal(joueur, effect)`), `Search.EncounterCard`. La carte revelee passe par SON When Revealed : elle est
# donc marquee resolue et retourne dans la defausse de dissuasion.
def GetAbilities() -> Sequence['Ability']:
    def oracle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.EncounterCard(effect, joueur, include_discard_pile=False, trait=TRAIT_DISSUASION)
        if face is not None:
            face.Reveal(joueur, effect)
        Worlds.GetEncounterDeck(effect).Shuffle(effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, oracle).SetCostFunc(CostFunc.Exhaust("This")),
    ]
