function toggleDark() {
  document.body.classList.toggle("dark");

  // save preference
  if (document.body.classList.contains("dark")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}
const form = document.querySelector("form");
  const fileInput = document.querySelector('input[type="file"]');

  function handleSubmit() {
    if (fileInput.files.length > 0) {
      showUploadToast(fileInput.files[0].name);
      form.requestSubmit(); // ✅ triggers submit event properly
    }
  }

  // Mouse submit
  form.addEventListener("submit", function () {
    if (fileInput.files.length > 0) {
      showUploadToast(fileInput.files[0].name);
    }
  });

  // Enter key submit
  document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSubmit();
    }
  });
// load saved theme
window.addEventListener("load", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
  }
});

function showUploadToast(fileName) {
  const toast = document.createElement("div");
  toast.className = "upload-toast";
  toast.innerText = `📄 File "${fileName}" submitted successfully!`;

  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("show"), 100);

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}