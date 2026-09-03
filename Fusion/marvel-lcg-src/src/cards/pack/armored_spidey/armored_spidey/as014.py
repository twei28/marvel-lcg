from . import *

# Corporate Expansion — OBLIGATION. Boost 2, donnee au joueur Peter Parker.
# Give to the Peter Parker player.
# You cannot play event cards while in hero form.
# Alter-Ego Response: After a card with the printed cost of 2 or more enters
#   play under your control, discard this obligation.
#
# Cartes de reference :
#  - **`11020`** Depowered : MEME STRUCTURE — une interdiction permanente
#    (`PlayersCannotPlayCardWhile("You", <filtre>)`) plus une sortie qui
#    defausse l'obligation. C'est le modele exact d'une obligation qui RESTE
#    en jeu, par opposition a `im014` / `si014`, qui se resolvent et
#    disparaissent aussitot.
#  - `as010` * Gwen Stacy pour le declencheur jumeau : `AfterCardEnterPlay`
#    + `under_your_control=True` + `CoutPrintedAuMoins(..., 2)`.
#  - `PlayerActionToDiscardThis` (attachment.py:8) pour la forme canonique de
#    « discard this obligation » : `Faces.DiscardAll([this], effect)`. Ici la
#    fabrique n'est pas utilisable telle quelle, le declencheur etant une
#    Reponse et non une Action.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « You cannot play **event** cards » : les EVENEMENTS seulement. Allies,
#    ameliorations, soutiens et ressources passent. Filtre `Event`.
#  - « **while in hero form** » : l'interdiction ne vaut qu'en forme heros.
#    En forme civile, tout se joue normalement — d'ou la condition
#    `IsHero()` sur l'initiateur de l'effet teste. Sans elle, l'obligation
#    verrouillerait les deux formes et rendrait sa propre sortie plus dure.
#  - « **Alter-Ego** Response » : la sortie exige la forme civile, alors que
#    la punition frappe la forme heros. C'est la tension de la carte : elle
#    force a ranger le costume.
#  - « **printed** cost of 2 or more » : cout IMPRIME, sans reduction.
#  - « enters play **under your control** » : pas « you play ». Une carte
#    posee par un autre effet compte.
#  - ⚠ Cette obligation est un vrai etau avec le reste du pack : en forme
#    heros, as004 a as009 sont TOUS des evenements, donc bloques. Ne restent
#    que les pouvoirs de base, as003 Spider-Bot et les ameliorations deja
#    posees. C'est bien ce que le texte impose.


def GetAbilities() -> Sequence['Ability']:

    def en_forme_heros(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        Unused(effect)
        joueur = message.check_effect.initiator
        return joueur is not None and Player.IsType(joueur) and joueur.IsHero()

    def corporate_expansion(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)

        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.PlayersCannotPlayCardWhile(
            "You",
            Event,
            conditions=[en_forme_heros],
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.AlterEgoResponse,
            CardFace,
            corporate_expansion,
            under_your_control=True,
            conditions=[
                lambda effect, message: CoutPrintedAuMoins(message.trigger, 2),
            ],
        ),
    ]
