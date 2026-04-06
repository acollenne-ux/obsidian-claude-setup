"""
chart_generator.py — Génère des graphiques professionnels pour les PDFs.
Usage : python chart_generator.py <type> <json_data> <titre> <output_path>

Types : line, bar, area, multi_line, scatter, hbar, combo
"""
import sys, json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from datetime import datetime

COLORS = ['#1a3a6b', '#2196F3', '#4CAF50', '#FF5722', '#9C27B0',
          '#FF9800', '#00BCD4', '#795548', '#607D8B', '#E91E63']
BG = '#FAFAFA'
GRID = '#E0E0E0'

def style_ax(ax, title, xlabel='', ylabel=''):
    ax.set_facecolor(BG)
    ax.set_title(title, fontsize=13, fontweight='bold', color='#1a3a6b', pad=12)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9, color='#555')
    if ylabel: ax.set_ylabel(ylabel, fontsize=9, color='#555')
    ax.grid(True, color=GRID, linewidth=0.7, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#555', labelsize=8)


def line_chart(data, title, output):
    """data = {"labels": [...], "values": [...], "ylabel": "..."}"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG)
    labels = data.get('labels', [])
    values = data.get('values', [])
    ax.plot(labels, values, color=COLORS[0], linewidth=2.5, marker='o',
            markersize=5, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(labels)), values, alpha=0.08, color=COLORS[0])
    style_ax(ax, title, ylabel=data.get('ylabel', ''))
    plt.xticks(range(len(labels)), labels, rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


def multi_line_chart(data, title, output):
    """data = {"labels": [...], "series": [{"name": "...", "values": [...]}], "ylabel": "..."}"""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(BG)
    labels = data.get('labels', [])
    for i, serie in enumerate(data.get('series', [])):
        vals = serie['values']
        ax.plot(range(len(labels)), vals, color=COLORS[i % len(COLORS)],
                linewidth=2.2, marker='o', markersize=4,
                label=serie.get('name', f'Serie {i+1}'))
    style_ax(ax, title, ylabel=data.get('ylabel', ''))
    plt.xticks(range(len(labels)), labels, rotation=30, ha='right')
    ax.legend(fontsize=8, loc='best', framealpha=0.8)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


def bar_chart(data, title, output):
    """data = {"labels": [...], "values": [...], "ylabel": "...", "colors": [...optional]}"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(BG)
    labels = data.get('labels', [])
    values = data.get('values', [])
    colors_list = data.get('colors', None)
    if colors_list is None:
        colors_list = [COLORS[2] if v >= 0 else COLORS[3] for v in values]
    bars = ax.bar(range(len(labels)), values, color=colors_list, width=0.6,
                  edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                f'{val:,.1f}', ha='center', va='bottom', fontsize=7.5, color='#333')
    style_ax(ax, title, ylabel=data.get('ylabel', ''))
    plt.xticks(range(len(labels)), labels, rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


def area_chart(data, title, output):
    """data = {"labels": [...], "series": [{"name":"...", "values":[...]}], "ylabel":"..."}"""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor(BG)
    labels = data.get('labels', [])
    x = range(len(labels))
    for i, serie in enumerate(data.get('series', [])):
        vals = serie['values']
        ax.fill_between(x, vals, alpha=0.25, color=COLORS[i % len(COLORS)])
        ax.plot(x, vals, color=COLORS[i % len(COLORS)], linewidth=2,
                label=serie.get('name', f'Serie {i+1}'))
    style_ax(ax, title, ylabel=data.get('ylabel', ''))
    plt.xticks(x, labels, rotation=30, ha='right')
    ax.legend(fontsize=8, loc='best', framealpha=0.8)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


def hbar_chart(data, title, output):
    """data = {"labels": [...], "values": [...], "ylabel": "..."}"""
    fig, ax = plt.subplots(figsize=(10, max(4, len(data.get('labels', []))*0.5)))
    fig.patch.set_facecolor(BG)
    labels = data.get('labels', [])
    values = data.get('values', [])
    y = range(len(labels))
    colors_list = [COLORS[2] if v >= 0 else COLORS[3] for v in values]
    bars = ax.barh(y, values, color=colors_list, edgecolor='white', height=0.6)
    for bar, val in zip(bars, values):
        ax.text(val + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                f'{val:,.1f}', va='center', fontsize=7.5, color='#333')
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    style_ax(ax, title, xlabel=data.get('ylabel', ''))
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


def scatter_chart(data, title, output):
    """data = {"points": [{"x":..., "y":..., "label":"..."}], "xlabel":"...", "ylabel":"..."}"""
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(BG)
    points = data.get('points', [])
    xs = [p['x'] for p in points]
    ys = [p['y'] for p in points]
    ax.scatter(xs, ys, color=COLORS[0], s=80, zorder=3, alpha=0.8)
    for p in points:
        ax.annotate(p.get('label', ''), (p['x'], p['y']),
                    textcoords='offset points', xytext=(5, 5), fontsize=7.5, color='#333')
    style_ax(ax, title, data.get('xlabel', ''), data.get('ylabel', ''))
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()


CHART_TYPES = {
    'line': line_chart,
    'multi_line': multi_line_chart,
    'bar': bar_chart,
    'area': area_chart,
    'hbar': hbar_chart,
    'scatter': scatter_chart,
}


def main():
    if len(sys.argv) < 5:
        print("Usage: python chart_generator.py <type> <json_data_or_file> <titre> <output.png>")
        print(f"Types disponibles : {', '.join(CHART_TYPES.keys())}")
        sys.exit(1)

    chart_type = sys.argv[1].lower()
    json_input = sys.argv[2]
    title = sys.argv[3]
    output = sys.argv[4]

    # Accepte un fichier JSON ou du JSON inline
    if os.path.exists(json_input):
        with open(json_input) as f:
            data = json.load(f)
    else:
        data = json.loads(json_input)

    if chart_type not in CHART_TYPES:
        print(f"Type inconnu : {chart_type}. Disponibles : {', '.join(CHART_TYPES.keys())}")
        sys.exit(1)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    CHART_TYPES[chart_type](data, title, output)
    print(f"Graphique genere : {output}")


if __name__ == "__main__":
    main()
