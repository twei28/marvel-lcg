from . import *

# Tactical Help (manigance annexe de campagne). Icone Acceleration (desc).
# When Defeated: The player who defeat this scheme searches Sebastian Shaw from the set-aside area, put it into play under the player's
# control. Remove this card from the campaign.
# [star] Boost: Reveal this card. Place 2 additional threat here.
#
# Cartes de reference : 04092 Super Absorbing Power (`WhenCardBecomeBoost("This", ...)` + `RevealThisCard`), `AbilitePotentialAlly`.
# « Remove this card from the campaign » : releve de carnet (campagne), pas une capacite de jeu : a la fin de la partie, la carte est retiree
# des cartes de campagne (cle de carnet `Removed Campaign Cards`, voir campagne hellfire_hunt).
def GetAbilities() -> Sequence['Ability']:
    def aide_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « Reveal this card. Place 2 additional threat here » : la carte n'est EN JEU qu'apres la revelation, les 2 menaces se posent donc
        # a son entree en jeu (`aide_entree`), seulement si elle vient d'un boost (drapeau).
        effect.this.hf_boost_en_cours = True
        RevealThisCard(effect, message)

    def aide_entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        if getattr(this, "hf_boost_en_cours", False):
            this.hf_boost_en_cours = False
            this.PlaceThreatOnSchemes([this], 2, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", aide_boost),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This", aide_entree),
        AbilitePotentialAlly("Sebastian Shaw"),
    ]
