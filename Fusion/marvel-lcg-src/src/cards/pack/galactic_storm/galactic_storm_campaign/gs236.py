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
#  - **`message.paid_resources`** (`sender_player.py:211`, `AfterPlayerPlayedCard`) : rend les ressources
#    REELLEMENT utilisees pour payer LA CARTE JOUEE, posees sur le MESSAGE (pas sur `effect`, qui est ici
#    celui de la Reponse declenchee APRES coup — `effect.GetPaidResources()` lirait le paiement de CETTE
#    reponse, vide, pas celui de Thor ; piege trouve en ecrivant le cas de test, 0 degat au lieu de 2).
#
# ⚠ Mots-pieges :
#  - « for each [energy] resource YOU USED TO PAY for him » : les ressources du PAIEMENT de Thor
#    lui-meme, pas une ressource generee ailleurs ;
#  - « each minion ENGAGED WITH YOU » : uniquement les sbires engages avec le controleur de Thor, pas le
#    mechant ni les sbires d'un autre joueur.


def GetAbilities() -> Sequence['Ability']:

    def thor(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        nombre = message.paid_resources.rbyg.y
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
