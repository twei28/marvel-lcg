from . import *

# Predator's Prize — TRAITRISE. Boost 3.
# When Revealed: Choose to either give this card to the active villain as a facedown boost card, or find your identity-specific ally and remove
#   it from the game.
#
# Cartes de reference : 60075 Bullseye (« give this card to the villain as a facedown boost card » OU autre chose, `ChooseAbilities`) ;
#   « identity-specific ally » : `CardFinder(card_class="IdentitySpecific")` (45015) ; « find » : `Find.Find` (regle Find).
#
# ⚠ Mots-pieges :
#  - « find » : partout (main, deck, defausse, en jeu) ; aucun allie propre a l'identite -> seule l'option boost est possible ;
#  - « remove from the GAME » (pas defausse) ; « the ACTIVE villain ».


def GetAbilities() -> Sequence['Ability']:

    def allie_propre(joueur: 'Player') -> 'CardFinder':
        return CardFinder(card_type=Ally, card_class="IdentitySpecific",
                          check_face_fn=lambda f: f.GetOwnerPlayer() is joueur)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = JoueurDuMessage(message, effect)

        def retirer(targets: Sequence['CardFace']) -> None:
            allie = Find.Find(effect, who_perform=joueur, finder=allie_propre(joueur))
            if allie is not None:
                Faces.RemoveAllFromGame([allie], effect)

        possede = any(allie_propre(joueur).Check(f) for f in list(joueur.player_deck.GetAll()) + list(joueur.hand_cards.GetAll())
                      + list(joueur.discard_pile.GetAll()) + list(Worlds.GetOnFieldCards(effect)))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Give this card to the active villain as a facedown boost card",
                                            lambda targets: DonnerCommeBoost(this, effect),
                                            condition=MechantActif(effect) is not None),
            AbilityFactory.ForChoiceAbility("Remove your identity-specific ally from the game", retirer, condition=possede),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
