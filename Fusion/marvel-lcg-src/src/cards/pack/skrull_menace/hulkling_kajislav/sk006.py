from . import *

# Shift and Strike — evenement signature (7/16). ATTACK. SKRULL.
# Cout 2 [physical].
# Hero Response (attack): After you change form, deal 4 damage to an enemy. If
#   you have the [[SKRULL]] trait, confuse that enemy. If you have the [[KREE]]
#   trait, stun that enemy.
#
# Cartes de reference :
#  - **`13014`** Surprise Attack : « Hero Response (attack): After you change
#    form, deal 3 damage to an enemy » : `AfterUnitChangeForm(HeroResponse,
#    "You", op).SetPlay().SetLabel('attack').SetTarget(Enemy)`.
#  - `32008` Steel Fist pour `Faces.GiveStatus(cibles, "Stunned"/"Confused")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you change **form** » : tout changement, heros/civil ET origine
#    (livret p. 4 cite justement Shift and Strike).
#  - « If you have SKRULL... If you have KREE... » : deux tests
#    INDEPENDANTS, lus A LA RESOLUTION, sur l'identite. Avec les deux traits
#    (sk010 Ancestors), l'ennemi est desoriente ET etourdi (FAQ du livret,
#    p. 21).
#  - « confuse / stun **that** enemy » : la cible des 4 degats, meme vaincue
#    entre-temps on ne donne rien (statut sur une carte hors jeu = rien).
#  - « (attack) » : `SetLabel('attack')`.


def GetAbilities() -> Sequence['Ability']:

    def frappe(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        identite = effect.GetInitiator().GetIdentity()
        cibles = list(effect.targets)
        this.DealDamage(cibles, 4, effect)
        en_jeu = [c for c in cibles if c.IsInPlay()]
        if identite.HasTrait("SKRULL"):
            Faces.GiveStatus(en_jeu, "Confused", effect)
        if identite.HasTrait("KREE"):
            Faces.GiveStatus(en_jeu, "Stunned", effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            frappe,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
