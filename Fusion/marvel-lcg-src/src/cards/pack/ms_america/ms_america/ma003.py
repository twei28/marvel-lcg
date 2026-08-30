from . import *

# * Hawkeye (Kate Bishop) — ALLIE signature, custom « jakxin »
# Cout 2, PV 2, ATQ 2*, CTR 1*, [wild], trait YOUNG AVENGER.
#
# [star] Hawkeye's attack gains piercing and ranged.
# Interrupt: When Hawkeye would be defeated by consequential damage, if you
#   have resolved "Star-Gaze" this turn, shuffle her into your deck instead.
#
# ---------------------------------------------------------------------------
# ⚠ COLLISION DE NOMS — TROIS CARTES POUR LE MEME PERSONNAGE
#
# Le catalogue contient DEJA `04011` « * Hawkeye » (Kate Bishop, allie
# officiel Leadership du pack trors) ET le heros du pack `kate_bishop`
# (kb001a/kb001b, dont l'allie signature kb002 s'appelle « * Hawkeye »,
# sous-titre Clint Barton). Avec ma003, cela fait TROIS cartes nommees
# « Hawkeye ».
#
# Consequence stricte : AUCUNE recherche par nom ni par sous-titre dans ce
# fichier. Les deux capacites ne parlent que d'elles-memes (`"This"`).
# Rien n'est corrige cote `trors` ni cote `kate_bishop`.
#
# ---------------------------------------------------------------------------
# CAPACITE 1 — « [star] Hawkeye's attack gains piercing and ranged »
#
# Carte de reference : `dt024` Elektra et `dt026` The Punisher, dont le texte
# imprime est mot pour mot « <X>'s attacks gain piercing and ranged » et qui
# s'ecrivent `AbilityFactory.UnitAttackGainKeyword("This", piercing=True,
# ranged=True)` (do_attack.py:827-838).
#
# ⚠ RAPPEL DE MOTEUR : `ranged` ignore la RIPOSTE, PAS le Garde.
# `can_retaliate.py:38` est le seul lecteur d'`IsRanged()` dans tout le
# moteur. `piercing`, lui, defausse les cartes de statut Tough de la cible.
#
# ---------------------------------------------------------------------------
# CAPACITE 2 — LE REMPLACEMENT DE LA DEFAITE
#
# Carte de reference : `kb002` Hawkeye / Clint Barton (pack kate_bishop),
# dont le texte est IDENTIQUE a la clause pres : « When Hawkeye would be
# defeated by consequential damage, shuffle him into your deck ». Meme
# fabrique `WhenUnitWouldBeDefeated(AbilityType.Interrupt, "This", ...,
# by_consequential_damage=True)`, meme `message.SetBeInstead(effect)`, meme
# `Faces.ShuffleAllTo([this], player.player_deck, effect)`.
#
# « by CONSEQUENTIAL damage » -> `by_consequential_damage=True`
#   (defeated.py:11 et 19-22, teste `type(message.by_effect) is
#   Consequential`). Sans ce filtre la capacite partirait sur N'IMPORTE
#   QUELLE defaite, y compris une attaque du vilain.
# « INSTEAD » -> `message.SetBeInstead(effect)` AVANT le deplacement : la
#   defaite n'a PAS lieu, la carte PART dans le deck. Lecon « instead » de
#   The Spot (PROCESSUS-CARTE §5) : sans le `SetBeInstead`, elle irait a la
#   defausse ET dans le deck.
# « SHUFFLE HER INTO YOUR DECK » -> `player.player_deck`, PAS la defausse.
# « if you have RESOLVED "STAR-GAZE" THIS TURN » -> le drapeau du set
#   (`StarGazeResolueCeTour`), pose par `ResoudreStarGaze` et vide a la fin
#   du tour par `RunAt.TurnEnd`. C'est bien « resolue », pas « une carte
#   SUPERPOWER jouee » : Star-Gaze eteinte, le drapeau reste baisse et
#   Hawkeye meurt.
#   La clause est portee par une `conditions=` : la capacite n'est PAS
#   proposee quand elle est fausse, donc la defaite suit son cours normal.


def GetAbilities() -> Sequence['Ability']:

    def star_gaze_resolue(effect: 'Effect',
                          message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        Unused(message)
        player = effect.this.GetControlByPlayer()
        if player is None:
            return False
        return StarGazeResolueCeTour(effect, player)

    def hawkeye(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)

        message.SetBeInstead(effect)

        player = this.GetControlByPlayer()
        if player:
            Faces.ShuffleAllTo([this], player.player_deck, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            ranged=True,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            hawkeye,
            by_consequential_damage=True,
            conditions=[star_gaze_resolue],
        ),
    ]
