from . import *
# Stolen Goods (Basic, amelioration 0 [wild]). ITEM. Max 2 per deck.
# Resource: Discard this card → generate [wild][wild]. Trigger this ability only if you have the OUTLAW trait.
#
# Cartes de reference : ze011 Mount Olympus / hc001a Empowered (`CanGenerateResources(.., conditions=[..]).SetCostFunc(..)`) ;
# `CostFunc.Discard("This")` pour « Discard this card → ». « only if YOU have the OUTLAW trait » : l'identite du joueur ;
# la condition doit etre dans `conditions` (sinon la ressource est OFFERTE au paiement meme quand elle est interdite, RECETTES §4).
# Aucune cible d'attache imprimee : l'amelioration entre en jeu pres de l'identite (comme 01034-like) : `CanPlayThisUpgradeCard()`.
# « Max 2 per deck » = `desc.MaxPerDeck "2"`, lu par le moteur et par le deck-builder.
def GetAbilities() -> Sequence['Ability']:
    def outlaw(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        joueur = message.GetToPlayer()
        return joueur is not None and joueur.GetIdentity().HasTrait("OUTLAW")
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("GG"),
            conditions=[outlaw],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
