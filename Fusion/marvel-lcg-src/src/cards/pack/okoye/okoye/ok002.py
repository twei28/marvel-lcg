from . import *

# * Aneka
# Response: After Aneka enters play, all other DORA MILAJE allies you
#   control get +1 ATK until the end of the phase.
#
# Modele exact : bp/51014.py (Manifold, `AbilityFactory.AfterCardEnterPlay`
# sur "This"). La cible n'est pas "Players" mais tous les AUTRES allies Dora
# Milaje en jeu : `Worlds.FindCardsOnField(effect, trait="DORA MILAJE",
# card_type=Ally)` filtre pour exclure "This", modele du filtre `exclude
# ="This"` deja utilise par bp/__init__.py sur la MEME famille de cartes
# (Aneka/Ayo/Okoye du pack officiel bp), ici recopie a la main puisque ce
# n'est pas une cible de `.SetTarget()` mais une liste calculee.


def GetAbilities() -> Sequence['Ability']:

    def aneka(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        autres = [f for f in Worlds.FindCardsOnField(effect, trait="DORA MILAJE", card_type=Ally) if f is not this]
        for face in autres:
            face.GainUntilPhaseEnd(effect, attack=1)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            aneka,
        ),
    ]
