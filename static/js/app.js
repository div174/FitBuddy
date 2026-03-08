/**
 * FitBuddy – global JavaScript utilities
 */

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener("click", e => {
    const target = document.querySelector(a.getAttribute("href"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// Auto-dismiss toasts
document.querySelectorAll(".toast").forEach(toast => {
  setTimeout(() => {
    toast.style.transition = "opacity 0.5s";
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 500);
  }, 4500);
});

// Shopping list checkbox toggle
document.querySelectorAll(".shop-item").forEach(item => {
  item.addEventListener("click", () => {
    if (item.textContent.startsWith("✓")) {
      item.textContent = "☐" + item.textContent.slice(1);
      item.style.opacity = "1";
      item.style.textDecoration = "none";
    } else {
      item.textContent = "✓" + item.textContent.slice(1);
      item.style.opacity = "0.5";
      item.style.textDecoration = "line-through";
    }
  });
});

// Print plan helper (can be triggered from UI)
function printPlan() {
  window.print();
}
