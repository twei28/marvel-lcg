from . import *

# * The Aegis (amelioration, cout 1, ARMOR OLYMPUS, physique)
# Response: After you resolve your "Skyfather's Tempest" ability, place
# 1 aegis counter here.
# Hero Interrupt (defense): When you would take any amount of damage, remove
# 2 aegis counters from here → prevent 3 of that damage.
#
# Modeles : ab007 (repondre a une capacite NOMMEE ; ici le Tempest est une
# Response, pas un Special, donc `AfterPlayerResolveAbility` avec
# `ability_name`), 05017 Energy Barrier (`WhenUnitWouldTakeDamage` + coût en
# compteurs + `PreventDamage`). Le compteur `aegis` a ete ajoute a l'enum
# COUNTER (card_face.py) et a compteurs-fr.ts le 11/09/2026.
#
# « When you would take any amount of damage » : l'identite, quelle que soit
# la source (attaque, degats indirects, traitrise). Le label `defense` suit
# l'imprime « (defense) ».

def GetAbilities() -> Sequence['Ability']:

    def poser_une_egide(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 1, COMPTEUR_EGIDE, effect)

    def prevenir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.PreventDamage(3, effect)

    return [
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.Response,
            "You",
            CardFinder(name="Zeus", card_type=Hero),
            poser_une_egide,
            ability_name=TEMPEST,
        ),

        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            prevenir,
        ).SetCostFunc(CostFunc.Counter("This", 2, COMPTEUR_EGIDE))
        .SetLabel('defense'),
    ]
