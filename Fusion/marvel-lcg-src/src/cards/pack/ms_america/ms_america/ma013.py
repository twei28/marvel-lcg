from . import *

# Star Portal — EVENEMENT signature, custom « jakxin »
# Cout 2, [wild], trait SUPERPOWER. Deux exemplaires physiques : ma013 et
# ma014, meme texte, meme code.
#
# Hero Action: Search any player's discard pile for an ally and put it into
#   any player's play area exhausted → remove threat from a scheme equal to
#   that ally's THW and deal damage to an enemy equal to that ally's ATK.
#
# ---------------------------------------------------------------------------
# LA CARTE EST MULTIJOUEUR DES DEUX COTES
#
# « ANY PLAYER'S discard pile » et « ANY PLAYER'S play area » : ni « your »,
# ni « you control ». En solo la difference est nulle, en multijoueur elle est
# majeure — Ms. America peut ressusciter l'allie d'un coequipier et le poser
# chez un troisieme. On ne restreint donc rien (mot-piege `you control` du
# PROCESSUS-CARTE §5).
#
# Le joueur de destination est une CIBLE de la capacite,
# `.SetTarget("Players", range=(1, 1))` — idiome de `01092` Helicarrier et de
# `51014` Manifold, ou `effect.targets[0].GetControlByPlayer()` rend le
# joueur choisi.
#
# La defausse fouillee, elle, ne peut pas etre une cible : `Search.PlayerCard`
# n'a pas d'option « n'importe quel joueur » (son argument `player` designe a
# la fois le proprietaire de la pile ET celui qui choisit,
# search_internal.py:77). On rassemble donc a la main les allies de TOUTES
# les defausses et on les propose en une seule liste, ce qui revient au meme
# pour le joueur et evite une question par joueur.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT — ECART DE CONSTRUCTION DOCUMENTE
#
# Le cout est « trouver un allie dans une defausse et le poser incline ».
# Aucune `CostFunc` du moteur ne sait le dire : `CostFunc.SearchForCard`
# (cost_func.py:979-1040) ne fouille que les zones de RENCONTRE, ne sait pas
# poser incline et ne sait pas viser un autre joueur. On rend donc la
# capacite INDISPONIBLE par une `conditions=` — « aucun allie dans aucune
# defausse = carte injouable » — exactement comme `pt017` branche 1, seule
# construction possible ici. Le corps re-verifie avant d'agir : si la
# recherche ne rend rien, AUCUN des deux effets ne part.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « put it into any player's play area EXHAUSTED » -> `PutIntoPlay(joueur,
#   effect, under_control=True, exhaust=True)` (face_on_event.py:170) :
#   `under_control=True` donne la propriete au joueur choisi,
#   `exhaust=True` enregistre l'inclinaison a l'entree en jeu
#   (face_on_event.py:189-202). Seul precedent du depot : `50088b`.
# « equal to that ally's THW » / « that ally's ATK » -> valeurs COURANTES
#   (`face.thwart`, `face.attack`), lues APRES l'entree en jeu pour que les
#   ameliorations deja posees chez le joueur de destination comptent. Le
#   mot-piege `that <nom>` est verifie : c'est bien LE MEME allie dans les
#   deux moities de la phrase, jamais un autre.
# « remove threat ... AND deal damage ... » -> deux CONSEQUENCES reliees par
#   « and », SANS fleche : les deux se resolvent toujours (`02021` Pumpkin
#   Bombs). Une valeur nulle ne fait simplement rien.
# « Hero Action » sans libelle imprime -> `.SetPlay()` sans `.SetLabel(...)`.


def GetAbilities() -> Sequence['Ability']:

    def allies_des_defausses(effect: 'Effect') -> List['CardFace']:
        faces: List['CardFace'] = []
        for joueur in Worlds.GetPlayers(effect):
            faces.extend(joueur.discard_pile.FindCards(card_type=Ally))
        return faces

    def star_portal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        candidats = allies_des_defausses(effect)
        if not candidats:
            return

        # « any player's play area » : le joueur de destination est la cible
        # de la capacite. En solo c'est toujours le joueur actif.
        destination = initiator
        if effect.targets:
            joueur = effect.targets[0].GetControlByPlayer()
            if joueur is not None:
                destination = joueur

        allie = initiator.MayChooseOneText(candidats)
        if allie is None:
            return

        allie.PutIntoPlay(destination, effect, under_control=True, exhaust=True)

        menace = max(0, getattr(allie, 'thwart', 0))
        degats = max(0, getattr(allie, 'attack', 0))

        if menace > 0:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Star Portal: remove threat from a scheme",
                    lambda targets:
                        this.RemoveThreatFromSchemes(list(targets), menace, effect),
                ).SetTarget(Scheme2),
            )

        if degats > 0:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Star Portal: deal damage to an enemy",
                    lambda targets:
                        this.DealDamage(list(targets), degats, effect),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            star_portal,
            conditions=[
                lambda effect, message: allies_des_defausses(effect) != [],
            ],
        ).SetPlay()
        .SetTarget("Players", range=(1, 1)),
    ]
