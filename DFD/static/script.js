const dropArea        = document.getElementById('drop-area');
const videoInput      = document.getElementById('video');
const submitBtn       = document.getElementById('submit-btn');
const previewContainer= document.getElementById('video-preview-container');
const previewVideo    = document.getElementById('video-preview');
const clearBtn        = document.getElementById('clear-video');
const resultPanel     = document.getElementById('result-panel');
const loadingSpinner  = document.getElementById('loading-spinner');
const resultLabel     = document.getElementById('result-label');
const confidenceScore = document.getElementById('confidence-score');

// Prevent default drag behaviors
['dragenter','dragover','dragleave','drop'].forEach(evt=>{
  dropArea.addEventListener(evt,e=>{
    e.preventDefault(); e.stopPropagation();
  });
});

// Highlight on drag over
['dragenter','dragover'].forEach(evt=>{
  dropArea.addEventListener(evt,()=>{
    dropArea.classList.add('border-accent','bg-neon/10','animate-pulse');
  });
});

// Un-highlight on leave/drop
['dragleave','drop'].forEach(evt=>{
  dropArea.addEventListener(evt,()=>{
    dropArea.classList.remove('border-accent','bg-neon/10','animate-pulse');
  });
});

// Handle drop
dropArea.addEventListener('drop',e=>{
  const files = e.dataTransfer.files;
  if(files.length){
    videoInput.files = files;
    videoInput.dispatchEvent(new Event('change'));

    dropArea.classList.add('animate-bounceOnce');
    dropArea.addEventListener('animationend',()=>dropArea.classList.remove('animate-bounceOnce'),{once:true});
  }
});


// Update preview on file select
videoInput.addEventListener('change',()=>{
  resultPanel.classList.add('hidden');
  resultLabel.textContent   = '';
  confidenceScore.textContent = '';

  if(videoInput.files.length){
    submitBtn.disabled = false;
    previewVideo.src   = URL.createObjectURL(videoInput.files[0]);
    previewContainer.classList.remove('hidden');
    previewContainer.classList.add('animate-fadeInQuick','opacity-100');
  } else {
    submitBtn.disabled = true;
    previewContainer.classList.add('hidden');
    previewVideo.src='';
  }
});

// Clear
clearBtn.addEventListener('click',()=>{
  videoInput.value='';
  submitBtn.disabled = true;
  previewContainer.classList.add('hidden');
  previewVideo.src='';
  resultPanel.classList.add('hidden');
});

// Submit (AJAX)
document.getElementById('upload-form').addEventListener('submit',e=>{
  e.preventDefault();

  resultPanel.classList.add('hidden');
  loadingSpinner.classList.remove('hidden');

  const formData = new FormData(e.target);

  fetch(e.target.action,{
      method:'POST',
      body:formData,
      headers:{'X-Requested-With':'XMLHttpRequest'}
  })
  .then(r=>r.json())
  .then(data=>{
      loadingSpinner.classList.add('hidden');
      resultLabel.textContent     = data.output;
      confidenceScore.textContent = `Confidence: ${data.confidence.toFixed(2)}%`;
      resultPanel.classList.remove('hidden');
      resultPanel.classList.add('animate-fadeScaleIn','opacity-100');
      resultPanel.addEventListener('animationend',()=>resultPanel.classList.remove('animate-fadeScaleIn'),{once:true});
  })
  .catch(()=>{
      loadingSpinner.classList.add('hidden');
      alert('Error processing video.');
  });
});
