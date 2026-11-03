from . import *

# * Spider-Man (Peter Parker) : ALLIE (WEB-WARRIOR), cout 4, [physical]. Classe Hero. THW 2 (consecutif), ATK 2 (consecutif), PV 4.
# Interrupt: When you would take any amount of damage from resolving Carnage's "Need to Kill" ability, exhaust Spider-Man and deal 1 damage to him -> prevent all of that damage.
#
# CARTES DE REFERENCE
#  - « When X would take damage -> prevent all » : `im012` (Hulkbuster) : `WhenUnitWouldTakeDamage(Interrupt, "You", op)` + `message.PreventDamage("All", effect)`.
#  - Declencheur lie a UNE capacite nommee : `ma002` / `mt001a` : `effect.ability.name` compare a la chaine posee par `.SetName()` (ici « Need to Kill », ca001a), lue sur `message.by_effect`.
#  - « exhaust X and deal 1 damage to him → » : les deux dans le COUT : `22012` (`CostFunc.DealDamage(1, "This")`) + `CostFunc.Exhaust("This")`.
#
# TEXTE CONTRE CODE
#  « Interrupt » NU : jouable dans les deux formes. « When YOU would take any amount of damage FROM RESOLVING Need to Kill » : seuls les degats de CETTE capacite (nom lu sur l'effet source), jamais une attaque ou un autre effet ; « you » = l'identite du joueur.
#  « exhaust Spider-Man AND deal 1 damage to him → » : deux couts ; ni l'un ni l'autre possible (deja epuise) = pas d'Interruption. « prevent ALL of that damage » : `PreventDamage("All")`.
#  Chiffres : cout 4, PV 4, un degat paye par Spider-Man.
#  ⚠ A RELIRE SUR LE SCAN : les notes de lecture marquent le PV de Spider-Man « non imprime lisible » ; `data/cards.json` porte 4.


NOM_NEED_TO_KILL_CA002 = "Need to Kill"


def GetAbilities() -> Sequence['Ability']:

    def degats_de_need_to_kill(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(effect)
        # ⚠ `by_effect` n'est pas toujours un effet de carte : une attaque ennemie ou une regle de jeu (`GameRule`) n'a PAS d'attribut `ability`
        # (AttributeError avale, vu en autoplay le 03/11 sur les degats d'une attaque de Rhino).
        source = message.by_effect
        ability = getattr(source, "ability", None)
        return ability is not None and getattr(ability, "name", None) == NOM_NEED_TO_KILL_CA002

    def spider_man(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        Unused(effect)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            spider_man,
            conditions=[degats_de_need_to_kill],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
