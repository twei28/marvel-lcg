from . import *

# Fear Projection — ATTACHEMENT. SPELL. Boost 1.
# Attach to Krahllak.
# Krahllak gains retaliate 1.
# Hero Action : Place 2 corruption counters on your Creeping Corruption → discard this card.
# Alter-Ego Action : Spend [mental][mental][mental] resources → discard this card. Remove 1 corruption counter from your Creeping Corruption.
#
# Cartes de reference : 01119 Solid-Sound Body (`GiveKeywordToAttached(.., retaliate=1)` + `PlayerActionToDiscardThis(HeroAction)` + `SetCost`), iman_model_42 `CoutDuReacteur` (un jeton
# pose PAR LE COUT, `CostFunc.Custom`, impayable sans cible : sinon l'action resout a vide et le pilote la rejoue sans fin), mister_fantastic/mf004 (`AlterEgoAction`).
# ⚠ Mots-pieges : « [mental][mental][mental] » = `BBB` (verifie contre une carte du meme pack : la ressource mentale est le reseau de noeuds, voir QUESTIONS.md Q9) ; la phrase « Remove 1
#  corruption counter » vient APRES la fleche : c'est un EFFET (de l'Alter-Ego Action uniquement), pas un cout ; « 2 counters » : DEUX jetons d'un coup (le seuil de 5 peut etre franchi) ;
#  l'Action Heros n'est offerte qu'avec une Creeping Corruption.


def GetAbilities() -> Sequence['Ability']:

    def retirer_un_jeton(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            RetirerCorruption(effect, joueur)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=KRAHLLAK)),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=KRAHLLAK), retaliate=1),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction, conditions=[PeutPayerCorruption])
            .SetCostFunc(CoutPlacerCorruption(2)),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction, ex_operation=retirer_un_jeton)
            .SetCost(Cost("BBB")),
    ]
