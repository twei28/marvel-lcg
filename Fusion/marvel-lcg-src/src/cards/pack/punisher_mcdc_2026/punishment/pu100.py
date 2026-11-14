from . import *

# Back Against the Wall — TRAITRISE x2. Boost ★+1.
# When Revealed (Alter-Ego) : Deal damage to Punisher equal to the TARGETED villain's ATK.
# When Revealed (Hero) : Flip Target Lock to its DISTRACTED side. Punisher activates.
# ★ Boost : Give Punisher a facedown boost card (if he is activating, resolve it).
#
# Cartes de reference : `WhenThisRevealed("Alter-Ego"|"Hero", ...)` (hobgoblin... jigsaw/pu070), `Enemy.DoActivate`, `DealDamage`,
# `message.would_message`/`GiveBoostCardForThisActivation` (sender_enemy.py) pour « if he is activating, resolve it ».
# ⚠ « damage EQUAL TO the TARGETED villain's ATK » : son ATQ courant (bonus compris) ; « Punisher activates » : contre le
# joueur qui revele ; « (if he is activating, resolve it) » : si Punisher s'active, la carte donnee s'ajoute a l'activation
# en cours (`message.GiveAdditionalBoostCardForThisActivation`) ; sinon elle reste face cachee devant lui.

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        punisher = Punisher(effect)
        cible = VilainCible(effect)
        if punisher is not None and cible is not None:
            this.DealDamage([punisher], cible.attack, effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        RetournerTargetLockVersDistracted(effect)
        punisher = Punisher(effect)
        joueur = message.GetToPlayer()
        if punisher is not None and joueur is not None:
            punisher.CastTo(Enemy).DoActivate(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        punisher = Punisher(effect)
        if punisher is None:
            return
        activant = getattr(message, 'activating_enemy', None)
        if activant is not None and activant is punisher and hasattr(message, 'GiveBoostCardForThisActivation'):
            message.GiveBoostCardForThisActivation(Villain, 1, effect)
        else:
            DonnerUneCarteBoostFaceCachee(effect, punisher, 1)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
