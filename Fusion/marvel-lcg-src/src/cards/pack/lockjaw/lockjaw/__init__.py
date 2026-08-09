from cards.pack import *

# Fabriques partagées du pack custom « Lockjaw » (Nugget, Marvel Champions
# Custom Project, Cycle I).
#
# Le pack tourne autour du trait TELEPORT : la plupart des cartes signature
# font changer de forme, et plusieurs cartes récompensent le paiement avec la
# ressource « os » du Tuning Fork. Le moteur n'ayant que quatre couleurs, cet
# os est rendu par [wild] (G) : le Tuning Fork en génère, et les cartes qui
# demandent « if you paid using a [os] resource » testent la couleur G.
# Écart documenté dans GUIDE-CREATION-CONTENU.md §9.


def Companion() -> List['Ability']:
    """« Companion » : hors limite d'alliés, et ne peut pas défendre.

    Mot-clé maison du pack, sans équivalent dans le moteur : il se compose de
    deux règles déjà existantes.
    """
    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.UnitCannotDefend(
            "This",
            None,
            cannot_trigger_defense_ability=True,
        ),
    ]


def PayeAvecMental(effect: 'Effect') -> bool:
    """« If you paid for this card using a [mental] resource ».

    CORRECTIF (9/8/2026) — signale en jeu : « Ruff Ambush n'a fait que 5 degats
    alors que j'ai paye en mental ». La fonction s'appelait `PayeAvecMental` et
    testait la couleur "G", c'est-a-dire une ressource WILD. L'icone des
    scans avait ete prise pour un os : ce sont des noeuds relies, l'icone de
    la ressource MENTALE de ce pack. Verification faite en comparant a
    l'icone imprimee de 78005 Kamala's Room, dont la fiche porte RES=B — meme
    forme, sur fond bleu — et a celle de 78002 Black Bolt, RES=G, qui est une
    ETOILE verte, tout autre.

    Quatre cartes reposaient sur cette lecture : 78001a Fetch!, 78009 Fast
    Travel, 78010 Zooming Around et 78011 Ruff Ambush. Leur clause bonus ne
    partait jamais quand le joueur payait comme la carte le demande.
    """
    return effect.GetPaidResources().HasColor("B")


# CORRECTIF 4/8/2026 : `ChangerDeForme` et `YouMayChangeForm` etaient appeles
# par Teleport To Safety 78008, Fast Travel 78009 et 78010, mais definis NULLE
# PART. Les trois cartes levaient un NameError et se defaussaient sans rien
# faire. Trouve en ecrivant le premier cas de comportement de Fast Travel.
def ChangerDeForme(joueur: 'Player', effect: 'Effect') -> None:
    """Fait changer de forme l'identite du joueur vise."""
    identite = joueur.GetIdentity()
    if identite is not None:
        identite.ChangeToOtherIdentityForm(effect)


def YouMayChangeForm(joueur: 'Player', effect: 'Effect') -> None:
    """« You may change your form » : le changement reste au choix du joueur."""
    joueur.MayChooseOneAbility(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Change your form",
            lambda targets: ChangerDeForme(joueur, effect),
        ).SetHasNoTargetEffect(),
    )
