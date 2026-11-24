from . import *

# * Lei Kung — SOUTIEN, cout 1, [energy]. K'UN-LUN. MARTIAL ARTIST. PERSONA. x1 (Iron Fist 9/15).
# Action: Exhaust Lei Kung and remove 1 chi counter from your identity -> draw 1 card.
#
# CARTES DE REFERENCE
#  - double cout « exhaust X and remove 1 <compteur> counter » : `tmnt_shinobi_taijutsu/sh010`
#    Martial Skill et `ua033` Pete (`SetCostFunc(Exhaust("This")).SetCostFunc(Counter(...))`) ;
#    le compteur pris sur l'IDENTITE : `venus/tv001b` (`CostFunc.Counter("YourIdentity", 1, ...)`).
#  - piocher : `joueur.DrawUp(1, effect)` (sh010).
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust Lei Kung AND remove 1 chi counter » : cout a DEUX parties, les deux payees ou rien.
#  ⚠ « from your IDENTITY » : utilisable dans les deux formes (« Action » nue).
#  ⚠ Unique (✦ imprime) : « * » devant le nom.


def GetAbilities() -> Sequence['Ability']:

    def lei_kung(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            lei_kung,
            conditions=[AuMoinsChi(1)],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, CHI)),
    ]
