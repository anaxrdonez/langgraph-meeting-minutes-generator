from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
import os
from tkinter import Tk, filedialog
import openai


# Configuración
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Definición del Estado
class State(TypedDict):
    notes: str                  # Texto original
    participants: List[str]     # Participantes
    topics: List[str]           # Temas principales
    action_items: List[str]     # Acciones y responsables
    minutes: str                # Minuta formal (acta reunión)
    summary: str                # Resumen ejecutivo


# ============= NODOS DEL WORKFLOW (GRAFO) =============
def participants_extractor(state: State) -> State:
    """ Extrae los participantes de la reunión. """
    prompt = f"""
    Analiza las siguientes notas de reunión y extrae únicamente los nombres de
    los participantes.

    Notas: {state['notes']}

    Instrucciones:
    - Responde SOLO con nombres separados por comas.
    - No incluyas explicaciones adicionales.
    - Formato: Juan García, María Lópes, Carlos Rúiz.
    """
    response = llm.invoke(prompt)
    participants = [p.strip() for p in response.content.split(',') if p.strip()]

    return {'participants': participants}


def topics_analyzer(state: State) -> State:
    """Identifica los temas pincipales discutidos."""
    prompt = f"""
    Identifica los 3-5 temas principales discutidos en esta reunión.

    Notas: {state['notes']}

    Responde SOLO con los temas separados por punto y coma (;).
    Ejemplo: Arquitecturas del sistma; Plazos de entrefa; Asignación de tareas
    """

    response = llm.invoke(prompt)
    topics = [t.strip() for t in response.content.split(';') if t.strip()]

    print(f"Temas identificados: {len(topics)} temas.")

    return {'topics': topics}


def actions_extractor(state: State) -> State:
    """Extrae las acciones acordadas y sus responsables"""
    prompt = f"""
    Extrae las acciones específicas acordadas en la reunión, incluyendo el responsable si se menciona.

    Notas: {state['notes']}

    Formato de respuesta: Una acción por línea, separadas por |
    Ejemplo: María se encargará del backend | Carlos preparará el plan de testing 

    Si no hay aciones claras, responde con: "No se identificaron acciones específicas."
    """
    response = llm.invoke(prompt)

    if "No se identificaron" in response.content:
        action_items = []
    else: 
        action_items = [a.strip() for a in response.content.split('|') if a.strip()]

    print(f"Acciones extraídas: {len(action_items)} items.")

    return {'action_items': action_items}


def min_generator(state: State) -> State:
    """Genera una minuta formal de la reunión"""
    participants_str = ", ".join(state['participants'])
    topics_str ="\n ".join(state['topics'])
    actions_str="\n ".join(state['action_items']) if state['action_items'] else "No se definieron acciones."

    prompt = f"""
    Genera una minuta formal y profesonal basándote en la siguiente información:

    PARTICIPANTES: {participants_str}

    TEMAS DISCUITIDOS: {topics_str}

    ACCIONES ACORDADADAS: {actions_str}

    NOTAS ORIGINALES: {state['notes']}

    Genera una minuta profesional de máximo 150 palabras que incluya:
    1. Encabezado con tipo de reunión.
    2. Lista de asistentes.
    3. Puntos principales discutidos.
    4. Acuerdos y próximos pasos.

    Usa un tono formal y structira clara.s
    """

    response = llm.invoke(prompt)

    print(f"Minuta generada: {len(response.content.split())} palabras.")

    return {'minutes': response.content}


def summary_generator(state: State) -> State:
    """Crea un resumen ejecutivo ultra-breve."""
    prompt = f"""
    Crea un resumen ejecutivo de MÁXIMO 2 líneas (30 palabras) que capture la esencia de esta reunión.
    
    Participantes: {', '.join(state['participants'][:3])}{'...' if len(state['participants']) > 3 else ''}
    Tema principal: {state['topics'][0] if state['topics'] else 'General'}
    Acciones clave: {len(state['action_items'])} acciones definidas
    
    El resumen debe ser conciso y directo al punto.
    """
    
    response = llm.invoke(prompt)
    
    print(f"✓ Resumen creado")
    
    return {'summary': response.content}


# ============= CONSTRUCCIÓN DEL GRAFO =============

def create_workflow():
    """Crea y configura el workflow de LangGraph"""
    
    # Crear el grafo
    graph = StateGraph(State)

    # Agregar todos los nodos
    graph.add_node("Participants", participants_extractor)
    graph.add_node("Topics", topics_analyzer)
    graph.add_node("Actions", actions_extractor)
    graph.add_node("Min", min_generator)
    graph.add_node("Summary", summary_generator)

    # Flujo de procesamiento
    # START → extract_participants → identify_topics → extract_actions 
    # → generate_minutes → create_summary → END
    graph.add_edge(START, "Participants")
    graph.add_edge("Participants", "Topics")
    graph.add_edge("Topics", "Actions")
    graph.add_edge("Actions", "Min")
    graph.add_edge("Min", "Summary")
    graph.add_edge("Summary", END)

    return graph.compile()


# ============= FUNCIONES DE PROCESAMIENTO =============

def transcribe_media_direct(file_path: str) -> str:
    """Transcribe usando directamente la API de OpenAI Whisper."""
    try:
        print("🎙️ Transcribiendo con OpenAI Whisper API directa...")
        
        client = openai.OpenAI()  # Usa OPENAI_API_KEY del entorno
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es",  # Español
                prompt="Esta es una reunión de trabajo en español con múltiples participantes.",
                response_format="text"
            )
        
        print(f"✓ Transcripción completada: {len(transcript)} caracteres")
        return transcript
        
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        return f"Error: {str(e)}"

def process_meeting_notes(notes: str, app):
    """Procesa una nota de reunión individual."""
    initial_state = {
        'notes': notes,
        'participants': [],
        'topics': [],
        'action_items': [],
        'minutes': '',
        'summary': ''
    }
    
    print("\n" + "="*60)
    print("🔄 Procesando nota de reunión...")
    print("="*60)
    
    result = app.invoke(initial_state)
    return result

def display_results(result: State, meeting_num: int):
    """Muestra los resultados de forma estructurada."""
    print(f"\n📋 RESULTADOS - REUNIÓN #{meeting_num}")
    print("-"*60)
    
    print(f"\n👥 Participantes ({len(result['participants'])}):")
    for p in result['participants']:
        print(f"   • {p}")
    
    print(f"\n📍 Temas tratados ({len(result['topics'])}):")
    for t in result['topics']:
        print(f"   • {t}")
    
    print(f"\n✅ Acciones acordadas ({len(result['action_items'])}):")
    if result['action_items']:
        for a in result['action_items']:
            print(f"   • {a}")
    else:
        print("   • No se definieron acciones específicas")
    
    print(f"\n📄 MINUTA FORMAL:")
    print("-"*40)
    print(result['minutes'])
    print("-"*40)
    
    print(f"\n💡 RESUMEN EJECUTIVO:")
    print(f"   {result['summary']}")
    
    print("\n" + "="*60)

# ============= DEMOSTRACIÓN =============

if __name__ == "__main__":
    app = create_workflow()

    # Pequeña interfaz gráfica: selector de archivo
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Selecciona un vídeo o transcripción",
        filetypes=[
            ("Vídeo/Audio", "*.mp4 *.mov *.m4a *.mp3 *.wav *.mkv *.webm"),
            ("Texto", "*.txt *.md")
        ]
    )

    if not file_path:
        print("No se seleccionó archivo.")
        raise SystemExit(0)

    ext = os.path.splitext(file_path)[1].lower()
    media_exts = {".mp4", ".mov", ".m4a", ".mp3", ".wav", ".mkv", ".webm"}

    if ext in media_exts:
        notes = transcribe_media_direct(file_path) 
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            notes = f.read()

    result = process_meeting_notes(notes, app)
    display_results(result, 1)