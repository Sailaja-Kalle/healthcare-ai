import streamlit as st
from database.history import get_user_history, delete_user_history, get_history_stats

def render_history_tab():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.info("👤 You are browsing as Guest. Login to save and view history.")
        return

    st.subheader("📜 Your History")

    stats = get_history_stats(user_id)
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💬 AI Chats", stats.get("ai_chat", 0))
        with col2:
            st.metric("📚 RAG Searches", stats.get("rag_search", 0))
        with col3:
            st.metric("🏥 Hospital Searches", stats.get("hospital_search", 0))
        with col4:
            st.metric("💰 Cost Estimates", stats.get("cost_estimate", 0))
        st.markdown("---")

    filter_type = st.selectbox(
        "Filter by type",
        ["All", "AI Chat", "RAG Search", "Hospital Search", "Cost Estimate"],
        key="history_filter"
    )

    type_map = {
        "All": None,
        "AI Chat": "ai_chat",
        "RAG Search": "rag_search",
        "Hospital Search": "hospital_search",
        "Cost Estimate": "cost_estimate"
    }

    selected_type = type_map[filter_type]
    history = get_user_history(user_id, tab_type=selected_type, limit=50)

    if history:
        if st.button("🗑️ Clear All History", type="secondary"):
            delete_user_history(user_id)
            st.success("✅ History cleared!")
            st.rerun()

    if not history:
        st.info("No history found. Start using the app to build your history!")
        return

    for item in history:
        tab_icons = {
            "ai_chat": "💬",
            "rag_search": "📚",
            "hospital_search": "🏥",
            "cost_estimate": "💰"
        }
        icon = tab_icons.get(item["tab_type"], "📝")
        label = item["tab_type"].replace("_", " ").title()

        with st.expander(f"{icon} {label} — {item['created_at'][:16]}"):
            st.markdown(f"**🔍 Query:** {item['query']}")
            st.markdown(f"**🤖 Response:**")
            st.write(item["response"][:500] + "..." if len(item["response"]) > 500 else item["response"])
            st.caption(f"Language: {item['language']}")

            if st.button(f"🗑️ Delete", key=f"del_{item['id']}"):
                delete_user_history(user_id, item["id"])
                st.success("Deleted!")
                st.rerun()