from . import *
def GetAbilities() -> Sequence['Ability']:
    def hellcat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        this.PutIntoPlay(player, effect)
        this.effect.RegisterTemp(
            AbilityFactory.AfterPhaseEnd(AbilityType.Temp0, None, lambda e, m: Faces.DiscardAll([this], e)),
            unregister_after_exec=True,
        )
    def check_defender(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        identity = effect.GetInitiator().GetIdentity()
        return bool(identity and identity.HasTrait('DEFENDER'))
    return [
        # ⚠ PAS DE `.SetPlay()` : il baptise la capacite « Play », et `Ally`
        # n'ajoute alors plus la mise en jeu normale (card_type/ally.py). L'Action
        # devenait la mise en jeu PAYANTE (cout 4) et Hellcat etait injouable
        # sans Defender (rapport BL-Stark n66). Modele 50013 Slingshot.
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, hellcat, conditions=[check_defender])
        .CanWorkOnlyInHand(),
    ]
