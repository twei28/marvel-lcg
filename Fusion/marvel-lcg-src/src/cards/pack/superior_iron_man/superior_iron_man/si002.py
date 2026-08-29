from . import *

# Endo-Sym Armor
#
# Deux capacites "Spend X [couleur] resources (minimum 1)", modele Lightning
# Strike (thor/thor/06006.py) : `Cost("R")`/`Cost("Y")` = minimum 1 du
# symbole imprime, le joueur peut en depenser plus. Cible d'attaque modele
# Ionic Blast (wonder_man/wonder_man/58004.py) : `.SetTarget(Enemy)` +
# `this.DealDamage(...)`. Interruption de defense modele Human Shield
# (determination/dt006.py) pour la fenetre `WhenUnitWouldTakeDamage` +
# `message.PreventDamage(...)`, "You" (pas "This", cette carte n'est pas un
# personnage) pour la cible "quand VOUS etes cense subir des degats".
#
# CORRECTIF (bug trouve en test) : PAS de `.SetPlay()` ici. `.SetPlay()`
# marque l'ability `func_name="Play"` (ability.py:613) -- correct pour un
# Event qu'on joue depuis la main (modele Ionic Blast), FAUX pour une
# capacite activee d'un Upgrade deja en jeu en permanence. `Upgrade.
# GetAbilities()` (card_type/upgrade.py) cherche automatiquement une ability
# `func_name="Play"` pour en deduire un point d'attache par defaut
# (`AttachToFaceWhenPutIntoPlayInternal`) : avec `.SetPlay()` ici, il prenait
# le `.SetTarget(Enemy)` de l'attaque pour "l'endroit ou s'attacher", et
# plantait (`AssertionError` dans `GetBindFace`) des que la carte entrait en
# jeu -- silencieusement via le Setup (PutIntoPlay renvoyait True sans rien
# faire), bruyamment via `Puzzle.PutIntoPlay` direct. Wonder Man n'a jamais
# ce probleme : aucune de ses abilities n'utilise `.SetPlay()`.

def GetAbilities() -> Sequence['Ability']:

    def attack(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        res = effect.cost_func.Get(CostFunc.Spend).return_res
        value = res.GetColor("R")
        this.DealDamage(effect.targets, 2 + value, effect)

    def defense(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        res = effect.cost_func.Get(CostFunc.Spend).return_res
        value = res.GetColor("Y")
        message.PreventDamage(1 + value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            attack,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Spend(Cost("R")))
        .SetTarget(Enemy)
        .LimitOncePerPhase(),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            defense,
        ).SetLabel('defense')
        .SetCostFunc(CostFunc.Spend(Cost("Y")))
        .LimitOncePerPhase(),
    ]
