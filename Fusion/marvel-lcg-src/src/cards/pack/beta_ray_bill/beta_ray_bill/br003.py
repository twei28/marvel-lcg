from . import *

# Hammer Throw — EVENEMENT, cout 3, [physical]. ATTACK. SUPERPOWER. x3.
# Hero Action (attack): Exhaust Stormbreaker -> deal 6 damage to an enemy.
#   Find Stormbreaker and add it to your hand. This attack gains overkill.
#
# ⚠ HOMONYME EXACT DE `06005`, la Hammer Throw OFFICIELLE de Thor, qui dit
# « Exhaust Mjolnir -> deal 8 damage ... and return Mjolnir to your hand ».
# Meme nom, meme structure, deux chiffres differents. Troisieme homonymie du
# depot apres « Hulk Smash » et « Limitless Strength » (pack hulk_rainy) : un
# `Search(name="Hammer Throw")` verrait les deux, et le texte francais doit
# etre ecrit sur le `card_id`, jamais sur le nom.
#
# CARTE DE REFERENCE : `06005`, copiee ligne pour ligne — c'est LE montage du
# depot pour « incliner une arme nommee, frapper, la rendre a la main ».
#  - `AttackProperty(overkill=True)` passe en `property=` de `DealDamage` ;
#  - la carte inclinee se recupere par
#    `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`, et non
#    par une recherche : c'est CELLE qu'on vient d'incliner qui rentre.
#
# TEXTE CONTRE CODE
#  « FIND Stormbreaker » la ou 06005 dit « RETURN Mjolnir » : la difference
#    est sans effet ici, la carte venant d'etre inclinee EN JEU. Le montage
#    reste celui de 06005.
#  « This attack gains OVERKILL » -> le surplus passe au complot principal.
#    Mot-cle : fiche `docs/reference/mots-cles/overkill.md`, base automatique
#    du moteur des lors que `AttackProperty(overkill=True)` est passe.
#  ⚠ Le cout d'inclinaison porte `from_where=["YouControlCards"]` : sans lui,
#    la fabrique irait chercher un Stormbreaker qui n'est pas a vous.


def GetAbilities() -> Sequence['Ability']:

    def lancer_de_marteau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage(effect.targets, 6, effect, property=AttackProperty(overkill=True))
        faces = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        if faces and joueur is not None:
            Faces.ReturnToHand(faces, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lancer_de_marteau,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(
            name=NOM_MARTEAU,
            card_type=Upgrade,
            from_where=["YouControlCards"]))
        .SetTarget(Enemy),
    ]
