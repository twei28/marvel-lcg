from . import *

# * Victoria Hand — SOUTIEN, cout 1, RES [mental]. PERSONA. REGISTERED.
# Action: Exhaust this card -> choose:
#   • Look at the top card of the REGISTERED deck. You may discard that card.
#   • Shuffle the topmost minion from the encounter discard pile into the
#     REGISTERED deck.
#
# ⚠⚠ C'EST LA SEULE CARTE QUI PILOTE LE DECK REGISTERED. Sans elle on subit
# l'ordre du paquet ; avec elle on jette un sbire trop cher et on recycle celui
# qu'on vient de vaincre. Les deux options tirent dans le meme sens.
#
# CARTES DE REFERENCE
#  - `ag004` Infiltrate : `joueur.LookAtDeck(deck, 1, effect)` — REGARDER
#    n'est pas DEFAUSSER, la carte reste en place — puis
#    `MayChooseOneAbility` + `Faces.DiscardAll` pour la defausse facultative.
#    ⚠ `LookAtDeck` accepte un `Deck` en premier argument, pas seulement le
#    litteral "EncounterDeck" (player_action.py:1143). On lui passe donc
#    directement `DeckRegistered(joueur)`.
#  - `ip001b` Norman Osborn : `Faces.ShuffleAllTo(..., DeckRegistered(...))`.
#
# TEXTE CONTRE CODE
#  ⚠ « choose: » -> UNE des deux options, obligatoirement, une fois l'Action
#    declenchee. `ChooseAbilities(..., forced=True)`, pas
#    `MayChooseOneAbility` : le « you may » de la carte ne porte que sur la
#    DEFAUSSE a l'interieur de la premiere option.
#  ⚠ « the TOPMOST MINION from the encounter discard pile » : le dernier sbire
#    defausse, pas un au choix. D'ou `Get(from_top=True)` puis `[0]` des
#    SBIRES seulement — une traitrise au-dessus de la pile ne bloque rien, on
#    descend jusqu'au premier sbire.
#    ⚠ On lit la defausse par `Worlds.GetEncounterDiscardPile(effect)` et NON
#    par `GetEncounterDiscardPileCards`, dont les deux branches n'ont pas le
#    meme sens de lecture (worlds.py:369, `.Get(True)` cote vilain, `.Get()`
#    cote scenario). Ici le SENS EST LE SUJET DE LA PHRASE.
#  ⚠ « SHUFFLE ... into » : le sbire est melange dans le deck REGISTERED, il
#    n'est pas pose sur le dessus. On ne choisit pas quand il reviendra.
#  ⚠ Une option sans matiere n'est pas proposee : deck REGISTERED vide, ou
#    aucun sbire en defausse de rencontre. Sans les deux, l'Action ne fait
#    rien plutot que de planter.


def GetAbilities() -> Sequence['Ability']:

    def sbire_du_dessus_de_la_defausse(effect: 'Effect') -> 'CardFace|None':
        defausse = Worlds.GetEncounterDiscardPile(effect)
        for face in defausse.Get(from_top=True):
            if Minion.IsType(face):
                return face
        return None

    def victoria_hand(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def regarder(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            faces = joueur.LookAtDeck(DeckRegistered(joueur), 1, effect)
            if not faces:
                return
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard that card",
                    lambda targets: Faces.DiscardAll(faces, effect),
                ).SetHasNoTargetEffect(),
            )

        def recycler(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            sbire = sbire_du_dessus_de_la_defausse(effect)
            if sbire is None:
                return
            Faces.ShuffleAllTo([sbire], DeckRegistered(joueur), effect)

        options: List['Ability'] = []
        if DeckRegistered(joueur).GetSize() > 0:
            options.append(
                AbilityFactory.ForChoiceAbility(
                    "Look at the top card of the REGISTERED deck. You may discard that card",
                    regarder,
                ).SetHasNoTargetEffect())
        if sbire_du_dessus_de_la_defausse(effect) is not None:
            options.append(
                AbilityFactory.ForChoiceAbility(
                    "Shuffle the topmost minion from the encounter discard pile into the REGISTERED deck",
                    recycler,
                ).SetHasNoTargetEffect())
        if not options:
            return
        joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            victoria_hand,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
