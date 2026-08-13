from . import *

# * Morph

def GetAbilities() -> Sequence['Ability']:

    # « Quand la boite de texte de Morph S'APPRETE a etre traitee comme vide » :
    # la fenetre existe et porte ce nom exact — `WhenCardWouldTreatAsIfBlank`,
    # envoyee par treat_blank.py avant que la boite ne soit videe. Le premier
    # jet ne l'avait pas trouvee et se rabattait sur le mot-cle deja pose.
    def check_this(effect: 'Effect', message: 'Message.WhenCardWouldTreatAsIfBlank') -> bool:
        return effect.this == message.trigger

    def morph(effect: 'Effect', message: 'Message.WhenCardWouldTreatAsIfBlank') -> None:
        this = effect.this.CastTo(Ally)
        # « jusqu'a ce qu'il quitte le jeu » : un gain DURABLE, qui s'en va
        # avec la carte — c'est `Gain` (precedent mw023.py:25).
        this.Gain(effect, 1, attack=2, thwart=2)

    return [
        Ability(
            AbilityType.ForcedInterrupt,
            Message.WhenCardWouldTreatAsIfBlank,
            [check_this],
            morph,
            is_local=True
        ),
    ]
