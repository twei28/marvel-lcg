from . import *

# Tribute
# SONG.
# Limit 1 per deck.
# Hero Action: After you play Tribute from your hand, choose 1 non-identity
#   event in your collection. Tribute becomes a copy of that card, (except for
#   its cost) but keeps the SONG trait, until it is placed in the discard pile.
#
# `Search.Collection` cherche dans TOUTE la base du jeu et FABRIQUE la carte
# choisie dans la defausse du joueur. Mecanique officielle, portee par Armed to
# the Teeth (Deadpool 44009), Baron Zemo (50171) et deux cartes Determination.
# Prouvee en partie reelle avant d'ecrire cette carte : 407 evenements
# non-identite proposes, 0 fuite d'identity-specific, effet reellement resolu,
# cout NON paye.
#
# « non-identity event » : PAS `card_classes="Any"`, qui ne vaut que les cinq
# aspects officiels et jetterait les 72 evenements basiques et les 41
# Determination. On exclut la classe `Hero`, ce qui est le sens litteral.
#
# « BECOMES A COPY (except for its cost) » est rendu par « on joue la carte
# trouvee sans payer son cout » : le resultat en jeu est le meme, et le moteur
# n'a pas de mecanisme pour changer l'identite d'une carte. La carte fabriquee
# doit d'abord passer par la MAIN — sortie de la defausse, elle n'est pas
# jouable (`is_like_in_hand`, ability.py:235).


def GetAbilities() -> Sequence['Ability']:

    def non_identite(paper: 'Paper') -> bool:
        classes = (paper.desc.get("Class") or "").split(";")
        return "Hero" not in classes

    def tribute(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        face = Search.Collection(
            effect, joueur, card_type=Event, check_fn=non_identite)
        if face is None:
            return

        Faces.AddToHand([face], joueur, effect)
        joueur.PlayCardsLikeInTurn([face], effect, ignore_resources_cost=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tribute,
        ).SetPlay().SetLabel(),
    ]
