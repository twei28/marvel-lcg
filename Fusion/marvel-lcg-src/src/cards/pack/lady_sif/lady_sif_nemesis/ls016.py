from . import *

# Hypnotic Suggestion — ATTACHEMENT nemesis (N 4/5). TEMPTATION.
# 1 icone de boost.
# Attach to your identity.
# Forced Action: Exhaust this card -> draw 1 card, then play that card
#   (paying its costs). If you cannot, place 2 threat on the main scheme.
# Alter-Ego Action: Exhaust this card and spend a [mental] resource ->
#   discard this card.
#
# Cartes de reference :
#  - **`55008b` Trance of Greed** (pack enchantress), jumeau de la premiere
#    capacite au repli pres : meme `WhenInYourPlayTurn(ForcedAction, op)` +
#    `CostFunc.Exhaust("This")`, et surtout meme couple
#    `player.DrawUp(1, effect)` puis `player.PlayCardsLikeInTurn(faces,
#    effect)`, dont le RETOUR dit si la carte a pu etre jouee. Chez elle le
#    repli est 1 degat ; ici, 2 menaces ;
#  - `02048` All Tied Up pour `AttachToFaceWhenPutIntoPlay("YourIdentity")` et
#    pour `PlayerActionToDiscardThis(...)` paye en ressources.
#
# ⚠ HOMONYME : `ag014` Hypnotic Suggestion est une TRAITRISE du pack maison
# agent_13. Deux cartes distinctes de meme nom, dans deux packs maison.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - `Forced Action` : la phase du joueur NE PEUT PAS se terminer tant que
#    toutes les actions forcees possibles n'ont pas ete faites
#    (ability_type.py:56). Le joueur ne peut donc pas l'ignorer — il subit la
#    pioche forcee, ou les 2 menaces.
#  - « **then play that card (paying its costs)** » : le joueur PAIE. Ce n'est
#    pas une mise en jeu gratuite, d'ou `PlayCardsLikeInTurn` sans
#    `ignore_resources_cost` — l'inverse exact de dd003 Doombot, qui, lui,
#    avait deja paye.
#  - « **If you cannot** » : la carte piochee est injouable (ressources
#    insuffisantes, mauvaise forme, aucune carte a piocher). Cas TRES
#    atteignable — une amelioration a 3 avec une main vide suffit. On lit le
#    RETOUR de `PlayCardsLikeInTurn`, on ne devine pas (piege `wd028`).
#  - L'Action d'alter-ego a DEUX parties de cout : incliner CETTE carte ET
#    depenser un [mental]. Les deux, jamais l'une des deux (piege `wd005`,
#    ou la moitie d'un cout etait absente).
#  - « Attach to YOUR identity » : la carte se colle a l'identite du joueur
#    qui la revele, pas au vilain.


def GetAbilities() -> Sequence['Ability']:

    def hypnotic_suggestion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        faces = joueur.DrawUp(1, effect)
        if not joueur.PlayCardsLikeInTurn(faces, effect):
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity"
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.ForcedAction,
            hypnotic_suggestion,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
