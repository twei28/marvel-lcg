from . import *

# Top Speed (exemplaire 1/2) — carte RESSOURCE signature, custom « CptScorp »
# [energy], classe Hero, aucun trait, aucun cout (c'est une ressource).
# Interrupt: When you spend this card, you may generate an additional [energy]
#   resource ([energy][energy] instead if there is an explosive counter in
#   play). If you do, you cannot play cards for the rest of the turn.
#
# Exemplaire physique 1 de 2 (sd011, sd012). Commentaire complet ici, pointeur
# bref sur sd012.
#
# ---------------------------------------------------------------------------
# MODELE EXACT : `58006` Energy Siphon (Wonder Man) — « Hero Interrupt: When
# you spend this card, take up to 3 damage -> this card generates 1 additional
# [energy] resource for each damage taken this way ». Meme forme, au mot pres :
# une ressource dont le RENDEMENT est decide au moment ou on la depense.
#
# Le couple d'abilites est celui de 58006, et il n'y en a pas d'autre dans le
# depot :
#   1. `AbilityFactory.DoDiscardThisToGenerateResources(AbilityType.Interrupt,
#      res_fn=...)` + `.SetCostFunc(CostFunc.Custom(None, ...))` : le
#      `CostFunc` est execute AU MOMENT DE LA DEPENSE, avant que `res_fn` ne
#      soit lu. C'est la qu'on pose la question « you may » et qu'on retient le
#      supplement ;
#   2. `AbilityFactory.CheckThisCanDropPay(...)` : ce que la carte ANNONCE
#      pouvoir couvrir avant qu'on la depense. Sans cette seconde capacite, le
#      moteur ne proposerait jamais Top Speed pour financer un cout de 2 ou 3,
#      et le bonus serait inatteignable.
#
# Ces deux capacites ne sont PAS deux `CanGenerateResources` : l'assert de
# `ClassCard.GetAbilities` (card_player.py:83-84) n'en tolere qu'une, et
# aucune des deux ne porte ce nom de fonction (« DiscardPay » et
# « CheckThisCanDropPay »). C'est justement pour ca que 58006 est le modele.
#
# ---------------------------------------------------------------------------
# « YOU MAY » -> `joueur.ChooseAbilities(effect, ForChoiceAbility(...)
# .SetHasNoTargetEffect(), forced=False)`, l'idiome du depot pour un choix
# REFUSABLE (modele `determination/__init__.py:64-71`, « Take 1 damage to
# return this card to your hand »). Une seule option est proposee ; la refuser
# est une reponse legale du protocole.
# 58006 emploie `DeclareNumber(0, 3)` parce que son supplement est une PLAGE ;
# ici le texte n'offre pas de plage : c'est tout ou rien.
#
# ⚠ NE PAS PROPOSER DEUX OPTIONS FORCEES (« prendre » / « refuser ») via
# `AskChooseOneText` ou `MayChooseOneAbility` : ecrit ainsi d'abord, le pack a
# produit une `AssertionError: True` en autoplay
# (`engine/controller/controller.py:274`, avalee en silence). Cause : le
# garde-fou anti-repetition du pilote (`MAX_REPETITIONS`, tools/autoplay.py:47)
# epuise ses deux options quand les DEUX exemplaires de Top Speed financent le
# MEME paiement — meme question, meme empreinte de plateau — puis repond « 0 »,
# ce que `ChoiceOne` refuse sur un choix FORCE a plus d'une option. Avec
# `forced=False`, « 0 » est une reponse legale : le refus est le refus, et
# l'assertion ne peut plus partir. Constate et corrige le 30/08/2026.
#
# « [ENERGY][ENERGY] INSTEAD IF THERE IS AN EXPLOSIVE COUNTER IN PLAY » : le
# supplement vaut 2 au lieu de 1, jamais « jusqu'a 2 ». « in play » = N'IMPORTE
# OU en jeu (`IlYAUnCompteurExplosifEnJeu`), rien n'exige que le compteur soit
# sur une cible du joueur de Speed ni que Speed l'ait pose.
#
# ---------------------------------------------------------------------------
# « IF YOU DO, YOU CANNOT PLAY CARDS FOR THE REST OF THE TURN » ->
# `AbilityFactory.PlayersCannotPlayCardWhile(joueur)` (factory/player.py:8),
# enregistree en TEMPORAIRE sur l'IDENTITE (jamais sur la carte, qui part en
# zone de ressources puis a la defausse) avec `until_turn_end=True` — le TOUR
# (`Turn`), pas le round : c'est le mot imprime.
#
# ⚠ POINT RISQUE, verifie par un cas de test dedie : la restriction ne doit
# PAS bloquer la carte qu'on est justement en train de payer, sinon Top Speed
# n'a aucun sens. Elle ne le fait pas, parce que `PlayersCannotPlayCardWhile`
# repond a `Message.CheckEffectCondition` et que la jouabilite de la carte
# financee a deja ete etablie quand `ProcessSelfCost` appelle le `CostFunc` :
# la carte en cours part, les SUIVANTES sont bloquees. Le cas
# « sd011 ... la carte payee part quand meme » est la pour que ce point ne
# reste pas une croyance.
#
# La restriction n'est posee QUE si le joueur a pris le supplement
# (« if you do ») : refuser le bonus laisse le tour intact.


def GetAbilities() -> Sequence['Ability']:

    class Supplement:
        # Retenu entre le `CostFunc` (qui pose la question) et `res_fn` (qui
        # rend les ressources) : meme technique que `SiphonState` dans 58006.
        valeur = 0

    def supplement_disponible(effect: 'Effect') -> int:
        return 2 if IlYAUnCompteurExplosifEnJeu(effect) else 1

    def demander_le_supplement(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        Supplement.valeur = 0

        joueur = effect.GetInitiator()
        if joueur is None:
            return True

        supplement = supplement_disponible(effect)

        def prendre_le_supplement(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Supplement.valeur = supplement
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.effect.RegisterTemp(
                    AbilityFactory.PlayersCannotPlayCardWhile(joueur),
                    unregister_after_exec=False,
                    until_turn_end=True,
                )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Generate {supplement} additional [energy] resource(s) — you cannot play cards for the rest of the turn",
                prendre_le_supplement,
            ).SetHasNoTargetEffect(),
            forced=False,
        )
        return True

    def ressources_generees(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        return Resources("Y" * (1 + Supplement.valeur))

    def ressources_annoncees(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        return Resources("Y" * (1 + supplement_disponible(effect)))

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(
            AbilityType.Interrupt,
            res_fn=ressources_generees,
        ).SetCostFunc(CostFunc.Custom(None, demander_le_supplement)),
        AbilityFactory.CheckThisCanDropPay(ressources_annoncees),
    ]
