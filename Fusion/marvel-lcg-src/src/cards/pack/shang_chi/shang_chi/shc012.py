from . import *

# Chi Jabs — EVENEMENT, cout 1, impression 10/15 : ressource(s) imprimee(s) physique. ATTACK. (card_id shc012)
# Hero Action (attack): Choose up to 3 different enemies. Deal 1 damage to each of them.
# Flow (attack): [physical] → deal 2 damage to the villain.
#
# ⚠ IMPRESSIONS : Chi Jabs existe en DEUX cartes (shc011) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `shc` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `10005` Thunderclap : « Choose up to 3 different enemies. Deal N damage to each » = `SetTarget(Enemy, range=(1, 3))`.
#  - cible VILAIN : `27015` (`Villain`, `SetTarget`).
#
# ⚠ Mots-pieges :
#  - « up to 3 DIFFERENT enemies » : le ciblage standard interdit les doublons.
#  - Flow [physical] : un poing imprime exige sur la carte du dessus ; « the VILLAIN » : degats au vilain (pas a un ennemi au choix).
#  - 2 degats s'ajoutent au 1 deja inflige au vilain s'il etait une des cibles.


def GetAbilities() -> Sequence['Ability']:

    def chi_jabs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        if joueur is None or not AccepterFlow(effect, joueur, "R"):
            return
        vilains = Worlds.FindCardsOnField(effect, card_type=Villain)
        if vilains:
            this.DealDamage(list(vilains), 2, effect)
        FlowResolu(joueur, this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chi_jabs,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 3)),
    ]
