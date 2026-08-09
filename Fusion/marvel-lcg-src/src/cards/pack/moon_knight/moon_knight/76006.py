from . import *

# Different Strokes — custom « DesignHacker »
# Interrupt: When you play an aspect card, place a madness counter here.
#   (Limit once per round for each aspect.)
# Action: Remove 3 madness counters → ready your identity or change form.
# Forced Interrupt: When the player phase ends, remove all madness counters.
#
# La limite « une fois par round et par aspect » est suivie dans un attribut
# maison de `world`, remis à zéro en même temps que les compteurs.

ASPECTS = ("Aggression", "Justice", "Leadership", "Protection")


def _aspects_marques(world: 'Any') -> set:
    marques = getattr(world, "mk_strokes_aspects_round", None)
    if marques is None:
        marques = set()
        setattr(world, "mk_strokes_aspects_round", marques)
    return marques


def GetAbilities() -> Sequence['Ability']:

    def carte_aspect_jouee(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        # Le trigger du message est le JOUEUR ; la carte jouee est played_face.
        classe = message.played_face.paper.desc.get("Class", "")
        marques = _aspects_marques(effect.world)
        if classe not in ASPECTS or classe in marques:
            return
        marques.add(classe)
        Faces.PlaceCountersOn([this], 1, 'madness', effect)

    def redresser_ou_changer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        identite = initiator.GetIdentity()

        def redresser(targets: Sequence['CardFace']) -> None:
            if identite is not None:
                Faces.ReadyAll([identite], effect)

        def changer(targets: Sequence['CardFace']) -> None:
            ChoisirEtChangerDeForme(initiator, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Ready your identity", redresser),
            AbilityFactory.ForChoiceAbility("Change form", changer),
        )

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        _aspects_marques(effect.world).clear()
        n = this.GetCounters('madness')
        if n > 0:
            Faces.RemoveCountersOn(this, "All", 'madness', effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            None,
            carte_aspect_jouee,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            redresser_ou_changer,
        ).SetName("Different Strokes")
        .SetCostFunc(CostFunc.Counter("This", 3, 'madness')),
        Ability(
            AbilityType.ForcedInterrupt,
            Message.WhenPhaseEnd,
            [
                # « When the PLAYER phase ends » : ne pas purger les compteurs
                # gagnés pendant la phase du méchant (défenses type Gear Up).
                lambda effect, message: message.phase_name == "Player",
            ],
            fin_de_phase,
        ),
    ]
