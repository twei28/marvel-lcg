from . import *

# Spray and Pray — EVENEMENT, cout 3, [energy]. ATTACK. TACTIC. x2.
# Hero Action: Make the following attack 5 times against any targets you
#   choose:
#   (attack): Deal 1 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `th010` It's Clobberin' Time! (pack the_thing) et `hk004` Hulk Smash :
#    une SUITE d'attaques d'un meme evenement. th010 imprime des attaques sans
#    contrainte de cible et repose un `ForChoiceAbility(...).SetTarget(Enemy)`
#    a CHAQUE attaque : c'est exactement « against ANY targets you choose ».
#  - `01053` Relentless Assault : `hero.DealDamage(..., property=
#    AttackProperty(...))`, ce qui fait de chaque tir une vraie ATTAQUE du
#    heros, et non un simple effet de degats.
#
# TEXTE CONTRE CODE
#  ⚠ « the following ATTACK 5 times » -> CINQ attaques d'1, pas une attaque de
#    5. La difference se voit : Reeling (ar008) donne overkill a chacune,
#    Sundered (ar009) ajoute +1 a chacune (5 -> 10 sur un sbire sondere),
#    une Riposte part cinq fois, un Tenace n'absorbe que la premiere, et
#    l'Aegis Breastplate (ar013) renvoie chaque tir a Ares.
#  ⚠ « against ANY targets you choose » -> le selecteur est repose a chaque
#    tir : on peut repartir les cinq degats, ou tout mettre sur le meme.
#  ⚠ Chaque tir est une attaque DU HEROS (source = Ares), pas de la carte :
#    c'est ce qui rend la lecture « attacker » de l'Aegis Breastplate juste,
#    et ce qui alimente Ares' Battle Helm (« After Ares attacks and defeats »).
#  ⚠ Une cible peut mourir en cours de route : le selecteur du tir suivant ne
#    la propose plus. S'il n'y a plus d'ennemi, les tirs restants tombent dans
#    le vide.


TIRS = 5


def GetAbilities() -> Sequence['Ability']:

    def arroser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if joueur is None or heros is None:
            return

        def tirer(cibles: Sequence['CardFace']) -> None:
            ennemis = [c for c in cibles if c is not None and Enemy.IsType(c)]
            if ennemis:
                heros.DealDamage(ennemis, 1, effect, property=AttackProperty())

        for _ in range(TIRS):
            if not EnnemisEnJeu(effect):
                break
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", tirer)
                .SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            arroser,
        ).SetPlay().SetLabel('attack'),
    ]
