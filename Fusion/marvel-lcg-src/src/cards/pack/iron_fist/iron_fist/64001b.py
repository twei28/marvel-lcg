from . import *

# * Danny Rand (face alter ego, 1B) — CIVILIAN. PV 10, REC 4, main 6.
# Your Technique cards lose temporary.
# Meditation — Action: Search your deck and discard pile for a Technique card. Put that
#   card into play. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - « lose(s) the temporary keyword » en continu : `cyclops/33004` Field Commander
#    (`GiveKeywordToInPlayWhenApplyThis(CardFinder(...), temporary=-1)`).
#  - « Search your deck and discard pile for X and put it into play » : `bp/51025` Heart of the
#    Panther et `kate_bishop/kb001b` (`Search.PlayerCard(..., include_player_deck=True,
#    include_discard_pile=True)` puis `face.PutIntoPlay(joueur, effect)`).
#  - « (Limit once per phase.) » : `phoenix/34001a` (`LimitOncePerPhase()`).
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR Technique cards » : `control_by="You"` ; le trait, jamais le nom.
#  ⚠ « lose temporary » : capacite CONTINUE de la face Danny Rand seulement. Au retournement en
#    Iron Fist, la face qui la porte n'est plus visible : les Techniques redeviennent Temporary et
#    partent a la fin du round (`ProcessTemporary`) — decision utilisateur n°2.
#  ⚠ « Put that card into play » : sans paiement ; une amelioration sans cible imprimee s'attache a
#    l'identite du joueur (selecteur par defaut de `CanPlayThisUpgradeCard`, play.py) — decision n°1.
#  ⚠ « deck AND discard pile » : les deux zones ; deck remelange (comportement par defaut).
#  ⚠ « Action » nue imprimee sur l'alter ego : utilisable en forme Danny Rand seulement (la face).
#  ⚠ « Limit once per phase » : temoin d'epuisement dans les cas.


def GetAbilities() -> Sequence['Ability']:

    def meditation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            trait=TRAIT_TECHNIQUE,
        )
        if face:
            face.PutIntoPlay(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Upgrade, trait=TRAIT_TECHNIQUE),
            control_by="You",
            temporary=-1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            meditation,
        ).SetName("Meditation")
        .LimitOncePerPhase(),
    ]
