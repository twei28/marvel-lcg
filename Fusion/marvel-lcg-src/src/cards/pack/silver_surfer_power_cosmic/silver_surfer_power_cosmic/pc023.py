from . import *

# Hungry Master — TRAITRISE NEMESIS (5/5).
#
# Texte imprime :
#  « When Revealed: add 1 threat to the Herald of Galactus side scheme,
#    then Terrax attacks you. If no attack was made this way, this card
#    gains surge. »
#
# CARTES DE REFERENCE
#  - `sm014`/`this.PlaceThreatOnSchemes([cible], n, effect)` : « add 1
#    threat to the Herald of Galactus side scheme », cible trouvee par
#    `Worlds.FindCardOnField(effect, name=.., card_type=EncounterSideScheme)`.
#  - `dz023` Taunting Light (dazzler_nemesis) : `minion.DoAttackYou(joueur,
#    effect, if_no_attack_was_made=...)` -- « Terrax attacks you », avec le
#    repli « if no attack was made this way ».
#  - `ThisCardGainSurge(effect)` (helper global, modele `ag014`) : « this
#    card gains surge ».
#
# TEXTE CONTRE CODE
#  « add 1 threat to the Herald of Galactus side scheme » : seulement si le
#    complot annexe est bien EN JEU (absent, aucune menace ajoutee, mais
#    l'attaque de Terrax suit quand meme -- le texte ne lie pas les deux
#    phrases par une condition).
#  « TERRAX attacks you » : Terrax precisement, jamais le mechant actif si
#    ce n'est pas lui (absent -> « if no attack was made », surge).
#  « IF NO ATTACK WAS MADE this way » : couvre a la fois « Terrax absent »
#    et « Terrax etourdi » (`if_no_attack_was_made`, modele 27029/22031).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        complot = Worlds.FindCardOnField(effect, name="Herald of Galactus", card_type=EncounterSideScheme)
        if complot is not None:
            complot.PlaceThreatOnSchemes([complot], 1, effect)

        terrax = Worlds.FindCardOnField(effect, name="Terrax", card_type=Minion)

        def aucune_attaque() -> None:
            ThisCardGainSurge(effect)

        if terrax is not None:
            terrax.CastTo(Enemy).DoAttackYou(joueur, effect, if_no_attack_was_made=aucune_attaque)
        else:
            aucune_attaque()

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
