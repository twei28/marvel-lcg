from . import *

# Embrace It! — evenement signature, x2. SKILL. Cout 0, ressource [mental].
# Response: After you remove a metal counter from Spider Armor, ready your
#   identity.
#
# Cartes de reference :
#  - **`34002a`** Phoenix Force pour le declencheur
#    `AfterCardRemovedCounter(..., 'power', op)` : c'est la seule fabrique qui
#    ecoute le RETRAIT d'un compteur nomme.
#  - `an001a` / `31009` / `ho011` pour `Faces.ReadyAll([identite], effect)`.
#  - `ls005` (pack lady_sif) pour la garde `IsHero()` : `Player.GetHero()`
#    leve un assert hors forme heros, avale par le moteur, et la carte ne
#    fait alors RIEN sans que rien ne le signale.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « ready **your identity** » : l'identite, pas « your hero ». Redresser
#    marche donc AUSSI en forme civile — et c'est utile, Peter Parker
#    s'inclinant pour as007 Sell It! et as011 Parker Industries.
#    `GetIdentity()`, jamais `GetHero()`.
#  - « After **you** remove » : c'est VOTRE armure. En multijoueur, celle
#    d'un autre Armored Spidey ne declenche rien (helper `EstMonArmure`).
#  - « a metal counter » : UN compteur suffit, sans condition de dernier ni
#    de nombre. Pas de `is_last_counter`.
#  - « **Response** » nu, pas « Hero Response » : la carte se joue dans les
#    deux formes, et c'est deliberé — as007 Sell It! vide l'armure en forme
#    civile, celle-ci redresse dans la foulee.
#  - ⚠ La fenetre s'ouvre pour CHAQUE retrait, y compris ceux payes par un
#    cout (as001a, as004, as006, as007, as008, as009) : c'est bien ce qui est
#    imprime, la carte ne distingue pas la source du retrait.


def GetAbilities() -> Sequence['Ability']:

    def embrace_it(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        identite = initiator.GetIdentity()
        if identite is None:
            return
        Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.Response,
            CardFinder(name=NOM_ARMURE, card_type=Upgrade),
            'metal',
            embrace_it,
            conditions=[lambda effect, message: EstMonArmure(effect, message.trigger)],
        ).SetPlay(),
    ]
