import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import kb, profile_builder, style_extractor, advisor, writer

# --- Page Config ---
st.set_page_config(
    page_title="Cover Letter Assistant",
    page_icon="✉️",
    layout="wide",
)

# --- Session State Initialization ---
def init_state():
    defaults = {
        "profile_messages": [],
        "advisor_messages": [],
        "writer_messages": [],
        "advisor_image_path": None,
        "advisor_image_loaded": False,
        "profile_save_status": None,
        "brief_save_status": None,
        "draft_save_status": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# --- Sidebar ---
with st.sidebar:
    st.title("✉️ Cover Letter Assistant")
    st.divider()

    st.subheader("Workspace Status")
    profile_exists = bool(kb.read_personal_profile().strip().replace("# Personal Profile", "").strip())
    guidelines_exist = bool(kb.read_style_guidelines().strip().replace("# Style Guidelines", "").strip())
    brief_exists = bool(kb.read_application_brief())
    draft_exists = bool(kb.read_final_draft())

    st.markdown(f"{'✅' if profile_exists else '⬜'} Personal Profile")
    st.markdown(f"{'✅' if guidelines_exist else '⬜'} Style Guidelines")
    st.markdown(f"{'✅' if brief_exists else '⬜'} Application Brief")
    st.markdown(f"{'✅' if draft_exists else '⬜'} Final Draft")

    st.divider()
    if st.session_state.advisor_image_path:
        img_path = Path(st.session_state.advisor_image_path)
        if img_path.exists():
            st.subheader("Active Job Description")
            st.image(str(img_path), use_container_width=True)

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Profile Builder",
    "🎨 Style Extractor",
    "🔍 Application Advisor",
    "✍️ Cover Letter Writer",
])

# =====================================================================
# TAB 1 — PROFILE BUILDER
# =====================================================================
with tab1:
    st.header("👤 Profile Builder")
    st.caption("Upload your CV or other materials, then chat with the agent to build your personal profile.")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_material = st.file_uploader(
            "Upload a raw material (CV, LinkedIn export, etc.)",
            type=["txt", "md", "pdf"],
            key="profile_uploader",
        )
        raw_text = None
        if uploaded_material:
            try:
                raw_bytes = uploaded_material.read()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
                saved_path = kb.save_raw_material(raw_bytes, uploaded_material.name)
                st.success(f"Uploaded: `{uploaded_material.name}`")
                with st.expander("Preview uploaded content"):
                    st.text(raw_text[:2000] + ("..." if len(raw_text) > 2000 else ""))
            except Exception as e:
                st.error(f"Could not read file: {e}")

    with col2:
        current_profile = kb.read_personal_profile()
        with st.expander("View current personal_profile.md", expanded=False):
            st.markdown(current_profile if current_profile.strip() else "*No profile yet.*")

    st.divider()

    # Chat
    for msg in st.session_state.profile_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Talk to the Profile Builder...", key="profile_input"):
        st.session_state.profile_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = profile_builder.get_response(
                    messages=st.session_state.profile_messages,
                    raw_material_text=raw_text,
                )
            st.markdown(response)
            st.session_state.profile_messages.append({"role": "assistant", "content": response})

            if profile_builder.save_profile_from_response(response):
                st.success("Profile automatically saved to `my_info/personal_profile.md`!")

    if st.session_state.profile_messages:
        if st.button("💾 Save Profile from Last Response", key="save_profile_btn"):
            if st.session_state.profile_messages:
                last = st.session_state.profile_messages[-1]
                if last["role"] == "assistant":
                    if profile_builder.save_profile_from_response(last["content"]):
                        st.success("Profile saved!")
                    else:
                        st.warning("No profile found in the last response. Ask the agent to generate one.")

# =====================================================================
# TAB 2 — STYLE EXTRACTOR
# =====================================================================
with tab2:
    st.header("🎨 Style Extractor")
    st.caption("Upload your past cover letters to automatically extract your writing style and create guidelines.")

    uploaded_drafts = st.file_uploader(
        "Upload reference cover letters (one or more)",
        type=["txt", "md"],
        accept_multiple_files=True,
        key="style_uploader",
    )

    if uploaded_drafts:
        st.write(f"**{len(uploaded_drafts)} file(s) ready for analysis.**")
        if st.button("🎨 Extract Style & Generate Guidelines", type="primary"):
            draft_texts = []
            for f in uploaded_drafts:
                try:
                    text = f.read().decode("utf-8", errors="replace")
                    kb.save_reference_draft(text.encode("utf-8"), f.name)
                    draft_texts.append(text)
                except Exception as e:
                    st.error(f"Error reading {f.name}: {e}")

            if draft_texts:
                with st.spinner("Analyzing your writing style..."):
                    guidelines = style_extractor.extract_and_save(draft_texts)
                st.success("Style guidelines saved to `knowledge/style_guidelines.md`!")
                st.markdown(guidelines)

    st.divider()
    current_guidelines = kb.read_style_guidelines()
    with st.expander("View / Edit current style_guidelines.md", expanded=False):
        if current_guidelines.strip():
            st.markdown(current_guidelines)
        else:
            st.info("No style guidelines yet. Upload some reference drafts above.")

    st.divider()
    st.subheader("Manually Add a Rule")
    new_rule = st.text_area("Add a new rule or note to append to style_guidelines.md:", key="new_rule_input")
    if st.button("➕ Append Rule", key="append_rule_btn") and new_rule.strip():
        kb.append_to_style_guidelines(f"\n- {new_rule.strip()}")
        st.success("Rule appended!")

# =====================================================================
# TAB 3 — APPLICATION ADVISOR
# =====================================================================
with tab3:
    st.header("🔍 Application Advisor")
    st.caption("Upload a screenshot of the job description and chat with the Advisor to evaluate the role and generate your application brief.")

    uploaded_job = st.file_uploader(
        "Upload job description screenshot (PNG or JPG)",
        type=["png", "jpg", "jpeg"],
        key="job_uploader",
    )

    if uploaded_job:
        img_bytes = uploaded_job.read()
        saved_img_path = kb.save_job_description_image(img_bytes, uploaded_job.name)
        st.session_state.advisor_image_path = str(saved_img_path)
        st.session_state.advisor_image_loaded = True
        st.image(img_bytes, caption="Job Description", use_container_width=True)

    st.divider()

    if not st.session_state.advisor_image_path:
        st.info("Upload a job description screenshot above to begin.")
    else:
        # Chat history
        for msg in st.session_state.advisor_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Talk to the Advisor...", key="advisor_input"):
            st.session_state.advisor_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    # Pass image only on the first turn
                    img_path = Path(st.session_state.advisor_image_path)
                    use_image = img_path if len(st.session_state.advisor_messages) <= 2 else None
                    response = advisor.get_response(
                        messages=st.session_state.advisor_messages,
                        image_path=use_image,
                    )
                st.markdown(response)
                st.session_state.advisor_messages.append({"role": "assistant", "content": response})

                if advisor.save_brief_from_response(response):
                    st.success("Application Brief automatically saved to `workspace/application_brief.md`!")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Generate Application Brief Now", key="gen_brief_btn", type="primary"):
                trigger_msg = {"role": "user", "content": "Please generate the application_brief.md now."}
                st.session_state.advisor_messages.append(trigger_msg)
                with st.spinner("Generating brief..."):
                    img_path = Path(st.session_state.advisor_image_path)
                    response = advisor.get_response(
                        messages=st.session_state.advisor_messages,
                        image_path=img_path if len(st.session_state.advisor_messages) <= 2 else None,
                    )
                st.session_state.advisor_messages.append({"role": "assistant", "content": response})
                if advisor.save_brief_from_response(response):
                    st.success("Application Brief saved!")
                st.rerun()

        with col2:
            if st.button("🔄 Reset Advisor Chat", key="reset_advisor_btn"):
                st.session_state.advisor_messages = []
                st.session_state.advisor_image_path = None
                st.session_state.advisor_image_loaded = False
                st.rerun()

        current_brief = kb.read_application_brief()
        if current_brief:
            with st.expander("View current application_brief.md"):
                st.markdown(current_brief)

# =====================================================================
# TAB 4 — COVER LETTER WRITER
# =====================================================================
with tab4:
    st.header("✍️ Cover Letter Writer")
    st.caption("Iteratively refine your cover letter with the Writer agent. Start by generating the initial draft.")

    brief_exists = bool(kb.read_application_brief())
    if not brief_exists:
        st.warning("No Application Brief found. Please complete the Advisor phase in Tab 3 first.")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Chat history
            for msg in st.session_state.writer_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if not st.session_state.writer_messages:
                if st.button("🚀 Generate Initial Draft", type="primary", key="gen_draft_btn"):
                    init_msg = {"role": "user", "content": "Please write the initial cover letter draft."}
                    st.session_state.writer_messages.append(init_msg)
                    with st.spinner("Writing your cover letter..."):
                        response = writer.get_response(messages=st.session_state.writer_messages)
                    st.session_state.writer_messages.append({"role": "assistant", "content": response})
                    if writer.save_draft_from_response(response):
                        st.success("Draft saved to `workspace/final_draft.md`!")
                    st.rerun()
            else:
                if prompt := st.chat_input("Ask the Writer to make changes...", key="writer_input"):
                    st.session_state.writer_messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    with st.chat_message("assistant"):
                        with st.spinner("Revising..."):
                            response = writer.get_response(messages=st.session_state.writer_messages)
                        st.markdown(response)
                        st.session_state.writer_messages.append({"role": "assistant", "content": response})
                        if writer.save_draft_from_response(response):
                            st.success("Draft saved!")

        with col2:
            st.subheader("Current Draft")
            final_draft = kb.read_final_draft()
            if final_draft:
                st.markdown(final_draft)
                st.download_button(
                    label="⬇️ Download final_draft.md",
                    data=final_draft,
                    file_name="final_draft.md",
                    mime="text/markdown",
                )
            else:
                st.info("No draft yet. Generate one from the left panel.")

            if st.button("🔄 Reset Writer Chat", key="reset_writer_btn"):
                st.session_state.writer_messages = []
                st.rerun()
