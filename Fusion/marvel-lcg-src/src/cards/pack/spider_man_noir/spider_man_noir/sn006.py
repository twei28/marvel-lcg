from . import *

# * The Black Cat Club — SOUTIEN, cout 1, [wild]. LOCATION. UNIQUE.
# Alter-Ego Action: Exhaust The Black Cat Club and discard a card tucked under
#   your identity -> choose to either draw 2 cards or heal 4 damage from your
#   identity.
#
# CARTES DE REFERENCE
#  - `br007` * Skuttlebutt : le squelette d'un soutien signature unique
#    (`CanPlayThisSupportCard()` + cout d'inclinaison + `ChooseAbilities` a
#    deux branches).
#  - `53029` Harlem's Protector : une capacite reservee a la forme civile.
#  - `ho009` : `CostFunc.Custom` chaine derriere un `CostFunc.Exhaust`.
#
# TEXTE CONTRE CODE
#  ⚠ DEUX COUTS, tous deux devant la fleche : incliner la carte ET defausser
#    une carte glissee. Oublier le second rendrait le club gratuit — piege
#    `wd005`, ou une moitie de cout avait ete perdue.
#  « under YOUR IDENTITY » -> la meme pile que « under your hero » ailleurs
#    dans le set : elle est portee par la CARTE, pas par la face
#    (card_face.py:1017).
#  « ALTER-EGO Action » -> indisponible en forme heros. C'est ce qui fait de
#    ce club le seul endroit ou la pile se convertit en cartes ou en soins,
#    et il faut passer en civil pour s'en servir.
#  « CHOOSE TO EITHER ... OR ... » -> exclusif. Le pilote prend la premiere
#    branche par defaut, les cas forcent celle qu'ils mesurent.
#  « heal 4 damage FROM YOUR IDENTITY » -> l'identite, pas un allie.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_une_carte_glissee(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUneCarteGlissee(effect)

    def le_club(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = IdentiteDuJoueur(effect, joueur)

        def piocher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.DrawUp(2, effect)

        def soigner(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is not None:
                this.HealthUnits([identite], 4, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Draw 2 cards", piocher),
            AbilityFactory.ForChoiceAbility("Heal 4 damage from your identity", soigner),
        )

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            le_club,
            conditions=[PileNonVide],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_une_carte_glissee)),
    ]
