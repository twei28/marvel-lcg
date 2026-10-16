from . import *

# Out of Control — OBLIGATION. 2 icones de boost (deux icones rouges lues sur
# le scan). Bandeau « RAPHAEL » (set du HEROS, donc module dans raphael/raphael/,
# PAS dans raphael_nemesis/ : piege bt019 & suivants).
# Give to the Raph player.
# Flip to hero form and exhaust your identity. You cannot change forms, thwart,
#   or defend.
# Hero Action: Remove 2 rage counters from Raphael -> flip to alter-ego form
#   and discard Out of Control.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `vv011` Grounded / `36030` Claustrophobia : obligation qui force une forme,
#    interdit de changer de forme (`PlayersCannotChangeForms(NonKeyword,
#    "AttachedPlayer")`, qui EXCLUT deja l'effet de sa propre carte :
#    player.py:~118 `effect.this != message.by_effect.this` — c'est ce qui
#    laisse l'Action de sortie retourner Raph en civil).
#  - `30024` : `WhenThisObligationGiveToYou` + `message.GetGaveToPlayer()` pour
#    agir sur le joueur destinataire.
#  - `32150` Wrapped in Metal : « cannot thwart / defend » =
#    `UnitCannotThwartTarget(..., cannot_thwart=True,
#    cannot_trigger_thwart_ability=True)` et `UnitCannotDefend(...,
#    cannot_trigger_defense_ability=True)`. Ici la cible est « YOU » = l'IDENTITE
#    (`"YourIdentity"`, qui gere la zone des obligations : condition.py
#    `check_you` / `is_obligations_area`), PAS les allies.
#  - `attachment.py:8` `PlayerActionToDiscardThis(type, ex_operation=...)` pour
#    « ... -> flip ... and discard this card » ; cout `CostFunc.Counter(
#    "YourIdentity", 2, 'rage')` (modele 30024).
#
# TEXTE CONTRE CODE
#  ⚠ « Flip to hero form AND exhaust your identity » : deux effets obligatoires
#    a la reception (pas « you may »), dans cet ordre.
#  ⚠ « You cannot CHANGE FORMS, THWART, or DEFEND » : trois interdictions
#    continues, sur l'IDENTITE seulement ; les allies peuvent contrer et
#    defendre. Un « cannot thwart » vise aussi les capacites d'evenement.
#  ⚠ « REMOVE 2 rage counters FROM RAPHAEL -> » : COUT (fleche), pris sur la
#    carte d'identite ; sans 2 compteurs l'Action n'est pas offerte. Rien ne
#    plafonne ni ne donne de rage ici : le joueur doit en avoir gagne.
#    Decision du 15/10/2026 : « vous » = l'IDENTITE seulement (les allies
#    peuvent contrer et defendre). Le texte n'a PAS de sortie sans rage : lecture
#    litterale conservee (seul moyen : gagner de la rage par les allies, Gekido,
#    Seething Rage...).
#  ⚠ « flip to alter-ego form AND discard Out of Control » : l'ordre imprime,
#    `ex_operation` s'execute AVANT la defausse. « discard » : l'obligation
#    retourne au deck rencontre du joueur (pas `RemoveFromGame`).
#  ⚠ `desc.GiveTo = "Raph"` : le nom de l'ALTER-EGO (PROCESSUS-HEROS etape 1).


def GetAbilities() -> Sequence['Ability']:

    def hors_de_controle(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        # « Flip to hero form » : sans effet si deja en forme heros.
        identite.ChangeToForm(Hero, effect)
        # « and exhaust your identity » : on relit l'identite, la face a change.
        Faces.ExhaustAll([joueur.GetIdentity()], effect)

    def reprendre_forme_civile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            hors_de_controle,
        ),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
        ),
        *AbilityFactory.UnitCannotThwartTarget(
            "YourIdentity",
            cannot_thwart=True,
            cannot_trigger_thwart_ability=True,
        ),
        *AbilityFactory.UnitCannotDefend(
            "YourIdentity",
            None,
            cannot_trigger_defense_ability=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            ex_operation=reprendre_forme_civile,
        ).SetCostFunc(CostFunc.Counter("YourIdentity", 2, RAGE)),
    ]
