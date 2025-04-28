document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const form = document.getElementById("upload-form");
  const message = document.getElementById("message");
  const progressBar = document.getElementById("progress-bar");
  const progressContainer = document.getElementById("progress-container");

  let selectedFile = null;

  // Click to open file picker
  dropzone.addEventListener("click", () => fileInput.click());

  // Drag styling
  dropzone.addEventListener("dragover", e => {
      e.preventDefault();
      dropzone.classList.add("bg-light");
  });

  dropzone.addEventListener("dragleave", () => {
      dropzone.classList.remove("bg-light");
  });

  // File dropped
  dropzone.addEventListener("drop", e => {
      e.preventDefault();
      dropzone.classList.remove("bg-light");
      selectedFile = e.dataTransfer.files[0];
      dropzone.textContent = selectedFile.name;
  });

  // File chosen manually
  fileInput.addEventListener("change", () => {
      selectedFile = fileInput.files[0];
      dropzone.textContent = selectedFile.name;
  });

  // Form submit
  form.addEventListener("submit", async e => {
      e.preventDefault();
      if (!selectedFile) return alert("Please select a PDF file.");

      // Reset UI
      message.innerHTML = "";
      progressBar.style.width = "0%";
      progressContainer.style.display = "block";

      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
          const xhr = new XMLHttpRequest();

          xhr.open("POST", "/upload/", true);
          xhr.responseType = "blob";

          xhr.upload.onprogress = function (e) {
              if (e.lengthComputable) {
                  const percent = (e.loaded / e.total) * 100;
                  progressBar.style.width = percent + "%";
                  progressBar.textContent = Math.floor(percent) + "%";
              }
          };

          xhr.onload = function () {
              if (xhr.status === 200) {
                  const blob = xhr.response;
                  const previewUrl = URL.createObjectURL(blob);

                  // Preview image
                  const imgPreview = document.createElement("img");
                  imgPreview.src = previewUrl;
                  imgPreview.classList.add("img-fluid", "my-3", "border", "rounded");

                  message.innerHTML = "";
                  message.appendChild(imgPreview);

                  // Trigger download
                  const a = document.createElement("a");
                  a.href = previewUrl;
                  a.download = selectedFile.name.replace(".pdf", ".tiff");
                  a.click();

                  URL.revokeObjectURL(previewUrl);
              } else {
                  message.textContent = "❌ Conversion failed.";
              }

              progressBar.style.width = "100%";
              progressBar.textContent = "Done";
              setTimeout(() => {
                  progressContainer.style.display = "none";
                  progressBar.style.width = "0%";
                  progressBar.textContent = "";
              }, 1500);
          };

          xhr.onerror = function () {
              message.textContent = "❌ Upload failed.";
              progressContainer.style.display = "none";
          };

          xhr.send(formData);
      } catch (err) {
          console.error(err);
          message.textContent = "❌ Something went wrong.";
          progressContainer.style.display = "none";
      }
  });
});