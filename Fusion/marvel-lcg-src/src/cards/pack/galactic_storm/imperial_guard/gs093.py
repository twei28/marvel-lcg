from . import *

# Noble Bearing — ENVIRONNEMENT (Imperial Guard). CONDITION. SETTING. Setup.
# Setup.
# Each IMPERIAL GUARD minion gains guard and the ELITE trait.
# Special: Discard the top 3 cards of the encounter deck.
# When Revealed: Discard each other SETTING environment in play.
#
# Cartes de reference :
#  - « Setup » : BASE AUTOMATIQUE `desc.Setup = "1"` (fiche setup.md, modele fne 60113a) : l'environnement entre en jeu a la mise en
#    place ; son « When Revealed » ne joue qu'en cas de revelation tardive.
#
#  - « gains guard and the ELITE trait » : `GiveKeywordToInPlayWhenApplyThis(.., guard=1, trait="ELITE")`, modeles sk091 Skrull Empire (`guard=1`)
#    et blade bl012 (`trait=`) ; ELITE existe dans l'enum des traits.
#  - « Discard the top 3 cards of the encounter deck » : `Worlds.DiscardEncounterCards(3, effect)`.
#  - « When Revealed: Discard each other SETTING environment in play » : `Worlds.DiscardEachOther(effect, this, trait=SETTING,
#    card_type=Environment)` (modele du moteur, worlds.py).
#  - « Special » : capacite nommee `WhenResolveSpecialAbility("This", ..)` (fiche special.md, modele ab007 / baxter_stockman tx004b),
#    resolue par les sbires via `ResoudreLeSpecial`.
#
# ⚠ Mots-pieges : « guard AND the ELITE trait » : les deux, sur chaque sbire IMPERIAL GUARD ; « the TOP 3 cards of the ENCOUNTER deck » (deck vide : le moteur melange la defausse).


def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        Worlds.DiscardEncounterCards(3, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(trait=IG, card_type=Minion), guard=1, trait="ELITE"),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        EnvironnementImperialGuard(),
    ]
