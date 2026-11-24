from . import *

# Chaos in Hell's Kitchen — TRAITRISE. Boost ★.
# When Revealed : Change the villain's position if it has not changed this phase. If the villain's position is Atop the Tenshu, place 2 threat on the main scheme;
#   otherwise, take 2 damage.
# [star] Boost : Resolve this card's "When Revealed" ability.
#
# Cartes de reference : hood/.../24059 Citywide Crisis (`Faces.ResolveAbility([this], player, AbilityType.WhenRevealed, effect)` en boost), mut_gen/sabretooth/32069.
# ⚠ « take 2 damage » = l'IDENTITE du joueur subit 2 degats (degats directs, pas indirects) ; la position peut changer PENDANT le boost aussi (meme limite par phase).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        ChangerSiPasChange(effect)
        if AuTenshu(effect):
            this.PlaceThreatOnSchemes("MainScheme", 2, effect)
        else:
            this.DealDamage([joueur.GetIdentity()], 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.ResolveAbility([effect.this], message.GetToPlayer(), AbilityType.WhenRevealed, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
