from . import *

# Quack and Burn — ATTACK. THWART — evenement, cout 2
# Hero Action (attack/thwart): Find Man-Thing and add him to your hand. Deal
#   damage to an enemy equal to Man-Thing's ATK and remove threat from a
#   scheme equal to Howard the Duck's THW.
#
# « Find Man-Thing and add him to your hand » : modele exact ok001b (Vanguard
# Leader) et ss001b (Spider Link), couple `Search.PlayerCard(...,
# include_discard_pile=True, name=...)` + `initiator.GainCard(face, effect)`.
# La recherche se fait PAR NOM, comme kb003 pour « Hawkeye » : le deck d'un
# joueur Howard ne contient que ses propres Man-Thing.
#
# Les DEUX montants sont DYNAMIQUES, lus sur les cartes :
#   - « Man-Thing's ATK » : si un Man-Thing est en jeu, sa valeur EFFECTIVE
#     (`.attack`, modifiable par d'autres cartes) ; sinon la valeur IMPRIMEE
#     (`.printed_attack`) de l'exemplaire trouve. Ce couple reprend la lecon
#     de ss022 (Forced Contract) : `.attack` d'une face qui n'est pas en jeu
#     rend 0, seul `printed_attack` est fiable hors du terrain.
#   - « Howard the Duck's THW » : `initiator.GetHero().thwart` (la face Heros
#     est active, la stat calculee est fiable — modele next_evol/cable/
#     40009.py Askani'son, qui lit exactement `initiator.GetHero().thwart`).
#
# Les deux cibles (un ennemi, une manigance) sont independantes. Le couple
# `SetTarget` + `SetTarget2` (modele il009 Vision AI) a ete ecarte apres essai :
# il fonctionne quand les deux cibles sont resolues automatiquement (il009 les
# prend « du dessus » et « du dessous » de la defausse, une seule carte legale
# chacune), mais le pilote generique de `test_capacites` ne renvoie QU'UNE
# liste de cibles par question — `effect.targets2` restait vide et la moitie
# « retrait de menace » de la carte n'etait jamais exercee (constate le
# 30/08/2026, cas hd009 rouge pour cette raison). La seconde cible passe donc
# par un `ChooseAbilities` imbrique (modele ok008 Spear Thrust / hd003), qui
# pose une question distincte et reste testable.


def GetAbilities() -> Sequence['Ability']:

    def attaque_de_man_thing(effect: 'Effect', trouve: 'CardFace|None') -> int:
        en_jeu = Worlds.FindCardOnField(effect, name=NOM_MAN_THING, card_type=Ally)
        if en_jeu is not None:
            return en_jeu.attack
        if trouve is not None:
            return trouve.printed_attack
        return 0

    def quack_and_burn(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        trouve = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_MAN_THING,
            card_type=Ally,
        )
        if trouve:
            initiator.GainCard(trouve, effect)

        degats = attaque_de_man_thing(effect, trouve)
        if degats > 0 and effect.targets:
            this.DealDamage(effect.targets, degats, effect)

        menace = initiator.GetHero().thwart
        if menace <= 0:
            return

        def nettoyer(schemes: Sequence['CardFace']) -> None:
            if schemes:
                this.RemoveThreatFromSchemes(schemes, menace, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove threat from a scheme equal to Howard the Duck's THW",
                nettoyer,
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            quack_and_burn,
        ).SetPlay().SetLabel()
        .SetTarget(Enemy),
    ]
