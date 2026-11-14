from . import *

# Steel Serpent — COMPLOT ANNEXE nemesis d'Iron Fist (N 5/5). Menace de depart 4[per_hero]. Icone Acceleration.
#   2 icones de boost.
# Forced Interrupt: When Davos attacks, discard a Crane Daughter tucked under him or defeat a Crane Daughter in play
#   → Davos gets +3 ATK for this attack.
#
# MOTS-CLES : acceleration (fiche acceleration.md : `desc.Acceleration`, natif), tuck (tuck.md).
#
# CARTES DE REFERENCE
#  - « gets +N ATK for this attack » : `fne/60004` Heightened Hearing (`GainForThisActive(effect, message, attack=...)`).
#  - vaincre par effet : `Faces.DefeatUnits`.
#
# TEXTE CONTRE CODE
#  ⚠ COUT avant la fleche : sans Crane Daughter (ni dessous ni en jeu), pas de +3.
#  ⚠ « discard ... OR defeat » : quand les deux sont possibles, le joueur attaque choisit.
#  ⚠ « DISCARD a tucked » : vers la defausse de rencontre, pas melangee. « DEFEAT in play » : son « When Defeated » la
#    melange dans le deck.
#  ⚠ Davos EN JEU seulement, toute attaque de Davos (activation ou Quickstrike d'un autre effet).

DEFAUSSER = "Discard a Crane Daughter tucked under Davos"
VAINCRE = "Defeat a Crane Daughter in play"


def GetAbilities() -> Sequence['Ability']:

    def davos_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attaquant = message.trigger
        if attaquant is None or not attaquant.IsInPlay() or attaquant.paper.name.lstrip("* ") != NOM_DAVOS:
            return False
        return bool(CranesSous(attaquant) or CranesEnJeu(effect))

    def serpent_d_acier(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        davos = message.trigger
        dessous = CranesSous(davos)
        en_jeu = CranesEnJeu(effect)
        if dessous and en_jeu:
            joueur = message.against_player if Player.IsType(message.against_player) else effect.world.GetCurrentPlayer()
            choix = joueur.AskChooseOneText([DEFAUSSER, VAINCRE])
        else:
            choix = DEFAUSSER if dessous else VAINCRE
        if choix == DEFAUSSER:
            Faces.DiscardAll([dessous[0]], effect)
        else:
            Faces.DefeatUnits([en_jeu[0]], None, effect)
        davos.CastTo(Unit2).GainForThisActive(effect, message, attack=3)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            None,
            serpent_d_acier,
            conditions=[davos_attaque],
        ),
    ]
