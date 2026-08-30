from . import *

# The Real Question — MANIGANCE ANNEXE nemesis (carte paysage), custom
# « CptScorp ». 3 icones de bonus, `StartingThreat "2*"` = 2 PAR JOUEUR.
# When Revealed: Discard cards from the top of the encounter deck until an
#   attachment is discarded. Reveal that attachment.
# While this scheme is in play, attachments gain Permanent.
#
# `StartingThreat "2*"` : l'etoile est le symbole « par joueur », lue
# nativement par le moteur (`Scheme2.RegisterAttribute("StartingThreat")` +
# `Worlds.ConvertPerPlayerIconToInt`). Modele `01108` Crowd Control, meme
# `"2*"`. Rien a coder.
#
# ---------------------------------------------------------------------------
# BLOC 1, le When Revealed -> modele EXACT : `40093` The Senator's Support et
# `wd104` "Legitimate Business", qui impriment la MEME phrase (« discards cards
# from the top of the encounter deck until an attachment is discarded and
# reveals that card ») et emploient toutes deux
# `Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)` puis
# `face.Reveal(player, effect)`. `24030` Ruination donne la meme forme sur un
# When Revealed.
#
# ⚠ ET SI LE DECK DE RENCONTRE NE CONTIENT AUCUN ATTACHEMENT ? Le set nemesis
# de Speed n'en compte que DEUX (sd020, sd021) ; une fois posees, il peut n'en
# rester aucune. Le moteur ne boucle PAS : `Deck.DiscardUntil` (deck.py:470)
# parcourt un INSTANTANE du deck (`self.Get()[::-1]`), donc au plus une passe,
# et rend `(None, ...)` si le deck se vide. La carte defausse alors tout ce qui
# reste et ne revele rien — exactement le comportement des deux cartes
# officielles ci-dessus. Aucune garde supplementaire n'est necessaire, et en
# ajouter une divergerait du moteur.
#
# ---------------------------------------------------------------------------
# BLOC 2, « attachments gain Permanent » ->
# `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Attachment, permanent=1)`
# (factory/environment.py:66, parametre `permanent` ligne 106). C'est la
# fabrique « tant que CETTE carte est en jeu, telles cartes gagnent tel
# mot-cle » : elle s'eteint d'elle-meme quand la manigance quitte le jeu.
# Modele de forme : `15024` The Next Evolution (meme genre de manigance annexe
# nemesis dont le texte modifie globalement les cartes rencontre) et `ss018`
# Assassins Guild chez le meme auteur.
#
# La fiche `docs/reference/mots-cles/permanent.md` est formelle : le mot-cle
# lui-meme est gere nativement (`HasPermanent.OnWhenCardLeavePlay`), on ne code
# JAMAIS le blocage de sortie de jeu dans un script. Ici on ne fait que
# DONNER le mot-cle, ce qui est bien une capacite imprimee.
#
# ⚠ COLLISION AVEC sd020 Inspirational Art, tranchee dans sd020.py : tant que
# The Real Question est en jeu, la « Hero Action: Spend [energy][physical]
# resources -> discard this card » d'Inspirational Art devient INDISPONIBLE
# (condition sur la capacite) plutot que d'echouer. C'est l'intention de
# l'auteur : battre la manigance d'abord.


def GetAbilities() -> Sequence['Ability']:

    def the_real_question(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        player = message.GetToPlayer()

        face = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=Attachment,
        )
        if face:
            face.Reveal(player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            the_real_question,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Attachment),
            permanent=1,
        ),
    ]
