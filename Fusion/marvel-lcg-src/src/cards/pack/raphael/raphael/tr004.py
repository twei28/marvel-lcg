from . import *

# Headbutt — EVENEMENT, cout 2, [physical]. ATTACK. x2.
# Requirement ([physical][physical]).
# Hero Action (attack): Deal 4 damage to an enemy. Stun or confuse that enemy.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# `desc.Requirement = "RR"` : « 2 dont au moins 2 physiques » sur une carte a
# cout 2, c'est-a-dire que les DEUX ressources doivent etre physiques.
#
# CARTES DE REFERENCE
#  - `ma015` Break Through : « stun OR confuse an enemy » = deux
#    `ForChoiceAbility` dans un `ChooseAbilities`, avec `canbe_stunned` /
#    `canbe_confused`. Ici la cible est CELLE DE L'ATTAQUE (« that enemy »),
#    pas un second choix : les options visent la meme carte, sans `SetTarget`.
#  - `01053` : `hero.DealDamage(effect.targets, n, effect)` pour que le HEROS
#    soit l'auteur des degats (Raphael « defeats an enemy » de `tr012`).
#  - `ho003` : modele de montage `SetPlay().SetLabel('attack').SetTarget(Enemy)`.
#
# TEXTE CONTRE CODE
#  ⚠ « THAT enemy » -> la cible des 4 degats, jamais une nouvelle selection.
#    Si elle est vaincue par les degats, il n'y a plus rien a etourdir : les
#    options sont alors sans effet (le statut ne se pose pas sur une carte
#    hors jeu).
#  ⚠ « Stun OR confuse » : un CHOIX du joueur, pas les deux. Le pilote du
#    harnais prend la premiere option : la branche « confuse » n'est atteignable
#    qu'avec `preferer_option` en phase C.
#  ⚠ « Deal 4 damage » AVANT « stun or confuse » : l'ordre imprime.
#  ⚠ Homonyme : `07058` Headbutt est une trahison du pack Thunderball. Rien ici
#    ne cherche par le nom.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_boule(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        cibles = [t for t in effect.targets if t is not None]
        if heros is None or not cibles:
            return

        heros.DealDamage(cibles, 4, effect)

        vivants = [t for t in cibles if t.IsInPlay()]
        if not vivants:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Headbutt: stun that enemy",
                lambda targets:
                    Faces.GiveStatus(vivants, "Stunned", effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Headbutt: confuse that enemy",
                lambda targets:
                    Faces.GiveStatus(vivants, "Confused", effect),
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            coup_de_boule,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
