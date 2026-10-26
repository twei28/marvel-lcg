from . import *
# Ghosts of the Past — OBLIGATION (Give to the Bruce Wayne player). « You may flip to alter-ego form. Choose: • Exhaust Bruce Wayne -> remove Ghosts of the
# Past from the game. • Search and remove all of the deterrence cards from the encounter deck. Add these cards to your deterrence deck. Shuffle the
# encounter deck. Discard this card. »
# Reference : 01160 Legal Work (meme squelette, `YouMayFlipToYourAlterEgoForm`).
def GetAbilities() -> Sequence['Ability']:
    def ghosts(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        YouMayFlipToYourAlterEgoForm(joueur, effect)
        def recuperer(targets: Sequence['CardFace']) -> None:
            cartes = [f for f in Worlds.GetEncounterDeckCards(effect) if EstDissuasion(f)]
            if cartes:
                Faces.FlipAllTo(cartes, False, effect)
                Faces.MoveAllTo(cartes, joueur.additional_deck, effect)
                for face in cartes:
                    PreparerDissuasion(joueur, face)
                    face.card.visible.Set(joueur)
                    EtatBm(face)["resolu"] = False
                joueur.additional_deck.Shuffle(effect)
            Worlds.GetEncounterDeck(effect).Shuffle(effect)
            Faces.DiscardAll([this], effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Bruce Wayne → remove Ghosts of the Past from the game",
                lambda targets: Faces.RemoveAllFromGame([this], effect),
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility("Add the deterrence cards of the encounter deck to your deterrence deck. Discard this obligation", recuperer),
        )
    return [AbilityFactory.WhenThisObligationGiveToYou(ghosts)]
