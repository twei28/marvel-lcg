from . import *
# * Corsair's Rapier. Amelioration WEAPON, cout 1, Restricted.
#
# Corsair gets +1 ATK.
# Hero Response: After you discard a SKILL card from your hand, exhaust Corsair's Rapier → tuck that card under Corsair.
#
# Cartes de reference : 03009 (bonus d'attaque a l'attache : `GiveKeywordToAttached`), 47004 Jubilee's Coat (Hero Response
# + `Exhaust("This")`), 60037a Echo (ranger la carte depuis la defausse).
# FAQ de l'auteur : « Rapier doesn't care how the card was discarded. If a skill is discarded from your hand for any
# reason, you can tuck it » : `AfterCardDiscard` sans filtre sur la cause, depuis la main OU la zone de ressources (une
# carte DEPENSEE en ressource part de la main).
def GetAbilities() -> Sequence['Ability']:
    def de_ma_main(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        joueur = JoueurDe(effect)
        if joueur is None:
            return False
        # CORRECTIF (26/10/2026) : la carte doit encore attendre dans la defausse (Pocket Universe Gems cr001a a pu la glisser avant)
        if message.trigger.card.area is not joueur.discard_pile:
            return False
        zone = message.from_area
        if zone is joueur.hand_cards:
            return True
        return bool(zone.flags.is_resources_area) and message.trigger.GetControlByOrOwner() is joueur
    def rapier(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        identite = IdentiteDe(effect)
        # les Reponses de Gems et de Rapier sont declenchees ENSEMBLE : la 2e se resout apres que la 1re a glisse la carte
        if identite is not None and ToujoursEnDefausse(effect, message):
            identite.TuckCardUnderHere(message.trigger, effect)
    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Corsair"),
            attack=1,
        ),
        AbilityFactory.AfterCardDiscard(
            AbilityType.HeroResponse,
            CardFinder(trait="SKILL"),
            rapier,
            conditions=[de_ma_main],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
