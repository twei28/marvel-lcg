from . import *

# Throat Punch — EVENEMENT, cout 0, impression 1/15 : ressource(s) imprimee(s) physique + mental. ATTACK. (card_id ch003)
# Hero Action (attack): Deal 1 damage to the villain. Draw a card.
# Flow: [wild] → draw 2 additional cards.
#
# ⚠ IMPRESSIONS : Throat Punch existe en DEUX cartes (ch004) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `01087` Haymaker (`SetPlay().SetLabel('attack').SetTarget(...)`) ; cible VILAIN : `27015` / `sm/27017` (`SetTarget(Villain)`).
#  - pioche : `joueur.DrawUp(n, effect)` (`nt005`).
#
# ⚠ Mots-pieges :
#  - « the VILLAIN » : cible unique (le vilain), pas « an enemy ».
#  - Flow [wild] : une icone WILD (etoile) exigee, donc la carte du dessus doit IMPRIMER un wild (correspondance stricte).
#  - « 2 ADDITIONAL cards » : 1 + 2 = 3 cartes au total ; le Flow s'ajoute a la pioche, ne la remplace pas.
#  - le Flow est facultatif (« you MAY also resolve »).


def GetAbilities() -> Sequence['Ability']:

    def throat_punch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        if joueur is None:
            return
        joueur.DrawUp(1, effect)
        if AccepterFlow(effect, joueur, "G"):
            joueur.DrawUp(2, effect)
            FlowResolu(joueur, this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            throat_punch,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Villain),
    ]
