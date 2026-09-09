from . import *

# Star Jump — EVENEMENT, cout X, [mental]. TACTIC. x2.
# Action: Choose X of the following:
#   • Seek a minion from the encounter deck and put it into play engaged with
#     you -> ready Skuttlebutt.
#   • Find a Beta Ray Bill card and add it to your hand.
#   • Ready Beta Ray Bill.
#
# ⚠ LA SEULE CARTE QUI REDRESSE SKUTTLEBUTT. br007 dit « does not ready at the
# end of the player phase » : sans cette premiere branche, le vaisseau ne sert
# qu'une fois par partie. Et le prix a payer est de CONVOQUER UN SBIRE.
#
# CARTES DE REFERENCE
#  - `14006` Speed Cyclone : le cout X (`effect.GetCostX()`).
#  - `br011` Hammer Time : la convocation d'un sbire depuis le deck rencontre.
#    ⚠ Hammer Time imprime « SEARCH the encounter deck », pas « seek » : elle
#    n'est PAS concernee par le correctif du 08/09/2026 (tableau de
#    `mots-cles/seek.md`).
#
# TEXTE CONTRE CODE
#  « Choose X OF THE FOLLOWING » -> X branches parmi trois, et rien n'interdit
#    de reprendre la meme deux fois : le texte ne dit pas « different ». On
#    ouvre donc le choix X fois de suite.
#  « ACTION » et non « Hero Action » -> jouable AUSSI en forme civile, ce qui
#    est coherent avec `Starfarer` (br001b), qui va la chercher.
#  « a BETA RAY BILL card » -> `IsDeckBuildingClass`, la primitive du moteur,
#    et non une comparaison de `set_name` a la main.
#  ⚠ « Ready BETA RAY BILL » vise l'IDENTITE, dont les deux faces portent le
#    meme nom : on redresse celle qui est en jeu, quelle qu'elle soit.


def GetAbilities() -> Sequence['Ability']:

    def saut_stellaire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        x = effect.GetCostX()
        if x <= 0:
            return

        def convoquer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            # ⚠⚠ CORRECTIF DU 08/09/2026 — `seek` N'EST PAS UNE RECHERCHE.
            # L'insert du pack `spider_man_2099` (meme auteur, Rainy) definit
            # enfin le mot-cle : « discards cards from the top of a deck until
            # a certain type of card is discarded ». On defausse donc le dessus
            # du deck rencontre jusqu'a un sbire — les cartes traversees restent
            # dans la defausse rencontre, ce que l'ancienne lecture escamotait.
            # ⚠ La TROISIEME branche, elle, dit « FIND a Beta Ray Bill card » :
            # c'est bien une recherche, et elle N'EST PAS touchee.
            # Arbitrage utilisateur du 08/09/2026. Fiche : `mots-cles/seek.md`.
            sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
            if sbire is not None:
                sbire.PutIntoPlay(joueur, effect)
                if sbire.card.IsOnField():
                    sbire.CastTo(Minion).EngagePlayer(joueur, effect)
            vaisseau = VaisseauEnJeu(effect)
            if vaisseau is not None:
                Faces.ReadyAll([vaisseau], effect)

        def chercher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            face = Search.PlayerCard(
                effect, joueur,
                include_player_deck=True,
                include_discard_pile=True,
                finder=CardFinder(deck_building_class=SET_HEROS),
            )
            if face is not None:
                joueur.GainCard(face, effect)

        def redresser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

        for _ in range(x):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Seek a minion and ready Skuttlebutt", convoquer),
                AbilityFactory.ForChoiceAbility(
                    "Find a Beta Ray Bill card", chercher),
                AbilityFactory.ForChoiceAbility(
                    "Ready Beta Ray Bill", redresser),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            saut_stellaire,
        ).SetPlay(),
    ]
