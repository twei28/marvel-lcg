from . import *

# Repulsor Barrage — evenement signature, x2 (n/15 = 1 et 2).
# ATTACK. SUPERPOWER. Cout 2, ressource [energy].
# Hero Action (attack): Deal 3 damage to an enemy. This attack gains ranged.
#   You may remove 1 reactor counter from Iron Man to deal 3 additional damage
#   to that enemy. If Iron Man has the AERIAL trait, you may divide damage
#   among enemies as you choose.
#
# Cartes de reference :
#  - `01053` Relentless Assault / `hk006` pour l'evenement d'attaque a
#    `AttackProperty` ;
#  - **`27071` Sand Storm** pour la repartition libre :
#    `player.AssignDamage(cibles, source, total, effect)`, qui fait CHOISIR au
#    joueur comment repartir un total ;
#  - `50134` / `ho010` pour le « you may » paye
#    (`MayChooseOneAbility`) ;
#  - `RetirerUnReacteur` (helper du set) pour le cout en compteur.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **You MAY** remove 1 reactor counter » : facultatif. Et c'est un COUT,
#    donc les 3 degats supplementaires ne tombent que si le compteur a
#    reellement ete retire — d'ou le RETOUR de `RetirerUnReacteur`, jamais une
#    supposition. Sans compteur, la carte fait 3, pas 6.
#  - « to **that** enemy » : les 3 degats supplementaires vont sur la MEME
#    cible, pas sur une seconde. C'est le mot-piege `that <nom>`.
#  - « **If** Iron Man has the AERIAL trait » : condition d'EFFET lue au
#    moment de la resolution, pas au moment du paiement. im004 Take Flight et
#    im010 Rocket Boots sont les deux sources du trait.
#  - « you may **divide** damage among enemies » : la repartition est
#    FACULTATIVE et libre. `AssignDamage` couvre les deux : le joueur peut
#    tout mettre sur une seule cible.
#  - ⚠ ECART ASSUME : `AssignDamage` (player_action.py:93) n'accepte PAS de
#    `property`, donc la branche AERIAL ne porte pas le mot-cle `ranged`. La
#    branche normale, elle, le porte. La difference ne se voit que face a une
#    Riposte. Signale plutot que masque.


def GetAbilities() -> Sequence['Ability']:

    def repulsor_barrage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        degats = 3

        # « You MAY remove 1 reactor counter ... to deal 3 additional damage »
        if CompteursReacteur(identite) >= 1:
            choix = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 reactor counter to deal 3 additional damage",
                    lambda cibles: None,
                ),
            )
            if choix is not None and RetirerUnReacteur(identite, effect):
                degats += 3

        if identite.HasTrait("AERIAL"):
            ennemis = Worlds.GetOnFieldEnemies(effect)
            if ennemis:
                joueur.AssignDamage(list(ennemis), this, degats, effect)
                return

        this.DealDamage(effect.targets, degats, effect,
                        property=AttackProperty(ranged=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            repulsor_barrage,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
