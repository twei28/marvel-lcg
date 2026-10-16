from . import *

# Brainwashed Betrayal — OBLIGATION (Boost 2), donnee au joueur Leo.
# Flip to hero form and discard an ally you control. You cannot attack the
#   villain.
# Forced Response: After your turn begins, deal 3 damage to an ally.
# Alter-Ego Action: Exhaust Leo and take 2 damage -> remove Brainwashed
#   Betrayal from the game.
#
# Cartes de reference :
#  - `ls005` Lady Sif : `identite.ChangeToForm(Hero, effect)` (bascule FORCEE) ;
#  - `ls012` Unrequited Love : `WhenThisObligationGiveToYou(op)` ;
#  - `11049` Fear of Kang : `PlayersCannotAttackWhile("You", CardFinder(...))` ;
#  - `45080` Drawing Near : `AfterPlayerTurnBegin(ForcedResponse,
#    "AttachedPlayer", op)` sur une obligation, joueur lu par
#    `this.GetGaveToPlayer()` ;
#  - `32055` / `25028` : `PlayerActionToRemoveThisFromGame(AlterEgoAction)` ;
#  - `90106` / `vp008` : `CostFunc.TakeDamage(n, "YourIdentity")` en cout.
#
# Mots-pieges :
#  - « Flip to hero form » : OBLIGATOIRE (≠ « you may flip »). Si le joueur est
#    deja heros, rien a faire ;
#  - « discard AN ALLY YOU CONTROL » : un seul, au choix du joueur, uniquement
#    parmi les siens ; sans allie, rien ;
#  - « You cannot attack THE VILLAIN » : le vilain seulement (les sbires restent
#    attaquables). DECISION UTILISATEUR (15/10/2026) : lecture litterale, tant que
#    l'obligation est en jeu, pour le(s) joueur(s) vises par « You » ;
#  - « Forced Response: AFTER your turn begins » : AfterPlayerTurnBegin, pas
#    When ;
#  - « deal 3 damage to AN ALLY » : DECISION UTILISATEUR — n'importe quel allie en
#    jeu (lecture litterale), choisi par le joueur ; ici pas de filtre de
#    controle ;
#  - « Exhaust Leo AND take 2 damage -> » : DEUX parties de cout ; l'alter-ego
#    est « Leo » (la capacite est une Alter-Ego Action : le joueur doit donc
#    repasser en alter-ego avant de pouvoir s'en servir) ;
#  - desc.Boost = 2 (deux icones), desc.GiveTo = « Leo ».


def GetAbilities() -> Sequence['Ability']:

    def brainwashed_betrayal(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        # 1. « Flip to hero form » (obligatoire).
        if joueur.IsAlterEgo():
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.ChangeToForm(Hero, effect)

        # 2. « discard an ally you control ».
        allies = list(joueur.allies.Get())
        if allies:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard an ally you control",
                    lambda cibles: Faces.DiscardAll(
                        [f for f in cibles if f is not None], effect),
                ).SetTarget(Ally, from_where=["YouControlCards"]),
            )

    def trois_degats_a_un_allie(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)

        joueur = this.GetGaveToPlayer()
        if joueur is None:
            return
        allies = list(Worlds.GetOnFieldAllies(effect))
        if not allies:
            return
        choisi = joueur.AskChooseFace(allies, effect,
                                      prompt="Deal 3 damage to an ally")
        this.DealDamage([choisi or allies[0]], 3, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            brainwashed_betrayal
        ),
        AbilityFactory.PlayersCannotAttackWhile(
            "You",
            CardFinder(card_type=Villain),
        ),
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.ForcedResponse,
            "AttachedPlayer",
            trois_degats_a_un_allie,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity")),
    ]
