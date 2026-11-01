from . import *

# Lunar Eclipse. Traitrise SPELL. « When Revealed : Remove 1[per_hero] time counter from Beneath the Sun. If you cannot, place 1[per_hero] time
# counter on Under the Moonlight. [star] Boost : Reveal this card. »
# Cartes de reference : hf110 (`RevealThisCard` en boost), hf407a/b (compteurs `time`). ⚠ « If you cannot » : le JOUR n'est pas la face visible
# (rien a retirer) ; le retour est le nombre de compteurs reellement retires. Eternal Night ne bloque que la NUIT : ici on retire du jour.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        n = Worlds.GetPlayerNumIcon(effect)
        env = Temps(effect)
        if env is not None and env.IsName(NOM_JOUR):
            if RetirerDuTemps(effect, env, n) > 0:
                return
        if env is not None and env.IsName(NOM_NUIT):
            PoserDuTemps(effect, env, n)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
