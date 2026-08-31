from . import *

# Repulsor Blast — evenement. ATTACK. SUPERPOWER. Cout 2. x2
# Hero Action (attack): Stun an enemy. Deal 4 damage to that enemy.
#
# Carte de reference : 05015 Tackle (pack msm), squelette exact — « Hero
# Action (attack): Stun an enemy. [...] deal 3 damage to that enemy » via
# `WhenInYourPlayTurn(HeroAction, ...).SetPlay().SetLabel('attack')
# .SetTarget(Enemy, canbe_stunned=True)` + `Faces.GiveStatus` puis
# `DealDamage`. Ici les degats sont inconditionnels (Tackle les conditionne
# au paiement physique, pas cette carte-ci).
#
# ⚠ « to THAT enemy » : une seule cible pour les deux moities — le stun ET
# les 4 degats vont au meme ennemi (piege « that <nom> », etape 5).
# L'ordre imprime compte : le stun tombe AVANT les degats, donc une cible
# avec tough est d'abord sonnee, puis le tough absorbe les 4 degats.
#
# ⚠ Homonyme : 01031 Repulsor Blast (signature Iron Man) a un texte
# entierement different (X degats payes en energie). Aucun partage de code.

def GetAbilities() -> Sequence['Ability']:

    def repulsor_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        Faces.GiveStatus(effect.targets, "Stunned", effect)
        this.DealDamage(effect.targets, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            repulsor_blast
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, canbe_stunned=True),
    ]
