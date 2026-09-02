from . import *

# You Are My God — COMPLOT ANNEXE. Seuil 2 (FIXE, aucune icone joueur), icone
# de CRISE, 2 icones de boost.
#
# Hinder 1[per_hero].
# Forced Response: After Gorr the God Butcher attacks, he attacks again. Deal
#   him no boost cards for this attack. (Limit once per player per phase.)
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Hinder` (mots-cles/hinder.md) : BASE AUTOMATIQUE, `desc.Hinder = "1*"`.
#   Le moteur pose la menace sur CETTE carte a son entree en jeu. Aucun script.
# - `Crisis` (mots-cles/crisis.md) : base automatique elle aussi.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After X attacks, he attacks again » : `AfterUnitAttackEnd` puis
#   `DoAttackYou`, la forme de 07020 (Ball and Chain) pour le declencheur.
#   ⚠ Le « no boost cards » est le parametre `do_not_give_boost=True` de
#   `DoActivate` (enemy.py:203) : `DoAttackYou` (enemy.py:98) ne l'accepte
#   PAS. On passe donc par `DoActivate`, qui choisit lui-meme attaque ou
#   manigance selon la forme du joueur vise — ici toujours l'attaque, puisque
#   la carte ne se declenche qu'apres une attaque.
# - « Limit once per player per phase » : ⚠ NI `LimitOncePerPhase` (globale :
#   wd056b documente la panne, elle interdit l'effet a tous les autres joueurs
#   des qu'un seul l'a declenche), NI `LimitOncePerPhasePerPlayer`, qui
#   `assert isinstance(message, TriggerNonePlayerMessage)`
#   (condition/once_per.py:30) — or `AfterUnitAttackEnd` n'en est pas un, et
#   l'assertion, avalee par `effect_checker.py`, rendait la carte INERTE en
#   silence. Constate par le cas gb020 le 02/09/2026.
#   La condition est donc ecrite a la main sur le meme registre du moteur
#   (`world.stat.IsOncePerPhasePerPlayer`), avec le joueur pris sur le message
#   d'attaque (`GetAgainstPlayer`) au lieu de `GetToPlayer`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After Gorr the God Butcher ATTACKS » -> apres son attaque, y compris une
#   attaque declenchee par une autre carte, pas seulement l'activation de la
#   phase du vilain.
# « HE ATTACKS AGAIN » -> une seconde attaque contre le MEME joueur que la
#   premiere (le texte ne change pas de cible).
# « Deal him NO BOOST CARDS for this attack » -> la seconde attaque seulement.
# « (Limit ONCE PER PLAYER PER PHASE) » -> un joueur ne peut subir la seconde
#   attaque qu'une fois par phase ; a plusieurs, chacun a la sienne.
# ⚠ Sans cette limite, une attaque en declencherait une autre indefiniment.


def GetAbilities() -> Sequence['Ability']:

    def une_fois_par_joueur_par_phase(effect: 'Effect',
                                      message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = message.GetAgainstPlayer()
        if not isinstance(joueur, Player):
            return False
        return effect.world.stat.IsOncePerPhasePerPlayer(effect.ability, joueur)

    def il_frappe_encore(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this
        Unused(this)

        vilain = TrouverGorr(effect)
        joueur = message.GetAgainstPlayer()
        if vilain and isinstance(joueur, Player):
            vilain.DoActivate(joueur, effect, do_not_give_boost=True)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name=NOM_GORR),
            il_frappe_encore,
            conditions=[une_fois_par_joueur_par_phase],
        ),
    ]
