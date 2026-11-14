from . import *

# The Power Cosmic — Ressource [energy][energy].
# Response: After you spend this card to play a [[COSMIC]] event, deal 2 damage to an enemy.
#
# Cartes de reference :
#  - `42008` Avian Anatomy (angel) : `AfterYouSpendThisCard(Response, op, to_pay_card=CardFinder2("AERIAL", Event))`,
#    meme texte « After you spend this card to pay for a <trait> event ».
#  - `sh001` : meme fabrique, Hero Response sur un evenement (sans `SetPlay`).
#
# ⚠ Mots-pieges :
#  - « Response » nue (pas « Hero Response ») : se joue sous toute identite.
#  - « to play a COSMIC EVENT » : trait COSMIC ET type Event ; une amelioration ou un soutien COSMIC ne declenche pas.
#  - « an enemy » : un ennemi quelconque (sbire ou mechant), choisi par le joueur.
#  - La ressource vaut YY : le deck compte 2 exemplaires.


def GetAbilities() -> Sequence['Ability']:

    def pouvoir_cosmique(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(message)

        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            pouvoir_cosmique,
            to_pay_card=CardFinder2("COSMIC", Event),
        ).SetTarget(Enemy),
    ]
