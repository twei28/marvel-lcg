from . import *

# Adored Ones (1/2)
# Hero Action: Choose one:
# - Create 2 Dora Milaje allies and put them into play.
# - Search your deck and discard pile for Aneka or Ayo and put her into play.
#
# Exemplaire physique 1 de 2 (ok004, ok005 : meme texte, deux card_id
# distincts, modele kb019/kb020). "Create 2 Dora Milaje allies" : jeton hors
# deck, modele `CreerJetonEtMettreEnJeu` (okoye/__init__.py, lui-meme calque
# sur moon_knight/age_of_khonshu). "Search... for Aneka or Ayo" : nom en
# liste via `check_face_fn`, modele kb008 (`CardFinder(check_face_fn=...)`),
# `Search.PlayerCard` ne prenant qu'un seul `name=` a la fois.


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
