from . import *

# Follow My Lead — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [mental], aucun trait.
#
# Resource: Exhaust Follow My Lead -> generate a [wild] resource for an ally
#   or an upgrade that can be attached to an ally.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE : `mw006` Weaving a Web (Madame Web), qui imprime
# EXACTEMENT la meme phrase amputee de sa seconde moitie (« Resource: Exhaust
# Weaving a Web -> generate a [wild] resource for an ally ») et s'ecrit
# `CanGenerateResources(AbilityType.Resource, Resources("G"),
# CardFinder(card_type=Ally)).SetCostFunc(CostFunc.Exhaust("This"))`.
#
# ⚠ UNE SEULE `CanGenerateResources` PAR CARTE. `card_player.py:82-84` porte
# un `assert len(resources_abilities) <= 1` : deux capacites Resource sur la
# meme carte font PLANTER la construction. La restriction doit donc etre
# portee par UNE capacite, pas par deux.
#
# ---------------------------------------------------------------------------
# LA RESSOURCE EST **RESTREINTE**
#
# Le moteur sait le faire : `CanGenerateResources` accepte un filtre sur la
# carte payee. Deux voies existent, et une seule convient ici.
#
#  - `for_card=CardFinder(...)` (3e positionnel) : le filtre est evalue par
#    `for_card.Check(message.paying_for_effect.this)` (resources.py:163-166),
#    donc SANS `effect`. Or `CardFinder.check_effect_fn` n'est evalue que
#    lorsqu'un `effect` est fourni (card_finder/checker.py:473-481) : la
#    moitie « attachable a un allie », qui a besoin de connaitre les allies
#    en jeu, y serait SILENCIEUSEMENT ignoree. C'est la voie de `mw006`, et
#    elle ne suffit pas ici.
#  - `conditions=[...]` : chaque condition recoit `(effect, message)` avec
#    `message: Message.CheckPlayerCanPayCost`, dont `paying_for_effect.this`
#    est la carte en train d'etre payee (sender_player.py:247-266, meme
#    attribut que `message.for_effect.this` chez Reed Richards `mf001b`).
#    C'est la voie retenue : elle rend les DEUX moities du texte.
#
# `for_card` reste donc a `None` — les deux filtres se cumuleraient (ET).
#
# ---------------------------------------------------------------------------
# « AN UPGRADE THAT CAN BE ATTACHED TO AN ALLY »
#
# `Upgrade.CanAttachTo(face)` (card_type/upgrade.py:83-100) exige une FACE
# concrete, pas un type : on teste donc l'amelioration payee contre chaque
# ALLIE REELLEMENT EN JEU, exactement comme le fait `45017` Suit Up
# (`can_attach_to_ally`, la seule carte du depot qui pose deja cette
# question).
#
# ECART ASSUME, PLUS SEVERE QUE LA CARTE, JAMAIS PLUS PERMISSIF : sans le
# moindre allie en jeu, aucune amelioration ne passe le test, et la ressource
# ne peut plus payer qu'un ALLIE. Le moteur n'a aucun moyen de repondre
# « attachable a un allie » dans l'abstrait — la question n'a de sens que
# contre une face. Consequence en jeu : Follow My Lead ne finance pas Revenge
# tant qu'il n'y a personne a qui l'attacher, ce qui est de toute facon le
# moment ou Revenge est injouable. La restriction ne laisse donc jamais
# passer un paiement que la carte interdit.
#
# ⚠ On teste les allies de TOUS les joueurs (`Worlds.GetOnFieldAllies`) et
# pas seulement ceux du controleur : le texte dit « an ally », sans « you
# control ». En solo la difference est nulle.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET
#
# Cout = « Exhaust Follow My Lead » -> `CostFunc.Exhaust("This")`, comme
# `mw006`. Une amelioration deja inclinee ne genere rien.


def GetAbilities() -> Sequence['Ability']:

    def paye_une_carte_legale(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        payee = message.paying_for_effect.this
        if payee is None:
            return False

        # « for an ally »
        if Ally.IsType(payee):
            return True

        # « or an upgrade that can be attached to an ally »
        if not Upgrade.IsType(payee):
            return False
        for allie in Worlds.GetOnFieldAllies(effect):
            if payee.CanAttachTo(allie):
                return True
        return False

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            conditions=[paye_une_carte_legale],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
