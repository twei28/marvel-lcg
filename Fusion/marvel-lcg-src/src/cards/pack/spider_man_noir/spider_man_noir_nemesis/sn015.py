from . import *

# Thunderstorm — ENVIRONNEMENT nemesis (N 5/5). CONDITION. 2 icones de boost.
# Cards from this set gain surge.
# Forced Response: After the surge keyword on an encounter card is resolved
#   (including this one), the player resolving it takes 1 indirect damage if
#   they are in hero form.
# Hero Action: Spend [energy][energy] resources -> discard this card.
#
# ⚠ HOMONYME : `36004` Thunderstorm (pack storm) est un SOUTIEN de Storm, sans
# rapport. Deux cartes distinctes de meme nom — le texte francais s'ecrit sur
# le `card_id`.
#
# MOT-CLE : SURGE — fiche `docs/reference/mots-cles/surge.md`. Ici il n'est PAS
# une base automatique de CETTE carte : elle l'ACCORDE a d'autres. C'est le
# parametre `surge=` de `GiveKeywordToInPlayWhenApplyThis`
# (environment.py:99), la fabrique prevue pour un environnement qui modifie
# les cartes en jeu.
#
# CARTES DE REFERENCE
#  - `04080` Dense Forest : le squelette d'un environnement nemesis
#    (declencheur + `TakeIndirectDamage`).
#  - `01100` / `04072` / `sd020` : `PlayerActionToDiscardThis(...).SetCost(...)`,
#    la Hero Action de defausse a cout de ressources.
#  - `WhenSurgeWouldBeResolved` (resolve.py:286) : la seule prise du moteur sur
#    « the surge keyword ... is resolved ».
#
# TEXTE CONTRE CODE
#  ⚠ « Cards from THIS SET gain surge » -> le SET NEMESIS, pas toutes les
#    cartes de rencontre. Le filtre est le `set_name`, et il inclut cette
#    carte-ci — d'ou le « (including this one) » de la phrase suivante, qui ne
#    serait pas necessaire autrement.
#  ⚠ « the player RESOLVING it » -> celui qui resout le surge, pas le premier
#    joueur ni le porteur de la carte.
#  ⚠ « IF THEY ARE IN HERO FORM » -> aucun degat en forme civile. Mot-piege
#    « if » : la branche existe, et un cas doit prouver le ZERO en alter-ego,
#    sans quoi la condition pourrait etre absente sans que rien ne le voie.
#  « 1 INDIRECT damage » -> `TakeIndirectDamage`, que le joueur peut repartir
#    sur ses allies. Ce n'est pas `TakeDamage`.
#  « Spend [energy][energy] » -> `Cost("YY")`, le litteral du moteur pour deux
#    energies. Cout releve sur le scan, pas devine.


def GetAbilities() -> Sequence['Ability']:

    def orage(effect: 'Effect', message: 'Message.WhenSurgeWouldBeResolved') -> None:
        this = effect.this.CastTo(Environment)

        joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if not Player.IsType(joueur):
            return
        # « IF THEY ARE IN HERO FORM » : rien en civil.
        if not joueur.IsHero():
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(this, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(set_name="Spider-Man Noir Nemesis"),
            surge=1,
        ),
        AbilityFactory.WhenSurgeWouldBeResolved(
            AbilityType.ForcedResponse,
            None,
            orage,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YY")),
    ]
