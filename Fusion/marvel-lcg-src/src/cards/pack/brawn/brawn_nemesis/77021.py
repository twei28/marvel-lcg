from . import *

# Imperius Rex! (traitrise nemesis) — custom « Rainy »
# When Revealed: Namor activates against you. If he is not in play, find Namor,
#   put him into play engaged with you and give him 1 facedown boost card.
# [star] Boost: Deal this card to yourself as a facedown encounter card.
#
# Montage d'Ancient Grudge 11051, carte officielle au texte jumeau : on active
# l'ennemi s'il est deja la, sinon on le cherche et on le fait entrer. Le sbire
# qui vient d'arriver n'agit PAS dans la foulee — il arrive seulement avec une
# carte de boost d'avance.

def GetAbilities() -> Sequence['Ability']:

    def imperius_rex(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        namor = Worlds.FindCardOnField(effect, name="Namor", card_type=Enemy)
        if namor:
            namor.DoActivate(joueur, effect)
            return

        namor = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name="Namor",
        )
        if namor:
            namor.PutIntoPlay(joueur, effect)
            namor.CastTo(Minion).GiveFacedownBoostCardsInternal(1, effect, None)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        # « Deal this card to yourself as a facedown encounter card » : la carte
        # de boost revient sur le joueur, face cachee, et sera revelee plus tard
        # avec son When Revealed.
        #
        # ⚠ La DEPLACER ici ne sert a rien : une carte de boost est rangee par le
        # moteur APRES la resolution de son effet, et le deplacement est ecrase
        # (mesure du 7/8/2026 : la carte finissait dans `AsideDeck`). Meme piege
        # que « put this card into your reserve » sur les evenements — il faut
        # DETOURNER le rangement a venir, pas devancer le moteur.
        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return

        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            message2.SetToArea(joueur.dealt_encounter_cards)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                rediriger,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            imperius_rex,
        ),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
