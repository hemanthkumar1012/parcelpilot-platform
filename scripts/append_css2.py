with open('frontend/style.css', 'a', encoding='utf-8') as f:
    f.write("""

/* ==========================================================================
   ANIMATIONS & MOTION (Step 4)
   ========================================================================== */

/* Skeleton Loader */
@keyframes pulseSkeleton {
  0% { background-color: var(--border-light); }
  50% { background-color: var(--bg-tertiary); }
  100% { background-color: var(--border-light); }
}

.skeleton, .skeleton * {
  animation: pulseSkeleton 1.5s infinite ease-in-out !important;
  color: transparent !important;
  border-color: transparent !important;
  border-radius: var(--radius-md);
}

/* Scroll Reveal */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 400ms ease, transform 400ms ease;
}

.animate-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Page Transitions */
@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-enter {
  animation: slideUpFade 400ms forwards;
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .animate-on-scroll {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
""")
