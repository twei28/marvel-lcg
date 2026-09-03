from . import *

# * Six-Armed Spider-Man — Peter Parker (Earth-39811). Allie d'aspect
# PROTECTION, x1. VARIANT. WEB-WARRIOR. Cout 3, PV 4, CTR 1*, ATQ 2**,
# ressource [physical].
# Response: After Six-Armed Spider-Man defends against an attack, discard the
#   top 6 cards of your deck. Deal 1 damage to the attacking enemy for each
#   different card type discarded this way.
#
# Cartes de reference :
#  - **`06030`** Trickster : `player.DiscardDeckTopCards(n, effect)` puis
#    `FacesCounter.GetDifferentTypesCount(faces)`. C'est la MEME phrase
#    (« for each different card type discarded this way »), a la cible pres.
#    Voir aussi `07059` Leading the Charge et `21135` Time Stone.
#  - `bt012` / `42018` * Angel's Aerie pour
#    `AfterUnitDefendAgainstAttack(Response, "This", op)`.
#  - `message.attacker` (Message.AfterUnitDefendEnd) pour « the attacking
#    enemy », modele `an006` et `bt004`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After **Six-Armed Spider-Man** defends » : CET allie, pas le heros ni
#    un autre personnage. `who_defense="This"`.
#  - « the **attacking** enemy » : celui qui vient d'attaquer, lu dans le
#    message, pas un choix offert au joueur (piege `that <nom>`).
#  - « for each **different** card type » : le nombre de types DISTINCTS,
#    pas le nombre de cartes. Six evenements defausses valent 1 degat.
#    `GetDifferentTypesCount`, jamais `len(faces)`.
#  - « **your** deck » : le deck du joueur qui controle l'allie.
#  - Aucune condition de degats subis : contrairement a `as018` Just a
#    Ricochet, la reponse tombe meme si l'allie a encaisse. Pas de
#    `take_no_damage`.
#  - Un deck de moins de 6 cartes ne fait pas tomber la capacite : le moteur
#    defausse ce qu'il peut (et remelange si la regle l'impose).


def GetAbilities() -> Sequence['Ability']:

    def six_armed_spider_man(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        faces = initiator.DiscardDeckTopCards(6, effect)
        types = FacesCounter.GetDifferentTypesCount(faces)
        if types <= 0:
            return

        attaquant = message.attacker
        if attaquant is None:
            return
        this.DealDamage([attaquant], types, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "This",
            six_armed_spider_man,
        ),
    ]
