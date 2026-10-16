from . import *

# * Mona Lisa — SOUTIEN 0 [mental], aspect Justice (MC Custom Content, Inkwire). PERSONA. NYC.
# Response: After Mona Lisa enters play, choose a [[THWART]] event in your discard pile and tuck it here.
# Action: Play the card tucked here (paying its cost). Then, discard Mona Lisa.
#
# MOT-CLE (fiche lue AVANT le code) : TUCK — docs/reference/mots-cles/tuck.md : `TuckCardUnderHere(faces,
# effect)` range la carte dans la zone `PlaceCardArea` de Mona Lisa (hors jeu).
#
# CARTES DE REFERENCE
#  - `60030` Contingency Planning : glisser une carte sous un soutien/amelioration (`TuckCardUnderHere`) et
#    lire la zone (`GetPlacedCardArea().Get()`).
#  - `ar007` / `25001a` : « play <that card> (paying its cost) » = `joueur.PlayCardsLikeInTurn([face],
#    effect)` (cout PAYE, la carte est jouee comme si elle etait en main ; refus ou cout impayable : elle
#    reste ou elle est, `if_not_play_discard_it` ne vise que la zone de traitement).
#  - RECETTES §1 : « After <carte> enters play » = `AfterCardEnterPlay(Response, "This", op)`.
#
# ⚠ PAS d'`AttachedCardCanPlayLikeInHand` : le texte n'autorise PAS a jouer la carte glissee « comme si elle
#   etait en main » a tout moment (Donatello's Shell, Echo) ; il donne UNE Action de Mona Lisa qui la joue,
#   puis defausse Mona Lisa.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « choose a THWART EVENT in YOUR discard pile » : type Event ET trait THWART, ta defausse seulement.
#    Aucune carte de ce genre : la Reponse n'est pas proposee (rien a glisser).
#  ⚠ « Action » (pas Hero Action) : jouable dans les deux formes ; c'est la carte glissee qui impose ses
#    propres conditions de jeu (un evenement « Hero Action » n'est jouable qu'en forme heros).
#  ⚠ « (paying its cost) » : cout normal de la carte glissee.
#  ⚠ « Then, discard Mona Lisa » : apres la tentative de jeu, Mona Lisa est defaussee (la carte glissee
#    qui n'a pas ete jouee part avec elle, en defausse : `PlaceCardArea` suit sa porteuse).
#  ⚠ L'Action n'est offerte que s'il y a une carte glissee (« the card tucked here »).
#  Aucune limite imprimee.


def CarteGlissee(this: 'CardFace') -> 'CardFace|None':
    glissees = this.GetPlacedCardArea().Get()
    return glissees[0] if glissees else None


def GetAbilities() -> Sequence['Ability']:

    def glisser(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        if effect.targets:
            this.TuckCardUnderHere(list(effect.targets)[:1], effect)

    def jouer_la_carte(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = effect.GetInitiator()
        face = CarteGlissee(this)
        if joueur is not None and face is not None:
            joueur.PlayCardsLikeInTurn([face], effect)
        if this.IsInPlay():
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            glisser,
        ).SetTarget(finder=CardFinder(card_type=Event, trait="THWART"), from_where=["YourDiscardPile"],
                    range=(1, 1)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            jouer_la_carte,
            conditions=[lambda effect, message: CarteGlissee(effect.this) is not None],
        ),
    ]
