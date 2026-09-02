from . import *

# All-Black Necroverse — ENVIRONNEMENT, face B de gb007a (Godbomb). NECROVERSE.
# Le complot 3A retourne la carte sur cette face, ou la pose directement.
#
# While All-Black Necroverse has the following number of necro counters:
# • 3[per_hero]: Gorr the God Butcher's attacks gain overkill.
# • 6[per_hero]: All NECROVERSE enemies get +1 ATK.
# • 9[per_hero]: All NECROVERSE enemies get +1 SCH.
# • 12[per_hero]: The players lose the game.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Bonus continu donne par un environnement : 50090b (Alert Level),
#   `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...), scheme=1,
#   attack=1)`. Ici les bonus sont CONDITIONNELS : la fabrique accepte un
#   `condition` (environment.py:71) et un `change_on_event`
#   (environment.py:116) pour recalculer.
# - Recalcul quand un compteur bouge : `OnEvent.Counter("This", 'necro')`
#   (message/on_event/on_event.py:635). Sans lui, les paliers seraient figes
#   a l'etat du plateau au moment ou l'environnement est entre en jeu — c'est
#   exactement le piege paye sur al001a (le malus ne suivait pas
#   l'accrochage).
# - Defaite au seuil : 39003b (The Champion), `IfThereAreAtLeastCounterHere`.
# - Overkill permanent sur les attaques d'un personnage : 50107b (M.O.D.O.K.),
#   `UnitAttackGainKeyword("This", overkill=True)`. Ici c'est une AUTRE carte
#   qui l'accorde, donc `CardFinder(name=...)` a la place de "This".
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « WHILE ... has the following number » -> effets CONTINUS, pas des reponses :
#   ils s'allument et s'eteignent avec le nombre de compteurs.
# « 3[per_hero] », « 6[per_hero] », « 9[per_hero] », « 12[per_hero] » -> tous
#   par joueur : "3*", "6*", "9*", "12*". `GetPlayerNumValue` fait le calcul.
# « GORR THE GOD BUTCHER's attacks » -> le vilain nomme, pas tous les
#   NECROVERSE : le premier palier est plus etroit que les deux suivants.
# « ALL NECROVERSE ENEMIES » -> les ennemis (vilain ET sbires) qui portent le
#   trait, Gorr compris (il l'a imprime).
# « +1 ATK » puis « +1 SCH » -> deux paliers distincts qui se cumulent a 9.
#
# ⚠ Les paliers ne se remplacent pas : a 9 compteurs, les trois premiers sont
# actifs en meme temps.


def GetAbilities() -> Sequence['Ability']:

    def au_moins(seuil: str) -> Callable[['Effect'], bool]:
        """Vrai quand cette carte porte au moins `seuil` compteurs `necro`."""
        def verifier(effect: 'Effect') -> bool:
            this = effect.this
            return this.GetCounters('necro') >= this.FormatPlayerNumValue(seuil)
        return verifier

    return [
        # Palier 3 : les attaques de Gorr gagnent overkill. Overkill n'est PAS
        # un mot-cle de `GiveKeywordToInPlayWhenApplyThis` (il n'existe aucune
        # cle `desc` non plus, cf. mots-cles/overkill.md) : il se donne a
        # l'ATTAQUE, par `UnitAttackGainKeyword`, dont le `conditions` est
        # evalue a chaque attaque — donc toujours a jour, sans
        # `change_on_event`.
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name=NOM_GORR),
            overkill=True,
            conditions=[lambda effect, message: au_moins("3*")(effect)],
        ),
        # Palier 6 : +1 ATQ a tous les ennemis NECROVERSE.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="NECROVERSE", card_type=Enemy),
            condition=au_moins("6*"),
            change_on_event=OnEvent.Counter("This", 'necro'),
            attack=1,
        ),
        # Palier 9 : +1 MNG a tous les ennemis NECROVERSE.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="NECROVERSE", card_type=Enemy),
            condition=au_moins("9*"),
            change_on_event=OnEvent.Counter("This", 'necro'),
            scheme=1,
        ),
        # Palier 12 : les joueurs perdent.
        AbilityFactory.IfThereAreAtLeastCounterHere(
            "12*",
            'necro',
            lambda effect, message: Worlds.SetGameOver(False, effect),
        ),
    ]
