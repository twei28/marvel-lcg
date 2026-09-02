from . import *

# * Bruce Banner (face alter-ego) — GENIUS. SCIENTIST.
# REC 4 — HS 6 / PV 15
# Bring Out The Big Guy — Interrupt: When an enemy would scheme, spend a
#   [physical] resource -> change to your hero form. That enemy attacks you
#   instead.
#
# Carte de reference : **`52019` Ready for a Fight** (pack `silk`),
# src/cards/pack/silk/52019.py. C'est un JUMEAU MOT POUR MOT :
#   « Interrupt: When an enemy would scheme, discard Ready for a Fight ->
#     change to hero form. That enemy attacks you instead. »
# Meme declencheur, meme paire d'effets, meme ordre. Seul le COUT differe :
# defausser l'amelioration la-bas, depenser une ressource physique ici.
#
# ⚠ Le dossier de preparation annonçait « aucun modele identifie dans le
# depot, c'est le seul vrai point d'attention du pack ». C'est FAUX : le grep
# du 02/09/2026 a rendu 52019 immediatement. La prepa a ete corrigee.
#
# Montage repris tel quel de 52019 :
#   `WhenUnitWouldScheme(Interrupt, Enemy, op).SetTarget("YourIdentity")`
#   puis, dans l'ordre imprime :
#     1. `effect.targets[0].CastTo(Identity).ChangeToForm(Hero, effect)`
#     2. `message.SetBeInstead(effect)`
#     3. `message.trigger.CastTo(Enemy).DoAttackYou(initiator, effect)`
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « an ENEMY would scheme » : vilain ET sbires, aucun filtre de type
#    au-dela d'`Enemy`.
#  - L'ORDRE compte et il est respecte : on change de forme AVANT que
#    l'attaque ne parte, sinon Bruce Banner (qui ne defend pas) encaisserait
#    l'attaque en forme civile. C'est tout l'interet de la carte.
#  - « spend a [physical] resource » est un COUT, pas une condition d'effet :
#    `SetCost(Cost("R"))`. A ne pas confondre avec le « if you paid using a
#    [physical] resource » de hk006, qui est une condition d'EFFET.
#  - « That enemy attacks YOU » : le joueur, donc `DoAttackYou(initiator)`.
#  - `Interrupt` nu, et non `Alter-Ego Interrupt` : la carte EST la face
#    alter-ego, elle n'existe que dans cette forme de toute facon.


def GetAbilities() -> Sequence['Ability']:

    def bring_out_the_big_guy(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None or not effect.targets:
            return

        effect.targets[0].CastTo(Identity).ChangeToForm(Hero, effect)
        message.SetBeInstead(effect)
        message.trigger.CastTo(Enemy).DoAttackYou(initiator, effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.Interrupt,
            Enemy,
            bring_out_the_big_guy,
        ).SetCost(Cost("R"))
        .SetName("Bring Out The Big Guy")
        .SetTarget("YourIdentity"),
    ]
