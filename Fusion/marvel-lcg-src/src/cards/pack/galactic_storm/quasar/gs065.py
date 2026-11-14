from . import *

# Protector of the Universe — OBLIGATION de Quasar (numero imprime 65, bandeau
# « QUASAR » sans n/16). 2 icones de boost (chevrons rouges, convention validee).
# Give to the Wendell Vaughn player.
# Uses (3 duty counters).
# You cannot flip to alter-ego form.
# Hero Response: After you defeat an enemy or a scheme, or defend against an
#   attack and take no damage, remove 1 duty counter from here.
#
# Cartes de reference :
#  - **`tr013`** Out of Control / `vv011` Grounded / `36030` : obligation qui
#    reste en jeu et interdit un changement de forme :
#    `PlayersCannotChangeForms(NonKeyword, "AttachedPlayer", to_form=AlterEgo)`
#    (factory/player.py) ; « AttachedPlayer » = le joueur qui l'a recue.
#  - **`sk029`** Glorious Flight / `52001a` Silk : « After you defeat an enemy
#    or a side scheme » = `AfterUnitDefeatedUnit(type, "You", Enemy, op)` +
#    `AfterUnitDefeatedScheme(type, "You", <manigance>, op)`.
#  - **`bt001a`** Beast / `09020` Unflappable : « defend against an attack and
#    take no damage » = `AfterUnitDefendAgainstAttack(type, "You", op,
#    take_no_damage=True)`.
#  - **`53029`** : retrait d'un pion d'une carte a Uses,
#    `Faces.RemoveCountersOn([this], 1, '<nom>', effect)` (fiche uses.md).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Uses (3 duty counters) » : base automatique (desc.Uses, has_uses.py) :
#    les 3 pions a l'entree en jeu, et la carte PART quand le dernier est
#    retire (regle du mot-cle, rien d'imprime, rien a coder : fiche uses.md).
#    Compteur `duty` ajoute a l'enum CardFace.COUNTER (20/10/2026).
#  - « You cannot flip to ALTER-EGO form » : seulement vers l'alter ego ; un
#    joueur deja en civil a la reception peut passer en heros, puis ne plus
#    revenir (`to_form=AlterEgo`).
#  - « an enemy OR A SCHEME » : sbire ou vilain (Enemy), et une manigance
#    vaincue (videe de sa menace) ; le complot principal ne se « vainc » pas.
#  - « defend against an attack AND TAKE NO DAMAGE » : il faut avoir DEFENDU
#    (pas une attaque non defendue absorbee par Tenace).
#  - « you » : le joueur qui a recu l'obligation (ses cartes comprises, comme
#    sk029) ; « remove 1 duty counter FROM HERE » : sur cette obligation.
#  - Trois declencheurs, UNE Reponse de heros chacun, sans limite imprimee.
#  - « **Hero** Response » : forme heros (de toute facon imposee tant qu'elle
#    est en jeu, sauf si elle arrive en civil).
#  - `desc.GiveTo = "Wendell Vaughn"` : le nom de l'ALTER EGO (PROCESSUS-HEROS
#    etape 1).


def GetAbilities() -> Sequence['Ability']:

    def retirer_un_devoir(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, 'duty', effect)

    return [
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
            to_form=AlterEgo,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Enemy,
            retirer_un_devoir,
        ),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            Scheme2,
            retirer_un_devoir,
        ),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            retirer_un_devoir,
            take_no_damage=True,
        ),
    ]
