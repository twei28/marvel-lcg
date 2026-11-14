from . import *

# Detonation (222B) — ENVIRONNEMENT (Nega-Bomb), verso de la Nega-Bomb.
# When Revealed: Deal X damage to each friendly character and minion in play ignoring any tough status card,
#   where X is equal to the amount of threat here divided by the total number of friendly characters and
#   minions in play (rounded up). Remove this card from the game.
#
# Cartes de reference :
#  - **`luke_cage/62028`** / `sentinel/__init__` : `DamageProperty(damage=N, ignore_tough=True)` = « ignoring
#    any tough status card ».
#  - « each friendly character » : identites et allies des joueurs (`joueur.GetControlCharacters()`,
#    `next_evol/40110`) ; « and minion » : tous les sbires en jeu.
#  - `Faces.RemoveAllFromGame([this], effect)` (GUIDE §3.1) pour « remove this card from the game ».
#
# ⚠ Mots-pieges : « EACH friendly character AND MINION » (heros/alter ego, allies ET sbires ; pas le mechant) ;
# « X = threat HERE / total number (ROUNDED UP) » : la menace est celle de la Nega-Bomb au retournement (notee
# par gs222a) ; le nombre est compte AVANT les degats ; « IGNORING any tough status card » (la carte Tenace
# reste, elle n'absorbe rien) ; « Remove this card from the game » (pas defaussee).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this
        menace = int(getattr(this.card, ATTR_MENACE, 0) or 0)
        cibles = PersonnagesAmisEtSbires(effect)
        x = DegatsDeDetonation(menace, len(cibles))
        if x > 0 and cibles:
            this.DealDamage(cibles, DamageProperty(damage=x, ignore_tough=True), effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
