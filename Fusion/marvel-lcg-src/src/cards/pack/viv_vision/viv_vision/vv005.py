from . import *

# Solar Beam — evenement signature, x4 (n/15 = 6, 7, 8 et 9). La carte la plus
# nombreuse du kit. ATTACK. SUPERPOWER. THWART.
# Cout 2, ressource [energy], Requirement ([energy]).
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains ranged.
# Hero Action (thwart): Remove 4 threat from a scheme.
#
# Cartes de reference :
#  - 26008 Solar Beam, la carte signature du VISION OFFICIEL (homonyme exact,
#    voir le __init__ du pack) : meme structure a DEUX `WhenInYourPlayTurn`
#    `.SetPlay()`, l'une `.SetLabel('attack').SetTarget(Enemy)`, l'autre
#    `.SetLabel('thwart').SetTarget(Scheme2)`. Ecarts : 26008 conditionne
#    chaque branche a une forme de masse (Dense / Intangible) que Viv n'a pas,
#    et ses valeurs sont 7 / 5 pour un cout de 3 ;
#  - ag003 Burst Fire (meme auteur, Rainy) et 41030 Psi-Bow Attack pour le
#    ranged ponctuel : `property=AttackProperty(ranged=True)` passe a
#    `DealDamage`.
#
# ⚠ DEUX CAPACITES `Play` SUR UN MEME EVENEMENT : `game/card/factory.py`
# refuse par defaut (assert `play_count == 1`) et la partie plante AU SETUP,
# invisible pour test_cards.py. `vv005` est donc declaree dans la liste
# blanche de ce fichier, juste apres son homonyme officiel 26008 qui y figure
# deja pour la meme raison.
#
# ⚠ AUCUN script pour le `Requirement` : `desc.Requirement` = "Y", base
# automatique (voir mots-cles/requirement.md).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « THIS ATTACK gains ranged » porte sur la branche ATTAQUE seule. La
#    branche menee n'a aucun mot-cle. `AttackProperty(ranged=True)` n'est donc
#    passe qu'a `DealDamage`.
#  - Le sens de `ranged` s'inverse selon le message vise : sur une attaque que
#    la carte DECLENCHE, c'est `AttackProperty(ranged=True)`, jamais
#    `message.GainRanged` qui donnerait ranged a l'ENNEMI (piege documente sur
#    ag005, voir mots-cles/ranged.md).
#  - « Deal 5 damage TO AN ENEMY » : une seule cible, `SetTarget(Enemy)`.
#    Ranged n'annule que la Riposte, ni la Robustesse ni le blocage par un
#    allie.
#  - « Remove 4 threat FROM A SCHEME » : une seule manigance,
#    `SetTarget(Scheme2)`. Aucune mention de crisis : ce retrait de menace
#    n'est PAS une menee, donc `breakthrough` ne s'y applique pas et le crisis
#    du complot principal le bloque normalement.
#  - Les deux branches sont des `Hero Action` : sous-type dedie, pas `Action`
#    nu (piege « Hero Response/Hero Action » de l'etape 5).


def GetAbilities() -> Sequence['Ability']:

    def solar_beam_attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 5, effect, property=AttackProperty(ranged=True))

    def solar_beam_thwart(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            solar_beam_attack,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            solar_beam_thwart,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
