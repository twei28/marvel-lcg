from . import *

# Arrival of the Triple-Evil! (Obligation, « Give to the Delroy Garrett Jr. player »)
#
# When Revealed: Find The Triune Understanding support and put it into play. Place 1 acceleration counter on
#   it and it gains the Permanent keyword.
# Response: After you use The Triune Understanding's Alter-Ego Action, place 1 apostasy counter on it. When
#   there are 3 such counters on it, discard it and remove this obligation from the game.
#
# CARTES DE REFERENCE
#  - `GiveTo` : natif (`desc.GiveTo`), aucun code -- obligation donnee au joueur Delroy Garrett Jr., comme
#    toute autre carte "Give to the <X> player".
#  - "Find <nom> support and put it into play" : modele `bs001b` Hank McCoy (Beast) : `Search.PlayerCard(effect,
#    joueur, include_player_deck=True, include_discard_pile=True, name=.., card_type=Support)` puis
#    `face.PutIntoPlay(joueur, effect, under_control=True)`.
#  - "Place 1 acceleration counter on it" : modele `rr002` Sentry (`Faces.PlaceCountersOn([face], n, nom, effect)`),
#    meme nom de compteur deja enregistre nativement pour `pu007` Burning Building (`card_face.py:355`,
#    "acceleration").
#  - "it gains the Permanent keyword" -> `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..),
#    permanent=1)`, modele `sd018` The Real Question : donner le mot-cle est bien une capacite imprimee, le
#    moteur (`HasPermanent.OnWhenCardLeavePlay`) gere seul le blocage de sortie de jeu une fois le mot-cle pose.
#  - "After you use The Triune Understanding's Alter-Ego Action" -> `AbilityFactory.AfterPlayerResolveAbility(
#    ForcedResponse, "You", CardFinder(name=..), op, which_abilities="AlterEgoAction")`, modele `rc011` Officer
#    Lewis (meme fabrique, meme filtre `which_abilities` sur le type d'habilete declenchee).
#  - "Place 1 apostasy counter" / "When there are 3 such counters ... discard it" : modele `dm012` Secret
#    Initiative (meme session) : `Faces.PlaceCountersOn` + `AbilityFactory.AfterCounterPlacedOn(.., at_least=3, ..)`.
#  - "remove this obligation from the game" : `Faces.RemoveAllFromGame([effect.this], effect)` (modele `16155`).
#
# TEXTE CONTRE CODE
#  "Find THE TRIUNE UNDERSTANDING support" : recherche par NOM (`name="The Triune Understanding"`), pioche ET
#    defausse (comme bs001b) -- aucune restriction imprimee a la pioche seule. Sans copie trouvable (deja en
#    jeu, ou jamais incluse au deck), rien ne se passe : `Search.PlayerCard` rend `None` silencieusement.
#  "and PUT IT INTO PLAY" : sous le controle du joueur (`under_control=True`), pas dans la main.
#  "Place 1 acceleration counter on IT" : sur LA CARTE trouvee (The Triune Understanding), jamais sur
#    l'obligation elle-meme -- l'obligation ne porte pas `CanPlaceCounter` pour ce compteur.
#  "IT gains the Permanent keyword" : meme carte, en PERMANENCE (pas "until end of round") -- la fabrique
#    `GiveKeywordToInPlayWhenApplyThis` s'eteint seulement si l'obligation elle-meme quitte le jeu, ce qui
#    n'arrive qu'au meme instant que la defausse de la carte elle-meme (branche 2, ci-dessous) : aucune fenetre
#    ou le mot-cle manquerait avant que la protection ne soit plus necessaire.
#  "After YOU use ... Alter-Ego Action" : le joueur qui a recu l'obligation (`trigger_player="You"`), jamais un
#    autre -- un seul joueur peut de toute facon controler The Triune Understanding dans ce deck mono-joueur.
#  "place 1 apostasy counter ON IT" : toujours sur The Triune Understanding, jamais sur l'obligation.
#  "When there are 3 SUCH counters" : le compteur `apostasy`, pas un autre -- `AfterCounterPlacedOn(..,
#    "apostasy", at_least=3)`.
#  "discard IT and remove THIS obligation from the game" : DEUX cibles distinctes dans la meme phrase -- The
#    Triune Understanding est DEFAUSSEE (`Faces.DiscardAll`, meme set "3-D Man" que l'obligation : le mot-cle
#    Permanent qu'elle porte ne bloque pas cette sortie-ci, lecture confirmee par `permanent.md`), et
#    l'obligation elle-meme est RETIREE DU JEU (`Faces.RemoveAllFromGame`, pas une simple defausse).
#
# Chiffres : 1 compteur acceleration (pose une fois, a l'entree en jeu) ; 1 compteur apostasy par usage de
# l'Action alter-ego ; seuil 3.


def GetAbilities() -> Sequence['Ability']:

    def arrivee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        comprehension = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name="The Triune Understanding",
            card_type=Support,
        )
        if comprehension is None:
            return
        if not comprehension.PutIntoPlay(joueur, effect, under_control=True):
            return
        Faces.PlaceCountersOn([comprehension.CastTo(CanPlaceCounter)], 1, "acceleration", effect)

    def apres_action_alter_ego(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        Unused(message)
        comprehension = message.trigger.CastTo(CanPlaceCounter)
        Faces.PlaceCountersOn([comprehension], 1, "apostasy", effect)

    def seuil_atteint(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Faces.DiscardAll([message.trigger], effect)
        Faces.RemoveAllFromGame([effect.this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            arrivee,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="The Triune Understanding"),
            permanent=1,
        ),
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.ForcedResponse,
            "You",
            CardFinder(name="The Triune Understanding"),
            apres_action_alter_ego,
            which_abilities="AlterEgoAction",
        ),
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedResponse,
            CardFinder(name="The Triune Understanding"),
            "apostasy",
            seuil_atteint,
            at_least=3,
        ),
    ]
