from . import *

# Mutant Hunter — TRAITRISE (x2). SKILL. Boost 1.
# When Revealed (Alter-Ego): Resolve the "Special" ability on the copy of Bleeding Out attached to your identity. This card gains surge.
# When Revealed (Hero): Place 1 bleed counter on the copy of Bleeding Out attached to your identity. Lady Deathstrike attacks you.
#
# Cartes de reference :
#  - deux « When Revealed » selon la forme : `WhenThisRevealed("AlterEgo"?)` — modele `02030` I See You (`player.IsAlterEgo()`), `01124`
#    Klaw (« When Revealed (Alter-Ego) ») ; `ThisCardGainSurge(effect)` (`nt015`, `ag013`) ;
#  - attaque : `villain.DoAttackYou(joueur, effect)` (`ld013`) ; compteur : `Faces.PlaceCountersOn([saignement], 1, 'bleed', effect)`.
#
# ⚠ Mots-pieges :
#  - UNE SEULE des deux branches selon la forme DU JOUEUR QUI REVELE (alter-ego : Special + surge ; heros : compteur + attaque) ;
#  - forme HEROS : seulement +1 compteur bleed (PAS un Special : aucune defausse de deck) puis l'attaque normale (avec boost) ;
#  - « This card gains surge » en alter-ego seulement.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        if joueur.IsAlterEgo():
            ResoudreSaignement(effect, joueur)
            ThisCardGainSurge(effect)
            return
        saignement = LeSaignement(joueur)
        if saignement is not None:
            Faces.PlaceCountersOn([saignement], 1, 'bleed', effect)
        vilain = LadyDeathstrike(effect)
        if vilain is not None:
            vilain.DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ),
    ]
