from . import *

# Psi-Web Trap — EVENEMENT, cout 0, RES [mental], x2.
# PSIONIC. SUPERPOWER. THWART.
# Hero Action (thwart): Remove X psionic web counters from Spider-Woman ->
#   remove X threat from a scheme.
#
# ⚠ LA JUMELLE EXACTE DE `sw007` Psionic Web Blast, a un mot pres :
#     sw006  THWART  X menaces retirees d'une manigance
#     sw007  ATTACK  X degats a un ennemi
# Meme cout, meme prix, meme structure.
#
# CARTE DE REFERENCE
#  - `sw001a` Spider-Woman : le meme stock, `RetirerDesToiles`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « Remove X counters -> remove X threat » : X n'est PAS choisi librement,
#    c'est ce qu'on RETIRE VRAIMENT. Demander 5 avec 2 compteurs en stock ne
#    retire que 2 menaces — d'ou la valeur RENDUE par `RetirerDesToiles`, et
#    jamais celle demandee.
#  ⚠ La fleche fait du retrait un COUT : stock vide, la carte ne se joue pas
#    pour rien, elle ne fait rien.
#  ⚠ « from A SCHEME » : une seule, au choix. C'est `sw009` Web Formation qui
#    frappe toutes les manigances.


def GetAbilities() -> Sequence['Ability']:

    def piege_de_toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cibles = [c for c in effect.targets if c is not None]
        if joueur is None or not cibles:
            return
        combien = DemanderCombienDeToiles(joueur, effect)
        retire = RetirerDesToiles(joueur, combien, effect)
        if retire > 0:
            this.RemoveThreatFromSchemes(cibles, retire, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            piege_de_toile,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
