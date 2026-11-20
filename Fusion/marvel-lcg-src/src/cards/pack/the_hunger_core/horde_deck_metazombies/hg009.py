from . import *

# Zombie Hulk — METAZOMBIE (Horde deck). GAMMA. SCH 0. ATK 4. PV 15[per_hero].
# Overkill.
# Devour — Forced Response: After Zombie Hulk defeats an ally, he heals damage equal to that ally's maximum
# hit points.
#
# Cartes de reference :
#  - « Overkill » (mot-cle officiel, fiche mots-cles/overkill.md) : AUCUN vilain officiel ne le porte en
#    texte imprime nu (grep `data/cards.json` sur `"Overkill."` : aucun resultat), ce n'est donc PAS un
#    attribut natif lu depuis `desc` (contrairement a Toughness/Restricted). La fiche precise les DEUX voies
#    de la mecanique : statique (parametre `overkill=True` des fabriques `DoAttack`, reservees aux cartes
#    JOUEUR) et dynamique (`message.GainOverKill(effect)` sur le message d'attaque, modele `an013` Hel-Wolf
#    « this attack gains overkill » cote boost). Un vilain qui a Overkill en PERMANENCE (pas un boost) prend
#    donc la voie dynamique, degainee a CHAQUE attaque : modele `40074b` Harpoon (Marauders), qui appelle
#    `message.GainOverKill(effect)` sur `WhenUnitWouldAttackUnit` (ForcedInterrupt).
#  - « Devour — After Zombie Hulk defeats an ally, he heals damage equal to that ally's maximum hit points » :
#    `AbilityFactory.AfterUnitDefeatedUnit(ForcedResponse, who_killer="This", who_be_defeated=Ally, op)` (voir
#    PROCESSUS-CARTE.md §7 point 8 : la legon Angela sur `AfterUnitDefeatedUnit`/`LimitOncePerRound`, qui
#    confirme que c'est bien la fabrique native pour « apres que CETTE carte vainc une autre carte », a
#    distinguer de `WhenUnitBeDefeated`/`WhenUnitWouldBeDefeated` qui ecoutent cote VICTIME) ; le soin lui-meme,
#    `this.HealHealth(valeur, effect)` (`CanHealth.HealHealth`, native).
#
# ⚠ Mots-pieges :
#  - « Overkill » SANS restriction imprimee : toute attaque de Zombie Hulk (pas seulement contre un allie)
#    gagne l'excedent -> `WhenUnitWouldAttackUnit` filtre sur `CardFinder(card_type=Identity|Ally)` (les deux
#    cibles possibles d'une attaque de vilain), pas seulement Ally.
#  - « defeats an ALLY » (Devour) : seulement Ally, PAS l'identite (contrairement a Overkill ci-dessus) :
#    `who_be_defeated=Ally` exclusivement.
#  - « heals damage equal to that ally's MAXIMUM hit points » : `max_health` de la cible, PAS ses degats subis
#    ni ses PV imprimes bruts (qui peuvent differer si l'allie portait un bonus de PV) ; lu sur `message.target`
#    APRES la defaite (le message `AfterUnitDefeatedUnit` le porte encore, `max_health` est une propriete
#    stable de la face, pas remise a zero en quittant le jeu).
#  - « HE heals » (Zombie Hulk lui-meme, pas un allie du Coeur ni le Coeur) : `effect.this`, pas `message.target`.
#  - `HealHealth` ne fait rien si `this` n'est plus en jeu (`IsInPlay()` natif) : pas de garde supplementaire a
#    coder (ex. Zombie Hulk lui-meme vaincu dans le MEME coup que l'allie -> aucun soin, deja couvert).


def GetAbilities() -> Sequence['Ability']:

    def toujours_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    def devour(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Villain)
        allie_vaincu = message.target
        this.HealHealth(allie_vaincu.max_health, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt, "This", CardFinder(card_type=Identity | Ally), toujours_overkill,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse, "This", Ally, devour,
        ),
    ]
