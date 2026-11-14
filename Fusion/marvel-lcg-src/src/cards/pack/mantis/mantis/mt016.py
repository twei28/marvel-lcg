from . import *

# Mindlink : EVENEMENT Basic, cout 0, [wild]. Team-Up (Drax and Mantis). Max 1 per deck. (Version « evenement » envoyee par l'utilisateur ; la planche PDF imprime une autre version, en amelioration.)
# Hero Action: Spend up to 2 [mental] resources → heal 2 damage from an identity for each [mental] resource spent. You may take 1 damage to shuffle this card into your deck.
#
# CARTES DE REFERENCE
#  - `hc020` Green Hell / `mots-cles/teamup.md` : evenement Team-Up = `desc.TeamUp` + `.SetTarget("TeamUp")` obligatoire (assert du chargeur) ; les alliés comptent.
#  - `vision/26022` Machine Man / `gmw/nebula/16093` : « Spend up to N » = `.SetCost(Cost("..", up_to=True))`, lu par `effect.GetPaidResources().val`.
#  - `mf004` / `ra010` : `SetTarget(Identity, canbe_heal=True)` pour « an identity ».
#  - `53003` Bird of Prey : « You may ... » apres l'effet = `MayChooseOneAbility(effect, ForChoiceAbility(..))` ; `dt009` : `TakeDamage(source, n, effect)` ; `gs006` : se melanger au deck (`Faces.ShuffleAllTo`).
#
# TEXTE CONTRE CODE
#  « Spend UP TO 2 [mental] » : 0, 1 ou 2 ressources mentales (la wild compte). « heal 2 damage FROM AN identity FOR EACH [mental] resource spent » : 2 par ressource depensee, sur UNE identite au choix (de n'importe
#  quel joueur). « You MAY take 1 damage TO shuffle this card » : facultatif ; le degat (1) est subi par l'identite du joueur, puis la carte retourne dans son deck.
#  Chiffres : cout 0, 2 ressources, 2 soins, 1 degat.


def GetAbilities() -> Sequence['Ability']:

    def mindlink(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        depenses = joueur.AskSpendResourcesInternal(Cost("BB", up_to=True), effect)
        depensees = depenses.val if depenses is not None else 0
        this.HealthUnits(effect.targets2, 2 * depensees, effect)

        def se_melanger(cibles: Sequence['CardFace']) -> None:
            identite = joueur.GetIdentity()
            identite.CastTo(Unit2).TakeDamage(this, 1, effect)
            Faces.ShuffleAllTo([this], joueur.player_deck, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 1 damage to shuffle this card into your deck",
                se_melanger,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mindlink,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Identity, is_optional=False),
    ]
