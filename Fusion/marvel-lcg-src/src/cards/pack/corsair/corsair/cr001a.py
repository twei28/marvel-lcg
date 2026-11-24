from . import *
# * Corsair, face heros. Prefixe `cr`.
#
# You may play cards tucked under here as if they were in your hand.
# Pocket Universe Gems — Response: After a card in your hand is discarded to pay for a cost, tuck that card under
#   Corsair. (Limit once per round.)
#
# Cartes de reference :
#  - jouer comme en main : `AttachedCardCanPlayLikeInHand` (td012 Donatello's Shell, tc013 Casey's Bag), SANS
#    `also_spend` ni `also_discard` : le FAQ de l'auteur dit « cards tucked under Corsair can only be played, not
#    spent to generate resources » ;
#  - depense de ressources : 65001a Wave (`AfterCardsBeSpendAsResource`, la carte est dans la zone de ressources,
#    AVANT `DiscardResourcesArea`) ;
#  - ranger depuis la defausse : 60037a Echo (`TuckCardUnderHere`).
#
# ⚠ DEUX CHEMINS pour « discarded to pay for a cost » (FAQ : « a cost is anything before the arrow, or when the card
# says "spend" ») : (1) la depense de ressources de la main (Wave), (2) un cout `CostFunc.Discard` d'une carte
# (« discard a card from your hand → ... »). Les deux partagent UNE limite par round (marqueur sur l'identite).
#
# CORRECTIF (26/10/2026, RR « Cost » : « a player spends resources that they generate by discarding cards from their
# hand ») : au chemin (1) la carte depensee est DEFAUSSEE (zone de ressources -> defausse), PUIS la Reponse la glisse
# depuis la defausse. Les autres Reponses « after you discard » (Corsair's Rapier cr003) la voient donc. Avant ce
# correctif la Reponse partait sur `AfterCardsBeSpendAsResource` et glissait la carte AVANT sa defausse (ecart assume,
# aujourd'hui supprime). Chaque carte depensee ouvre sa propre fenetre `AfterCardDiscard` : la limite d'une fois par round
# reste portee par le marqueur de l'identite, et un joueur qui refuse la 1re carte peut encore glisser la 2e.
def GetAbilities() -> Sequence['Ability']:
    def gemmes_ressources(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Hero)
        if not ToujoursEnDefausse(effect, message):
            return
        GemmesUtilisees(effect)
        this.TuckCardUnderHere(message.trigger, effect)
    def depense_de_ma_main(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        joueur = JoueurDe(effect)
        if joueur is None or not message.from_area.flags.is_resources_area or not GemmesDisponibles(effect):
            return False
        # la carte est partie de LA MAIN de ce joueur et attend toujours dans sa defausse (une autre Reponse a pu la glisser)
        return message.trigger.GetControlByOrOwner() is joueur and message.trigger.card.area is joueur.discard_pile
    def gemmes_cout(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Hero)
        if not ToujoursEnDefausse(effect, message):
            return
        GemmesUtilisees(effect)
        this.TuckCardUnderHere(message.trigger, effect)
    def cout_de_defausse_de_ma_main(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        joueur = JoueurDe(effect)
        if joueur is None or message.from_area is not joueur.hand_cards or not GemmesDisponibles(effect):
            return False
        if message.trigger.card.area is not joueur.discard_pile:   # deja glissee par une autre Reponse (Rapier)
            return False
        # « to pay for a COST » : la defausse vient d'un `CostFunc.Discard` de l'effet qui la provoque.
        par = message.by_effect
        cout = getattr(par, "cost_func", None)   # DebugRule / GameRule n'en ont pas
        return cout is not None and cout.Get(CostFunc.Discard) is not None
    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(),
            gemmes_ressources,
            conditions=[depense_de_ma_main],
        ).SetName("Pocket Universe Gems"),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(),
            gemmes_cout,
            conditions=[cout_de_defausse_de_ma_main],
        ).SetName("Pocket Universe Gems"),
    ]
