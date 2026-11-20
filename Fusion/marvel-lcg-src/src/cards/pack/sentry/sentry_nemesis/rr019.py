from . import *

# Equilibrium Intent : TRAHISON, boost ★ + 1 icone. Set « Sentry Nemesis » (x2).
# When Revealed: If the Void is in play, he activates. If the Void is not in play, place 1 balance counter on Duality Aspect, then this card gains surge.
# ★ Boost: Discard 1 identity-specific card you control at random. If you cannot, discard an identity-specific card from your hand.
#
# CARTES DE REFERENCE
#  - « X activates » : `ca016` (`ennemi.DoActivate(joueur, effect)`) ; surge : `this.GainSurge(1, effect)` ; `ca018` pour le Boost (`WhenCardBecomeBoost("This", ..)`).
#  - compteur : helper `PoserEquilibre`.
#
# TEXTE CONTRE CODE
#  « If the Void is in play, he activates » : il s'active (contre le joueur qui revele). « If the Void is NOT in play » : 1 compteur sur Duality Aspect PUIS surge. Boost : « identity-specific »
#  = carte de classe Hero (`card_classes` : `IdentitySpecific`) ; « you control » = en jeu sous le controle du joueur, tirage AU HASARD ; faute de carte en jeu, une carte de la MAIN (au choix).
#  Chiffres : boost 1.


def GetAbilities() -> Sequence['Ability']:

    def equilibrium_intent(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        void = VoidEnJeu(effect)
        if void is not None and joueur is not None:
            void.CastTo(Enemy).DoActivate(joueur, effect)
        else:
            PoserEquilibre(effect, 1)
            this.GainSurge(1, effect)

    def specifique(face: 'CardFace') -> bool:
        return "IdentitySpecific" in getattr(face, "card_classes", []) and not (Hero.IsType(face) or AlterEgo.IsType(face))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        joueur = effect.world.GetCurrentPlayer()
        if joueur is None:
            return
        en_jeu = [f for f in joueur.GetControlCards() if f.IsInPlay() and specifique(f)]
        if en_jeu:
            Faces.DiscardAll([effect.world.random.choice(en_jeu)] if hasattr(effect.world, "random") else [en_jeu[0]], effect)
            return
        en_main = [f for f in joueur.hand.Get() if specifique(f)]
        if en_main:
            choisie = joueur.AskChooseFace(en_main, effect, not_move=True)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            equilibrium_intent,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
