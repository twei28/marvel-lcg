from . import *

# Entropy Ascendant — MANIGANCE ANNEXE NEMESIS de Quasar (QUASAR NEMESIS 2/5,
# numero imprime 239, en collision avec Goin' Rogue de Binary : suffixe q).
# Menace de depart 3 (case noire, sans icone « par joueur »), 3 icones de boost.
# Hinder 1 [per_player].
# Each event card gains requirement ([energy]).
#
# Icones relues sur l'image le 20/10/2026 (carte pivotee) : la silhouette apres
# « Hinder 1 » est l'icone « par joueur » ; l'eclair du texte est [energy]
# (decoupe contre le reskin Energy 65 du deck de Quasar, RES=YY).
#
# Cartes de reference :
#  - Hinder : base automatique (`desc.Hinder`, `"1*"` = par joueur ; fiche
#    hinder.md, RECETTES §3).
#  - **`65011`** Alontech's Greatest Achievement : manigance nemesis qui
#    modifie le cout des EVENEMENTS de CHAQUE joueur =
#    `UpdateCostOfCardInternal(CardFinder(card_type=Event), ..., "EachPlayer")`
#    sur `Message.WhenCalculateEffectCost`, capacite constante de la manigance.
#  - Requirement : fiche requirement.md ; le moteur l'encode DANS LE COUT
#    (`HasCost.GetPrintedCostWithRequirement`, has_cost.py) : « 2 dont 1
#    [mental] » = Cost « B » + 1 generique. On fait pareil : une ressource
#    generique du cout devient [energy].
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « EACH event card » : tous les evenements, de tous les joueurs (pas
#    seulement ceux du joueur Quasar), tant que la manigance est en jeu.
#  - « gains REQUIREMENT ([energy]) » : ce n'est PAS un cout en plus (fiche
#    requirement.md) : un evenement a 2 coute toujours 2, dont au moins une
#    [energy] (un joker la vaut). Seul un evenement a 0 (aucune ressource
#    generique a convertir) devient « [energy] » : il faut bien la depenser.
#  - Une capacite qui n'est pas un « jouer » (`is_play`) n'est pas touchee.


def GetAbilities() -> Sequence['Ability']:

    def exiger_une_energie(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        from game.element.rbyg import ResRBYG, ResRBYGA
        Unused(effect)
        cout = message.cost
        energie = ResRBYG(0, 0, 1, 0)
        generique = cout.rbyga.a
        if generique >= 1:
            nouveau = ResRBYGA(generique - 1, cout.rbyga.rbyg + energie)
        else:
            nouveau = ResRBYGA(generique, cout.rbyga.rbyg + energie)
        message.cost = Cost(nouveau, rule=cout.rule)

    def evenement_joue(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        return message.is_play and Event.IsType(message.check_effect.this)

    return [
        AbilityFactory.WhenCalculateEffectCost(
            AbilityType.NonKeyword,
            exiger_une_energie,
            conditions=[evenement_joue],
        ),
    ]
