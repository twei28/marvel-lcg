from . import *

# Revenge — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [physical], `MaxPerUnit "1"`, aucun trait.
#
# Attach to an ally. Max 1 per ally.
# Interrupt: When Patriot takes any amount of damage from an attack, discard
#   Revenge -> the attached ally gets +2 ATK until the end of the next round.
#
# ---------------------------------------------------------------------------
# « ATTACH TO AN ALLY. MAX 1 PER ALLY. »
#
# `AbilityFactory.CanPlayThisUpgradeCard(Ally)` : modele `01074` Inspired,
# `03031` Enraged, `12018` Reinforced Suit — les trois ameliorations
# officielles qui se posent sur un allie.
#
# ⚠ `MaxPerUnit` est lu NATIVEMENT dans `desc` : `HasMaxPer.max_per_unit`,
# relu par `Asset2.CanAttachTo` (base/asset.py:69-73) et par le
# `max_per_unit` interne de `CanPlayThisUpgradeCard` (play.py:122-124).
# AUCUN module a ecrire pour lui — coder une capacite fantome serait une
# faute (PROCESSUS-CARTE §5, « bases automatiques a ne pas recoder »).
#
# ---------------------------------------------------------------------------
# LE DECLENCHEUR : « WHEN PATRIOT TAKES ANY AMOUNT OF DAMAGE FROM AN ATTACK »
#
# `WhenUnitWouldTakeDamage(AbilityType.Interrupt, "YourHero", ...,
# is_from_attack=True)`.
#
#  - `"YourHero"` et non `CardFinder(name="Patriot")` : le catalogue contient
#    DEJA deux allies officiels nommes « Patriot » (`29016` et `56041`), et
#    une recherche par nom les attraperait. La cible-chaine `"YourHero"`
#    designe la face HEROS du controleur de cette amelioration, donc Patriot
#    et lui seul — et rien en identite civile, ce qui est correct : la carte
#    nomme le HEROS.
#  - `is_from_attack=True` rend « FROM AN ATTACK » : les degats de trahison
#    (« deal 1 damage to your identity ») ne declenchent RIEN.
#  - « ANY AMOUNT » : au moins 1. C'est deja le defaut de la fabrique
#    (`at_least_damage=1`), et on le reverifie sur `will_take_damage`.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « discard Revenge » -> `CostFunc.Discard("This")` (modele `mw007`
# Life-Support System, meme construction sur une amelioration). Si la carte
# ne peut pas etre defaussee, l'interruption n'est pas proposee.
#
# ---------------------------------------------------------------------------
# « UNTIL THE END OF THE **NEXT** ROUND » : DEUX FINS DE ROUND
#
# Piege : `GainUntilRoundEnd` (model/face_action.py:410) s'arrete a la fin du
# round COURANT — un round trop tot. Et `TemporaryGain(end_event=
# Message.WhenRoundEnd)` cable sa condition sur `lambda: True`
# (face_action.py:322-327), donc on ne peut pas y glisser de compteur.
#
# Aucune carte officielle n'imprime « until the end of the next round » : le
# seul precedent du depot est `sd017` No Outrunning This (pack speed), qui
# compte les fins de round a la main.
#
# Construction retenue, la plus simple qui soit juste :
#   1. `allie.Gain(effect, +1, attack=2)` applique le bonus
#      (model/face_gain.py:13, l'API que `TemporaryGain` appelle elle-meme) ;
#   2. une capacite TEMPORAIRE `WhenRoundEnd` est enregistree SUR L'ALLIE,
#      avec `round_id = effect.world.round_id + 1`. La fabrique
#      `AbilityFactory.WhenRoundEnd(ability_type, round_id, operation)`
#      (factory/turn_phase.py:284-303) compare `round_id == message.round_id`,
#      et `Message.WhenRoundEnd.round_id` vaut `world.round_id`
#      (sender_round.py:100-106). Le round N ne declenche donc RIEN, seul le
#      round N+1 rabaisse le bonus. C'est exactement « la fin du PROCHAIN
#      round ».
#
# ⚠ ENREGISTRE SUR L'ALLIE, PAS SUR REVENGE : Revenge est DEFAUSSEE par son
# propre cout, et une capacite temporaire posee sur une carte qui quitte le
# jeu part avec elle (lecon `sd017`). Corollaire voulu : si l'allie est
# vaincu avant la fin du prochain round, la capacite meurt avec lui — il n'y
# a plus rien a rabaisser.
#
# `world.round_id` est incremente au DEBUT de chaque round
# (world/world.py:755) : pendant la phase du vilain du round N il vaut bien N.


def GetAbilities() -> Sequence['Ability']:

    def revenge(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        if message.will_take_damage <= 0:
            return

        # ⚠ L'ALLIE PORTEUR EST LU DANS `effect.targets`, PAS PAR
        # `this.GetBindFace()`. Le cout (`CostFunc.Discard("This")`) est paye
        # AVANT que le corps ne s'execute (`Effect.ProcessSelfCost`,
        # effect.py:135, appele en tete de `ResolveSelfInternal`) : a ce
        # moment-la Revenge est DEJA dans la defausse, elle n'a plus de
        # porteur, et `GetBindFace()` leve un `AssertionError` seche —
        # AVALEE par le moteur, donc invisible partout sauf dans le journal
        # d'une partie reellement jouee. Bug trouve par
        # `tools/test_capacites.py` le 30/08/2026 (cas pt013).
        #
        # Les CIBLES, elles, sont choisies avant le paiement et rangees dans
        # `effect.context.targets_internal` : la cible-chaine `"Attached"`
        # (selector_target_helper.py:29-34) rend donc le porteur d'origine,
        # meme apres la defausse.
        if not effect.targets:
            return
        allie = effect.targets[0]
        if not Ally.IsType(allie) or not allie.IsInPlay():
            return

        allie.Gain(effect, +1, attack=2)

        fin_du_prochain_round = effect.world.round_id + 1

        def rabaisser(e2: 'Effect', m2: 'Message.WhenRoundEnd') -> None:
            Unused(m2)
            if allie.card.face.IsInPlay():
                allie.Gain(e2, -1, attack=2)

        allie.effect.RegisterTemp(
            AbilityFactory.WhenRoundEnd(
                AbilityType.Temp2,
                fin_du_prochain_round,
                rabaisser,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "YourHero",
            revenge,
            is_from_attack=True,
        ).SetTarget("Attached", range=(1, 1), not_move=True)
        .SetCostFunc(CostFunc.Discard("This")),
    ]
