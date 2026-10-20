# Backlog 8 (connexion et inscription) : points restés ouverts (20/10/2026)

La fiche du 09/10 tranche la mise en page, le bandeau mobile, les deux corrections de texte et le pied de page.
Elle ne tranche pas les points ci-dessous : rien n'a été codé pour eux.

## 1. Palette : rouge actuel du site, ou bleu Épuré ?

La fiche dit « respecter le mode sobre » ; la mémoire du projet dit que l'Épuré est devenu la base visuelle (fond #111318, accent bleu #3f86e0,
titres en Bangers). Le site n'a pas de mode Épuré (seul `SOBRE_SITE` existe) et ses pages gardent le rouge Marvel.
Fait : la page n'utilise que des variables CSS, donc le mode sobre la ternit comme les autres pages du site.
- Option A (recommandée) : laisser le rouge et le fond du site pour l'instant. Connexion, accueil du site et admin restent cohérents entre eux.
- Option B : passer ces pages seules en Épuré (fond #111318, bouton bleu, titres en Bangers). Écran : plus proche de l'accueil du jeu, mais
  la page de connexion ne ressemble plus au reste du site (accueil, admin, signalements) tant qu'ils ne suivent pas.
- Option C : Épuré sur tout le site, chantier à part.

## 2. Sélecteur FR / EN

Le nouvel en-tête fin l'accueille à droite, pour que la page soit montrable en anglais (avant : aucune bascule sur ces pages).
Sur mobile, l'en-tête disparaît au profit du bandeau : pas de bascule de langue (comme avant). 
- Option A (recommandée) : laisser ainsi (la langue vient du cookie, puis du navigateur).
- Option B : ajouter la bascule dans le bandeau mobile, à droite du titre (un bouton de plus dans un bandeau de 56 px).

## 3. Illustration de la scène

La scène montre la mascotte du moment (`/narwhal.png`, change toutes les trois heures) et le titre de la page.
La fiche dit « illustration » sans préciser laquelle.
- Option A (recommandée) : la mascotte du moment.
- Option B : une illustration fixe de héros ou de vilain, comme l'assistant (choix et droits d'image à trancher).

## 4. Accents ailleurs sur le site

Remis : connexion, inscription, réinitialisation, erreurs de ces formulaires. Restent sans accent (hors périmètre de la fiche) :
écran de reprise, signalements, écran d'attente, page d'arrêt, bouton d'installation (clés de `langue.py`, tous les « Reponse », « Recu », « Reessayer », etc.).
Question : étendre aux autres pages (même opération, clés et tests à renommer) ?
