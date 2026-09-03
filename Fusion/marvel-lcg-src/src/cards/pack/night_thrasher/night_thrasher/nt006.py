from . import *

# Melon Grab — evenement signature, x1 (n/16 = 9). ATTACK. SKILL.
# Cout 3, ressource [physical].
# Hero Action (attack): Deal 8 damage to an enemy. If the Battle Board upgrade
#   has the:
#   • [[VEHICLE]] trait, damage from this attack can be divided among enemies
#     as you choose.
#   • [[WEAPON]] trait, this attack gains piercing and overkill.
#
# Cartes de reference :
#  - **`im002`** Repulsor Barrage (pack iron_man_model_42) : MEME structure —
#    des degats de base, puis une repartition libre conditionnee a un etat du
#    plateau. `player.AssignDamage(cibles, source, total, effect)` (modele
#    `27071` Sand Storm) fait CHOISIR au joueur comment repartir un total.
#  - `27078` / `ho016` pour `AttackProperty(piercing=True, overkill=True)`.
#  - `05015` Tackle pour l'evenement d'attaque a libelle.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **8 damage** » pour un cout de 3 : c'est la plus grosse frappe du pack,
#    et c'est bien ce qui est imprime. Ne pas « corriger » a la baisse.
#  - « damage from this attack **can be** divided » : la repartition est
#    FACULTATIVE et libre. `AssignDamage` couvre les deux, le joueur pouvant
#    tout mettre sur une seule cible.
#  - Les deux branches sont EXCLUSIVES : une planche ne porte jamais les deux
#    traits. Sans planche, les 8 degats tombent sur la cible unique, sans
#    mot-cle — c'est le cas de base, pas un oubli.
#  - ⚠ ECART ASSUME, identique a celui d'`im002` : `AssignDamage`
#    (player_action.py:93) n'accepte PAS de `property`, donc la branche
#    VEHICLE ne peut porter aucun mot-cle d'attaque. Elle n'en a pas a porter
#    ici — c'est la branche WEAPON qui donne percant et deferlement — donc
#    l'ecart est SANS consequence sur cette carte, contrairement a im002.
#  - « **(attack)** » : le libelle livre la carte a Sonne. Un seul `SetLabel`.


def GetAbilities() -> Sequence['Ability']:

    def melon_grab(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        if PlancheEstVehicule(effect):
            joueur = effect.GetInitiator()
            ennemis = Worlds.GetOnFieldEnemies(effect)
            if joueur is not None and ennemis:
                joueur.AssignDamage(list(ennemis), this, 8, effect)
                return

        if PlancheEstArme(effect):
            this.DealDamage(effect.targets, 8, effect,
                            property=AttackProperty(piercing=True, overkill=True))
            return

        this.DealDamage(effect.targets, 8, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            melon_grab,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
