from . import *

# Threat Suppression — Evenement 1 [physical], classe Hero. ATTACK.
# [star] As an additional cost to play this event, exhaust Legs (Intact) or
#   destroy it.
# Hero Action (attack): Deal 1 damage to up to 3 different enemies and stun up
#   to 2 of those enemies.
#
# Cartes de reference :
#  - `dt005` Blast Radius : `range=("Zero", 3)` sur `Enemy` pour « up to 3 ».
#  - `al012` / `hd001b` / `ih003` : `joueur.MayChooseFace(candidats, effect)`
#    pour designer une carte PARMI une liste deja etablie.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **of those** enemies » : l'assommement ne vise pas n'importe qui, mais
#    les ennemis QUI VIENNENT D'ETRE BLESSES. Un second `SetTarget` ouvrirait
#    toute la table ; on repart donc de `effect.targets`, filtres sur ceux qui
#    sont encore en jeu et assommables.
#  - « up to 2 » : on demande DEUX FOIS, et le joueur peut s'arreter apres
#    zero ou un (`MayChooseFace` rend `None` s'il refuse).
#  - « different enemies » : trois cibles distinctes ; le selecteur ne rend
#    jamais deux fois la meme carte, aucune regle a ajouter.


def GetAbilities() -> Sequence['Ability']:

    def threat_suppression(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(effect.targets, 1, effect)

        joueur = effect.GetInitiator()
        candidats = [c for c in effect.targets
                     if c.IsInPlay() and c.CastTo(Unit2).CanbeStunned()]
        Unused(this)
        for _ in range(2):
            if not candidats:
                break
            choisi = joueur.MayChooseFace(candidats, effect, not_move=True)
            if choisi is None:
                break
            Faces.GiveStatus([choisi], "Stunned", effect)
            candidats.remove(choisi)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            threat_suppression,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Custom(
            SelecteurComposantIntact(nom=NOM_LEGS),
            InclinerOuDetruire,
        ))
        .SetTarget(Enemy, range=("Zero", 3)),
    ]
