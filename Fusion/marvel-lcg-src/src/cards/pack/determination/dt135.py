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
        # ECART ASSUME, ET NON SIMULE. « Tarantula gagne une icone [wild] par
        # jeton de degat sur elle » : `have_res_icon` n'existe que pour une
        # carte qui accorde une icone a UNE AUTRE (GiveKeywordToAttached), pas
        # pour une carte qui se l'accorde a elle-meme, et rien ne donne une
        # icone PAR JETON. La ligne n'est donc pas implementee plutot que rendue
        # de travers : le reste de la carte fonctionne.
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
