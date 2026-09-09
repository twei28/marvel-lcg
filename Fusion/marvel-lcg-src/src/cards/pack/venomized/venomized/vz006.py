from . import *

# * Venom (Eddie Brock) — ALLIE, cout 2, PV 3, CTR 1* / ATQ 2*. SYMBIOTE.
# Venom gets +1 ATK for each Venomized (black) card tucked under it.
# Response: After you defeat a minion, tuck a card from your hand under here.
#
# CARTES DE REFERENCE
#  - `su012` Contingency Plan (pack superior_spider_man) : la lecture d'une
#    zone de cartes POSEES DESSOUS. ⚠⚠ `Get(True)` et non `Get()` — le
#    drapeau demande aussi les cartes FACE CACHEE, et c'est ainsi qu'une
#    carte glissee est posee. Sans lui la zone parait vide.
#  - `CardFace.TuckCardUnderHere` (`card_face.py:1032`) : un
#    `PlaceCardHere(..., face_up=False)` nomme, exactement le geste imprime.
#  - `48021` Gambit : le modele d'une caracteristique qui compte ce qui est
#    pose sous la carte (`get_new_value`).
#
# TEXTE CONTRE CODE
#  ⚠ « +1 ATK for each VENOMIZED (black) card » : on ne compte PAS toutes les
#    cartes glissees, seulement celles de l'aspect. Une carte basique glissee
#    ne donne rien — et le texte invite quand meme a la glisser, puisque la
#    seconde phrase, elle, ne filtre pas.
#  ⚠ « After YOU defeat a minion » : c'est le JOUEUR qui met K.O., par
#    n'importe quel moyen, pas Venom lui-meme. `AfterUnitDefeatedUnit` avec
#    l'attaquant « You », et non « This ».
#  ⚠ « tuck a card from your hand » : la joueuse choisit, et rien ne
#    l'oblige — main vide, rien ne se passe.
def GetAbilities() -> Sequence['Ability']:

    def cartes_glissees_venomized(effect: 'Effect', this: 'CardFace',
                                  attaches: List['CardFace']) -> int:
        Unused(effect, attaches)
        lire = getattr(this, "GetPlacedCardArea", None)
        if lire is None:
            return 0
        return len([c for c in lire().Get(True)
                    if c is not None and EstUneCarteVenomized(c)])

    def venom(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        main = list(joueur.hand_cards.Get())
        if not main:
            return

        def glisser(cibles: Sequence['CardFace']) -> None:
            this.TuckCardUnderHere(list(cibles), effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Tuck a card from your hand under Venom", glisser,
            ).SetTarget(main, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "This",
            get_new_value=cartes_glissees_venomized,
            attack=0,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            venom,
        ),
    ]
