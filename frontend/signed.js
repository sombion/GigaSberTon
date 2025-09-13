document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("searchBtn");
    const searchInput = document.getElementById("searchInput");
    const docsList = document.getElementById("docsList");
    const totalCountEl = document.getElementById("totalCount");
    const foundCountEl = document.getElementById("foundCount");
    const wordEl = document.getElementById("word");

    const docCards = Array.from(docsList.querySelectorAll(".app-card"));

    // Всего
    totalCountEl.textContent = docCards.length;

    function declension(num) {
      num = Math.abs(num) % 100;
      const n1 = num % 10;
      if (num > 10 && num < 20) return "документов";
      if (n1 > 1 && n1 < 5) return "документа";
      if (n1 === 1) return "документ";
      return "документов";
    }

    function updateCounter(count) {
      foundCountEl.textContent = count;
      wordEl.textContent = declension(count);
    }

    function doSearch() {
      const query = searchInput.value.trim().toLowerCase();
      let found = 0;

      docCards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = "flex";
          found++;
        } else {
          card.style.display = "none";
        }
      });

      updateCounter(found);
    }

    searchBtn.addEventListener("click", doSearch);
    searchInput.addEventListener("keydown", e => {
      if (e.key === "Enter") doSearch();
    });

    updateCounter(docCards.length);
});