/* Onglet « Decks des joueurs » de /admin (19/10/2026).
 *
 * Deux parties :
 *  - `rendre(donnees, textes)` : PURE, rend le HTML de la liste (testee sous
 *    node : site/test-admin-decks-joueurs.mjs) ;
 *  - `monter(racine, textes)` : branche la liste sur les deux routes du site.
 * Tout ce qui vient du serveur passe par `echapper` : un nom de deck est ecrit
 * par un joueur.
 * Le serveur reste seul juge : cacher un bouton n'est pas une protection. */
(function (racine) {
  function echapper(t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function rendre(donnees, textes) {
    var comptes = (donnees && donnees.comptes) || [];
    if (!comptes.length) return '<p class="vide">' + echapper(textes.aucun) + "</p>";
    return comptes.map(function (c) {
      var lignes = c.decks.map(function (d) {
        return '<li class="dj-deck">' +
          '<div class="dj-infos"><strong>' + echapper(d.nom) + "</strong>" +
          '<span class="dj-meta">' + echapper(d.heros) + " · " + echapper(d.cartes) + " " +
          echapper(textes.cartes) + " · " + echapper(d.date) + "</span></div>" +
          '<button type="button" class="dj-importer" data-compte="' + echapper(c.compte) +
          '" data-deck="' + echapper(d.id) + '" data-nom="' + echapper(d.nom) + '">' +
          echapper(textes.importer) + "</button></li>";
      }).join("");
      return '<section class="dj-compte"><h3>' + echapper(c.compte) +
        ' <span class="compte">' + c.decks.length + "</span></h3><ul>" + lignes + "</ul></section>";
    }).join("");
  }

  function monter(zone, textes) {
    var liste = zone.querySelector(".dj-liste");
    var message = zone.querySelector(".dj-message");
    function dire(texte, erreur) {
      message.textContent = texte;
      message.className = "dj-message" + (erreur ? " dj-erreur" : texte ? " dj-ok" : "");
    }
    function charger() {
      dire("", false);
      return fetch("/api/admin/decks-joueurs", { credentials: "same-origin" })
        .then(function (r) {
          if (!r.ok) throw new Error(String(r.status));
          return r.json();
        })
        .then(function (j) { liste.innerHTML = rendre(j, textes); })
        .catch(function () { liste.innerHTML = ""; dire(textes.echec_liste, true); });
    }
    liste.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".dj-importer");
      if (!b) return;
      var question = textes.confirmer.replace("{deck}", b.dataset.nom).replace("{compte}", b.dataset.compte);
      if (!window.confirm(question)) return;
      b.disabled = true;
      fetch("/api/admin/decks-joueurs/importer", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "X-Importer-Deck": "1" },
        body: "compte=" + encodeURIComponent(b.dataset.compte) + "&deck=" + encodeURIComponent(b.dataset.deck)
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) dire(textes.reussi.replace("{fichier}", res.j.fichier), false);
          else dire(textes.echec_import + " (" + (res.j.error || "?") + ")", true);
        })
        .catch(function () { dire(textes.echec_import, true); })
        .then(function () { b.disabled = false; });
    });
    zone.querySelector(".dj-actualiser").addEventListener("click", charger);
    return charger();
  }

  var api = { rendre: rendre, monter: monter, echapper: echapper };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else racine.DecksJoueursAdmin = api;
})(typeof window !== "undefined" ? window : this);
