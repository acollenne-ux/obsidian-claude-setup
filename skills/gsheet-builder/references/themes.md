# Themes Google Sheets — Palettes Consulting-Grade

Les couleurs sont au format Google Sheets API (RGB 0.0-1.0).

## 1. McKinsey Blue

```yaml
mckinsey_blue:
  name: "McKinsey Blue"
  primary:    { red: 0.0,   green: 0.169, blue: 0.361 }   # #002B5C
  accent:     { red: 0.0,   green: 0.494, blue: 0.898 }   # #007EE5
  header_bg:  { red: 0.839, green: 0.894, blue: 0.941 }   # #D6E4F0
  alt_row:    { red: 0.949, green: 0.969, blue: 0.984 }   # #F2F7FB
  positive:   { red: 0.114, green: 0.451, blue: 0.141 }   # #1D7324
  negative:   { red: 0.757, green: 0.071, blue: 0.122 }   # #C1121F
  tab_dashboard: { red: 0.0, green: 0.169, blue: 0.361 }
  tab_data:      { red: 0.0, green: 0.494, blue: 0.898 }
  tab_config:    { red: 0.5, green: 0.5,   blue: 0.5   }
  font: "Inter"
  font_fallback: "Arial"
```

## 2. Goldman Dark

```yaml
goldman_dark:
  name: "Goldman Dark"
  primary:    { red: 0.106, green: 0.165, blue: 0.290 }   # #1B2A4A
  accent:     { red: 0.773, green: 0.647, blue: 0.353 }   # #C5A55A
  header_bg:  { red: 0.910, green: 0.878, blue: 0.816 }   # #E8E0D0
  alt_row:    { red: 0.961, green: 0.953, blue: 0.937 }   # #F5F3EF
  positive:   { red: 0.180, green: 0.545, blue: 0.341 }   # #2E8B57
  negative:   { red: 0.698, green: 0.133, blue: 0.133 }   # #B22222
  tab_dashboard: { red: 0.106, green: 0.165, blue: 0.290 }
  tab_data:      { red: 0.773, green: 0.647, blue: 0.353 }
  tab_config:    { red: 0.5,   green: 0.5,   blue: 0.5   }
  font: "Inter"
  font_fallback: "Arial"
```

## 3. Dashboard Green

```yaml
dashboard_green:
  name: "Dashboard Green"
  primary:    { red: 0.059, green: 0.298, blue: 0.227 }   # #0F4C3A
  accent:     { red: 0.204, green: 0.827, blue: 0.600 }   # #34D399
  header_bg:  { red: 0.820, green: 0.980, blue: 0.898 }   # #D1FAE5
  alt_row:    { red: 0.941, green: 0.992, blue: 0.957 }   # #F0FDF4
  positive:   { red: 0.020, green: 0.588, blue: 0.412 }   # #059669
  negative:   { red: 0.863, green: 0.149, blue: 0.149 }   # #DC2626
  tab_dashboard: { red: 0.059, green: 0.298, blue: 0.227 }
  tab_data:      { red: 0.204, green: 0.827, blue: 0.600 }
  tab_config:    { red: 0.5,   green: 0.5,   blue: 0.5   }
  font: "Inter"
  font_fallback: "Arial"
```

## 4. Minimal Gray

```yaml
minimal_gray:
  name: "Minimal Gray"
  primary:    { red: 0.067, green: 0.067, blue: 0.067 }   # #111111
  accent:     { red: 0.420, green: 0.447, blue: 0.498 }   # #6B7280
  header_bg:  { red: 0.953, green: 0.957, blue: 0.965 }   # #F3F4F6
  alt_row:    { red: 0.976, green: 0.980, blue: 0.984 }   # #F9FAFB
  positive:   { red: 0.086, green: 0.639, blue: 0.290 }   # #16A34A
  negative:   { red: 0.937, green: 0.267, blue: 0.267 }   # #EF4444
  tab_dashboard: { red: 0.067, green: 0.067, blue: 0.067 }
  tab_data:      { red: 0.420, green: 0.447, blue: 0.498 }
  tab_config:    { red: 0.5,   green: 0.5,   blue: 0.5   }
  font: "Inter"
  font_fallback: "Arial"
```

## 5. Startup Orange

```yaml
startup_orange:
  name: "Startup Orange"
  primary:    { red: 0.486, green: 0.176, blue: 0.071 }   # #7C2D12
  accent:     { red: 0.976, green: 0.451, blue: 0.086 }   # #F97316
  header_bg:  { red: 1.0,   green: 0.969, blue: 0.929 }   # #FFF7ED
  alt_row:    { red: 1.0,   green: 0.984, blue: 0.961 }   # #FFFBF5
  positive:   { red: 0.133, green: 0.773, blue: 0.369 }   # #22C55E
  negative:   { red: 0.882, green: 0.114, blue: 0.282 }   # #E11D48
  tab_dashboard: { red: 0.486, green: 0.176, blue: 0.071 }
  tab_data:      { red: 0.976, green: 0.451, blue: 0.086 }
  tab_config:    { red: 0.5,   green: 0.5,   blue: 0.5   }
  font: "Inter"
  font_fallback: "Arial"
```

---

## Couleurs Conditionnelles (communes a tous les themes)

```yaml
conditional:
  positive_bg:   { red: 0.820, green: 0.980, blue: 0.898 }  # #D1FAE5
  positive_text: { red: 0.086, green: 0.392, blue: 0.204 }  # #166534
  amber_bg:      { red: 0.996, green: 0.953, blue: 0.780 }  # #FEF3C7
  amber_text:    { red: 0.573, green: 0.251, blue: 0.055 }  # #92400E
  negative_bg:   { red: 0.996, green: 0.886, blue: 0.886 }  # #FEE2E2
  negative_text: { red: 0.600, green: 0.106, blue: 0.106 }  # #991B1B
  border_light:  { red: 0.898, green: 0.906, blue: 0.922 }  # #E5E7EB
```

## Regles d'Application

1. **Max 6 couleurs** par spreadsheet (les 6 du theme choisi)
2. Les couleurs conditionnelles sont un **bonus autorise** (ne comptent pas dans les 6)
3. Font **Inter** partout, **Arial** en fallback si Inter non disponible
4. Header : 11pt bold | Body : 10pt regular | Title : 14pt bold | KPI value : 18pt bold
5. **JAMAIS** de couleur custom en dehors du theme
