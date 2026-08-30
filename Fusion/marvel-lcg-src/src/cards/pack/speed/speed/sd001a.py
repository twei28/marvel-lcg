from . import *

# * Speed (face heros) — custom « CptScorp »
# YOUNG AVENGER. PV 9 / ATQ 1 / CTR 1 / DEF 2 / main 5.
# Hyperkinetic Fuel — Interrupt: When you pay for an event with only [energy]
#   resources, put an explosive counter on an enemy or scheme. (See insert.)
#
# ---------------------------------------------------------------------------
# DECLENCHEUR -> `AbilityFactory.WhenPlayerWouldPlayCard(AbilityType.Interrupt,
# "You", Event, ...)` (factory/play.py:191). C'est LE moment exact du texte :
# `CardPlayer.Play` (card_player.py:134-139) paie d'abord le cout
# (`ProcessSelfCost`), envoie ENSUITE `WhenPlayerWouldPlayCard`, et ne resout
# l'evenement (`ResolveSelf`) qu'apres. « When you PAY FOR an event » tombe
# donc exactement la, et le compteur est pose AVANT que l'evenement se
# resolve.
#
# C'est TOUT le design du pack : Blasting Velocity (sd003/sd004), Kinetic
# Flurry (sd006/sd007) et Swift Strikes (sd008-sd010) trouvent ensuite une
# cible DEJA marquee. Ne jamais transformer cet Interrupt en Response.
#
# `which_card=Event` : le texte dit « an event », pas « a card ». Les
# ameliorations, soutiens et allies payes en energie ne declenchent rien.
#
# ---------------------------------------------------------------------------
# « ONLY [ENERGY] RESOURCES » -> `message.paid_resources.OnlyHasColor("Y")`.
# C'est la convention du MOTEUR pour ce libellé officiel exact : Hulk Smash
# (10003), Sub-Orbital Leap (10004), Limitless Strength (10006), Venom 20006,
# Gamma Strike bw006 emploient tous `OnlyHasColor` pour « you paid for this
# card using only [X] resources ».
#
# Deux consequences, VOULUES, de `ResRBYG.OnlyHasColor` (element/rbyg.py:47) :
#   - `y + g == total` : le WILD compte comme energie. Une main de wilds
#     declenche donc Hyperkinetic Fuel. C'est la regle du jeu (« un wild vaut
#     n'importe quelle couleur »), pas une facilite ;
#   - `if self.total == 0: return False` : un evenement paye ZERO ressource
#     (cout 0, ou cout entierement reduit) ne declenche JAMAIS la capacite.
#     Coherent avec « when you PAY FOR an event » : sans paiement, rien.
#
# ---------------------------------------------------------------------------
# LA CIBLE -> `PoserUnCompteurExplosif` (speed/speed/__init__.py), qui pose la
# question via un `ChooseAbilities` a une branche `.SetTarget("Enemy|Scheme")`
# plutot que via un `.SetTarget` sur cette capacite-ci. Raison : la branche
# sd005 ci-dessous ne doit PAS demander de cible, et un selecteur declare sur
# la capacite la reclamerait quand meme.
#
# Aucune limite imprimee : chaque evenement paye uniquement en energie pose un
# compteur. Le plafond de 1 PAR CARTE (insert) est porte par
# `ReglesDesCompteursExplosifs`, pas par une limite de declenchement.
#
# ---------------------------------------------------------------------------
# LE « INSTEAD » DE sd005 « I'm Out » -> la carte payee est-elle dans
# `CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL` ? Le texte de sd005 dit « If you
# would RESOLVE Speed's Hyperkinetic Fuel ability when playing this event,
# ... INSTEAD » : c'est la resolution de CETTE capacite-ci qui est remplacee,
# donc le test appartient a cette capacite-ci, pas a sd005 qui n'a aucun moyen
# de se voir en train d'etre payee. La ressource imprimee de sd005 est
# MENTALE : le cas « payee uniquement en energie » est reel (wilds, Never
# Ending Spark, Top Speed) mais jamais automatique.
#
# L'INTERRUPTEUR de l'obligation sd017 est une CONDITION de declenchement
# (« You cannot RESOLVE Speed's Hyperkinetic Fuel Interrupt ») : quand il est
# leve, rien ne part — ni compteur, ni branche sd005.
#
# ---------------------------------------------------------------------------
# LES DEUX REGLES TRANSVERSES de l'insert sont ajoutees ici ET sur sd001b :
# elles n'appartiennent a aucune carte, elles doivent survivre a un changement
# de forme, et le balayage doit tomber meme si Speed finit la phase en
# alter-ego. Voir le grand commentaire de speed/speed/__init__.py.


def GetAbilities() -> Sequence['Ability']:

    def paye_uniquement_en_energie(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> bool:
        return message.paid_resources.OnlyHasColor("Y")

    def capacite_active(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> bool:
        Unused(message)
        return HyperkineticFuelActif(effect)

    def hyperkinetic_fuel(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        player = message.GetToPlayer()
        card_id = getattr(message.play_face.paper, "card_id", None)

        if card_id in CARTES_QUI_REMPLACENT_HYPERKINETIC_FUEL:
            RemonterUnEvenementEtPiocher(player, effect)
            return

        PoserUnCompteurExplosif(player, effect)

    return [
        AbilityFactory.WhenPlayerWouldPlayCard(
            AbilityType.Interrupt,
            "You",
            Event,
            hyperkinetic_fuel,
            conditions=[paye_uniquement_en_energie, capacite_active],
        ).SetName("Hyperkinetic Fuel"),
        *ReglesDesCompteursExplosifs(),
    ]
