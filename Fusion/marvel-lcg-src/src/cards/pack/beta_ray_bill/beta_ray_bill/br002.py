from . import *

# Eye of the Storm — EVENEMENT, cout X, [mental]. SUPERPOWER. x2.
# Hero Action: Spend X [energy] resources and choose a player -> remove X
#   threat from each scheme in play. That player engages up to X minions in
#   play. This action ignores the crisis icon if you have the [[AERIAL]] trait
#   or used Stormbreaker to pay for this card.
#
# CARTES DE REFERENCE
#  - `14006` Speed Cyclone : le cout X, lu par `effect.GetCostX()`. Le X vit
#    dans `desc.Cost` et le moteur le gere seul.
#  - `42006` Natural Flight (pack angel) : `.SetIgnoreKeyword('Crisis', ...)`
#    avec une `condition=` — c'est la SEULE facon d'ignorer la crise sur une
#    capacite donnee.
#  - `dz036` (pack dazzler) : lire QUELLE carte a paye, via
#    `paid_this_res_effects` (helper `MarteauAPaye`).
#
# MOT-CLE : CRISIS — fiche `docs/reference/mots-cles/crisis.md`. Le blocage
# vit dans `RemoveThreatFromSchemes` lui-meme, via son parametre
# `ignore_crisis` que `SetIgnoreKeyword` alimente. Rien a recoder.
#
# ⚠ ECART ASSUME : « Spend X [ENERGY] resources ». `desc.Cost` ne connait que
# `"X"` (16 cartes du depot) et `"R"` (une seule, `10002` Crushing Blow), mais
# PAS de X type : aucune carte du jeu ne combine les deux. Le joueur paie donc
# X ressources de n'importe quel type. L'ecart est en sa faveur, et il est
# signale ici plutot que masque.
#
# TEXTE CONTRE CODE
#  « remove X threat from EACH SCHEME IN PLAY » -> toutes les manigances, pas
#    une choisie : c'est le nettoyeur du pack.
#  « THAT PLAYER engages up to X minions » -> le joueur CHOISI, qui n'est pas
#    forcement vous. En solo la distinction ne se voit pas ; a plusieurs, si.
#  « UP TO X » -> le joueur peut en prendre moins, y compris zero.
#  « if you have the AERIAL trait » -> br010 Stormbreaker l'accorde justement.
#    Les deux moities de la condition passent donc par le marteau.


def GetAbilities() -> Sequence['Ability']:

    def a_le_vol_ou_le_marteau(effect: 'Effect') -> bool:
        """« if you have the AERIAL trait OR used Stormbreaker to pay »."""
        heros = HerosDuJoueur(effect)
        if heros is not None and heros.HasTrait("AERIAL"):
            return True
        return MarteauAPaye(effect)

    def oeil_du_cyclone(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        x = effect.GetCostX()
        if x <= 0:
            return

        manigances = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                      if s.threat > 0]
        if manigances:
            this.RemoveThreatFromSchemes(manigances, x, effect)

        def engager(joueur_vise: 'Player') -> None:
            libres = [m for m in Worlds.FindCardsOnField(effect, card_type=Minion)
                      if m.CastTo(Minion).GetEngagedPlayer() is not joueur_vise]
            for sbire in libres[:x]:
                sbire.CastTo(Minion).EngagePlayer(joueur_vise, effect)

        Players.ForEachTargets(effect.targets, engager)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            oeil_du_cyclone,
        ).SetPlay()
        .SetTarget("Players")
        .SetIgnoreKeyword('Crisis', condition=a_le_vol_ou_le_marteau),
    ]
