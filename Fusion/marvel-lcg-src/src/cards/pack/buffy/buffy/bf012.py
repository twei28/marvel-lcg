from . import *

# Redeemed — AMELIORATION (PREPARATION), cout 4, [mental].
# Response: After a non-ELITE minion enters play, attach Redeemed to it.
# Take control of attached minion and treat it as a SLAYER ally with a blank text box. Its THW is equal to its printed SCH and it takes 1
# consequential damage after it thwarts or attacks.
#
# CARTES DE REFERENCE
#  - `51036` Redemption / `34009` Mind Control : `TakeControlOfAttachedMinion(<fiche modele>)` (`Faces.TreatAsAlly`) pour toute la 2e phrase ;
#    la fiche modele `buffy_redeemed_ally` (cards.json) porte le trait SLAYER et les degats consequents `0*` (THW/ATQ), comme `redemption_redeemed_ally`.
#  - `27189b` Wrist Navigators : `AfterCardEnterPlay(.., op).SetTarget("Trigger")` + `this.AttachTo2(message.trigger, effect)` pour « after a minion enters
#    play, attach this to it ».
#
# TEXTE CONTRE CODE
#  « non-ELITE minion » -> `NonEliteMinion` (jamais un ELITE). « Response » nu (pas Hero Response, pas Forced). « attach Redeemed to it » -> la carte quitte
#    le heros et s'attache au sbire ; c'est alors, et alors seulement, que le controle est pris (`AfterCardGainUpgrade`).
#  La Reponse est OPTIONNELLE : le joueur peut refuser. THW = SCH imprime et degat consequent 1 : rendus par `Faces.TreatAsAlly`.


def GetAbilities() -> Sequence['Ability']:

    def redeemed(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        this.AttachTo2(message.trigger, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            NonEliteMinion,
            redeemed,
        ).SetTarget("Trigger"),
        AbilityFactory.TakeControlOfAttachedMinion(NOM_MODELE_REDEEMED),
    ]
