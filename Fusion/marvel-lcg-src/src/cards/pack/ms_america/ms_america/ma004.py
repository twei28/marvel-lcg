from . import *

# * Santana Family — SOUTIEN signature, custom « jakxin »
# Cout 1, [mental], trait PERSONA.
#
# Events attached to Santana Family may be played as if they were in your
#   hand.
# Alter-Ego Action: Exhaust Santana Family → search your discard pile for an
#   event and attach it to this card facedown (to a maximum of 2).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# Capacite 1 (« may be played as if they were in your hand ») : `27007`
# George Stacy (Ghost-Spider) et `dz014` Lightbringr (pack dazzler, trait
# PERSONA lui aussi), tous deux montes sur
# `*AbilityFactory.AttachedCardCanPlayLikeInHand(CardFinder(card_type=Event))`
# — qui delegue a `YouMayPlayCardLikeInHand(from_where="ThisPlacedCard")`
# (play.py:332-341). ⚠ La fabrique rend une LISTE d'abilities : deballage
# `*` obligatoire.
#
# Capacite 2 (action qui glisse une carte SOUS le soutien, face cachee, avec
# un plafond) : meme `27007` George Stacy, meme
# `conditions=[... GetPlacedCardArea().GetSize() < N]` et meme
# `CostFunc.Exhaust("This")`. La difference : George Stacy prend la carte
# dans la MAIN (`.SetTarget(Event, from_where=["YourHandCards"])`), Santana
# Family la cherche dans la DEFAUSSE. Pour cette moitie-la, le modele est
# `dt079` Borrowed Gear, qui fouille `discard_pile` puis appelle
# `this.TuckCardUnderHere(face, effect)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Events attached » -> `CardFinder(card_type=Event)` : seuls les
#   EVENEMENTS attaches sont jouables ainsi. La carte ne peut de toute facon
#   en attacher d'autres, mais le filtre est ecrit parce que le texte l'ecrit.
# « FACEDOWN » -> `TuckCardUnderHere(face, effect)` sans `peek=` :
#   `PlaceCardHere(faces, False, effect)` (card_face.py:958-963), donc face
#   CACHEE. `53021` Resource Reserve emploie `peek=True` (visible pour toi
#   seul), ce n'est PAS ce que ce texte demande.
# « (to a maximum of 2) » -> `MAX_EVENEMENTS_SANTANA`, porte par une
#   `conditions=` qui rend l'action indisponible des que la zone est pleine.
#   Le moteur n'a aucun mecanisme dedie : c'est l'idiome de `27007` (3),
#   `dz014` (3) et `60030` (1).
# « ALTER-EGO Action » -> `AbilityType.AlterEgoAction` sur une carte JOUEUR
#   (mot-piege du PROCESSUS-CARTE §5 : sous-type dedie, pas le type nu).
#   ⚠ Consequence en jeu : la carte se REMPLIT en identite civile et se
#   DEPENSE en forme heros. C'est le texte.
#
# LA FLECHE EST UN COUT : « Exhaust Santana Family → search... ». Rendu par
# `CostFunc.Exhaust("This")` porte par la capacite : incline, l'action n'est
# pas proposee (cost_func.py:49).


def GetAbilities() -> Sequence['Ability']:

    def zone_pleine(effect: 'Effect') -> bool:
        zone = effect.this.GetPlacedCardArea()
        return zone is None or zone.GetSize() >= MAX_EVENEMENTS_SANTANA

    def santana_family(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        player = effect.GetInitiator()
        if player is None:
            return

        face = Search.PlayerCard(
            effect,
            player,
            include_player_deck=False,
            include_discard_pile=True,
            card_type=Event,
        )
        if face:
            this.TuckCardUnderHere(face, effect)

    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(
            CardFinder(card_type=Event),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            santana_family,
            conditions=[
                lambda effect, message: not zone_pleine(effect),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
