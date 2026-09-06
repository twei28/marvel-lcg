from . import *

# Hot Pursuit — EVENEMENT, cout 0, [energy]. AERIAL. FIRE. SUPERPOWER. x4.
# Hero Response: After you attach a copy of Burning to an enemy, ready Sunfire.
#
# QUATRE EXEMPLAIRES, le plus gros tirage du pack : c'est le moteur d'action
# de Sunfire. Chaque brulure posee peut le redresser, et il en pose une a
# CHAQUE attaque et a CHAQUE defense de base (`sf001a`).
#
# CARTES DE REFERENCE
#  - `AbilityFactory.AfterCardAttachTo` (card_move.py:141) : la seule fenetre
#    du moteur pour « after you ATTACH X to Y ». C'est `AttachTo2` qui l'emet,
#    d'ou l'obligation de passer par `AttacherUneBrulure` partout dans le pack.
#  - `10003` Hulk Smash : l'evenement joue en reaction -> `.SetPlay()`.
#
# TEXTE CONTRE CODE
#  ⚠ « After YOU attach » -> une brulure posee par une carte de RENCONTRE ne
#    declencherait pas. En pratique aucune carte du jeu ne pose de Burning
#    hors de ce pack, mais on ecrit la condition plutot que de s'en remettre a
#    cette absence.
#  ⚠ « a copy of BURNING » -> le nom, et il n'a AUCUN homonyme au depot
#    (verifie sur les 5933 cartes). Le filtre par nom est donc licite ici,
#    contrairement a « Sunfire ».
#  ⚠ « to AN ENEMY » -> `AttacherUneBrulure` refuse deja tout le reste, mais
#    la condition est ecrite ici aussi : deux gardes valent mieux qu'une quand
#    l'une des deux est dans un helper partage.
#  « ready SUNFIRE » -> la face HEROS, par le TYPE et jamais par le nom.
#    « Hero Response » confirme d'ailleurs qu'on est en forme heros.


def GetAbilities() -> Sequence['Ability']:

    def cest_bien_une_brulure(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> bool:
        Unused(effect)
        carte = message.trigger
        hote = getattr(message, "to_face", None) or Hote(carte)
        return (carte is not None and carte.IsName(NOM_BRULURE)
                and hote is not None and Enemy.IsType(hote))

    def poursuite_ardente(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        heros = HerosDuJoueur(effect)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.AfterCardAttachTo(
            AbilityType.HeroResponse,
            None,
            None,
            poursuite_ardente,
            conditions=[cest_bien_une_brulure],
        ).SetPlay(),
    ]
