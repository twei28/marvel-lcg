from . import *

# Wall Crawling — EVENEMENT, cout 1 [mental]. SUPERPOWER. THWART.
# Hero Action (thwart): Remove 2 threat from a scheme (3 threat instead if you
#   played this card using your Acceleration ability). You may place this
#   event on the bottom of your deck.
#
# CARTES DE REFERENCE
#  - `05015` Tackle / `ho003` pour la forme « Hero Action (thwart) » sur un
#    evenement, `SetLabel('thwart')`.
#  - `an004`, `vp001a` : `this.RemoveThreatFromSchemes(cibles, n, effect)`.
#  - `ag001b`, `bt011` : `Faces.MoveAllToDeck([face], deck, "Bottom", effect)`,
#    position en argument POSITIONNEL.
#
# TEXTE CONTRE CODE
#  ⚠ « Remove 2 threat from A SCHEME » : une cible au choix, complot principal
#    ou annexe — pas « the main scheme ».
#  ⚠ « 3 threat INSTEAD » : remplacement, pas addition. 3, jamais 2+3.
#  ⚠ « YOU MAY place this event on the bottom of your deck » : optionnel, donc
#    une question. C'est ce qui fait de Wall Crawling la carte que
#    l'Acceleration recycle indefiniment — et c'est aussi elle que vise le
#    troisieme Q/R de l'insert (« Wall Crawling resolves first so it goes on
#    the bottom of your deck, followed by the other cards you discarded »).
#    ⚠ L'ORDRE COMPTE, et il est deja bon : cet evenement se resout A
#    L'INTERIEUR de `PlayCardsLikeInTurn`, donc AVANT que `sm001a` ne renvoie
#    les cartes traversees sous le deck. La carte se place donc la premiere,
#    exactement comme l'insert le dit. Rien de special a coder pour cela, mais
#    c'est a VERIFIER par un cas (l'ordre du deck, pas seulement la presence).
#  ⚠ « place this EVENT » : c'est `this`, la carte elle-meme, qui est en cours
#    de resolution. Sans ce deplacement elle irait a la defausse comme tout
#    evenement joue.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def ramper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)

        menace = 3 if JoueViaAcceleration(effect) else 2
        this.RemoveThreatFromSchemes(effect.targets, menace, effect)

        if joueur is None:
            return
        deck = getattr(joueur, "player_deck", None)
        if deck is None:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place Wall Crawling on the bottom of your deck",
                lambda cibles: Faces.MoveAllToDeck([this], deck, "Bottom", effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Leave Wall Crawling in your discard pile",
                lambda cibles: None,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ramper,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
