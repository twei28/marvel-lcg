from . import *

# Clan of Shadows (1B) — COMPLOT PRINCIPAL, face B. Menace de depart 1[per_hero],
# cible 6[per_hero], escalade +1[per_hero].
# When Revealed: Cloak Shredder.
# Forced Response: After a FOOT CLAN minion is defeated, place 1 threat on this scheme.
#
# Cartes de reference : `sk179` (Shapeless Wastes : `AfterUnitBeDefeated(
# ForcedResponse, CardFinder(card_type=...), op)`), `01095` pour un When Revealed
# de complot ; `Cloak` du pack (fiche cloak.md).
#
# Mots-pieges : « AFTER a FOOT CLAN minion IS DEFEATED » (Reponse forcee, apres) ;
# tout sbire FOOT CLAN, du deck OU modulaire, nemesis compris ; « on THIS scheme »
# (ce complot, pas « the main scheme » d'ailleurs) ; « Cloak Shredder » = le
# vilain Shredder, retrouve par card_id.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, TrouverShredder(effect))

    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        this.PlaceThreatOnSchemes([this], 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Minion, trait="FOOT CLAN"),
            sbire_vaincu,
        ),
    ]
