from . import *

# Demonic Limbs — ATTACHEMENT NEMESIS. +1 ATQ.
# Attach to Master Pandemonium. If you cannot, stun a character you control
#   and confuse a character you control.
# Master Pandemonium cannot take damage.
# Hero Action: Spend [energy][energy] resources -> discard this card.
#
# CARTES DE REFERENCE
#  - `04117` Defensive Programming et `02019` Goblin Glider : LE montage d'un
#    attachement de rencontre — `AttachToFaceWhenPutIntoPlay(...)` avec sa
#    clause `if_cannot_operation`, et `PlayerActionToDiscardThis(...)
#    .SetCost(Cost("YY"))` pour la sortie payante. ⚠ `CanAttachToCard`
#    N'EXISTE PAS : c'etait une API inventee, que `test_cards` a sortie.
#  - `bk018` Timebroker : `UnitCannotTakeDamage`.
#
# TEXTE CONTRE CODE
#  « ATTACH TO MASTER PANDEMONIUM. IF YOU CANNOT, ... » -> la clause de repli
#    n'est PAS decorative : Portal to Hell revele l'attachement meme quand le
#    sbire n'est pas en jeu, et c'est le cas frequent. Sans elle, la carte
#    serait inerte la moitie du temps.
#  « STUN a character AND CONFUSE a character » -> DEUX cartes de statut, et
#    rien n'oblige a viser le meme personnage. Le texte dit « a character »
#    deux fois.
#  « MASTER PANDEMONIUM cannot take damage » -> l'effet vise l'HOTE, pas
#    l'attachement : `UnitCannotTakeDamage` sur la carte accrochee. Tant que
#    les membres sont la, le sbire est intouchable, et le seul moyen de le
#    frapper est de payer les deux energies.
#  « +1 ATK » est imprime en `desc`, lu nativement : rien a coder.


def GetAbilities() -> Sequence['Ability']:

    def faute_de_demon(effect: 'Effect', joueur: 'Player') -> None:
        """La clause de repli : « If you cannot [attach], stun a character you
        control and confuse a character you control. »

        ⚠ ELLE PASSE PAR `if_cannot_operation`, le point d'entree prevu par la
        fabrique (asset.py:151) : elle n'est appelee QUE si aucune cible
        legale n'a ete trouvee. Ecrire le test a la main sur `Hote(this)`
        apres coup marcherait aussi, mais dupliquerait une decision que le
        moteur vient de prendre.
        """
        if joueur is None:
            return
        def sous_controle(_effect: 'Effect', face: 'CardFace') -> bool:
            """⚠ `SetTarget` N'A PAS DE `control_by=` (ability.py:701) : le
            passer leve `TypeError: unexpected keyword argument`. Le filtre de
            controle se fait par `check_fn`."""
            Unused(_effect)
            return face.GetControlByOrOwner() is joueur

        for statut in ("Stunned", "Confused"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Give %s to a character you control" % statut,
                    lambda cibles, statut=statut: Faces.GiveStatus(cibles, statut, effect),
                ).SetTarget(Friend, check_fn=sous_controle),
            )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_PANDEMONIUM, card_type=Minion),
            if_cannot_operation=faute_de_demon,
        ),
        # ⚠ `"Attached"` N'EST PAS UN `CardTypeMin` : `Condition.CheckWhichCard`
        # tombe sur `assert not isinstance(check_rule, Sequence)`
        # (card_type.py:247) a chaque degat inflige a n'importe qui. Le moteur
        # avale l'exception, mais la prevention ne s'applique jamais. On nomme
        # donc l'hote, ce que le texte imprime fait deja mot pour mot.
        *AbilityFactory.UnitCannotTakeDamage(
            CardFinder(name=NOM_PANDEMONIUM, card_type=Minion),
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YY")),
    ]
