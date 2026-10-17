from . import *

# Shadow Summon — EVENEMENT 1 [energy], Ninjutsu (TMNT Shinobi, Inkwire). TACTIC.
# Action: Discard cards from the top of your deck until you discard a NINJA ally and put it into play. If that ally is
# still in play at the end of the phase, add it to your hand.
# « We will need to hide our numbers. » —Leonardo
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : aucun (pas de Cloak sur le texte imprime).
#
# Cartes de reference :
#  - `22009` Combat Ready : « Discard cards from the top of your deck until you discard a <trait> <type>. Put that ... into
#    play » = `initiator.DiscardDeckUntil(effect, trait=..., card_type=...)` + `face.PutIntoPlay(initiator, effect)` ;
#  - `ul035` "Turtle Power!" : « If that ally is still in play at the end of the phase, add it to your hand » =
#    `RunAt.TheEndOfThePhase(effect, fn)` + `initiator.GainCard(face, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard cards from the top of YOUR deck UNTIL you discard a NINJA ALLY » : on defausse jusqu'a l'allie NINJA inclus
#    (les autres cartes defaussees restent defaussees, meme sans allie NINJA : tout le deck y passe) ; « and put it INTO
#    PLAY » : l'allie defausse revient en jeu (gratuit, sans payer son cout).
#  ⚠ « If that ally is STILL IN PLAY at the END OF THE PHASE, add it to YOUR HAND » : controle a la fin de la PHASE (pas du
#    tour ni du round), la carte revient dans la main de son controleur (le joueur) ; un allie parti avant (vaincu,
#    defausse) reste ou il est.
#  ⚠ « Action » (les deux formes).


def GetAbilities() -> Sequence['Ability']:

    def shadow_summon(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        initiator = effect.GetInitiator()
        face = initiator.DiscardDeckUntil(effect, trait="NINJA", card_type=Ally)
        if face:
            face.PutIntoPlay(initiator, effect)

            def add_it_to_hand() -> None:
                if face.card.area.flags.is_in_play:
                    initiator.GainCard(face, effect)

            RunAt.TheEndOfThePhase(effect, add_it_to_hand)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            shadow_summon,
        ).SetPlay().SetLabel(),
    ]
