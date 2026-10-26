from . import *
# I Am the Night — EVENEMENT cout X [energy]. SKILL. THWART. « Resolve this action X times (to a maximum of 3). » Hero Action (thwart) : remove
# up to 2 threat from a scheme. If this removes the last threat on that scheme, deal 1 damage to a minion.
# Reference : sm004 Rapid Strikes (`effect.GetCostX()`, une cible par repetition) ; `RemoveThreatFromSchemes(..., if_this_remove_last_threat=)`.
# ⚠ Un cout X exige la cle `surpayer` dans les cas de test (le pilote paie le minimum, zero).
def GetAbilities() -> Sequence['Ability']:
    def night(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for _ in range(min(int(effect.GetCostX() or 0), 3)):
            complots = [f for f in Worlds.GetOnFieldCards(effect) if Scheme2.IsType(f) and f.threat > 0]
            cible = joueur.AskChooseFace(complots, effect) if complots else None
            if cible is None:
                return
            def sbire_blesse() -> None:
                sbires = Worlds.GetOnFieldMinions(effect)
                if sbires:
                    this.DealDamage([joueur.AskChooseFace(sbires, effect)], 1, effect)
            this.RemoveThreatFromSchemes([cible], 2, effect, if_this_remove_last_threat=sbire_blesse)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, night).SetPlay().SetLabel('thwart'),
    ]
