from . import *

# * Teen Abomination (Jammy)
#
# Compteurs "rage" entree en jeu : `ThisEnterPlayWithCounters`. Bonus continu
# +1 ATK par compteur : modele Wonder Man lui-meme (wonder_man/wonder_man/
# 58001a.py, "+1 ATK per card tucked") -- `ThisGainKeyword(fn_qui_compte,
# attack=1, change_on_event=OnEvent.Counter("This", 'rage'))`. Retrait d'un
# compteur apres une attaque de base : meme fenetre que Wonder Man (`After...
# makes a basic attack`) -> `AfterUnitUseBasicPower(powers=['ATK'])`.

def GetAbilities() -> Sequence['Ability']:

    def rage_count(effect: 'Effect', ui: List['CardFace']) -> int:
        return effect.this.CastTo(Ally).GetCounters('rage')

    def after_basic_attack(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Faces.RemoveCountersOn([this], 1, 'rage', effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(4, 'rage'),
        AbilityFactory.ThisGainKeyword(
            rage_count,
            attack=1,
            change_on_event=OnEvent.Counter("This", 'rage'),
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            'This',
            after_basic_attack,
            powers=['ATK'],
        ),
    ]
