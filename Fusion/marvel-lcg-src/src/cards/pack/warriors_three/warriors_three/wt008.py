from . import *


def fandral_est_actif(effect: 'Effect', message=None) -> bool:
    hote = effect.this.bind_face
    return hote is not None and Hero.IsType(hote) and hote.IsName("Fandral")


def GetAbilities() -> Sequence['Ability']:
    def menace(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        effect.this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Fandral"), thwart=1),
        # « while he is your ACTIVE hero ignore all crisis icons in play » : toute icone Crise EN JEU est ignoree (RR « Crisis Icon » :
        # equivalente a « player cards cannot remove threat from the main scheme »), donc pour TOUTE source (allies, evenements, autres
        # joueurs), tant que la carte est attachee a la face HEROS de Fandral.
        AbilityFactory.UnitIgnoreKeywordIcons(CardFinder(), crisis=True, conditions=[fandral_est_actif]),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            menace,
            conditions=[lambda effect, message: message.trigger.IsName("Fandral")],
        ).SetTarget(Scheme2),
    ]
