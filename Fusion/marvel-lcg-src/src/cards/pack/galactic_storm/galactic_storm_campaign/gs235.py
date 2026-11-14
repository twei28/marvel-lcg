from . import *

# * Spider-Woman (JULIA CARPENTER) — ALLIE de campagne (Identity-Specific / Campaign, n° 235). Cout 3.
# THW 2 / ATK 1, 3 PV. Aucun trait imprime.
# Honorary.
# Response: After Spider-Woman is discarded from the top of your deck, stun up to 2 enemies.
#
# Carte de reference :
#  - **`next_evol/domino/40043`** Jackpot! : `AbilityFactory.AfterCardDiscardInternal(Response, "This",
#    op, from_where="PlayerDeckTop")` — PRECEDENT DIRECT pour « After THIS CARD is discarded from the top
#    of your deck » (trouve apres une recherche plus large que la premiere passe du 21/10/2026, qui avait
#    cherche le TEXTE imprime au lieu de l'API `from_where="PlayerDeckTop"` ; la mecanique existe bien
#    dans le moteur, ce n'etait pas une brique manquante).
#
# ⚠ Mots-pieges :
#  - « from the top of YOUR deck » : `from_where="PlayerDeckTop"`, pas n'importe quelle defausse ;
#  - « UP TO 2 enemies » : 0, 1 ou 2 cibles au choix du joueur (`range=(0, 2)`), jamais forcé a 2 ;
#  - l'allie elle-meme est DEJA hors du jeu (en defausse) au moment ou cette Reponse part : `effect.this`
#    reste utilisable pour la capacite (modele Jackpot!, meme situation : `Faces.ShuffleAllTo([this],...)`
#    agit bien sur elle-meme une fois en defausse).


def GetAbilities() -> Sequence['Ability']:

    def spider_woman(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        Unused(message)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.Response,
            "This",
            spider_woman,
            from_where="PlayerDeckTop",
        ).SetTarget(Enemy, canbe_stunned=True, range=(0, 2)),
    ]
