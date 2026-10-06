'use strict';

// toggle the "active" class on an element
const elementToggleFunc = function (elem) { elem.classList.toggle("active"); };

// sidebar: show/hide contact info on small screens
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

if (sidebar && sidebarBtn) {
  sidebarBtn.addEventListener("click", function () { elementToggleFunc(sidebar); });
}

// page navigation (About / Resume / Projects)
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

const showPage = function (name) {
  let found = false;
  pages.forEach(function (page) {
    const match = page.dataset.page === name;
    page.classList.toggle("active", match);
    if (match) found = true;
  });
  navigationLinks.forEach(function (link) {
    link.classList.toggle("active", link.dataset.navLink === name);
  });
  return found;
};

navigationLinks.forEach(function (link) {
  link.addEventListener("click", function () {
    const name = this.dataset.navLink;
    if (showPage(name)) {
      history.replaceState(null, "", "#" + name);
      window.scrollTo(0, 0);
    }
  });
});

// open the page named in the URL hash, e.g. index.html#projects
if (location.hash) {
  showPage(location.hash.slice(1));
}
