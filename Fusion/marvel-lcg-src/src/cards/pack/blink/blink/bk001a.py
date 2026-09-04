from . import *

# * Blink (face heros) — X-MEN. THW 2 / ATK 2 / DEF 2, main 5, PV 9.
# Portal Manipulation - Action: Return 1 [[PORTAL]] upgrade from play to your
#   hand. (Limit once per round.)
# Response: After you change to this form, shuffle 1 [[PORTAL]] upgrade from
#   your discard pile into your deck.
#
# TEXTE CONTRE CODE
#  « from PLAY to your HAND » -> `Faces.ReturnToHand`, pas une defausse : le
#    portail est REUTILISABLE, c'est tout l'interet.
#  « (Limit once per round.) » -> `.LimitOncePerRound()`. ⚠ Cette limite etait
#    SILENCIEUSEMENT INERTE avant le correctif moteur du 03/09/2026
#    (once_per.py / GetForDelayAbility) ; elle mord ici parce qu'il s'agit
#    d'une Action ordinaire, non batie sur une DelayAbility.
#  « shuffle 1 ... from your DISCARD PILE into your DECK » -> une SEULE, et
#    depuis la defausse : contraste imprime avec l'alter-ego bk001b, qui en
#    remelange CHACUNE et depuis le JEU.


def GetAbilities() -> Sequence['Ability']:

    def rappeler_un_portail(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        portails = PortailsEnJeu(effect)
        if not portails:
            return
        Faces.ReturnToHand([portails[0]], "Owner", effect)

    def remelanger_un_portail(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for face in joueur.discard_pile.Get(True):
            if face.HasTrait(TRAIT_PORTAIL):
                Faces.ShuffleAllTo([face], joueur.player_deck, effect)
                return

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            rappeler_un_portail,
        ).SetName("Portal Manipulation")
        .LimitOncePerRound(),
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.Response,
            remelanger_un_portail,
        ),
    ]
