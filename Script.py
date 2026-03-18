import streamlit as st
from openai import OpenAI

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Scriptoria AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0a0a, #2d1515, #1a0d24);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03);
    border-right: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
}

.script-header {
    background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(168,85,247,0.18));
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

.script-header h1 {
    background: linear-gradient(90deg, #f87171, #c084fc, #fb923c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
}

.script-header p {
    color: rgba(255,255,255,0.6);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.result-box {
    background: rgba(26,10,10,0.95);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #e2e8f0;
    line-height: 1.85;
    white-space: pre-wrap;
    font-size: 0.94rem;
    font-family: 'Courier New', monospace;
}

.result-box-prose {
    background: rgba(26,10,10,0.95);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #e2e8f0;
    line-height: 1.85;
    white-space: pre-wrap;
    font-size: 0.94rem;
}

.section-title {
    color: #f87171;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    border-left: 4px solid #f87171;
    padding-left: 0.75rem;
}

.stButton > button {
    background: linear-gradient(135deg, #dc2626, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #b91c1c, #6d28d9) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(220,38,38,0.4) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

label, .stMarkdown p { color: rgba(255,255,255,0.82) !important; }

.metric-badge {
    display: inline-block;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    color: #f87171;
    font-weight: 600;
    margin: 0.2rem;
}

div[data-testid="stTabs"] button { color: rgba(255,255,255,0.55) !important; font-weight: 600 !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #f87171 !important; border-bottom-color: #f87171 !important; }
</style>
""", unsafe_allow_html=True)

# ── Model & Client ────────────────────────────────────────────────────────────
MODEL = "openai/gpt-4o"  # openai/gpt-oss-120b via OpenRouter

def call_ai(prompt: str, system: str = "You are Scriptoria, an expert AI screenwriter and film pre-production specialist.") -> str:
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return "⚠️ Please enter your OpenRouter API key in the sidebar."
    try:
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0.85,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="color:#f87171;font-size:1.1rem;font-weight:700;margin-bottom:1rem;">⚙️ Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-...")
    if api_key:
        st.session_state["api_key"] = api_key

    st.markdown("---")
    st.markdown("""
    <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>
    <b style='color:#f87171'>Model:</b> openai/gpt-oss-120b<br><br>
    <b style='color:#f87171'>Features:</b><br>
    📝 Screenplay Generation<br>
    👤 Character Development<br>
    🎵 Sound Design Planning<br>
    📦 Production Planning<br>
    🎨 Creative Workflow<br>
    💬 Film AI Assistant
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span class="metric-badge">GPT-OSS-120B</span><span class="metric-badge">OpenRouter</span>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="script-header">
    <h1>🎬 Scriptoria AI</h1>
    <p>Generative AI–Powered Film Pre-Production System</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📝 Screenplay", "👤 Characters", "🎵 Sound Design", "📦 Production Plan", "🎨 Creative Workflow", "💬 Film Assistant"])

# ── Tab 1: Screenplay Generation ─────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">📝 AI Screenplay Generator</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        logline = st.text_area("Your Idea / Logline", placeholder="e.g. A disgraced detective in 2049 Mumbai discovers an AI that can predict crimes before they happen...", height=100)
        genre = st.selectbox("Genre", ["Thriller / Noir", "Drama", "Sci-Fi", "Action / Adventure", "Comedy", "Horror", "Romance", "Fantasy", "Historical / Period", "Documentary", "Animation"])
        tone = st.selectbox("Tone", ["Dark & Gritty", "Light & Comedic", "Epic & Grandiose", "Intimate & Character-driven", "Satirical", "Surreal / Experimental"])
    with col2:
        format_type = st.selectbox("Format", ["Feature Film (90-120 min)", "Short Film (10-30 min)", "Web Series (Episode)", "TV Pilot", "Mini-Series (3-6 eps)"])
        setting = st.text_input("Setting / World", placeholder="e.g. Near-future Mumbai, 1940s Paris, Post-apocalyptic Earth")
        theme = st.text_input("Central Theme", placeholder="e.g. Redemption, Love vs Duty, Technology & Humanity")

    num_acts = st.selectbox("Story Structure", ["3-Act Structure", "4-Act Structure", "Hero's Journey", "Non-Linear / Fragmented", "Kishōtenketsu (Japanese)"])

    if st.button("📝 Generate Screenplay", key="screenplay"):
        with st.spinner("Writing your screenplay..."):
            prompt = f"""Write a professional screenplay excerpt for:

LOGLINE / IDEA: {logline}
GENRE: {genre}
TONE: {tone}
FORMAT: {format_type}
SETTING: {setting}
CENTRAL THEME: {theme}
STRUCTURE: {num_acts}

Generate:
1. TITLE PAGE (Title, Written by, Format)
2. LOGLINE (one sentence)
3. SYNOPSIS (3 paragraphs — setup, confrontation, resolution)
4. STORY OUTLINE ({num_acts} breakdown with key beats)
5. OPENING SCENE — Full screenplay format (3-5 pages):
   - Scene headings (INT./EXT.)
   - Action lines
   - Dialogue with parentheticals
   - Scene transitions
6. KEY PLOT POINTS summary
7. CLIMAX scene outline

Write in proper Hollywood screenplay format (Courier, sluglines, action blocks, centered dialogue)."""
            result = call_ai(prompt, system="You are a WGA-level screenwriter and story architect. Write in proper screenplay format with compelling dialogue and vivid action lines.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 2: Character Development ─────────────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">👤 AI Character Development Studio</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        char_film = st.text_input("Film / Story Title", placeholder="e.g. Neon Shadows")
        char_genre = st.selectbox("Film Genre", ["Thriller", "Drama", "Sci-Fi", "Action", "Comedy", "Horror", "Romance", "Fantasy"])
        num_chars = st.number_input("Number of Characters to Develop", min_value=1, max_value=10, value=3)
    with col2:
        char_roles = st.text_area("Character Roles / Archetypes", placeholder="e.g. Protagonist: brooding detective, Antagonist: corporate AI CEO, Sidekick: street-smart hacker", height=100)
        char_setting = st.text_input("Story World / Setting", placeholder="e.g. 2049 Mumbai")

    if st.button("👤 Develop Characters", key="characters"):
        with st.spinner("Building rich character profiles..."):
            prompt = f"""Create comprehensive character profiles for a {char_genre} film titled "{char_film}" set in {char_setting if char_setting else 'a compelling fictional world'}.

Number of Characters: {num_chars}
Character Roles: {char_roles if char_roles else 'Protagonist, Antagonist, Supporting character'}

For EACH character provide:
1. FULL NAME & ALIAS
2. VITAL STATS (Age, Appearance, Nationality)
3. BACKSTORY (500 words — formative experiences, trauma, motivation origin)
4. PERSONALITY PROFILE
   - Core traits (5-7 descriptors)
   - Myers-Briggs type
   - Greatest strength & fatal flaw
   - Internal conflict
   - External goal vs Internal need
5. CHARACTER ARC (beginning → transformation → end state)
6. RELATIONSHIPS with other characters
7. SIGNATURE DIALOGUE SAMPLES (3-5 lines that capture their voice)
8. PHYSICALITY & MANNERISMS
9. WARDROBE / VISUAL IDENTITY
10. ACTOR INSPIRATION (real actors who could play this role)

Make each character feel vivid, complex, and three-dimensional."""
            result = call_ai(prompt, system="You are a master storyteller and character architect. Create psychologically rich, memorable film characters with depth and authenticity.")
        st.markdown(f'<div class="result-box result-box-prose">{result}</div>', unsafe_allow_html=True)

# ── Tab 3: Sound Design Planning ─────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">🎵 AI Sound Design Planner</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        sd_film = st.text_input("Film Title", placeholder="e.g. Neon Shadows")
        sd_genre = st.selectbox("Genre", ["Thriller / Noir", "Sci-Fi", "Drama", "Action", "Horror", "Comedy", "Fantasy", "Period / Historical"])
        sd_mood = st.text_input("Overall Mood / Feel", placeholder="e.g. tense, atmospheric, melancholic, euphoric")
    with col2:
        sd_setting = st.text_input("Key Settings / Locations", placeholder="e.g. futuristic city, dense forest, 1940s nightclub")
        sd_influences = st.text_input("Musical/Sound References", placeholder="e.g. Blade Runner, Interstellar, The Dark Knight")
        sd_budget = st.selectbox("Production Budget Level", ["Micro / Indie (<$100K)", "Low ($100K–$1M)", "Mid ($1M–$10M)", "High ($10M–$50M)", "Studio ($50M+)"])

    sd_scenes = st.text_area("Key Scenes to Design Sound For", placeholder="Describe 3-5 key scenes you need sound design for...", height=100)

    if st.button("🎵 Generate Sound Design Plan", key="sound"):
        with st.spinner("Composing your sound design blueprint..."):
            prompt = f"""Create a comprehensive sound design plan for film: "{sd_film}"

Genre: {sd_genre}
Mood: {sd_mood}
Key Settings: {sd_setting}
Audio References: {sd_influences if sd_influences else 'Original / not specified'}
Budget Level: {sd_budget}
Key Scenes:
{sd_scenes if sd_scenes else 'General film sound design'}

Generate a professional sound design document including:
1. SONIC IDENTITY STATEMENT (the film's overall sound philosophy)
2. SCORE / MUSIC PLAN
   - Instrumentation palette
   - Key musical themes (leitmotifs per character/concept)
   - Genre influences and fusion
   - Silence as a storytelling tool
3. SOUND EFFECTS STRATEGY
   - Ambient/environment sounds per location
   - Signature sound effects (unique to this film's world)
   - Practical vs designed sounds
4. DIALOGUE & VOICE DESIGN
   - ADR requirements
   - Voice processing (if futuristic/supernatural)
5. SCENE-BY-SCENE SOUND BREAKDOWN (for provided key scenes)
6. EQUIPMENT & RECORDING NEEDS
7. POST-PRODUCTION AUDIO PIPELINE
8. BUDGET ALLOCATION RECOMMENDATIONS
9. REFERENCE TRACKS / TEMP SCORE SUGGESTIONS

Format as a professional sound design brief."""
            result = call_ai(prompt, system="You are an award-winning film sound designer and music supervisor with experience across major Hollywood and indie productions.")
        st.markdown(f'<div class="result-box result-box-prose">{result}</div>', unsafe_allow_html=True)

# ── Tab 4: Production Plan ────────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">📦 Pre-Production Planner</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        pp_title = st.text_input("Film / Project Title", placeholder="e.g. Neon Shadows")
        pp_format = st.selectbox("Format", ["Feature Film", "Short Film", "Web Series", "Documentary", "Music Video", "Commercial"])
        pp_duration = st.text_input("Estimated Runtime", placeholder="e.g. 95 minutes, 12 minutes")
    with col2:
        pp_budget = st.text_input("Total Production Budget", placeholder="e.g. ₹50 Lakhs, $200,000")
        pp_crew = st.number_input("Core Crew Size", min_value=2, max_value=500, value=20)
        pp_shoot_days = st.number_input("Estimated Shoot Days", min_value=1, max_value=365, value=25)

    pp_synopsis = st.text_area("Brief Synopsis", placeholder="2-3 lines about your film...", height=80)

    if st.button("📦 Generate Production Plan", key="prodplan"):
        with st.spinner("Building your pre-production blueprint..."):
            prompt = f"""Create a comprehensive pre-production plan for:

Title: {pp_title}
Format: {pp_format}
Runtime: {pp_duration}
Budget: {pp_budget}
Core Crew: {pp_crew}
Shoot Days: {pp_shoot_days}
Synopsis: {pp_synopsis if pp_synopsis else 'No synopsis provided'}

Generate a full pre-production document:
1. PRE-PRODUCTION TIMELINE (week-by-week schedule)
2. DEPARTMENT BREAKDOWN
   - Direction team
   - Camera / DOP department
   - Art / Production Design
   - Costume & Makeup
   - Sound department
   - Production Management
3. LOCATION SCOUTING PLAN
4. CASTING STRATEGY
   - Principal cast requirements
   - Audition schedule
   - Casting director recommendation
5. SHOT LIST APPROACH (types of shots, style notes)
6. STORYBOARD PRIORITIES (key sequences to board)
7. EQUIPMENT LIST (cameras, lenses, lighting, sound gear)
8. BUDGET ALLOCATION (by department, % split)
9. PERMITS & LEGAL REQUIREMENTS
10. RISK MANAGEMENT & CONTINGENCY PLANS
11. CREW CALL SHEET TEMPLATE
12. DAY-OUT-OF-DAYS (rough schedule summary)

Make it production-ready."""
            result = call_ai(prompt, system="You are a seasoned film producer and production manager with experience across feature films, indie projects, and commercial productions.")
        st.markdown(f'<div class="result-box result-box-prose">{result}</div>', unsafe_allow_html=True)

# ── Tab 5: Creative Workflow Automation ──────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">🎨 Creative Workflow Automation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        cw_idea = st.text_area("Raw Idea / Concept", placeholder="Describe your film idea, even if rough...", height=120)
        cw_stage = st.selectbox("Current Development Stage", ["Just an idea", "Concept Stage", "Treatment Written", "Script Draft 1", "Script Polish", "Pre-Production"])
    with col2:
        cw_challenges = st.text_area("Creative Challenges / Blocks", placeholder="What are you stuck on? What needs development?", height=120)
        cw_deadline = st.text_input("Target Deadline", placeholder="e.g. Film festival submission: March 2026")

    if st.button("🎨 Automate Creative Workflow", key="workflow"):
        with st.spinner("Generating your creative workflow..."):
            prompt = f"""Help automate and structure the creative workflow for a filmmaker:

Raw Idea: {cw_idea}
Current Stage: {cw_stage}
Creative Challenges: {cw_challenges if cw_challenges else 'None specified'}
Target Deadline: {cw_deadline if cw_deadline else 'Not specified'}

Provide:
1. IDEA DEVELOPMENT ROADMAP
   - From concept to shooting script (phase-by-phase)
2. IMMEDIATE NEXT STEPS (this week's action items)
3. TREATMENT OUTLINE (2-page summary structure)
4. STORY DEVELOPMENT EXERCISES
   - Character questionnaires
   - World-building prompts
   - Scene ideation exercises
5. WRITER'S ROOM WORKFLOW (if team)
6. REVISION STRATEGY (for each draft pass — story, character, dialogue, polish)
7. FEEDBACK LOOP PLAN (table reads, screenplay consultants, test screenings)
8. PITCH MATERIALS TO PREPARE (logline, synopsis, deck, sizzle reel)
9. FESTIVAL & DISTRIBUTION STRATEGY roadmap
10. TOOLS & SOFTWARE RECOMMENDATIONS
    (Final Draft, Celtx, StudioBinder, Notion for writers, etc.)
11. CREATIVE BLOCK BUSTERS (specific exercises for challenges mentioned)

Make it a motivating, actionable creative roadmap."""
            result = call_ai(prompt, system="You are a creative development executive, script consultant, and filmmaker's coach. Help artists bring their visions to life through structured creative workflows.")
        st.markdown(f'<div class="result-box result-box-prose">{result}</div>', unsafe_allow_html=True)

# ── Tab 6: Film AI Assistant ──────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">💬 Scriptoria Film Assistant</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:0.9rem;">Ask anything about screenwriting, directing, film theory, production, festivals, or storytelling.</p>', unsafe_allow_html=True)

    if "film_chat" not in st.session_state:
        st.session_state.film_chat = []

    for msg in st.session_state.film_chat:
        if msg["role"] == "user":
            st.markdown(f"""<div style="background:rgba(220,38,38,0.15);border:1px solid rgba(220,38,38,0.3);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
            <b style="color:#f87171">You:</b> {msg['content']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
            <b style="color:#c084fc">Scriptoria AI:</b> {msg['content']}</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask Scriptoria...", placeholder="e.g. How do I write a compelling villain? What's the three-act structure?", key="film_input", label_visibility="collapsed")
    with col2:
        send = st.button("Send →", key="film_send")

    if send and user_input:
        st.session_state.film_chat.append({"role": "user", "content": user_input})
        history_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.film_chat[-6:]])
        with st.spinner("Thinking..."):
            response = call_ai(history_prompt, system="You are Scriptoria, a world-class AI film consultant combining the storytelling genius of screenwriters like Aaron Sorkin and Christopher Nolan with production expertise. Answer questions about screenwriting, directing, cinematography, film theory, festivals, pitching, and the craft of filmmaking.")
        st.session_state.film_chat.append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="film_clear"):
        st.session_state.film_chat = []
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.3); font-size:0.8rem; padding:1rem 0;">
    🎬 Scriptoria AI — Powered by <b style="color:#f87171">openai/gpt-oss-120b</b> via OpenRouter &nbsp;|&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
