import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Care Load & Placement Demand", page_icon="📊", layout="wide")
st.markdown("""
<style>
/* Submission styling */
h1 {color:#123B63!important; border-left:6px solid #17A2A4; padding-left:.65rem; border-bottom:2px solid #C9DFF0;}
h2 {color:#174A7E!important; border:1px solid #B9D7EF; border-left:5px solid #2585C7; padding:.45rem .7rem; border-radius:8px; background:rgba(37,133,199,.08);}
h3 {color:#146B65!important; border-left:4px solid #26A69A; padding-left:.55rem;}
div[data-testid="stMetric"] {border:1px solid #B8D6EA; border-bottom:4px solid #2585C7; border-radius:10px; padding:12px;}
div[data-testid="stExpander"] {border:1px solid #B9D7EF; border-left:4px solid #17A2A4; border-radius:9px;}

.block-container{padding-top:1.2rem}
div.stButton>button{width:100%;min-height:2.7rem;border-radius:9px;font-weight:600}
div[data-testid="stMetric"]{background:rgba(128,128,128,.07);padding:12px;border-radius:10px}
.demo{padding:12px;border:1px solid #D6A84F;border-radius:9px;background:rgba(214,168,79,.1)}
</style>""", unsafe_allow_html=True)
from pathlib import Path as _Path
_logo = _Path(__file__).resolve().parent / "hhsgov_cover.jpg"
if _logo.exists():
    st.image(str(_logo), use_container_width=True)
st.title("Care Load & Placement Demand")
st.caption("Interactive dashboard · trends · forecasting · capacity scenarios")
with st.expander("Project objectives and KPIs", expanded=True):
    st.markdown("### Project objectives")
    st.markdown("""
    - **Forecast care load:** estimate the short-term number of children in HHS care.
    - **Estimate flow imbalance:** compare expected intake/inflow with transfers and discharges to identify potential changes in care demand.
    - **Predict discharge demand:** forecast short-term discharge volumes to support planning.
    - **Provide early warnings:** highlight possible surges and capacity pressure before they occur.
    - **Quantify uncertainty:** show approximate forecast ranges and compare forecasting approaches.
    """)
    st.markdown("### Key performance indicators (KPIs)")
    kpi_cols = st.columns(3)
    kpi_cols[0].markdown("**Forecast Accuracy (%)**\\n\\nMeasures how closely predictions match observed values. This demo uses holdout error metrics as supporting evidence; accuracy is not a guarantee.")
    kpi_cols[1].markdown("**Surge Lead Time**\\n\\nThe number of days of advance notice before a defined surge threshold is reached. Requires an agreed surge definition.")
    kpi_cols[2].markdown("**Capacity Breach Probability**\\n\\nThe estimated chance that forecast care load exceeds an approved capacity threshold. The demo threshold is a scenario input.")
    kpi_cols = st.columns(2)
    kpi_cols[0].markdown("**Forecast Stability Index**\\n\\nIndicates how much forecasts vary when the data window or model changes. This prototype does not calculate a standardized stability index.")
    kpi_cols[1].markdown("**Model Robustness**\\n\\nAssesses whether model performance remains consistent across time periods and validation samples. This prototype compares simple models on one chronological holdout.")
    st.caption("KPI definitions describe the project goals. Some KPIs require agreed operational thresholds and additional validation before they can be calculated reliably.")

@st.cache_data
def demo_data():
    rng=np.random.default_rng(20261027)
    dates=pd.date_range(end=pd.Timestamp.today().normalize(),periods=1095,freq="D")
    n=len(dates); t=np.arange(n); annual=np.sin(2*np.pi*t/365.25)
    weekday=np.array([d.weekday() for d in dates])
    app=rng.poisson(np.clip(34+8*annual+2*np.sin(2*np.pi*t/90)+np.where(weekday>=5,-2,1),8,None))
    trans=rng.poisson(np.clip(31+7*annual+2*np.sin(2*np.pi*(t-5)/90),6,None))
    cbp=np.zeros(n); cbp[0]=620
    hin=rng.poisson(np.clip(24+6*annual+1.8*np.sin(2*np.pi*t/120),5,None))
    dis=rng.poisson(np.clip(22+5*annual+1.5*np.sin(2*np.pi*(t-10)/120),5,None))
    hhs=np.zeros(n); hhs[0]=1850
    for i in range(1,n):
        cbp[i]=max(80,cbp[i-1]+app[i]-trans[i]+rng.normal(0,7))
        hhs[i]=max(450,hhs[i-1]+hin[i]-dis[i]+rng.normal(0,9))
    names=["Children apprehended and placed in CBP custody","Children in CBP custody",
           "Children transferred out of CBP custody","Children in HHS Care","Children discharged from HHS Care"]
    return pd.DataFrame({"Date":dates,names[0]:app,names[1]:np.round(cbp).astype(int),
        names[2]:trans,names[3]:np.round(hhs).astype(int),names[4]:dis,
        "Simulated HHS inflow":hin})

df=demo_data()
MEASURES=list(df.columns[1:6])
SHORT={MEASURES[0]:"Apprehended / placed in CBP",MEASURES[1]:"Children in CBP custody",
       MEASURES[2]:"Transferred out of CBP",MEASURES[3]:"Children in HHS Care",
       MEASURES[4]:"Discharged from HHS Care"}
if "section" not in st.session_state: st.session_state.section="Overview"
nav=st.columns(5)
for col,key,label in zip(nav,["Overview","Trends","Forecast","Flow & Capacity","Model Performance"],
                         ["📌 Overview","📈 Trends","🔮 Forecast","🏢 Flow & Capacity","🧪 Model Performance"]):
    with col:
        if st.button(label,key="nav_"+key,type="primary" if st.session_state.section==key else "secondary"):
            st.session_state.section=key
st.divider()

with st.sidebar:
    st.header("Dashboard controls")
    st.write("No upload needed — demo data are generated automatically.")
    start=st.date_input("History start",df.Date.min().date(),min_value=df.Date.min().date(),max_value=df.Date.max().date())
    end=st.date_input("History end",df.Date.max().date(),min_value=df.Date.min().date(),max_value=df.Date.max().date())
    if start>end: st.error("Start date must be before end date."); st.stop()
    data=df[(df.Date.dt.date>=start)&(df.Date.dt.date<=end)].copy()
    smooth=st.slider("Smoothing window (days)",1,30,7)
    horizon=st.slider("Forecast horizon (days)",7,90,30)
    capacity=st.number_input("Illustrative capacity threshold",min_value=0,max_value=100000,value=2500,step=100,
        help="Scenario only. Use an approved capacity figure for real analysis.")

def plot_trend(frame,col,title,window):
    fig,ax=plt.subplots(figsize=(12,4.5))
    ax.plot(frame.Date,frame[col],alpha=.4,lw=1,label="Daily values")
    if window>1: ax.plot(frame.Date,frame[col].rolling(window,min_periods=1).mean(),lw=2,label=f"{window}-day average")
    ax.set_title(title); ax.set_xlabel("Date"); ax.set_ylabel("Children (count)")
    ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)

if data.empty: st.warning("No data in selected date range."); st.stop()
sec=st.session_state.section
if sec=="Overview":
    st.subheader("At-a-glance summary")
    c=st.columns(4)
    c[0].metric("Latest HHS care load",f"{int(data['Children in HHS Care'].iloc[-1]):,}")
    c[1].metric("Latest CBP custody",f"{int(data['Children in CBP custody'].iloc[-1]):,}")
    c[2].metric("Average daily HHS discharges",f"{data['Children discharged from HHS Care'].mean():,.1f}")
    c[3].metric("HHS load change",f"{int(data['Children in HHS Care'].iloc[-1]-data['Children in HHS Care'].iloc[0]):+,}")
    plot_trend(data,"Children in HHS Care","Children in HHS Care",smooth)
    left,right=st.columns(2)
    left.metric("Apprehended in selected period",f"{data[MEASURES[0]].sum():,}")
    left.metric("Transferred out of CBP",f"{data[MEASURES[2]].sum():,}")
    right.metric("Discharged from HHS care",f"{data[MEASURES[4]].sum():,}")
    right.metric("Highest daily discharge count",f"{data[MEASURES[4]].max():,}")

elif sec=="Trends":
    st.subheader("Explore historical trends")
    target=st.selectbox("Measure",MEASURES,index=3,format_func=lambda x:SHORT[x])
    plot_trend(data,target,SHORT[target],smooth)
    st.dataframe(data[target].describe().rename("Value").to_frame().style.format("{:,.2f}"),use_container_width=True)
    chosen=st.multiselect("Compare up to four measures",MEASURES,default=[MEASURES[1],MEASURES[3]],format_func=lambda x:SHORT[x],max_selections=4)
    if chosen:
        fig,ax=plt.subplots(figsize=(12,4.5))
        for m in chosen: ax.plot(data.Date,data[m].rolling(smooth,min_periods=1).mean(),label=SHORT[m])
        ax.set_title(f"Measure comparison ({smooth}-day average)"); ax.grid(True,alpha=.25); ax.legend()
        fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)

elif sec=="Forecast":
    st.subheader("Short-term forecast")
    target=st.selectbox("Measure to forecast",MEASURES,index=4,format_func=lambda x:SHORT[x])
    y=data[target].astype(float).to_numpy()
    if len(y)<30: st.warning("Select at least 30 days of history.")
    else:
        split=max(20,int(len(y)*.8)); x=np.arange(len(y)).reshape(-1,1)
        model=LinearRegression().fit(x[:split],y[:split]); test_pred=np.maximum(0,model.predict(x[split:]))
        mae=mean_absolute_error(y[split:],test_pred) if len(y[split:]) else float("nan")
        rmse=np.sqrt(mean_squared_error(y[split:],test_pred)) if len(y[split:]) else float("nan")
        final=LinearRegression().fit(x,y)
        fx=np.arange(len(y),len(y)+horizon).reshape(-1,1)
        forecast=np.maximum(0,.65*final.predict(fx)+.35*np.mean(y[-min(14,len(y)):]))
        residual=y[split:]-test_pred if len(y[split:])>1 else y-final.predict(x)
        spread=max(float(np.std(residual)),1.0); lower=np.maximum(0,forecast-1.96*spread); upper=forecast+1.96*spread
        dates=pd.date_range(data.Date.iloc[-1]+pd.Timedelta(days=1),periods=horizon,freq="D")
        out=pd.DataFrame({"Date":dates,"Forecast":forecast.round(1),"Lower estimate":lower.round(1),"Upper estimate":upper.round(1)})
        m=st.columns(3); m[0].metric("Holdout MAE",f"{mae:,.2f}"); m[1].metric("Holdout RMSE",f"{rmse:,.2f}"); m[2].metric("Forecast average",f"{forecast.mean():,.1f}")
        fig,ax=plt.subplots(figsize=(12,4.8)); tail=min(len(data),180)
        ax.plot(data.Date.iloc[-tail:],data[target].iloc[-tail:],label="Observed (simulated)")
        ax.plot(dates,forecast,label="Forecast",lw=2); ax.fill_between(dates,lower,upper,alpha=.2,label="Approx. prediction band")
        ax.axvline(data.Date.iloc[-1],ls="--",alpha=.6); ax.set_title(f"{SHORT[target]} — next {horizon} days")
        ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
        st.dataframe(out,use_container_width=True,hide_index=True)
        st.download_button("Download forecast table",out.to_csv(index=False).encode(),file_name="illustrative_forecast.csv",mime="text/csv")
        st.caption("Simple demo forecast; its prediction band is approximate and not an operational confidence interval.")

elif sec=="Flow & Capacity":
    st.subheader("Flow balance and capacity scenario")
    inflow=int(data["Simulated HHS inflow"].sum()); discharge=int(data[MEASURES[4]].sum())
    a=st.columns(3); a[0].metric("Simulated HHS inflow",f"{inflow:,}"); a[1].metric("HHS discharges",f"{discharge:,}"); a[2].metric("Net flow",f"{inflow-discharge:+,}")
    fig,ax=plt.subplots(figsize=(12,4.5))
    ax.plot(data.Date,data["Simulated HHS inflow"].rolling(7,min_periods=1).mean(),label="Simulated inflow (7-day avg)")
    ax.plot(data.Date,data[MEASURES[4]].rolling(7,min_periods=1).mean(),label="Discharges (7-day avg)")
    ax.set_title("Illustrative inflow versus discharges"); ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout()
    st.pyplot(fig,use_container_width=True); plt.close(fig)
    load=data[MEASURES[3]]
    if capacity>0:
        c=st.columns(3); c[0].metric("Scenario threshold",f"{capacity:,}"); c[1].metric("Days at/above threshold",f"{int((load>=capacity).sum()):,}"); c[2].metric("Latest load minus threshold",f"{int(load.iloc[-1]-capacity):+,}")
        fig,ax=plt.subplots(figsize=(12,4.5)); ax.plot(data.Date,load,label="HHS care load"); ax.axhline(capacity,ls="--",label="Scenario threshold")
        ax.set_title("Capacity threshold scenario"); ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close(fig)
    st.caption("Inflow is independently simulated and is not an official or reconciled transfer measure.")

else:
    st.subheader("Demonstration model comparison")
    target=st.selectbox("Target measure",MEASURES,index=4,format_func=lambda x:SHORT[x],key="model_target")
    y=data[target].astype(float).to_numpy()
    if len(y)<60: st.warning("Select at least 60 days for model comparison.")
    else:
        split=max(30,int(len(y)*.8)); train,test=y[:split],y[split:]
        preds={"Last-value baseline":np.repeat(train[-1],len(test)),
               "7-day moving average":np.repeat(np.mean(train[-min(7,len(train)):]),len(test))}
        lm=LinearRegression().fit(np.arange(len(train)).reshape(-1,1),train)
        preds["Linear trend"]=np.maximum(0,lm.predict(np.arange(len(train),len(train)+len(test)).reshape(-1,1)))
        result=pd.DataFrame([{"Model":k,"MAE":mean_absolute_error(test,v),"RMSE":np.sqrt(mean_squared_error(test,v))} for k,v in preds.items()]).sort_values("MAE")
        st.dataframe(result.style.format({"MAE":"{:,.2f}","RMSE":"{:,.2f}"}),use_container_width=True,hide_index=True)
        st.metric("Lowest holdout MAE",f"{result.iloc[0]['MAE']:,.2f}",help=f"Model: {result.iloc[0]['Model']}")
        st.bar_chart(result.set_index("Model")[["MAE","RMSE"]])
        st.caption("Single chronological holdout split using simulated data; not evidence of real-world model performance.")

# -------------------------- Final objective solutions and KPI scorecard --------------------------
st.divider()
st.header("Project Outcomes: Objective Solutions & KPI Scorecard")
st.write(
    "This final section translates the selected date range into decision-support findings. "
    "All calculations use the dashboard's simulated data and should be recalculated with validated historical data before operational use."
)

def forecast_series(values, horizon_days):
    values=np.asarray(values,dtype=float)
    x=np.arange(len(values)).reshape(-1,1)
    split=max(20,int(len(values)*0.8))
    split=min(split,len(values)-1)
    train_model=LinearRegression().fit(x[:split],values[:split])
    holdout_pred=np.maximum(0,train_model.predict(x[split:]))
    actual=values[split:]
    mae=mean_absolute_error(actual,holdout_pred) if len(actual) else float("nan")
    rmse=np.sqrt(mean_squared_error(actual,holdout_pred)) if len(actual) else float("nan")
    nonzero=np.abs(actual)>0
    mape=float(np.mean(np.abs((actual[nonzero]-holdout_pred[nonzero])/actual[nonzero]))*100) if nonzero.any() else float("nan")
    final_model=LinearRegression().fit(x,values)
    fx=np.arange(len(values),len(values)+horizon_days).reshape(-1,1)
    trend=final_model.predict(fx)
    recent=float(np.mean(values[-min(14,len(values)):]))
    forecast=np.maximum(0,0.65*trend+0.35*recent)
    residual=actual-holdout_pred if len(actual)>1 else values-train_model.predict(x)
    spread=max(float(np.std(residual)),1.0)
    return forecast, np.maximum(0,forecast-1.96*spread), forecast+1.96*spread, mae, rmse, mape, residual

if len(data)>=30:
    discharge_values=data["Children discharged from HHS Care"].astype(float).to_numpy()
    discharge_fc, discharge_lo, discharge_hi, discharge_mae, discharge_rmse, discharge_mape, discharge_resid = forecast_series(discharge_values,horizon)
    care_values=data["Children in HHS Care"].astype(float).to_numpy()
    care_fc, care_lo, care_hi, care_mae, care_rmse, care_mape, care_resid = forecast_series(care_values,horizon)
    future_dates=pd.date_range(data["Date"].iloc[-1]+pd.Timedelta(days=1),periods=horizon,freq="D")

    # Model robustness proxy: compare three baseline models on the same chronological holdout.
    split=max(30,int(len(discharge_values)*0.8))
    split=min(split,len(discharge_values)-1)
    train,test=discharge_values[:split],discharge_values[split:]
    holdout_x=np.arange(len(discharge_values)).reshape(-1,1)
    model_predictions={
        "Last-value baseline":np.repeat(train[-1],len(test)),
        "7-day moving average":np.repeat(np.mean(train[-min(7,len(train)):]),len(test)),
    }
    trend_model=LinearRegression().fit(np.arange(len(train)).reshape(-1,1),train)
    model_predictions["Linear trend"]=np.maximum(0,trend_model.predict(np.arange(len(train),len(train)+len(test)).reshape(-1,1)))
    model_maes=np.array([mean_absolute_error(test,pred) for pred in model_predictions.values()])
    mean_model_mae=float(np.mean(model_maes))
    robustness=float(np.clip(100*(1-np.std(model_maes)/(mean_model_mae+1e-9)),0,100))

    accuracy=float(np.clip(100-discharge_mape,0,100)) if np.isfinite(discharge_mape) else float("nan")
    stability=float(np.clip(100*(1-np.std(discharge_resid)/(np.mean(np.abs(discharge_values))+1e-9)),0,100))
    expected_breach_days=int(np.sum(care_fc>=capacity)) if capacity>0 else None
    upper_exposure_days=int(np.sum(care_hi>=capacity)) if capacity>0 else None
    crossings=np.where(care_fc>=capacity)[0] if capacity>0 else np.array([],dtype=int)
    surge_lead=int(crossings[0]+1) if len(crossings) else None

    st.subheader("KPI results")
    kpi=st.columns(5)
    kpi[0].metric("Forecast accuracy proxy",f"{accuracy:.1f}%" if np.isfinite(accuracy) else "N/A",
                  help="100 − holdout MAPE for discharge forecasts, clipped at 0%.")
    kpi[1].metric("Surge lead time",f"{surge_lead} day(s)" if surge_lead is not None else "No crossing",
                  help="First day the point forecast for HHS care load reaches the selected scenario threshold.")
    kpi[2].metric("Capacity exposure proxy",f"{(100*upper_exposure_days/horizon):.1f}%" if capacity>0 else "Set threshold",
                  help="Percentage of forecast days whose approximate upper estimate meets/exceeds the scenario threshold. This is not a calibrated breach probability.")
    kpi[3].metric("Forecast stability proxy",f"{stability:.1f}/100",
                  help="Project-defined proxy based on holdout residual variation relative to average observed discharge volume.")
    kpi[4].metric("Model robustness proxy",f"{robustness:.1f}/100",
                  help="Project-defined consistency score derived from the spread of MAE across three simple baseline models on one holdout.")

    st.subheader("Answers to the project objectives")
    latest_load=int(data["Children in HHS Care"].iloc[-1])
    latest_custody=int(data["Children in CBP custody"].iloc[-1])
    net_hhs=int(data["Simulated HHS inflow"].sum()-data["Children discharged from HHS Care"].sum())
    findings=[
        ("1. Forecast care load",
         f"The latest simulated HHS care load is {latest_load:,}. The {horizon}-day forecast averages {np.mean(care_fc):,.1f} children, with an approximate daily forecast range shown in the Forecast section."),
        ("2. Estimate flow imbalance",
         f"Across the selected period, simulated HHS inflow totals {int(data['Simulated HHS inflow'].sum()):,} and discharges total {int(data['Children discharged from HHS Care'].sum()):,}, giving a net simulated flow of {net_hhs:+,} children. This inflow is generated independently for demonstration."),
        ("3. Predict discharge demand",
         f"The forecast estimates an average of {np.mean(discharge_fc):,.1f} discharges per day over the next {horizon} days, or approximately {np.sum(discharge_fc):,.0f} discharges across the forecast horizon."),
        ("4. Provide early warnings",
         (f"The point forecast first reaches the selected capacity scenario threshold of {capacity:,} after {surge_lead} day(s)." if surge_lead is not None else
          (f"The point forecast does not reach the selected threshold of {capacity:,} during the next {horizon} days." if capacity>0 else
           "Enter a capacity threshold in the sidebar to evaluate a potential capacity warning."))),
        ("5. Quantify uncertainty and compare models",
         f"The dashboard shows approximate forecast bands and compares three simple discharge forecasting baselines. The lowest holdout MAE is {float(np.min(model_maes)):,.2f} children per day; the comparison table is available under Model Performance.")
    ]
    for title,detail in findings:
        with st.expander(title,expanded=True):
            st.write(detail)

    st.subheader("Recommended actions from this analysis")
    st.markdown("""
    1. **Capacity planning:** review the forecast and upper estimate against an approved operational capacity threshold; investigate any projected crossing.
    2. **Staffing and discharge coordination:** use the discharge forecast as a planning signal, then validate it with case-level and placement availability information.
    3. **Monitor net flow:** review periods where simulated/observed intake exceeds exits, since sustained positive net flow can increase the care load.
    4. **Validate before decisions:** replace demo data with verified daily historical observations, use chronological backtesting across multiple windows, and recalibrate forecast intervals.
    5. **Formalize KPI definitions:** agree on the surge threshold, capacity definition, target accuracy metric, and acceptance criteria with program stakeholders.
    """)
    st.caption("Interpretation note: accuracy, stability, robustness, and capacity exposure shown here are prototype indicators. Capacity exposure is not a statistically calibrated probability, and surge lead time depends on the selected threshold.")
else:
    st.info("Select at least 30 days of data in the sidebar to calculate objective outcomes and KPI proxies.")

st.divider()
st.caption("Prototype for project presentation · simulated data only · not for operational decisions.")
