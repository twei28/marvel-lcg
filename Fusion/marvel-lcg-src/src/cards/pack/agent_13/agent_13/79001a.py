from . import *

# Agent 13 (face heros) — custom « Rainy »
# Hand-to-Hand Specialist — Response: After Agent 13 uses a basic hero power,
# ready Agent 13 and make a basic attack against an enemy. (Limit once per
# round.)
#
# Modele pour le declencheur : Black Panther (51001a, meme structure
# « apres que TA propre identite utilise un pouvoir de base -> reponse » sur
# la face heros elle-meme), via `AbilityFactory.AfterUnitUseBasicPower`
# (src/game/ability/factory/friend.py:373). `powers="Hero"` est le raccourci
# du moteur pour `["ATK", "THW", "DEF"]` -- exactement « a basic HERO power »
# du texte imprime, les trois pouvoirs de base du heros. `which_unit="You"`
# restreint a ta propre identite (`Condition.GetYouRule` -> "YourIdentity"),
# ce qu'aucun allie ne peut jamais satisfaire : conforme au brief.
#
# Piege signale par le brief : l'attaque de base declenchee ne doit pas
# redeclencher la capacite en boucle. `this.BasicAttack(...)` cree elle-meme
# une attaque marquee `AttackProperty(is_basic_power=True)` par defaut
# (src/game/card/face/attribute/can_attack.py:503), ce qui renvoie
# `WhenUnitUseBasicPower` puis `AfterUnitUseBasicPower` -- exactement le
# message que CETTE capacite ecoute. Verifie en lisant
# `src/game/effect/effect_invoke.py:159` : `Effect.SetHasSpellInPhase()`
# (qui pose le compteur « une fois par round ») s'execute AVANT
# `EffectInvoker.InvokeOperation`, donc l'attaque imbriquee retrouve la
# limite deja posee et ne redeclenche rien. `.LimitOncePerRound()` est donc
# a la fois le texte imprime et le garde-fou structurel -- meme montage que
# 79001b (`Super Spy`, deja ecrite).
#
# Modele pour se redresser soi-meme apres avoir agi : She-Hulk, One-Two Punch
# (01024), `Faces.ReadyAll([this], effect)`.

def GetAbilities() -> Sequence['Ability']:

    def agent_13(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)

        Faces.ReadyAll([this], effect)
        this.BasicAttack(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            agent_13,
            powers="Hero",
        ).SetName("Hand-to-Hand Specialist")
        .SetTarget(Enemy)
        .LimitOncePerRound(),
    ]
