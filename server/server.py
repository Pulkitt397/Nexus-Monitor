import time
import psutil
import requests
import subprocess
import os
import pyperclip
from flask import Flask, jsonify, request
from collections import deque
from datetime import datetime

PORT = 5000
LHM_URL = "http://192.168.29.174:8090/data.json"
app = Flask(__name__)

now = datetime.now()
current_datetime = now.strftime("%A, %d %B %Y, %H:%M")
last_net_io = psutil.net_io_counters()
last_time = time.time()
cpu_temp_buffer = deque(maxlen=3)
gpu_load_buffer = deque(maxlen=3)


def smooth_temp(raw_temp):
    if raw_temp > 0:
        cpu_temp_buffer.append(raw_temp)
        return round(sum(cpu_temp_buffer) / len(cpu_temp_buffer), 1)
    return 0


def fetch_lhm_sensors():
    cpu_temp = 0
    gpu_temp = 0
    gpu_load = 0
    fps = 0

    try:
        resp = requests.get(LHM_URL, timeout=1)
        if resp.status_code != 200:
            return cpu_temp, gpu_temp, gpu_load, fps

        data = resp.json()

        # --- UNIVERSAL GPU FINDER ---
        gpu_node = None
        # Keywords to identify common GPUs (NVIDIA, AMD, Intel)
        gpu_keywords = ["radeon", "nvidia", "geforce", "rtx", "gtx", "arc", "intel hd", "intel uhd", "iris"]

        def find_gpu(node):
            nonlocal gpu_node
            if "Text" in node:
                name = node["Text"].lower()
                if any(keyword in name for keyword in gpu_keywords):
                    gpu_node = node
                    return
            
            if "Children" in node:
                for child in node["Children"]:
                    find_gpu(child)
                    if gpu_node: return

        find_gpu(data)
        # -----------------------------

        # Scan CPU temp from root
        def scan_cpu(node):
            nonlocal cpu_temp
            if "Text" in node and "Value" in node:
                name = node["Text"]
                value_str = node["Value"]
                try:
                    value = float(value_str.replace("°C", "").replace("°c", "").strip())
                except:
                    value = 0

                if name == "CPU Package" and "°C" in value_str:
                    cpu_temp = value
                elif name == "Core Average" and "°C" in value_str and cpu_temp == 0:
                    cpu_temp = value

            if "Children" in node:
                for child in node["Children"]:
                    scan_cpu(child)

        scan_cpu(data)

        # Scan GPU from the found node
        if gpu_node:
            def scan_gpu(node):
                nonlocal gpu_temp, gpu_load, fps
                if "Text" in node and "Value" in node:
                    name = node["Text"]
                    value_str = node["Value"]
                    try:
                        value = float(
                            value_str.replace("°C", "")
                            .replace("°c", "")
                            .replace("%", "")
                            .strip()
                        )
                    except:
                        value = 0

                    if name == "GPU Core" and "°C" in value_str:
                        gpu_temp = value
                    
                    # Check for load (covers both "D3D 3D" and generic "GPU Core" load)
                    if (name == "D3D 3D" or name == "GPU Core") and "%" in value_str:
                        if value > gpu_load:
                            gpu_load = value
                            
                    if name == "Fullscreen FPS" and value > 0:
                        fps = int(value)

                if "Children" in node:
                    for child in node["Children"]:
                        scan_gpu(child)

            scan_gpu(gpu_node)

    except:
        pass

    if gpu_load > 0:
        gpu_load_buffer.append(gpu_load)
        gpu_load = round(sum(gpu_load_buffer) / len(gpu_load_buffer), 1)

    return smooth_temp(cpu_temp), gpu_temp, gpu_load, fps


@app.route('/stats')
def stats():
    global last_net_io, last_time

    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent

    download = 0.0
    upload = 0.0
    try:
        current_net = psutil.net_io_counters()
        now = time.time()
        elapsed = now - last_time

        if elapsed > 0.1:
            download = (current_net.bytes_recv - last_net_io.bytes_recv) / 1024 / 1024 / elapsed
            upload = (current_net.bytes_sent - last_net_io.bytes_sent) / 1024 / 1024 / elapsed
            last_net_io = current_net
            last_time = now
    except:
        pass

    cpu_temp, gpu_temp, gpu_usage, fps = fetch_lhm_sensors()

    return jsonify({
        "cpu": cpu_usage,
        "ram": ram_usage,
        "gpu": gpu_usage,
        "cpu_temp": cpu_temp,
        "gpu_temp": gpu_temp,
        "download": round(download, 1),
        "upload": round(upload, 1),
        "fps": fps
    })


@app.route('/gaming_mode')
def gaming_mode():
    """Close apps and clear RAM for gaming"""
    try:
        # Kill processes
        apps_to_close = ['chrome.exe', 'msedge.exe', 'spotify.exe', 'ChatGPT.exe']
        for app in apps_to_close:
            subprocess.run(f'taskkill /F /IM {app}', shell=True, capture_output=True)

        # Clear RAM cache
        subprocess.run(
            'powershell.exe -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"',
            shell=True, capture_output=True
        )
        subprocess.run(
            'powershell.exe -Command "[System.GC]::Collect()"',
            shell=True, capture_output=True
        )

        # Empty standby list (requires admin)
        subprocess.run(
            'powershell.exe -Command "Clear-Host"',
            shell=True, capture_output=True
        )

        return jsonify({"status": "success", "message": "Gaming Mode Active"})
    except:
        return jsonify({"status": "error", "message": "Failed"})


# ---------- Groq AI chat ----------
@app.route('/ai_chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # 1) Live PC status
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram_usage = psutil.virtual_memory().percent
        cputemp, gputemp, gpu_usage, fps = fetch_lhm_sensors()

        status_context = (
            f"Current date and time: {current_datetime}. "
            "Live PC snapshot: "
            f"CPU usage {cpu_usage:.0f}%, GPU usage {gpu_usage:.0f}%, "
            f"RAM usage {ram_usage:.0f}%, "
            f"CPU temperature {cputemp:.0f}°C, GPU temperature {gputemp:.0f}°C. "
            "If temps are above 80°C treat them as high; above 90°C as very high. "
            "If usage is above 85% consider it heavy load."
        )

        # 2) System prompt
        system_prompt = (
            "You are LAMA Stands For Bhondu PC Monitor AI inside a desktop monitoring app. "
            "You can answer general questions about the world, code, and dates. "
            "Use the date/time and PC status I give you when relevant. "
            "Do not say you lack access to the system or calendar; just answer directly. "
            "Keep answers short (2–4 sentences) unless the user asks for more detail."
        )

        groq_api_key = "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"  # <--- YOUR KEY HERE

        groq_response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {groq_api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'system', 'content': status_context},
                    {'role': 'user', 'content': user_message},
                ],
                'temperature': 0.6,
                'max_tokens': 512,
            },
            timeout=10,
        )

        if groq_response.status_code == 200:
            ai_reply = groq_response.json()['choices'][0]['message']['content']
            return jsonify({'reply': ai_reply})
        else:
            return jsonify({'error': f'Groq API error: {groq_response.status_code}'}), 500

    except Exception as e:
        print("AI_CHAT ERROR:", e)
        return jsonify({'error': str(e)}), 500


# ---------- NEW: Clipboard Features ----------
@app.route('/clipboard', methods=['GET'])
def get_clipboard():
    """PC -> Phone: Send current PC clipboard text"""
    try:
        text = pyperclip.paste()
        return jsonify({"status": "success", "content": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/clipboard', methods=['POST'])
def set_clipboard():
    """Phone -> PC: Receive text and copy to PC clipboard"""
    try:
        data = request.json
        if not data or 'content' not in data:
            return jsonify({"status": "error", "message": "No content provided"}), 400
        
        text_to_copy = data['content']
        pyperclip.copy(text_to_copy)
        print(f"📋 Clipboard updated via Phone: {text_to_copy}")
        return jsonify({"status": "success", "message": "Clipboard updated on PC"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Server running on port", PORT)
    app.run(host='0.0.0.0', port=PORT, debug=False)
