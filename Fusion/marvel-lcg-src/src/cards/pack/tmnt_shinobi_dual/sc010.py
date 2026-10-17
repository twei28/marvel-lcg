from . import *

# Kusuri — AMELIORATION DUALE Kuji-Kiri/Taijutsu, cout 2, [physical]. ITEM. MYSTIC.
# Classe : « Kuji-Kiri;Taijutsu ».
# Max 1 per player.
# Action: Exhaust this card and discard an ATTACK event from your hand -> heal 2 damage from a friendly character.
#
# Mots-cles (fiches lues AVANT le code) : Max N per player (base native `desc.MaxPerUnit`) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - « heal N damage from a friendly character » (Action, cible `Friend`) : `rainy/thor_jane_foster/ra001b` Physician
#    (`SetTarget(Friend, canbe_heal=True)`, `this.HealthUnits(effect.targets, n, effect)`) ;
#  - cout « Exhaust this card AND discard a <trait> <type> from your hand » : `CostFunc.Exhaust("This")` +
#    `CostFunc.Discard("YourHandCards", card_type=..., trait=...)` (`CostFunc.Discard`, `cost_func.py`) ;
#  - « Max 1 per player » : `01018` Energy Channel.
#
# TEXTE CONTRE CODE
#  ⚠ « discard an ATTACK EVENT from your hand » : un EVENEMENT portant le trait ATTACK, dans la MAIN (pas une amelioration
#    ATTACK, pas un evenement non ATTACK) ; sans tel evenement en main l'action n'est pas proposee. COUT (devant la fleche) :
#    la carte est defaussee meme si personne n'est blesse.
#  ⚠ « heal 2 damage FROM A FRIENDLY CHARACTER » : identite ou allie de n'importe quel joueur ; jamais un ennemi.
#  ⚠ « Action » (et non « Hero Action ») : les deux formes. « Max 1 per player » : un seul exemplaire en jeu par joueur.


def GetAbilities() -> Sequence['Ability']:

    def kusuri(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.HealthUnits(effect.targets, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kusuri,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", card_type=Event, trait="ATTACK"))
        .SetTarget(Friend, canbe_heal=True),
    ]
