from . import *

# * Fantasti-Car — SOUTIEN BASIC, cout 2 [energie]. FANTASTIC FOUR. VEHICLE.
# Response: After Fantasti-Car enters play, ready a FANTASTIC FOUR card.
# Alter-Ego Action: Exhaust Fantasti-Car → choose a player. That player may shuffle
#   1 card from their discard pile into their deck.
#
# Cartes de reference :
#  - **`mf005`** Fantasticar (pack mister_fantastic, autre auteur) : « choose a player » =
#    `.SetTarget("Players")` puis `target.GetControlByPlayer()` ; cout d'inclinaison.
#  - **`27023`** : `AfterCardEnterPlay`/`Response` ; **`an001a`** : `Faces.ReadyAll`.
#  - **`hd001b`** / **`27008`** : `MayChooseFace(...)` + `Faces.ShuffleAllTo(faces, deck, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « ready a FANTASTIC FOUR CARD » : n'importe quelle carte FF en jeu qui peut etre
#    redressee (personnage, soutien, amelioration), pas seulement un personnage.
#  - « After Fantasti-Car ENTERS PLAY » : Reponse a l'entree en jeu ("This").
#  - « ALTER-EGO Action » : forme alter ego seulement ; « choose A PLAYER » : n'importe quel
#    joueur ; « MAY shuffle » : facultatif ; « 1 card ... INTO THEIR DECK » (le deck du joueur
#    choisi, qui melange).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    def recycler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            carte = joueur.MayChooseFace(list(joueur.discard_pile.Get(True)), effect, not_move=True) \
                if joueur.discard_pile.Get(True) else None
            if carte is not None:
                Faces.ShuffleAllTo([carte], joueur.player_deck, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            redresser,
        ).SetTarget(CardFinder(trait="FANTASTIC FOUR", canbe_ready=True)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            recycler,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("Players"),
    ]
