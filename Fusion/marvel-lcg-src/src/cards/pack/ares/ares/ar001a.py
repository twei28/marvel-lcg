from . import *

# * Ares — HEROS. THW 1 / ATK 3 / DEF 2, main 4, 14 PV. AVENGER. OLYMPUS.
# Bring the War — Action: Seek a minion from the encounter deck and put it
#   into play engaged with you -> draw 2 cards or play an event from your hand,
#   ignoring its resource cost. (Limit once per round.)
#
# ⚠⚠ LES DEUX FACES S'APPELLENT « ARES » (comme Beta Ray Bill), et « * Ares »
# est DEJA `59036`, un sbire du set Hercules Nemesis : l'identite se retrouve
# par le TYPE, jamais par le nom (helper `HerosDuJoueur`).
#
# CARTES DE REFERENCE
#  - `56007` Hunted (pack cw/tigra) : « seek a minion ... put it into play
#    engaged with you » EN COUT, par `CostFunc.SearchForCard(Minion,
#    "PutIntoPlayEngagedYou", include_encounter_deck=True)`, et le sbire
#    convoque relu dans `effect.cost_func.Get(CostFunc.SearchForCard)
#    .searched_faces`.
#  - `br005` Star Jump / `br011` Hammer Time (pack beta_ray_bill) : la
#    lecture du mot-cle maison `seek` (fiche `mots-cles/seek.md`, creee pour
#    ce pack) et l'engagement explicite `EngagePlayer`.
#  - `15003` Chaos Magic / `bc004` Big Heist : « play ... ignoring its resource
#    cost » = `PlayCardsLikeInTurn(..., ignore_resources_cost=True)` sur une
#    carte choisie par `SetTarget(canbe_play=True, from_where=["YourHandCards"])`.
#  - `08013` Stealth Strike : le choix a deux branches dans l'operation.
#
# TEXTE CONTRE CODE
#  ⚠ « ACTION », pas « Hero Action » : mais la capacite vit sur la face HEROS,
#    donc elle n'existe qu'en forme heros. Rien a ajouter.
#  ⚠ « Seek a minion ... → » : la convocation est le COUT, la fleche le dit.
#    ⚠⚠ Depuis le 08/09/2026 elle est ecrite DANS l'operation et non plus par
#    `CostFunc.SearchForCard` : `seek` DEFAUSSE le dessus du deck rencontre
#    jusqu'a un sbire (definition de l'auteur, enfin trouvee dans l'insert de
#    spider_man_2099). La `conditions=[deck_rencontre_a_un_sbire]` reste la
#    garantie que l'action n'est pas offerte pour rien, exactement comme quand
#    c'etait un cout.
#    ⚠ RECETTES §5 : un cout `SearchForCard` est OFFERT meme si le deck
#    rencontre n'a aucun sbire (`HasTargets` rend vrai sur `Select.From("This")`)
#    — d'ou `conditions=[deck_rencontre_a_un_sbire]`, sans quoi l'action serait
#    proposee, le cout echouerait et la limite par round serait consommee pour
#    rien.
#  ⚠ « ENGAGED WITH YOU » : `PutIntoPlay(joueur)` engage deja un sbire
#    (minion.py:61, RECETTES §1), on engage quand meme explicitement comme
#    `br011`, ce qui est neutre si c'est deja fait.
#  ⚠ « draw 2 cards OR play an event » : DEUX branches, une seule resolue. La
#    seconde n'est offerte que s'il y a un evenement jouable en main (le
#    selecteur n'a pas de cible sinon).
#  ⚠ « ignoring its RESOURCE cost » : les autres couts (inclinaison, etc.)
#    restent dus, c'est exactement `ignore_resources_cost=True`.
#  ⚠ « Limit once per round » -> `LimitOncePerRound()` ; temoin d'epuisement
#    exige (PROCESSUS-CARTE 7 bis).


def GetAbilities() -> Sequence['Ability']:

    def deck_rencontre_a_un_sbire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        deck = Worlds.GetEncounterDeck(effect)
        if deck is None:
            return False
        return any(f is not None and Minion.IsType(f) for f in list(deck.GetAll()))

    def apporter_la_guerre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # ⚠⚠ CORRECTIF DU 08/09/2026 — `seek` N'EST PAS UNE RECHERCHE.
        # L'insert du pack `spider_man_2099` (meme auteur) definit enfin le
        # mot-cle : « discards cards from the top of a deck until a certain type
        # of card is discarded ». On DEFAUSSE donc le dessus du deck rencontre
        # jusqu'a en defausser un sbire, puis on met CE sbire en jeu engage.
        # Les cartes traversees restent dans la defausse rencontre : c'est tout
        # le cout que l'ancienne lecture (`CostFunc.SearchForCard`) escamotait.
        # Arbitrage utilisateur du 08/09/2026 : corriger partout.
        # Fiche : `docs/reference/mots-cles/seek.md`.
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None:
            sbire.PutIntoPlay(joueur, effect)
            if Minion.IsType(sbire) and sbire.card.IsOnField():
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)

        def piocher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.DrawUp(2, effect)

        def jouer_sans_payer(cibles: Sequence['CardFace']) -> None:
            faces = [c for c in cibles if c is not None]
            if faces:
                joueur.PlayCardsLikeInTurn(faces, effect, ignore_resources_cost=True)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Draw 2 cards", piocher),
            AbilityFactory.ForChoiceAbility(
                "Play an event from your hand, ignoring its resource cost",
                jouer_sans_payer,
            ).SetTarget(Event, canbe_play=True, from_where=["YourHandCards"]),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            apporter_la_guerre,
            conditions=[deck_rencontre_a_un_sbire],
        ).SetName("Bring the War")
        .LimitOncePerRound(),
    ]
