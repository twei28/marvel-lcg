from . import *

# * Dario Agger — SBIRE NEMESIS de Roz. PV 3, SCH 3, ATK 1, boost 2. ROXXON.
# Forced Interrupt: When a player would attack Dario Agger, that player must discard an upgrade or support from
#   their hand or play area. If no card is discarded this way, Dario Agger cannot be defeated by this attack.
# (Roz's nemesis minion.)
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « When X would be attacked » : `AbilityFactory.WhenUnitWouldBeAttacked(ForcedInterrupt, "This", op)`
#    (do_attack.py:880) ; `message.attacker` = l'attaquant.
#  - « cannot be defeated » : `aa016` Death / `16080b` Collector : `*AbilityFactory.UnitCannotBeDefeatedWhile(
#    NonKeyword, "This")`. Ici LIMITE A CETTE ATTAQUE : enregistree en temporaire `until_event_end=message`
#    (`04004` Hawkeye, `tg006` : `this.effect.RegisterTemp(..., unregister_after_exec=False, until_event_end=message)`).
#  - choix d'une carte a defausser : `14015` Side Step (`AskChooseFace(faces, effect)`) + `Faces.DiscardAll`.
#
# MOTS-PIEGES
#  - « THAT PLAYER must discard » : le joueur QUI ATTAQUE (le controleur de l'attaquant, heros OU allie), pas
#    le joueur Roz. Obligatoire, pas un « may ».
#  - « an upgrade OR support FROM THEIR HAND OR PLAY AREA » : les deux zones, deux types.
#  - « IF NO CARD IS DISCARDED THIS WAY » : le joueur n'avait ni amelioration ni soutien, ou la defausse n'a pas
#    eu lieu → Dario ne peut pas etre vaincu PAR CETTE ATTAQUE (il reste a 1 PV au moins ; la protection
#    disparait avec l'attaque).
#  - le 1er attribut : `desc.Nemesis = "Roz"` (set nemesis du deck de depart).
def GetAbilities() -> Sequence['Ability']:

    def avocats_contre_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        attaquant = message.attacker
        controleur = attaquant.GetControlByOrOwner() if attaquant is not None else None
        if not Player.IsType(controleur):
            return
        joueur = controleur
        candidates = [f for f in list(joueur.hand_cards.Get()) + list(joueur.GetControlCards())
                      if f is not None and (Upgrade.IsType(f) or Support.IsType(f))]
        defaussee = False
        if candidates:
            face = joueur.AskChooseFace(candidates, effect)
            if face:
                Faces.DiscardAll([face], effect)
                defaussee = True
        if not defaussee:
            this.effect.RegisterTemp(
                *AbilityFactory.UnitCannotBeDefeatedWhile(AbilityType.NonKeyword, "This"),
                unregister_after_exec=False,
                until_event_end=message,
            )

    return [
        AbilityFactory.WhenUnitWouldBeAttacked(
            AbilityType.ForcedInterrupt,
            "This",
            avocats_contre_attaque,
        ),
    ]
