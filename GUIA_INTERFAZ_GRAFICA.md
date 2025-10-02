# 🎯 GUÍA RÁPIDA - INTERFAZ GRÁFICA

## ✨ ¡Ahora es súper fácil procesar múltiples archivos JSON!

### 🚀 **CÓMO USAR LA INTERFAZ GRÁFICA:**

#### 1️⃣ **Ejecutar la interfaz:**
```bash
python ejecutar_gui.py
```

#### 2️⃣ **Pasos en la interfaz:**

1. **📂 Seleccionar Archivos:**
   - Haz clic en "📂 Seleccionar Archivos JSON"
   - Selecciona uno o más archivos `.json` de Slack
   - Puedes seleccionar múltiples manteniendo `Ctrl` presionado

2. **📄 Configurar nombre de salida:**
   - Cambia el nombre del archivo Excel si quieres
   - Por defecto: `commits_consolidados.xlsx`

3. **🚀 Procesar:**
   - Haz clic en "🚀 Procesar Archivos"
   - Espera a que termine (verás una barra de progreso)

4. **✅ ¡Listo!**
   - Se generará un archivo Excel con todos los commits consolidados
   - Verás un resumen con estadísticas

---

## 📊 **VENTAJAS DE LA INTERFAZ GRÁFICA:**

✅ **Selección múltiple** - Procesa varios JSON a la vez
✅ **Interfaz amigable** - No necesitas escribir comandos
✅ **Progreso visual** - Sabes qué está pasando
✅ **Reporte consolidado** - Un solo Excel con todo
✅ **Estadísticas por archivo** - Sabes qué vino de dónde

---

## 🔄 **COMPARACIÓN DE MÉTODOS:**

### 🎯 **Interfaz Gráfica** (RECOMENDADA)
```bash
python ejecutar_gui.py
```
- ✅ Múltiples archivos
- ✅ Interfaz visual
- ✅ Fácil de usar
- ✅ Reporte consolidado

### 📝 **Script Simple** (Un archivo)
```bash
python ejecutar_extractor.py
```
- ✅ Rápido para un archivo
- ❌ Solo un archivo a la vez

### 🔧 **Script Avanzado** (Personalizable)
```bash
python slack_github_extractor.py archivo.json -o salida.xlsx
```
- ✅ Control total
- ❌ Requiere comandos

---

## 🎉 **¡PRUÉBALO AHORA!**

1. Ejecuta: `python ejecutar_gui.py`
2. Selecciona tus archivos JSON
3. ¡Obtén tu reporte consolidado!

---

*🚀 La interfaz gráfica hace todo más fácil y rápido*