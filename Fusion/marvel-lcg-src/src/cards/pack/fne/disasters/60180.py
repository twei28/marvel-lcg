from . import *

# Collapsing Bridge (side scheme, 1, hazard) — [star] Hinder 2[per_hero] : base.
# Forced Response: After any amount of threat is removed from Collapsing
#   Bridge, place 1 threat here.
# AfterSchemeRemoveThreat("This") ; « any amount » : la valeur retiree > 0.
# ⚠ Le moteur envoie AfterSchemeRemoveThreat AVANT de constater la defaite
# (scheme.py:145-150) : sans garde, un pont ramene a 0 recevait 1 menace et
# n'etait JAMAIS vaincu (harnais du 18/09/2026). Un complot annexe est vaincu
# des que sa derniere menace part (RRG « Defeated ») : la reponse ne resout
# que s'il reste de la menace, donc si le pont est encore en jeu.

def GetAbilities() -> Sequence['Ability']:

    def rechute(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def au_moins_une(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        return getattr(message, "value", 1) > 0

    def encore_de_la_menace(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        return effect.this.CastTo(EncounterSideScheme).threat > 0

    return [
        AbilityFactory.AfterSchemeRemoveThreat(AbilityType.ForcedResponse, "This", rechute, conditions=[au_moins_une, encore_de_la_menace]),
    ]
