from . import *

# Optimism — ressource signature, x2 (9/15 et 10/15). Ressource [wild].
# Response: After you spend this card, heal 1 damage from your identity and
#   draw 1 card.
#
# Cartes de reference :
#  - `ant/12006` Pym Particles et `mts/21058` Innovation :
#    `AbilityFactory.AfterYouSpendThisCard(type, op)` (resources.py:508) ;
#  - soin : `this.HealthUnits(cibles, 1, effect)` (ls007) ;
#  - pioche : `joueur.DrawUp(1, effect)`.
#
# ⚠ Mots-pieges :
#  - « Response », PAS « Hero Response » : jouable aussi en forme d'alter-ego
#    (AbilityType.Response, non HeroResponse comme 12006).
#  - « heal 1 damage from your IDENTITY » : l'identite du joueur, quelle que
#    soit sa forme. Pas de `SetTarget(canbe_heal=True)` : la cible serait
#    obligatoire et la PIOCHE serait perdue a pleine sante. Les deux effets
#    sont independants.
#  - « After you spend THIS card » : la fabrique filtre `effect.this in
#    message.faces`.
#  - La ressource generee [wild] vient de `desc.RES = G`, base automatique.

def GetAbilities() -> Sequence['Ability']:

    def optimism(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            this.HealthUnits([identite], 1, effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            optimism,
        ),
    ]
