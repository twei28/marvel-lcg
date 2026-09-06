from . import *

# Solar Blast — EVENEMENT, cout 2, [energy]. ATTACK. FIRE. SUPERPOWER. x3.
# Hero Action (attack): Deal 3 damage to an enemy. Choose an attachment with
#   the text "Hero Action" or "Hero Response" attached to that enemy and
#   discard it. Otherwise, attach a set-aside copy of Burning to that enemy.
#
# CARTES DE REFERENCE
#  - `sf003` Burning Hands : la carte jumelle, cote contre. Meme phrase, UNE
#    difference imprimee, voir ci-dessous.
#  - `bc004` / `bc010` : la selection d'un attachement PAR SON TEXTE.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « attached TO THAT ENEMY » — C'EST LA SEULE DIFFERENCE AVEC `sf003`, et
#    elle est imprimee. Ici on ne regarde QUE les attachements de l'ennemi
#    frappe ; `sf003`, qui n'a pas cette clause, regarde tout le terrain.
#    Harmoniser les deux serait une erreur, et la difference est OBSERVABLE :
#    un attachement pose sur un AUTRE ennemi n'est pas arrachable par cette
#    carte-ci.
#  ⚠ « OTHERWISE, attach ... TO THAT ENEMY » -> le repli vise le MEME ennemi,
#    pas un au choix. Seconde difference avec `sf003`, imprimee elle aussi.
#  ⚠ « OTHERWISE » n'est pas un choix : le repli tombe quand cet ennemi-la ne
#    porte aucun attachement eligible.
#  ⚠ ORDRE : les 3 degats tombent AVANT. Si l'ennemi meurt, il n'y a plus
#    d'attachement a arracher ni d'ennemi a brûler — et c'est ce que dit la
#    carte, dans cet ordre.
#  « Deal 3 damage to AN ENEMY » -> une seule cible.


def GetAbilities() -> Sequence['Ability']:

    def rayon_solaire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets or [])
        this.DealDamage(cibles, 3, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for cible in cibles:
            if cible is None or not cible.IsInPlay():
                continue
            # ⚠ SEULEMENT les attachements de CET ennemi (voir l'encadre).
            candidats = [f for f in cible.GetAttachedAttachments()
                         if AttachementAvecActionDeHeros(f)]
            if candidats:
                choisi = joueur.AskChooseFace(candidats, effect)
                if choisi is not None:
                    Faces.DiscardAll([choisi], effect)
                    continue
            # « OTHERWISE, attach a set-aside copy of Burning TO THAT ENEMY. »
            AttacherUneBrulure(effect, cible, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rayon_solaire,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
