from . import *

# Lightning Leap — EVENEMENT, cout 1, [energy]. SUPERPOWER. x2.
# Hero Interrupt: When you make a basic attack against a minion engaged with
#   a player, resolve that attack against the villain and each minion engaged
#   with that player instead, ignoring the guard keyword.
#
# CARTE DE REFERENCE
#  - `25013` * Thor: Odinson (pack valk) : « Interrupt: When Thor attacks a
#    minion engaged with a player, spend a [energy] resource -> resolve this
#    attack against each minion engaged with that player (in the order of your
#    choice) ». LE jumeau structurel, a deux mots pres. Le montage y est :
#    `WhenUnitWouldAttack(..., attack_targets=Minion)` et
#    `message.AddTarget(...)`. ⚠ Son `.SetTarget(fn, range="All")` n'est PAS
#    repris ici : voir le commentaire du corps.
#  - `10003` Hulk Smash / `06015` Mean Swing : l'evenement joue en
#    « Hero Interrupt » sur une attaque de BASE -> `.SetPlay()` et
#    `is_basic_attack=True`.
#
# TEXTE CONTRE CODE
#  ⚠ « INSTEAD » ne veut PAS dire que le sbire vise sort de l'attaque : il est
#    lui-meme « un sbire engage avec ce joueur », donc il fait partie de la
#    nouvelle liste. Le mot dit que l'attaque, au lieu de se resoudre contre
#    LUI SEUL, se resout contre l'ensemble. On AJOUTE donc les cibles
#    manquantes au lieu de remplacer la liste (`AddTarget`, pas
#    `ReplaceTarget`) — c'est aussi ce que fait `25013`.
#  ⚠ ET ON N'AJOUTE JAMAIS UNE CIBLE DEJA PRESENTE : la resolution compte les
#    doublons (`FacesHelper.ListToDict`, can_attack.py:179) et frapperait deux
#    fois le meme sbire. Le filtre est explicite dans le corps.
#  « against a minion engaged with A PLAYER » -> n'importe quel joueur, pas
#    seulement vous. En solo ca revient au meme ; a plusieurs, frapper le
#    sbire d'un voisin arrose le vilain ET tout ce qui est sur lui.
#  « the VILLAIN and each minion » -> le vilain est ajoute en plus. C'est ce
#    qui fait de cette carte a 1 ressource la plus grosse attaque du pack.
#  ⚠ « ignoring the GUARD keyword » -> fiche `mots-cles/guard.md`. AUCUN CODE
#    N'EST NECESSAIRE, et c'est verifie par un cas : le garde n'est lu QUE par
#    `Villain.CanBeAttackBy` (villain.py:72), c'est-a-dire a la SELECTION des
#    cibles. Une cible ajoutee apres coup par `AddTarget` ne repasse pas par
#    ce filtre (`ability.py:956` est le seul appelant). La clause est donc
#    satisfaite nativement, comme le « cannot be found » de `br012`.
#    ⚠ Ecart assume, note ici pour ne pas etre redecouvert : le message
#    `AfterIgnoreKeywordOnCard("Guard")` n'est pas emis, faute d'avoir eu a
#    ignorer quoi que ce soit. Une carte qui reagit a « after you ignore the
#    guard keyword » (`32034` Acute Control, Justice) ne se declencherait donc
#    pas sur ce montage.


def GetAbilities() -> Sequence['Ability']:

    def saut_de_foudre(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        # ⚠ LES CIBLES SONT CALCULEES ICI, PAS DANS UN `SetTarget`. Le montage
        # de `25013` (un selecteur qui lit `effect.GetBindMessage`) marche pour
        # une capacite d'ALLIE, dont l'effet est deja lie au message quand le
        # selecteur tourne. Pour un EVENEMENT joue en Interruption (`.SetPlay()`),
        # le selecteur est evalue AVANT la liaison : il rendait une liste vide,
        # l'abilite n'avait donc aucune cible legale et n'etait JAMAIS proposee.
        # Symptome : le vilain et le second sbire prenaient 0 degat, et la carte
        # restait en main sans un mot. Mesure du 05/09/2026.
        # Ici il n'y a de toute facon AUCUN choix a faire : le texte dit « each ».
        deja_vises = list(message.attacked_targets)
        ajouts: List['CardFace'] = []
        for cible in list(message.attacked_targets):
            if not Minion.IsType(cible) or not cible.engaged_player:
                continue
            for sbire in cible.engaged_player.GetEngagedMinions():
                if sbire not in deja_vises and sbire not in ajouts:
                    ajouts.append(sbire)
            for vilain in Worlds.GetVillains(effect):
                if vilain not in deja_vises and vilain not in ajouts:
                    ajouts.append(vilain)
        if ajouts:
            message.AddTarget(*ajouts)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            saut_de_foudre,
            attack_targets=Minion,
            is_basic_attack=True,
        ).SetPlay(),
    ]
