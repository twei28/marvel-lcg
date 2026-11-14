from . import *

# * Deathbird (I) — MECHANT, stade 1 (Majestrix's Verdict). SHI'AR. PV 16[per_hero], MNG 2, ATQ 2[star].
# [star] Forced interrupt: When Deathbird initiates an attack against you, if you control a STARJAMMER
#   ally, she attacks that ally instead with +1 ATK.
#
# Cartes de reference :
#  - « attacks that ally instead » : `WhenUnitWouldAttack(ForcedInterrupt)` + `message.ReplaceTarget(allie)`,
#    modele OFFICIEL 50089b Extract Captives (« When an enemy attacks, it attacks a Rescued Captive instead »).
#    Le moteur sait deja qu'un ennemi attaque un allie : ce n'est PAS la brique commune « un ennemi attaque un
#    ennemi » (attaque initiee par un effet), seulement une cible remplacee.
#  - « with +1 ATK » : `GainATKForThisAttack(1)` (sender_damage.py), le bonus ne vaut que pour CETTE attaque.
#  - l'etoile en exposant de l'ATQ renvoie a ce texte (convention Skrull Menace validee) : ATK = "2".
#
# ⚠ Mots-pieges : « initiates an attack AGAINST YOU » (l'attaque vise l'identite d'un joueur : une attaque
# deja dirigee vers un allie ne declenche rien) ; « if YOU control » (un STARJAMMER d'un AUTRE joueur ne
# compte pas) ; « THAT ally » (un des STARJAMMER de ce joueur, choisi par lui s'il en a plusieurs).


def GetAbilities() -> Sequence['Ability']:
    return [AttaqueDetourneeVersStarjammer(bonus_atq=1)]
