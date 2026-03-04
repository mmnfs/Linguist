import os

# Read the HTML file
html_path = 'reading_ordering_exercise.html'
with open(html_path, 'r') as f:
    html_content = f.read()

# Target header
target_header_old = """            <!-- Card Header -->
            <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center gap-6">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary shrink-0">
                        <span class="material-symbols-outlined text-2xl">menu_book</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">Read the text</p>
                        <h3 class="text-xl font-bold text-slate-900 dark:text-white leading-none">A Busy Morning</h3>
                    </div>
                </div>
            </div>"""

target_header_new = """            <!-- Card Header -->
            <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary shrink-0">
                        <span class="material-symbols-outlined text-2xl">menu_book</span>
                    </div>
                    <div>
                        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">Read the text</p>
                        <h3 class="text-xl font-bold text-slate-900 dark:text-white leading-none">A Busy Morning</h3>
                    </div>
                </div>
                <!-- Audio Player Controls -->
                <div class="flex flex-wrap items-center gap-3">
                    <button id="btn-play" class="flex items-center gap-2 bg-primary hover:bg-primary/90 text-background-dark px-6 py-2.5 rounded-lg font-bold transition-all shadow-lg shadow-primary/20">
                        <span class="material-symbols-outlined">volume_up</span>
                        <span>Play Text</span>
                    </button>
                    <div class="flex items-center bg-slate-200 dark:bg-slate-800 rounded-lg p-1">
                        <button id="speed-075" class="px-3 py-1.5 text-xs font-bold rounded-md text-slate-500 dark:text-slate-400 hover:text-primary transition-colors">0.75x</button>
                        <button id="speed-100" class="px-3 py-1.5 text-xs font-bold rounded-md bg-white dark:bg-slate-700 text-primary shadow-sm">1x</button>
                        <button id="speed-125" class="px-3 py-1.5 text-xs font-bold rounded-md text-slate-500 dark:text-slate-400 hover:text-primary transition-colors">1.25x</button>
                    </div>
                </div>
            </div>"""

# Ensure the header is replaced properly
if target_header_old in html_content:
    html_content = html_content.replace(target_header_old, target_header_new)
else:
    print("Warning: Could not find exactly the Card Header in the HTML. Replacing visually.")

# Now for the JS section. Replace inside the `<script>` block before `// Init`.
# Read base64
with open('reading_audio.b64', 'r') as f:
    b64_audio = f.read().strip()

target_js_old = """        // Init
        renderItems(currentOrder);"""

target_js_new = """        // Audio Playback
        const btnPlay = document.getElementById('btn-play');
        const speedBtns = {
            "0.75": document.getElementById("speed-075"),
            "1.0": document.getElementById("speed-100"),
            "1.25": document.getElementById("speed-125")
        };
        let currentRate = 1.0;

        const audioPath = "data:audio/mp3;base64,""" + b64_audio + """";
        const audioElement = new Audio(audioPath);

        function playAudio() {
            audioElement.pause();
            audioElement.currentTime = 0;
            audioElement.playbackRate = currentRate;
            audioElement.preservesPitch = true;
            audioElement.play().catch(error => {
                console.error("Audio playback failed:", error);
                alert("Sorry, there was an error playing the audio file!");
            });
        }

        if (btnPlay) {
            btnPlay.addEventListener("click", playAudio);
        }

        // Speed controls
        function updateSpeedButtonStyles(activeKey) {
            Object.keys(speedBtns).forEach(key => {
                const btn = speedBtns[key];
                if(btn) {
                    if (key === activeKey) {
                        btn.classList.remove("bg-transparent", "text-slate-500", "dark:text-slate-400");
                        btn.classList.add("bg-white", "dark:bg-slate-700", "text-primary", "shadow-sm");
                    } else {
                        btn.classList.add("bg-transparent", "text-slate-500", "dark:text-slate-400");
                        btn.classList.remove("bg-white", "dark:bg-slate-700", "text-primary", "shadow-sm");
                    }
                }
            });
        }

        Object.keys(speedBtns).forEach(key => {
            if(speedBtns[key]) {
                speedBtns[key].addEventListener("click", () => { currentRate = parseFloat(key); updateSpeedButtonStyles(key); });
            }
        });

        // Init
        renderItems(currentOrder);"""

if target_js_old in html_content:
    html_content = html_content.replace(target_js_old, target_js_new)
else:
    print("Warning: Could not find exactly the Init script tag in the HTML.")

with open(html_path, 'w') as f:
    f.write(html_content)

print("Updated reading_ordering_exercise.html successfully.")
