from . import *

# Atomic Fire — EVENEMENT, cout 3, [energy]. FIRE. SUPERPOWER. x2.
# Hero Action: Choose a player and attach a set-aside copy of Burning to the
#   villain and each minion engaged with that player. Deal 3 damage to each
#   enemy with a copy of Burning attached.
#
# LA CARTE LA PLUS CHERE DU PACK, ET SA RECOMPENSE : elle pose des brulures
# EN NOMBRE, puis frappe TOUS les ennemis qui en portent — y compris ceux
# allumes plus tot par le heros ou par les autres cartes.
#
# CARTES DE REFERENCE
#  - `tg003` Great Courage : « choose a player » puis un effet sur chaque
#    sbire engage avec CE joueur.
#  - `sf001a` : le meme geste, un ennemi a la fois.
#
# TEXTE CONTRE CODE
#  ⚠ « the villain AND EACH MINION engaged with that player » -> le VILAIN
#    (une seule fois, il n'est engage avec personne) PLUS les sbires du joueur
#    choisi. Un sbire engage avec un AUTRE joueur ne recoit rien.
#  ⚠ « Deal 3 damage to EACH ENEMY WITH A COPY OF BURNING ATTACHED » -> la
#    seconde phrase ne se limite PAS au joueur choisi : elle balaie TOUT le
#    terrain. C'est la difference entre les deux moities, et c'est imprime.
#  ⚠ ORDRE IMPRIME : on attache D'ABORD, on frappe ENSUITE. Les ennemis qu'on
#    vient d'allumer prennent donc les 3 degats eux aussi.
#  ⚠ Une brulure posee ici declenche `sf004` Hot Pursuit, qui redresse le
#    heros : c'est voulu, et c'est pourquoi tout le pack passe par
#    `AttacherUneBrulure`.
#  « a SET-ASIDE copy » -> quand la reserve est vide, on n'attache plus rien,
#    et la seconde phrase frappe quand meme ce qui brule deja.


def GetAbilities() -> Sequence['Ability']:

    def feu_atomique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur_qui_joue = JoueurDeCetteCarte(effect)

        # « CHOOSE A PLAYER » : ⚠ `SetTarget("Players")` rend la FACE
        # D'IDENTITE du joueur choisi, PAS un objet `Player`. Passer cette face
        # a `Player.IsType` leve « AttributeError: 'Hero' object has no
        # attribute 'IsPlayer' » (player.py:303) — AVALEE par le moteur, donc
        # une carte simplement INERTE : 0 degat, aucune brulure, et le journal
        # ne dit rien d'autre qu'un traceback. Trouve par le cas le 06/09/2026.
        for cible in list(effect.targets or []):
            recup = getattr(cible, "GetControlByPlayer", None)
            choisi = recup() if recup is not None else None
            if choisi is None or not Player.IsType(choisi):
                continue
            for vilain in Worlds.GetAllVillains(effect):
                AttacherUneBrulure(effect, vilain, joueur_qui_joue)
            for sbire in choisi.GetEngagedMinions():
                AttacherUneBrulure(effect, sbire, joueur_qui_joue)

        # « Deal 3 damage to EACH ENEMY WITH A COPY OF BURNING ATTACHED »
        # ⚠ tout le terrain, pas seulement le joueur choisi.
        en_feu = EnnemisEnFeu(effect)
        if en_feu:
            this.DealDamage(en_feu, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            feu_atomique,
        ).SetPlay().SetLabel()
        .SetTarget("Players"),
    ]
