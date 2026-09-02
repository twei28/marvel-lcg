from . import *

# Superdense Strike — evenement signature, x2 (n/15 = 10 et 11).
# ATTACK. SUPERPOWER. Cout 2, ressource [physical]. PAS de Requirement.
# Hero Interrupt: When your hero makes a basic attack against an enemy, she
#   gets +4 ATK for that attack and that attack gains piercing. Give your hero
#   a tough status card.
#
# Cartes de reference :
#  - 56017 Savage Strike (pack cw) : le modele exact du couple bonus+mot-cle
#    sur sa propre attaque de base —
#    `WhenUnitMakeAttack(HeroInterrupt, "You", ..., is_basic_attack=True)
#    .SetPlay().SetLabel()` puis `message.GainATKForThisAttack(N, effect)` et
#    `message.GainPiercing(effect)`. Ecart : Savage Strike donne +6 pour 3, ici
#    +4 pour 2, et Superdense Strike ajoute la carte de statut ;
#  - 05015 Tackle / 01083 Mockingbird pour `Faces.GiveStatus(..., "Tough", ...)`.
#
# ⚠ NE PAS partir de l'homonyme officiel 26009 Superdense Strike (Vision) :
# c'est une Hero Action qui inflige elle-meme 5 degats, pas une Interruption
# sur l'attaque de base, et elle est conditionnee a la forme Dense.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « AGAINST AN ENEMY » : filtre `attack_targets=Enemy` sur la fabrique. Le
#    texte le precise, Savage Strike non — une attaque de base peut viser
#    autre chose qu'un ennemi (un allie du camp adverse en competitif, par
#    exemple), le mot imprime est donc code.
#  - « for THAT attack » : `GainATKForThisAttack`, borne a l'attaque en cours,
#    et non un `GainUntilPhaseEnd`.
#  - « THAT ATTACK gains piercing » : le mot-cle est sur l'ATTAQUE, jamais sur
#    le personnage. `message.GainPiercing(effect)` sur le message de NOTRE
#    attaque — le meme appel sur le message d'une attaque ENNEMIE donnerait
#    piercing a l'ennemi (piege documente sur ag005, cf. mots-cles/ranged.md,
#    meme famille).
#  - « Give YOUR HERO a tough status card » : le heros, c'est-a-dire
#    l'attaquant (`message.attacker`), pas la carte ni un allie. La phrase est
#    une TROISIEME phrase, sans « → » : ce n'est pas un cout, c'est un effet,
#    et il s'applique meme si l'attaque ne fait aucun degat.
#  - « she gets » : le pronom feminin designe Viv. Aucune consequence de code,
#    mais il confirme que la carte parle du heros et non de la carte.
#  - Aucun Requirement imprime sur cette carte, contrairement a vv002, vv004,
#    vv005 et vv009 : ne pas en inventer un (`desc` n'a pas la cle).


def GetAbilities() -> Sequence['Ability']:

    def superdense_strike(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GainATKForThisAttack(4, effect)
        message.GainPiercing(effect)

        heros = message.attacker
        if heros is not None:
            Faces.GiveStatus([heros], "Tough", effect)

    return [
        # ⚠ `WhenUnitMakeAttack` (le raccourci qu'emploie 56017) N'EXPOSE PAS
        # `attack_targets` : le parametre est commente dans sa signature
        # (do_attack.py:84). On appelle donc directement `WhenUnitWouldAttack`,
        # vers laquelle il delegue de toute facon, pour pouvoir coder le
        # « against an enemy » imprime.
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            superdense_strike,
            is_basic_attack=True,
            attack_targets=Enemy,
        ).SetPlay().SetLabel(),
    ]
