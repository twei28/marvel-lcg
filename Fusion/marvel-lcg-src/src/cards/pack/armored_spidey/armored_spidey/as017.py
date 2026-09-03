from . import *

# Defensive Briefing — evenement d'aspect PROTECTION, x1. TACTIC. Cout X,
# ressource [mental].
# Hero Action: Choose up to X heroes. Each chosen hero gets +3 DEF until the
#   end of the round.
#
# Cartes de reference :
#  - **`14006`** Speed Cyclone : MEME MONTAGE pour un cout X qui borne le
#    NOMBRE de cibles — `SetTarget(..., range=(1, "All"))` a l'annonce, puis
#    `effect.targets[:effect.GetCostX()]` a la resolution. Le moteur n'a pas
#    de portee dynamique, la troncature est la forme retenue.
#  - `ho004` / `im003` pour `effect.GetCostX()`.
#  - **`12016`** / `ab003` / `50040` pour
#    `face.GainUntilRoundEnd(effect, defense=3)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Choose up to X **heroes** » : les faces HEROS, pas les identites ni les
#    allies. Un joueur en forme civile n'est pas une cible legale, et c'est
#    voulu : un alter-ego n'a pas de DEF.
#  - « **each chosen** hero » : le bonus va a toutes les cibles retenues, y
#    compris celles des AUTRES joueurs. Aucune restriction « you control ».
#  - « until the end of **the round** » : `GainUntilRoundEnd`, pas
#    `GainUntilPhaseEnd` ni `TemporaryGain` sur l'attaque en cours.
#  - « X » : dans les cas de test, `surpayer: True` est OBLIGATOIRE, sinon
#    X vaut 0 et la carte ne fait rien (piege deja paye sur ho004).
#  - « **Hero Action** » sans libelle : ce n'est ni une attaque ni une menee.
#    Aucun `SetLabel`.


def GetAbilities() -> Sequence['Ability']:

    def defensive_briefing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        combien = effect.GetCostX()
        for heros in list(effect.targets)[:combien]:
            heros.GainUntilRoundEnd(effect, defense=3)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            defensive_briefing,
        ).SetPlay()
        .SetTarget(Hero, range=(1, "All")),
    ]
