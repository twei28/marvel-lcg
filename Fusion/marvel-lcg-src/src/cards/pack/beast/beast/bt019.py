from . import *

# Unfinished Projects — obligation. Boost 2. GiveTo: Dr Hank McCoy.
# Give to the Hank McCoy player.
# You may flip to alter-ego form. Choose:
#  • Discard 2 upgrade/support cards in play -> remove Mutation Degeneration
#    from the game.
#  • Exhaust your identity and take 2 damage. Discard this obligation.
#
# Cartes de reference :
#  - aa014 Chaotic Forces (pack agatha_harkness) : MEME structure a la ligne
#    pres — `WhenThisObligationGiveToYou`, puis
#    `YouMayFlipToYourAlterEgoForm`, puis un `ChooseAbilities` a deux puces
#    dont la PREMIERE retire l'obligation de la partie et la SECONDE la
#    defausse. C'est le squelette d'an010 Banished from Asgard (recette §1).
#  - la defausse de cartes en jeu comme cout d'une puce : `Faces.DiscardAll`
#    sur une selection faite par le joueur.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : « remove **Mutation Degeneration**
# from the game » nomme une carte QUI N'EXISTE PAS dans le pack, et rien ne la
# met en jeu. Decision : c'est l'obligation ELLE-MEME, exactement comme aa014
# dit « remove Chaotic Forces from the game » en se nommant. L'auteur a
# visiblement copie ce gabarit sans renommer. Consigne au §6 du journal de
# portage, point 1, pour l'auteur.
#
# ⚠ L'ASYMETRIE DES DEUX PUCES EST LE SEL DE LA CARTE, et c'est ce qui rend
# l'arbitrage ci-dessus coherent : la premiere la RETIRE DE LA PARTIE (elle ne
# reviendra jamais), la seconde la DEFAUSSE (elle repassera dans le deck de
# rencontre). Payer deux cartes en jeu s'en debarrasse pour de bon ; encaisser
# 2 degats ne fait que la repousser.
#
# ⚠ « upgrade/**support** cards **in play** » : les deux types, et seulement
# ce que le joueur controle — on ne defausse pas l'equipement des autres pour
# regler sa propre obligation.
#
# ⚠ La premiere puce n'est proposee QUE si le joueur a vraiment 2 cartes a
# defausser (meme prudence que la condition d'aa014) : sans ce garde-fou, le
# joueur pourrait choisir une branche qu'il ne peut pas payer et se retrouver
# avec une obligation ni retiree ni defaussee.

def GetAbilities() -> Sequence['Ability']:

    def unfinished_projects(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        if player is None:
            return

        YouMayFlipToYourAlterEgoForm(player, effect)

        def cartes_defaussables() -> List['CardFace']:
            return [f for f in player.GetControlCards()
                    if (Upgrade.IsType(f) or Support.IsType(f))]

        def payer_avec_deux_cartes(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            choisies = player.AskChooseFaces(cartes_defaussables(), (2, 2), effect)
            if choisies:
                Faces.DiscardAll(choisies, effect)
            Faces.RemoveAllFromGame([this], effect)

        def encaisser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            identite = player.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)
                this.DealDamage([identite], 2, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard 2 upgrade/support cards in play → remove this "
                "obligation from the game",
                payer_avec_deux_cartes,
                condition=len(cartes_defaussables()) >= 2,
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity and take 2 damage. Discard this "
                "obligation",
                encaisser,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            unfinished_projects
        ),
    ]
