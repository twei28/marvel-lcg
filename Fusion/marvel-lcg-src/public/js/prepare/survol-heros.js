// survol-heros.js - l'INTENTION du survol, dans l'écran « Choisis ton héros » (scène à gauche, roster à droite).
//
// La scène montre le héros survolé, avec son bouton « Voir ses cartes » et sa biographie. Mais ce bouton est dans la SCÈNE, pas sur la
// tuile : pour l'atteindre il faut quitter la tuile. Or la scène était redessinée à chaque `mouseleave` (retour au héros du siège, ou au
// vide) et à chaque tuile croisée en chemin : le bouton disparaissait ou changeait de héros avant que la souris n'y arrive. Signalé sur
// le Discord le 26/10/2026 (« dès que je bouge la souris ça change le héros »).
//
// Règle : on RETIENT le dernier héros regardé.
//  - le premier survol s'affiche tout de suite ;
//  - une tuile croisée sans s'y arrêter (moins de `delaiIntention`) ne change rien ;
//  - quitter la tuile ne ramène la scène au héros du siège qu'après `delaiRetour`, et seulement si la souris n'est pas allée dans la scène ;
//  - dans la scène, le héros regardé reste jusqu'à ce qu'on en sorte (puis `delaiRetour`).
//
// Après un CLIC (choix réel d'un héros), la scène se GÈLE sur ce choix : survoler les autres tuiles ne la fait
// plus bouger. Seul un nouveau clic (un autre héros choisi) la dégèle et la regèle sur le nouveau choix. Sans
// ça, le survol qui suit immédiatement le clic (la souris est toujours sur la grille) écrasait le héros tout
// juste choisi avant même que le joueur ait pu lire sa fiche. Signalé le 27/10/2026.
// Le module est pur : le minuteur est injecté (les tests le font avancer à la main).

export const DELAI_INTENTION = 200;
export const DELAI_RETOUR = 900;

export function creerSurvolHeros({
    afficher,
    revenir,
    minuteur = { set: (fn, ms) => setTimeout(fn, ms), clear: (id) => clearTimeout(id) },
    delaiIntention = DELAI_INTENTION,
    delaiRetour = DELAI_RETOUR,
}) {
    let courant = null; // le héros montré par SURVOL (null : la scène montre le héros du siège)
    let attente = null; // l'intention en cours : { heros, id }
    let retour = null; // le minuteur du retour au héros du siège
    let dansLaScene = false;
    let gele = false; // un clic a figé la scène : le survol n'y touche plus jusqu'au prochain clic

    const annulerAttente = () => {
        if (attente) { minuteur.clear(attente.id); attente = null; }
    };
    const annulerRetour = () => {
        if (retour !== null) { minuteur.clear(retour); retour = null; }
    };
    const montrer = (h) => {
        if (courant === h) return;
        courant = h;
        afficher(h);
    };
    const programmerRetour = () => {
        annulerRetour();
        retour = minuteur.set(() => {
            retour = null;
            if (dansLaScene) return;
            if (courant !== null) {
                courant = null;
                revenir();
            }
        }, delaiRetour);
    };

    return {
        /** La souris entre sur la tuile d'un héros. */
        entrer(h) {
            if (gele) return;
            annulerRetour();
            annulerAttente();
            if (courant === null || courant === h) {
                montrer(h);
                return;
            }
            // Un autre héros est déjà en scène : on attend que la souris s'arrête sur cette tuile.
            attente = { heros: h, id: minuteur.set(() => { attente = null; montrer(h); }, delaiIntention) };
        },
        /** La souris quitte la tuile : la scène garde son héros le temps de rejoindre le bouton. */
        sortir() {
            if (gele) return;
            annulerAttente();
            if (!dansLaScene) programmerRetour();
        },
        /** Clavier : le focus montre le héros tout de suite. */
        entrerAuClavier(h) {
            if (gele) return;
            annulerRetour();
            annulerAttente();
            montrer(h);
        },
        entrerDansLaScene() {
            dansLaScene = true;
            annulerRetour();
            annulerAttente();
        },
        sortirDeLaScene() {
            dansLaScene = false;
            if (!gele) programmerRetour();
        },
        /** Un héros vient d'être CHOISI (clic) : la scène se fige dessus, le survol n'y touche plus
         *  tant qu'un autre choix ne la refige pas. */
        geler(h) {
            annulerAttente();
            annulerRetour();
            gele = true;
            courant = h;
            afficher(h); // toujours redessiné (même héros ou null) : `montrer` ignorerait un héros déjà en scène par survol
        },
        /** Changement d'étape : plus rien ne doit revenir sur une scène qui n'existe plus. */
        remettreAZero() {
            annulerAttente();
            annulerRetour();
            courant = null;
            dansLaScene = false;
            gele = false;
        },
    };
}
