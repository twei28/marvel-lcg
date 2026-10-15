from . import *

# The Infiltration Has Begun 1B — complot principal, face B. Objectif 8[per_hero], escalade +1[per_hero] (etoile),
# menace de depart 2[per_hero].
# ★ Place 1 additional threat here for each SKRULL enemy in play and each IMPOSTOR ally in play.
# Forced Response: After your turn ends, if there are less than 2[per_hero] suspicion counters on "Who Do You
#   Trust?", put a CAMOUFLAGED ally at random from the IMPOSTOR deck into play under your control.
#
# Cartes de reference :
#  - ★ menace additionnelle a l'escalade : **`60121b`** / **`16091b`** (`WhenCalcThisSchemeEscalation(operation)`,
#    qui s'ajoute a l'escalade imprimee de la phase du complot principal).
#  - Reponse forcee « After your turn ends » : **`gorr gb022`**, **`mojo 39022`** (`AfterPlayerTurnEnd`).
#  - Mettre un allie du paquet : helper `MettreAllieCamoufle` (set), allie sous le controle du joueur dont le tour finit.
#
# ⚠ Mots-pieges : « each SKRULL ENEMY » (sbires ET mechant : Veranke est SKRULL) ; « each IMPOSTOR ALLY » (allies
# seulement : un sbire IMPOSTOR n'est compte qu'en tant que SKRULL enemy) ; « LESS THAN 2[per_hero] » (strictement ;
# 2 par joueur) ; « AFTER YOUR turn ends » : pour CHAQUE joueur, a la fin de son tour, l'allie va a CE joueur ;
# « 2[per_hero] jetons » : Veranke I et II, lecture de `SeuilSoupcons`.


def GetAbilities() -> Sequence['Ability']:

    def escalade(effect: 'Effect') -> int:
        return len(EnnemisSkrull(effect)) + len(AlliesImpostor(effect))

    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        if MoinsDeSoupcons(effect):
            MettreAllieCamoufle(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenCalcThisSchemeEscalation(escalade),
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "AnyPlayer", fin_de_tour),
    ]
