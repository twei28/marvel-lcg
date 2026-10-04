from . import *

# * Tide Wall — evenement signature, x2 (11-12/15). DEFENSE. SUPERPOWER.
# Cout 0.
# Hero Interrupt (defense): When you would take any damage, prevent up to 3
# of that damage. For each point of damage prevented this way, place the top
# card of your deck faceup in the Rising Tide area.
#
# Modele du declencheur et de la prevention : 01003 Backflip
# (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", ...).SetPlay().
# SetLabel('defense')`, `message.PreventDamage(...)`) -- sauf que Backflip
# previent « All » et rend un bool ; ici on previent UN NOMBRE (« up to 3 »)
# et `PreventDamage(value, effect) -> int` rend le nombre REELLEMENT prevenu
# (sender_damage.py:836), qui peut etre < 3 si l'attaque infligeait moins.
# « any damage » (pas seulement d'attaque) -> `is_from_attack` NON precise
# (defaut None), contrairement a Backflip qui le force a `True`.
# La pose en Rising Tide reutilise `PlacerFaceVisibleDansRisingTide`, une
# fois par point REELLEMENT prevenu -- la meme carte de dessus ne peut pas
# etre reposee deux fois, on relit `GetTop()` a chaque tour de boucle.

def GetAbilities() -> Sequence['Ability']:

    def tide_wall(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return

        prevenus = message.PreventDamage(3, effect)
        for _ in range(prevenus):
            dessus = initiator.player_deck.GetTop()
            if dessus is None:
                break
            PlacerFaceVisibleDansRisingTide(dessus, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            tide_wall,
        ).SetPlay().SetLabel('defense'),
    ]
