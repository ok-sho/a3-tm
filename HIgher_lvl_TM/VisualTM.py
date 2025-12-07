import webbrowser
import os
import time


class VisualTM:
    def __init__(self, speed=1):
        self.html_path = None
        self.speed = speed  # Speed in seconds between instructions

    def initiate(self):
        """Initialize the display and open browser"""
        # Write HTML file to current directory
        current_dir = os.getcwd()
        self.html_path = os.path.join(current_dir, 'tm_display.html')

        print(f"Display HTML will be at: {self.html_path}")

        # Create initial HTML file
        self._write_initial_html()

        # Now open in browser
        time.sleep(0.3)
        webbrowser.open('file://' + os.path.abspath(self.html_path))

    def _write_initial_html(self):
        """Write initial HTML with empty state"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Turing Machine Simulator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        }
        .tape-container {
            scroll-behavior: smooth;
        }
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
    <div class="p-8">
        <div class="max-w-6xl mx-auto">
            <h1 class="text-4xl font-bold text-white mb-8 text-center">
                Higher Level Turing Machine Simulator
            </h1>
            <div class="bg-gray-800 rounded-lg p-6 text-center">
                <p class="text-white text-xl">Waiting for first update...</p>
            </div>
        </div>
    </div>
    <script>
        // Auto-refresh every 500ms
        setTimeout(() => {
            location.reload();
        }, 500);
    </script>
</body>
</html>"""

        with open(self.html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def update(self, tape, head_pos, state, curr_instruction_num, instructions):
        """Update the display with current state"""
        if self.html_path is None:
            return

        # Get current instruction for logging
        if state != "ACCEPT" and curr_instruction_num < len(instructions.get(state, [])):
            current_instruction = instructions[state][curr_instruction_num]
        else:
            current_instruction = "ACCEPT"

        # Ensure tape has at least some cells visible
        display_tape = tape[:] if len(tape) > 0 else [0]

        # Extend display to show at least 20 cells or up to headPos + 10
        min_display_length = max(20, head_pos + 10)
        if len(display_tape) < min_display_length:
            display_tape.extend([0] * (min_display_length - len(display_tape)))

        # Get head value
        head_value = display_tape[head_pos] if head_pos < len(display_tape) else 0

        # Generate tape cells HTML
        tape_cells_html = ""
        for idx, cell in enumerate(display_tape):
            is_head = idx == head_pos
            if is_head:
                tape_cells_html += f'''
                <div class="min-w-[80px] h-32 flex items-center justify-center rounded-lg transition-all duration-500 bg-gradient-to-b from-blue-500 to-purple-600 border-2 border-blue-400 scale-105" style="box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);">
                    <span class="text-3xl font-bold text-white">{cell}</span>
                </div>'''
            else:
                tape_cells_html += f'''
                <div class="min-w-[80px] h-32 flex items-center justify-center rounded-lg transition-all duration-500 bg-gradient-to-b from-gray-700 to-gray-800 border border-gray-600">
                    <span class="text-3xl font-bold text-gray-400">{cell}</span>
                </div>'''

        # Create full HTML content with current state
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Turing Machine Simulator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        }}
        .tape-container {{
            /* No smooth scrolling - we control scroll position directly */
        }}
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
    <div class="p-8">
        <div class="max-w-6xl mx-auto">
            <h1 class="text-4xl font-bold text-white mb-8 text-center">
                Higher Level Turing Machine Simulator
            </h1>

            <!-- Tape Display -->
            <div class="bg-gradient-to-b from-gray-800 to-gray-900 rounded-lg p-8 mb-6 shadow-2xl border border-purple-500/30 overflow-hidden relative">
                <h2 class="text-xl font-semibold text-white mb-4">Tape Roll</h2>

                <div id="tapeContainer" class="tape-container overflow-x-auto relative">
                    <div id="tapeRoll" class="flex gap-1 py-4">
                        {tape_cells_html}
                    </div>
                </div>
            </div>

            <!-- State Display -->
            <div class="grid grid-cols-3 gap-4 mb-6">
                <div class="bg-gray-800 rounded-lg p-4 shadow-xl border border-purple-500/20">
                    <h3 class="text-sm font-semibold text-gray-400 mb-2">Current State</h3>
                    <p id="currentState" class="text-2xl font-bold text-purple-400">{state}</p>
                </div>
                <div class="bg-gray-800 rounded-lg p-4 shadow-xl border border-purple-500/20">
                    <h3 class="text-sm font-semibold text-gray-400 mb-2">Head Position</h3>
                    <p id="headPosition" class="text-2xl font-bold text-green-400">{head_pos}</p>
                </div>
                <div class="bg-gray-800 rounded-lg p-4 shadow-xl border border-purple-500/20">
                    <h3 class="text-sm font-semibold text-gray-400 mb-2">Value at Head</h3>
                    <p id="headValue" class="text-2xl font-bold text-yellow-400">{head_value}</p>
                </div>
            </div>

            <!-- Controls -->
            <div class="bg-gray-800 rounded-lg p-6 mb-6 shadow-xl border border-purple-500/20">
                <div class="flex gap-4 items-center justify-center">
                    <button id="pauseBtn" class="bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg transition shadow-lg font-semibold">
                        <span id="pauseText">Pause</span>
                    </button>
                </div>
            </div>

            <!-- Execution Log -->
            <div class="bg-gray-800 rounded-lg p-6 shadow-xl border border-purple-500/20">
                <h2 class="text-xl font-semibold text-white mb-4">Execution Log</h2>
                <div id="logContainer" class="bg-gray-900 rounded p-4 h-48 overflow-y-auto font-mono text-sm">
                    <div class="text-green-400 mb-1">[{state}:{curr_instruction_num}] {current_instruction}</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const tapeContainer = document.getElementById('tapeContainer');
        const cellWidth = 84;
        const headPos = {head_pos};

        // Get saved scroll position from previous load
        let savedScroll = localStorage.getItem('tmScrollPos');

        // On first load, center on head
        if (savedScroll === null) {{
            const containerWidth = tapeContainer.offsetWidth;
            const centerOffset = (containerWidth / 2) - (cellWidth / 2);
            savedScroll = (headPos * cellWidth) - centerOffset;
        }}

        // CRITICAL: Always restore to exact saved position FIRST (instantly, no animation)
        tapeContainer.scrollLeft = parseInt(savedScroll);

        // Now check if head is out of view
        const headPixelPos = headPos * cellWidth;
        const containerWidth = tapeContainer.offsetWidth;
        const visibleStart = tapeContainer.scrollLeft;
        const visibleEnd = tapeContainer.scrollLeft + containerWidth;

        // Only scroll if head is actually out of view (with small margin)
        const margin = 100;
        let needsScroll = false;
        let targetScroll = tapeContainer.scrollLeft;

        if (headPixelPos < visibleStart + margin) {{
            // Head going off left edge - scroll left
            targetScroll = headPixelPos - margin;
            needsScroll = true;
        }} else if (headPixelPos + cellWidth > visibleEnd - margin) {{
            // Head going off right edge - scroll right
            targetScroll = headPixelPos + cellWidth + margin - containerWidth;
            needsScroll = true;
        }}

        if (needsScroll) {{
            // Smooth scroll from current position to target
            tapeContainer.scrollTo({{
                left: targetScroll,
                behavior: 'smooth'
            }});

            // Save the target position (will be reached after animation)
            setTimeout(() => {{
                localStorage.setItem('tmScrollPos', tapeContainer.scrollLeft);
            }}, 400);
        }} else {{
            // Head is in view - save current position immediately
            localStorage.setItem('tmScrollPos', tapeContainer.scrollLeft);
        }}

        // Pause functionality
        const pauseBtn = document.getElementById('pauseBtn');
        const pauseText = document.getElementById('pauseText');

        // Check if paused
        let isPaused = localStorage.getItem('tmPaused') === 'true';

        // Update button text based on pause state
        if (isPaused) {{
            pauseText.textContent = 'Resume';
            pauseBtn.className = 'bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg transition shadow-lg font-semibold';
        }}

        // Toggle pause state on click
        pauseBtn.addEventListener('click', () => {{
            isPaused = !isPaused;
            localStorage.setItem('tmPaused', isPaused);
            if (isPaused) {{
                pauseText.textContent = 'Resume';
                pauseBtn.className = 'bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg transition shadow-lg font-semibold';
            }} else {{
                pauseText.textContent = 'Pause';
                pauseBtn.className = 'bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-lg transition shadow-lg font-semibold';
                // Resume - reload immediately
                location.reload();
            }}
        }});

        // Auto-refresh every 500ms, but stop if state is ACCEPT or paused
        const currentState = '{state}';
        if (currentState !== 'ACCEPT' && !isPaused) {{
            setTimeout(() => {{
                location.reload();
            }}, 500);
        }}
    </script>
</body>
</html>"""

        # Write to HTML file
        try:
            with open(self.html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Updated display: State={state}, HeadPos={head_pos}, TapeLen={len(display_tape)}")
        except Exception as e:
            print(f"Error writing display: {e}")
