from . import *

# * Wave's Swords — amelioration signature, x1 (14/15). Restricted. TECH.
# WEAPON. Cout 1.
# Hero Action: Exhaust Wave's Swords and flip a faceup card in your Rising
# Tide area facedown -> ready Wave.
#
# DEUX couts empiles sur UNE capacite : `.SetCostFunc(A).SetCostFunc(B)`
# EMPILE (`Ability.SetCostFunc`, `cost_funcs.append`), ne remplace pas --
# modele `luke_cage/62018.py`, `.SetCostFunc(CostFunc.Exhaust("This"))
# .SetCostFunc(CostFunc.Counter("This", 1, 'block'))` sur la meme capacite.
# « Restricted » est lu directement dans `desc` (base automatique,
# PROCESSUS-CARTE etape 5, voir an009 Xiphos). Pas de `.SetPlay()` : ce n'est
# pas la mise en jeu de la carte mais une action APRES qu'elle soit deja en
# jeu (memes precedents Ebony/Xiphos).

def GetAbilities() -> Sequence['Ability']:

    def waves_swords(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return
        hero = initiator.GetHero()
        if hero is not None:
            hero.card.Ready(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            waves_swords,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CoutRetournerUneCarteRisingTide(
            face_visible=True,
            prompt="Flip to ready Wave",
        )),
    ]
