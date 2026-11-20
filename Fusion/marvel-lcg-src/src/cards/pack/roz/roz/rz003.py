from . import *

# * Thor (Odinson) — ALLIE signature, cout 4, [wild], 4 PV, THW 1★ / ATK 3★. ASGARD.
# Reduce the cost to play this card by 2 if you resolved a "Special" ability this turn.
# Each Thor ally gains "Response: After you resolve a "Special" ability on a card you control, deal 1 damage
#   to an enemy (limit once per turn)."
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - cout conditionnel : `bl002` Gear Up (`ReduceCostToPlayThis(1, conditions=[...])`).
#  - octroi : `alopex/ta009`, `leonardo/tl011` (`GiveKeywordToInPlayWhenApplyThis(..., given_abilities=[...])`).
#  - « After you resolve a Special ability » : `storm/36007` Storm's Cape
#    (`AfterPlayerResolveAbility(..., which_abilities=["Special"], control_by_you=True)`).
#  - « once per TURN » : rendu « une fois par round » (arbitrage technique de `hc002`, 11/09/2026).
#
# MOTS-PIEGES
#  - « BY 2 IF you resolved a Special THIS turn » : la reduction est de 2 d'un coup (pas par Special) et
#    conditionnelle ; contraste avec rz002 (1 PAR Special).
#  - « Special ability ON A CARD YOU CONTROL » : `control_by_you=True`.
#  - « deal 1 damage to AN enemy » : vilain ou sbire, au choix.
def GetAbilities() -> Sequence['Ability']:

    def special_resolu_ce_tour(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        return SpecialsResolusCeTour(effect.GetInitiator()) > 0

    return [
        AbilityFactory.ReduceCostToPlayThis(
            2,
            conditions=[special_resolu_ce_tour],
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            FinderThor(),
            # « EACH Thor ally gains » : l'octroi se rafraichit APRES l'entree en jeu d'un autre Thor. L'evenement par defaut
            # (`EnterPlayWhen`, « when ») part avant que la carte soit en jeu : seul le Thor deja la recevait, jamais l'autre
            # (CORRECTIF du 26/10/2026, constate au cas `rz_nb_reponses`).
            change_on_event=OnEvent.EnterPlayAfter(FinderThor()),
            given_abilities=[ReponseDonneeParOdinson()],
        ),
    ]
