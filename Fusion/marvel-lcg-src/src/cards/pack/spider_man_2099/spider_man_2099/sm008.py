from . import *

# Accelerated Vision — AMELIORATION, cout 1 [mental]. CONDITION. SUPERPOWER.
# You may resolve your Acceleration ability one additional time per phase
#   (but still once per trigger).
# When resolving your Acceleration ability, you may continue discarding until
#   you discard a different event and may play that instead.
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce : une carte qui REAGIT a une capacite nommee
#    portee par une AUTRE carte, par
#    `WhenResolveSpecialAbility(CardFinder(...), op)`. C'est le montage exact
#    de la seconde phrase, branchee sur le message `NOM_ACCEL_DEBUT` que
#    `sm001a` envoie avant de defausser.
#  - `sm001a` pour l'autre bout du fil.
#
# TEXTE CONTRE CODE
#  ⚠ « ONE ADDITIONAL TIME PER PHASE » : c'est la raison pour laquelle la
#    limite d'Acceleration n'est PAS un `LimitOncePerPhase()` du moteur, qui
#    ne sait pas compter jusqu'a deux. `LimiteAcceleration` (helper du pack)
#    rend 2 quand cette carte est en jeu.
#    ⚠⚠ ET C'EST UN ECART DE SUBSTITUTION ASSUME : ce bonus-la est lu par la
#    PRESENCE de la carte, pas par son module. Substituer `sm008` par un
#    module vide laisse donc le « +1 usage » en place, et le cas qui le mesure
#    reste VERT. Le journal doit le dire (PROCESSUS-CARTE §7.3 : « un
#    contre-cas qui reste vert sous substitution s'assume, il ne se maquille
#    pas »). La SECONDE phrase, elle, mord : sans le module, le drapeau de
#    continuation n'est jamais pose.
#  ⚠ « but still ONCE PER TRIGGER » : un meme pouvoir de base ne peut pas
#    declencher Acceleration deux fois. Rien a coder : le moteur n'envoie
#    `AfterUnitUseBasicPower` qu'une fois par pouvoir, et une Response ne se
#    resout qu'une fois par message.
#  ⚠ « until you discard a DIFFERENT event » : different de CELUI QU'ON VIENT
#    DE DEFAUSSER, pas « d'un autre nom ». `sm001a` compare donc les FACES
#    (`f is not evenement`), jamais les card_id — le deck contient deux
#    exemplaires de quatre evenements du pack.
#  ⚠ « and MAY PLAY THAT INSTEAD » : « instead » remplace le premier
#    evenement ; celui-ci ne reste pas jouable. L'insert dit ou il va :
#    « Place it on the bottom of your deck with the other discarded cards. »
#    C'est ce que fait `sm001a`.
#  ⚠ « YOU MAY continue » : c'est optionnel, donc une question — posee par
#    `sm001a` au moment ou le premier evenement est connu, pas ici : au
#    moment ou cette carte parle, rien n'a encore ete defausse.
#  ⚠ Aucune limite imprimee sur CETTE carte : etape 7 bis sans objet (la
#    limite qu'elle modifie est celle de sm001a, dont le temoin d'epuisement
#    doit exister EN DEUX VERSIONS : sans cette carte, la 2e tentative est
#    refusee ; avec elle, la 2e passe et la 3e est refusee).


def GetAbilities() -> Sequence['Ability']:

    def autoriser(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        AutoriserContinuation(joueur)

    return [
        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(card_ids=[ID_HEROS]),
            autoriser,
        ).SetName(NOM_ACCEL_DEBUT),
    ]
