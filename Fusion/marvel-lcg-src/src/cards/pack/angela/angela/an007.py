from . import *

# Asgard's Assassin — amelioration. ASGARD. TITLE. Cout 2. x2
# Hero Resource: Exhaust Asgard's Assassin -> generate a [physical] resource
#   (if you defeated a minion this round, generate [wild] instead).
#
# Carte de reference : ma005 * Star Light (pack ms_america), meme montage
# `CanGenerateResources(HeroResource, ...)` paye par
# `CostFunc.Exhaust("This")`.
#
# ⚠ UNE SEULE `CanGenerateResources` PAR CARTE (assert card_player.py:50).
# Le montage a DEUX capacites mutuellement exclusives, qui marche pour les
# portees de ciblage (13006 Wasp Sting, an003 plus bas), est donc INTERDIT
# ici : il ferait tomber la carte des la creation de la partie. Le conditionnel
# passe par `resources_fn`, evalue au moment du paiement — ce qui est d'ailleurs
# plus juste, la condition pouvant changer entre deux utilisations du tour.
#
# ⚠ « instead » : les deux branches sont EXCLUSIVES, la carte ne genere jamais
# deux ressources — `resources_fn` en rend UNE, l'une ou l'autre.

def GetAbilities() -> Sequence['Ability']:

    def ressource(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        Unused(message)
        if AuMoinsUnSbireVaincuCeRound(effect):
            return Resources("G")
        return Resources("R")

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            resources_fn=ressource,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
