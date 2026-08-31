from . import *

# * Killer Thrill — sbire nemesis. ALIEN. BOUNTY HUNTER. PV 5 / SCH 2 / ATK 2*.
# [star] Killer Thrill gets +1 ATK for each adrenaline counter on her.
# Forced Interrupt: When the player phase ends, put 1 adrenaline counter on
#   Killer Thrill. Then, if there are 2 or more adrenaline counters on her,
#   remove them all and she activates.
# (Venompool's nemesis minion.)
#
# Cartes de reference :
#  - 12011 Ant-Man (pack ant) : `ThisGainKeyword(lambda: GetCounters(...),
#    attack=1, change_on_event=OnEvent.Counter("This", '<compteur>'))`, motif
#    exact du « +1 ATK par compteur ».
#  - bw021 Imperius Rex! (pack brawn) : `face.DoActivate(joueur, effect)` pour
#    « she activates ».
#
# Le compteur `adrenaline` a du etre declare dans l'enum COUNTER du moteur
# (game/card/face/card_face.py) : sans lui, `IsCounter` refuse le nom et la
# carte tombe des la creation de la partie. Meme correctif que les compteurs
# `flame` (human_torch), `calm` (lockjaw) ou `evidence` (jessica_jones).
#
# ⚠ « remove them ALL » : on retire la totalite ("All"), pas 2 — sinon un
# troisieme compteur accumule survivrait a l'activation.

COMPTEUR = 'adrenaline'
SEUIL = 2


def GetAbilities() -> Sequence['Ability']:

    def adrenaline(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        Faces.PlaceCountersOn([this], 1, COMPTEUR, effect)
        if this.GetCounters(COMPTEUR) < SEUIL:
            return

        Faces.RemoveCountersOn([this], "All", COMPTEUR, effect)
        joueur = this.GetEngagedPlayer()
        this.DoActivate(joueur, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui:
                effect.this.CastTo(Minion).GetCounters(COMPTEUR),
            attack=1,
            change_on_event=OnEvent.Counter("This", COMPTEUR),
        ),
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.ForcedInterrupt,
            adrenaline,
        ),
    ]
