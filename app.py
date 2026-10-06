import streamlit as st

from modules.symptom_analyzer import analyze_symptoms
from auth import register_user, login_user
from history import save_analysis, get_user_history


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HealthAI",
    page_icon="🏥",
    layout="wide"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 20px;
    }

    .dashboard-card {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #eef6ff,
            #ffffff
        );
        border: 1px solid #d8e8f7;
        min-height: 145px;
        margin-bottom: 15px;
    }

    .dashboard-card h3 {
        margin-bottom: 8px;
    }

    .dashboard-card h2 {
        margin: 5px 0;
    }

    .dashboard-card h1 {
        margin: 5px 0;
    }

    .dashboard-card p {
        color: #666666;
    }

    .recent-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #dddddd;
        background: #fafafa;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HELPER FUNCTION
# =====================================================

def get_result_text(record):

    result = record.get(
        "result",
        "Unknown"
    )

    if isinstance(result, dict):

        return str(
            result.get(
                "condition",
                "Unknown"
            )
        )

    if isinstance(result, list):

        if result:

            if isinstance(
                result[0],
                dict
            ):

                return str(
                    result[0].get(
                        "condition",
                        "Unknown"
                    )
                )

            return str(result[0])

        return "Unknown"

    return str(result)


# =====================================================
# LOGIN / REGISTER
# =====================================================

if not st.session_state.logged_in:

    st.title("🏥 HealthAI")

    st.subheader(
        "AI-Powered Healthcare Assistance System"
    )

    st.write(
        "An educational AI/ML application for "
        "basic symptom-pattern analysis."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )


    # =================================================
    # LOGIN
    # =================================================

    with login_tab:

        st.subheader("🔐 Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            key="login_button"
        ):

            success, username = login_user(
                login_email,
                login_password
            )

            if success:

                st.session_state.logged_in = True

                st.session_state.username = (
                    username
                )

                st.session_state.user_email = (
                    login_email.lower().strip()
                )

                st.session_state.page = (
                    "🏠 Dashboard"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )


    # =================================================
    # REGISTER
    # =================================================

    with register_tab:

        st.subheader("📝 Create Account")

        register_name = st.text_input(
            "Full Name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="register_button"
        ):

            if (
                not register_name
                or not register_email
                or not register_password
            ):

                st.error(
                    "Please fill in all fields."
                )

            elif register_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(register_password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                success, message = register_user(
                    register_name,
                    register_email,
                    register_password
                )

                if success:

                    st.success(message)

                    st.info(
                        "Account created successfully. "
                        "Please login."
                    )

                else:

                    st.error(message)

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🏥 HealthAI")

st.sidebar.caption(
    "AI-Powered Healthcare Assistance"
)

st.sidebar.success(
    f"Welcome, {st.session_state.username}! 👋"
)

st.sidebar.markdown(
    "### 📌 Navigation"
)


# =====================================================
# NAVIGATION
# =====================================================

if st.sidebar.button(
    "🏠 Dashboard",
    use_container_width=True,
    key="navigation_dashboard"
):

    st.session_state.page = "🏠 Dashboard"


if st.sidebar.button(
    "🩺 Symptom Analyzer",
    use_container_width=True,
    key="navigation_analyzer"
):

    st.session_state.page = (
        "🩺 Symptom Analyzer"
    )


if st.sidebar.button(
    "📜 History",
    use_container_width=True,
    key="navigation_history"
):

    st.session_state.page = "📜 History"


if st.sidebar.button(
    "📊 Health Information",
    use_container_width=True,
    key="navigation_health"
):

    st.session_state.page = (
        "📊 Health Information"
    )


if st.sidebar.button(
    "🚨 Safety",
    use_container_width=True,
    key="navigation_safety"
):

    st.session_state.page = "🚨 Safety"


if st.sidebar.button(
    "ℹ️ About",
    use_container_width=True,
    key="navigation_about"
):

    st.session_state.page = "ℹ️ About"


# =====================================================
# LOGOUT
# =====================================================

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True,
    key="navigation_logout"
):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_email = ""
    st.session_state.page = "🏠 Dashboard"

    st.rerun()


page = st.session_state.page


# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        '🏥 HealthAI Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Smart AI-powered health assistance at your fingertips'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Welcome back, "
        f"**{st.session_state.username}** 👋"
    )

    st.divider()

    user_history = get_user_history(
        st.session_state.user_email
    )

    total_analyses = len(
        user_history
    )

    # -------------------------------------------------
    # LATEST RESULT
    # -------------------------------------------------

    if user_history:

        latest_result = get_result_text(
            user_history[-1]
        )

    else:

        latest_result = "No analysis yet"


    # -------------------------------------------------
    # MAIN CARDS
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <h3>📋 Total Analyses</h3>
                <h1>{total_analyses}</h1>
                <p>Completed health analyses</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <h3>🤖 Latest Pattern</h3>
                <h2>{latest_result}</h2>
                <p>Most recent AI/ML result</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="dashboard-card">
                <h3>🔐 Account</h3>
                <h2>Active</h2>
                <p>Your HealthAI account is active</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -------------------------------------------------
    # QUICK ACTIONS
    # -------------------------------------------------

    st.divider()

    st.subheader("⚡ Quick Actions")

    action1, action2, action3 = st.columns(3)

    with action1:

        if st.button(
            "🩺 Start New Analysis",
            use_container_width=True,
            key="quick_analysis"
        ):

            st.session_state.page = (
                "🩺 Symptom Analyzer"
            )

            st.rerun()

    with action2:

        if st.button(
            "📜 View History",
            use_container_width=True,
            key="quick_history"
        ):

            st.session_state.page = (
                "📜 History"
            )

            st.rerun()

    with action3:

        if st.button(
            "🚨 Safety Information",
            use_container_width=True,
            key="quick_safety"
        ):

            st.session_state.page = (
                "🚨 Safety"
            )

            st.rerun()


    # -------------------------------------------------
    # ANALYSIS OVERVIEW
    # -------------------------------------------------

    st.divider()

    st.subheader("📊 Analysis Overview")

    if user_history:

        results = []

        for record in user_history:

            results.append(
                get_result_text(record)
            )

        unique_results = len(
            set(results)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                <div class="dashboard-card">
                    <h3>🩺 Completed Analyses</h3>
                    <h1>{len(results)}</h1>
                    <p>Total analyses in your account</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="dashboard-card">
                    <h3>📊 Different Patterns</h3>
                    <h1>{unique_results}</h1>
                    <p>Different AI/ML patterns recorded</p>
                </div>
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # RECENT ACTIVITY
        # -------------------------------------------------

        st.subheader("🕒 Recent Activity")

        recent_records = list(
            reversed(
                user_history[-3:]
            )
        )

        for record in recent_records:

            result = get_result_text(
                record
            )

            symptoms = record.get(
                "symptoms",
                "Not available"
            )

            date = record.get(
                "date",
                "Not available"
            )

            st.markdown(
                f"""
                <div class="recent-card">
                    <h4>🤖 {result}</h4>
                    <p>
                        🩺 <b>Symptoms:</b>
                        {symptoms}
                    </p>
                    <p>
                        🗓️ <b>Date:</b>
                        {date}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "📭 No analyses yet. "
            "Click 'Start New Analysis' to begin."
        )


    # -------------------------------------------------
    # SAFETY NOTICE
    # -------------------------------------------------

    st.divider()

    st.warning(
        "⚠️ HealthAI is an educational AI/ML "
        "project. Its results are not medical "
        "diagnoses. For health concerns, consult "
        "a qualified healthcare professional."
    )


# =====================================================
# SYMPTOM ANALYZER
# =====================================================

elif page == "🩺 Symptom Analyzer":

    st.title("🩺 Symptom Analyzer")

    st.write(
        "Enter basic information and select symptoms "
        "to generate an educational AI/ML pattern."
    )

    st.divider()


    # -------------------------------------------------
    # BASIC INFORMATION
    # -------------------------------------------------

    st.subheader("👤 Basic Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=20,
            key="health_age"
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Prefer not to say",
                "Female",
                "Male",
                "Other"
            ],
            key="health_gender"
        )

    with col3:

        duration = st.selectbox(
            "Symptom Duration",
            [
                "Less than 1 day",
                "1–3 days",
                "4–7 days",
                "More than 1 week"
            ],
            key="health_duration"
        )


    st.divider()


    # -------------------------------------------------
    # SYMPTOMS
    # -------------------------------------------------

    st.subheader(
        "🩺 Select Your Symptoms"
    )

    st.caption(
        "Select all symptoms that apply."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        fever = st.checkbox(
            "🌡️ Fever",
            key="health_fever"
        )

        cough = st.checkbox(
            "😷 Cough",
            key="health_cough"
        )

        sore_throat = st.checkbox(
            "🗣️ Sore Throat",
            key="health_sore_throat"
        )

    with col2:

        headache = st.checkbox(
            "🤕 Headache",
            key="health_headache"
        )

        runny_nose = st.checkbox(
            "👃 Runny Nose",
            key="health_runny_nose"
        )

        fatigue = st.checkbox(
            "😴 Fatigue",
            key="health_fatigue"
        )

    with col3:

        stomach_pain = st.checkbox(
            "🤢 Stomach Pain",
            key="health_stomach_pain"
        )

        vomiting = st.checkbox(
            "🤮 Vomiting",
            key="health_vomiting"
        )

        diarrhea = st.checkbox(
            "💧 Diarrhea",
            key="health_diarrhea"
        )


    st.divider()


    # -------------------------------------------------
    # ADDITIONAL INFORMATION
    # -------------------------------------------------

    st.subheader(
        "📝 Additional Information"
    )

    additional_info = st.text_area(
        "Anything else you would like to mention?",
        placeholder=(
            "Example: mild body pain, reduced appetite, etc."
        ),
        key="health_additional_info"
    )


    st.divider()


    # -------------------------------------------------
    # ANALYZE
    # -------------------------------------------------

    if st.button(
        "🔍 Analyze Symptoms",
        use_container_width=True,
        key="health_analyze"
    ):

        selected_symptoms = []

        if fever:
            selected_symptoms.append(
                "fever"
            )

        if cough:
            selected_symptoms.append(
                "cough"
            )

        if sore_throat:
            selected_symptoms.append(
                "sore throat"
            )

        if headache:
            selected_symptoms.append(
                "headache"
            )

        if runny_nose:
            selected_symptoms.append(
                "runny nose"
            )

        if fatigue:
            selected_symptoms.append(
                "fatigue"
            )

        if stomach_pain:
            selected_symptoms.append(
                "stomach pain"
            )

        if vomiting:
            selected_symptoms.append(
                "vomiting"
            )

        if diarrhea:
            selected_symptoms.append(
                "diarrhea"
            )


        if not selected_symptoms:

            st.error(
                "⚠️ Please select at least one symptom."
            )

        else:

            symptom_text = ", ".join(
                selected_symptoms
            )

            # -----------------------------------------
            # AI/ML ANALYSIS
            # -----------------------------------------

            condition = analyze_symptoms(
                symptom_text
            )

            # -----------------------------------------
            # SAVE HISTORY
            # -----------------------------------------

            save_analysis(
                st.session_state.user_email,
                symptom_text,
                condition
            )

            st.success(
                "✅ Analysis completed successfully."
            )

            st.divider()


            # -----------------------------------------
            # SUMMARY
            # -----------------------------------------

            st.subheader(
                "📋 Analysis Summary"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "👤 Age",
                    age
                )

            with col2:

                st.metric(
                    "🩺 Symptoms",
                    len(selected_symptoms)
                )

            with col3:

                st.metric(
                    "🗓️ Duration",
                    duration
                )


            st.divider()


            # -----------------------------------------
            # AI RESULT
            # -----------------------------------------

            st.subheader(
                "🤖 AI/ML Result"
            )

            st.info(
                f"Possible symptom pattern: "
                f"**{condition}**"
            )

            st.caption(
                "This is an educational AI/ML prediction "
                "based on the project's sample dataset."
            )


            # -----------------------------------------
            # SELECTED SYMPTOMS
            # -----------------------------------------

            st.subheader(
                "🩺 Selected Symptoms"
            )

            symptom_cols = st.columns(3)

            for index, symptom in enumerate(
                selected_symptoms
            ):

                with symptom_cols[
                    index % 3
                ]:

                    st.success(
                        f"✓ {symptom.title()}"
                    )


            # -----------------------------------------
            # INFORMATION PROVIDED
            # -----------------------------------------

            st.subheader(
                "👤 Information Provided"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Age:** {age}"
                )

                st.write(
                    f"**Gender:** {gender}"
                )

            with col2:

                st.write(
                    f"**Duration:** {duration}"
                )

                st.write(
                    f"**Number of Symptoms:** "
                    f"{len(selected_symptoms)}"
                )


            if additional_info.strip():

                st.subheader(
                    "📝 Additional Information"
                )

                st.write(
                    additional_info
                )


            # -----------------------------------------
            # GUIDANCE
            # -----------------------------------------

            st.divider()

            st.subheader(
                "💡 General Guidance"
            )

            st.info(
                "Maintain adequate hydration, get "
                "appropriate rest, and monitor how "
                "you feel. If symptoms persist, "
                "worsen, or concern you, contact a "
                "qualified healthcare professional."
            )


            # -----------------------------------------
            # SAFETY
            # -----------------------------------------

         # =====================================================
# SAFETY + FOOD GUIDE
# =====================================================

elif page == "🚨 Safety":

    st.title("🚨 Safety & Food Guide")

    st.write(
        "Select a possible symptom pattern to view "
        "general food, hydration, rest and self-care suggestions."
    )

    st.warning(
        "⚠️ HealthAI provides educational information only. "
        "It does not diagnose diseases or prescribe medicines."
    )

    st.divider()

    # =================================================
    # SELECT PATTERN
    # =================================================

    st.subheader("🩺 Select Health Pattern")

    selected_pattern = st.selectbox(
        "Choose a pattern",
        [
            "Common Cold",
            "Flu",
            "Gastroenteritis",
            "Throat Infection",
            "Headache"
        ]
    )

    st.divider()

    # =================================================
    # SAFETY INFORMATION
    # =================================================

    safety_data = {

        "Common Cold": {

            "eat": [
                "🍲 Warm soups",
                "🥣 Light and nutritious meals",
                "🍌 Fruits such as banana",
                "🍎 Fresh fruits",
                "🥗 Vegetables",
                "☕ Warm fluids"
            ],

            "avoid": [
                "🌶️ Very spicy foods if they cause discomfort",
                "🍟 Very heavy or greasy foods if they feel uncomfortable",
                "🚫 Foods that personally worsen your symptoms"
            ],

            "hydration": [
                "💧 Drink water regularly",
                "☕ Warm fluids may feel soothing",
                "🥤 Maintain adequate fluid intake"
            ],

            "rest": [
                "😴 Get adequate sleep",
                "🛌 Take enough rest",
                "🧘 Avoid unnecessary physical strain"
            ],

            "medical": (
                "Seek appropriate medical care if symptoms "
                "are severe, getting worse, persistent, "
                "or causing significant concern."
            )
        },


        "Flu": {

            "eat": [
                "🍲 Light soups",
                "🍚 Simple nutritious meals",
                "🍌 Fresh fruits",
                "🥗 Nutritious foods as tolerated",
                "🥣 Easy-to-eat meals"
            ],

            "avoid": [
                "🌶️ Very spicy foods if they cause discomfort",
                "🍔 Very heavy meals when feeling unwell",
                "🚫 Foods that personally worsen symptoms"
            ],

            "hydration": [
                "💧 Drink fluids regularly",
                "🥤 Maintain adequate hydration",
                "☕ Warm fluids may feel comfortable"
            ],

            "rest": [
                "😴 Get enough sleep",
                "🛌 Take adequate rest",
                "🚶 Return to normal activity gradually"
            ],

            "medical": (
                "Seek professional medical care if symptoms "
                "become severe, worsen, persist, or cause "
                "significant concern."
            )
        },


        "Gastroenteritis": {

            "eat": [
                "🍚 Simple and light foods as tolerated",
                "🍌 Banana",
                "🥣 Light meals",
                "🍞 Plain foods that feel comfortable",
                "🥗 Nutritious foods as tolerated"
            ],

            "avoid": [
                "🌶️ Very spicy foods",
                "🍟 Very greasy or heavy foods",
                "🚫 Foods that clearly make stomach symptoms worse"
            ],

            "hydration": [
                "💧 Take fluids regularly",
                "🥤 Pay attention to hydration",
                "💧 Replace fluids after vomiting or diarrhea"
            ],

            "rest": [
                "😴 Get adequate rest",
                "🛌 Allow your body time to recover",
                "🏃 Avoid unnecessary strenuous activity"
            ],

            "medical": (
                "Seek appropriate medical care if vomiting "
                "or diarrhea is persistent, symptoms become "
                "severe, or you are unable to maintain hydration."
            )
        },


        "Throat Infection": {

            "eat": [
                "🥣 Soft foods",
                "🍲 Warm soups",
                "🍌 Soft fruits",
                "🥗 Nutritious foods that are comfortable to eat",
                "☕ Warm fluids"
            ],

            "avoid": [
                "🌶️ Very spicy foods if they irritate your throat",
                "🚫 Foods that cause throat discomfort",
                "🥨 Very hard foods if swallowing is uncomfortable"
            ],

            "hydration": [
                "💧 Drink water regularly",
                "☕ Warm fluids may feel soothing",
                "🥤 Stay adequately hydrated"
            ],

            "rest": [
                "😴 Get adequate sleep",
                "🛌 Take sufficient rest",
                "🗣️ Avoid unnecessary voice strain"
            ],

            "medical": (
                "Seek appropriate medical care if throat "
                "symptoms are severe, persistent, worsening, "
                "or causing significant difficulty."
            )
        },


        "Headache": {

            "eat": [
                "🍎 Fresh fruits",
                "🥗 Balanced meals",
                "🍚 Regular nutritious meals",
                "🥣 Light meals if preferred"
            ],

            "avoid": [
                "🚫 Skipping meals",
                "🍫 Foods that you personally notice trigger discomfort",
                "☕ Excessive caffeine if it makes you feel worse"
            ],

            "hydration": [
                "💧 Drink enough water",
                "🥤 Maintain regular fluid intake"
            ],

            "rest": [
                "😴 Get adequate sleep",
                "🧘 Rest in a comfortable environment",
                "📱 Take breaks from screens if they worsen discomfort"
            ],

            "medical": (
                "Seek appropriate medical care if headaches "
                "are severe, unusual, persistent, worsening, "
                "or causing significant concern."
            )
        }
    }


    # =================================================
    # GET CURRENT INFORMATION
    # =================================================

    current = safety_data[selected_pattern]


    # =================================================
    # FOOD SECTION
    # =================================================

    st.subheader("🍎 What You Can Eat")

    food_col1, food_col2 = st.columns(2)

    with food_col1:

        st.markdown("### 🍽️ Suggested Foods")

        for item in current["eat"]:

            st.success(item)

    with food_col2:

        st.markdown("### 💡 Food Tip")

        st.info(
            "Choose foods that are comfortable for you "
            "and try to maintain a balanced diet."
        )


    # =================================================
    # AVOID SECTION
    # =================================================

    st.divider()

    st.subheader("🚫 What to Avoid")

    for item in current["avoid"]:

        st.warning(item)


    # =================================================
    # HYDRATION SECTION
    # =================================================

    st.divider()

    st.subheader("💧 Hydration")

    for item in current["hydration"]:

        st.info(item)


    # =================================================
    # REST & SELF CARE
    # =================================================

    st.divider()

    st.subheader("😴 Rest & Self-Care")

    rest_col1, rest_col2 = st.columns(2)

    with rest_col1:

        for item in current["rest"]:

            st.success(item)

    with rest_col2:

        st.info(
            "💡 Listen to your body and avoid "
            "unnecessary physical strain while "
            "you are feeling unwell."
        )


    # =================================================
    # WHEN TO SEEK MEDICAL HELP
    # =================================================

    st.divider()

    st.subheader("🚨 When to Seek Medical Help")

    st.error(
        current["medical"]
    )


    # =================================================
    # GENERAL SAFETY
    # =================================================

    st.divider()

    st.subheader("🛡️ General Safety")

    st.write(
        """
        • HealthAI is an educational AI/ML project.

        • The displayed pattern is not a confirmed diagnosis.

        • Food suggestions are general wellness suggestions.

        • Do not use HealthAI to make important medical decisions.

        • If you are worried about your symptoms,
          speak with a qualified healthcare professional.

        • If symptoms are severe or rapidly worsening,
          seek appropriate medical care.
        """
    )


    # =================================================
    # FINAL DISCLAIMER
    # =================================================

    st.divider()

    st.warning(
        "⚠️ Important: HealthAI does not replace a "
        "qualified healthcare professional. The food, "
        "hydration and self-care information above is "
        "general educational guidance."
    )


# =====================================================
# HISTORY
# =====================================================

elif page == "📜 History":

    st.title("📜 Analysis History")

    st.write(
        "View your previous HealthAI symptom analyses."
    )

    st.divider()

    user_history = get_user_history(
        st.session_state.user_email
    )


    if not user_history:

        st.info(
            "📭 No analyses found yet."
        )

        st.write(
            "Go to 🩺 Symptom Analyzer to perform "
            "your first analysis."
        )

    else:

        total = len(
            user_history
        )

        results = []

        for record in user_history:

            results.append(
                get_result_text(record)
            )

        different_patterns = len(
            set(results)
        )


        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📋 Total Analyses",
                total
            )

        with col2:

            st.metric(
                "🤖 Different Patterns",
                different_patterns
            )


        st.divider()

        st.subheader(
            "🕒 Previous Analyses"
        )


        # -------------------------------------------------
        # RECORDS
        # -------------------------------------------------

        for index, record in enumerate(
            reversed(user_history)
        ):

            result = get_result_text(
                record
            )

            date = record.get(
                "date",
                "Unknown date"
            )

            symptoms = record.get(
                "symptoms",
                "Not available"
            )


            with st.expander(
                f"🤖 {result}  •  🗓️ {date}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**🩺 Symptoms**"
                    )

                    st.info(
                        symptoms
                    )

                with col2:

                    st.write(
                        "**🤖 AI/ML Pattern**"
                    )

                    st.success(
                        result
                    )

                st.caption(
                    f"Analysis #{total - index}"
                )


        st.divider()

        st.warning(
            "⚠️ These results are educational "
            "AI/ML patterns and are not medical diagnoses."
        )


# =====================================================
# HEALTH INFORMATION
# =====================================================

elif page == "📊 Health Information":

    st.title(
        "📊 Health Information"
    )

    st.write(
        "Explore basic educational information "
        "about common health conditions and symptoms."
    )

    st.divider()


    health_information = {

        "🤧 Common Cold": {
            "description":
                "A common respiratory illness that "
                "may include cough, runny nose, "
                "sore throat and tiredness.",

            "symptoms":
                "Cough, runny nose, sore throat "
                "and fatigue."
        },

        "🤒 Flu": {
            "description":
                "Flu is a respiratory illness that "
                "can cause several general symptoms.",

            "symptoms":
                "Fever, cough, headache and fatigue."
        },

        "🤢 Gastroenteritis": {
            "description":
                "Gastroenteritis can affect the "
                "digestive system and may cause "
                "stomach-related symptoms.",

            "symptoms":
                "Stomach pain, vomiting and diarrhea."
        },

        "🗣️ Throat Infection": {
            "description":
                "A throat infection may cause "
                "discomfort in the throat and "
                "related symptoms.",

            "symptoms":
                "Sore throat and discomfort "
                "while swallowing."
        },

        "🤕 Headache": {
            "description":
                "Headaches can have many possible "
                "causes and can vary in duration "
                "and intensity.",

            "symptoms":
                "Head pain and possible tiredness."
        }
    }


    # -------------------------------------------------
    # INFORMATION
    # -------------------------------------------------

    for title, information in (
        health_information.items()
    ):

        with st.expander(title):

            st.write(
                information["description"]
            )

            st.markdown(
                "**Common symptoms:**"
            )

            st.write(
                information["symptoms"]
            )


    # -------------------------------------------------
    # HEALTH TIPS
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "💡 General Health Tips"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "💧 Stay hydrated and drink "
            "enough fluids."
        )

    with col2:

        st.info(
            "😴 Get adequate rest and maintain "
            "a regular sleep routine."
        )

    with col3:

        st.info(
            "🥗 Maintain a balanced and "
            "nutritious diet."
        )


    # -------------------------------------------------
    # DISCLAIMER
    # -------------------------------------------------

    st.divider()

    st.warning(
        "⚠️ This information is provided for "
        "educational purposes only. It is not "
        "a medical diagnosis or a substitute "
        "for professional medical advice."
    )


# =====================================================
# SAFETY
# =====================================================

elif page == "🚨 Safety":

    st.title(
        "🚨 Safety Information"
    )

    st.warning(
        "HealthAI is an educational project "
        "and should not be used as a medical "
        "diagnostic tool."
    )

    st.divider()

    st.subheader(
        "🛡️ Important Safety Guidelines"
    )

    st.write(
        """
        • Do not use HealthAI as a replacement
          for professional healthcare.

        • AI/ML results are educational patterns
          based on a sample dataset.

        • If symptoms are severe or rapidly
          worsening, seek appropriate medical care.

        • If you are seriously concerned about
          your health, speak with a qualified
          healthcare professional.

        • If symptoms continue or do not improve,
          seek appropriate medical advice.
        """
    )

    st.divider()

    st.subheader(
        "⚠️ About AI Results"
    )

    st.info(
        "The prediction generated by this project "
        "is not a confirmed diagnosis. AI/ML systems "
        "can make mistakes and should not be used "
        "to make important healthcare decisions."
    )

    st.error(
        "For urgent or serious health concerns, "
        "seek appropriate professional medical care."
    )


# =====================================================
# ABOUT
# =====================================================

# =====================================================
# ABOUT MODULE
# =====================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About HealthAI")

    st.write(
        "AI-Powered Healthcare Assistance System"
    )

    st.divider()

    # -------------------------------------------------
    # ABOUT PROJECT
    # -------------------------------------------------

    st.subheader("🏥 About HealthAI")

    st.write(
        "HealthAI is an educational AI/ML-based "
        "healthcare assistance application developed "
        "using Python and Streamlit."
    )

    st.write(
        "The system allows users to enter selected "
        "symptoms and receive a possible symptom "
        "pattern based on a machine-learning model."
    )

    st.info(
        "💡 HealthAI is designed as an educational "
        "college project and is not a medical diagnostic system."
    )


    # -------------------------------------------------
    # PROJECT OBJECTIVE
    # -------------------------------------------------

    st.subheader("🎯 Project Objective")

    st.write(
        """
        The main objectives of HealthAI are:

        • Provide a simple and user-friendly healthcare interface.

        • Demonstrate how machine learning can be
          integrated into a Streamlit application.

        • Analyze selected symptoms using a basic
          machine-learning model.

        • Store previous analysis results for the user.

        • Provide general health and safety information.
        """
    )


    # -------------------------------------------------
    # HOW AI/ML WORKS
    # -------------------------------------------------

    st.subheader("🤖 How AI/ML Works")

    st.write(
        """
        HealthAI uses a machine-learning model to
        analyze the symptoms selected by the user.

        The selected symptoms are converted into
        input features and provided to the trained
        model.

        The model then produces a possible symptom
        pattern based on the project's sample dataset.
        """
    )

    st.info(
        "The result is a possible pattern from the "
        "training dataset and should not be considered "
        "a confirmed medical diagnosis."
    )


    # -------------------------------------------------
    # TECHNOLOGIES
    # -------------------------------------------------

    st.subheader("⚙️ Technologies Used")

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:

        st.markdown("### 💻 Programming")

        st.write(
            """
            • Python
            • Streamlit
            • Pandas
            • Scikit-learn
            """
        )

    with tech_col2:

        st.markdown("### 🧠 Machine Learning")

        st.write(
            """
            • Decision Tree Classifier
            • Label Encoding
            • Feature-based symptom analysis
            """
        )


    # -------------------------------------------------
    # FEATURES
    # -------------------------------------------------

    st.divider()

    st.subheader("✨ Key Features")

    features = [
        "🔐 User Registration & Login",
        "🏠 Interactive Dashboard",
        "🩺 AI/ML Symptom Analyzer",
        "📜 Analysis History",
        "📊 Health Information",
        "🚨 Safety & Food Guide",
        "💧 General Wellness Suggestions"
    ]

    feature_col1, feature_col2 = st.columns(2)

    for index, feature in enumerate(features):

        if index % 2 == 0:

            with feature_col1:

                st.success(feature)

        else:

            with feature_col2:

                st.success(feature)


    # -------------------------------------------------
    # DATASET
    # -------------------------------------------------

    st.divider()

    st.subheader("📊 Dataset Information")

    st.write(
        """
        The project uses a sample symptom dataset
        containing selected symptoms such as:

        • Fever
        • Cough
        • Sore throat
        • Headache
        • Runny nose
        • Fatigue
        • Stomach pain
        • Vomiting
        • Diarrhea

        The dataset is used for demonstrating the
        machine-learning workflow of the project.
        """
    )

    st.warning(
        "⚠️ The sample dataset is for educational "
        "demonstration and is not clinically validated."
    )


    # -------------------------------------------------
    # SAFETY & LIMITATIONS
    # -------------------------------------------------

    st.divider()

    st.subheader("🛡️ Safety & Limitations")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🏥 HealthAI | AI-Powered Healthcare Assistance "
    "System | Educational AI/ML Project"
)