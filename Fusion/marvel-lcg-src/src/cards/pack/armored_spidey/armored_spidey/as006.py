from . import *

# Kick It! — evenement signature, x2. ATTACK. Cout 2, ressource [physical].
# Hero Action (attack): Deal 4 damage to an enemy. You may remove 1 metal
#   counter from Spider Armor to stun that enemy.
#
# Cartes de reference :
#  - `05015` Tackle / `ho003` / `im002` pour l'evenement d'attaque :
#    `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)`.
#  - **`im002`** Repulsor Barrage (pack iron_man_model_42) pour le « you may »
#    paye en compteur : `MayChooseOneAbility(ForChoiceAbility(...))` puis
#    retrait dont on LIT le retour.
#  - `05015` / `01083` pour `Faces.GiveStatus(cibles, "Stunned", effect)` et
#    le filtre `canbe_stunned=True`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « to stun **that** enemy » : LA MEME cible que celle des 4 degats, pas un
#    second choix (piege `wd022`). D'ou `effect.targets`, jamais un nouveau
#    selecteur — c'est la difference exacte avec as009 Swing It!, qui ecrit
#    « confuse **an** enemy » et ouvre bien un second ciblage.
#  - « **You may** remove 1 metal counter **to** stun » : facultatif, et le
#    « to » en fait la condition du bonus, pas de la carte. Les 4 degats
#    tombent de toute facon — c'est pourquoi le retrait passe ici par
#    `RetirerUnMetal` (corps) et non par `CostFunc.Counter` : la carte ne
#    peut pas resoudre en ne faisant rien, donc aucun risque de boucle
#    d'autoplay (leçon im007/im013).
#  - Sans compteur sur l'armure, l'option n'est meme pas proposee : le test
#    `CompteursMetal` precede le `MayChooseOneAbility`.
#  - « **(attack)** » : le libelle alimente Sonne et la Riposte. `SetLabel`
#    ne s'appelle QU'UNE fois (assert ability.py:380).
#  - « Deal 4 damage » sans mot-cle : ni portee, ni percant. Ne rien ajouter.


def GetAbilities() -> Sequence['Ability']:

    def kick_it(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets)
        this.DealDamage(cibles, 4, effect)

        if CompteursMetal(effect) < 1:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        choix = initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 metal counter to stun that enemy",
                lambda targets: None,
            ),
        )
        if choix is not None and RetirerUnMetal(effect):
            Faces.GiveStatus(cibles, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kick_it,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
