from . import *

# Rewrite History — TRAITRISE. Boost 3, Peril (natif).
# When Revealed : Choose : • Discard your hand, shuffle your discard pile into your deck, draw up to your hand size, and ready your identity. Search the
# encounter deck and discard pile for a BARGAIN attachment. Attach it to your identity. • Mephisto schemes against you. Give him 2 additional boost cards
# for this activation.
#
# Cartes de reference : mp023 (meme structure : `ChercherEtAttacherUnPacte`, choix), `Faces.DiscardAll`, `Faces.ShuffleAllTo(.., joueur.player_deck, ..)`,
# `DrawUp("Max")`, `DoSchemes(.., operation=..)` + `GiveAdditionalBoostCardForThisActivation(2)`.
# ⚠ Mots-pieges : « Discard your HAND » puis « shuffle your DISCARD PILE (main defaussee comprise) into your deck » : l'ordre compte, la main defaussee
# retourne dans le deck ; « draw UP TO your hand size » ; « Mephisto SCHEMES against you » : manigance meme en forme heros ; « 2 ADDITIONAL boost
# cards » : en plus de la carte normale.


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def reecrit(targets: Any) -> None:
            Faces.DiscardAll(list(joueur.hand_cards.GetAll()), effect)
            defausse = list(joueur.discard_pile.GetAll())
            if defausse:
                Faces.ShuffleAllTo(defausse, joueur.player_deck, effect)
            joueur.DrawUp("Max", effect)
            Faces.ReadyAll([joueur.GetIdentity()], effect)
            ChercherEtAttacherUnPacte(effect, joueur)

        def manigance(targets: Any) -> None:
            vilain = Worlds.FindVillainByGameArea(joueur.GetIdentity().card.game_area)
            if vilain is None:
                return
            vilain.CastTo(Villain).DoSchemes(joueur, effect, property=SchemeProperty(against_player=joueur),
                                             operation=lambda would: would.GiveAdditionalBoostCardForThisActivation(2, effect))

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard your hand, shuffle your discard pile into your deck, draw up to your hand size, ready your identity and attach a BARGAIN attachment", reecrit),
            AbilityFactory.ForChoiceAbility("Mephisto schemes against you", manigance),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
