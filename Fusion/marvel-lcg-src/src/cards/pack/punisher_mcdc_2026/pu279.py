from .commun import *

# Rise of the Machines (defi 1, p279, ID 6140) : Vision (Synthezoid Smackdown), complots Rallying Call / Neighborhood Protectors (Civil War), sets Sentinels,
# Future Past, Doomsday Chair, Vision Nemesis, Super Strength (attachements seulement). Difficulte 5.
# Regles speciales : (1) « Cards with a printed [energy] deal 1 additional damage » ; (2) « All Future Past cards lose victory 1 » ;
# (3) « When the villain stage advances, advance the main scheme to 2A ».
#
# Cartes de reference : mojo/fantasy/39042 (`UnitTakeAdditionalDamageFromCards` + `CardFinder(has_printed_res="Y")`, meme fabrique), pu139 (`printed_victory`),
# challenges/2412 (avancer le complot a 2A).
# Decision de l'utilisateur (22/10/2026) : « deal 1 additional damage » = TOUT degat inflige par la carte (evenement, attaque d'allie, amelioration...).
# Decisions de portage : « lose victory 1 » = la carte n'a plus de Victory (`printed_victory = None`), posee quand la carte entre en jeu (une carte jamais
# en jeu n'a pas de victoire a perdre).

SET_FUTURE_PAST = "Future Past"


def GetAbilities() -> Sequence['Ability']:

    def perdre_la_victoire(effect: 'Effect', message: 'Message.AfterCardPutIntoPlay') -> None:
        message.trigger.printed_victory = None

    def est_future_past(effect: 'Effect', message: 'Message.AfterCardPutIntoPlay') -> bool:
        return message.trigger.paper.set_name == SET_FUTURE_PAST and getattr(message.trigger, 'printed_victory', None) is not None

    return [
        AbilityFactory.UnitTakeAdditionalDamageFromCards(Unit2, 1, CardFinder(has_printed_res="Y")),
        Ability(AbilityType.Challenge, Message.AfterCardPutIntoPlay, [est_future_past], perdre_la_victoire),
        ComplotEn2A(),
    ]
