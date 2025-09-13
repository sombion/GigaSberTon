document.addEventListener("DOMContentLoaded", () => {
  const districtBtn = document.getElementById("districtBtn");
  const districtDropdown = document.getElementById("districtDropdown");
  const districtSearch = document.getElementById("districtSearch");
  const districtList = document.getElementById("districtList");

  // --- Работа с дропдауном ---
  districtBtn.addEventListener("click", () => {
    districtDropdown.parentElement.classList.toggle("show");
  });

  // Поиск района
  districtSearch.addEventListener("input", () => {
    const query = districtSearch.value.toLowerCase();
    const labels = districtList.querySelectorAll("label");
    labels.forEach(label => {
      const text = label.textContent.toLowerCase();
      label.style.display = text.includes(query) ? "block" : "none";
    });
  });

  // Закрытие дропдауна при клике вне его
  window.addEventListener("click", e => {
    if (!e.target.closest(".dropdown")) {
      districtDropdown.parentElement.classList.remove("show");
    }
  });
});
