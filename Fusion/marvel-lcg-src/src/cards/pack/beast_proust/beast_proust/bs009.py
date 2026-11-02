from . import *

# Tech Support : EVENEMENT (TACTIC), cout 0, [energy]. x3.
# Hero Action: Exhaust Beast's Lab, then choose: • discard a card tucked under Beast's Lab, then ready your hero. • search your deck or discard pile for a TECH upgrade, then tuck it under Beast's Lab.
#
# CARTES DE REFERENCE
#  - `hz002`-like / `nt005` : `WhenInYourPlayTurn(HeroAction, op).SetPlay()` + `.SetCostFunc(CostFunc.Exhaust("YouControlCards", name=..))` ; UNE SEULE capacite `Play` (un « Choose one » en deux `Play` fait tomber le montage,
#    RECETTES §5) : le choix se fait dans l'operation par `ChooseAbilities`.
#  - `dy013` : `ForChoiceAbility(.., condition=..)` (branche offerte seulement si elle est possible). `14001a` : `Faces.ReadyAll`.
#  - `bs001a` (meme set) : `Glisser` ; `Search.PlayerCard(include_player_deck=True, include_discard_pile=True, trait=, card_type=)`.
#
# TEXTE CONTRE CODE
#  « Exhaust Beast's Lab, THEN choose » : l'inclinaison est un COUT commun aux deux branches (donc l'evenement n'est offert que si le Lab est PRET). « discard a card tucked under » : au choix du joueur ;
#    « THEN ready YOUR HERO » : la face heros. « search your deck OR discard pile » : les deux zones dans la meme fenetre ; « TECH upgrade » : amelioration TECH ; « tuck it under Beast's Lab » : sous le Lab, visible,
#    plafond de 3 applique par le Lab.
#  Chiffres : cout 0.


def GetAbilities() -> Sequence['Ability']:

    def lab_pret(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and LabPret(joueur)

    def tech_support(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        glissees = GlisseesSousLab(joueur)

        def defausser_et_redresser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            carte = joueur.AskChooseFace(glissees, effect, prompt="Discard a card tucked under Beast's Lab", peek=True, not_move=True)
            if carte is not None:
                Faces.DiscardAll([carte], effect)
            Faces.ReadyAll([joueur.GetHero()], effect)

        def chercher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            ChercherTechEtGlisser(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a card tucked under Beast's Lab, then ready your hero",
                defausser_et_redresser,
                condition=bool(glissees),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Search your deck or discard pile for a TECH upgrade, then tuck it under Beast's Lab",
                chercher,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tech_support,
            conditions=[lab_pret],
        ).SetPlay()
        .SetCostFunc(CostFunc.Exhaust("YouControlCards", name=NOM_LAB)),
    ]
