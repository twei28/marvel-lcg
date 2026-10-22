from . import *

# * Clint Barton (MC×DC 2026) — face ALTER-EGO (p283). REC 3, main 6, 9 PV. S.H.I.E.L.D. SPY.
# Response : After you change to this form, shuffle 2 ARROW cards from your discard pile into your deck.
# Action : Spend 1 resource of any type -> find either Hawkeye's Bow or Hawkeye's Quiver and put it into play. (Limit once per phase.)
#
# Cartes de reference : trors/hawkeye/04001b (le Clint Barton OFFICIEL : « Weapon of Choice », `Search.PlayerCard(include_player_deck, include_discard_pile, name=BOW)`,
# `Cost("1")`, `LimitOncePerPhase`), nebu/nebula/22009 (« Shuffle up to 2 ... from your discard pile into your deck » : `SetTarget(..., from_where=["YourDiscardPile"],
# range=...)` + `Faces.ShuffleAllTo(targets, joueur.player_deck, effect)`), core/01019a (`AfterUnitChangeForm(Response, "You", op, to_this_form=True)`).
# ⚠ Mots-pieges : « After you change TO THIS FORM » (pas au depart de la partie : ce n'est pas un changement) ; « shuffle 2 » = DEUX, ni plus ni moins, mais « autant
# que possible » s'il y en a moins (RR : un effet se resout autant qu'il le peut) -> minimum = min(2, ARROW en defausse) ; « ARROW cards » = le trait, tout type ;
# « find » = deck ET defausse, comme le Weapon of Choice officiel ; « put it into play » (pas en main) et SANS payer son cout ; « either ... or » = UN seul des deux,
# au choix du joueur, parmi ceux qui ne sont pas deja en jeu (uniques) ; « Limit once per PHASE ».


def GetAbilities() -> Sequence['Ability']:

    def arcs_en_defausse(joueur: 'Player') -> List['CardFace']:
        return [f for f in joueur.discard_pile.Get() if f.HasTrait("ARROW")]

    def melanger(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        arcs = arcs_en_defausse(joueur)
        if not arcs:
            return
        # DEUX, ou autant que la defausse en contient (RR : un effet se resout autant qu'il le peut). Le moteur ne sait pas borner un minimum
        # a « min(2, legales) » dans `SetTarget` : le choix se fait ici.
        n = min(2, len(arcs))
        choisies = joueur.AskChooseFaces(arcs, (n, n), effect, not_move=True)
        if choisies:
            Faces.ShuffleAllTo(list(choisies), joueur.player_deck, effect)

    def trouver(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def mettre_en_jeu(nom: str) -> None:
            face = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True, name=nom, card_type=Upgrade)
            if face:
                face.PutIntoPlay(joueur, effect)

        choix = [AbilityFactory.ForChoiceAbility(f"Put {nom} into play", lambda cibles, nom=nom: mettre_en_jeu(nom))
                 for nom in (HAWKEYE_BOW_NAME, HAWKEYE_QUIVER_NAME) if EnJeu(joueur, nom) is None]
        if choix:
            joueur.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.AfterUnitChangeForm(AbilityType.Response, "You", melanger, to_this_form=True),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, trouver)
        .SetCost(Cost("1"))
        .LimitOncePerPhase(),
    ]
