from . import *

# Trouble in Central Park — OBLIGATION. 2 icones de boost.
#   Uses (3 foe counters). Victory 0.
# Give to the Puddlegulp player.
# Forced Action: Seek a minion from the encounter deck and put it into play
#   engaged with you -> remove 1 foe counter from here. That enemy attacks
#   you. (Limit once per round.)
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « THROG », pas
# « ... NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc
# ICI et pas dans `throg_nemesis/`. Piege bt019 / nt012 / yd013 / dr010 /
# bk017 / tt020 / br012 — HUITIEME fois, et la quatrieme ou il est vu AVANT
# d'ecrire. Une obligation rangee dans le mauvais dossier n'est JAMAIS
# chargee, en silence : la carte entre en jeu et ne fait rien.
#
# ⚠ « Give to the PUDDLEGULP player » : c'est l'ALTER-EGO qui est nomme, pas
# le heros. `desc.GiveTo` vaut donc « Puddlegulp ». `Worlds.FindPlayerByName`
# passe par `player.IsName`, qui reconnait les deux faces — mais on ecrit ce
# qui est imprime.
#
# MOT-CLE : USES — fiche `docs/reference/mots-cles/uses.md`, creee pour cette
# carte. Base automatique : `desc.Uses = "3,foe"` pose les 3 pions a l'entree
# en jeu ET fait sortir la carte quand le dernier part
# (`has_uses.py:46`). AUCUN SCRIPT, et surtout PAS de
# `WhenTheLastCounterIsRemovedFromHere` qui defausserait une deuxieme fois.
# Le compteur `foe` a ete ajoute a l'enum `COUNTER` de `card_face.py` : sans
# lui, `IsCounter('foe')` refuse le nom et la carte tombe des la construction
# du deck (meme panne que 'style' pour kate_bishop).
#
# CARTES DE REFERENCE
#  - `61033a` Suggestion ([energy]) : LE jumeau structurel — une obligation a
#    `Uses`, dont la capacite est une `Forced Action` payee sur la carte
#    elle-meme. Montage :
#    `WhenInYourPlayTurn(AbilityType.ForcedAction, op).SetCostFunc(...)`.
#  - `br005` Star Jump : « Seek a minion from the encounter deck and put it
#    into play engaged with you » -> `Search.SearchForCard(...,
#    include_encounter_deck=True, card_type=Minion)` puis `PutIntoPlay` et
#    `EngagePlayer`. Le texte est identique au mot pres.
#  - `10015` Toe to Toe : « That enemy attacks you » ->
#    `target.DoAttackYou(joueur, effect)`.
#  - `ho009` : `CostFunc.Custom(None, fn)`, le cout arbitraire dont le `False`
#    bloque le paiement.
#
# TEXTE CONTRE CODE
#  ⚠ LA FLECHE EST APRES « put it into play engaged with you ». Convoquer le
#    sbire est donc le COUT, et retirer un pion la RECOMPENSE. L'inverse
#    (pion en cout, sbire en effet) donnerait le meme resultat presque
#    toujours, mais pas quand le deck de rencontre n'a plus de sbire : la
#    version imprimee ne retire alors AUCUN pion, et l'obligation reste. Le
#    cout est donc ecrit en cout.
#  « FORCED Action » -> la phase des joueurs ne peut pas se terminer tant
#    qu'elle est jouable. Avec la limite par round et l'absence de sbire dans
#    le deck de rencontre, elle cesse de l'etre.
#  « That ENEMY attacks you » -> « that », donc LE sbire qu'on vient de poser,
#    pas un ennemi au choix. Mot-piege `wd022`, verifie : on garde la
#    reference exacte, on ne re-cherche pas.
#  « (Limit once per ROUND.) » -> `.LimitOncePerRound()`, et le temoin
#    d'epuisement (etape 7 bis) mesure le nombre de pions restants au second
#    declenchement du meme round.
#  « Victory 0 » -> ⚠ ecart moteur connu, decrit dans `mots-cles/uses.md` :
#    `has_uses.py:54` teste `if self.victory:`, et `0` est faux, donc la carte
#    est DEFAUSSEE au lieu d'aller dans la pile de victoire. Sans consequence
#    tant qu'aucune carte ne compte la pile de victoire. Meme traitement que
#    `51031`, `53029` et `br012`.


def GetAbilities() -> Sequence['Ability']:

    def convoquer_un_sbire(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        """Le COUT : « Seek a minion from the encounter deck and put it into
        play engaged with you ». Rend False si le deck de rencontre n'a aucun
        sbire — la Forced Action n'est alors pas jouable, et aucun pion ne
        part."""
        Unused(cibles)
        joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return False
        sbire = Search.SearchForCard(
            effect, joueur,
            include_encounter_deck=True,
            card_type=Minion,
        )
        if sbire is None:
            return False
        sbire.PutIntoPlay(joueur, effect)
        sbire.CastTo(Minion).EngagePlayer(joueur, effect)
        # « THAT enemy » : on garde la reference exacte pour le corps, plutot
        # que de rechercher « un sbire engage » apres coup.
        setattr(effect, "_tg011_sbire_convoque", sbire)
        return True

    def des_ennuis_a_central_park(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)

        # « remove 1 foe counter from here. »
        Faces.RemoveCountersOn([this], 1, COMPTEUR_ENNEMI, effect)

        # « That enemy attacks you. »
        joueur = message.GetToPlayer()
        sbire = getattr(effect, "_tg011_sbire_convoque", None)
        if joueur is not None and sbire is not None and sbire.card.IsOnField():
            sbire.CastTo(Minion).DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.ForcedAction,
            des_ennuis_a_central_park,
        ).SetCostFunc(CostFunc.Custom(None, convoquer_un_sbire))
        .LimitOncePerRound(),
    ]
