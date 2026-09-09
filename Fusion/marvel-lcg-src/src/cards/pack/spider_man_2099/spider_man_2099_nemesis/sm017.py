from . import *

# Charged — ATTACHEMENT nemesis. Boost 1.
# Attach to your identity.
# Forced Response: After you discard any number of cards from the top of your
#   deck, take 1 indirect damage.
# Hero Action: Choose to either take 2 indirect damage or discard a card you
#   control with a printed [energy] resource -> discard this card.
#
# CARTES DE REFERENCE
#  - `aa018` (nemesis d'Agatha), `av016` : « Attach to your identity » =
#    `AttachToFaceWhenPutIntoPlay("YourIdentity")`.
#  - `Deck.DiscardCardsInternal` (deck.py:424) et `Deck.DiscardUntil`
#    (deck.py:480) envoient tous deux **un seul** `Message.AfterCardsMoved`
#    PAR LOT, avec `by_discard=True` : c'est exactement le grain de « any
#    NUMBER of cards ». La fabrique est `AfterCardsMoved(ForcedResponse, None,
#    op)`.
#  - `al022`, `16026` : `identite.TakeIndirectDamage(this, N, effect)`.
#  - `22005`, `08013` : le « choose either A or B » par `ChooseAbilities` +
#    deux `ForChoiceAbility`, la seconde portant son propre coût.
#  - `45014` : `CostFunc.Discard(...)` avec `has_printed_res` pour « a card
#    with a printed [energy] resource », pose par `.SetCostFunc()` sur la
#    branche de choix.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « ANY NUMBER OF CARDS » : UN declenchement par LOT defausse, pas un par
#    carte. C'est toute la difference entre `AfterCardsMoved` (un message pour
#    le lot) et `AfterCardDiscard` (un par carte) : avec le second, une
#    Acceleration qui traverse 4 cartes infligerait 4 degats au lieu d'1.
#  ⚠ « FROM THE TOP OF YOUR DECK » : la defausse doit venir du DECK du joueur,
#    pas de sa main ni du jeu. On lit `message.face_areas`, qui donne la zone
#    d'ORIGINE de chaque carte (`sender_card.py:855`), et non `into_areas`.
#  ⚠ Et « YOUR deck » = celui du joueur A QUI cette carte est attachee. Une
#    carte de rencontre n'a pas de controleur joueur (lecon `bl011` The
#    Thirst) : on passe par l'hote de l'attachement.
#  ⚠ La capacite se declenche AUSSI sur les defausses du HEROS lui-meme —
#    l'Acceleration en tete. C'est le propos de la carte : elle punit
#    precisement ce que le heros fait tout le temps. Ne pas la borner a la
#    nemesis.
#  ⚠ « FORCED Response » : pas de choix, elle part toute seule.
#  ⚠ « discard a card YOU CONTROL with a printed [energy] resource » : une
#    carte EN JEU sous son controle, pas une carte en main (piege `wd165`,
#    PROCESSUS-CARTE §5 : `you control` a une portee precise).
#  ⚠ « → discard this card » : la fleche fait des DEUX branches un cout ; ce
#    qui suit est l'effet, c'est-a-dire se debarrasser de Charged. Les deux
#    branches y menent, seul le prix change.
#  ⚠ « Hero Action » : pas disponible en forme civile.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def joueur_porteur(effect: 'Effect') -> 'Player|None':
        hote = Hote(effect.this)
        if hote is None:
            return None
        joueur = hote.GetControlByPlayer()
        return joueur if EstJoueur(joueur) else None

    def depuis_mon_deck(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        """« ANY NUMBER OF CARDS FROM THE TOP OF YOUR DECK » : au moins une
        carte du lot vient du deck du joueur porteur, et le lot est bien une
        DEFAUSSE."""
        joueur = joueur_porteur(effect)
        if joueur is None:
            return False
        deck = getattr(joueur, "player_deck", None)
        defausse = getattr(joueur, "discard_pile", None)
        if deck is None or defausse is None:
            return False

        # ⚠⚠ NE PAS LIRE `message.by_discard` : le constructeur d'
        # `AfterCardsMoved` accepte bien ce parametre, mais **ne le stocke
        # PAS** — seul `by_shuffle` devient un attribut (sender_card.py:860).
        # Un `getattr(message, "by_discard", False)` rend donc toujours None,
        # la condition est toujours fausse, et la Reponse Forcee ne part
        # JAMAIS. Mesure du 08/09/2026 : l'abilite etait bien declenchee 13
        # fois, avec le bon hote et le bon joueur, et ce seul test l'arretait
        # (0 degat au lieu de 1, « rouges 0/1 » a la substitution).
        # On lit donc le MOUVEMENT reel : partie du deck, arrivee en defausse.
        for face, zone in message.face_areas.items():
            vient_du_deck = zone is deck or getattr(
                getattr(zone, "flags", None), "is_player_deck", False)
            arrive_en_defausse = face.card.area is defausse
            if vient_du_deck and arrive_en_defausse:
                return True
        return False

    def decharge(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        joueur = joueur_porteur(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 1, effect)

    def se_defausser(effect: 'Effect') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)

    def encaisser(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
        this = effect.this.CastTo(Attachment)
        Unused(cibles)
        joueur = joueur_porteur(effect)
        if joueur is not None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 2, effect)
        se_defausser(effect)

    def purger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = joueur_porteur(effect)
        if joueur is None:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 2 indirect damage",
                lambda cibles: encaisser(effect, cibles),
            ),
            # ⚠ PAS `ForChoiceAbilityWithCost` : son premier argument est un
            # `Cost` (des RESSOURCES a depenser), pas un `CostFunc`. Lui passer
            # un `CostFunc.Discard` leve `TypeError: 'Discard' object is not
            # callable` — que le moteur AVALE, si bien que l'Action entiere ne
            # fait plus rien (mesure du 08/09/2026 : 0 degat, carte toujours en
            # jeu). Un cout NON-RESSOURCE sur une branche de choix passe par
            # `.SetCostFunc(...)`. (RECETTES §5 ne parlait que de `SetCost`,
            # qui lui leve un assert explicite du moteur.)
            AbilityFactory.ForChoiceAbility(
                "Discard a card you control with a printed [energy] resource",
                lambda cibles: se_defausser(effect),
            ).SetCostFunc(CostFunc.Discard(
                "YouControlCards",
                has_printed_res="Y",
            )),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),

        AbilityFactory.AfterCardsMoved(
            AbilityType.ForcedResponse,
            None,
            decharge,
            conditions=[depuis_mon_deck],
        ),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            purger,
        ).SetName("Charged"),
    ]
