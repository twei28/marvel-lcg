from . import *

# * Jessica Jones (alter-ego) — custom « ekAugust »
# Setup: Shuffle the On the Job set into the encounter deck.
# Pays the Bills — Response: After a side scheme is revealed, draw 2 cards.
#   (Limit once per phase.)
#
# Le set « On the Job » est declare comme set de rencontre supplementaire au
# moment ou le monde construit le deck rencontre (Message.WhenGameBeginSetup) :
# c'est le seul point ou les cartes peuvent encore etre melangees dedans, le
# deck etant cree puis melange juste apres (voir World.Begin, etape 10).

ON_THE_JOB = "on_the_job"


def GetAbilities() -> Sequence['Ability']:

    def with_on_the_job(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)

        def add_encounter_set(effect2: 'Effect', message2: 'Message.WhenGameBeginSetup') -> None:
            if ON_THE_JOB not in message2.encounter_set_names:
                message2.encounter_set_names.append(ON_THE_JOB)

        this.effect.RegisterTemp(
            AbilityFactory.WhenGameBeginSetup(add_encounter_set),
            unregister_after_exec=True,
        )

    def pays_the_bills(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        this = effect.this.CastTo(AlterEgo)
        this.GetControlByPlayer().DrawUp(2, effect)

    return [
        # Meme marqueur que sur la face heros : Crack the Case est une simple
        # « Action », donc jouable aussi en alter-ego.
        RecordSideSchemeDefeat(),

        AbilityFactory.WhenPlayerSelectHero(
            "This",
            with_on_the_job,
        ),

        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.Response,
            "AnyPlayer",
            SchemeSide2,
            pays_the_bills,
        ).SetName("Pays the Bills")
        .LimitOncePerPhase(),
    ]
