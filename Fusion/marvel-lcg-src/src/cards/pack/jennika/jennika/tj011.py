from . import *

# Sosaiken (la Voie, type imprime PATH) — carte PERMANENTE de Jennika, 16/16. SENPAI.
# Permanent.
# Response: After you play a Shinobi card, exhaust this card -> draw 1 card.
#
# Type moteur : Support (le moteur n'a pas de type Path ; TODO-QUESTION Q3,
# .planning/tmnt/jennika-questions.md). Mise de cote, jamais dans le deck : le Setup de
# tj001b la met en jeu (modele `wonder_man/58002` Ionic Physiology).
#
# Mot-cle : Permanent (mots-cles/permanent.md) : BASE AUTOMATIQUE (`desc.Permanent`),
# aucun script pour lui — le moteur interdit de la retirer du jeu par un effet d'un
# autre set.
#
# Cartes de reference :
#  - `michelangelo/tm011` : `AfterPlayerPlayedCard(Response, "You", CardFinder(...), op)`
#    + `CostFunc.Exhaust("This")` ;
#  - `DrawUp(1, effect)` : 01026 et autres.
#
# ⚠ Mots-pieges :
#  - « Response » (sans « Hero ») : tient dans les DEUX formes ;
#  - « After YOU play a Shinobi card » : le joueur, carte portant l'une des quatre classes ;
#  - le « -> » est un COUT : incliner d'abord ; pas de limite imprimee (une fois par
#    redressement) ;
#  - aucune limite « once per round » imprimee.


# TODO-QUESTION Q3 (type Path rendu par un Support) : .planning/tmnt/jennika-questions.md
def GetAbilities() -> Sequence['Ability']:

    def sosaiken(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CarteShinobi(),
            sosaiken,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
