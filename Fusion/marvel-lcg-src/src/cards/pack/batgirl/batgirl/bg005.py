from . import *

# Batarangs — evenement, cout 2, [physical]. « Hero Action (attack): Deal 2 damage to an enemy. This attack gains ranged. For each
# resource you used to pay for this event, if that resource is: [energy] - Stun an enemy. [physical] - Deal 2 damage to an enemy.
# [mental] - Confuse an enemy. »
# Cartes de reference : `23006` Missile Launcher (`DealDamage(.., property=AttackProperty(ranged=True))`), `01083` (statut Stunned),
# `Faces.GiveStatus(.., "Confused")`. Chaque ligne se compte sur les ressources payees ; RR « Wild Resource » (arbitrage du 26/10/2026) :
# un wild depense compte pour UN type, celui que le joueur declare au paiement (`GetPaidResources(True)` le lui demande et le
# remplace par la couleur choisie, modele No Holding Back `gs301`). Sous Recalled Trauma (`SansType`) on ne demande rien : aucune ligne.


def GetAbilities() -> Sequence['Ability']:

    def batarangs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect, property=AttackProperty(ranged=True))
        if joueur is None:
            return
        res = effect.GetPaidResources(not SansType(effect))
        for emplacement, action in (("Y", "stun"), ("R", "degats"), ("B", "confuse")):
            n = Compter(effect, res, Icone(effect, emplacement), convert_green_res=False)
            for _ in range(n):
                cible = ChoisirUnEnnemi(joueur, effect)
                if cible is None:
                    break
                if action == "stun":
                    Faces.GiveStatus([cible], "Stunned", effect)
                elif action == "confuse":
                    Faces.GiveStatus([cible], "Confused", effect)
                else:
                    this.DealDamage([cible], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            batarangs,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
