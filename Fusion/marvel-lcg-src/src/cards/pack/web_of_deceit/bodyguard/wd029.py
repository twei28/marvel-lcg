from . import *

# Multiverse Recruit

def GetAbilities() -> Sequence['Ability']:

    def recrue(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        # ECART ASSUME, ecrit plutot que silencieux.
        #
        # Texte : « Search your COLLECTION for a nemesis minion and put it into
        # play engaged with you with Multiverse Recruit attached. »
        #
        # « Votre collection » est ce qui est hors de la partie : le moteur ne
        # sait ouvrir que ce qui est DANS la partie (deck, defausse, cartes
        # mises de cote). On prend donc le sbire de nemesis mis de cote par le
        # joueur, qui est la seule nemesis que la partie connaisse. A defaut,
        # la carte ne fait rien de plus.
        joueur = message.GetToPlayer()
        sbire = Search.SearchForCard(
            effect,
            joueur,
            include_set_aside=True,
            card_type=Minion,
        )
        if sbire:
            sbire.PutIntoPlay(joueur, effect)
            this.AttachTo2(sbire, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            recrue
        ),
        # « Attached minion ignores the unique rule and gains Victory 0. »
        #
        # La regle d'unicite est levee sur le SBIRE porteur, pas sur
        # l'attachement : `UniqueRuleNotApplyTo` ne sait viser que « This » ou
        # un nom, d'ou l'abilite ecrite a la main sur le meme message.
        #
        # ECART ASSUME : « gains Victory 0 » n'est pas rendu. Victory est un
        # attribut de carte que le moteur lit dans les donnees, pas un mot-cle
        # qui se donne en jeu : `GainVictory` existe, mais en commentaire
        # (has_victory.py:45).
        #
        # ⚠ CORRECTION DU 01/09/2026 — la portee de cet ecart etait SOUS-ESTIMEE
        # ici. Il etait ecrit que « le sbire ne rapportera rien a l'affichage
        # des points de victoire », ce qui laisse croire a une perte de points.
        # Ce n'est pas la question : `victory` est un BOOLEEN,
        # `printed_victory != None` (has_victory.py:51). Victory 0 vaut bien
        # zero point, mais il ENVOIE LA CARTE a l'affichage des victoires, donc
        # HORS DE LA PARTIE. Sans lui, le sbire de nemesis recrute retourne a la
        # defausse et peut donc revenir. C'est un ecart de REGLE, pas de score.
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfFaceApplyUniqueRule,
            [lambda effect, message:
                message.which_face == effect.this.CastTo(Attachment).GetBindFace()],
            lambda effect, message: message.IgnoreUniqueRule(effect),
            is_local=True,
        ),
    ]
