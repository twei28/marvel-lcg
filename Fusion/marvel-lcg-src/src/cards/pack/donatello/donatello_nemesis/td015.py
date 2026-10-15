from . import *

# * Baxter Stockman — SBIRE nemesis (2/5). GENIUS. PV 3, MNG 2, ATQ 0, boost 2.
# Quickstrike.
# Baxter Stockman cannot take damage while there are any MOUSERS or FLYBORGS in
#   play.
# Forced Interrupt: When Baxter Stockman would attack you, he schemes instead.
# (Donatello's nemesis minion.)
#
# LECTURE DU SCAN (verifiee contre 01167 Vulture) : le disque orange « 3 » est
# les POINTS DE VIE (pas le boost) ; les deux marques rouges du coin sont le
# BOOST (2).
#
# CARTES DE REFERENCE
#  - `04117`/`tt023` Master Pandemonium / `jj018` : « cannot take damage » =
#    `UnitCannotTakeDamage`, ici sous CONDITION : `UnitCannotTakeDamageWhile(
#    NonKeyword, "This", while_face_is_in_play=CardFinder(...))`
#    (damage.py:301, qui prevoit exactement ce parametre).
#  - `ra029` (thor_jane_foster_nemesis) / `jj019` Purple Man : « would attack,
#    X instead » = `WhenUnitWouldAttack(ForcedInterrupt, "This", op)` +
#    `message.SetBeInstead(effect)` puis `this.DoSchemes(player, effect)`.
#  - `01167` Vulture : `desc.Quickstrike = "1"` lu nativement.
#
# TEXTE CONTRE CODE
#  « any MOUSERS OR FLYBORGS IN PLAY » -> OU, minions en jeu ; Baxter n'a ni
#    l'un ni l'autre de ces traits : il ne se protege pas lui-meme.
#  « would attack YOU, he SCHEMES INSTEAD » -> remplacement (`SetBeInstead`),
#    le sbire manigance contre le joueur attaque ; Quickstrike le declenche a
#    l'engagement, donc il manigancera des l'engagement.
#  « Quickstrike » : `desc`, aucun script (mots-cles/quickstrike.md).
#  ⚠ Nom unique SANS l'etoile pour tout `CardFinder(name=...)`.


def GetAbilities() -> Sequence['Ability']:

    def manigancer_a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        joueur = message.property.against_player or this.GetEngagedPlayer()
        if joueur:
            this.DoSchemes(joueur, effect)

    return [
        AbilityFactory.UnitCannotTakeDamageWhile(
            AbilityType.NonKeyword,
            "This",
            while_face_is_in_play=CardFinder(traits=TRAITS_ESSAIM, card_type=Minion),
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            manigancer_a_la_place,
        ),
    ]
