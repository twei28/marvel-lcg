from . import *

# "You're in My World" — MANIGANCE SECONDAIRE du set MOLECULE MAN (2/6).
# 5 menaces, boost 3.
# This card cannot leave play while Molecule Man is in play.
# When Revealed: Name a resource type ([energy], [mental], [physical], or
#   [wild]). While You're in My World is in play, each player cannot play cards
#   with that printed resource type from their hand.
#
# ⚠⚠ ELLE VERROUILLE UNE COULEUR POUR TOUTE LA TABLE, ET ON NE PEUT PAS LA
# CONTRER TANT QUE MOLECULE MAN TIENT DEBOUT. C'est la carte qui force a tuer
# le sbire en premier.
#
# CARTES DE REFERENCE
#  - `07004` Day of Reckoning : `AbilityFactory.SchemeCannotLeavlPlayWhile(
#    "This", while_card_is_in_play=CardFinder(name=...))`. ⚠ La faute de frappe
#    « Leavl » est CELLE DU MOTEUR, pas la notre.
#  - `41028` Psionic Illusion : `player.DeclareResourceType()` pour nommer une
#    couleur, et `FacesCounter.GetPrintedResources([face]).HasColorPrinted(...)`
#    pour la relire sur une carte.
#  - `AbilityFactory.PlayersCannotPlayCardWhile(...)` (factory/player.py:8).
#
# TEXTE CONTRE CODE
#  ⚠ « PRINTED resource type » : l'icone imprimee sur la carte, pas la
#    ressource qu'on genererait avec. `GetPrintedResources`, et
#    `HasColorPrinted` — qui ne convertit PAS le joker en couleur
#    (resources.py:136). Une carte [wild] n'est donc bloquee que si c'est
#    [wild] qui a ete nomme.
#  ⚠ « EACH PLAYER » : toute la table, pas seulement celui qui a revele.
#  ⚠ « FROM THEIR HAND » : jouer depuis la main. Une carte mise en jeu par un
#    effet passe.
#  ⚠⚠ La couleur nommee doit survivre a la revelation : elle est rangee sur
#    `effect.world`, sous la cle de la carte, comme le fait `jessica_jones`
#    pour son suivi de round. Une variable de module ne conviendrait pas — les
#    modules sont partages par toutes les parties du processus.


ATTR_COULEUR = "iron_patriot_youre_in_my_world"


def _couleurs(world: Any) -> Any:
    table = getattr(world, ATTR_COULEUR, None)
    if table is None:
        table = {}
        setattr(world, ATTR_COULEUR, table)
    return table


def GetAbilities() -> Sequence['Ability']:

    def nommer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        _couleurs(effect.world)[id(this.card)] = joueur.DeclareResourceType()

    def carte_de_la_couleur_nommee(effect: 'Effect',
                                   message: 'Message.CheckEffectCondition') -> bool:
        couleur = _couleurs(effect.world).get(id(effect.this.card))
        if couleur is None:
            return False
        face = message.check_effect.this
        if face is None:
            return False
        return FacesCounter.GetPrintedResources([face]).HasColorPrinted(couleur)

    return [
        AbilityFactory.SchemeCannotLeavlPlayWhile(
            "This",
            while_card_is_in_play=CardFinder(name="Molecule Man"),
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            nommer,
        ),
        AbilityFactory.PlayersCannotPlayCardWhile(
            "AnyPlayer",
            conditions=[carte_de_la_couleur_nommee],
        ),
    ]
