from . import *

# Getting Ruthless — TRAITRISE x2 (Paibok). 2 boosts.
# When Revealed (Alter-Ego): Resolve the "Boost" ability on each attachment in play that belongs to the
#   Paibok encounter set. If no "Boost" ability was resolved this way, this card gains surge.
#   (phrase « If no Boost... surge » ajoutee dans la version Kajislav du 03/11/2026 ; image Drive du
#   17/11/2026.)
# When Revealed (Hero): Paibok attacks you. Give him 1 additional boost card if you are stunned or
#   confused.
#
# Cartes de reference :
#  - Deux « When Revealed » selon la forme : **`01106`** Stampede (`WhenThisRevealed("Hero", ...)` /
#    `WhenThisRevealed("Alter-Ego", ...)`).
#  - Attaque + carte de boost de plus : **`sk100`** (meme coffret) : `villain.DoAttackYou(player, effect,
#    operation=lambda attaque: attaque.GiveAdditionalBoostCardForThisActivation(1, effect))`.
#  - Resolution des Boost : helper `ResoudreLesBoosts` (modele `24017`), qui rend le nombre de Boost
#    resolus.
#  - « this card gains surge » : idiome global `ThisCardGainSurge(effect)`, modele `nt015` (« If no
#    damage was taken this way, this card gains surge ») et `sk158` (meme pack).
#
# ⚠ Mots-pieges : « (Alter-Ego) » et « (Hero) » : la forme du joueur qui REVELE ; « IF you are stunned or
# confused » est lu AVANT l'attaque (Sonne n'agit que sur l'attaque du heros, pas sur sa defense) ; la
# carte de boost de plus n'est donnee que dans ce cas ; « Paibok attacks YOU » : le mechant, contre le
# joueur qui revele.
# « If NO Boost ability was resolved THIS WAY » : zero Boost resolu par la phrase qui precede (aucun
# attachement du set en jeu, ou aucun qui porte un Boost). Le surge ne vaut que pour la face ALTER-EGO ;
# la face HEROS ne le dit pas.


def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if ResoudreLesBoosts(effect, message.GetToPlayer()) == 0:
            ThisCardGainSurge(effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        paibok = PaibokEnJeu(effect)
        if paibok is None:
            return
        identite = joueur.GetIdentity()
        if identite.IsStunned() or identite.IsConfused():
            paibok.DoAttackYou(joueur, effect,
                               operation=lambda attaque: attaque.GiveAdditionalBoostCardForThisActivation(1, effect))
        else:
            paibok.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
    ]
