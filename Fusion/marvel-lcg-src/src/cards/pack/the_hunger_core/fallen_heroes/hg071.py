from . import *

# Zombie Quicksilver — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). AVENGER. SCH 1.
# ATK 2. PV 3. Guard.
# Guard.
# Super Speed. This minion activates twice. While the engaged player controls an ally, its attacks target
# one of those allies (that player's choice) instead of their identity.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, `desc.Guard` = "1". Aucun script requis.
# - « Super Speed » : ABSENT de `docs/reference/mots-cles/README.md` (grep exhaustif : aucune fiche
#   `super-speed.md`, aucune autre carte du moteur ne le reprend comme mot-cle officiel ou maison). A la
#   difference de « Charge » (hg068, ambiance pure sans regle propre), « Super Speed » est suivi IMMEDIATEMENT
#   de sa propre definition complete sur la carte (« This minion activates twice »), exactement comme les noms
#   d'ambiance deja arbitres 6 fois dans ce pack (« Shield », « Storm », « Web », « Absorption », « Ambush »,
#   « Hex », « Portal to Limbo », hg007-hg015) : le nom lui-meme n'ouvre aucune fiche, SEULE la phrase qui le
#   suit porte une regle a coder. Pas de "A CONFIRMER" ici : ce motif est deja tranche pour ce pack, pas
#   ambigu.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « This minion activates twice » (= 1 activation supplementaire, pas un doublement recursif) :
#   `AbilityFactory.AfterEnemyActivationEnd(NonKeyword, "This", op, conditions=[pas_deja_double])` +
#   `this.DoActivate(joueur, effect)`, modele EXACT `sk249` Cloning Program (« Each SKRULL minion activates 1
#   additional time... » -> meme fabrique, meme appel `Enemy.DoActivate`, meme garde anti-boucle par un
#   attribut dynamique pose sur la carte pendant l'activation de surcroit, sans quoi celle-ci se
#   rappellerait elle-meme sans fin). Difference avec `sk249` : aucune restriction « during step two » ni «
#   SKRULL » ici -- Zombie Quicksilver double TOUJOURS sa propre activation, quelle que soit l'etape, donc pas
#   de condition `en_etape_deux` equivalente, et le filtre `which_enemy` vaut directement "This" (pas un
#   `CardFinder` par trait).
# - « While the engaged player controls an ally, its attacks target one of those allies (that player's
#   choice) instead of their identity » : `AbilityFactory.WhenUnitWouldAttackUnit(ForcedInterrupt, "This",
#   Identity, op)` + `message.ChangeTarget(cible, effect)`, modele EXACT `41028` Psionic Illusion (Psylocke) :
#   meme message `Message.WhenUnitWouldAttackUnit`, meme methode `ChangeTarget(unit, by_effect)` (sender_damage
#   .py:409, « Change le qui-est-attaque de CETTE attaque precise, avant qu'elle ne se resolve ») pour
#   rediriger une attaque qui viserait l'identite vers un autre personnage choisi par un joueur. Difference :
#   `41028` fait choisir l'ATTAQUANT (Psylocke controlee par le heros) parmi SES propres allies (`Friend`) ;
#   ici c'est « that player's choice » = LE JOUEUR ATTAQUE (le proprietaire de l'identite visee) qui choisit
#   PARMI SES PROPRES allies -- `player.AskChooseFace(allies, effect)`, modele EXACT `45065` Infinite Hunter
#   (meme pack officiel, meme appel pour choisir une cible parmi les allies CONTROLES par le joueur concerne).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. » -> natif, rien a coder.
# « Super Speed. » -> ambiance, voir bloc ci-dessus, rien a coder en elle-meme.
# « This minion ACTIVATES TWICE » -> 1 activation imprimee + 1 activation de surcroit declenchee
#   `AfterEnemyActivationEnd` = DEUX au total ; la garde `activation_super_speed` empeche l'activation de
#   surcroit elle-meme de se redoubler (elle enverrait sinon un second `AfterEnemyActivationEnd`).
# « its attacks target one of those allies ... INSTEAD OF their identity » -> le filtre `who_be_attacked=
#   Identity` de la fabrique garantit que la redirection ne se declenche QUE si l'attaque visait l'identite ;
#   si Zombie Quicksilver attaque deja un allie (par un autre effet du scenario, ex. Guard d'un autre sbire
#   engage), rien ne se passe ici -- deja la bonne cible, aucune redirection necessaire.
# « WHILE the engaged player controls an ally » -> condition lue EN DIRECT au moment de CHAQUE tentative
#   d'attaque (`joueur.GetControlAllies()`, liste vide -> aucune redirection, l'attaque frappe l'identite
#   normalement) ; pas une condition figee a l'entree en jeu du sbire.
# « target ONE of those allies (THAT PLAYER'S choice) » -> `player.AskChooseFace(allies, effect)` sur
#   `joueur = message.target.GetControlByPlayer()`, c-a-d le proprietaire de L'IDENTITE VISEE par CETTE
#   attaque (donc le "engaged player", puisqu'un sbire n'attaque que le joueur avec lequel il est engage) --
#   jamais un joueur fixe ni le controleur de Zombie Quicksilver (qui n'appartient a aucun joueur, c'est un
#   Minion de rencontre).
# « its attacks » (PLURIEL, generique) -> aucune restriction a l'attaque BASIQUE ni a une attaque issue d'un
#   boost : la redirection s'applique a TOUTE attaque de Zombie Quicksilver visant une identite, y compris les
#   DEUX activations issues de « Super Speed » (chacune declenche son propre `WhenUnitWouldAttackUnit`,
#   independamment de l'ability ci-dessus qui gere seulement le NOMBRE d'activations).
#
# A CONFIRMER : aucune autre carte du depot ne combine « activates twice » (nombre fixe, pas « an additional
# time » conditionne a une etape/un trait) ET une redirection de cible choisie par le joueur ATTAQUE (pas
# l'attaquant) -- lecture retenue, au mot pres du texte imprime : les deux clauses sont independantes (le
# nombre d'activations ne change rien a QUI est vise par chacune, la redirection de cible ne change rien au
# NOMBRE d'activations), donc codees comme deux abilities distinctes sans interaction explicite entre elles.
# Aucune autre lecture plausible identifiee.
#
# Bloc nombres texte <-> code : "twice" -> UNE SEULE activation de surcroit ajoutee (1 imprimee + 1 ajoutee =
# 2, jamais une boucle `while`) ; "one of those allies" -> `AskChooseFace` avec une plage (1, 1) interne
# (jamais plusieurs cibles choisies a la fois). Aucune autre valeur numerique imprimee sur cette carte en
# dehors de `desc` (SCH 1 / ATK 2 / PV 3 / Guard 1, deja conformes a `cards_custom.json`).


def GetAbilities() -> Sequence['Ability']:

    def pas_deja_double(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        Unused(effect)
        sbire = message.trigger
        return sbire.IsInPlay() and not getattr(sbire, "activation_super_speed", False)

    def super_speed(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        sbire = message.trigger.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        sbire.activation_super_speed = True
        try:
            sbire.DoActivate(joueur, effect)
        finally:
            sbire.activation_super_speed = False

    def rediriger_sur_allie(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        joueur = message.target.GetControlByPlayer()
        if joueur is None:
            return

        allies = joueur.GetControlAllies()
        if not allies:
            return

        cible = joueur.AskChooseFace(allies, effect)
        if cible is not None:
            message.ChangeTarget(cible, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.NonKeyword,
            "This",
            super_speed,
            conditions=[pas_deja_double],
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "This",
            Identity,
            rediriger_sur_allie,
        ),
    ]
