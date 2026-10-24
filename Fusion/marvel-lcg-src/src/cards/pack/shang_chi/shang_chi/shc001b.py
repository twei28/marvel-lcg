from . import *

# * Shang-Chi (face ALTER-EGO) — MARTIAL ARTIST. PV 9, REC 4, main 6.
# Multiple Forms — You may include up to 3 copies of 1 ATTACK event from each aspect other than your chosen aspect.
# Meditate — Response: After you change to this form, shuffle a card from State of Flow into your deck.
# (+ mise en place : State of Flow, Permanent. Setup., entre en jeu.)
#
# Cartes de reference :
#  - Setup d'une carte mise de cote : `36001b` * Ororo Munroe (storm) : `BeginGameWithSetAside([...])` +
#    `WhenCardSetup("This", op)` puis `PutIntoPlay`. State of Flow est « Permanent. Setup. » et n'est PAS une des 15 cartes
#    du deck de heros (les impressions sont numerotees 1/15 a 15/15 sans elle) : elle part de cote.
#  - Response au changement de forme : `tc001b` * Casey Jones : `AfterUnitChangeForm(Response, "You", op, to_this_form=True)`.
#  - choix dans une liste donnee : `tc001b` (`ForChoiceAbility(...).SetTarget(liste, range=(1, 1), not_move=True)`).
#  - Multiple Forms (CONSTRUCTION de deck, pas une capacite de jeu) : `metadata.deckbuilding.hors_aspect` du deck de
#    depart, lu par `public/js/deckbuilder/regles.js` (`quotaHorsAspect`, etendu au quota PAR ASPECT).
#
# ⚠ Mots-pieges :
#  - « shuffle A CARD from State of Flow » : DECISION UTILISATEUR (24/10/2026) = une carte AU CHOIX de la pile (pas celle
#    du dessus, pas toute la pile). Pile vide : rien.
#  - « After you change TO THIS FORM » : `to_this_form=True` ; au Setup la partie commence en alter-ego sans changement.
#  - la pile garde ses autres cartes ; la carte choisie est melangee dans LE DECK DU JOUEUR (pas la defausse).
#  - « Multiple Forms » n'a aucun code de jeu : il se prouve cote constructeur (cas Node regles-deck).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None or LaPile(joueur) is not None:
            return
        candidates = list(joueur.set_aside_deck.Get()) + list(joueur.additional_discard_pile.Get())
        for face in candidates:
            if face.paper.card_id == ID_PILE:
                face.CastTo(Support).PutIntoPlay(joueur, effect)
                return

    def meditate(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        cartes = CartesDeLaPile(joueur)
        if not cartes:
            return

        def melanger(cibles: Sequence['CardFace']) -> None:
            Faces.ShuffleAllTo(list(cibles), joueur.player_deck, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Shuffle a card from State of Flow into your deck",
                melanger,
            ).SetTarget(cartes, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.BeginGameWithSetAside([ID_PILE]),
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            meditate,
            to_this_form=True,
        ).SetName("Meditate"),
    ]
