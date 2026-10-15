from . import *

# Tricky Assault — TRAITRISE (Expert Skrull). 2 icones de boost. (Numero imprime « 162 » : coquille, card_id sk262.)
# When Revealed: Flip to hero form. The villain attacks you. If this attack is undefended, the villain schemes.
#
# Cartes de reference :
#  - « Flip to hero form » : `identite.ChangeToForm(Hero, effect)` (identity.py, modele `YouMayFlipToYourAlterEgoForm`
#    de cards/pack/__init__.py dans l'autre sens).
#  - « The villain attacks you. If this attack is undefended ... » : **`01187`** Assault (`villain.DoAttackYou`) avec
#    le crochet `if_undefended=` de `Enemy.DoAttackYou` (enemy.py) ; modele **`sk100`** Emperor's Throne.
#
# ⚠ Mots-pieges : « FLIP to hero form » : un joueur deja en heros ne fait rien (pas de retour en alter-ego) ;
# le changement n'est PAS la flip normale d'un tour (pas de limite une fois par tour) ; « The villain attacks YOU »
# (le joueur qui revele, maintenant en heros) ; « UNDEFENDED » : personne n'a defendu (un defenseur, meme s'il subit
# tout, annule le complot) ; le complot est CONTRE ce joueur.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur.IsAlterEgo():
            joueur.GetIdentity().ChangeToForm(Hero, effect)
        mechant = LeMechant(effect)
        if mechant is None:
            return
        mechant.DoAttackYou(joueur, effect, if_undefended=lambda: mechant.DoSchemes(joueur, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
