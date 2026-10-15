from . import *

# Untrustworthiness — OBLIGATION du set Lyja (n° 65). 2 icones boost.
# Give to the Laura Green player.
# Forced Interrupt: When a "Boost" or "When Revealed" ability on a TREACHERY card would
#   be resolved, cancel that ability. Then, deal yourself 1 facedown encounter card.
# Alter-Ego Action: Exhaust Laura Green → discard Untrustworthiness.
#
# Cartes de reference :
#  - **`16108`** Kree Command Ship / **`dz037`** Coolest Team-Up Ever! :
#    `WhenPlayerRevealCard(Interrupt, "AnyPlayer", <carte>, "WhenRevealed", op,
#    from_encounter=True)` + `message.CancelWhenRevealedEffect(effect)` : annuler le
#    « When Revealed » d'une traitrise AVANT qu'il se resolve (le mot-cle
#    « WhenRevealed » reserve a l'annulation du seul When Revealed ; « All » annulerait
#    aussi Surge/Incitation, hors texte).
#  - **`22012`** Wraith / **`16158`** : `WhenBoostCardTurnedFaceUp(Interrupt, "Ability", op)`
#    + `message.CancelBoostAbility(effect)` pour annuler le « ★ Boost ».
#  - **`player.DealEncounterCards(n, effect)`** (player_action.py) pour « deal yourself 1
#    facedown encounter card » (utilise aussi par les cartes qui envoient une carte
#    cachee a un joueur).
#  - **`sk031`** Interracial Hatred (Hulkling, meme coffret) : « Alter-Ego Action: Exhaust
#    <alter ego> → discard this obligation ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a "Boost" OR "When Revealed" ability » : DEUX fenetres, les deux branchees.
#  - « on a TREACHERY card » : type Treachery OU trait TREACHERY (decision du 15/10/2026),
#    donc aussi les evenements de Lyja ; une carte sans effet « When Revealed » / « Boost »
#    ne declenche rien (rien a annuler : pas de carte donnee non plus).
#  - « cancel THAT ability » : seulement le When Revealed / le Boost, pas les icones de boost.
#  - « THEN deal yourself » : apres l'annulation ; « yourself » = le porteur de l'obligation,
#    pas le joueur qui revele.
#  - « Forced » Interrupt : obligatoire.


def GetAbilities() -> Sequence['Ability']:

    def se_donner_une_carte(effect: 'Effect') -> None:
        this = effect.this.CastTo(Obligation)
        # Le porteur : le joueur dont la zone d'obligations contient la carte (une obligation
        # n'est « en jeu » pour personne : `GetControlByPlayer` y leve une assertion).
        joueur = next((j for j in Worlds.GetPlayers(effect) if this.card.area == j.obligations_area), None)
        if joueur is None:
            joueur = Worlds.GetFirstPlayer(effect)
        joueur.DealEncounterCards(1, effect)

    def annuler_revelation(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        message.CancelWhenRevealedEffect(effect)
        se_donner_une_carte(effect)

    def annuler_boost(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        message.CancelBoostAbility(effect)
        se_donner_une_carte(effect)

    def defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.ForcedInterrupt,
            "AnyPlayer",
            FinderTraitrise(),
            "WhenRevealed",
            annuler_revelation,
        ),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.ForcedInterrupt,
            "Ability",
            annuler_boost,
            conditions=[lambda effect, message: EstTraitrise(message.trigger)],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            defausser,
        ).SetCostFunc(CostFunc.Exhaust("YourAlterEgo")),
    ]
