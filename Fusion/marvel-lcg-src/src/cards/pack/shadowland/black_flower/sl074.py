from . import *

# * Tongue of the Beast — SBIRE. DEMON. HAND. ATQ 2 / MNG 1 / PV 1, Boost ★.
# When Defeated : The defeating player places 2 corruption counters on their Creeping Corruption.
# [star] Boost : Choose: Either place 1 corruption counter on your Creeping Corruption, or this card gains [boost][boost][boost].
#
# Cartes de reference : fne/purple_man/60104 (`WhenUnitBeDefeated(WhenDefeated, "This", op)` + joueur vainqueur), aoa/clan_akkaba/45162 (boost « Choose: either ... or this card gains [boost]x3 »),
#  aoa/genosha/45134 (`message.GainBoostIcon(3, effect)`).
# ⚠ Mots-pieges : « the defeating player » (pas le premier joueur ; a defaut le joueur engage) ; DEUX compteurs d'un coup : peuvent passer de 4 a 6 sur la Creeping Corruption, qui
#  retire alors TOUS ses compteurs ; « this card gains [boost][boost][boost] » = 3 icones POUR CETTE ACTIVATION (carte revelee en boost), pas de mot-cle permanent ; sans
#  Creeping Corruption la 1re branche n'est pas choisissable.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = getattr(message, 'defeating_player', None) or effect.this.CastTo(Minion).GetEngagedPlayer()
        if joueur is not None:
            PoserCorruption(effect, joueur, 2)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            BrancheCorruption(effect, joueur, 1),
            AbilityFactory.ForChoiceAbility("This card gains [boost][boost][boost]", lambda cibles: message.GainBoostIcon(3, effect)),
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
