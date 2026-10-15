from . import *

# Camouflage — TRAITRISE x3 (Secret Invasion). ★ + 1 boost.
# When Revealed (Queen Veranke): Flip Queen Veranke. Remove 3 suspicion counter from "Who Do You Trust?".
# When Revealed (Spider-Woman): Spider-Woman schemes.
# ★ Boost: Flip Queen Veranke, after this activation ends.
#
# Cartes de reference : **`sk189b`** (retourner Veranke : `Card.Flip`, helper `RetournerVeranke`) ; « the villain schemes » :
# **`sk098`** (`mechant.DoSchemes(joueur, effect)`) ; Boost « after this activation ends » : **`sk107`**
# (`RunAt.AfterEnemyActivationEnd`).
#
# ⚠ Mots-pieges : les deux « When Revealed » portent une CONDITION entre parentheses : la face visible du mechant
# (REVEALED = Queen Veranke, CAMOUFLAGED = Spider-Woman) ; « Remove 3 suspicion counter » (singulier imprime) : 3 jetons ;
# « Spider-Woman SCHEMES » contre le joueur qui revele (le mechant ne s'attaque pas) ; Boost : « Flip QUEEN VERANKE » : seulement
# si c'est sa face visible (la carte la renvoie sur Spider-Woman), jamais l'inverse.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if VerankeRevelee(effect):
            RetournerVeranke(effect)
            RetirerSoupcons(effect, 3)
        elif VerankeCamouflee(effect):
            Veranke(effect).DoSchemes(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def apres() -> None:
            if VerankeRevelee(effect):
                RetournerVeranke(effect)
        RunAt.AfterEnemyActivationEnd(effect, message.would_message, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
