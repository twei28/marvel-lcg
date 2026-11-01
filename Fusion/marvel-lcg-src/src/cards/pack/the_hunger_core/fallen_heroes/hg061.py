from . import *

# Zombie Giant-Man — METAZOMBIE (Fallen Heroes, modulaire). AVENGER. SCH 0. ATK 3. HP 8.
# Guard. Overkill.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) : cle native `desc.Guard`, aucun script -- meme statut que hg059.
#  - « Overkill » (mot-cle officiel, fiche mots-cles/overkill.md) : contrairement a Guard/Toughness/
#    Retaliate/Villainous, Overkill N'EST JAMAIS lu depuis une cle `desc` (confirme : `data/cards_custom.json`
#    n'a pas de cle « Overkill » sur cette carte, et la fiche precise que la propriete `overkill` de
#    `can_attack.py` ne se donne QUE statiquement (fabriques `DoAttack`, reservees aux cartes JOUEUR) ou
#    dynamiquement (`message.GainOverKill(effect)` sur le message d'attaque). Un ennemi qui a Overkill EN
#    PERMANENCE suit donc la voie dynamique, degainee a CHAQUE attaque : modele EXACT `hg009` Zombie Hulk
#    (Horde deck, meme scenario) -- `AbilityFactory.WhenUnitWouldAttackUnit(ForcedInterrupt, "This",
#    CardFinder(card_type=Identity|Ally), toujours_overkill)` ou `toujours_overkill` appelle
#    `message.GainOverKill(effect)`. hg061 est un Minion (pas un Villain comme hg009) mais la fabrique et le
#    message sont generiques a tout attaquant (`Unit2`/`CanAttack`) : aucune adaptation necessaire au-dela
#    du changement de type de `effect.this`.
#
# ⚠ Mots-pieges :
#  - « Overkill » SANS restriction imprimee : TOUTE attaque de Zombie Giant-Man (contre l'identite OU contre
#    une alliee defenseuse) gagne l'exces -> filtre `CardFinder(card_type=Identity|Ally)`, pas seulement
#    Ally -- meme piege deja documente sur hg009.
#  - Overkill n'est PAS une cle `desc` qu'on aurait simplement oubliee de poser dans `cards_custom.json` :
#    c'est le fonctionnement NORMAL du mot-cle pour tout ennemi qui l'a de facon permanente (aucune carte
#    officielle de vilain/sbire ne l'imprime nue avec une cle `desc.Overkill`, grep confirme dans la fiche).
#    Rien a signaler comme bug de donnees ici, a la difference de hg062/hg063 (Quickstrike, voir ces fichiers
#    et le rapport de fin de travail).
#  - L'exces d'une attaque de Zombie Giant-Man contre une ALLIE va a l'IDENTITE du joueur qui la controle
#    (regle du livret RR 1.8 p.31, `CanAttack.DefaultOverkillTarget`) ; contre l'IDENTITE elle-meme (aucune
#    alliee en defense), rien ne peut deborder plus loin (un joueur ne peut pas etre « overkill » au-dela de
#    0 PV, `TakeDamageWithOverkillTarget` s'arrete nativement) -- pas de garde a ecrire, deja gere par le
#    moteur, meme lecture que hg009.
#
# Bloc nombres texte <-> code : SCH 0 / ATK 3 / HP 8 / Guard 1 -> `desc` ; aucune valeur numerique propre au
# script (Overkill ne porte pas de nombre imprime, juste la mention du mot-cle).


def GetAbilities() -> Sequence['Ability']:

    def toujours_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "This",
            CardFinder(card_type=Identity | Ally),
            toujours_overkill,
        ),
    ]
