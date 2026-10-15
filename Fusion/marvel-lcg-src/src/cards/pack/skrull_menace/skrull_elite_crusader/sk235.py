from . import *

# Rivals to the End — TRAITRISE x2 (Skrull Elite - Crusader). 2 icones de boost.
# When Revealed: Choose a minion. That minion attacks your hero twice in a row. If no attack was made
#   this way, give the villain 1 facedown boost card for each character you control.
#
# Cartes de reference :
#  - « <sbire> attacks your hero » : `Minion.DoAttackYou(joueur, effect)` (enemy.py), la meme
#    primitive que `Worlds.Enemies.AllMinionAttackTheHeroItEngagedWith` (sk116) ; un joueur en ALTER-EGO
#    n'a pas de heros a attaquer (le helper de sk116 le saute de meme).
#  - « Choose a minion » : `joueur.AskChooseFace(sbires, effect)` (modele sk122/hera ze002).
#  - « if no attack was made this way » : `DoAttackYou` rend None quand l'attaque n'a pas lieu
#    (sbire empeche d'activer, etc.) ; `ActivatedResult` de sk116 compte pareil.
#
# ⚠ Mots-pieges : « Choose a MINION » (n'importe lequel en jeu, engage avec ce joueur ou non) ;
# « attacks YOUR HERO » (le joueur qui revele, en forme heros) ; « TWICE IN A ROW » : deux attaques
# successives, chacune une activation complete (carte de boost comprise) ; si la premiere termine la
# partie / le joueur, la seconde ne part pas ; « if NO attack was made » : zero attaque (aucun sbire,
# alter-ego, activation empechee) ; « FOR EACH CHARACTER you control » : identite + allies.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        attaques = 0
        sbires = Worlds.GetOnFieldMinions(effect)
        if sbires and joueur.IsHero():
            sbire = joueur.AskChooseFace(sbires, effect)
            if sbire is not None:
                for _ in range(2):
                    if Worlds.IsGameOver(effect) or not sbire.IsInPlay():
                        break
                    if sbire.CastTo(Minion).DoAttackYou(joueur, effect) is not None:
                        attaques += 1
        if attaques == 0:
            DonnerBoostAuMechant(effect, len(joueur.GetControlCharacters()))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
