from . import *

# * Thor (Jane Foster) — ALLIE signature, cout 3, [wild], 3 PV, THW 2★ / ATK 2★. ASGARD.
# Reduce the cost of this card by 1 for each "Special" ability resolved this turn.
# Each Thor ally gains "Response: After this card uses a basic power, resolve the "Special" on a [[WAKANDA]]
#   card you control."
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - cout : `wd157` Spider-Mobile (`ReduceCostToPlayThis(fn)` : `fn(effect)` rend le nombre a retrancher).
#  - « each X gains an ability » : `alopex/ta009` et `leonardo/tl011` (DECISION UTILISATEUR TMNT du 15/10/2026 :
#    VRAI octroi) : `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(finder, control_by="You",
#    given_abilities=[...])`.
#  - Response donnee : `51001a` (`AfterUnitUseBasicPower(Response, "This", op)` + `ResolveSpecialAbility`).
#
# MOTS-PIEGES
#  - « EACH Thor ally gains » : chaque allie nomme Thor que tu controles, y compris cette carte et Odinson
#    (rz003) ; la Reponse est portee par CHAQUE allie, pas par rz002.
#  - « each Special ABILITY resolved THIS TURN » : `PlayerStat.this_turn_resolved_specials` (CORRECTIF du
#    25/10/2026, `EffectInvoker._ResolveSelfInternal`) ; vide a chaque tour. Compte les capacites Special
#    REELLEMENT resolues (cout paye) POUR le joueur : deux Specials sur une meme carte (rz006) en font deux.
#  - « After THIS CARD uses a basic power » : l'allie Thor lui-meme (`"This"` sur la capacite donnee).
#  - « a WAKANDA card YOU CONTROL » : `from_where=["YouControlCards"]`, seules les cartes a Special.
def GetAbilities() -> Sequence['Ability']:

    def reduction(effect: 'Effect') -> int:
        return SpecialsResolusCeTour(effect.GetInitiator())

    return [
        AbilityFactory.ReduceCostToPlayThis(reduction),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            FinderThor(),
            # « EACH Thor ally gains » : l'octroi se rafraichit APRES l'entree en jeu d'un autre Thor. L'evenement par defaut
            # (`EnterPlayWhen`, « when ») part avant que la carte soit en jeu : seul le Thor deja la recevait, jamais l'autre
            # (CORRECTIF du 26/10/2026, constate au cas `rz_nb_reponses`).
            change_on_event=OnEvent.EnterPlayAfter(FinderThor()),
            given_abilities=[ReponseDonneeParJane()],
        ),
    ]
