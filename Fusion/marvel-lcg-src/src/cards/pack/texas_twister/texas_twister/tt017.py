from . import *

# * Phantom Rider (Hamilton Slade) — ALLIE BASIC, cout 3, PV 3,
#   CTR 1* / ATQ 2*. RANGER. [wild].
# Phantom Rider takes -1 consequential damage after he ingores [sic] the guard
#   and patrol keywords, and any crisis icons ([crisis]) in play.
#
# ⚠ TEXTE IMPRIME FAUTIF, ET LA LECTURE RETENUE. Le scan porte « ingores »
# pour « ignores », et la phrase colle deux effets sans conjonction. Deux
# lectures sont possibles : (a) il ignore Garde/Patrouille/Crise, ET il subit
# 1 degat consequent de moins ; (b) la reduction ne vaut que lors des usages
# ou il ignore effectivement quelque chose. (b) est inapplicable — le moteur
# ne signale pas « une exemption a servi » — et rendrait la carte muette la
# plupart du temps. C'est donc (a), la lecture litterale des deux effets.
# Question posee a l'auteur.
#
# MOTS-CLES : GUARD, PATROL, CRISIS — fiches lues avant d'ecrire. Les trois
# sont des BASES AUTOMATIQUES du moteur (`desc.Guard`, `desc.Patrol`,
# `desc.Crisis`) : rien a recoder, seulement a IGNORER. Crise se joue dans
# `RemoveThreatFromSchemes` lui-meme, via son parametre `ignore_crisis`.
#
# CARTE DE REFERENCE
#  - `as012` Night Vision (pack armored_spidey) : `UnitIgnoreKeywordIcons`,
#    et surtout LA LEÇON PAYEE — `which_unit` doit etre un `CardFinder(name=)`,
#    JAMAIS `"You"`. Le moteur convertit `"You"` en `"This"` puis le compare a
#    `effect.this`, qui est la carte porteuse : la comparaison echoue toujours
#    et l'exemption ne s'applique jamais. Mesure du 03/09/2026.
#  - `dt035` Gladiator : `ThisGainKeyword(..., attack_consequential_damage=-N,
#    thwart_consequential_damage=-N)`.
#
# TEXTE CONTRE CODE
#  « GUARD AND PATROL keywords, AND any CRISIS icons » -> les TROIS, ce qui
#    est rare : `as012` n'en prend que deux et son commentaire previent de ne
#    pas copier le modele au-dela du texte. Ici le texte les cite bien tous.
#  « takes -1 CONSEQUENTIAL damage » -> les DEUX pouvoirs, attaque et contre :
#    le texte ne distingue pas, contrairement a tt014 Firebird qui ne parle
#    que du contre.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.ThisGainKeyword(
            attack_consequential_damage=-1,
            thwart_consequential_damage=-1,
        ),
        AbilityFactory.UnitIgnoreKeywordIcons(
            CardFinder(name="Phantom Rider"),
            guard=True,
            patrol=True,
            crisis=True,
        ),
    ]
