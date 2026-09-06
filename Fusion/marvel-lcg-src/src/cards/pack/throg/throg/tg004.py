from . import *

# Hammer Throw — EVENEMENT, cout 2, [physical]. ATTACK. SUPERPOWER. x2.
# Hero Action (attack): Exhaust Frogjolnir and return it to your hand ->
#   deal 6 damage to an enemy. This attack gains overkill.
#
# ⚠ TROISIEME « Hammer Throw » DU DEPOT. Les trois, cote a cote :
#   - `06005` (Thor, officiel)      : incline Mjolnir      -> 8 degats, puis le rend a la main ;
#   - `br003` (Beta Ray Bill, Rainy): incline Stormbreaker -> 6 degats, puis le CHERCHE ;
#   - `tg004` (Throg, Rainy)        : incline Frogjolnir ET le rend a la main -> 6 degats.
# Un `Search(name="Hammer Throw")` voit les trois, et le texte francais doit
# etre ecrit sur le `card_id`, jamais sur le nom (leçon « Hulk Smash »).
#
# CARTES DE REFERENCE
#  - `06005` / `br003` : LE montage du depot pour « incliner une arme nommee,
#    frapper, la rendre a la main ». `AttackProperty(overkill=True)` en
#    `property=` de `DealDamage`, et la carte inclinee recuperee par
#    `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards` — jamais
#    par une recherche, c'est CELLE qu'on vient d'incliner qui rentre.
#
# TEXTE CONTRE CODE
#  ⚠ ICI LE RETOUR EN MAIN EST DEVANT LA FLECHE, contrairement a `06005` et
#    `br003` ou il est derriere. C'est donc une seconde moitie de COUT, pas un
#    effet. Consequence en jeu : AUCUNE. Incliner exige deja que le marteau
#    soit en jeu et pret, et un marteau en jeu revient toujours en main — le
#    cout ne peut pas echouer a mi-chemin. Le retour est donc ecrit dans le
#    corps, AVANT les degats, ce qui rend l'ordre imprime a l'identique sans
#    ouvrir au joueur une seconde selection de la meme carte unique.
#    (Choix purement technique, sans effet sur les regles : GUIDE §9.)
#  « deal 6 damage to AN ENEMY » -> vilain OU sbire, une seule cible.
#  « This attack gains OVERKILL » -> fiche `mots-cles/overkill.md` : base
#    automatique du moteur des lors que `AttackProperty(overkill=True)` est
#    passe, le surplus part sur le complot principal.
#  ⚠ Le cout d'inclinaison porte `from_where=["YouControlCards"]` : sans lui,
#    la fabrique irait chercher un Frogjolnir qui n'est pas a vous.


def GetAbilities() -> Sequence['Ability']:

    def lancer_de_marteau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        faces = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        if faces and joueur is not None:
            Faces.ReturnToHand(faces, joueur, effect)

        this.DealDamage(effect.targets, 6, effect, property=AttackProperty(overkill=True))

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
