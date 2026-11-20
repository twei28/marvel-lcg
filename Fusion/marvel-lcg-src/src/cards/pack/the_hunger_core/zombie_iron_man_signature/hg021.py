from . import *

# Rotten Thrusters — ATTACHMENT (set signature Zombie Iron Man, carte 3/5 : hg019-hg023). Traits TECH, UPGRADE.
# Attach to Zombie Iron Man.
# Zombie Iron Man gets +1 SCH and cannot be attacked by allies.
# Hero Action: Spend 2 resources -> discard this card.
#
# Cartes de reference :
#  - Attache : AUCUNE fabrique « AttachToFaceWhenPutIntoPlay » ici. Cette carte, comme tout le deck signature
#    de Zombie Iron Man, n'est jamais jouee par un joueur depuis une main : elle est attachee directement par
#    `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (`trouvee.CastTo(Attachment).AttachTo2(metazombie,
#    effect)`), appelee par `hg008` a l'entree en jeu de Zombie Iron Man et par `hg023` Hunger Protocol. Le
#    texte imprime « Attach to Zombie Iron Man » decrit donc un fait DEJA accompli par le moteur-scenario, pas
#    une capacite a coder dans CE module.
#  - « +1 SCH » sur l'hote : meme fabrique que `sm/osborn_tech/27149` Kinetic Armor (« Villain gains
#    retaliate 1 », `GiveKeywordToAttached(Villain, retaliate=1)`), ici avec `scheme=1` a la place.
#  - « cannot be attacked by ALLIES » : fabrique `AbilityFactory.UnitCannotBeAttacked` (do_attack.py:990,
#    message `CheckIfUnitCanBeAttackBy`), modele general `sm/osborn_tech/27152` / `sk242` Changing Appearance /
#    `raza/rl014` (cible = `"AttachedVillain"`, `conditions=[...]` sur le message). Le filtre sur le TYPE
#    d'attaquant reprend `wonder_man/58030` (`Ally.IsType(...)`), mais applique a `message.attacker` --
#    champ direct de `CheckIfUnitCanBeAttackBy` (sender.py:116, l'unite qui attaquerait) -- et non
#    `message.trigger`, qui appartient a un AUTRE message (`WhenUnitWouldAttack`).
#  - Cout « Hero Action: Spend 2 resources -> discard this card » : fabrique
#    `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("2"))`, meme fabrique que
#    `sm/osborn_tech/27148` Ionic Boots (`.SetCost(Cost("YBR"))` colore) ; ici `Cost("2")` = cout generique
#    « of any type », modele texte identique a des cartes officielles comme `33241`/`26723`
#    (« Spend N resources of any type »).
#
# A CONFIRMER : le texte imprime ne precise pas explicitement « of any type » (contrairement a certaines
# cartes officielles qui emploient la meme formule) ; par coherence avec le reste du deck signature (hg019
# « Spend 2 resources », hg020 « Spend 3 resources », meme absence de couleur), le cout est traite comme
# generique (`Cost("2")`), aucune couleur n'etant imprimee sur AUCUNE carte signature de ce Metazombie.
#
# Mots-pieges :
#  - « ZOMBIE IRON MAN gets +1 SCH » (lui seul, pas chaque Metazombie : contraste avec `hg007` Zombie Captain
#    America « Each OTHER Metazombie gets +1 ATK ») -- cible = `Villain` via `GiveKeywordToAttached`, qui ne
#    touche QUE l'hote attache (jamais `Metazombies(effect)` globalement).
#  - « cannot be attacked by ALLIES » : seuls les ALLIES sont vises, pas les heros -- la condition filtre
#    STRICTEMENT sur `Ally.IsType(message.attacker)` ; sans ce filtre, un heros serait bloque a tort.
#  - « Hero Action » sur un attachement cote RENCONTRE (attache au Metazombie, pas a un joueur) : disponible a
#    N'IMPORTE QUEL joueur (il n'y a pas de « controleur ») -- modele `27148`/`27149`/`27152`, aucune
#    restriction de joueur codee dans `PlayerActionToDiscardThis`.
#  - Pas de « unless »/« otherwise »/surge dans le texte imprime : rien d'autre a coder.


def GetAbilities() -> Sequence['Ability']:

    def attaquant_est_un_allie(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        Unused(effect)
        return Ally.IsType(message.attacker)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Villain,
            scheme=1,
        ),
        AbilityFactory.UnitCannotBeAttacked(
            "AttachedVillain",
            conditions=[attaquant_est_un_allie],
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2")),
    ]
