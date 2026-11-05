from . import *

# Cleave The Way — TRAITRISE NEMESIS (4/5).
#
# Texte imprime :
#  « When Revealed: Find and reveal Terrax's Axe. Then, the character that
#    Terrax's Axe is attached to attacks you. »
#
# CARTES DE REFERENCE
#  - `pc021` Terrax's Axe porte sa PROPRE regle d'attache (`pc019.py` :
#    « find X and attach it to Terrax » met deja en jeu de la meme facon) :
#    il suffit de `Find.FindAndReveal`, elle s'attache TOUTE SEULE.
#  - `dz023` Taunting Light (dazzler_nemesis) : `vilain.DoAttackYou(joueur,
#    effect, if_no_attack_was_made=...)` -- modele pour « <character>
#    attacks you », y compris le repli « if no attack was made this way »
#    (vilain etourdi, modele 27029/22031).
#
# TEXTE CONTRE CODE
#  « Find AND REVEAL Terrax's Axe » : si un exemplaire est deja en jeu
#    (attachee a Terrax ou au mechant depuis un tour precedent), rien de
#    nouveau n'est trouve -- `Find.FindAndReveal` rend alors None, et aucune
#    attaque forcee n'a lieu non plus (le texte suppose la carte TROUVEE).
#  « THE CHARACTER THAT Terrax's Axe is attached to attacks you » : le
#    PORTEUR actuel de la hache (Terrax ou le mechant selon qui etait en jeu
#    au moment de l'attache), jamais Terrax par defaut.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        hache = Find.FindAndReveal(
            effect, joueur,
            name="Terrax's Axe",
            card_type=Attachment,
        )
        if hache is None:
            return
        porteur = hache.GetBindFace()
        if porteur is not None and Enemy.IsType(porteur):
            porteur.CastTo(Enemy).DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
