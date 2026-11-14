from . import *

# * Cassandra Nova (sbire ELITE HELLFIRE PSIONIC, PV 2, ATQ 3, MNG 3, Steady, [star] Boost 0 icone). « Steady. When Revealed : Find the Cassandra's Telepathic Cloak
# attachment and put it into play. [star] Boost : Put Cassandra Nova into play engaged with you. »
# Cartes de reference : wd064 Princess Python / pt019 Mr. Hyde (`Search...` + `PutIntoPlay` + `AttachTo2(this, effect)` depuis le When Revealed d'un sbire), 01121 Weapons
# Runner (boost « put into play engaged with you » : `face.PutIntoPlay(joueur, effect)`), hf313 (meme boost).
# ⚠ « Find » (livret p.4) : le manteau peut etre dans le deck de rencontre, sa defausse OU la zone mise de cote (`ChercherLeManteau`) ; le manteau est ensuite attache A ELLE.
# Le boost met le sbire en jeu engage avec le joueur : elle est donc cherchee la ou elle se trouve (elle peut etre dans le deck Hellfire, ou ici, deja en jeu = rien).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        manteau = ChercherLeManteau(effect)
        if manteau is not None:
            manteau.PutIntoPlay(joueur, effect)
            manteau.AttachTo2(this, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        if not this.IsInPlay():
            this.PutIntoPlay(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
