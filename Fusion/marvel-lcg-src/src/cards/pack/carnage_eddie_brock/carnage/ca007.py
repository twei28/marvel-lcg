from . import *

# * Hunting Hosts : AMELIORATION (SKILL.), cout 2, [mental]. Classe Hero.
# Response: After you attack and defeat an ELITE minion -> ready this card.
# Action: Exhaust this card -> search the encounter deck and discard pile for a minion and put it into play engaged with you. (Shuffle.)
#
# CARTES DE REFERENCE
#  - « After you attack and defeat a MINION » : `an001a` (Frenzy) : `AfterUnitDefeatedUnit(Response, "You", Minion, op)` + `LimitOncePerRound` (absente ici) ; `is_from_attack=True` pour « attack AND defeat » (`an004`).
#    Condition ELITE : `message.target.HasTrait("ELITE")` (`ua003`).
#  - « search the encounter deck and discard pile for a minion and put it into play engaged with you » : `ar014` (Lead the Charge) : `Search.EncounterCard(effect, joueur, include_discard_pile=True, card_type=Minion)` + `PutIntoPlay(joueur, ..)` ;
#    mise en jeu engagee : `ca001b` (Dark Urges, meme carte modele 01116b).
#
# TEXTE CONTRE CODE
#  « Response » NU (pas Hero Response) : jouable dans les deux formes. « After YOU attack AND defeat an ELITE MINION » : `"You"` + `is_from_attack=True` + type `Minion` (le vilain ne compte pas) + condition ELITE. « ready THIS card » : l'amelioration, pas Carnage.
#  « Exhaust this card → » : COUT. « encounter deck AND discard pile » : `include_discard_pile=True`. « a minion » : un seul, au choix du joueur. « engaged WITH YOU » : mis en jeu pour ce joueur. « (Shuffle.) » : le deck de rencontre est remelange par la recherche (comportement par defaut).
#  Chiffres : cout 2, un sbire.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        Faces.ReadyAll([effect.this], effect)

    def sbire_elite(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        Unused(effect)
        return message.target.HasTrait("ELITE")

    def chasser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            card_type=Minion,
        )
        if face is not None:
            face.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            redresser,
            is_from_attack=True,
            conditions=[sbire_elite],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chasser,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
