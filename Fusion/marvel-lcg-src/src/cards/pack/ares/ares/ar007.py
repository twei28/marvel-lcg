from . import *

# God of War — AMELIORATION, cout 2, [wild]. OLYMPUS. TITLE. x1.
# Hero Response: After a minion enters play, search your deck for a TACTIC
#   upgrade that can be attached to that minion and play it on that minion.
#   (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `br009` Oathbrother (pack beta_ray_bill) : « Hero Response: After a minion
#    enters play, seek ... (Limit once per phase.) », la meme fenetre
#    `AfterCardEnterPlay(HeroResponse, Minion, op)` + `LimitOncePerPhase()`.
#  - `an001b` / `ho007` : `Search.PlayerCard(finder=CardFinder(...,
#    check_face_fn=...))`.
#  - `bc004` Big Heist / `dz031` Tribute : jouer une carte trouvee hors de la
#    main = `Faces.AddToHand` PUIS `PlayCardsLikeInTurn` (une carte hors main
#    n'est pas jouable, ability.py:235).
#  - `yd012` Yaka Arrow (pack yondu) : `AttachTo2(cible, effect)`, la seule
#    voie pour DEPLACER une amelioration deja en jeu vers un autre hote.
#
# TEXTE CONTRE CODE
#  ⚠ « that CAN BE ATTACHED to that minion » -> helper `PeutSAttacherA` : on
#    pose au moteur sa propre question (`Message.CheckIfFaceCanAttachTo`, que
#    `ar012` Athena ecoute pour refuser les TACTIC) puis « Max 1 per enemy ».
#    Un sbire qui a deja un Feint ne recoit pas un second Feint.
#  ⚠ « and PLAY it on that minion » -> ARBITRAGE UTILISATEUR DU 07/09/2026 : la
#    carte est JOUEE, son cout en ressources est PAYE (`PlayCardsLikeInTurn`
#    sans `ignore_resources_cost`). Feint, Reeling et Sundered coutent 0 ; une
#    amelioration TACTIC d'aspect empruntee par Lord of War coute son prix, et
#    l'obligation Ire of Athena (+1 par TACTIC) s'applique. Si le joueur ne
#    peut pas payer, la carte est defaussee (`if_not_play_discard_it`, le
#    comportement standard d'une carte jouee « like in turn »).
#  ⚠ « ON THAT MINION » -> la carte se joue par son propre selecteur, puis
#    `AttachTo2(sbire)` la deplace sur le sbire si elle a atterri ailleurs
#    (modele yd012 Yaka Arrow). ⚠ Un verrou temporaire `CheckIfFaceCanAttachTo`
#    a ete essaye d'abord : le selecteur de `CanPlayThisUpgradeCard` ne le
#    consulte pas, la carte partait sur Rhino (cas du 07/09/2026).
#  ⚠ « After a minion ENTERS PLAY » : quel que soit le chemin (revelation,
#    boost, convocation par Bring the War). ⚠ Athena (ar012) refuse les TACTIC
#    : sur elle la recherche ne trouve rien d'eligible et la Reponse ne fait
#    rien, mais la limite par phase est consommee si elle a ete acceptee.
#  ⚠ « Limit once per PHASE » -> `LimitOncePerPhase()` ; temoin d'epuisement
#    exige.


def GetAbilities() -> Sequence['Ability']:

    def dieu_de_la_guerre(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        sbire = getattr(message, "trigger", None)
        if joueur is None or sbire is None or not Minion.IsType(sbire) or not sbire.card.IsOnField():
            return

        def attachable_au_sbire(face: 'CardFace') -> bool:
            return EstUneAmeliorationTactic(face) and PeutSAttacherA(effect, face, sbire)

        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            finder=CardFinder(card_type=Upgrade, trait=TRAIT_TACTIC, check_face_fn=attachable_au_sbire),
        )
        if face is None:
            return

        # « on THAT minion » : la carte est jouee normalement (cout paye, cible
        # choisie par le selecteur de l'amelioration), puis, si elle a atterri
        # ailleurs, `AttachTo2` la ramene sur le sbire — le chemin de `yd012`
        # Yaka Arrow, seule voie pour deplacer une amelioration en jeu.
        # ⚠ Une premiere version verrouillait la cible par une regle temporaire
        # `CheckIfFaceCanAttachTo` : le selecteur de `CanPlayThisUpgradeCard`
        # ne consulte pas ce message, Feint partait sur Rhino (cas du 07/09).
        Faces.AddToHand([face], joueur, effect)
        joueur.PlayCardsLikeInTurn([face], effect)
        if face.card.IsOnField() and Hote(face) is not sbire and sbire.card.IsOnField():
            face.AttachTo2(sbire, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            dieu_de_la_guerre,
        ).LimitOncePerPhase(),
    ]
