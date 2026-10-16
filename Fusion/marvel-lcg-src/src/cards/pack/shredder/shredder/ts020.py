from . import *

# Foot Rikugun (x2) — COMPLOT ANNEXE. Menace 2[per_hero], icone HAZARD (verifiee
# par decoupe contre 01107 Hazard, voir le gabarit), 2 icones de boost.
# Forced Response: After a FOOT CLAN minion enters play, cloak it. If you cannot,
#   give it a tough status card.
#
# Cartes de reference : `hs222` (`AfterCardEnterPlay(ForcedResponse, CardFinder(
# trait=..., card_type=Minion), op)`, `message.trigger` = le sbire) ; RECETTES
# §2 « give X a tough status card. If you cannot » (lire le RETOUR, ne pas
# conditionner la cible).
#
# Mots-pieges : « If YOU CANNOT » = Cloaked refuse (le sbire est DEJA Cloaked :
# un seul par personnage) ; « it » = le sbire qui entre ; une copie par exemplaire
# en jeu.


def GetAbilities() -> Sequence['Ability']:

    def entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        sbire = message.trigger
        if not Cloak(effect, sbire):
            Faces.GiveStatus([sbire], "Tough", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            CardFinder(trait="FOOT CLAN", card_type=Minion),
            entree,
        ),
    ]
