from . import *

# Lurking — amelioration signature, x3 (al014 R, al015 B, al016 Y).
# PREPARATION. Cout 0. Max 1 per player.
# Hero Response: After a minion enters play, discard Lurking → Alligator Loki
#   makes a basic attack against that minion without exhausting. Alligator
#   Loki gets +1 ATK for this attack.
#
# ⚠ al015 et al016 n'ont PAS de module : `ability_link` vers al014
# (database.py:124). Meme texte, icone de ressource differente, portee par
# `desc`.
#
# Cartes de reference :
#  - an006 : « discard this card → » est un COUT, `CostFunc.Discard("This")` ;
#  - bw024 Strong as Silk : « makes a basic attack without exhausting » ->
#    `heros.BasicAttack([cible], effect)`, qui n'incline rien (c'est l'action
#    de base du joueur qui incline, pas l'attaque) ;
#  - 19029, 16117 : « +1 ATK for this attack » ->
#    `AttackProperty(additional_value=1)`, lu par `GetDamage`
#    (can_attack.py:33) ;
#  - `AfterCardEnterPlay(HeroResponse, Minion, op)` (card_move.py:113) pour
#    « after a minion enters play ».
#
# ⚠ « Max 1 per player » : cle `MaxPerUnit` de `desc`, la seule limite par
# porteur que le moteur connaisse (has_max_per.py:10) ; l'amelioration etant
# attachee a l'identite, « par unite » et « par joueur » coincident. Aucune
# cle `MaxPerPlayer` n'existe dans les 5000 cartes du depot.
# ⚠ « A minion », sans « engaged with you » : un sbire qui entre chez un autre
# joueur declenche aussi. Et Lurking, une fois defaussee, retourne dans la
# defausse ou Butterfly Swamp (al011) peut la repecher.
# ⚠ Le sbire peut avoir quitte le jeu entre l'entree et la reponse (When
# Revealed qui le defausse, par exemple) : on verifie avant d'attaquer.

def GetAbilities() -> Sequence['Ability']:

    def lurking(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        joueur = effect.GetInitiator()
        heros = joueur.GetHero() if joueur else None
        sbire = message.trigger
        if heros is None or sbire is None or not sbire.card.IsOnField():
            return
        heros.BasicAttack(
            [sbire], effect,
            property=AttackProperty(additional_value=1),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            lurking,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
