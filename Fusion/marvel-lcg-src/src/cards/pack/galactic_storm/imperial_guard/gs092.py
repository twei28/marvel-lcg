from . import *

# Loyal Devotion — ENVIRONNEMENT (Imperial Guard). CONDITION. SETTING. Setup.
# Setup.
# Each IMPERIAL GUARD minion gains teamwork (IMPERIAL GUARD).
# Special: Place 1 threat on the main scheme.
# When Revealed: Discard each other SETTING environment in play.
#
# Cartes de reference :
#  - « Setup » : BASE AUTOMATIQUE `desc.Setup = "1"` (fiche setup.md, modele fne 60113a) : l'environnement entre en jeu a la mise en
#    place ; son « When Revealed » ne joue qu'en cas de revelation tardive.
#
#  - « Each IMPERIAL GUARD minion gains teamwork (IMPERIAL GUARD) » : `GiveKeywordToInPlayWhenApplyThis(.., teamwork="IMPERIAL GUARD")`, modele
#    blade bl012 (`teamwork=`, fiche teamwork.md : le trait existe dans l'enum, le moteur fait le reste).
#  - « Place 1 threat on the main scheme » : `PlaceThreatOnSchemes("MainScheme", 1)` (modele 40189).
#  - « When Revealed: Discard each other SETTING environment in play » : `Worlds.DiscardEachOther(effect, this, trait=SETTING,
#    card_type=Environment)` (modele du moteur, worlds.py).
#  - « Special » : capacite nommee `WhenResolveSpecialAbility("This", ..)` (fiche special.md, modele ab007 / baxter_stockman tx004b),
#    resolue par les sbires via `ResoudreLeSpecial`.
#
# ⚠ Mots-pieges : « teamwork (IMPERIAL GUARD) » : un sbire IMPERIAL GUARD qui ENTRE en jeu et s'engage s'active si un AUTRE sbire IMPERIAL GUARD est deja en jeu ; « the MAIN scheme » (pas une manigance annexe).


def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(trait=IG, card_type=Minion), teamwork=IG),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        EnvironnementImperialGuard(),
    ]
