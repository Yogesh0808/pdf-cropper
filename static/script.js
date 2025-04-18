const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');

dropArea.addEventListener('click', () => fileInput.click());

dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.classList.add('bg-light');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('bg-light');
});

dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.classList.remove('bg-light');
  const files = e.dataTransfer.files;
  fileInput.files = files;
  showPreview(files);
});

fileInput.addEventListener('change', () => {
  showPreview(fileInput.files);
});

function showPreview(files) {
  preview.innerHTML = '';
  Array.from(files).forEach(file => {
    const fileBox = document.createElement('div');
    fileBox.className = 'file-box';
    fileBox.innerHTML = `
      <strong>${file.name}</strong><br>
      ${(file.size / 1024).toFixed(1)} KB
      <div class="progress mt-2">
        <div class="progress-bar bg-success" role="progressbar" style="width: 0%"></div>
      </div>
    `;
    preview.appendChild(fileBox);
  });
}

document.getElementById('upload-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const files = fileInput.files;
  if (!files.length) return;

  const previews = document.querySelectorAll('.file-box');

  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append('file', files[i]);

    const res = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = files[i].name.replace('.pdf', '.tiff');
      document.body.appendChild(a);
      a.click();
      a.remove();

      const bar = previews[i].querySelector('.progress-bar');
      bar.style.width = '100%';
      bar.textContent = 'Done';
    } else {
      const bar = previews[i].querySelector('.progress-bar');
      bar.classList.remove('bg-success');
      bar.classList.add('bg-danger');
      bar.style.width = '100%';
      bar.textContent = 'Failed';
    }
  }
});