#!/usr/bin/env python3
"""
audio_engine.py — Moteur audio partage pour traitement, mixage et conversion

Commandes:
    python audio_engine.py info --input file.mp3
    python audio_engine.py normalize --input file.mp3 --target-lufs -16 --output norm.wav
    python audio_engine.py concat --inputs "a.wav,b.wav,c.wav" --gap 0.5 --output out.wav
    python audio_engine.py mix --tracks "voice.wav:100,music.wav:15" --output mix.wav
    python audio_engine.py fade --input file.wav --fade-in 1.0 --fade-out 2.0 --output faded.wav
    python audio_engine.py convert --input file.wav --format mp3 --bitrate 320k --output out.mp3
    python audio_engine.py trim --input file.wav --start 5.0 --end 30.0 --output trimmed.wav
    python audio_engine.py volume --input file.wav --gain -3 --output quieter.wav
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def run_ffmpeg(args, check=True):
    """Execute ffmpeg avec les arguments donnes."""
    cmd = [FFMPEG, "-y"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"ffmpeg erreur: {result.stderr[:500]}")
    return result


def run_ffprobe(args):
    """Execute ffprobe avec les arguments donnes."""
    cmd = [FFPROBE] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe erreur: {result.stderr[:500]}")
    return result


def cmd_info(args):
    """Affiche les informations d'un fichier audio."""
    input_file = args.input

    # Info basique via ffprobe
    result = run_ffprobe([
        "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams",
        input_file
    ])

    info = json.loads(result.stdout)
    fmt = info.get("format", {})
    streams = info.get("streams", [])

    audio_stream = None
    for s in streams:
        if s.get("codec_type") == "audio":
            audio_stream = s
            break

    output = {
        "file": input_file,
        "format": fmt.get("format_name"),
        "duration_seconds": float(fmt.get("duration", 0)),
        "size_bytes": int(fmt.get("size", 0)),
        "bitrate_kbps": int(fmt.get("bit_rate", 0)) // 1000,
    }

    if audio_stream:
        output.update({
            "codec": audio_stream.get("codec_name"),
            "sample_rate": int(audio_stream.get("sample_rate", 0)),
            "channels": int(audio_stream.get("channels", 0)),
            "bits_per_sample": audio_stream.get("bits_per_raw_sample"),
        })

    # Mesurer le volume (LUFS + peak)
    try:
        vol_result = run_ffmpeg([
            "-i", input_file,
            "-af", "loudnorm=print_format=json",
            "-f", "null", "-"
        ], check=False)

        # Parser le JSON de loudnorm depuis stderr
        stderr = vol_result.stderr
        json_start = stderr.rfind("{")
        json_end = stderr.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            loudnorm_data = json.loads(stderr[json_start:json_end])
            output["input_i"] = loudnorm_data.get("input_i")
            output["input_tp"] = loudnorm_data.get("input_tp")
            output["input_lra"] = loudnorm_data.get("input_lra")
    except Exception:
        pass

    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_normalize(args):
    """Normalise le volume d'un fichier audio au LUFS cible."""
    target_lufs = args.target_lufs

    # Premiere passe : mesurer
    measure_result = run_ffmpeg([
        "-i", args.input,
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-"
    ], check=False)

    stderr = measure_result.stderr
    json_start = stderr.rfind("{")
    json_end = stderr.rfind("}") + 1

    if json_start >= 0 and json_end > json_start:
        measured = json.loads(stderr[json_start:json_end])
        measured_i = measured.get("input_i", "-24")
        measured_tp = measured.get("input_tp", "-2")
        measured_lra = measured.get("input_lra", "7")
        measured_thresh = measured.get("input_thresh", "-34")

        # Deuxieme passe : normaliser
        run_ffmpeg([
            "-i", args.input,
            "-af", (f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11:"
                    f"measured_I={measured_i}:measured_TP={measured_tp}:"
                    f"measured_LRA={measured_lra}:measured_thresh={measured_thresh}:"
                    f"linear=true"),
            "-ar", "44100", "-ac", "2",
            args.output
        ])
    else:
        # Fallback : normalisation simple
        run_ffmpeg([
            "-i", args.input,
            "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
            "-ar", "44100", "-ac", "2",
            args.output
        ])

    print(f"Normalise a {target_lufs} LUFS: {args.output}")


def cmd_concat(args):
    """Concatene plusieurs fichiers audio avec silence optionnel entre eux."""
    inputs = [f.strip() for f in args.inputs.split(",")]
    gap = args.gap

    if gap > 0:
        # Creer un silence
        silence_path = Path(args.output).parent / "_silence.wav"
        run_ffmpeg([
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
            "-t", str(gap), "-ar", "44100", "-ac", "2",
            str(silence_path)
        ])

        # Interleaver fichiers + silences
        interleaved = []
        for i, f in enumerate(inputs):
            interleaved.append(f)
            if i < len(inputs) - 1:
                interleaved.append(str(silence_path))

        # Creer fichier concat
        concat_file = Path(args.output).parent / "_concat_list.txt"
        with open(concat_file, "w") as cf:
            for f in interleaved:
                cf.write(f"file '{os.path.abspath(f)}'\n")

        run_ffmpeg([
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c", "copy", args.output
        ])

        silence_path.unlink(missing_ok=True)
        concat_file.unlink(missing_ok=True)
    else:
        concat_file = Path(args.output).parent / "_concat_list.txt"
        with open(concat_file, "w") as cf:
            for f in inputs:
                cf.write(f"file '{os.path.abspath(f)}'\n")

        run_ffmpeg([
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c", "copy", args.output
        ])
        concat_file.unlink(missing_ok=True)

    print(f"Concatene {len(inputs)} fichiers: {args.output}")


def cmd_mix(args):
    """Mixe plusieurs pistes audio avec volumes differents."""
    # Format: "file1.wav:100,file2.wav:15"
    tracks = []
    for track_spec in args.tracks.split(","):
        parts = track_spec.strip().rsplit(":", 1)
        if len(parts) == 2:
            tracks.append({"file": parts[0], "volume": int(parts[1])})
        else:
            tracks.append({"file": parts[0], "volume": 100})

    # Construire le filtre amix
    inputs = []
    filter_parts = []
    for i, t in enumerate(tracks):
        inputs.extend(["-i", t["file"]])
        vol = t["volume"] / 100.0
        filter_parts.append(f"[{i}]volume={vol}[a{i}]")

    mix_inputs = "".join(f"[a{i}]" for i in range(len(tracks)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(tracks)}:duration=longest[out]")

    filter_str = ";".join(filter_parts)

    run_ffmpeg(inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-ar", "44100", "-ac", "2",
        args.output
    ])

    print(f"Mixe {len(tracks)} pistes: {args.output}")


def cmd_fade(args):
    """Ajoute fade in et/ou fade out a un fichier audio."""
    filters = []

    if args.fade_in and args.fade_in > 0:
        filters.append(f"afade=t=in:ss=0:d={args.fade_in}")

    if args.fade_out and args.fade_out > 0:
        # Obtenir la duree totale
        probe = run_ffprobe([
            "-v", "quiet", "-print_format", "json", "-show_format", args.input
        ])
        duration = float(json.loads(probe.stdout)["format"]["duration"])
        fade_start = duration - args.fade_out
        filters.append(f"afade=t=out:st={fade_start}:d={args.fade_out}")

    if not filters:
        # Pas de fade, copier simplement
        run_ffmpeg(["-i", args.input, "-c", "copy", args.output])
    else:
        run_ffmpeg([
            "-i", args.input,
            "-af", ",".join(filters),
            args.output
        ])

    print(f"Fade applique: {args.output}")


def cmd_convert(args):
    """Convertit un fichier audio en un autre format."""
    extra = []
    if args.bitrate:
        extra.extend(["-b:a", args.bitrate])
    if args.sample_rate:
        extra.extend(["-ar", str(args.sample_rate)])

    run_ffmpeg(["-i", args.input] + extra + [args.output])
    print(f"Converti: {args.output}")


def cmd_trim(args):
    """Decoupe un fichier audio entre start et end."""
    extra = []
    if args.start:
        extra.extend(["-ss", str(args.start)])
    if args.end:
        extra.extend(["-to", str(args.end)])

    run_ffmpeg(["-i", args.input] + extra + ["-c", "copy", args.output])
    print(f"Decoupe: {args.output}")


def cmd_volume(args):
    """Ajuste le volume d'un fichier audio (gain en dB)."""
    run_ffmpeg([
        "-i", args.input,
        "-af", f"volume={args.gain}dB",
        args.output
    ])
    print(f"Volume ajuste ({args.gain}dB): {args.output}")


def main():
    parser = argparse.ArgumentParser(description="Audio Engine — traitement audio via ffmpeg")
    subparsers = parser.add_subparsers(dest="command")

    # info
    p = subparsers.add_parser("info", help="Informations fichier audio")
    p.add_argument("--input", required=True)

    # normalize
    p = subparsers.add_parser("normalize", help="Normaliser le volume")
    p.add_argument("--input", required=True)
    p.add_argument("--target-lufs", type=float, default=-16.0)
    p.add_argument("--output", required=True)

    # concat
    p = subparsers.add_parser("concat", help="Concatener des fichiers")
    p.add_argument("--inputs", required=True, help="Fichiers separes par virgules")
    p.add_argument("--gap", type=float, default=0.0, help="Silence entre fichiers (secondes)")
    p.add_argument("--output", required=True)

    # mix
    p = subparsers.add_parser("mix", help="Mixer des pistes")
    p.add_argument("--tracks", required=True, help="file:volume,file:volume (volume en %)")
    p.add_argument("--output", required=True)

    # fade
    p = subparsers.add_parser("fade", help="Ajouter fade in/out")
    p.add_argument("--input", required=True)
    p.add_argument("--fade-in", type=float, default=0.0)
    p.add_argument("--fade-out", type=float, default=0.0)
    p.add_argument("--output", required=True)

    # convert
    p = subparsers.add_parser("convert", help="Convertir format")
    p.add_argument("--input", required=True)
    p.add_argument("--format", default="mp3")
    p.add_argument("--bitrate", default="320k")
    p.add_argument("--sample-rate", type=int, default=None)
    p.add_argument("--output", required=True)

    # trim
    p = subparsers.add_parser("trim", help="Decouper")
    p.add_argument("--input", required=True)
    p.add_argument("--start", type=float, default=None)
    p.add_argument("--end", type=float, default=None)
    p.add_argument("--output", required=True)

    # volume
    p = subparsers.add_parser("volume", help="Ajuster le volume")
    p.add_argument("--input", required=True)
    p.add_argument("--gain", type=float, required=True, help="Gain en dB (ex: -3, +6)")
    p.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "info":
        cmd_info(args)
    elif args.command == "normalize":
        cmd_normalize(args)
    elif args.command == "concat":
        cmd_concat(args)
    elif args.command == "mix":
        cmd_mix(args)
    elif args.command == "fade":
        cmd_fade(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "trim":
        cmd_trim(args)
    elif args.command == "volume":
        cmd_volume(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
