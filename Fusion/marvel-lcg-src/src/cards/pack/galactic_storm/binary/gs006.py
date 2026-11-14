from . import *

# Energy Torrent — RESSOURCE, [energy][energy]. Binary 9/15.
# Response: After you spend this card, shuffle it into your deck.
#
# Cartes de reference :
#  - **`gmw/16033`** Salvage : « Response: After you spend this card, ... » sur
#    une RESSOURCE = `AfterYouSpendThisCard(AbilityType.Response, op)`.
#  - remelanger une carte dans le deck : `Faces.ShuffleAllTo([face], deck,
#    effect)` (`bt006`, RECETTES §2).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Response » (pas Forced) : facultative, le joueur peut la refuser.
#  - « After you SPEND this card » : depensee pour payer, pas defaussee par
#    Burnout ou Energy Transfer (contre-cas).
#  - « shuffle IT into your deck » : la carte elle-meme, depuis la defausse ou
#    le paiement l'a posee ; le deck est remelange.
#  - Les deux icones [energy] sont dans `desc.RES` ("YY"), aucun script.


def GetAbilities() -> Sequence['Ability']:

    def recharger(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Faces.ShuffleAllTo([this], joueur.player_deck, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            recharger,
        ),
    ]
