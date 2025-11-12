#!/usr/bin/env python3
import json, sys, os, time, subprocess
from pathlib import Path

def sh(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def write_json(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2))

def main():
    if len(sys.argv) < 4:
        print("Usage: orchestrator.py <task_json> <OUTPUT_DIR> <TEMP_DIR>")
        sys.exit(1)

    task_json = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    temp_dir = Path(sys.argv[3])

    if not task_json.exists():
        print("Task json not found")
        sys.exit(2)

    task = json.loads(task_json.read_text())
    task["status"] = "running"
    task.setdefault("notes", []).append("Boss AI started.")
    write_json(task_json, task)

    audio = task["inputs"].get("audio")
    videos = task["inputs"].get("videos", [])

    # Simulate worker steps
    # 1) Audio analysis (BPM, mood) — stub
    time.sleep(0.5)
    audio_result = {
        "bpm": 120,
        "mood": "energetic",
        "peaks": [1.0, 3.2, 7.5, 12.0]
    }
    Path(temp_dir / f"{task['id']}_audio.json").write_text(json.dumps(audio_result, indent=2))
    task["notes"].append("Audio analyzed.")

    # 2) Scene detection — stub
    time.sleep(0.5)
    scene_result = {
        "scenes": [{"start":0,"end":3}, {"start":3,"end":7}, {"start":7,"end":12}]
    }
    Path(temp_dir / f"{task['id']}_scenes.json").write_text(json.dumps(scene_result, indent=2))
    task["notes"].append("Scenes detected.")

    # 3) Lyric align — stub
    time.sleep(0.5)
    lyric_result = {
        "lines": [
            {"t":0.0, "text":"(intro)"},
            {"t":1.2, "text":"feel the beat"},
            {"t":3.5, "text":"cut to motion"},
            {"t":7.0, "text":"rise to hook"}
        ]
    }
    Path(temp_dir / f"{task['id']}_lyrics.json").write_text(json.dumps(lyric_result, indent=2))
    task["notes"].append("Lyrics aligned.")

    # 4) Edit plan — combine
    edit_plan = {
        "bpm": audio_result["bpm"],
        "mood": audio_result["mood"],
        "timeline": scene_result["scenes"],
        "captions": lyric_result["lines"]
    }
    edit_plan_path = temp_dir / f"{task['id']}_edit_plan.json"
    edit_plan_path.write_text(json.dumps(edit_plan, indent=2))
    task["notes"].append("Edit plan generated.")

    # 5) Render preview (safe fallback):
    # If user passed multiple video clips, concat. Else, re-encode single.
    out_name = f"preview_{int(time.time()*1000)}.mp4"
    out_path = output_dir / out_name
    if len(videos) > 1:
        concat_list = temp_dir / f"concat_{task['id']}.txt"
        concat_list.write_text("\n".join([f"file '{v}'" for v in videos]))
        cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c:v libx264 -preset ultrafast -crf 25 -c:a aac "{out_path}"'
        proc = sh(cmd)
        try: concat_list.unlink()
        except: pass
        if proc.returncode != 0:
            task["status"] = "error"
            task["notes"].append("FFmpeg concat failed.")
            write_json(task_json, task)
            print(proc.stderr.decode()[:500])
            sys.exit(3)
    elif len(videos) == 1:
        cmd = f'ffmpeg -y -i "{videos[0]}" -c:v libx264 -preset ultrafast -crf 25 -c:a aac "{out_path}"'
        proc = sh(cmd)
        if proc.returncode != 0:
            task["status"] = "error"
            task["notes"].append("FFmpeg transcode failed.")
            write_json(task_json, task)
            print(proc.stderr.decode()[:500])
            sys.exit(3)
    else:
        # no videos — create a black preview
        cmd = f'ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=5 -vf "drawtext=text=PREVIEW:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" "{out_path}"'
        sh(cmd)

    task["status"] = "completed"
    task["output"] = str(out_path)
    task["notes"].append("Preview render completed.")
    write_json(task_json, task)
    print(f"✅ Done: {out_path}")

if __name__ == "__main__":
    main()
