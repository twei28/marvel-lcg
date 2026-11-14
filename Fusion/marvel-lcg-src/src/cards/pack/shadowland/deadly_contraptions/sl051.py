from . import *

# Caltrops — TRAITRISE. TRAP! Boost 1.
# When Revealed : Choose :
#  • Avoid — Discard a DEFENSE event from your hand.
#  • Disarm — Discard 1 identity-specific card from your hand, then deal 2 damage to an enemy.
#  • Trip — Deal 2 damage to your identity and stun it.
#
# Cartes de reference : sl050 (meme gabarit), player_action.py `DiscardRandomHandCards(rule="IdentitySpecific")` / `IsClass("IdentitySpecific")` (card_player.py), core/rhino/01101.
# ⚠ Mots-pieges : « 1 identity-specific card » : une carte du paquet de HEROS (classe IdentitySpecific), a CHOISIR dans la main (pas au hasard) ; « an ENEMY » : un sbire ou le
#  vilain, au choix ; « then » : les degats ne partent que si la carte a ete defaussee ; Avoid : evenement DEFENSE ; Trip : etourdit l'identite.


def GetAbilities() -> Sequence['Ability']:

    def specifiques(joueur: 'Player') -> List['CardFace']:
        return [f for f in joueur.hand_cards.Get() if ClassCard.IsType(f) and f.IsClass("IdentitySpecific")]

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        this = effect.this

        def evite() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, EvenementsDeLaMain(joueur, "DEFENSE"))

        def desarme() -> None:
            if DefausserUneCarteDeLaMain(effect, joueur, specifiques(joueur)) is None:
                return
            ennemi = ChoisirUneCarte(effect, joueur, Worlds.GetOnFieldEnemies(effect))
            if ennemi is not None:
                this.DealDamage([ennemi], 2, effect)

        def declenche() -> None:
            DegatsEtStatut(effect, joueur, 2, "Stunned")

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Discard a DEFENSE event from your hand", evite, faisable=bool(EvenementsDeLaMain(joueur, "DEFENSE"))),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Discard 1 identity-specific card from your hand, then deal 2 damage to an enemy", desarme,
                                   faisable=bool(specifiques(joueur))),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Deal 2 damage to your identity and stun it", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
