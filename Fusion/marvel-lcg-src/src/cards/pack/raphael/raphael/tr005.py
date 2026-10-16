from . import *

# Savage Assault — EVENEMENT, cout 4, [physical]. ATTACK.
# Requirement ([physical][physical][physical]).
# Hero Action (attack): Deal 10 damage divided among enemies as you choose.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# `desc.Requirement = "RRR"` sur une carte a cout 4 : 3 physiques au minimum
# parmi les 4 ressources.
#
# CARTES DE REFERENCE
#  - `vp003` Talk About Armed Assault / `13006` Wasp Sting : « N damage divided
#    among enemies as you choose » = `SetTarget(Enemy, range=(1, N),
#    repeat_rules="Health")` + 1 degat par selection. `repeat_rules="Health"`
#    autorise a reprendre la MEME cible tant qu'elle a des PV, ce qui permet de
#    mettre les 10 degats sur un seul ennemi.
#  - `01053` : `hero.DealDamage(...)` pour que Raphael soit l'auteur.
#
# TEXTE CONTRE CODE
#  ⚠ « 10 damage DIVIDED among enemies AS YOU CHOOSE » : le joueur repartit,
#    il n'y a pas 10 degats a CHAQUE ennemi (piege `each`).
#  ⚠ `range=(1, 10)` autorise a choisir MOINS de 10 cibles (donc a perdre des
#    degats), comme `vp003` : c'est la borne maximale du precedent, pas un
#    « exactement 10 ». Le pilote du harnais ne prend qu'UNE selection (le
#    minimum) : le cas de phase C doit forcer `cibles` et mesurer le total.
#  ⚠ Plafond de PV : `repeat_rules="Health"` n'autorise pas plus de selections
#    que le total de PV restants (sbires + vilain) ; en dessous de 10 PV au
#    total, tous les points ne sont pas distribuables. Meme comportement que
#    les cartes modeles.


def GetAbilities() -> Sequence['Ability']:

    def assaut_sauvage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        if heros is None:
            return
        heros.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            assaut_sauvage,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 10), repeat_rules="Health"),
    ]
