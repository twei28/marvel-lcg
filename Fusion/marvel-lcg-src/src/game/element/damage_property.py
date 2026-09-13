from core import *

@dataclass
class DamageProperty:
    damage: int = field(default=0)
    ignore_tough: bool = field(default=False)
    is_from_overkill: bool = field(default=False)
    is_indirect_damage: bool = field(default=False)
    # CORRECTIF (12/09/2026) : « unpreventable damage ».
    #
    # Le moteur n'avait AUCUN moyen de le dire. Les deux cartes officielles qui
    # emploient le mot (62001a Luke Cage, 62028 Internal Injury) s'en tiraient
    # avec `ignore_tough`, qui ne couvre qu'une seule forme de prevention : la
    # carte Coriace. Toutes les autres passaient au travers.
    #
    # Le pack `sentinel` a rendu le trou visible et NUISIBLE. Son mot-cle maison
    # DESTROY inflige « 2 degats imblocables », et son heros porte « Interrupt :
    # quand vous devriez subir n'importe quelle quantite de degats, detruisez
    # plutot une amelioration COMPONENT ». Sans ce drapeau, les 2 degats de la
    # destruction declenchaient a leur tour l'interruption : le robot se
    # demontait entierement d'un seul coup de sbire (mesure du 12/09/2026, cas
    # st015 : quatre pieces retournees pour une attaque a 2).
    #
    # Honore par `Message.WhenUnitWouldTakeDamage` : ni `PreventDamage`, ni
    # `SetBeInstead`, ni Coriace n'y touchent.
    unpreventable: bool = field(default=False)

    def Copy(self) -> 'DamageProperty':
        return DamageProperty(
            damage=self.damage,
            ignore_tough=self.ignore_tough,
            is_from_overkill=self.is_from_overkill,
            is_indirect_damage=self.is_indirect_damage,
            unpreventable=self.unpreventable
        )

