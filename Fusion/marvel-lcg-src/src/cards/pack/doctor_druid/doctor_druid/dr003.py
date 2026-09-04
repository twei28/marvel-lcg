from . import *

# * Ancient One — SOUTIEN, cout 1, [mental]. MYSTIC. PERSONA.
# While this card is in your hand, your basic attacks gain overkill, piercing
#   and ranged.
# Alter-Ego Action: Exhaust Ancient One -> look at the top 3 cards of your
#   deck, add each Doctor Druid card to your hand and discard the others.
#
# CARTES DE REFERENCE
#  - `do_attack.py` `UnitAttackGainKeyword(..., is_basic_attack=True)`.
#  - `ok001b` / `yd001b` pour la fouille du dessus du deck avec tri.
#
# TEXTE CONTRE CODE
#  « your BASIC attacks » -> `is_basic_attack=True` : une attaque d'evenement
#    ne gagne rien. Mot-piege, le texte le dit et c'est facile a rater.
#  « each Doctor Druid card » -> `EstCarteDuDruide`, donc
#    `IsDeckBuildingClass("Doctor Druid")`. PLUS RESTRICTIF que
#    « identity-specific » : la carte signature d'un AUTRE heros ne compte pas.
#  « and discard the OTHERS » -> ce qui reste part a la defausse, ce n'est pas
#    remis sur le deck. Et c'est une bonne chose pour ce heros : `dr001a`
#    rejoue justement depuis la defausse.
#  « ALTER-EGO Action » -> `AbilityType.AlterEgoAction`, sous-type dedie.


def GetAbilities() -> Sequence['Ability']:

    def consulter_le_deck(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # ⚠ `LookAtDeck` est l'idiome du depot pour « regardez les N premieres
        # cartes » (modele aa003) : il expose les faces SANS les deplacer.
        dessus = list(joueur.LookAtDeck(joueur.player_deck, 3, effect))
        gardees = [f for f in dessus if EstCarteDuDruide(f)]
        autres = [f for f in dessus if f not in gardees]

        if gardees:
            joueur.GainCard(gardees, effect)
        if autres:
            Faces.DiscardAll(autres, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        *DepuisLaMain([
            AbilityFactory.UnitAttackGainKeyword(
                CardFinder(name=NOM_HEROS),
                None,
                is_basic_attack=True,
                overkill=True,
                piercing=True,
                ranged=True,
            ),
        ]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            consulter_le_deck,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
