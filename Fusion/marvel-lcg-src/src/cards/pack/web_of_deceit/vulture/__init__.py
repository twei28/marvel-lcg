from cards.pack.web_of_deceit import *

# Le scenario tourne autour des compteurs « pigeon », qui vivent sur le complot
# PRINCIPAL et non sur une manigance secondaire : ils sont un bouclier, pas une
# menace. Tant qu'il y en a trois, la prochaine tentative de retirer de la
# menace en retire trois a la place — le reseau de surveillance encaisse.


def PigeonsSurLeComplot(effect: 'Effect', combien: int) -> None:
    """« Place N pigeon counters on the main scheme. »"""
    complot = Worlds.FindMainScheme(effect)
    if complot:
        Faces.PlaceCountersOn([complot], combien, 'pigeon', effect)


def LAttaqueEstAerienne(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
    """« unless the attacker or attack has the AERIAL trait, or the attack has
    ranged. »

    La meme clause tient les trois stades de Vulture ; elle est ecrite une fois.

    ⚠ ECART, ecrit : `ranged` est une propriete de l'ATTAQUE, pas d'une carte, et
    la fenetre qui decide si Vulture peut etre CIBLE (`CheckIfUnitCanBeAttackBy`)
    est anterieure a la declaration de l'attaque — la portee n'y existe pas
    encore. Seul le trait AERIAL est donc verifie, sur l'attaquant comme sur la
    carte qui porte l'attaque. C'est la voie que le scenario met en avant : le
    Wingsuit distribue a la mise en place donne justement ce trait.
    """
    attaquant = message.attacker
    if attaquant and attaquant.HasTrait("AERIAL"):
        return True
    source = message.by_effect.this
    return bool(source and source.HasTrait("AERIAL"))


def NePeutEtreAttaqueQueParLesAeriens() -> 'Ability':
    return AbilityFactory.UnitCannotBeAttacked(
        "This",
        conditions=[
            lambda effect, message:
                not LAttaqueEstAerienne(effect, message)
        ],
    )
