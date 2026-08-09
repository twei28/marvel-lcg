from . import *

# * Scarlet Spider: Kaine — custom « Kajislav », carte d'aspect PROTECTION
# Hero Response: After Scarlet Spider enters play, ready your hero.

def GetAbilities() -> Sequence['Ability']:

    def scarlet_spider(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            "This",
            scarlet_spider
        ).SetTarget("YourHero"),
    ]
