from . import *

# * Thor (ERIC MASTERSON) — ALLIE de campagne (Identity-Specific / Campaign, n° 236). Cout 4.
# THW 1* / ATK 3*, 3 PV. ASGARD.
# Honorary.
# Response: After you play Thor from your hand, deal 1 damage to each minion engaged with you for each
#   [energy] resource you used to pay for him.
#
# Cartes de reference :
#  - **`core/spider_man/01002`** Black Cat : `AbilityFactory.AfterPlayerPlayedCard(ForcedResponse, "You",
#    "This", ...)`.
#  - **`game/effect/effect.py:512`** `Effect.GetPaidResources()` : rend les ressources REELLEMENT
#    utilisees pour payer la carte (`effect.context.paid_this_resources`), pose par `ClassCard.Play`
#    (`card_player.py:143`, `SetPaidResources`) a chaque mise en jeu depuis la main.
#
# ⚠ Mots-pieges :
#  - « for each [energy] resource YOU USED TO PAY for him » : les ressources du PAIEMENT de Thor
#    lui-meme, pas une ressource generee ailleurs ;
#  - « each minion ENGAGED WITH YOU » : uniquement les sbires engages avec le controleur de Thor, pas le
#    mechant ni les sbires d'un autre joueur.


def GetAbilities() -> Sequence['Ability']:

    def thor(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        Unused(message)
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        nombre = effect.GetPaidResources().rbyg.y
        if nombre <= 0:
            return
        sbires = [m.CastTo(Minion) for m in Worlds.FindCardsOnField(effect, CardFinder(card_type=Minion))
                  if m.CastTo(Minion).GetEngagedPlayer() == joueur]
        if sbires:
            this.DealDamage(sbires, nombre, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            "This",
            thor,
        ),
    ]
