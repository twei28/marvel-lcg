from . import *

# Necrotic Repulsors — ATTACHMENT (deck signature de Zombie Iron Man, carte 1/5). Traits TECH, UPGRADE.
# Attach to Zombie Iron Man.
# His attacks gain Piercing.
# Hero Action: Spend 2 resources → discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[piercing]] (mots-cles/piercing.md) : propriete booleenne de l'attaque, accordee ici de facon
#   PERMANENTE (tant que la carte est en jeu), pas sur une seule attaque declenchee par un cout. Fiche lue :
#   deux chemins possibles (statique `piercing=True` d'une fabrique d'attaque, ou dynamique
#   `message.GainPiercing(effect)`) — le chemin retenu ici est le 3e, deja utilise par des cartes OFFICIELLES
#   pour « <Nom>'s attacks gain/have piercing » attribue depuis une carte TIERCE (pas « This » qui attaque) :
#   `AbilityFactory.UnitAttackGainKeyword(cible, piercing=True)` (do_attack.py:828), qui pose une Ability
#   `NonKeyword` ecoutant `Message.CheckIfAttackMessageHasKeyword` et appelle `message.GainPiercing(effect)`
#   des que l'attaquant correspond a la cible — exactement la fiche piercing.md, juste sans action intermede.
# - « Hero Action » n'est PAS une fiche mots-cles dediee (absente du README, c'est un sous-type d'Ability de
#   base — cf. PROCESSUS-CARTE.md etape 5, ligne « Hero Response/Hero Action : sous-type dedie, pas le type
#   nu »). Rien a ouvrir, mais bien choisir `AbilityType.HeroAction` et pas `AbilityType.Action`.
# - « Spend 2 resources » (sans qualificatif « of any type »/« of the same type » imprime dans
#   `cards_custom.json`) : PAS un mot-cle, mais une convention de cout a confirmer — voir A CONFIRMER plus
#   bas.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to Zombie Iron Man » : AUCUN code necessaire. Cette carte n'est jamais jouee depuis une main ni
#   mise en jeu seule (pas de `Message.AfterCardPutIntoPlay` a son sujet) : elle est piochee et attachee
#   DIRECTEMENT par `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (appelee par `hg008` Zombie Iron
#   Man a son entree en jeu, et plus tard par `hg023` Hunger Protocol), qui appelle
#   `trouvee.CastTo(Attachment).AttachTo2(metazombie, effect)` -- `metazombie` est TOUJOURS Zombie Iron Man
#   pour ce deck signature (`DECKS_SIGNATURE["Zombie Iron Man"]` ne contient que hg019-hg023, commun.py).
#   Meme lecture que le commentaire de `hg008` sur `hg019-hg022` : « le code ne filtre pas la source, comme le
#   texte imprime ne le fait pas non plus » -- pas d'`AbilityFactory.AttachToFaceWhenPutIntoPlay` ici, elle
#   n'ecouterait jamais rien (cette carte ne passe jamais par `PutIntoPlay`), contrairement a `01100`
#   Enhanced Ivory Horn (Rhino) ou l'attachement EST jouee/mise en jeu par un joueur.
# - « His attacks gain Piercing » : `sk077`/`sk078`/`sk076` * Empress R'Klll (« Empress R'Klll's attacks gain
#   piercing ») : `AbilityFactory.UnitAttackGainKeyword("This", piercing=True)` -- mais la-bas l'Ability vit
#   SUR le personnage qui attaque ("This" = lui-meme). Ici l'Ability vit sur l'ATTACHEMENT, pas sur Zombie
#   Iron Man : modele exact `27078` "Now We're Angry!" (pack `sm/venom`), attachement de Venom qui pose
#   `AbilityFactory.UnitAttackGainKeyword(CardFinder(name="Venom"), overkill=True)` -- la cible est nommee,
#   pas "This". Meme substitution ici : `CardFinder(name="Zombie Iron Man")`.
# - « Hero Action: Spend 2 resources → discard this card » : `01100` Enhanced Ivory Horn (pack `core/rhino`) :
#   `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("RRR"))` -- MEME fabrique,
#   cout COLORE. Ici le texte ne porte aucune icone de ressource (juste « 2 resources »), modele du cote
#   « cout generique, n'importe quel type » : `sq017` Revealed Identity (pack `spider_punisher_nemesis`, meme
#   texte officiel « Spend 2 resources of any type → discard this card ») pose `.SetCost(Cost("2"))` -- le
#   litteral numerique NU ("2", pas "RR"/"BB"/...) est precisement le cout « N ressources de N'IMPORTE QUEL
#   TYPE », au contraire d'un cout colore qui fixe le type. Combine aux deux : `PlayerActionToDiscardThis(
#   AbilityType.HeroAction).SetCost(Cost("2"))`. Vu aussi `ze015` Shroud of the Nightmother (meme texte, cout
#   via `SetCostFunc(CostFunc.Spend(...))`) : chemin alternatif qui ne sert qu'a relire le MONTANT depense
#   apres coup (`self.return_res`, utile pour un effet du type « spend X, deal X damage ») -- inutile ici,
#   rien dans le texte ne redemande le montant, donc `.SetCost()` simple (comme `sq017` et `01100`) est le
#   choix le plus proche de la carte imprimee.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Iron Man » -> aucun module (voir CARTES DE REFERENCE : attache geree par
#   `commun.DefausserJusquaUneAmeliorationDuDeckSignature`, deja en jeu depuis `hg008`).
# « HIS attacks gain Piercing » -> `AbilityFactory.UnitAttackGainKeyword(CardFinder(name="Zombie Iron Man"),
#   piercing=True)`. « His » = Zombie Iron Man (l'antecedent de la phrase precedente, « Attach to Zombie Iron
#   Man »), jamais un autre Metazombie : `CardFinder(name=...)` filtre par NOM exact, donc aucune attaque d'un
#   AUTRE Metazombie (meme Zombie Captain America portant une amelioration similaire) n'est touchee.
# « attacks GAIN Piercing » -> toutes ses attaques, pas seulement les attaques de base : `is_basic_attack`
#   laisse a `None` (defaut de la fabrique) = aucun filtre, comme `27078` qui ne restreint pas non plus
#   « Now We're Angry! » aux attaques de base de Venom.
# « HERO Action » -> `AbilityType.HeroAction`, pas `AbilityType.Action` (sous-type distinct, PROCESSUS-CARTE
#   etape 5).
# « Spend 2 resources » -> `.SetCost(Cost("2"))` (2 ressources, n'importe quel type, modele `sq017`/`ze015`).
# « → discard this card » -> `AbilityFactory.PlayerActionToDiscardThis`, qui defausse `effect.this` (la carte
#   elle-meme, PAS Zombie Iron Man) ; aucune action complementaire au-dela de la defausse (contrairement a
#   `hk063` Shroud of the Nightmother qui ajoute un jeton apres la defausse -- rien de tel imprime ici).
#
# A CONFIRMER : le texte source (`data/cards_custom.json`, hg019) dit juste « Spend 2 resources », sans
# qualificatif. TOUTES les cartes OFFICIELLES grep-ees avec un cout non colore portent explicitement « of any
# type » ou « of the same type » (jamais nu) -- la version TTS/livret fan-made a visiblement elide ce
# qualificatif a la retranscription. Lecture retenue : « of any type » (lecture la plus simple, et celle des
# cartes-soeurs du MEME deck signature, hg018/hg020/hg021 qui portent le meme patron « Spend N resources ->
# discard this card » sans icone colore non plus -- a verifier ensemble si une de ces cartes venait a
# contredire cette lecture). Aucune regle ne depend du choix inverse (« same type » interdirait de payer avec
# [physical]+[mental] ; rien dans le scenario ne force un joueur a n'avoir qu'un type de ressource) : ne
# bloque pas le script, mais a confirmer avec l'auteur/le reste du deck avant de livrer hg020-hg023 si l'un
# d'eux porte un cout colore qui trancherait la question a rebours.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Zombie Iron Man"),
            piercing=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2")),
    ]
