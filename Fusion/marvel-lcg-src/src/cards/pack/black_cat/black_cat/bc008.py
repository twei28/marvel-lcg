from . import *

# * Black Cat's Claws — AMELIORATION, cout 2, [physical]. WEAPON. UNIQUE.
# Hero Action (attack): Exhaust Black Cat's Claws and discard the top card of
#   the encounter deck -> deal damage to an enemy equal to the number of icons
#   in that card's boost area. If that number was 0, tuck it under Black Cat.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir / `br010` : le squelette d'une amelioration d'arme.
#  - `ho009` : `CostFunc.Custom(None, fn)`, le cout arbitraire dont le `False`
#    bloque le paiement.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « the number of ICONS » — SANS « ([star] and [boost]) ». C'est la SEULE
#    carte du set, avec `bc002`, a ne PAS preciser. On code ce qui est
#    imprime : `IconesSeules` (`CountTotalBoostIcons`), donc les icones
#    CHIFFREES uniquement. La difference est OBSERVABLE, et c'est meme tout le
#    sel de la carte : une carte a etoile seule vaut 0 ici, donc elle DECLENCHE
#    la branche « If that number was 0, tuck it » — alors qu'ailleurs dans le
#    set elle vaudrait 1. Ne pas « harmoniser ».
#  ⚠ DEUX COUTS devant la fleche : incliner ET defausser le dessus du deck de
#    rencontre. Deck vide, la carte n'est pas jouable — d'ou la condition
#    d'offre `DeckDeRencontreNonVide`, sans laquelle l'arme s'inclinerait pour
#    rien (piege `sn005`, RECETTES §5).
#  ⚠ « If that number WAS 0 » -> la consolation, pas un choix : quand l'arme
#    ne fait aucun degat, la carte rejoint la pile. Zero degat n'est donc
#    jamais un coup perdu.
#  « deal damage to AN ENEMY » -> une seule cible.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_le_dessus(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return False
        setattr(effect, "_bc008_carte_defaussee", face)
        return True

    def deck_de_rencontre_non_vide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return Worlds.GetEncounterDeckCards(effect) != []

    def griffes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        defaussee = getattr(effect, "_bc008_carte_defaussee", None)
        # ⚠ « the number of ICONS », sans l'etoile : voir l'encadre.
        degats = IconesSeules([defaussee]) if defaussee is not None else 0

        if degats > 0:
            this.DealDamage(effect.targets, degats, effect)
        elif defaussee is not None:
            # « If that number was 0, tuck it under Black Cat. »
            GlisserSousIdentite(effect, [defaussee], JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            griffes,
            conditions=[deck_de_rencontre_non_vide],
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_le_dessus))
        .SetTarget(Enemy),
    ]
