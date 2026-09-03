from . import *

# * Thor (Odinson) — ALLIE signature, x1 (n/15 = 1).
# ASGARD. AVENGER. Cout 3 / PV 3 / CTR 1* / ATQ 2*
# Ressource imprimee : etoile VERTE = wild (RES = "G"), verifiee sur le scan
# contre ls007 (icone MENTALE bleue) et ls006 (icone ENERGIE jaune) du meme
# pack — leçon Lockjaw, une icone ne se nomme jamais a vue.
# [star] Response: After Thor attacks, choose a player. Deal 1 damage to each
#   minion engaged with that player.
#
# Cartes de reference :
#  - `hk002` * Black Widow (pack hulk_rainy) pour le squelette « allie
#    signature avec une Response [star] » ;
#  - `AfterUnitAttackEnd(Response, "This", op)` (recette §1) pour « After
#    <allie> attacks » ;
#  - `50013` * Slingshot pour le choix d'un JOUEUR :
#    `SetTarget("Players")` puis `Players.ForEachTargets(cibles, fn)`, le fn
#    recevant un `Player`.
#
# ⚠ ECART AVEC L'HOMONYME OFFICIEL. `25013` * Thor: Odinson porte le meme nom
# ET le meme sous-titre, mais une capacite TOTALEMENT differente (une
# Interruption qui ajoute des cibles a sa propre attaque, payee en energie).
# Ne pas copier son module : ce sont deux cartes distinctes.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After Thor ATTACKS » : l'attaque suffit, aucun dégât requis. Ce n'est
#    ni « attacks and damages » ni « attacks or engages » — trois declencheurs
#    differents, et c'est le premier qui est imprime.
#  - « choose A PLAYER » : n'importe lequel de la table, pas forcement le
#    controleur de Thor. En solo il n'y en a qu'un, mais le code ne doit pas
#    l'ecrire en dur.
#  - « each minion engaged with that player » : TOUS ses sbires, sans choix et
#    sans exception — y compris celui que Thor vient d'attaquer, le texte ne
#    l'exclut pas.
#  - Le degat rendu n'est PAS une attaque : ni overkill, ni riposte adverse.
#  - Le `[star]` en tete de la Response est une capacite PERMANENTE de la
#    carte, pas une capacite de boost (fiche mots-cles/special.md).
#  - CTR 1* et ATQ 2* : l'etoile est le degat consequent, lu nativement dans
#    `desc`, aucun script.


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def frapper_les_sbires(joueur: 'Player') -> None:
            sbires = list(joueur.GetEngagedMinions())
            if sbires:
                this.DealDamage(sbires, 1, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to each minion engaged with that player",
                lambda cibles: Players.ForEachTargets(cibles, frapper_les_sbires),
            ).SetTarget("Players"),
        )

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            apres_attaque,
        ),
    ]
