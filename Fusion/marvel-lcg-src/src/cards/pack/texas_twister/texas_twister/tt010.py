from . import *

# * Texas Twister's Hat — AMELIORATION, cout 2, [mental]. ITEM.
# Texas Twister gains steady.
# Alter-Ego Action: Exhaust Texas Twister's Hat -> ready Drew Daniels.
#
# CARTE DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached`, bonus continu d'une
#    amelioration de heros. Le parametre `steady=` y est expose (asset.py:28).
#
# MOT-CLE : STEADY — fiche `docs/reference/mots-cles/steady.md`, lue avant
# d'ecrire. Steady donne DEUX compteurs Etourdi et DEUX compteurs Confus de
# marge : le personnage n'est reellement etourdi qu'au deuxieme. La fiche
# insiste sur un point : le mot-cle est normalement lu dans `desc.Steady` et
# ne demande AUCUN script. Ici il est ACCORDE par une autre carte, ce qui est
# le seul cas ou il faut l'ecrire — et `GiveKeywordToAttached(steady=1)` est
# la voie prevue par le moteur.
#
# TEXTE CONTRE CODE
#  « ready DREW DANIELS » -> l'ALTER-EGO, pas le heros : la carte se joue en
#    forme heros (c'est une amelioration de heros) mais ne sert qu'en forme
#    civile. ⚠ Et l'obligation tt020 interdit precisement de redresser
#    l'identite : les deux cartes se parlent.
#  ⚠ `Faces.ReadyAll` sur l'identite, pas sur `this` : c'est l'IDENTITE qui
#    est redressee, l'amelioration, elle, s'incline en COUT.


def GetAbilities() -> Sequence['Ability']:

    def redresser_le_civil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            steady=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            redresser_le_civil,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
