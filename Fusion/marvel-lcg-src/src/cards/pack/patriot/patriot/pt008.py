from . import *

# Commandeer — AMELIORATION signature, custom « CptScorp »
# Cout 2, ressource [physical], trait TACTIC.
#
# Hero Action: Exhaust and discard Commandeer, choose an ally -> move 1
#   attachment from an enemy to that ally until the end of the round. Treat
#   the attachment's text box as blank and treat SCH as THW.
#
# C'est la carte la plus lourde du pack : quatre mecaniques distinctes, dont
# deux qu'aucune carte du depot ne fait ensemble. Tout ce qui suit a ete
# MESURE dans le moteur, pas suppose.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Deplacer un attachement DEJA EN JEU : `56207` (pack cw, Captain America),
#   seule carte du depot qui le fasse. Elle ecrit exactement
#   `attachement.CastTo(Attachment).AttachTo2(nouveau_porteur, effect)` avec
#   une garde `GetBindFace() != cible` pour eviter le non-evenement.
#   `AttachTo2` (attribute/can_attach.py:49-83) DETACHE TOUT SEUL de l'ancien
#   porteur (lignes 68-69) : il ne faut surtout pas appeler `DetachFrom2`,
#   qui marque la carte comme retiree et laisse a l'appelant le soin de lui
#   trouver une destination.
# - Attacher un attachement A UN ALLIE : `44041` ('Pool-ized, pack deadpool),
#   qui prouve que le moteur l'accepte. `Attachment.CanAttachTo`
#   (card_type/attachment.py:24-33) ne verifie que `max_per_unit` : AUCUNE
#   restriction de type de porteur.
# - Texte blanc temporaire : `29024` Vivian (pack ironheart), qui ecrit
#   `target.TreatAsIfBlank(effect, until_round_end=True)`.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET, ET LE COUT A **DEUX** PARTIES
#
# « Exhaust AND discard Commandeer » : les deux, pas l'un ou l'autre
# (mot-piege « and remove » du PROCESSUS-CARTE §5, celui qui a attrape
# `wd005`). `Ability.SetCostFunc` EMPILE les couts (ability.py:991-993) :
# on chaine donc `CostFunc.Exhaust("This")` puis `CostFunc.Discard("This")`,
# comme le fait `cd014` Lovers Quarrel avec ses deux inclinaisons.
#
# « choose an ally » est la troisieme partie du cout : rendue par
# `.SetTarget(Ally, range=(1, 1))`. Sans allie en jeu, aucune cible legale,
# la Hero Action n'est pas proposee.
#
# ECART ASSUME (plus severe que la carte, jamais plus permissif) : la
# capacite porte EN PLUS une condition « il existe au moins un attachement
# sur un ennemi ». A la lettre, le cout serait payable meme sans attachement
# a deplacer, et le joueur brulerait sa carte pour rien. On prefere ne pas
# proposer l'action : c'est le comportement habituel du moteur pour une
# capacite sans cible legale, et il ne rend jamais possible quelque chose que
# la carte interdit.
#
# ---------------------------------------------------------------------------
# INCONNUE (a) MESUREE : « TREAT SCH AS THW »
#
# LE MOTEUR NE SAIT PAS LE FAIRE TOUT SEUL. Verifie ligne a ligne :
#
#  - un attachement porte ses bonus dans `desc` sous les cles `ATK+`, `SCH+`
#    et `THW+`, lues nativement en `modify_atk` / `modify_sch` / `modify_thw`
#    (attribute/has_modify.py:16-24), puis reversees au PORTEUR par
#    `GiveKeywordToAttached(attack=..., scheme=..., thwart=...)`
#    (has_modify.py:33-38) — quel que soit le porteur, aucun test de type ;
#  - MAIS `face.Gain` n'applique `scheme=` que `if HasScheme.IsType(unit)`
#    (model/face_gain.py:120-125), et `Ally` (card_type/ally.py:11) n'est PAS
#    `HasScheme`. Un `SCH+` pose sur un allie est donc SILENCIEUSEMENT PERDU.
#    Rien ne plante, rien ne le signale ;
#  - aucune API de conversion n'existe : ni `UseSCHAsTHW`, ni `consider_as`
#    (model/consider_as.py ne gere que nom, trait et type de carte), ni quoi
#    que ce soit dans `face_gain.py`. Le seul precedent SCH->THW du depot est
#    `Faces.TreatAsAlly` (operate/faces.py:340, lignes 358-359), qui RECOPIE
#    `printed_scheme` dans `printed_thwart` — mais en echangeant la FACE d'un
#    sbire, ce qui n'a rien a voir avec un attachement.
#
# La conversion est donc ECRITE A LA MAIN ici, et c'est une NECESSITE, pas un
# raffinement : sans elle, la moitie « treat SCH as THW » serait inerte.
#
# INCONNUE (b) MESUREE : `TreatAsIfBlank` EMPORTE AUSSI LES BONUS
#
# `on_while.py:135-146` (`process_when_treat_as_blank`) force la valeur
# donnee a 0 des que `is_treat_as_if_blank` est vrai : rendre l'attachement
# blanc annule donc SES `ATK+`/`SCH+`/`THW+` en meme temps que son texte.
# C'est exactement ce qu'il faut ici — on les reapplique nous-memes a la
# main, sinon on les compterait deux fois.
#
# Ordre retenu, et il compte :
#   1. `AttachTo2(allie)` — le bonus est recalcule tout seul pour le nouveau
#      porteur (`on_while.py:93-99`, « Fix 31001a ») ;
#   2. `TreatAsIfBlank(..., until_round_end=True)` — texte blanc ET bonus
#      d'origine a 0 ;
#   3. `allie.GainUntilRoundEnd(effect, attack=ATK+, thwart=SCH+ + THW+)` —
#      on rend l'ATQ telle quelle et on convertit le SCH en CTR. Un `THW+`
#      deja imprime s'ajoute au meme endroit, ce qui est la seule lecture
#      possible de « treat SCH as THW ».
#
# INCONNUE (c) MESUREE : L'ATTACHEMENT REVIENT-IL A L'ENNEMI ?
#
# OUI : le texte dit « UNTIL THE END OF THE ROUND ». Ce n'est pas seulement
# le texte blanc qui est temporaire, c'est le DEPLACEMENT. On enregistre donc
# un `WhenRoundEnd` temporaire qui rend l'attachement a son porteur
# d'origine.
#
# ⚠ OU L'ENREGISTRER. Pas sur Commandeer : elle est DEFAUSSEE par son propre
# cout, et une capacite temporaire posee sur une carte qui quitte le jeu part
# avec elle (lecon `sd017`). Pas sur l'attachement non plus : il vient d'etre
# rendu BLANC, et `is_treat_as_if_blank` eteint ses capacites. On l'enregistre
# donc SUR L'ALLIE, qui reste en jeu et n'est pas blanchi.
#
# Deux cas de retour, tous deux traites :
#   - l'ennemi d'origine est encore sur le terrain -> `AttachTo2(ennemi)`.
#     `AttachTo2` refuse si la cible n'est pas sur le terrain
#     (can_attach.py:54-55), d'ou la garde explicite ;
#   - l'ennemi est mort entre-temps -> l'attachement est DEFAUSSE. Choix
#     technique documente : le texte exige qu'il quitte l'allie a la fin du
#     round, et il n'a plus de porteur legitime. Le laisser sur l'allie
#     serait un ecart PLUS PERMISSIF pour le vilain (l'allie garderait un
#     malus, ou un bonus, que la carte ne prevoit pas au-dela du round).
#
# ---------------------------------------------------------------------------
# ⚠ PAS de `SetPlay()` sur cette Hero Action (piege `66006`/`66007` du
# 4/8/2026 : `SetPlay` sur la capacite d'une AMELIORATION la rend inerte une
# fois la carte posee).


def GetAbilities() -> Sequence['Ability']:

    def attachements_sur_un_ennemi(effect: 'Effect') -> List['CardFace']:
        faces: List['CardFace'] = []
        for face in Worlds.GetOnFieldCards(effect):
            if not Attachment.IsType(face):
                continue
            porteur = face.GetBindFace()
            if porteur is not None and Enemy.IsType(porteur):
                faces.append(face)
        return faces

    def il_y_a_un_attachement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return attachements_sur_un_ennemi(effect) != []

    def commandeer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None or not effect.targets:
            return
        allie = effect.targets[0].CastTo(Ally)

        def deplacer(targets: Sequence['CardFace']) -> None:
            if not targets:
                return
            attachement = targets[0].CastTo(Attachment)
            # `.bind_face` et non `GetBindFace()` : le second porte un
            # `assert` (card_face.py:977-980) qui explose sans porteur.
            ennemi = attachement.bind_face
            if ennemi is None or ennemi == allie:
                return

            # Les bonus imprimes, releves AVANT le blanchiment (qui les met a
            # zero) : `ATK+`, `SCH+`, `THW+` (has_modify.py:16-24).
            bonus_atk = attachement.modify_atk
            bonus_thw = attachement.modify_sch + attachement.modify_thw

            # 1. Le deplacement (AttachTo2 detache tout seul de l'ennemi).
            if not attachement.AttachTo2(allie, effect):
                return

            # 2. « Treat the attachment's text box as blank » — et, du meme
            #    coup, ses ATK+/SCH+/THW+ tombent a zero.
            attachement.TreatAsIfBlank(effect, until_round_end=True)

            # 3. « treat SCH as THW » : reapplique a la main sur l'allie.
            if bonus_atk or bonus_thw:
                allie.GainUntilRoundEnd(
                    effect,
                    attack=bonus_atk or None,
                    thwart=bonus_thw or None,
                )

            # 4. « until the end of the round » : le deplacement se defait.
            def rendre(e2: 'Effect', m2: 'Message.WhenRoundEnd') -> None:
                Unused(m2)
                if not attachement.IsInPlay():
                    return
                if ennemi.card.IsOnField():
                    attachement.AttachTo2(ennemi, e2)
                else:
                    Faces.DiscardAll([attachement], e2)

            allie.effect.RegisterTemp(
                AbilityFactory.WhenRoundEnd(
                    AbilityType.Temp2,
                    None,
                    rendre,
                ),
                unregister_after_exec=True,
            )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Move 1 attachment from an enemy to that ally until the end of the round",
                deplacer,
            ).SetTarget(attachements_sur_un_ennemi, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            commandeer,
            conditions=[il_y_a_un_attachement],
        ).SetTarget(Ally, range=(1, 1))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("This")),
    ]
