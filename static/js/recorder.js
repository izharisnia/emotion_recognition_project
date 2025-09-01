// Web Speech API (browser STT) + analyze call
(() => {
  const recBtn = document.getElementById("recBtn");
  const textBox = document.getElementById("transcriptBox");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const resultWrap = document.getElementById("resultWrap");
  const notification = document.getElementById("notification");

  let recognition = null;
  let listening = false;

  function showNotification(message, isError = false) {
    notification.innerText = message;
    notification.style.display = 'block';
    notification.classList.remove('bg-green-500', 'bg-red-500', 'opacity-0', 'scale-95');
    if (isError) {
      notification.classList.add('bg-red-500');
    } else {
      notification.classList.add('bg-green-500');
    }
    
    // Animate in
    setTimeout(() => {
      notification.classList.add('opacity-100', 'scale-100');
    }, 10);

    // Animate out
    setTimeout(() => {
      notification.classList.remove('opacity-100', 'scale-100');
      notification.classList.add('opacity-0', 'scale-95');
    }, 3000);
  }

  function initSTT(){
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!SR) return null;
    const r = new SR();
    r.lang = "en-US";
    r.interimResults = false; // Set to false to get final results only
    r.continuous = false; // Set to false to stop listening after a pause
    
    r.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      textBox.value = transcript.trim();
    };
    
    r.onerror = (event) => {
      stop();
      if (event.error !== 'no-speech') {
        showNotification(`Error: ${event.error}. Please try again.`, true);
      }
    };
    
    r.onend = () => {
      // This event fires when the speech recognition service has disconnected.
      // We can trigger the analysis here.
      stop();
      if (textBox.value.trim() !== "") {
        analyze();
      }
    };
    
    return r;
  }

  function start(){
    if(!recognition){ recognition = initSTT(); }
    if(recognition){
      listening = true;
      recognition.start();
      recBtn.innerText = "Stop Recording";
      recBtn.classList.add("bg-red-500","text-white");
      showNotification("Listening...", false);
    }else{
      showNotification("Your browser doesn't support Speech Recognition. Type instead.", true);
    }
  }

  function stop(){
    if(recognition && listening){
      recognition.stop();
    }
    listening = false;
    recBtn.innerText = "Start Recording";
    recBtn.classList.remove("bg-red-500","text-white");
  }

  async function analyze(){
    const transcript = (textBox.value || "").trim();
    if(!transcript){ showNotification("Say something or type your mood!", true); return; }
    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "Analyzing…";

    const r = await fetch("/analyze", {
      method:"POST",
      headers:{ "Content-Type":"application/json" },
      body: JSON.stringify({ transcript, audio_seconds: 0 })
    });
    const data = await r.json();
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = "Generate My Recipe";

    if(!data.ok){ showNotification(data.error || "Failed", true); return; }

    resultWrap.innerHTML = `
      <div class="card-soft p-5 bg-white mt-6">
        <div class="text-sm text-slate-500">Detected mood</div>
        <div class="text-2xl font-semibold capitalize mt-1">${data.mood}
          <span class="text-sm font-normal text-slate-500">(${(data.confidence*100).toFixed(0)}%)</span>
        </div>
        <div class="mt-4 flex items-center gap-4">
          <img src="${data.recipe.image_url || 'https://placehold.co/400x300?text=No+Image'}"
               class="w-28 h-28 object-cover rounded-xl" alt="">
          <div>
            <div class="font-semibold text-lg">${data.recipe.title}</div>
            <p class="text-slate-600 text-sm line-clamp-3">${data.recipe.description || ''}</p>
            <a class="mt-3 inline-block btn-accent px-4 py-2 rounded-xl"
               href="/recipe/${data.recipe.id}?mood=${encodeURIComponent(data.mood)}">
               View Recipe
            </a>
          </div>
        </div>
      </div>`;
    window.scrollTo({ top: document.body.scrollHeight, behavior:'smooth' });
  }

  recBtn?.addEventListener("click", () => listening ? stop() : start());
  analyzeBtn?.addEventListener("click", analyze);
})();
