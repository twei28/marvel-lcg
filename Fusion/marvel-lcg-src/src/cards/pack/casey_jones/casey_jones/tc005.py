from . import *

# Grand Slam — EVENEMENT, cout 3, [physical]. ATTACK. x2.
# Requirement ([wild]). (While paying for this card, spend the listed resources.)
# Hero Action (attack): Deal 8 damage to an enemy.
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# BASE AUTOMATIQUE : `desc.Requirement = "G"` (une icone wild : meme glyphe que
# `04010`, verifiee par decoupe). AUCUN SCRIPT pour lui. « 3 dont au moins 1
# wild », pas « 3 + 1 ». Precedent : `dt084` Off the Cuff (`"Requirement": "G"`).
#
# CARTES DE REFERENCE
#  - `raphael/tr004` Headbutt : `SetPlay().SetLabel('attack').SetTarget(Enemy)`
#    + `heros.DealDamage(cibles, N, effect)` (le heros est l'auteur).
#
# TEXTE CONTRE CODE
#  ⚠ « Deal 8 damage » : 8, pas 3 ; sur l'ennemi CHOISI (vilain ou sbire).
#  ⚠ Le Requirement est lu dans `desc`, pas dans ce script.


def GetAbilities() -> Sequence['Ability']:

    def grand_slam(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        heros = joueur.GetHero()
        cibles = [t for t in effect.targets if t is not None]
        if heros is None or not cibles:
            return
        heros.DealDamage(cibles, 8, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            grand_slam,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
