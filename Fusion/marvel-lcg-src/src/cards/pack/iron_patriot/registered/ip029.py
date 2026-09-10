from . import *

# * Venom — SBIRE du deck REGISTERED (16/20). 6 PV, ATQ 3, MNG 1, boost 3.
# AVENGER. ELITE. SYMBIOTE.
# Retaliate 1. Toughness.
# While Venom's remaining hit points are less than half his starting hit
#   points, he gets +1 ATK and -1 SCH or -1 THW.
# Symbiotic Devour — Special: This ally attacks a character. This ally takes -1
#   consequential damage if they defeat a character this way.
#
# CARTES DE REFERENCE
#  - `dt018` Feel the Pain / `43019` "Now I'm Mad" : le seuil de points de vie.
#    Le commentaire de `dt018` tranche le vocabulaire : « maximum hit points »
#    lit `max_health`, « STARTING hit points » lit `starting_health`. Venom
#    imprime « starting », donc `starting_health` (can_health.py:9).
#  - `17020` * Cosmo : `message.DoesNotTakeConsequentialDamage(effect)`.
#  - `al014` : `unite.BasicAttack(cibles, effect, if_this_defeat_unit=...)`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « -1 SCH OR -1 THW » : le « ou » n'est pas un choix, c'est une
#    disjonction de FORME. Sbire, Venom a une MNG ; allie, il a une CTR.
#    Les deux ne peuvent PAS partir dans la meme `ThisGainKeyword` : une seule
#    des deux caracteristiques existe sur la face, et `unit.Gain` sort alors
#    sans rien appliquer — Y COMPRIS LE +1 ATQ, qui voyageait avec. Mesure du
#    09/09/2026 : ATQ mesuree 3 au lieu de 4, sur un Venom a 2 PV sur 6.
#    On separe donc en TROIS capacites : le +1 ATQ pour tout le monde, le
#    -1 MNG pour la face de sbire, le -1 CTR pour la face d'allie.
#  ⚠ « LESS THAN half » : strictement. 6 PV de depart, le bonus s'allume a 2
#    PV restants, pas a 3.
#  ⚠ `change_on_event=OnEvent.Health("This")` : sans lui, le bonus ne serait
#    recalcule qu'au prochain evenement venu, et Venom frapperait a 3 alors
#    qu'il vient de tomber sous le seuil.
#  ⚠⚠ « takes -1 CONSEQUENTIAL DAMAGE » : le gabarit `registered_ally` porte
#    une seule etoile de degat consecutif. -1 vaut donc exactement « aucun »,
#    et c'est `DoesNotTakeConsequentialDamage` qui le dit au moteur. On l'arme
#    DANS `if_this_defeat_unit`, c'est-a-dire au moment ou la condition
#    « if they defeat a character this way » devient vraie, et avant que les
#    degats consecutifs ne soient appliques (can_attack.py:225 declenche le
#    rappel bien avant la fin de l'attaque).
#  ⚠ « attacks A CHARACTER » : un personnage, donc un ennemi comme un ami. On
#    laisse le choix ouvert, c'est ce qui est ecrit.
#  ⚠ Retaliate 1 et Toughness sont des BASES NATIVES de sbire, qui tombent a
#    la conversion en allie.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.


def GetAbilities() -> Sequence['Ability']:

    def sous_la_moitie(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Unit2)
        Unused(ui)
        if this is None or this.starting_health <= 0:
            return 0
        return 1 if this.health * 2 < this.starting_health else 0

    def devoration(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        # ⚠ `CastTo(Ally)` et non `Unit2` : `BasicAttack` vit sur `CanAttack`,
        # dont `Ally` herite, pas sur `Unit2`. Le « Special » ne se resout que
        # sur un allie, la conversion est donc toujours faite ici.
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        personnages = [f for f in Worlds.GetOnFieldCharacters(effect)
                       if f is not None and f is not effect.this]
        if this is None or joueur is None or not personnages:
            return
        cibles = joueur.AskChooseFaces(personnages, (1, 1), effect,
                                       prompt="This ally attacks a character")
        if not cibles:
            return

        annonce: List['Message.WhenUnitWouldAttack'] = []

        def retenir(attack_effect: 'Effect',
                    attack_message: 'Message.WhenUnitWouldAttack') -> None:
            Unused(attack_effect)
            annonce.append(attack_message)

        def si_il_tue(vaincu: 'CardFace') -> None:
            Unused(vaincu)
            if annonce:
                annonce[0].DoesNotTakeConsequentialDamage(effect)

        garde = this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "This",
                retenir,
            ),
            unregister_after_exec=False,
        )
        this.BasicAttack(cibles, effect, if_this_defeat_unit=si_il_tue)
        Effects.UnRegister(garde)

    def sous_la_moitie_en_sbire(effect: 'Effect', ui: List['CardFace']) -> int:
        return sous_la_moitie(effect, ui) if Minion.IsType(effect.this) else 0

    def sous_la_moitie_en_allie(effect: 'Effect', ui: List['CardFace']) -> int:
        return sous_la_moitie(effect, ui) if Ally.IsType(effect.this) else 0

    return [
        AbilityFactory.ThisGainKeyword(
            sous_la_moitie,
            attack=1,
            change_on_event=OnEvent.Health("This"),
        ),
        AbilityFactory.ThisGainKeyword(
            sous_la_moitie_en_sbire,
            scheme=-1,
            change_on_event=OnEvent.Health("This"),
        ),
        AbilityFactory.ThisGainKeyword(
            sous_la_moitie_en_allie,
            thwart=-1,
            change_on_event=OnEvent.Health("This"),
        ),
        SpecialRegistered("Symbiotic Devour", devoration),
    ]
