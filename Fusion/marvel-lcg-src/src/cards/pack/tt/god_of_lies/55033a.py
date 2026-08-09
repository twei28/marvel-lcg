from . import *
def GetAbilities() -> Sequence['Ability']:
    def mischief_and_mayhem_before(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        avatars = GetSetAsideAvatars(effect)
        if avatars:
            villain = Rand.RandomChoice(avatars, effect)
            villain.Reveal(None, effect)
            Faces.MoveAllTo(GetSetAsideAvatars(effect), Worlds.GetScenario(effect).villain_deck, effect)
        for face in Worlds.GetSetAsideAreaCards(effect):
            if (face.paper.name == 'Loki, God of Lies'):
                face.Reveal(None, effect)
                break
    def mischief_and_mayhem(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)
        for name in ('Domineering Force', 'Feigned Retreat', 'Mounting Resistance', 'Unified Front'):
            SetupCards.PutIntoPlay(effect, name=name, card_type=Environment)
        if Worlds.IsExpert(effect):
            avatar = FindAvatarOfLoki(effect)
            if avatar:
                for face in Worlds.GetSetAsideAreaCards(effect):
                    if (face.paper.name == 'Intense Focus'):
                        face.CastTo(Attachment).AttachTo2(avatar, effect)
                        break
        first_player = Worlds.GetFirstPlayer(effect)
        scheme = Worlds.MainSchemesDeck(effect).Get()
        if scheme:
            scheme[0].Reveal(first_player, effect)
    return [AbilityFactory.WhenCardSetupBeforePutSetupCards(mischief_and_mayhem_before),
            AbilityFactory.WhenCardSetup('This', mischief_and_mayhem)]
