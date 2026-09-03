from . import *

# * Scarlet Spider — Peter Parker (Earth-98311). Allie d'aspect PROTECTION,
# x1. VARIANT. WEB-WARRIOR. Cout 3, PV 3, CTR 1*, ATQ 2*, ressource [energy].
# Scarlet Spider enters play with 3 sense counters on him.
# Interrupt: When the villain activates against you, remove 1 sense counter
#   from Scarlet Spider -> reduce the amount of boost icons ([boost]) on each
#   boost card by 1 for that activation.
#
# Cartes de reference :
#  - `ThisEnterPlayWithCounters(3, 'sense')` (counter.py:6) pour la premiere
#    phrase : la fabrique existe et pose les compteurs a l'arrivee.
#  - **`27082`** Biting Retort : c'est LA carte qui montre comment modifier
#    les icones de boost sur toute la duree d'une activation —
#    `RegisterTemp(WhenBoostIconsWouldBeCount(Temp0, ... UpdateBoostIcon(...)))`
#    autour de l'activation, puis desenregistrement. Elle le fait a +1 ; ici
#    c'est -1.
#  - **`an006`** Angelic Ribbons (pack angela) pour
#    `WhenEnemyActivateAgainstYou(Interrupt, ..., op)` et pour la lecture de
#    `message.would_message`.
#  - `RegisterTemp(..., until_event_end=message)` (face_effect.py:97) :
#    `WhenEnemyActivateAgainstYou` est un `HasEndEventMessage`
#    (sender_enemy.py:118), donc le moteur retire l'effet TOUT SEUL a la fin
#    de l'activation. C'est plus sur que le `Effects.UnRegister` manuel de
#    27082, qui ne vaut que parce que 27082 declenche l'activation elle-meme.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « When **the villain** activates against you » : le VILAIN, pas un sbire.
#    `CardFinder(card_type=Villain)`, pas `Enemy` — c'est la difference exacte
#    avec an006, qui imprime « an enemy ».
#  - « against **you** » : `WhenEnemyActivateAgainstYou` teste deja
#    `message.to_player != None` ; l'activation contre un autre joueur ne
#    declenche rien.
#  - « remove 1 sense counter from Scarlet Spider **->** » : la fleche en fait
#    un COUT. `CostFunc.Counter("This", 1, 'sense')` refuse le paiement quand
#    il n'y a plus de compteur, donc l'option n'est meme pas offerte.
#    ⚠ « from **Scarlet Spider** », donc `"This"`, PAS la Spider Armor : c'est
#    la seule carte du pack a depenser un compteur qui n'est pas du `metal`.
#  - « on **each** boost card » : toutes les cartes de boost de cette
#    activation, pas la premiere.
#  - « **for that activation** » : la reduction expire avec l'activation.
#    `until_event_end=message`, jamais `until_round_end`.
#  - ⚠ HOMONYME : `mw022` * Scarlet Spider (pack maison madame_web) porte le
#    MEME nom et est AUSSI de classe Protection. Deux cartes distinctes, aux
#    capacites differentes, qui peuvent se croiser dans un meme deck : c'est
#    le `set_name` qui les separe.


def GetAbilities() -> Sequence['Ability']:

    def scarlet_spider(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        this = effect.this.CastTo(Ally)

        # Le compteur `sense` a deja ete retire par le COUT.
        this.effect.RegisterTemp(
            AbilityFactory.WhenBoostIconsWouldBeCount(
                AbilityType.Temp0,
                lambda boost_effect, boost_message:
                    boost_message.UpdateBoostIcon(-1, boost_effect),
            ),
            unregister_after_exec=False,
            until_event_end=message,
        )

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.ThisEnterPlayWithCounters(3, 'sense'),
        AbilityFactory.WhenEnemyActivateAgainstYou(
            AbilityType.Interrupt,
            CardFinder(card_type=Villain),
            scarlet_spider,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'sense')),
    ]
