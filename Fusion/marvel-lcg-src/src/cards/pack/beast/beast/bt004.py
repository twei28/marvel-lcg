from . import *

# Experimental Warfare — evenement signature. DEFENSE. Cout 1. RES [mental]
# Interrupt (defense): Exhaust all upgrade cards in play, Beast gains +1 DEF
#   for each exhausted upgrade when defending this attack. If the attack dealt
#   "0" damage, deal 3 damage to the attacking character and ready your
#   identity.
#
# Cartes de reference :
#  - le declencheur et le bonus de defense : 03033 Expert Defense, « Hero
#    Interrupt (defense): When your hero defends against an attack, it gets +3
#    DEF for that attack », soit `WhenUnitDefendAgainstAttack(type, "YourHero",
#    op).SetPlay().SetLabel('defense')` puis
#    `message.GainDEFForThisAttack(n, effect)`. Comparable trait pour trait ;
#    seule la VALEUR du bonus change, fixe chez Expert Defense, calculee ici.
#  - la seconde phrase, qui n'agit qu'APRES la resolution de l'attaque :
#    `RunAt.AfterEnemyActivationEnd(by_effect, would_message, operation)`
#    (run_at.py:175), le point de reprise prevu pour « une fois l'activation
#    de l'ennemi terminee ».
#  - le redressement de l'identite : an001a Frenzy, `Faces.ReadyAll`.
#  - le redressement de l'identite : an001a Frenzy, `Faces.ReadyAll`.
#
# ⚠ PREMIERE VERSION ABANDONNEE, et pourquoi : la seconde phrase avait d'abord
# ete montee sur `this.effect.RegisterTemp(AbilityFactory.
# AfterUnitDefendAgainstAttack(AbilityType.Temp0, ..., take_no_damage=True,
# against_which_attack=...))`, sur le modele de ho006. La capacite temporaire
# ne s'est JAMAIS declenchee : le journal du cas montre la defense resolue a 0
# degat, puis « n'appliquent plus Experimental Warfare » sans que rien ne parte
# (01/09/2026). `RunAt.AfterEnemyActivationEnd` fait le travail sans
# intermediaire, et la condition « 0 degat » se lit alors directement sur les
# PV de l'identite, releves avant l'attaque.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : « all upgrade cards **in play** »
# n'est pas qualifie. Codee comme LES TIENNES uniquement. A la lettre, en
# multijoueur, Beast inclinerait l'equipement de toute la table pour se
# proteger seul. Consigne au §6 du journal de portage, point 10, pour l'auteur.
#
# ⚠ On ne compte QUE les ameliorations reellement inclinees par cette carte :
# une amelioration deja inclinee ne rapporte rien (« +1 DEF for each EXHAUSTED
# upgrade », c'est-a-dire pour chacune que cet effet vient d'incliner). D'ou le
# comptage sur la liste RENDUE par `Faces.ExhaustAll`, jamais sur celle qu'on
# lui a passee : la fonction ne retient que les cartes qu'elle a vraiment
# inclinees (faces.py:25).
#
# ⚠ Aucun pre-filtre sur « peut-elle etre inclinee » : `CanBeExhaust` N'EXISTE
# PAS sur une face (la methode du moteur est `CanExhaust()`, sans argument, et
# `Faces.ExhaustAll` fait deja le tri). L'appel fantome levait
# `AttributeError: 'Upgrade' object has no attribute 'CanBeExhaust'` en pleine
# defense — trouve par le cas de test le 01/09/2026, PAS par
# `verifier_api_cartes.py`, qui ne verifie que les appels de premier niveau.
#
# ⚠ « If the attack dealt "0" damage » : c'est bien 0 DEGAT ENCAISSE, pas
# « l'attaque a ete annulee ». Avec DEF 3 imprime plus le bonus, c'est le cas
# frequent, pas le cas limite — la carte est concue pour ca.
#
# ⚠ « the attacking character » = l'attaquant de CETTE attaque, pas un ennemi
# au choix (mot-piege `that <nom>`). C'est `message.attacker`.

def GetAbilities() -> Sequence['Ability']:

    def experimental_warfare(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        ameliorations = [f for f in initiator.GetControlCards() if Upgrade.IsType(f)]
        inclinees = Faces.ExhaustAll(ameliorations, effect)

        if inclinees:
            message.GainDEFForThisAttack(len(inclinees), effect)

        identity = initiator.GetIdentity()
        if identity is None:
            return
        pv_avant = identity.health

        def apres_l_attaque() -> None:
            if identity.health != pv_avant:
                return
            attaquant = message.attacker
            if attaquant is not None:
                this.DealDamage([attaquant], 3, effect)
            Faces.ReadyAll([identity], effect)

        RunAt.AfterEnemyActivationEnd(effect, message.would_atk_message,
                                      apres_l_attaque)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "You",
            experimental_warfare,
        ).SetPlay().SetLabel('defense'),
    ]
