import streamlit as st
from clarifyrec.strategies import STRATEGIES

st.set_page_config(page_title="ClarifyRec", page_icon="🎬", layout="wide")
st.title("🎬 ClarifyRec")
st.caption("An uncertainty-aware conversational movie recommender — local prototype")
st.info("Prototype scope: transparent rule-based local language processing over a small illustrative movie catalogue. No external API or user data transmission.")

if "strategy_name" not in st.session_state: st.session_state.strategy_name = "ClarifyRec"
if "engine" not in st.session_state: st.session_state.engine = STRATEGIES[st.session_state.strategy_name]()
if "messages" not in st.session_state: st.session_state.messages = [{"role":"assistant", "content":"Tell me what kind of film you would like. You can also correct my recommendations in natural language."}]

with st.sidebar:
    st.header("Experiment settings")
    selected = st.selectbox("Preference-update strategy", list(STRATEGIES), index=list(STRATEGIES).index(st.session_state.strategy_name))
    if selected != st.session_state.strategy_name:
        st.session_state.strategy_name = selected; st.session_state.engine = STRATEGIES[selected]()
        st.session_state.messages = [{"role":"assistant", "content":"Strategy changed. Start a new conversation with your preferences."}]
    st.caption("Use the same conversation scenarios with each strategy for a fair comparison.")
    if st.button("Reset conversation", use_container_width=True):
        st.session_state.engine = STRATEGIES[st.session_state.strategy_name]()
        st.session_state.messages = [{"role":"assistant", "content":"Conversation reset. What would you like to watch?"}]
        st.rerun()
    st.divider(); st.subheader("Current preference profile")
    st.json(st.session_state.engine.profile.to_dict())

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

prompt = st.chat_input("E.g. I like romance, but nothing too heavy…")
if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt})
    result = st.session_state.engine.process(prompt)
    response = result["message"]
    if result["recommendations"]:
        response += "\n\n**Recommendations**\n"
        for i, movie in enumerate(result["recommendations"], 1):
            response += f"\n{i}. **{movie['title']} ({movie['year']})** — {movie['description']}  \n   *Match score: {movie['score']}*"
    st.session_state.messages.append({"role":"assistant", "content":response})
    st.rerun()

st.divider()
st.markdown("**Try these scenarios**")
cols = st.columns(3)
examples = ["I like romance, but nothing too heavy.", "Actually, I want something serious rather than comedy.", "I don't want a tragic ending."]
for col, example in zip(cols, examples):
    with col:
        if st.button(example, use_container_width=True):
            st.session_state.messages.append({"role":"user", "content":example})
            result = st.session_state.engine.process(example)
            response = result["message"]
            if result["recommendations"]:
                response += "\n\n**Recommendations**\n" + "\n".join(f"- **{m['title']} ({m['year']})** — {m['description']}" for m in result["recommendations"])
            st.session_state.messages.append({"role":"assistant", "content":response})
            st.rerun()
