from . import *

# * Lita — ALLIE 3 [energy], aspect Justice (TMNT Aspects, Inkwire). NINJA. TEMPORAL. TURTLE.
# PV 3, THW 2 (1 degat consecutif), ATK 1 (1 degat consecutif).
# [star] Response: After Lita thwarts, look at the top card of your deck. You may discard 1 card from your
#   hand to add that card to your hand.
#
# Le [star] (et l'etoile a cote du THW) : icone de rappel des Rules Reference, aucune ligne de code.
#
# CARTES DE REFERENCE
#  - `aa019` Wiccan : « After <allie> thwarts » = `AfterUnitAttackOrThwart(Response, "This", op,
#    conditions=[seulement le message AfterUnitThwartEnd])`.
#  - `52021` Madame Web : « look at the top card(s) » = `joueur.LookAtDeck(<deck>, N, effect)`.
#  - « You may ... » : `joueur.MayChooseOneAbility(...)` (Annuler toujours offert) ; la carte de la main est
#    choisie parmi `GetHandCardsAndTuckedDiscardable()` (fiche tuck.md : « discard from your hand »).
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After LITA thwarts » : elle seule (pas un autre personnage).
#  ⚠ « look at the top card of YOUR deck » : on regarde TOUJOURS (meme sans carte en main) ; la carte reste
#    au dessus du deck si le joueur refuse.
#  ⚠ « You MAY discard 1 card from your hand TO add THAT card » : facultatif ; la defausse est le prix de la
#    carte regardee (sans carte en main, rien a proposer).
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def lita(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        regardees = joueur.LookAtDeck(joueur.player_deck, 1, effect)
        if not regardees:
            return
        dessus = regardees[0]
        main = joueur.GetHandCardsAndTuckedDiscardable()
        if not main:
            return

        def echanger(cibles: Sequence['CardFace']) -> None:
            if Faces.DiscardAll(list(cibles), effect) == list(cibles):
                Faces.AddToHand([dessus], joueur, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 1 card from your hand to add the top card of your deck to your hand", echanger,
            ).SetTarget(main, range=(1, 1), canbe_discard=True, not_move=True),
        )

    def seulement_contre(effect: 'Effect', message: 'Message2') -> bool:
        return isinstance(message, Message.AfterUnitThwartEnd)

    return [
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.Response,
            "This",
            lita,
            conditions=[seulement_contre],
        ),
    ]
