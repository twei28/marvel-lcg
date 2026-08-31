from . import *

# * Bullseye — sbire nemesis. EARTH-6160. ASSASSIN. PV 6 / SCH 1 / ATK 1*. x2
# Stalwart. Villainous.
# [star] Bullseye's attack gains piercing and overkill.
#
# Cartes de reference :
#  - Stalwart et Villainous : bases automatiques du moteur, lues dans `desc`
#    (fiches mots-cles/stalwart.md et villainous.md, modele 11041 Deathunt
#    9000 qui cumule desc + capacite annexe scriptee) — RIEN a coder ici
#    pour ces deux mots-cles ;
#  - l'etoile : 27078 « Now We're Angry! » (« Venom's attacks gain
#    overkill »), meme fabrique `UnitAttackGainKeyword` avec les drapeaux
#    `piercing`/`overkill` (fiches mots-cles/piercing.md et overkill.md).
#    `attacker="This"` : seul CE Bullseye est concerne, pas les sbires
#    homonymes officiels (56088, 60033).
#
# ⚠ Texte imprime avec deux coquilles (« Villainious », « Bullseyes's »),
# corrigees a la saisie.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            overkill=True,
        ),
    ]
