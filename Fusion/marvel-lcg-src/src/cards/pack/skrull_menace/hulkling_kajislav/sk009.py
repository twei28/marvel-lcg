from . import *

# * Alliance — soutien signature (11/16). KREE. SKRULL. Cout 3 [energy].
# Response: After you play a card with the [[KREE]] trait from your hand, deal
#   1 damage to an enemy.
# Response: After you play a card with the [[SKRULL]] trait from your hand,
#   remove 1 threat from the main scheme.
#
# Cartes de reference :
#  - **`18010`** * Gamora's Sword : « Response: After you play an [[attack]]
#    event, deal 1 damage to an enemy. » `AfterPlayerPlayedCard(Response,
#    "You", <filtre>, op).SetTarget(Enemy)`.
#  - `sk001a` (meme set) pour `from_hand=True` et le filtre de trait.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - DEUX Responses distinctes : une carte KREE+SKRULL (sk010, sk012, sk013,
#    sk009 elle-meme ne compte pas : elle est deja jouee) declenche LES DEUX.
#  - « from your hand » : `from_hand=True`.
#  - « **the main** scheme » : le complot principal, pas un annexe.
#  - Aucune condition de forme ni de trait de l'identite : contrairement a
#    sk001a, ici on ne demande PAS que Hulkling partage le trait.
#  - Pas de limite imprimee.
#  - « an enemy » : sbire ou vilain, cible choisie.


def GetAbilities() -> Sequence['Ability']:

    def kree(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    def skrull(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        this.RemoveThreatFromSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="KREE"),
            kree,
            from_hand=True,
        ).SetTarget(Enemy),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="SKRULL"),
            skrull,
            from_hand=True,
        ),
    ]
