from . import *

# * Mister Sinister : SBIRE (ELITE. GENIUS.), nemesis de Destiny. SCH 3, ATQ 3, PV 5, boost 2. Incite 2. Villainous.
# While Destiny's Warning side scheme is in play, Mister Sinister does not activate.
# When Revealed: If Mister Sinister is already in play, discard this card then Mister Sinister activates against you even if Destiny's Warning side scheme is in play.
#
# CARTES DE REFERENCE
#  - `49007` Wrapped in Metal / `60113b` : `EnemyCannotActivate(NonKeyword, "This", conditions=[..])` pour « does not activate » (annule l'activation par `SetBeInstead`).
#  - `sn014` : `ennemi.DoActivate(joueur, effect)` pour « activates against you ».
#  - `incite.md`, `villainous.md` : `Incite 2` et `Villainous 1` lus NATIVEMENT dans `desc`, aucun script.
#
# TEXTE CONTRE CODE
#  « WHILE Destiny's Warning is in play » : l'interdiction n'existe que si une Destiny's Warning est en jeu (et elle disparait avec elle). « does not ACTIVATE » : ni attaque ni manigance. « If Mister Sinister is ALREADY
#    in play » : un AUTRE exemplaire (celui-ci vient d'etre revele). « discard THIS card THEN Sinister activates against YOU even if Warning is in play » : la carte revelee part, puis celui deja en jeu active contre le
#    joueur qui revele, en ignorant l'interdiction (`ActiverSinister` leve le drapeau `dy_forcer`).
#  Chiffres : PV 5, ATQ 3, SCH 3, boost 2, Incite 2.


def GetAbilities() -> Sequence['Ability']:

    def warning_en_jeu(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        return bool(WarningsEnJeu(effect)) and not getattr(effect.this, "dy_forcer", False)

    def deja_en_jeu(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        autres = [f for f in SinistersEnJeu(effect) if f is not this]
        if not autres or joueur is None:
            return
        Faces.DiscardAll([this], effect)
        ActiverSinister(effect, autres[0], joueur)

    return [
        # ⚠ Sinister est UNIQUE : sans cette ligne le moteur defausse en silence la 2e copie AVANT son « When Revealed », et « Mister Sinister activates against you even if
        # Destiny's Warning is in play » ne partait jamais (branche decouverte au pack Mystique, 02/11/2026, cas `dy014 ... DEJA en jeu`). Par NOM : la copie qu'on revele n'est pas
        # encore en jeu, seule la copie DEJA en jeu entend la question.
        AbilityFactory.UniqueRuleNotApplyTo(name=NOM_SINISTER),
        AbilityFactory.EnemyCannotActivate(
            AbilityType.NonKeyword,
            "This",
            conditions=[warning_en_jeu],
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            deja_en_jeu,
        ),
    ]
