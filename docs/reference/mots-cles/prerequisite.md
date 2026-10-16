# Prerequisite (<trait>)

**Texte imprimé / définition** : « Prerequisite ([[MARTIAL ARTIST]]). » Imprimé sans texte de rappel. Une seule
carte officielle du dépôt le porte : `61029` * Defend Our City (manigance annexe joueur, « Prerequisite
([[Defender]]) »), dont le script ne code RIEN pour ce mot-clé. Aspect TMNT : `ua019` Flow of Battle
(Aggression).

**Lecture non tranchée** : question posée à l'utilisateur (`.planning/tmnt/aspects-aggression-questions.md`,
Q-UA1). Lecture codée en attendant (recommandée) : la carte ne peut être JOUÉE que si votre identité a le
trait indiqué (même effet que « Play only if your identity has the X trait », `SetPlay(only_if_your_identity_
has_trait=...)` pour un événement, condition de `CanPlayThisUpgradeCard` pour une amélioration). Autre lecture
possible : contrainte de CONSTRUCTION de deck seulement (le deck-builder ne l'exprime pas).

**Mécanisme moteur** : aucun mot-clé moteur ; condition `IdentiteATrait(effect, trait)` dans le script de la
carte.

**Carte exemple** : `ua019` Flow of Battle.

**Pièges connus** : forme alter-ego : le trait se lit sur l'identité courante (un trait d'héros absent de
l'alter-ego bloque le jeu en alter-ego, comme « Play only if your identity has... »).

**Variantes maison** : aucune.
