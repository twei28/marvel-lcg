from . import *

# * Endless Power : AMELIORATION (CONDITION. SPLIT. SUPERPOWER.), cout 3, [physical]. Classe Hero.
# Sentry gets +1 ATK and gains retaliate 1.
# Hero Response: After you play an event using your "Golden Guardian" ability, exhaust this card → shuffle that event into your deck.
# Special: The Void stuns and confuses each other enemy and each character under your control.
#
# CARTES DE REFERENCE
#  - « NAME gets +1 ATK and gains retaliate 1 » : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..), control_by="You", attack=1, retaliate=1)` (`ca004`, `ra013`).
#  - « After you play an event » : `AfterPlayerPlayedCard(HeroResponse, "You", Event, op)` (RECETTES §1) ; « using Golden Guardian » : marqueur `joueur.rr_gg_evenement` pose par rr001a.
#  - Special : `AbilityFactory.WhenResolveSpecialAbility("This", op)` (RECETTES §27, `rz006`) ; statuts : `Faces.GiveStatus(cibles, "Stunned"/"Confused", effect)`.
#
# TEXTE CONTRE CODE
#  « SENTRY gets » : nom propre = la face heros. « using your Golden Guardian ability » : l'evenement DONT LE COUT a ete reduit par Golden Guardian (marqueur de rr001a), pas n'importe quel evenement.
#  « shuffle THAT event into your deck » : l'evenement qui vient d'etre joue (il est alors dans la defausse). « The Void stuns AND confuses » : le Void (en jeu) etourdit ET embrouille chaque AUTRE
#  ennemi et chaque personnage sous le controle du joueur ; sans Void en jeu le Special n'a pas d'effet. Chiffres : cout 3, +1 ATK, retaliate 1.


def GetAbilities() -> Sequence['Ability']:

    def evenement_golden(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return (joueur is not None and getattr(joueur, "rr_gg_evenement", None) is message.play_face
                and getattr(joueur, "rr_gg_phase", None) == effect.world.phase_id)

    def remelanger_l_evenement(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        evenement = message.play_face
        Faces.ShuffleAllTo([evenement], joueur.player_deck, effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        if VoidEnJeu(effect) is None:
            return
        joueur = JoueurDeCetteCarte(effect) or JoueurSentry(effect)
        cibles = [*AutresEnnemis(effect), *(PersonnagesDuJoueur(joueur) if joueur is not None else [])]
        Faces.GiveStatus(cibles, "Stunned", effect)
        Faces.GiveStatus(cibles, "Confused", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_SENTRY),
            control_by="You",
            attack=1,
            retaliate=1,
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(card_type=Event),
            remelanger_l_evenement,
            conditions=[evenement_golden],
        ).SetName("Endless Power").SetCostFunc(CostFunc.Exhaust("This")),
        # ⚠ `NoOutOfPlayLimit` : le Void resout ce Special DEPUIS LA DEFAUSSE (carte hors jeu) ; sans lui la capacite est inactive (constate le 03/11 : aucun effet).
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
