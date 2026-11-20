from . import *

def GetAbilities() -> Sequence['Ability']:
    def est_incline(effect: 'Effect') -> bool:
        this = getattr(effect, "this", None)
        return this is not None and this.IsExhaust()

    def ma_carte(effect: 'Effect', message: 'Message2') -> bool:
        return getattr(message, "trigger", None) is getattr(effect, "this", None)

    # Aucun OnEvent n'existe pour l'inclinaison : on le construit sur les deux messages du moteur (modele des evenements
    # `OnEvent.Status` / `OnEvent.Faceup`, `TemplateTrigger`), pour que la taille de main suive l'etat de Cr'reee.
    quand_elle_change = Condition.AddEvent(
        OnEvent.TemplateTrigger(Message.AfterCardExhausted, ma_carte),
        OnEvent.TemplateTrigger(Message.AfterCardReady, ma_carte),
    )

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            hand_size=1,
            condition=est_incline,
            change_on_event=quand_elle_change,
        ),
    ]
