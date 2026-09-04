from game.card.face import *
from game.ability import *
from game.message import *
from game.player import *

def GetForDelayAbility(effect: 'Effect') -> 'Ability|None':
    """L'objet Ability sur lequel une limite « once per ... » doit se compter.

    ⚠ CORRECTIF DU 03/09/2026. Ces deux lignes existaient, en commentaire, et
    leur absence rendait `LimitOncePerRound()` (et ses soeurs) SILENCIEUSEMENT
    INERTE sur toute capacite construite au-dessus d'une `DelayAbility` — en
    pratique toute la famille `AfterUnitDefeatedUnit`. Signale en jeu sur le
    pack maison `angela` : « elle peut faire ses trucs plusieurs fois par
    round ». Reproduit, puis sonde a l'appui.

    Le montage : `AbilityFactory.AfterUnitDefeatedUnit` ne rend PAS la Reponse
    demandee. Elle rend une enveloppe `DelayAbility` branchee sur
    `WhenFaceWouldDealDamage` (factory/defeated.py:330) qui, a chaque defaite,
    FABRIQUE une capacite interne portant la vraie Reponse et l'enregistre en
    temporaire. D'ou deux objets :
      - l'ENVELOPPE, celle que la carte tient et sur laquelle
        `.LimitOncePerRound()` a ete pose. Tous ses drapeaux de type sont a
        False, donc `Effect.SetHasSpellInPhase` (effect.py:161) ne l'inscrit
        JAMAIS dans `world.stat.once_per_round_effects` ;
      - l'INTERNE, bien inscrite, mais RECREEE A NEUF a chaque defaite.
    La condition interrogeait l'enveloppe, la liste ne contenait que des
    internes : `ability not in [...]` etait vrai a tous les coups.

    `CopyFromDelayEffect` (ability.py:1139) pose justement
    `effect.delay_ability = self` sur l'effet de l'enveloppe : c'est le pont
    prevu. On le suit ici. `delay_ability` vaut None avant la premiere
    resolution (effect.py:34), donc le PREMIER declenchement reste autorise.

    Le commentaire d'origine lisait `effect.ability.type.is_delay_ability` ;
    l'attribut reel est `flags.is_delay_ability` (ability_type.py:438, et tous
    les autres appels du moteur). C'est probablement ce qui l'a fait desactiver.
    """
    if effect.ability.flags.is_delay_ability:
        return effect.delay_ability
    return effect.ability

class ConditionOncePer:

    @staticmethod
    def LimitOncePerRound(effect: 'Effect', message: 'Message2') -> bool:
        world = effect.world
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerRound(ability)

    @staticmethod
    def LimitOncePerRoundPerPlayer(effect: 'Effect', message: 'Message2') -> bool:
        from game.message.sender.sender import TriggerNonePlayerMessage
        assert isinstance(message, TriggerNonePlayerMessage)
        world = effect.world
        player = message.GetToPlayer()
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerRoundPerPlayer(ability, player)

    @staticmethod
    def LimitOncePerPhasePerPlayer(effect: 'Effect', message: 'Message2') -> bool:
        from game.message.sender.sender import TriggerNonePlayerMessage
        assert isinstance(message, TriggerNonePlayerMessage)
        world = effect.world
        player = message.GetToPlayer()
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerPhasePerPlayer(ability, player)

    @staticmethod
    def LimitOncePerPhase(effect: 'Effect', message: 'Message2') -> bool:
        world = effect.world
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerPhase(ability)

    @staticmethod
    def LimitOncePerEvent(effect: 'Effect', message: 'Message2') -> bool:
        ability = GetForDelayAbility(effect)
        return ability not in [x.ability for x in message.once_per_event_effects]

    @staticmethod
    def LimitOnceCardNamePerEvent(effect: 'Effect', message: 'Message2') -> bool:
        ability = GetForDelayAbility(effect)
        if ability == None:
            return True
        return ability.paper not in [x.ability.paper for x in message.once_per_event_effects]

