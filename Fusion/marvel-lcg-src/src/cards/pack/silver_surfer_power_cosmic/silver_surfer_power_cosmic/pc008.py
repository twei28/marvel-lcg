from . import *

# Cosmic Blast — EVENEMENT. ATTACK. POWER COSMIC. Cout 2, ressource [energy].
# x2 (pc008 (x2 exemplaires), meme carte).
#
# Texte imprime : « Hero Response (attack): After Silver Surfer departs a
# PLANET, deal 5 damage to an enemy. If that PLANET was Sakaar, this attack
# gains piercing and you may spend a [energy] resource to ready Silver
# Surfer. »
#
# CARTES DE REFERENCE
#  - `19007` Payback (drax) : `AbilityFactory.AfterUnitAttackUnit(HeroResponse,
#    ...).SetPlay().SetLabel('attack').SetTarget(Villain)` — gabarit d'un
#    EVENEMENT joue EN REPONSE a un declencheur (pas une carte deja en jeu).
#  - `ls005` To Arms! (lady_sif) : `initiator.MayChooseOneAbility(effect,
#    AbilityFactory.ForChoiceAbilityWithCost(Cost("1"), "Ready your hero",
#    lambda cibles, res: Faces.ReadyAll([heros], effect)))` — « you MAY spend
#    N resource to ready ».
#  - helper `EstSilverSurfer` (__init__.py du pack) : filtre « After SILVER
#    SURFER departs », pas n'importe quel personnage (Nova Frankie Raye
#    aussi « departs a planet », mais ce n'est jamais elle que ce texte vise).
#  - `bl005.py` Vampire Bite : `AttackProperty(piercing=...)` pour
#    « this attack gains piercing ».
#
# TEXTE CONTRE CODE
#  « After SILVER SURFER departs a PLANET » : EstSilverSurfer(message.
#    character_face), jamais Nova Frankie Raye ni un allie.
#  « deal 5 damage to AN ENEMY » : cible choisie (`.SetTarget(Enemy)`).
#  « If that PLANET was Sakaar » : `message.planet_face` card_id == 'pc005'.
#  « this attack gains piercing » : seulement dans la branche Sakaar, pas par
#    defaut.
#  « you MAY spend a [energy] resource to ready » : facultatif
#    (`MayChooseOneAbility`), cout `Cost("Y")` (energie), seulement si Sakaar.


def GetAbilities() -> Sequence['Ability']:

    def est_silver_surfer_qui_part(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> bool:
        Unused(effect)
        return EstSilverSurfer(message.character_face)

    def cosmic_blast(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        this = effect.this.CastTo(Event)
        if not effect.targets:
            return
        depuis_sakaar = getattr(message.planet_face.paper, "card_id", None) == "pc005"
        this.DealDamage(effect.targets, 5, effect, property=AttackProperty(piercing=depuis_sakaar))

        if depuis_sakaar:
            joueur = JoueurDeCetteCarte(effect)
            if joueur is None:
                return
            silver_surfer = joueur.GetIdentity()
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbilityWithCost(
                    Cost("Y"),
                    "Ready Silver Surfer",
                    lambda cibles, res: Faces.ReadyAll([silver_surfer], effect),
                ),
            )

    return [
        Ability(
            AbilityType.HeroResponse,
            Message.AfterCharacterDepartPlanet,
            [est_silver_surfer_qui_part],
            cosmic_blast,
        ).SetPlay().SetLabel('attack').SetTarget(Enemy),
    ]
