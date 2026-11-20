from . import *

# Demon Soldier (mp123, deux exemplaires identiques) — SBIRE MYSTIC. PV 3, ATK 2, SCH 1, Boost 1, Guard 1, Teamwork (MYSTIC) (natifs).
# When Revealed : Take 1 indirect damage. [star] Boost : After this activation, put this minion into play engaged with you.
#
# Cartes de reference : mf017 (`identite.TakeIndirectDamage(this, 1, effect)`), ar012 (`message.AfterThisActivation`), `Minion.EngagePlayer`.
# ⚠ Mots-pieges : « INDIRECT » : degats indirects (le joueur repartit, pas d'attaque) ; Boost « AFTER this activation » : apres l'activation, pas pendant.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        joueur.GetIdentity().TakeIndirectDamage(effect.this, 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        message.AfterThisActivation(effect, lambda: this.EngagePlayer(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
