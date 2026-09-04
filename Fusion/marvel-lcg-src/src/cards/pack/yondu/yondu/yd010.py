from . import *

# Ravage — amelioration signature, x1 (n/15 = 13). SKILL. TACTIC.
# Cout 2, ressource [mental].
# Minions with a wound counter gain the fragile keyword. (Attacks against
#   fragile characters gain overkill.)
# Hero Response: After the Yaka Arrow upgrade is attached to a minion, exhaust
#   Ravage -> place a wound counter on that minion.
#
# Cartes de reference :
#  - **`Fragile()`** (src/cards/pack/determination/__init__.py:12) et la fiche
#    `docs/reference/mots-cles/fragile.md` : le crochet est OFFICIEL, c'est
#    `33032` Marked — `WhenUnitWouldAttackUnit` + `message.GainOverKill`.
#    ⚠ Le helper du pack determination est cable sur `"This"` ; ici la cible
#    n'est pas cette carte mais TOUT sbire portant un compteur, d'ou
#    l'ecriture directe avec `CardFinder(card_type=Minion,
#    has_counter='wound')`.
#  - **`AfterCardAttachTo`** (card_move.py:141), le meme declencheur que
#    `yd001a` D'ast Whistlin' — les deux cartes ecoutent le meme mouvement, et
#    Ravage ajoute le compteur pendant que le heros inflige son degat.
#  - `34001b` * Jean Grey / `as013` pour `Faces.PlaceCountersOn`.
#
# ⚠ COMPTEUR MAISON `wound`, ajoute a l'enum `COUNTER`
# (src/game/card/face/card_face.py) pour cette carte. Sans lui, `IsCounter`
# refuse le nom et la carte tombe des la CREATION de la partie, pas en jeu.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Minions** with a wound counter » : les SBIRES seulement. Un vilain
#    portant un compteur ne devient pas fragile, et la fleche peut fort bien
#    se planter sur lui.
#  - « attached to a **MINION** » : la Reponse ne se declenche pas quand la
#    fleche arrive sur le vilain ni sur l'identite. C'est le seul endroit du
#    pack qui distingue sbire et vilain.
#  - « on **that** minion » : celui qui vient de recevoir la fleche, jamais un
#    choix (piege `wd022`). Il se lit dans `message.to_face`.
#  - « exhaust Ravage **->** » : COUT. Deja inclinee, elle ne pose plus rien.
#  - La parenthese « (Attacks against fragile characters gain overkill.) » est
#    la DEFINITION du mot-cle, rappelee par la carte : elle ne se code pas
#    deux fois.


def GetAbilities() -> Sequence['Ability']:

    def fragile(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    def sur_un_sbire(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> bool:
        Unused(effect)
        return message.to_face is not None and Minion.IsType(message.to_face)

    def ravage(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.PlaceCountersOn([message.to_face], 1, 'wound', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            CardFinder(card_type=Minion, has_counter='wound'),
            fragile,
        ),
        AbilityFactory.AfterCardAttachTo(
            AbilityType.HeroResponse,
            CardFinder(name=NOM_FLECHE, card_type=Upgrade),
            None,
            ravage,
            conditions=[sur_un_sbire],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
