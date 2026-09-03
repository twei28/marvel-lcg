from . import *

# Cemented — complot ANNEXE nemesis (2/5). Menace de depart 2, Entrave 1 par
# joueur, Boost 2.
# Hinder 1[per_hero].
# Players cannot make basic attacks with heroes or allies or flip upgrades or
#   identities.
# Action: Each player may discard 1 card from their hand -> until the end of
#   the phase, each player who discarded a card this way may treat this card's
#   printed text box as if it were blank.
#
# Cartes de reference :
#  - **`PlayersCannotMakeBasicAttack`** (player.py:48) : la fabrique dediee,
#    qui teste `ability.flags.ability_type.flags.is_basic_power` ET
#    `"ATK" in ability.func_names`.
#  - **`YouCannotFlipCards`** (ability_factory.py:212) pour l'interdiction de
#    retournement, deja employee par `nt012` Practice.
#  - `iw015` Emotional Masterplan : le motif « Action ... -> treat the printed
#    text box of this card as if it were blank until ... », c'est-a-dire un
#    complot qui offre de se NEUTRALISER lui-meme contre une defausse.
#  - `face.TreatAsIfBlank(effect, message, until_phase_end=...)`
#    (face_action.py, via aoa/four_horsemen/__init__.py:70).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Hinder 1[per_hero].** » : base automatique lue dans `desc.Hinder`
#    (fiche mots-cles/hinder.md), et le `1*` du desc rend le « par joueur ».
#    AUCUN script — le recoder doublerait la menace posee.
#  - « basic attacks **with heroes or allies** » : les deux, et rien d'autre.
#    Un sbire ou le vilain ne sont pas concernes.
#  - « or flip **upgrades or identities** » : DEUX familles de cartes, pas
#    seulement la Battle Board. Le complot vise le pack de plein fouet — nt002,
#    nt004, nt006, nt007 et nt009 perdent leur moitie utile — mais il
#    frapperait aussi un Vision ou une Kitty Pryde.
#  - « **Each player MAY** discard » : facultatif, joueur par joueur, et seuls
#    ceux qui ont paye profitent du texte vierge. La fabrique du moteur ne sait
#    pas rendre ce grain-la (voir l'ecart ci-dessous).
#  - « until the end of the **phase** » : `until_phase_end`, pas le round.
#
# ⚠ ECART ASSUME, et il est double. (1) `YouCannotFlipCards` teste
# `message.trigger in Select.GetYou(effect).GetControlCards()`
# (ability_factory.py:215) : l'interdiction ne porte donc que sur les cartes du
# joueur COURANT, alors que le texte dit « Players ». En solo c'est identique ;
# a plusieurs, un joueur qui n'est pas le joueur courant pourrait retourner.
# (2) Le texte vierge est pose GLOBALEMENT, pas « pour chaque joueur qui a
# defausse » : le moteur ne connait pas de texte vierge par joueur. Les deux
# ecarts vont dans le sens du JOUEUR, jamais du vilain, et sont signales
# plutot que masques.


def GetAbilities() -> Sequence['Ability']:

    def cemented(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        a_paye = False
        for joueur in Worlds.GetPlayers(effect):
            cartes = list(joueur.hand_cards.Get())
            if not cartes:
                continue
            choix = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 1 card to blank « Cemented » until the end of the phase",
                    lambda cibles: None,
                ),
            )
            if choix is not None:
                Faces.DiscardAll(cartes[:1], effect)
                a_paye = True

        if a_paye:
            this.TreatAsIfBlank(effect, None, until_phase_end=True)

    return [
        AbilityFactory.PlayersCannotMakeBasicAttack("AnyPlayer"),
        AbilityFactory.YouCannotFlipCards(Upgrade),
        AbilityFactory.YouCannotFlipCards(Identity),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            cemented,
        ),
    ]
