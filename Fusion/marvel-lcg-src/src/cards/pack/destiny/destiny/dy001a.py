from . import *

# * Destiny (face heros) : PSIONIC. X-MEN. THW X / ATQ X / DEF X, main 5, PV 9.
# X is the number of icons ([star] and [boost]) on the card tucked under Glimpse of the Future.
# Interrupt: When a boost card is turned faceup, give the enemy another boost card for this activation. Then discard one of them. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `mw001a` Madame Web : stats « X » imprimees ; `desc` les declare a 0 et `ThisGainKeyword(fn, attack=1, thwart=1, defense=1, change_on_event=...)` les remonte a X.
#  - `sw001a` Spider-Woman / `08006` Attacrobatics : `WhenBoostCardTurnedFaceUp(Interrupt, None, op)` + `message.CancelAllBoostIcons` ; `CanBoost.GiveFacedownBoostCardsInternal(1, effect, message.would_message)` (modele sender_card.py, `GiveBoostCardForThisActivation`) pour « give the enemy another boost card ».
#  - `sn014` : `FacesCounter.CountTotalBoostStarAndBoost` (etoile + icones), voir `IconesSousGlimpse`.
#
# TEXTE CONTRE CODE
#  « a boost card is turned faceup » : toute activation (attaque ou manigance, contre n'importe quel joueur), aucun filtre `while_attack`. « give the enemy ANOTHER boost card FOR THIS ACTIVATION » : une carte de boost de
#    plus a l'ennemi qui active, face cachee. « Then discard ONE of them » : le joueur choisit entre la carte retournee (on annule ses icones et son effet [star] : elle ne compte plus) et la nouvelle carte, encore
#    face cachee (defaussee sans etre retournee). Doute de lecture signale en fin de travail. « Limit once per phase » : `LimitOncePerPhase`.
#  Chiffres : PV 9, main 5, ATQ/CTR/DEF = X (0 dans `desc`).


def GetAbilities() -> Sequence['Ability']:

    def x_icones(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = effect.this.CastTo(Hero).GetControlByPlayer()
        ui.extend(CartesSousGlimpse(joueur))
        return IconesSousGlimpse(joueur)

    def donner_une_autre(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        joueur = effect.GetInitiator()
        ennemi = message.being_message.by_face
        if joueur is None or ennemi is None:
            return
        pile = ennemi.components.boostable.GetDeck()
        avant = list(pile.Get())
        ennemi.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, message.would_message)
        nouvelles = [f for f in pile.Get() if f not in avant]
        if not nouvelles:
            return
        nouvelle = nouvelles[0]

        def defausser_la_retournee(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            message.CancelAllBoostIcons(effect)
            message.CancelBoostAbility(effect)

        def defausser_la_nouvelle(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.DiscardAll([nouvelle], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard the boost card that was turned faceup",
                defausser_la_retournee,
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Discard the other boost card (still facedown)",
                defausser_la_nouvelle,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.ThisGainKeyword(
            x_icones,
            attack=1,
            thwart=1,
            defense=1,
            change_on_event=[OnEvent.PlacedCard("Identity"), OnEvent.CardInPlay(CardFinder(name=NOM_GLIMPSE))],
        ).SetName("X"),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            None,
            donner_une_autre,
        ).LimitOncePerPhase(),
    ]
