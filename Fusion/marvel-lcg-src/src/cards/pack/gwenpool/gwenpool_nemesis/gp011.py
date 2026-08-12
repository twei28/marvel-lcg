from . import *

# Rules of the Universe — custom « ekAugust » (side scheme némésis de Gwenpool)
# Permanent (desc). Hazard 1 (desc), perdu tant qu'il n'y a pas de menace ici.
# Forced Interrupt: When you resolve an ability on a Gwenpool card, replace
# "____" with the phrase from the speech bubble on Evil Gwenpool.
#   (le remplacement forcé est câblé dans ResolveBlank, set gwenpool)

def GetAbilities() -> Sequence['Ability']:

    def sans_menace(effect: 'Effect', ui: 'List[CardFace]') -> int:
        this = effect.this.CastTo(EncounterSideScheme)
        return 1 if this.threat == 0 else 0

    return [
        # Retire l'icône hazard imprimée tant que le scheme n'a pas de menace.
        # CORRECTIF : sans change_on_event, la condition n'etait evaluee qu'a
        # l'entree en jeu. La manigance etant Permanente, l'icone hazard restait
        # figee meme quand la menace revenait a zero.
        AbilityFactory.ThisGainKeyword(
            sans_menace,
            hazard=-1,
            change_on_event=OnEvent.Threat("This"),
        ),
    ]
