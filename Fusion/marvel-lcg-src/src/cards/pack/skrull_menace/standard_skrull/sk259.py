from . import *

# Stick to the Plan — TRAITRISE x2 (Standard Skrull). Aucune icone de boost.
# When Revealed: The villain attacks the hero with the most remaining hit points. If no attack was made this
#   way, the villain schemes.
#
# Cartes de reference :
#  - « The villain attacks <joueur> » : **`01187`** Assault (`villain.DoAttackYou(joueur, effect)`).
#  - « the hero with the most remaining hit points » : `Filter.One(candidats, effect, most_remaining_hp=True)`
#    (modele sk098 Impostor ; operate/filter.py) ; les candidats sont les identites en forme HEROS.
#  - « the villain schemes » : **`sk098`** (`DoSchemes`).
#
# ⚠ Mots-pieges : « the HERO » (une identite en forme heros ; un joueur en alter-ego n'est pas un « hero ») ;
# « most REMAINING hit points » (PV restants, pas PV max ; egalite : le joueur choisit) ; « If NO attack was made »
# : aucun heros en jeu, ou attaque empechee -> le mechant complote CONTRE le joueur qui revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        mechant = LeMechant(effect)
        if mechant is None:
            return
        heros = [j.GetIdentity() for j in Worlds.GetPlayers(effect) if j.IsHero() and not j.is_eliminated]
        cible = Filter.One(heros, effect, most_remaining_hp=True) if heros else None
        attaque = None
        if cible is not None:
            attaque = mechant.DoAttackYou(cible.GetControlByPlayer(), effect)
        if attaque is None:
            mechant.DoSchemes(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
