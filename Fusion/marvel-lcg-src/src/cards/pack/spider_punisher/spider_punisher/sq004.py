from . import *


def GetAbilities() -> Sequence['Ability']:
    def web_snatch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        Faces.GiveStatus(effect.targets, "Stunned", effect)

        def chercher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                include_discard_pile=True,
                card_type=Upgrade,
            )
            if face:
                joueur.GainCard(face, effect)

        def defausser(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(list(cibles), effect)

        mechant = Worlds.FindVillain(effect)
        attachements = [f for f in (mechant.GetInventoryDeck().Get() if mechant else []) if Attachment.IsType(f)]
        options = [AbilityFactory.ForChoiceAbility(
            "Search your deck and discard pile for an upgrade and add it to your hand", chercher)]
        if attachements:
            options.append(AbilityFactory.ForChoiceAbility(
                "Discard an attachment from the villain's play area", defausser,
            ).SetTarget(Attachment, check_fn=lambda e, f: f in attachements))
        joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            web_snatch,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy, canbe_stunned=True),
    ]
