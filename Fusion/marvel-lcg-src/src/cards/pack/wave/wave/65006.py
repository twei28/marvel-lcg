from . import *

# * Ocean's Fury — evenement signature, x2 (9-10/15). SUPERPOWER. Cout 1.
# Max 1 per round.
# Hero Action: Until the end of the round, after Wave defeats an enemy or
# removes the last threat from a scheme, draw 1 card and flip a facedown
# card in your Rising Tide area faceup.
#
# Modele EXACT : 28006 Unleash Nova Force (pack nova) -- meme structure
# « jusqu'a la fin du round, apres [le heros] vainc un ennemi OU retire la
# derniere menace, fait X » : deux `AbilityFactory` enregistrees en TEMP sur
# la face du HEROS (`hero.effect.RegisterTemp`, pas sur l'evenement lui-meme,
# qui repart en defausse aussitot joue) avec `until_round_end=True`.
#  - « defeats an enemy » -> `AfterUnitDefeatedUnit(Temp0, "This", Enemy,
#    ...)`, « This » valant ici la face heros ou l'effet est enregistre.
#  - « removes the last threat from a scheme » -> `AfterSchemeRemoveThreat(
#    Temp0, None, ..., last_threat=True, by_who="This")` -- plus large que
#    « thwarts » (couvre TOUT retrait de menace par Wave, pas seulement un
#    Thwart), ce qui colle au verbe imprime « removes ».
# « Max 1 per round » -> `.MaxOnePerRound()` sur la capacite de jeu, meme
# lecture que 28006 (« Nova » MaxOnePerRound imprime pareillement).

def GetAbilities() -> Sequence['Ability']:

    def oceans_fury(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return
        hero = initiator.GetHero()
        if hero is None:
            return

        def declenche() -> None:
            initiator.DrawUp(1, effect)
            RetournerUneCarteRisingTide(
                effect, initiator, face_visible=False, forced=False,
                prompt="Flip a facedown card in your Rising Tide area faceup",
            )

        hero.effect.RegisterTemp(
            AbilityFactory.AfterUnitDefeatedUnit(
                AbilityType.Temp0, "This", Enemy,
                lambda effect2, message2: declenche(),
            ),
            AbilityFactory.AfterSchemeRemoveThreat(
                AbilityType.Temp0, None,
                lambda effect2, message2: declenche(),
                last_threat=True, by_who="This",
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            oceans_fury,
        ).SetPlay().SetLabel()
        .MaxOnePerRound(),
    ]
