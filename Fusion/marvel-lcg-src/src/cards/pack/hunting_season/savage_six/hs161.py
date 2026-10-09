from . import *

# hs161 * Tarantula
# [star] +1 ATK tant que l'identite engagee avec lui est confuse. [star] Forced Response : apres qu'il attaque et blesse
# un personnage, ce personnage est confus. Boost : +1 icone de boost si vous etes confus.

def GetAbilities() -> Sequence['Ability']:

    def identite_confuse(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = effect.this.CastTo(Minion).engaged_player
        return 1 if joueur is not None and joueur.GetIdentity().IsConfused() else 0

    def confus(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        return message.GetToPlayer().GetIdentity().IsConfused()

    return [
        AbilityFactory.ThisGainKeyword(identite_confuse, attack=1, change_on_event=OnEvent.Status(Unit2, 'Confused')),
        MalusApresDegats("Confused"),
        BoostPourIconeSi(confus),
        IconeEnPlus(),
    ]
