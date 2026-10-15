from . import *

# Assailed by Their Own — TRAITRISE nemesis de Hulkling (n° 35, 4/5).
# 2 icones boost.
# When Revealed (Alter-Ego): Exhaust your identity.
# When Revealed (Hero): Choose a character in play (other than your identity)
#   that shares a [[TRAIT]] with your hero. Take X damage where X is equal to
#   the chosen character's ATK. Otherwise, exhaust your identity.
#
# Cartes de reference :
#  - **`36030`** Claustrophobia / `39014b` : `WhenThisRevealed(None, op)`.
#    La forme se lit sur l'identite (`Hero.IsType(...)`), comme les packs
#    hulk_rainy (90109) et ares.
#  - `ab008` pour `Faces.ExhaustAll`, `dt043` pour `TakeDamage(source, n, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - DEUX textes selon la forme AU MOMENT de la revelation.
#  - « a character **in play** » : allie, sbire, vilain, autre identite — de
#    n'importe qui, sauf TON identite. « shares a TRAIT » = un trait en commun
#    avec ton heros.
#  - « Take X damage » : c'est TON identite qui encaisse, X = l'ATK ACTUELLE
#    du personnage choisi (une ATK 0 donne 0 degat, c'est le choix malin).
#  - « Choose » : le JOUEUR choisit parmi les candidats.
#  - « **Otherwise** » : SEULEMENT s'il n'y a aucun candidat, on incline.
#  - Les degats sont INFLIGES par cette traitrise (une carte Tough les absorbe).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        if not Hero.IsType(identite):
            Faces.ExhaustAll([identite], effect)
            return

        candidats = [
            f for f in Worlds.GetOnFieldCards(effect)
            if Unit2.IsType(f) and f != identite and f.IsInPlay() and identite.ShareTrait(f)
        ]
        if not candidats:
            Faces.ExhaustAll([identite], effect)
            return
        choisi = joueur.AskChooseFace(
            candidats, effect,
            prompt="Choose a character that shares a trait with your hero: take damage equal to its ATK",
        )
        if choisi is None:
            return
        x = getattr(choisi, "attack", 0) or 0
        if x > 0:
            identite.CastTo(Unit2).TakeDamage(this, x, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
    ]
