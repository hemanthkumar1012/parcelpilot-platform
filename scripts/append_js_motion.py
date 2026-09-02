with open('frontend/app.js', 'a', encoding='utf-8') as f:
    f.write("""
// --- ANIMATIONS AND MOTION (Step 4) ---
document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting) entry.target.classList.add("is-visible");
    });
  }, { threshold: 0.1 });
  
  setTimeout(() => {
    document.querySelectorAll(".panel, .stat-card, .panel-recent, .login-form-card").forEach((el, index) => {
      el.classList.add("animate-on-scroll");
      el.style.transitionDelay = `${index * 50}ms`;
      observer.observe(el);
    });

    const animateValue = (obj, start, end, duration) => {
      let startTimestamp = null;
      const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const easeOut = progress * (2 - progress);
        obj.innerHTML = Math.floor(easeOut * (end - start) + start);
        if (progress < 1) window.requestAnimationFrame(step);
      };
      window.requestAnimationFrame(step);
    };

    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      document.querySelectorAll(".stat-value").forEach(el => {
        const val = parseInt(el.innerText, 10);
        if(!isNaN(val) && val > 0) animateValue(el, 0, val, 1000);
      });
    }
  }, 500);

  document.body.classList.add("page-enter");
});
""")
