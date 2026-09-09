from . import *

# * Spider-Man (Miguel O'Hara) — HEROS. THW 2 / ATK 2 / DEF 2, main 4, 10 PV.
# WEB-WARRIOR.
# [star] Acceleration — Response: After your hero uses a basic power, seek an
#   event from your deck. You may play that event. Place each other card you
#   discarded this way on the bottom of your deck in the order you discarded
#   them. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `ab001a` * Albert (pack albert) : LE modele d'architecture. Une capacite
#    NOMMEE que d'autres cartes ecoutent s'ecrit
#    `WhenResolveSpecialAbility("This", op).SetName(...)`, et son declencheur
#    imprime est une ability SEPAREE qui appelle `ResolveSpecialAbility`.
#    `ab007` * Donald Pierce ecoute cette capacite depuis une autre carte :
#    c'est exactement ce que font ici sm010, sm011 et sm012.
#  - `14001a`, `tt001a`, `tg001a` : « After your hero uses a basic power » =
#    `AfterUnitUseBasicPower(type, "You", op, powers=["ATK","THW","DEF"])`
#    (RECETTES §1).
#  - `49001a` * Magneto : `DiscardDeckUntil(..., return_other_faces=...)`, le
#    « seek » du deck joueur, avec la liste des cartes traversees.
#  - `15003` Chaos Magic, `bc004` Big Heist, `ar001a` * Ares :
#    `PlayCardsLikeInTurn` pour « you may play that card ».
#  - `ag001b`, `bt011` : `Faces.MoveAllToDeck([...], deck, "Bottom", effect)`,
#    la position en argument POSITIONNEL.
#
# TEXTE CONTRE CODE
#  ⚠ « seek » : mot-cle MAISON, et sa definition est donnee par l'insert de CE
#    pack (fiche `mots-cles/seek.md`, corrigee le 08/09/2026) : « discard cards
#    from the top of a deck until a certain type of card is discarded ». C'est
#    une DEFAUSSE, pas une recherche. `DiscardDeckUntil` fait exactement cela,
#    et defausse aussi la carte trouvee (deck.py:443) — d'ou le fait qu'on la
#    joue depuis la defausse, ce que `PlayCardsLikeInTurn` sait faire.
#  ⚠ « your HERO uses a basic power » : la recuperation n'est pas concernee.
#    Elle a son propre message (`AfterUnitMakeRecovery`, cf. sm001b) et
#    n'existe qu'en alter-ego, ou cette face n'est pas en jeu. `powers` est
#    donc borne a ATK/THW/DEF.
#  ⚠ « You MAY play that event » : `PlayCardsLikeInTurn` sans
#    `ignore_resources_cost` — le cout est du. `forced=True` par defaut ne
#    force PAS quand le cout n'est pas ignore (player_action.py:960), le joueur
#    garde donc bien son choix.
#  ⚠ « each OTHER card » : l'evenement trouve ne part PAS sous le deck. S'il
#    n'est pas joue il reste dans la defausse (`if_not_play_discard_it`).
#    ⚠ SAUF sous Accelerated Vision (sm008), et c'est l'insert qui le dit :
#    « Q: where does that event go? A: Place it on the bottom of your deck with
#    the other discarded cards. » — le premier evenement rejoint alors la pile
#    des cartes traversees.
#  ⚠ « in the order you discarded them » : `return_other_faces` rend deja les
#    cartes dans l'ordre de defausse (deck.py:469-476), on ne trie pas.
#  ⚠ « Limit once per phase » : comptee par le pack et non par
#    `LimitOncePerPhase()`, parce que sm008 en autorise DEUX. Le registre reste
#    celui du moteur (`once_per_phase_player_effects`), vide a chaque fin de
#    phase. Temoin d'epuisement exige (PROCESSUS-CARTE 7 bis).
#  ⚠ Le `[star]` imprime est une convention d'IMPRESSION sur une face heros,
#    pas un `NonKeywordStar` (RECETTES §1). Rien a coder pour lui.
#  ⚠ Les petites etoiles imprimees a cote de THW/ATK/DEF ne sont pas des
#    valeurs de jeu : chez Rainy elles pointent la statistique visee par la
#    capacite etoile de la carte (meme convention que bl001a et bl013, ou elles
#    ont ete ignorees a raison).


def GetAbilities() -> Sequence['Ability']:

    def limite_pas_atteinte(effect: 'Effect', message: Any) -> bool:
        """⚠ LA CONDITION VA ICI, PAS DANS LE CORPS (RECETTES §1) : une Response
        branchee sur un message frequent est PROPOSEE au joueur des que le
        message part. Sans ce filtre, chaque pouvoir de base poserait la
        question meme quand la capacite est epuisee (lecon `bc010`, 250
        questions sur 8 parties)."""
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return UsagesCettePhase(joueur, effect) < LimiteAcceleration(joueur)

    def deck_non_vide(effect: 'Effect', message: Any) -> bool:
        """Rien a defausser, rien a chercher : ne pas proposer la Response."""
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        deck = getattr(joueur, "player_deck", None)
        return deck is not None and deck.GetSize() > 0

    def declencher(effect: 'Effect', message: Any) -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.ResolveSpecialAbility(joueur, effect, name=NOM_ACCEL)

    def acceleration(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        NoterUsage(joueur, effect)
        OuvrirAcceleration(joueur)

        # sm008 Accelerated Vision pose ici son drapeau « tu peux continuer ».
        this.ResolveSpecialAbility(joueur, effect, name=NOM_ACCEL_DEBUT)

        traversees: List['CardFace'] = []
        evenement = joueur.DiscardDeckUntil(
            effect,
            card_type=Event,
            return_other_faces=traversees,
        )

        # « you MAY continue discarding until you discard a DIFFERENT event »
        # (sm008 Accelerated Vision). La question se pose ICI, et pas dans
        # sm008 : au moment ou cette carte-la parle, rien n'a encore ete
        # defausse et le joueur n'a donc rien a arbitrer.
        if evenement is not None and ContinuationAutorisee(joueur):
            premier = evenement

            def continuer(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                nonlocal evenement, traversees
                autres: List['CardFace'] = []
                second = joueur.DiscardDeckUntil(
                    effect,
                    card_type=Event,
                    return_other_faces=autres,
                    check_face_fn=lambda f: f is not premier,
                )
                if second is not None:
                    # L'insert : le PREMIER evenement rejoint les traversees.
                    traversees = traversees + [premier] + autres
                    evenement = second
                else:
                    traversees = traversees + autres

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Keep discarding until a different event (Accelerated Vision)",
                    continuer,
                ),
                AbilityFactory.ForChoiceAbility(
                    "Stop here",
                    lambda cibles: None,
                ),
            )

        NoterDefaussees(joueur, traversees)

        if evenement is not None:
            NoterEventJoue(joueur, evenement)
            joues = joueur.PlayCardsLikeInTurn([evenement], effect)
            if not joues:
                # Non joue : le marqueur ne doit pas rester pose, sinon la
                # prochaine lecture de `JoueViaAcceleration` mentirait.
                NoterEventJoue(joueur, None)

        deck = getattr(joueur, "player_deck", None)
        if deck is not None and traversees:
            Faces.MoveAllToDeck(traversees, deck, "Bottom", effect)

        FermerAcceleration(joueur)
        this.ResolveSpecialAbility(joueur, effect, name=NOM_ACCEL_FINI)

    return [
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            acceleration,
        ).SetName(NOM_ACCEL),

        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            declencher,
            powers=["ATK", "THW", "DEF"],
            conditions=[limite_pas_atteinte, deck_non_vide],
        ).SetName(NOM_ACCEL),
    ]
