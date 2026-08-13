from . import *

# * Morph

def GetAbilities() -> Sequence['Ability']:

    # « quand la boite de texte de Morph serait traitee comme vide » : le
    # moteur ne publie pas de fenetre pour cela. APPROXIMATION ECRITE — le
    # bonus est donne quand une carte lui est attachee avec `treat_as_blank`,
    # ce qui est la seule facon de rendre sa boite vide dans ce jeu (dt113
    # Tabula Rasa, dt139 Flummoxed).
    def boite_vide(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        return 1 if this.GetKeyword('TreatAsBlank') else 0

    return [
        AbilityFactory.ThisGainKeyword(
            boite_vide,
            attack=2,
            thwart=2,
            change_on_event=OnEvent.CardInPlay(Upgrade),
        ),
    ]
