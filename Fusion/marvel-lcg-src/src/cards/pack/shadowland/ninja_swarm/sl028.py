from . import *

# * Black Mountain — SBIRE. BRUTE. HAND. NINJA. ATQ 2 / MNG 2 / PV 5, Boost ★.
# Guard.
# While Black Mountain is engaged with you, each other NINJA minion engaged with you cannot be attacked.
# [star] Boost : If an ally is defending against this attack, reveal this minion.
#
# Cartes de reference : core/hydra_mercenary/01101 (Guard natif dans `desc`), wave_nemesis/62030 Venomous Whispers (`UnitCannotAttackTarget(... cannot_attack=CardFinder(trait=...))`),
#  sk201 (condition « engage avec ce joueur »), shadows_in_the_night/sl006 (boost « un allie defend » -> `RevealThisCard`).
# ⚠ Mots-pieges : « each OTHER NINJA minion » (pas Black Mountain lui-meme : il reste attaquable, c'est ainsi qu'on leve le Guard) ; « engaged WITH YOU » = le joueur avec qui
#  Black Mountain est engage (un sbire NINJA engage avec un AUTRE joueur reste attaquable) ; « cannot be attacked » = par personne (heros, allie, evenement) ;
#  boost : l'ALLIE qui defend, pas le heros. Guard est lu dans `desc`, aucun script.


def GetAbilities() -> Sequence['Ability']:

    def autre_ninja_du_meme_joueur(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        cible = message.being_attack
        return joueur is not None and cible is not this and getattr(cible, 'engaged_player', None) == joueur

    return [
        AbilityFactory.UnitCannotBeAttacked(CardFinder2("NINJA", Minion), conditions=[autre_ninja_du_meme_joueur]),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard, during_attack=True, conditions=[UnAllieDefend]),
    ]
