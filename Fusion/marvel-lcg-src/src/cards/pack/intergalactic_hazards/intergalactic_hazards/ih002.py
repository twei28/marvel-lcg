from . import *

# Solar Flare — TRAITRISE. 1 icone de boost + une etoile.
#
# When Revealed: If you are confused, take 3 indirect damage. Otherwise, you
#   are confused.
# [star] Boost: Reveal this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Boost` etoile (mots-cles/boost.md) : le texte ne suffit pas, il faut la
#   capacite `WhenCardBecomeBoost`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Degats indirects : 01145 / kb019, `identite.TakeIndirectDamage(this, n,
#   effect)`.
# - Poser un statut : `Faces.GiveStatus([identite], "Confused", effect)`.
# - « [star] Boost: Reveal this card » : meme detournement qu'an014, une carte
#   de boost etant rangee APRES la resolution de son effet — on redirige le
#   rangement a venir par `RegisterTemp` + `WhenCardWouldDiscard`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « IF you are confused ... OTHERWISE » -> deux branches exclusives : la
#   carte punit deux fois plus fort quand le desordre est deja la.
# « take 3 INDIRECT damage » -> indirects, repartis par le joueur.
# « YOU are confused » -> le joueur qui revele, pas le premier joueur.


def GetAbilities() -> Sequence['Ability']:

    def eruption(effect: 'Effect', joueur: 'Player') -> None:
        identite = joueur.GetIdentity()
        if identite is None:
            return
        if identite.IsConfused():
            identite.TakeIndirectDamage(effect.this, 3, effect)
        else:
            Faces.GiveStatus([identite], "Confused", effect)

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur:
            eruption(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if not joueur:
            return

        def reveler(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            # ⚠ REVELER NE SUFFIT PAS : la carte entrait bien en jeu, puis le
            # moteur poursuivait son rangement et la defaussait aussitot
            # (constate au cas « [star] Boost » le 02/09/2026). Il faut donc
            # REMPLACER la defausse (`WhenCardWouldDiscard` porte
            # `CanBeInstead`), puis reveler.
            message2.SetBeInstead(effet_temp)
            this.Reveal(joueur, effet_temp)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                reveler,
            ),
            # ⚠ `unregister_after_exec` est OBLIGATOIRE (mot-cle sans defaut,
            # face_effect.py:98) : sans lui, `TypeError` avalee par le moteur
            # et le ★ Boost ne fait RIEN. Trouve par l'autoplay le 02/09/2026.
            # True : la redirection ne sert qu'une fois.
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
