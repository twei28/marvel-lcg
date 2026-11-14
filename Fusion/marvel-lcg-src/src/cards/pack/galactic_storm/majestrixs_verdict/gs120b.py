from . import *

# * Shi'ar Throne (face B) — SOUTIEN (Majestrix's Verdict), sans cout. LOCATION. SHI'AR.
# Resource: Exhaust Shi'ar Throne → generate a [mental] resource for any player.
# Forced Response: After Shi'ar Throne or Lilandra leaves play, flip this card and reveal it.
#
# Cartes de reference :
#  - « Resource: Exhaust → generate [x] for any player » : modele OFFICIEL 16142 Milano et sk062 Baxter Building
#    (`CanGenerateResources(Resource, ..).SetCostFunc(Exhaust("This")).AnyPlayerCanDoThis()`).
#  - icone [mental] : carre bleu « noeuds relies », verifie par decoupe contre sk003 Wiccan (RES=B) et l'icone
#    [mental] du texte de sk148 (meme auteur).
#  - « After X leaves play, flip this card and reveal it » : `AfterCardLeavePlay(ForcedResponse)` (la sienne
#    porte NoOutOfPlayLimit) ; la face A revelee est une manigance annexe qui entre en jeu avec 3[per_hero]
#    menaces (helper `RevelerLeTrone`).
#
# ⚠ Mots-pieges : « Shi'ar Throne OR Lilandra » (deux declencheurs) ; « for ANY player » ; la ressource est
# [mental], pas [wild].


def GetAbilities() -> Sequence['Ability']:

    def retourner(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        RevelerLeTrone(effect.this, effect)

    def lilandra_part(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        return EstLilandra(message.trigger) and effect.this.IsInPlay() and Support.IsType(effect.this)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
        AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, "This", retourner,
                                          conditions=[lambda effect, message: Support.IsType(effect.this.card.face)]),
        AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, CardFinder(name=LILANDRA, card_type=Ally),
                                          retourner, conditions=[lilandra_part]),
    ]
