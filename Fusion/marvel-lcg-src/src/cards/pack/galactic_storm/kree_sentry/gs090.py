from . import *

# Intruder Elimination — TRAITRISE (Kree Sentry), 2 exemplaires. 2 icones de boost.
# When Revealed: Choose a non-KREE character. Kree Sentry attacks that character (even if that character is an
#   alter-ego). If an enemy was attacked this way, this card gains surge.
#
# Cartes de reference :
#  - « X attacks that character (even if alter-ego) » : un JOUEUR (son identite) -> `villain.DoAttackYou(joueur, effect)`,
#    modele OFFICIEL 16114 Single-Minded Fury (repris par gs135) ; un ALLIE ou un SBIRE -> `Enemy.AttackCharacter`, brique
#    commune (RECETTES-MOTEUR §16.1) : decisions du 20/10/2026 — les joueurs PEUVENT defendre l'attaque visant un sbire
#    (`players_may_defend=True`), et `ally_attack_is_against_player=False` pour un allie (livret p.4).
#  - « If ... this card gains surge » : `ThisCardGainSurge(effect)`, modele 40189.
#  - FAQ du livret p.22 : si la cible est l'identite du premier joueur, Kree Sentry attaque Rick Jones (l'Interruption
#    forcee de gs081 detourne l'attaque contre « vous »).
#
# ⚠ Mots-pieges : « CHOOSE a non-KREE character » (le joueur qui revele choisit, toute identite, tout allie ou sbire,
# Rick Jones compris ; pas la Poigne, qui n'est pas un personnage, ni un personnage KREE) ; « (even if alter-ego) » ;
# « If an ENEMY was attacked » = la cible est un sbire (un joueur ou un allie ne donne pas de surge) ; l'attaque est une
# attaque de base du mechant (carte de boost comprise).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sentry = KreeSentry(effect)
        if sentry is None:
            return
        choix = [f for f in PersonnagesDeLaTable(effect) if f.IsInPlay() and not f.HasTrait("KREE")]
        if not choix:
            return
        cible = choix[0] if len(choix) == 1 else joueur.AskChooseFace(choix, effect)
        if cible is None:
            return
        if Enemy.IsType(cible):
            if sentry.AttackCharacter(cible, effect, for_player=joueur, players_may_defend=True) is not None:
                ThisCardGainSurge(effect)
        elif Ally.IsType(cible):
            sentry.AttackCharacter(cible, effect, ally_attack_is_against_player=False)
        else:
            proprietaire = cible.GetControlByPlayer()
            if proprietaire is not None:
                sentry.DoAttackYou(proprietaire, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
