from . import *

# Asteroid Belt — ENVIRONNEMENT. LOCATION. SETTING.
#
# Uses (2[per_hero] asteroid counters).
# Forced Response: After the end of the player phase, each player takes 2
#   indirect damage.
# Hero Action: Exhaust your hero → remove X asteroid counters from here, where
#   X is the highest of your ATK, THW, or DEF.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Uses` : BASE AUTOMATIQUE au format `"N,nom"` — ici `"2*,asteroid"`
#   (has_uses.py). Le moteur pose les compteurs a l'entree en jeu ET DEFAUSSE
#   LA CARTE quand le dernier part : c'est ainsi que l'environnement se
#   retire, il n'y a rien a scripter pour ca.
# - Le compteur `asteroid` est declare dans `CardFace.COUNTER` (extension du
#   pack) : sans lui, `IsCounter` refuse le nom et la carte tombe.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Environnement a compteurs `Uses` : 27174a (Public Outcry), meme montage.
# - « After the end of the player phase » : `WhenPhaseEnd("Player")`, la
#   fabrique employee par gb018 pour la phase du vilain.
# - Action de heros qui s'incline : 50090b (Alert Level), `WhenInYourPlayTurn`
#   + `CostFunc.Exhaust("YourHero")`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After the END OF THE PLAYER PHASE » -> une fois par tour, pas a chaque
#   fin de tour de joueur.
# « EACH player takes 2 INDIRECT damage » -> tous les joueurs, degats
#   indirects.
# « Exhaust YOUR HERO » -> le COUT (fleche) : l'action n'est pas jouable si le
#   heros est deja incline, et elle n'existe qu'en forme heros.
# « X is the HIGHEST of your ATK, THW, or DEF » -> le meilleur des trois, pas
#   leur somme.


def GetAbilities() -> Sequence['Ability']:

    def pluie_d_asteroides(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this
        Unused(message)

        def frapper(joueur: 'Player') -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 2, effect)

        Players.ForEachPlayer(effect, frapper)

    def deblayer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)

        heros = Select.GetYou(effect)
        if not isinstance(heros, Player):
            return
        identite = heros.GetIdentity()
        if identite is None:
            return
        meilleur = max(identite.attack, identite.thwart, identite.defense)
        if meilleur > 0:
            Faces.RemoveCountersOn([this], meilleur, 'asteroid', effect)

    return [
        AbilityFactory.WhenPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            pluie_d_asteroides,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deblayer,
        ).SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
