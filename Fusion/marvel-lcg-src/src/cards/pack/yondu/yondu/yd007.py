from . import *

# Jackpot! — RESSOURCE signature, x1 (n/15 = 10). Ressource [wild].
# Response: After you spend this card, treat the next card you spend as if it
#   has double the resources.
#
# Cartes de reference :
#  - **`AfterYouSpendThisCard(type, op)`** (resources.py:508) pour « After you
#    spend this card ».
#  - **`AfterGenerateResources(AbilityType.Rule, "You", op)`** (resources.py:
#    ~745, modele `cd003`) : la fenetre `WhenCardBeSpendAsResource`, envoyee
#    par `DoGenerateResources` JUSTE APRES que la carte depensee a verse ses
#    ressources dans `res_pool`. On y verse une seconde fois `message.res` :
#    « comme si elle avait le double ».
#  - `im013` / `as015` pour `RegisterTemp(..., unregister_after_exec=True)`.
#
# ⚠ CORRIGE LE 11/09/2026 : LA PREMIERE VERSION ETAIT INERTE. Elle passait par
# `WhenCountingResourcesOnCards` (modele Haywire `29038`), or cette fenetre
# est envoyee a CHAQUE LECTURE de `printed_resource` (has_resources.py:17) :
# le rendu des options la lit pour afficher ce que chaque carte de la main
# peut payer. Avec `unregister_after_exec=True`, le doublement etait consomme
# par la premiere lecture venue, jamais par une depense. Le montage du
# harnais (First Aid payee avec Jackpot, puis Webb's Team Strikes! surpayee
# avec UNE Haymaker) mesurait X = 1 au lieu de 2. Et de toute facon, la
# valeur versee a la depense est `message.expected_res` (DoGenerateResources),
# figee au moment du rendu, pas relue.
#
# ⚠ POURQUOI PAS `DoubleResourcesThisGenerates` (resources.py:36), employe par
# `01055` The Power of Aggression et ses quatre jumelles. Cette fabrique double
# ce que **CETTE** carte genere. Jackpot! double ce que genere **LA SUIVANTE**,
# et ne genere elle-meme qu'un [wild] ordinaire. Les deux textes se
# ressemblent, la mecanique est inverse.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the **NEXT** card you spend » : UNE seule carte, la premiere comptee
#    apres celle-ci. D'ou `unregister_after_exec=True`, qui retire l'effet des
#    qu'il a servi. Sans lui, tout le paiement serait double.
#  - « as if it has **double the resources** » : on double ce que la carte
#    VAUT, pas le cout a payer. `SetReturnValue(res * 2)`.
#  - « After you **spend** this card » : depensee comme RESSOURCE, pas jouee.
#    Jackpot! est une carte de type Resource, elle n'a pas d'autre usage.
#  - « the next card you **spend** » : `AfterGenerateResources` ne part que
#    pour une carte reellement depensee (jamais pour un simple comptage), et
#    seulement par « You » (`which_player="You"`).


def GetAbilities() -> Sequence['Ability']:

    def jackpot(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        def doubler(sous_effect: 'Effect', sous_message: 'Message.WhenCardBeSpendAsResource') -> None:
            # La carte vient de verser `res` : on le verse une seconde fois.
            sous_message.GetToPlayer().res_pool.Gain(sous_message.res, sous_effect)

        this.effect.RegisterTemp(
            AbilityFactory.AfterGenerateResources(
                AbilityType.Rule,
                "You",
                doubler,
            ),
            unregister_after_exec=True,
            until_phase_end=True,
        )

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            jackpot,
        ),
    ]
