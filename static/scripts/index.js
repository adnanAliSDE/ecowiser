const submitBtn = document.querySelector("#submitBtn");
console.log(submitBtn);
submitBtn.addEventListener('click',
  function lambda(e) {
    e.preventDefault()
  }
);

const btnContainer = document.querySelector(".uploadSection .btnContainer");
const uploadForm = document.querySelector(".uploadSection form");
const uploadSection = document.querySelector(".uploadSection");