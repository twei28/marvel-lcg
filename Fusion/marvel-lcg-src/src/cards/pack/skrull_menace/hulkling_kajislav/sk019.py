from . import *

# Provoked! — evenement d'aspect PROTECTION (n° 19). Cout 0 [physical].
# Hero Response: After you defend against an attack and take at least 1
#   damage, ready your hero.
#
# Cartes de reference :
#  - **`09020`** Unflappable : « After you defend against an attack and take no
#    damage » = `AfterUnitDefendAgainstAttack(Response, "You", op,
#    take_no_damage=True)`. Ici la condition INVERSE, `message.taken_damage >= 1`
#    (do_attack.py:315 lit le meme champ).
#  - `ho011` / `vv009` pour `Faces.ReadyAll`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After **you** defend » : TON identite est le defenseur (un allie qui
#    defend ne compte pas) : `"You"` avec `identity=True` dans la fabrique.
#  - « take **at least 1** damage » : tout prevenu (0) => rien.
#  - « **Hero** Response » : en forme heros seulement (on ne defend qu'en heros).
#  - « ready **your hero** » : l'identite.


def GetAbilities() -> Sequence['Ability']:

    def provoque(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            provoque,
            conditions=[lambda effect, message: message.taken_damage >= 1],
        ).SetPlay().SetLabel(),
    ]
