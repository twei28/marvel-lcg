from . import *

# * Rupert Giles — ALLIE (WATCHER), cout 3, [mental]. THW 2*, ATK 1*, PV 3. Unique.
# Response: After Rupert Giles enters play, remove 2 threat from a scheme (3 threat instead if Watcher's Guidance is in play).
#
# CARTES DE REFERENCE
#  - `hd001a` / `01083` Mockingbird : `AfterCardEnterPlay(Response, "This", op)` pour « after X enters play ».
#  - `25008` Flight of the Valkyrior : `SetTarget(Scheme2)` + `this.RemoveThreatFromSchemes(effect.targets, n, effect)`.
#
# TEXTE CONTRE CODE
#  « a scheme » -> `Scheme2` : le complot principal OU une manigance annexe, au choix du joueur.
#  « 3 threat instead if Watcher's Guidance is in play » -> la valeur est choisie A LA RESOLUTION, par le nom, sur toute carte en
#    jeu (celle de n'importe quel joueur). Watcher's Guidance n'est pas fournie par le Drive : sans elle, c'est toujours 2.
#  Chiffres : 2 menaces, 3 menaces avec Watcher's Guidance. Cout 3, THW 2*, ATK 1*, PV 3 (cards.json).


def GetAbilities() -> Sequence['Ability']:

    def giles_entre_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        guidance = Worlds.FindCardOnField(effect, name=NOM_WATCHERS_GUIDANCE)
        this.RemoveThreatFromSchemes(effect.targets, 3 if guidance else 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            giles_entre_en_jeu,
        ).SetTarget(Scheme2),
    ]
