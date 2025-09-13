document.addEventListener("DOMContentLoaded", function () {
  const districtBtn = document.getElementById("districtBtn");
  const districtList = document.getElementById("districtList");

  districtList.addEventListener("change", function () {
    const checked = [...districtList.querySelectorAll("input[type=checkbox]:checked")];
    if (checked.length === 0) {
      districtBtn.textContent = "Выберите районы ▾";
    } else if (checked.length <= 3) {
    const names = checked.map(cb => cb.value).join(", ");
      districtBtn.textContent = names + " ▾";
    } else {
        districtBtn.textContent = `Выбрано ${checked.length} районов`;
    }
  });


  // Модалка предпросмотра
    const modal = document.getElementById("modal");
    const modalText = document.getElementById("modalText");
    const closeBtn = document.querySelector(".close");

    // document.getElementsByClassName("sign-btn").forEach(btn => {
    //   btn.addEventListener("click", (e) => {
    //     const appCard = e.target.closest(".app-card");
    //     modalText.textContent = appCard.dataset.text;
    //     modal.style.display = "flex";
    //   });
    // })

    document.querySelectorAll(".sign-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const appCard = e.target.closest(".app-card");
        modalText.textContent = appCard.dataset.text;
        modal.style.display = "flex";
      });
    });

    closeBtn.addEventListener("click", () => modal.style.display = "none");
    window.addEventListener("click", e => { 
      if (e.target === modal) modal.style.display = "none"; 
    });
});

// document.addEventListener("DOMContentLoaded", () => {
//     const searchBtn = document.getElementById("searchBtn");
//     const searchInput = document.getElementById("searchInput");
//     const applicationsList = document.getElementById("applicationsList");
//     const totalCountEl = document.getElementById("totalCount");
//     const foundCountEl = document.getElementById("foundCount");
//     const wordEl = document.getElementById("word");

//     const appCards = Array.from(applicationsList.querySelectorAll(".app-card"));

//     // Установим общее количество
//     totalCountEl.textContent = appCards.length;

//     // Склонение слова "заявление"
//     function declension(num) {
//       num = Math.abs(num) % 100;
//       const n1 = num % 10;
//       if (num > 10 && num < 20) return "заявлений";
//       if (n1 > 1 && n1 < 5) return "заявления";
//       if (n1 === 1) return "заявление";
//       return "заявлений";
//     }

//     function updateCounter(count) {
//       foundCountEl.textContent = count;
//       wordEl.textContent = declension(count);
//     }

//     // Поиск
//     function doSearch() {
//       const query = searchInput.value.trim().toLowerCase();
//       let found = 0;

//       appCards.forEach(card => {
//         const text = card.textContent.toLowerCase();
//         if (text.includes(query)) {
//           card.style.display = "flex";
//           found++;
//         } else {
//           card.style.display = "none";
//         }
//       });

//       updateCounter(found);
//     }

//     searchBtn.addEventListener("click", doSearch);

//     // Поиск по Enter
//     searchInput.addEventListener("keydown", e => {
//       if (e.key === "Enter") {
//         doSearch();
//       }
//     });

//     // При загрузке страницы
//     updateCounter(appCards.length);

//     // Модалка предпросмотра
//     const modal = document.getElementById("modal");
//     const modalText = document.getElementById("modalText");
//     const closeBtn = document.querySelector(".close");

//     document.querySelectorAll(".sign-btn").forEach(btn => {
//       btn.addEventListener("click", (e) => {
//         const appCard = e.target.closest(".app-card");
//         modalText.textContent = appCard.dataset.text;
//         modal.style.display = "flex";
//       });
//     });

//     closeBtn.addEventListener("click", () => modal.style.display = "none");
//     window.addEventListener("click", e => { 
//       if (e.target === modal) modal.style.display = "none"; 
//     });
//   });