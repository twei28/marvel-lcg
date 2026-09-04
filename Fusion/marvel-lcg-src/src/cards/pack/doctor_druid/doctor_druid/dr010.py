from . import *

# Ancient Order of Druids — OBLIGATION. 2 icones de boost.
# Give to the Anthony Druid player.
# You may flip to alter-ego form. Choose:
#  - Exhaust Anthony Druid -> remove Ancient Order of Druids from the game.
#  - Discard each identity-specific event from your hand. If no event was
#    discarded this way, this card gains surge. Discard this obligation.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau de la carte dit « DOCTOR DRUID », pas
# « DOCTOR DRUID NEMESIS ». Son `set_name` est donc celui du set HEROS et le
# module vit ICI, dans `doctor_druid/`. `database.py:197` cherche le module
# dans le dossier qui porte le nom du SET : range dans `_nemesis/`, il ne
# serait JAMAIS charge et l'obligation entrerait en jeu sans rien faire, en
# silence. Piege deja paye par `bt019`, `nt012` et `yd013` — quatrieme fois.
#
# CARTES DE REFERENCE
#  - `yd013` Banished (pack yondu) : meme structure exacte, deux branches dont
#    l'une RETIRE DU JEU et l'autre DEFAUSSE.
#
# TEXTE CONTRE CODE
#  « remove ... FROM THE GAME » vs « DISCARD this obligation » : deux sorties
#    DIFFERENTES, a ne jamais coder l'une pour l'autre.
#  « each identity-specific EVENT » -> `EvenementsSpecifiquesEnMain`. EVENT,
#    pas « carte » : `dr012`, elle, dit bien « card ».
#  « If NO event was discarded this way » -> le Renfort ne tombe que si la
#    main n'en contenait AUCUN, pas « s'il en reste ».
#  ⚠ Le joueur est pris sur le MESSAGE (`GetGaveToPlayer`), jamais sur
#    `effect.this` : une obligation est une carte de RENCONTRE, et
#    `JoueurDeCetteCarte` ne rend alors aucun joueur (lecon yd013).


def GetAbilities() -> Sequence['Ability']:

    def ordre_ancien(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)
        identite = joueur.GetIdentity()

        def incliner_puis_retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if identite is None:
                return
            Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def defausser_les_evenements(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            evenements = EvenementsSpecifiquesEnMain(joueur)
            if evenements:
                Faces.DiscardAll(evenements, effect)
            else:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Anthony Druid to remove this from the game",
                incliner_puis_retirer,
                condition=(identite is not None and not identite.IsExhaust()),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard each identity-specific event from your hand",
                defausser_les_evenements,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            ordre_ancien,
        ),
    ]
