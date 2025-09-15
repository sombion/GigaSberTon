document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".menu-btn");
  const sections = document.querySelectorAll(".form-container > div");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // убираем активный класс у всех кнопок
      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      // скрываем все секции
      sections.forEach((section) => {
        section.style.display = "none";
      });

      // показываем нужную секцию
      const target = btn.dataset.section;
      const targetSection = document.querySelector(`.${target}-section`);
      if (targetSection) {
        targetSection.style.display = "block";
      }

      // если кнопка "Выйти" — можно тут повесить логику выхода
      if (target === "login") {
        window.location.href = "/logout.html";
      }
    });
  });
});
