from . import *

# Trophy Taken — TRAITRISE. Boost 2.
# When Revealed: The active villain attacks the friendly character with the fewest remaining hit points. If this attack defeats an ally,
#   remove that ally from the game.
# Insert : Trophy Taken a priorite sur Skulls for the Taking (l'allie retire du jeu n'est pas glisse dessous).
#
# Cartes de reference : `AttackCharacter(cible, if_this_defeat_unit=)` (brique 16.1) ; « fewest remaining hit points » : 07016 (egalite :
#   le joueur choisit) ; identite visee : `DoAttackYou(son joueur)`.
#
# ⚠ Mots-pieges :
#  - « FRIENDLY character » : identites et allies de TOUS les joueurs (les joueurs sont alliés) ;
#  - « remove from the GAME » (pas la defausse) : Skulls ne trouve plus l'allie et ne glisse rien.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        actif = MechantActif(effect)
        if actif is None:
            return
        persos = []
        for j in Worlds.GetPlayers(effect):
            persos.append(j.GetIdentity())
            persos += [a for a in j.GetControlCards() if Ally.IsType(a)]
        persos = [p for p in persos if p is not None]
        if not persos:
            return
        moins = min(p.health for p in persos)
        ex_aequo = [p for p in persos if p.health == moins]
        cible = ex_aequo[0] if len(ex_aequo) == 1 else (joueur.AskChooseFace(ex_aequo, effect, prompt="Attacked character") or ex_aequo[0])

        def trophee(abattu: 'CardFace') -> None:
            if Ally.IsType(abattu):
                Faces.RemoveAllFromGame([abattu.card.face], effect)

        if Ally.IsType(cible):
            actif.AttackCharacter(cible, effect, if_this_defeat_unit=trophee)
        else:
            actif.DoAttackYou(cible.GetControlByOrOwner(), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
