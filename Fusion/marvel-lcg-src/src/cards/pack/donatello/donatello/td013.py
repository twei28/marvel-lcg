from . import *

# Broken Shell — OBLIGATION (Boost 2). Give to the Donnie player.
# Flip to alter-ego form and you lose 5 hit points. If this would defeat your
#   identity, set your hit point dial to 1 instead. You cannot change to hero
#   form.
# Alter-Ego Action: Spend [mental][mental] resources or discard Donatello's
#   Shell from play -> remove Broken Shell from the game.
#
# ⚠ MODULE RANGE DANS `donatello/` ET NON `donatello_nemesis/` : le bandeau
# imprime dit « DONATELLO » (set_name « Donatello »). Meme piege que sf010.
#
# CARTES DE REFERENCE
#  - `ho013` Risky Business / `sf010` Shame : `WhenThisObligationGiveToYou(op)`
#    (`message.GetGaveToPlayer()`) + `PlayerActionToRemoveThisFromGame(
#    AlterEgoAction)` a cout.
#  - `sf015` Tachyon Whip : `PlayersCannotChangeForms(NonKeyword, "You",
#    to_form=...)` — ici l'inverse (`to_form=Hero`).
#  - `identity.py:ChangeToOtherIdentityForm` : heros -> alter-ego.
#  - `can_health.py:SetHealth(value, effect)` : « set your hit point dial ».
#  - `br004` : « A or B » sur un COUT = deux capacites. Pour une `Action` (non
#    `Play`) la liste blanche de `factory.py` ne s'applique PAS.
#
# TEXTE CONTRE CODE
#  « Flip to alter-ego form AND you lose 5 hit points » -> DEUX effets a la
#    remise : bascule (si deja en alter-ego, rien a basculer) puis -5 PV. Ce
#    n'est PAS de la degat : pas de prevention possible, pas de Tenace.
#  « If this would defeat your identity, set your hit point dial to 1
#    INSTEAD » -> plancher a 1 : `max(1, pv - 5)`.
#  « You CANNOT change to HERO form » -> `to_form=Hero`, tant que la carte est
#    en jeu. La bascule vers l'alter-ego faite par cette carte n'est pas
#    bloquee (et le test « `effect.this != message.by_effect.this` » du moteur
#    la laisserait passer de toute facon).
#  « Spend [mental][mental] resources OR discard Donatello's Shell from play »
#    -> DEUX capacites AlterEgoAction au meme effet : cout `BB`, ou cout
#    « defausser la Carapace EN JEU » (`from_where=["YouControlCards"]`).
#  « remove Broken Shell FROM THE GAME » -> `RemoveAllFromGame`, pas defausse.


def GetAbilities() -> Sequence['Ability']:

    def remise(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        if Hero.IsType(identite):
            identite.ChangeToOtherIdentityForm(effect)
            identite = joueur.GetIdentity()
        if identite is None:
            return
        identite.SetHealth(max(1, identite.health - 5), effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(remise),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "You",
            to_form=Hero,
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetName("Remove Broken Shell (spend [mental][mental])")
        .SetCost(Cost("BB")),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetName("Remove Broken Shell (discard Donatello's Shell)")
        .SetCostFunc(CostFunc.Discard(
            name=NOM_CARAPACE,
            card_type=Upgrade,
            from_where=["YouControlCards"],
        )),
    ]
