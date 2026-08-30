from . import *

# * Isaiah Bradley — SOUTIEN signature, custom « CptScorp »
# Cout 1, ressource [energy], trait PERSONA.
#
# You get +1 REC.
# Alter-Ego Action: Exhaust Isaiah Bradley -> heal 2 damage from Elijah
#   Bradley.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `iw003` Central City Estate (Invisible Woman,
# OFFICIELLE) et `gp007` Gwen's Room, qui impriment mot pour mot la meme
# structure (« You get +1 REC. » + « Alter-Ego Action: Exhaust X -> heal N
# damage from <alter-ego> »). Meme couple exact :
# `*AbilityFactory.GiveKeywordToAttached("You", recover=1)` puis
# `WhenInYourPlayTurn(AbilityType.AlterEgoAction, ...)`
# `.SetCostFunc(CostFunc.Exhaust("This"))`.
#
# ⚠ `GiveKeywordToAttached` sur un SOUTIEN n'est pas un abus de langage : la
# cible-chaine `"You"` designe l'identite du controleur, pas un porteur
# d'amelioration. C'est ainsi que les deux cartes de reference sont ecrites,
# et elles sont vertes au harnais.
#
# ⚠ Rend une LISTE d'abilites (l'etoile n'est pas optionnelle).
#
# LE BONUS DE REC N'A D'EFFET QU'EN ALTER-EGO : seule la face `pt001b` porte
# une valeur REC (3 imprimee -> 4 avec le soutien). C'est voulu : REC ne sert
# qu'en identite civile.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « Exhaust Isaiah Bradley » -> `CostFunc.Exhaust("This")`. Le soutien
# deja incline n'est pas propose (`canbe_exhaust=True` ajoute par la fabrique
# de cout, cost_func.py:227).
#
# « heal 2 damage from ELIJAH BRADLEY » : le texte NOMME l'alter-ego. Comme
# la capacite est deja `AlterEgoAction`, la face en jeu EST Elijah Bradley :
# on passe par `initiator.GetIdentity()` (la face reellement en jeu) plutot
# que par un `CardFinder(name="Elijah Bradley")`, qui chercherait un nom dans
# tout le monde. Meme montage que `gp007` (« heal 1 damage from Gwendolyn
# Poole » -> `HealthUnits([initiator.GetIdentity()], 1, effect)`).
#
# ---------------------------------------------------------------------------
# COUPLAGE AVEC L'OBLIGATION pt017
#
# `pt017` MGH Addiction propose « Discard the Isaiah Bradley support card ->
# remove MGH Addiction from the game ». C'est pt017 qui cherche cette carte
# (par `NOM_ISAIAH`, constante partagee du set) ; il n'y a rien a prevoir
# ici. Si ce soutien n'est pas en jeu, la branche de l'obligation est
# indisponible : voir pt017.py.


def GetAbilities() -> Sequence['Ability']:

    def isaiah_bradley(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        this.HealthUnits([initiator.GetIdentity()], 2, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            isaiah_bradley,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetName("Heal 2 damage from Elijah Bradley"),
    ]
