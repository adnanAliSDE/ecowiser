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

// Video Player
const video = document.getElementById('video'); // Replace 'video' with the ID of your video element
const jumpToTime = (timeStamp) => {
  console.log(timeStamp)
  video.currentTime = 50;
}
/*
const loader = document.getElementById('loader'); // Replace 'loader' with the ID of your loader element

video.addEventListener('loadedmetadata', () => {
  const duration = video.duration;
  const minutes = Math.floor(duration / 60);
  const seconds = Math.floor(duration % 60);
  const formattedDuration = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

  loader.innerHTML = `Loading... ${formattedDuration}`;
});

8 */