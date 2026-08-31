from . import *

# * Goblin Helmet — amelioration signature. ARMOR. TECH. Cout 2.
# Hero Action: Exhaust Goblin Helmet -> ready a TECH upgrade you control.
# Hero Resource: Exhaust Goblin Helmet and 1 TECH upgrade you control ->
#   generate the printed resource on that upgrade.
#
# Cartes de reference :
#  - le redressement : 31009 SP//dr Command (« ready an [[Interface]]
#    upgrade »), meme `SetTarget(Upgrade, trait=..., canbe_ready=True)` +
#    `Faces.ReadyAll` sous `CostFunc.Exhaust("This")` ;
#  - la ressource : an007 Asgard's Assassin pour le squelette
#    `CanGenerateResources(HeroResource, resources_fn=...)` paye par
#    `SetCostFunc`, et 21006 Energy Duplication pour la lecture de couleur
#    IMPRIMEE d'une autre carte (`FacesCounter.GetPrintedResources`).
#
# ⚠ POURQUOI PAS le couple Can+Do de 31001a SP//dr Suit : dans
# `DoGenerateResources.generate_resource` (resources.py:398), `res` est fige
# AVANT le `PayCost` des CostFunc — un `res_fn` qui lit
# `return_exhausted_cards` verrait donc l'etat d'AVANT le paiement. Constate
# en cas de comportement le 31/08/2026 : le casque s'epuisait, la TECH non.
# On suit donc le modele an007 : UNE `CanGenerateResources`, dont les couts
# sont payes par `generate_resource` via `cost_check_effect`.
#
# ⚠ ECART ASSUME : la carte epuisee est TOUJOURS la premiere amelioration
# TECH prete (ordre de `GetControlUpgrade`), car la couleur generee est figee
# a l'annonce, avant tout choix du joueur — offrir le choix desynchroniserait
# couleur annoncee et carte payee. Avec une seule TECH prete (le cas courant,
# et le deck de depart n'en superpose guere), aucun ecart observable.
# « the printed resource ON THAT upgrade » : couleur lue sur la TECH epuisee,
# pas sur le casque.

def GetAbilities() -> Sequence['Ability']:

    def candidates(effect: 'Effect') -> Sequence['CardFace']:
        this = effect.this
        initiator = effect.GetInitiator()
        if initiator is None:
            return []
        return [f for f in initiator.GetControlUpgrade(
                    CardFinder(canbe_exhaust=True, trait="TECH"))
                if f is not this]

    def ready_tech(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    def annonce(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        if this.IsExhaust():
            return None
        cands = candidates(effect)
        if not cands:
            return None
        return FacesCounter.GetPrintedResources(cands[:1])

    def epuiser_la_tech(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        cands = candidates(effect)
        if not cands:
            return False
        return Faces.ExhaustAll(cands[:1], effect) == list(cands[:1])

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ready_tech
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Upgrade, trait="TECH", from_where=["YouControlCards"],
                   canbe_ready=True),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            resources_fn=annonce,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, epuiser_la_tech)),
    ]
