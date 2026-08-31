from . import *

# One Too Many Voices — obligation. Boost 2. GiveTo: Wade Wilson.
# Give to the Wade Wilson player.
# You must flip to alter-ego form. Choose:
#  • Exhaust Wade Wilson -> remove One Too Many Voices from the game.
#  • Discard Klyntar Suit. If Klyntar Suit was not discarded this way, this
#    card gains surge. Discard this obligation.
#
# Carte de reference : 48026 Crisis of Faith (pack ncrawler) — meme squelette
# exact (`WhenThisObligationGiveToYou`, changement de forme, puis
# `player.ChooseAbilities` avec une `ForChoiceAbility` par puce, la premiere
# conditionnee a la forme alter-ego et payee par `CostFunc.Exhaust`).
# 16053 Crisis on Halfworld porte le meme patron.
#
# ⚠ DIFFERENCE AVEC LES DEUX MODELES, ET C'EST LE PIEGE DE CETTE CARTE :
# 48026 et 16053 disent « You MAY flip to alter-ego form » et passent donc par
# `YouMayFlipToYourAlterEgoForm`. Celle-ci dit « You MUST flip » : le
# changement de forme est FORCE, sans choix, d'ou l'appel direct a
# `ChangeToForm(AlterEgo, effect)`. Utiliser le helper « May » ici laisserait
# au joueur une echappatoire que la carte ne lui donne pas.
#
# ⚠ Le surge n'est PAS conditionne au choix de la puce, mais au fait qu'aucune
# Klyntar Suit n'ait ete defaussee (« If Klyntar Suit was not discarded THIS
# WAY ») : un joueur qui choisit la seconde puce sans controler la Suit
# declenche le surge.

def GetAbilities() -> Sequence['Ability']:

    def one_too_many_voices(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        if player is None:
            return

        # « You MUST flip to alter-ego form » : force, jamais propose.
        if player.IsHero():
            player.GetIdentity().ChangeToForm(AlterEgo, effect)

        def defausser_la_suit(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            suits = [f for f in player.GetControlCards()
                     if f.paper.name == KLYNTAR_SUIT_NAME]
            if suits:
                Faces.DiscardAll(suits, effect)
            else:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Wade Wilson → remove One Too Many Voices from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard Klyntar Suit. If it was not discarded this way, this card gains surge. Discard this obligation",
                defausser_la_suit,
            ),
            # Filet : la seconde puce est toujours ouverte, donc cette branche
            # ne devrait jamais servir. Elle resout a l'identique plutot que de
            # laisser l'obligation collee en jeu si le moteur la prend.
            AbilityFactory.Otherwise(defausser_la_suit),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            one_too_many_voices
        ),
    ]
