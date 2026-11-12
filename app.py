
import streamlit as st
import base64
from pathlib import Path

from engine.engine import analyze_flow
from engine.models import DataAsset, Destination, Sensitivity


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SentinelAI",
    page_icon="sentinelai_logo.png",
    layout="wide",
)

PROJECT_DIR = Path(__file__).parent
LOGO_PATH = PROJECT_DIR / "sentinelai_logo.png"
BACKGROUND_PATH = PROJECT_DIR / "sentinelai_background.png"


# --------------------------------------------------
# Background image styling
# --------------------------------------------------

if BACKGROUND_PATH.exists():
    with open(BACKGROUND_PATH, "rb") as image_file:
        background_base64 = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(2, 8, 25, 0.78),
                    rgba(2, 8, 25, 0.82)
                ),
                url("data:image/png;base64,{background_base64}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: rgba(2, 8, 25, 0.35);
        }}

        .block-container {{
            padding-top: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("Background image not found. Check its filename.")


# --------------------------------------------------
# Header and branding
# --------------------------------------------------

logo_col, title_col = st.columns([1, 7])

with logo_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=110)
    else:
        st.write("🛡️")

with title_col:
    st.title("SentinelAI")
    st.subheader("AI Agent Data Leak Detection Lab")

st.write(
    "Simulate how information moves through an AI workflow "
    "and identify data sent to unapproved destinations."
)

st.warning(
    "Training simulation only. Use fictional data, not real "
    "customer information, passwords, or API keys."
)

st.divider()


# --------------------------------------------------
# 1. Configure a simulated data flow
# --------------------------------------------------

st.header("1. Configure a simulated data flow")

left, right = st.columns(2)

with left:
    asset_choice = st.selectbox(
        "Choose the information being sent",
        [
            "Public product information",
            "Internal company notes",
            "Confidential customer email",
            "Secret API key",
        ],
    )

    sensitivity_by_asset = {
        "Public product information": Sensitivity.PUBLIC,
        "Internal company notes": Sensitivity.INTERNAL,
        "Confidential customer email": Sensitivity.CONFIDENTIAL,
        "Secret API key": Sensitivity.SECRET,
    }

    descriptions = {
        "Public product information":
            "Information intended for public viewing.",
        "Internal company notes":
            "Information intended for company use.",
        "Confidential customer email":
            "Fictional customer information that must be protected.",
        "Secret API key":
            "A simulated credential that must be protected.",
    }

    asset = DataAsset(
        name=asset_choice,
        sensitivity=sensitivity_by_asset[asset_choice],
        description=descriptions[asset_choice],
    )

with right:
    destination_choice = st.selectbox(
        "Choose where the information goes",
        [
            "Approved company database",
            "Unapproved external API",
            "Unapproved public logging service",
        ],
    )

    destination_details = {
    "Approved company database": ("database_1", True),
    "Unapproved external API": ("external_api_1", False),
    "Unapproved public logging service": ("logging_1", False),
    "Approved company logging service": ("logging_1", True),
}

    destination_id, is_approved = destination_details[
        destination_choice
    ]

    destination = Destination(
        destination_id=destination_id,
        name=destination_choice,
        approved=is_approved,
        description=(
            "Approved destination"
            if is_approved
            else "Not approved to receive this data"
        ),
    )

st.divider()


# --------------------------------------------------
# 2. Visualize the data flow
# --------------------------------------------------

st.header("2. Visualize the data flow")

source_col, arrow_col, destination_col = st.columns([5, 1, 5])

with source_col:
    st.markdown("#### 📄 Data source")
    st.info(
        f"**{asset.name}**\n\n"
        f"Sensitivity: **{asset.sensitivity.value.upper()}**"
    )

with arrow_col:
    st.markdown("#### ")
    st.markdown(
        "<div style='text-align:center; font-size:32px; "
        "padding-top:12px;'>→</div>",
        unsafe_allow_html=True,
    )

with destination_col:
    st.markdown("#### 🎯 Destination")

    if destination.approved:
        st.success(
            f"**{destination.name}**\n\n"
            "Approval: APPROVED"
        )
    else:
        st.error(
            f"**{destination.name}**\n\n"
            "Approval: UNAPPROVED"
        )

st.caption(
    "This diagram represents a simulated data flow, not a live "
    "connection to an external system."
)

st.divider()


# --------------------------------------------------
# 3. Run the security analysis
# --------------------------------------------------

st.header("3. Run the security analysis")

st.write(
    f"**Selected sensitivity:** "
    f"{asset.sensitivity.value.title()}  \n"
    f"**Destination status:** "
    f"{'Approved' if destination.approved else 'Unapproved'}"
)

if st.button("🔍 Analyze data flow", type="primary"):

    finding = analyze_flow(asset, destination)

    if finding is None:
        st.success(
            "No violation detected by the current security rules."
        )

        st.caption(
            "This does not guarantee the flow is secure; "
            "other security rules may not be implemented yet."
        )

    else:
        severity_value = getattr(
            finding.severity,
            "value",
            finding.severity,
        )
        severity_key = str(severity_value).lower()

        st.error(f"Severity: {severity_key.upper()}")

        st.write(f"**Data:** {asset.name}")
        st.write(
            f"**Sensitivity:** {asset.sensitivity.value.upper()}"
        )
        st.write(f"**Destination:** {destination.name}")
        st.write(
            f"**Destination approval:** "
            f"{'APPROVED' if destination.approved else 'UNAPPROVED'}"
        )

        explanation = None

        for attribute_name in (
            "message",
            "description",
            "reason",
            "details",
        ):
            candidate = getattr(
                finding,
                attribute_name,
                None,
            )

            if candidate:
                explanation = candidate
                break

        if explanation is None:
            explanation = (
                "The security engine detected a potential "
                "data-flow violation."
            )

        st.markdown(f"**Explanation:** {explanation}")

        recommended_actions = {
            "low": (
                "Review whether this destination should be "
                "approved for the selected information."
            ),
            "medium": (
                "Check the data-sharing policy and restrict "
                "access to the information if necessary."
            ),
            "high": (
                "Stop the simulated transfer and use an "
                "approved destination for confidential information."
            ),
            "critical": (
                "Block the simulated transfer. If a real credential "
                "were exposed, rotate it and investigate the exposure."
            ),
        }

        st.subheader("Recommended action")

        st.write(
            recommended_actions.get(
                severity_key,
                "Investigate this finding and review the data flow."
            )
        )

        st.caption(
            "This finding is based on simulated data and the "
            "current security policies."
        )

st.divider()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "SentinelAI prototype · Simulated scenarios · "
    "Security detection rules under development"
)
