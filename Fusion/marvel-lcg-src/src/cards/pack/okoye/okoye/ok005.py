from . import *

# Adored Ones (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok004 (voir ce fichier pour
# le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def adored_ones(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def creer(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            for _ in range(2):
                CreerJetonEtMettreEnJeu(ID_JETON_DORA_MILAJE, initiator, effect)

        def chercher(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            face = Search.PlayerCard(
                effect,
                initiator,
                include_player_deck=True,
                include_discard_pile=True,
                finder=CardFinder(
                    card_type=Ally,
                    check_face_fn=lambda f: f.IsName(NOM_ANEKA) or f.IsName(NOM_AYO),
                ),
            )
            if face:
                face.PutIntoPlay(initiator, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Create 2 Dora Milaje allies and put them into play",
                creer,
            ),
            AbilityFactory.ForChoiceAbility(
                "Search your deck and discard pile for Aneka or Ayo and put her into play",
                chercher,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            adored_ones,
        ).SetPlay(),
    ]
