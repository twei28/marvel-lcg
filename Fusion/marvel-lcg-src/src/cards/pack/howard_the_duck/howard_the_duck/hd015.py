from . import *

# Duckpool Suit — ITEM — amelioration, cout 2
# You get +3 hit points.
# Howard the Duck gets +1 ATK.
# Hero Response: After you defeat a side scheme, exhaust Duckpool Suit → deal
#   1 damage to an enemy.
#
# Amelioration sans ligne « Attach to... » : portee directement par le joueur,
# modele exact ok014 (Royal Protector) et ss015/ss016 (Spider Stealth Suit,
# Stings of Kaine), tous en
# `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(...)`.
#   - « YOU get +3 hit points » vise l'identite quelle que soit sa face
#     (`"You"`, comme ss015 : les PV suivent le joueur en forme civile aussi).
#   - « HOWARD THE DUCK gets +1 ATK » vise la face HEROS nommement
#     (`CardFinder(name=...)`) : elle n'existe en jeu que sous cette forme,
#     donc aucune condition de forme supplementaire (modele ok014, meme
#     distinction « identite » / « face heros nommee » sur la meme carte).
#
# « After you DEFEAT A SIDE SCHEME » : `AfterUnitDefeatedScheme(HeroResponse,
# "You", SchemeSide2, ...)` — restreint aux manigances ANNEXES (contrairement
# a hd014, qui accepte n'importe quelle manigance). Cout d'inclinaison :
# `.SetCostFunc(CostFunc.Exhaust("This"))` (modele ok014). Cible du degat
# choisie a la resolution : `.SetTarget(Enemy)`.


def GetAbilities() -> Sequence['Ability']:

    def duckpool_suit(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        if effect.targets:
            this.DealDamage(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=3,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_HOWARD_HEROS),
            control_by="You",
            attack=1,
        ),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            SchemeSide2,
            duckpool_suit,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
