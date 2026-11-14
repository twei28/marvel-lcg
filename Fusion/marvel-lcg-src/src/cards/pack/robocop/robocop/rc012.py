from . import *

# Classified : OBLIGATION. Boost 2. A donner au joueur d'Alex Murphy.
# You cannot attack the villain.
# When Revealed: You are stunned. Exhaust Auto-9.
# Hero Action: Exhaust your identity → discard Classified. Any player may trigger this ability.
#
# CARTES DE REFERENCE
#  - `hs015` Vermin Clone : `PlayersCannotAttackWhile("AnyPlayer", .., conditions=[meme_joueur])` (« characters you control » : alliés inclus ; « You » du moteur = l'identité seule).
#  - `11049` Fear of Kang : `PlayerActionToDiscardThis(..)`. `21026` Loss of Control : `CostFunc.Exhaust("YourIdentity")`.
#  - `bf025` Normal Again : `this.GetGaveToPlayer()` pour le joueur a qui l'obligation est donnee ; `Faces.GiveStatus([identite], "Stunned", effect)`.
#
# TEXTE CONTRE CODE
#  « You cannot attack THE VILLAIN » -> le vilain seulement (les sbires restent attaquables), pour le JOUEUR entier a qui elle est donnee (decision utilisateur 01/11 :
#    identite ET allies ; `"You"` du moteur n'exclut que l'identite, d'ou `"AnyPlayer"` + condition sur le joueur). « When Revealed: YOU are stunned » : l'identite
#    de ce joueur. « Exhaust Auto-9 » : l'arme nommee Auto-9 qu'il controle, si elle est en jeu (sinon rien). « Hero Action: Exhaust YOUR identity » : l'identite de celui
#    qui declenche (« Any player may trigger ») ; elle se defausse alors. Hero Action : forme heros seulement.
#  Chiffres : boost 2.


def GetAbilities() -> Sequence['Ability']:

    def classified_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        joueur = this.GetGaveToPlayer() or this.GetControlByPlayer()
        if joueur is None:
            return
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)
        armes = [f for f in joueur.GetControlUpgrade(CardFinder(name=NOM_AUTO_9))]
        if armes:
            Faces.ExhaustAll(armes, effect)

    def meme_joueur(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        this = effect.this.CastTo(Obligation)
        joueur = this.GetGaveToPlayer() or this.GetControlByPlayer()
        return joueur is not None and message.by_effect.GetInitiator() == joueur

    return [
        AbilityFactory.PlayersCannotAttackWhile(
            "AnyPlayer",
            CardFinder(card_type=Villain),
            conditions=[meme_joueur],
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            classified_revele,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .AnyPlayerCanDoThis(),
    ]
