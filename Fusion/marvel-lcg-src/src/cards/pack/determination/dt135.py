from . import *

# * Tarantula

def GetAbilities() -> Sequence['Ability']:

    def degat_supplementaire(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage([this], 1, effect)

    def check_pas_exactement_vaincu(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        return not message.has_defeated_target

    return [
        Fragile(),
        # « une icone [wild] PAR JETON de degat sur elle » : `ThisGainKeyword`
        # accepte desormais `have_res_icon` (CORRECTIF moteur), et son
        # `check_fn` rend le NOMBRE de fois ou le gain s'applique — donc une
        # icone par jeton, exactement.
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: effect.this.CastTo(CanHealth).sustained,
            have_res_icon="G",
            change_on_event=OnEvent.Health("This"),
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            Minion,
            degat_supplementaire,
            conditions=[check_pas_exactement_vaincu],
        ),
        AbilityFactory.AfterUnitThwartScheme(
            AbilityType.ForcedResponse,
            "This",
            EncounterSideScheme,
            degat_supplementaire,
        ),
    ]
