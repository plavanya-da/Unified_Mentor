import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Distributor",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

DATA_PATH = Path(
    r"D:\Nassau Candy Distributor  Project\02_Streamlit_Dashboard\Nassau_Candy_Processed.csv"
)

ASSET_FOLDER = Path("assets")

HEADER_IMAGE = ASSET_FOLDER / "candy_header.png"


# ============================================================
# CREATE SIMPLE CANDY HEADER PNG
# ============================================================

def create_header_image():

    if HEADER_IMAGE.exists():
        return

    try:

        from PIL import Image, ImageDraw, ImageFont

        ASSET_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        width = 1600
        height = 250

        image = Image.new(
            "RGB",
            (width, height),
            "#FFF5F2"
        )

        draw = ImageDraw.Draw(image)

        # Border
        draw.rounded_rectangle(
            (5, 5, width - 5, height - 5),
            radius=20,
            fill="#FFF5F2",
            outline="#E8D6D0",
            width=3
        )

        # ----------------------------------------------------
        # Chocolate bars on left
        # ----------------------------------------------------

        chocolate_x = 55
        chocolate_y = 65

        draw.rounded_rectangle(
            (
                chocolate_x,
                chocolate_y,
                chocolate_x + 190,
                chocolate_y + 100
            ),
            radius=12,
            fill="#6B3E2E"
        )

        for row in range(2):

            for col in range(3):

                x1 = (
                    chocolate_x
                    + 12
                    + col * 58
                )

                y1 = (
                    chocolate_y
                    + 12
                    + row * 43
                )

                draw.rounded_rectangle(
                    (
                        x1,
                        y1,
                        x1 + 45,
                        y1 + 32
                    ),
                    radius=5,
                    fill="#8A563F"
                )


        # ----------------------------------------------------
        # Candy circles
        # ----------------------------------------------------

        candies = [
            (1280, 55, 23, "#E86B7E"),
            (1350, 125, 28, "#4A9AC5"),
            (1430, 60, 24, "#F2B544"),
            (1500, 135, 25, "#6DB47C"),
            (1230, 145, 22, "#A86DB6"),
            (1540, 55, 20, "#E86B7E"),
        ]

        for x, y, radius, color in candies:

            draw.ellipse(
                (
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius
                ),
                fill=color
            )


        # ----------------------------------------------------
        # Simple lollipop
        # ----------------------------------------------------

        draw.line(
            (1150, 150, 1150, 225),
            fill="#8B6B5A",
            width=6
        )

        draw.ellipse(
            (1105, 90, 1195, 180),
            fill="#4A9AC5",
            outline="#FFFFFF",
            width=5
        )


        # ----------------------------------------------------
        # Fonts
        # ----------------------------------------------------

        try:

            title_font = ImageFont.truetype(
                "arialbd.ttf",
                58
            )

            subtitle_font = ImageFont.truetype(
                "arial.ttf",
                22
            )

        except:

            title_font = ImageFont.load_default()

            subtitle_font = ImageFont.load_default()


        # ----------------------------------------------------
        # Company Name
        # ----------------------------------------------------

        draw.text(
            (300, 55),
            "Nassau Candy Distributor",
            fill="#3B2020",
            font=title_font
        )


        draw.text(
            (400, 135),
            "Sweet Products | Stronger Business | Sweeter Insights",
            fill="#8A6A60",
            font=subtitle_font
        )


        image.save(
            HEADER_IMAGE
        )

    except Exception:

        # If Pillow is unavailable,
        # dashboard will use text fallback.
        pass


create_header_image()


# ============================================================
# COLORS
# ============================================================

NAVY = "#182235"
PINK = "#E76F86"
BROWN = "#8B5A3C"
TEXT = "#273142"
BORDER = "#E4E7EC"


# ============================================================
# DASHBOARD CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       MAIN PAGE
       ====================================================== */

    .stApp {{
        background-color: #F7F8FA;
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 2rem;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {{
        background-color: {NAVY};
        min-width: 250px;
        max-width: 250px;
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    [data-testid="stSidebar"] label {{
        color: white !important;
        font-size: 12px !important;
    }}

    [data-testid="stSidebar"] input {{
        background-color: white !important;
        color: #222222 !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] {{
        background-color: white !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: #222222 !important;
    }}


    /* ======================================================
       TITLE
       ====================================================== */

    .dashboard-title {{
        font-size: 27px;
        font-weight: 700;
        color: {TEXT};
        margin-top: 5px;
        margin-bottom: 3px;
    }}

    .dashboard-subtitle {{
        font-size: 12px;
        color: #8A8F98;
        margin-bottom: 15px;
    }}


    /* ======================================================
       SECTION HEADER
       ====================================================== */

    .section-header {{
        background-color: white;
        border: 1px solid {BORDER};
        border-left: 5px solid {PINK};
        border-radius: 7px;
        padding: 10px 14px;
        margin-top: 18px;
        margin-bottom: 14px;
        font-size: 17px;
        font-weight: 700;
        color: {TEXT};
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}


    /* ======================================================
       SUB HEADINGS
       ====================================================== */

    .sub-heading {{
        font-size: 13px;
        font-weight: 600;
        color: #3D4655;
        margin-bottom: 6px;
    }}


    /* ======================================================
       KPI CARDS
       ====================================================== */

    [data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid {BORDER};
        border-radius: 9px;
        padding: 14px 16px;
        min-height: 82px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}

    [data-testid="stMetricLabel"] {{
        color: #777777 !important;
        font-size: 11px !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {TEXT} !important;
        font-size: 23px !important;
        font-weight: 700 !important;
    }}


    /* ======================================================
       CHART CARD
       ====================================================== */

    .chart-card {{
        background-color: white;
        border: 1px solid {BORDER};
        border-radius: 9px;
        padding: 8px 10px 2px 10px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}


    /* ======================================================
       DEPENDENCY CARDS
       ====================================================== */

    .dependency-card {{
        background-color: white;
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 13px 16px;
        margin-bottom: 12px;
    }}

    .dependency-label {{
        font-size: 11px;
        color: #777777;
    }}

    .dependency-value {{
        font-size: 22px;
        font-weight: 700;
        color: {TEXT};
        margin-top: 4px;
    }}


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {{
        text-align: center;
        color: #999999;
        font-size: 11px;
        padding: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

try:

    data = pd.read_csv(
        DATA_PATH
    )

except FileNotFoundError:

    st.error(
        "Nassau_Candy_Processed.csv was not found."
    )

    st.info(
        "Please check this location:\n\n"
        r"D:\Nassau Candy Distributor  Project\02_Streamlit_Dashboard\Nassau_Candy_Processed.csv"
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

data["Order Date"] = pd.to_datetime(
    data["Order Date"],
    dayfirst=True,
    errors="coerce"
)


numeric_columns = [
    "Sales",
    "Gross Profit",
    "Cost",
    "Units"
]


for column in numeric_columns:

    if column in data.columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )


# ============================================================
# CALCULATED COLUMNS
# ============================================================

if "Gross Margin (%)" not in data.columns:

    data["Gross Margin (%)"] = (
        data["Gross Profit"]
        /
        data["Sales"].replace(0, pd.NA)
    ) * 100


if "Profit per Unit" not in data.columns:

    data["Profit per Unit"] = (
        data["Gross Profit"]
        /
        data["Units"].replace(0, pd.NA)
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:17px;
            font-weight:700;
            padding-bottom:12px;
            margin-bottom:18px;
            border-bottom:1px solid #4B5568;
        ">
        Dashboard Filters
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    valid_dates = data[
        "Order Date"
    ].dropna()


    if valid_dates.empty:

        st.error(
            "No valid Order Date values found."
        )

        st.stop()


    min_date = valid_dates.min().date()

    max_date = valid_dates.max().date()


    date_range = st.date_input(
        "Date Range",
        value=(
            min_date,
            max_date
        ),
        min_value=min_date,
        max_value=max_date
    )


    if len(date_range) == 2:

        start_date = pd.to_datetime(
            date_range[0]
        )

        end_date = pd.to_datetime(
            date_range[1]
        )

    else:

        start_date = pd.to_datetime(
            min_date
        )

        end_date = pd.to_datetime(
            max_date
        )


    # --------------------------------------------------------
    # DIVISION
    # --------------------------------------------------------

    divisions = sorted(
        data["Division"]
        .dropna()
        .unique()
    )


    selected_divisions = st.multiselect(
        "Division",
        divisions,
        default=divisions
    )


    # --------------------------------------------------------
    # MARGIN THRESHOLD
    # --------------------------------------------------------

    margin_threshold = st.slider(
        "Margin Threshold (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )


    # --------------------------------------------------------
    # PRODUCT SEARCH
    # --------------------------------------------------------

    product_search = st.text_input(
        "Product Search",
        placeholder="Search product..."
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_data = data[
    (data["Order Date"] >= start_date)
    &
    (data["Order Date"] <= end_date)
    &
    (data["Division"].isin(selected_divisions))
].copy()


if product_search:

    filtered_data = filtered_data[
        filtered_data["Product Name"]
        .astype(str)
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]


if filtered_data.empty:

    st.warning(
        "No data available for the selected filters."
    )

    st.stop()


# ============================================================
# COMPANY HEADER
# ============================================================

if HEADER_IMAGE.exists():

    st.image(
        str(HEADER_IMAGE),
        use_container_width=True
    )

else:

    st.markdown(
        """
        <div style="
            background:#FFF4F1;
            border:1px solid #E8D6D0;
            border-radius:12px;
            padding:22px;
            margin-bottom:15px;
        ">

            <div style="
                font-size:30px;
                font-weight:700;
                color:#3B2020;
            ">
                Nassau Candy Distributor
            </div>

            <div style="
                font-size:13px;
                color:#8A6A60;
            ">
                Sweet Products | Stronger Business | Sweeter Insights
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.markdown(
    """
    <div class="dashboard-title">
        Product Line Profitability & Margin Performance Analysis
    </div>

    <div class="dashboard-subtitle">
        Nassau Candy Distributor |
        Profitability & Margin Performance Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    """
    <div class="section-header">
        Executive Summary
    </div>
    """,
    unsafe_allow_html=True
)


total_sales = filtered_data[
    "Sales"
].sum()


total_profit = filtered_data[
    "Gross Profit"
].sum()


total_units = filtered_data[
    "Units"
].sum()


overall_margin = (

    total_profit
    /
    total_sales
    *
    100

    if total_sales != 0

    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Sales",
        f"₹{total_sales:,.2f}"
    )


with col2:

    st.metric(
        "Gross Profit",
        f"₹{total_profit:,.2f}"
    )


with col3:

    st.metric(
        "Total Units",
        f"{total_units:,.0f}"
    )


with col4:

    st.metric(
        "Gross Margin",
        f"{overall_margin:.2f}%"
    )


# ============================================================
# MODULE 1
# PRODUCT PROFITABILITY
# ============================================================

st.markdown(
    """
    <div class="section-header">
        🍬 1. Product Profitability Overview
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# PRODUCT MARGIN
# ------------------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="sub-heading">
        Product-Level Margin Leaderboard
        </div>
        """,
        unsafe_allow_html=True
    )


    product_margin = (

        filtered_data

        .groupby(
            "Product Name"
        )

        .agg(
            Sales=("Sales", "sum"),
            Gross_Profit=(
                "Gross Profit",
                "sum"
            ),
            Margin=(
                "Gross Margin (%)",
                "mean"
            )
        )

        .reset_index()

        .sort_values(
            "Margin",
            ascending=False
        )
    )


    fig_margin = px.bar(
        product_margin,
        x="Margin",
        y="Product Name",
        orientation="h",
        title="Product Gross Margin (%)",
        labels={
            "Margin": "Gross Margin (%)",
            "Product Name": "Product"
        }
    )


    fig_margin.update_layout(
        height=480,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        yaxis={
            "categoryorder":
                "total ascending"
        }
    )


    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_margin,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# PROFIT CONTRIBUTION
# ------------------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="sub-heading">
        Profit Contribution by Product
        </div>
        """,
        unsafe_allow_html=True
    )


    profit_contribution = (

        filtered_data

        .groupby(
            "Product Name"
        )["Gross Profit"]

        .sum()

        .sort_values(
            ascending=False
        )

        .reset_index()
    )


    profit_total = (
        profit_contribution[
            "Gross Profit"
        ].sum()
    )


    if profit_total != 0:

        profit_contribution[
            "Profit Contribution (%)"
        ] = (

            profit_contribution[
                "Gross Profit"
            ]
            /
            profit_total
            *
            100
        )

    else:

        profit_contribution[
            "Profit Contribution (%)"
        ] = 0


    fig_profit = px.bar(
        profit_contribution,
        x="Product Name",
        y="Profit Contribution (%)",
        title="Product Contribution to Total Profit",
        labels={
            "Profit Contribution (%)":
                "Profit Contribution (%)",
            "Product Name":
                "Product"
        }
    )


    fig_profit.update_layout(
        height=480,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=90
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_tickangle=-45
    )


    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MODULE 2
# DIVISION PERFORMANCE
# ============================================================

st.markdown(
    """
    <div class="section-header">
        📊 2. Division Performance Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# REVENUE VS PROFIT
# ------------------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="sub-heading">
        Revenue vs Profit by Division
        </div>
        """,
        unsafe_allow_html=True
    )


    division_performance = (

        filtered_data

        .groupby(
            "Division"
        )

        .agg(
            Sales=("Sales", "sum"),
            Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )

        .reset_index()
    )


    division_long = (
        division_performance
        .melt(
            id_vars="Division",
            value_vars=[
                "Sales",
                "Gross_Profit"
            ],
            var_name="Measure",
            value_name="Amount"
        )
    )


    fig_division = px.bar(
        division_long,
        x="Division",
        y="Amount",
        color="Measure",
        barmode="group",
        title="Revenue vs Gross Profit by Division"
    )


    fig_division.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=20
        )
    )


    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_division,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# MARGIN DISTRIBUTION
# ------------------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="sub-heading">
        Margin Distribution by Division
        </div>
        """,
        unsafe_allow_html=True
    )


    fig_division_margin = px.box(
        filtered_data,
        x="Division",
        y="Gross Margin (%)",
        title="Margin Distribution by Division"
    )


    fig_division_margin.add_hline(
        y=margin_threshold,
        line_dash="dash",
        annotation_text=(
            f"Threshold: "
            f"{margin_threshold}%"
        )
    )


    fig_division_margin.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=20
        )
    )


    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_division_margin,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MODULE 3
# COST VS MARGIN
# ============================================================

st.markdown(
    """
    <div class="section-header">
        ⚙️ 3. Cost vs Margin Diagnostics
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# COST VS SALES
# ------------------------------------------------------------

st.markdown(
    """
    <div class="sub-heading">
    Cost vs Sales
    </div>
    """,
    unsafe_allow_html=True
)


scatter_data = filtered_data[
    [
        "Product Name",
        "Cost",
        "Sales",
        "Gross Margin (%)"
    ]
].copy()


scatter_data["Cost"] = pd.to_numeric(
    scatter_data["Cost"],
    errors="coerce"
)


scatter_data["Sales"] = pd.to_numeric(
    scatter_data["Sales"],
    errors="coerce"
)


scatter_data["Gross Margin (%)"] = pd.to_numeric(
    scatter_data["Gross Margin (%)"],
    errors="coerce"
)


scatter_data = scatter_data.dropna(
    subset=[
        "Cost",
        "Sales",
        "Gross Margin (%)"
    ]
)


fig_scatter = px.scatter(
    scatter_data,
    x="Cost",
    y="Sales",
    size="Gross Margin (%)",
    hover_name="Product Name",
    hover_data=[
        "Gross Margin (%)"
    ],
    title="Cost vs Sales by Product"
)


fig_scatter.update_layout(
    height=430,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(
        l=10,
        r=10,
        t=50,
        b=20
    )
)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# MARGIN RISK FLAGS
# ------------------------------------------------------------

st.markdown(
    """
    <div class="sub-heading">
    Margin Risk Flags
    </div>
    """,
    unsafe_allow_html=True
)


risk_data = (

    filtered_data

    .groupby(
        "Product Name"
    )

    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=(
            "Gross Profit",
            "sum"
        ),
        Cost=("Cost", "mean"),
        Margin=(
            "Gross Margin (%)",
            "mean"
        )
    )

    .reset_index()
)


risk_data["Risk Flag"] = (
    risk_data["Margin"]
    .apply(
        lambda margin:

        "⚠️ Below Threshold"

        if margin < margin_threshold

        else "✅ Healthy"
    )
)


risk_data = risk_data.sort_values(
    "Margin",
    ascending=True
)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)


st.dataframe(
    risk_data[
        [
            "Product Name",
            "Sales",
            "Gross_Profit",
            "Cost",
            "Margin",
            "Risk Flag"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={

        "Sales":
            st.column_config.NumberColumn(
                "Sales",
                format="₹%.2f"
            ),

        "Gross_Profit":
            st.column_config.NumberColumn(
                "Gross Profit",
                format="₹%.2f"
            ),

        "Cost":
            st.column_config.NumberColumn(
                "Cost",
                format="₹%.2f"
            ),

        "Margin":
            st.column_config.NumberColumn(
                "Margin",
                format="%.2f%%"
            )
    }
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MODULE 4
# PROFIT CONCENTRATION
# ============================================================

st.markdown(
    """
    <div class="section-header">
        📈 4. Profit Concentration Analysis
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# REVENUE PARETO
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
    Revenue Pareto
    </div>
    """,
    unsafe_allow_html=True
)


revenue_pareto = (

    filtered_data

    .groupby(
        "Product Name"
    )["Sales"]

    .sum()

    .sort_values(
        ascending=False
    )

    .reset_index()
)


revenue_total = (
    revenue_pareto["Sales"].sum()
)


if revenue_total != 0:

    revenue_pareto[
        "Cumulative Sales (%)"
    ] = (

        revenue_pareto[
            "Sales"
        ].cumsum()
        /
        revenue_total
        *
        100
    )

else:

    revenue_pareto[
        "Cumulative Sales (%)"
    ] = 0


fig_revenue = px.bar(
    revenue_pareto,
    x="Product Name",
    y="Sales",
    title="Revenue Pareto by Product"
)


fig_revenue.add_scatter(
    x=revenue_pareto[
        "Product Name"
    ],
    y=revenue_pareto[
        "Cumulative Sales (%)"
    ],
    name="Cumulative %",
    yaxis="y2",
    mode="lines+markers"
)


fig_revenue.add_hline(
    y=80,
    line_dash="dot",
    annotation_text="80%"
)


fig_revenue.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(
        l=10,
        r=10,
        t=50,
        b=90
    ),
    xaxis_tickangle=-45,
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        range=[0, 110]
    )
)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# REVENUE DEPENDENCY
# ============================================================



total_revenue_products = len(
    revenue_pareto
)


if total_revenue_products > 0:

    products_to_80_revenue = int(

        (
            revenue_pareto[
                "Cumulative Sales (%)"
            ] < 80
        ).sum()

        + 1
    )


    products_to_80_revenue = min(
        products_to_80_revenue,
        total_revenue_products
    )


    revenue_dependency = (
        products_to_80_revenue
        /
        total_revenue_products
        *
        100
    )

else:

    products_to_80_revenue = 0

    revenue_dependency = 0


col1, col2 = st.columns(2)






# ============================================================
# PROFIT PARETO
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
    Profit Pareto
    </div>
    """,
    unsafe_allow_html=True
)


profit_pareto = (

    filtered_data

    .groupby(
        "Product Name"
    )["Gross Profit"]

    .sum()

    .sort_values(
        ascending=False
    )

    .reset_index()
)


profit_total = (
    profit_pareto[
        "Gross Profit"
    ].sum()
)


if profit_total != 0:

    profit_pareto[
        "Cumulative Profit (%)"
    ] = (

        profit_pareto[
            "Gross Profit"
        ].cumsum()
        /
        profit_total
        *
        100
    )

else:

    profit_pareto[
        "Cumulative Profit (%)"
    ] = 0


fig_profit_pareto = px.bar(
    profit_pareto,
    x="Product Name",
    y="Gross Profit",
    title="Profit Pareto by Product"
)


fig_profit_pareto.add_scatter(
    x=profit_pareto[
        "Product Name"
    ],
    y=profit_pareto[
        "Cumulative Profit (%)"
    ],
    name="Cumulative %",
    yaxis="y2",
    mode="lines+markers"
)


fig_profit_pareto.add_hline(
    y=80,
    line_dash="dot",
    annotation_text="80%"
)


fig_profit_pareto.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(
        l=10,
        r=10,
        t=50,
        b=90
    ),
    xaxis_tickangle=-45,
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        range=[0, 110]
    )
)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)

st.plotly_chart(
    fig_profit_pareto,
    use_container_width=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)



# ============================================================
# # ============================================================
# PROFIT DEPENDENCY
# ============================================================

st.markdown(
    "### Profit Dependency"
)

total_profit_products = len(profit_pareto)

if total_profit_products > 0:

    products_to_80_profit = int(
        (
            profit_pareto[
                "Cumulative Profit (%)"
            ] < 80
        ).sum() + 1
    )

    products_to_80_profit = min(
        products_to_80_profit,
        total_profit_products
    )

    profit_dependency = (
        products_to_80_profit
        /
        total_profit_products
        *
        100
    )

    # Products contributing to approximately 80% of profit
    profit_dependency_products = profit_pareto[
        "Product Name"
    ].head(
        products_to_80_profit
    ).tolist()

else:

    products_to_80_profit = 0
    profit_dependency = 0
    profit_dependency_products = []


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Products Needed for 80% Profit",
        products_to_80_profit
    )

with col2:

    st.metric(
        "Profit Dependency",
        f"{profit_dependency:.2f}%"
    )


# Show product names
if profit_dependency_products:

    st.info(
        "**Products contributing to approximately 80% of profit:**\n\n"
        + "\n".join(
            [
                f"{i+1}. {product}"
                for i, product in enumerate(
                    profit_dependency_products
                )
            ]
        )
    )


# ============================================================
# REVENUE DEPENDENCY
# ============================================================

st.markdown(
    "### Revenue Dependency"
)

total_revenue_products = len(revenue_pareto)

if total_revenue_products > 0:

    products_to_80_revenue = int(
        (
            revenue_pareto[
                "Cumulative Sales (%)"
            ] < 80
        ).sum() + 1
    )

    products_to_80_revenue = min(
        products_to_80_revenue,
        total_revenue_products
    )

    revenue_dependency = (
        products_to_80_revenue
        /
        total_revenue_products
        *
        100
    )

    # Products contributing to approximately 80% of revenue
    revenue_dependency_products = revenue_pareto[
        "Product Name"
    ].head(
        products_to_80_revenue
    ).tolist()

else:

    products_to_80_revenue = 0
    revenue_dependency = 0
    revenue_dependency_products = []


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Products Needed for 80% Revenue",
        products_to_80_revenue
    )

with col2:

    st.metric(
        "Revenue Dependency",
        f"{revenue_dependency:.2f}%"
    )


# Show product names
if revenue_dependency_products:

    st.info(
        "**Products contributing to approximately 80% of revenue:**\n\n"
        + "\n".join(
            [
                f"{i+1}. {product}"
                for i, product in enumerate(
                    revenue_dependency_products
                )
            ]
        )
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Nassau Candy Distributor |
        Product Line Profitability & Margin Performance Analysis
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# BUSINESS QUESTIONS & ANSWERS
# ============================================================

st.markdown(
    """
    <div class="section-header">
        🎯 Business Questions & Answers
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "The following questions address the key business problems identified "
    "in the profitability analysis."
)


# ============================================================
# BUSINESS QUESTION 1
# WHICH PRODUCT LINES DELIVER THE HIGHEST GROSS MARGIN?
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
        1. Which product lines deliver the highest gross margin?
    </div>
    """,
    unsafe_allow_html=True
)

product_question = (
    filtered_data
    .groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Margin=("Gross Margin (%)", "mean")
    )
    .reset_index()
    .sort_values("Margin", ascending=False)
)

if not product_question.empty:

    top_margin_product = product_question.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Margin Product",
            top_margin_product["Product Name"]
        )

    with col2:
        st.metric(
            "Gross Margin",
            f"{top_margin_product['Margin']:.2f}%"
        )

    with col3:
        st.metric(
            "Gross Profit",
            f"₹{top_margin_product['Gross_Profit']:,.2f}"
        )

    st.success(
        f"Answer: **{top_margin_product['Product Name']}** has the "
        f"highest average gross margin of **{top_margin_product['Margin']:.2f}%** "
        f"among the products currently selected."
    )

# ============================================================
# BUSINESS QUESTION 2
# ARE HIGH-SALES PRODUCTS ACTUALLY PROFITABLE?
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
        2. Are high-sales products actually profitable?
    </div>
    """,
    unsafe_allow_html=True
)

sales_analysis = (
    filtered_data
    .groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Margin=("Gross Margin (%)", "mean")
    )
    .reset_index()
)

if not sales_analysis.empty:

    # Top 25% sales products
    sales_cutoff = sales_analysis["Sales"].quantile(0.75)

    high_sales_products = sales_analysis[
        sales_analysis["Sales"] >= sales_cutoff
    ].copy()

    # Sort by sales
    high_sales_products = high_sales_products.sort_values(
        "Sales",
        ascending=False
    )

    # High-sales products below selected margin threshold
    high_sales_low_margin = high_sales_products[
        high_sales_products["Margin"] < margin_threshold
    ].copy()

    total_high_sales = len(high_sales_products)
    risk_high_sales = len(high_sales_low_margin)

    if total_high_sales > 0:
        risk_percentage = (
            risk_high_sales /
            total_high_sales *
            100
        )
    else:
        risk_percentage = 0

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High-Sales Products",
            total_high_sales
        )

    with col2:
        st.metric(
            "High-Sales / Low-Margin",
            risk_high_sales
        )

    with col3:
        st.metric(
            "Requiring Margin Review",
            f"{risk_percentage:.1f}%"
        )

    # --------------------------------------------------------
    # PRODUCT NAMES
    # --------------------------------------------------------

    st.markdown(
        "**High-Sales Products:**"
    )

    for i, row in high_sales_products.iterrows():

        st.write(
            f"• **{row['Product Name']}** — "
            f"Sales: ₹{row['Sales']:,.2f} | "
            f"Margin: {row['Margin']:.2f}%"
        )

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    if risk_high_sales > 0:

        risk_products = ", ".join(
            high_sales_low_margin["Product Name"].tolist()
        )

        st.warning(
            f"**Answer:** Not all high-sales products are highly profitable. "
            f"{risk_high_sales} high-sales product(s) are below the selected "
            f"{margin_threshold}% margin threshold."
        )

        st.markdown(
            f"**Products requiring margin review:** "
            f"{risk_products}"
        )

    else:

        st.success(
            f"**Answer:** All {total_high_sales} high-sales products "
            f"are currently above the selected "
            f"{margin_threshold}% margin threshold."
        )

        st.markdown(
            "**High-sales products with no margin risk:**"
        )

        for product in high_sales_products["Product Name"]:
            st.write(f"• {product}")
            
# ============================================================
# BUSINESS QUESTION 3
# HOW DOES PROFITABILITY VARY ACROSS PRODUCT DIVISIONS?
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
        3. How does profitability vary across product divisions?
    </div>
    """,
    unsafe_allow_html=True
)

division_question = (
    filtered_data
    .groupby("Division")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Margin=("Gross Margin (%)", "mean")
    )
    .reset_index()
)

if not division_question.empty:

    highest_profit_division = division_question.loc[
        division_question["Gross_Profit"].idxmax()
    ]

    highest_margin_division = division_question.loc[
        division_question["Margin"].idxmax()
    ]

    lowest_margin_division = division_question.loc[
        division_question["Margin"].idxmin()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Profit Division",
            highest_profit_division["Division"],
            f"₹{highest_profit_division['Gross_Profit']:,.2f}"
        )

    with col2:
        st.metric(
            "Highest Margin Division",
            highest_margin_division["Division"],
            f"{highest_margin_division['Margin']:.2f}%"
        )

    with col3:
        st.metric(
            "Lowest Margin Division",
            lowest_margin_division["Division"],
            f"{lowest_margin_division['Margin']:.2f}%"
        )

    st.info(
        f"Answer: **{highest_profit_division['Division']}** generates the "
        f"highest gross profit, while **{lowest_margin_division['Division']}** "
        f"has the lowest average margin and may require closer profitability review."
    )


# ============================================================
# BUSINESS QUESTION 4
# WHICH PRODUCTS REPRESENT MARGIN RISK?
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
        4. Which products represent margin risk?
    </div>
    """,
    unsafe_allow_html=True
)

margin_risk_analysis = (
    filtered_data
    .groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "mean"),
        Margin=("Gross Margin (%)", "mean")
    )
    .reset_index()
)

if not margin_risk_analysis.empty:

    # Products below selected margin threshold
    margin_risk = margin_risk_analysis[
        margin_risk_analysis["Margin"] < margin_threshold
    ].copy()

    margin_risk = margin_risk.sort_values(
        "Margin",
        ascending=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Products Below Threshold",
            len(margin_risk)
        )

    with col2:
        if not margin_risk.empty:
            highest_risk_product = margin_risk.iloc[0]

            st.metric(
                "Lowest Margin Product",
                highest_risk_product["Product Name"]
            )
        else:
            st.metric(
                "Lowest Margin Product",
                "None"
            )

    with col3:
        if not margin_risk.empty:
            st.metric(
                "Lowest Margin",
                f"{margin_risk.iloc[0]['Margin']:.2f}%"
            )
        else:
            st.metric(
                "Lowest Margin",
                "—"
            )

    if not margin_risk.empty:

        risk_products = ", ".join(
            margin_risk["Product Name"]
            .head(6)
            .tolist()
        )

        st.error(
            f"Answer: **{len(margin_risk)} product(s)** fall below the "
            f"selected {margin_threshold}% margin threshold. "
            f"Products requiring attention include: **{risk_products}**. "
            f"These products may require pricing, sourcing, or cost review."
        )

    else:

        st.success(
            f"Answer: No products fall below the selected "
            f"{margin_threshold}% margin threshold."
        )


# ============================================================
# BUSINESS QUESTION SUMMARY
# ============================================================

st.markdown(
    """
    <div class="sub-heading">
        Management Interpretation
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "These four questions connect the dashboard directly to the business "
    "problem: identifying profitable products, testing whether sales translate "
    "into profitability, comparing divisions, and highlighting potential "
    "margin-risk products."
)