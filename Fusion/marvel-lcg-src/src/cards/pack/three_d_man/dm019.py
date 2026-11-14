from . import *

# Brick Session (Event) -- miroir THW de dm018 Getting it Done
#
# Hero Interrupt: When you make a basic thwart, you get +3 THW for this thwart. You may split this threat
#   removal between schemes. If you reduced this card's cost, ready your hero.
#
# CARTES DE REFERENCE
#  - dm018 Getting it Done (meme pack, meme session) : structure IDENTIQUE cote ATQ -> ici
#    `AbilityFactory.WhenUnitMakeThwart(HeroInterrupt, "You", op, is_basic_power=True)` +
#    `message.GainTHWForThisThwart(3, effect)`.
#  - `mw005`/`sk042` : "divide threat removal among schemes as you choose" -> `.SetTarget(Scheme2, range=(1, N),
#    repeat_rules="Threat")` (chaque occurrence = 1 menace, plafonnee par la menace restante de chaque manigance
#    choisie), puis `this.RemoveThreatFromSchemes(effect.targets, 1, effect)`. N = 4 (CTR imprime 1 + bonus 3),
#    meme limite assumee que dm018 (boosts externes de CTR deja actifs non comptes).
#  - Meme arbitrage utilisateur que dm018 : partage REEL (pas une duplication du retrait complet sur chaque
#    manigance) -> annuler le contre normal (`message.SetBeInstead`) puis distribuer le total.
#  - "You MAY split" -> `initiator.ChooseAbilities` (Ne pas partager / Partager), modele dm018.

def GetAbilities() -> Sequence['Ability']:

    def brick_session(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Event)
        message.GainTHWForThisThwart(3, effect)

        initiator = effect.GetInitiator()

        def ne_pas_partager(targets: Sequence['CardFace']) -> None:
            Unused(targets)

        def partager(targets: Sequence['CardFace']) -> None:
            message.SetBeInstead(effect)
            this.RemoveThreatFromSchemes(targets, 1, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Don't split this threat removal", ne_pas_partager),
            AbilityFactory.ForChoiceAbility(
                "Split this threat removal between schemes",
                partager,
            ).SetTarget(Scheme2, range=(1, 4), repeat_rules="Threat"),
        )

        if CoutReduit(effect):
            identite = initiator.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.HeroInterrupt,
            "You",
            Scheme2,
            brick_session,
            is_basic_thwart=True,
        ).SetPlay(),
    ]
