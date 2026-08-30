from . import *

# Star Lightning — TRAHISON nemesis, custom « jakxin »
# `Boost 2`, trait SUPERPOWER. Deux exemplaires physiques : ma020 et ma021,
# meme texte, meme code.
#
# When Revealed: Catalina Chavez attacks you. If this attack deals damage,
#   stun your identity. If no attack is made this way, this card gains surge.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE — `pt021` Bulldozing Charge (pack patriot)
#
# Meme structure imprimee (« <sbire nemesis> attacks you. If no attack was
# made this way, ... »), meme brique de moteur :
#   1. `Worlds.FindCardOnField(effect, name=..., card_type=Enemy)` ;
#   2. si trouve -> `enemy.DoAttackYou(player, effect, ...)` ;
#   3. sinon -> le repli directement.
# Originaux officiels : `02040` Tail Sweep et `22031` Old Rivals.
#
# Le repli part donc dans DEUX cas : Catalina n'est pas en jeu, ou elle est
# en jeu mais l'attaque n'a pas eu lieu (joueur en identite civile, attaque
# annulee, sbire etourdi...).
#
# ---------------------------------------------------------------------------
# TROIS CLAUSES, TROIS CROCHETS DIFFERENTS
#
# « ATTACKS **YOU** » -> `message.GetToPlayer()`, le joueur a qui la carte
#   est distribuee.
# « If this attack DEALS DAMAGE, stun your identity » ->
#   `if_this_attack_deals_damage=` (enemy.py:80), le crochet dedie du moteur.
#   ⚠ Mot-piege `defeated` vs `damaged` : c'est bien « inflige des degats »,
#   pas « vainc ». Et ce n'est PAS « if this attack is undefended » : une
#   attaque bloquee qui passe quand meme 1 degat etourdit.
#   « your IDENTITY », pas « your hero » : `player.GetIdentity()`.
# « If NO ATTACK IS MADE this way, this card gains SURGE » ->
#   `if_no_attack_was_made=` puis `ThisCardGainSurge(effect)`
#   (cards/pack/__init__.py:100). SURGE CONDITIONNEL : le mot-cle n'est PAS
#   dans `desc`, il est gagne a la volee. Idiome de `il021`, `il022`, `22031`
#   et `pt017`. Fiche : docs/reference/mots-cles/surge.md.
#
# ⚠ LES DEUX CLAUSES S'EXCLUENT : soit l'attaque a lieu (et alors seule la
# clause « deals damage » peut partir), soit elle n'a pas lieu (et alors
# seule la clause « no attack » part). Aucun cas ne declenche les deux.
#
# ---------------------------------------------------------------------------
# LIMITE DU HARNAIS, DECLAREE
#
# La bascule du surge n'est pas observable de facon deterministe :
# `ThisCardGainSurge` n'est lisible ni dans `etat_attendu`, ni via un
# compteur, et la carte rencontre supplementaire qu'il distribue depend du
# deck. Meme limite que `pt017`, ecrite noir sur blanc dans
# docs/ms_america_cartes.md. Ce qui EST prouve par les cas : l'attaque a lieu
# et l'identite est Sonnee.


def GetAbilities() -> Sequence['Ability']:

    def star_lightning(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        def sonner(degats: int):
            Unused(degats)
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.GiveStatus([identite], "Stunned", effect)

        def deferlement():
            ThisCardGainSurge(effect, message)

        catalina = Worlds.FindCardOnField(effect, name=NOM_CATALINA,
                                          card_type=Enemy)
        if catalina:
            catalina.DoAttackYou(
                joueur,
                effect,
                if_this_attack_deals_damage=sonner,
                if_no_attack_was_made=deferlement,
            )
        else:
            deferlement()

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            star_lightning,
        ),
    ]
