from . import *

# Forge Ahead — TRAITRISE (Standard Skrull). 1 icone de boost.
# When Revealed: Each minion engaged with you schemes. If no scheme was made this way, the villain schemes.
#
# Cartes de reference :
#  - « Each minion engaged with you schemes » : `Worlds.Enemies.EngagedMinionSchemes(effect, joueur)` (enemies.py)
#    qui rend un `ActivatedResult` (`activated_cnt`) ; modele de repli `Worlds.Enemies.AllMinionAttackTheHeroItEngagedWith(
#    ..., if_no_attack=...)` (sk116).
#  - « the villain schemes » : **`sk098`** Impostor (`mechant.DoSchemes(joueur, effect)`).
#
# ⚠ Mots-pieges : « each minion ENGAGED WITH YOU » (pas les sbires engages avec un autre joueur) ; « SCHEMES » : meme
# si le joueur est en forme HEROS (le sbire complote, il n'attaque pas) ; « if NO scheme was made this way » : aucun sbire
# engage (ou aucune activation possible) -> le mechant complote, UNE fois.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        resultat = Worlds.Enemies.EngagedMinionSchemes(effect, joueur)
        if resultat.activated_cnt == 0:
            mechant = LeMechant(effect)
            if mechant is not None:
                mechant.DoSchemes(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
