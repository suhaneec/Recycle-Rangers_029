import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import PreProcessor

# Reading the datap
df = pd.read_csv("crime_district.csv")
df.drop_duplicates(inplace=True)

# Convert 'Year' column to datetime format (year only)
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year


# Calculate total crime
crime_columns = ['Murder', 'Assault on women', 'Kidnapping and Abduction', 
                 'Dacoity', 'Robbery', 'Arson', 'Hurt', 
                 'Prevention of atrocities (POA) Act', 
                 'Protection of Civil Rights (PCR) Act', 
                 'Other Crimes Against SCs']
df["Total Crime"] = df[crime_columns].sum(axis=1)

# Main Streamlit application
st.set_page_config(page_title="Crime Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")


st.title("🚨CRIME ANALYSIS AGAINST SCHEDULE CASTE")
st.subheader("Unveiling Crime Trends: A Comprehensive Analysis of Crime with SC Data Across Indian States and Districts")
st.markdown("---")

# Sidebar filters

# Add the logo to the sidebar
st.sidebar.image("logo.jpg", width = 280)
st.sidebar.title("🔍 Filters")
selected_State = PreProcessor.multiselect("Select State", df["STATE/UT"].unique())
selected_district = PreProcessor.multiselect("Select District", df["DISTRICT"].unique())
selected_year = PreProcessor.multiselect("Select Year", df["Year"].unique())
 

# Data Filtering
filter_df = df[(df["STATE/UT"].isin(selected_State)) & (df["Year"].isin(selected_year))]

# Metrics
st.markdown("### Headers")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("States/UT", filter_df["STATE/UT"].nunique())
with col2:
    st.metric("Districts", filter_df["DISTRICT"].nunique())
with col3:
    st.metric("Years Analyzed", filter_df["Year"].nunique())
with col4:
    st.metric("Total Crimes", int(filter_df["Total Crime"].sum()), "📈")

st.markdown("---")

# **1. Total Crimes by State/UT and Year**
st.subheader("📊 Total Crimes by State/UT and Year")
crime_summary = filter_df.groupby(["STATE/UT", "Year"])["Total Crime"].sum().reset_index()
fig1 = px.bar(
    crime_summary, x="STATE/UT", y="Total Crime", color="Year",
    barmode="group", title="Total Crimes by State/UT and Year",
    labels={"Total Crime": "Total Crimes", "STATE/UT": "State/UT"},
    color_discrete_sequence=px.colors.qualitative.Vivid
)
st.plotly_chart(fig1, use_container_width=True)
st.write("---")

# **2. slider column
df['Year'] = df['Year'].astype(str)
st.subheader("🔢 Filter Data by Numerical Column")
num_column = st.selectbox("Select a numerical column:", df.select_dtypes(include=np.number).columns)

# Get the min and max values for the input
min_value = float(df[num_column].min())
max_value = float(df[num_column].max())
# Number inputs for manual range selection
min_input = st.number_input(f"Enter minimum value for {num_column}:", min_value=min_value, max_value=max_value, value=min_value)
max_input = st.number_input(f"Enter maximum value for {num_column}:", min_value=min_value, max_value=max_value, value=max_value)
# Filter data based on the selected numerical column's range
filtered_data = df[(df[num_column] >= min_input) & (df[num_column] <= max_input)]
non_integer_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

columns_to_display = non_integer_columns + [num_column]

filtered_data = filtered_data[columns_to_display]
# Display the count of the index (number of rows)
st.write(f"**Number of rows after filtering:** {len(filtered_data)}")
st.write(filtered_data)

st.write("---")

# **3. Crime Trends Over Time**
df['Year'] = df['Year'].astype(int)
st.subheader("📈 Yearly Crime Analysis")
df_yearly = df.groupby('Year')['Total Crime'].sum().reset_index()
# bar plot
fig2 = px.bar(
    df_yearly, x='Year', y='Total Crime',
    labels={"Total Crime": "Total Crimes", "Year": "Year"},
    color_discrete_sequence=px.colors.qualitative.Prism
)
# Display the bar plot
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This graph highlights long-term crime trends, revealing a general increase in crime from 2001 to 2013, with a significant spike in 2013. 
        Further analysis could provide insights into the factors contributing to this trend and its broader implications on crime rates.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# **4. Special Acts Analysis (POA & PCR)**
st.subheader("🛡️ Crimes Under Special Acts Over the Years")
df_acts = df.groupby("Year")[["Prevention of atrocities (POA) Act", "Protection of Civil Rights (PCR) Act"]].sum().reset_index()
fig3 = px.line(
    df_acts, x="Year", y=["Prevention of atrocities (POA) Act", "Protection of Civil Rights (PCR) Act"],
    markers=True,
    labels={"value": "Crime Counts", "Year": "Year"},
    color_discrete_map={
        "Prevention of atrocities (POA) Act": "purple",
        "Protection of Civil Rights (PCR) Act": "skyblue"
    }
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This graph illustrates the trend in crime rates over time,showing a gradual increase from 2001 to 2013, with a notable surge in 2013.
        This pattern suggests a rising concern in crime levels, especially in the later years. Further investigation could uncover the contributing factors to this escalation and help assess the impact of various socio-economic elements on the crime rates.
    </div>
    """,
    unsafe_allow_html=True
)
            
st.write("---")


# Sum the values from the crime columns
crime_sums = df[crime_columns].sum()


# **5.Crime Categories with Highest Incident KPI**
# Create a DataFrame for the pie chart
crime_sums_df = pd.DataFrame({
    'Crime Category': crime_columns,
    'Total Crimes': crime_sums
})

# Create the pie chart using plotly.express
st.subheader("PieChart of Crime Categories with Highest Incident KPI ")
fig4 = px.pie(
    crime_sums_df, 
    names='Crime Category', 
    values='Total Crimes', 
    color='Crime Category',  # Differentiates each segment by color
    color_discrete_sequence=px.colors.qualitative.Set3_r # Color palette
)

# Display the pie chart in Streamlit
st.plotly_chart(fig4, use_container_width=True)
# Markdown text with 20px font size
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The crime categories displayed in the pie chart represent the relative frequency of each type, 
        helping us identify which crimes are most prevalent.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")


# **6. Crime Rates by State**
st.subheader("Barplot of Top 5 States with Highest and Lowest Crime Rates")
df['Total Crimes'] = df.iloc[:, 3:].sum(axis=1)  # Create a column for total crimes
state_crime_rates = df.groupby('STATE/UT')['Total Crimes'].sum()
top_5_states_highest = state_crime_rates.nlargest(5)  # Top 5 highest crime states
top_5_states_lowest = state_crime_rates.nsmallest(5)  # Top 5 lowest crime states

# Prepare the data for the plot
top_states = pd.concat([top_5_states_highest, top_5_states_lowest]).reset_index()
top_states['Crime Category'] = ['Highest'] * len(top_5_states_highest) + ['Lowest'] * len(top_5_states_lowest)
# Create the plot using plotly.express
fig6 = px.bar(
    top_states, x='STATE/UT', y='Total Crimes', color='Crime Category',
    
    labels={'Total Crimes': 'Total Crimes', 'STATE/UT': 'State/UT'},
    color_discrete_map={'Highest': '#FF6347', 'Lowest': '#00BFFF'},
    barmode='group'
)
# Display the plot
st.plotly_chart(fig6, use_container_width=True)
st.markdown("<h1 style='font-size: 20px;'>This Bar Graph show's a Comparison of Top 5 States with Highest and Lowest Crime Rates over the years against SC's </h1>", unsafe_allow_html=True)
st.write("---")

# **7. Trends of Murders and Assaults on Women by Year

st.subheader("Trends of Murders and Assaults on Women by Year")
# Calculate yearly sums
yearly_data = df.groupby('Year')[['Murder', 'Assault on women']].sum().reset_index()

# Melt the data for easier plotting
melted_data = yearly_data.melt(id_vars='Year', var_name='Crime Type', value_name='Number of Cases')

# Create line plot
fig8 = px.line(
    melted_data,
    x='Year',
    y='Number of Cases',
    color='Crime Type',
    markers=True,
)
st.plotly_chart(fig8, use_container_width=True)
st.markdown("<h1 style='font-size: 20px;'> This line Graph indicates the trends of Murder's and Assaults on Women Over the years</h1>", unsafe_allow_html=True)

st.write("---")

# 8. Most Common Crime by State
st.subheader("Most Common Crime In Each State")
# Calculate total crime
crime_columns = ['Murder', 'Assault on women', 'Kidnapping and Abduction', 
                 'Dacoity', 'Robbery', 'Arson', 'Hurt', 
                 'Prevention of atrocities (POA) Act', 
                 'Protection of Civil Rights (PCR) Act', 
                 'Other Crimes Against SCs']
total_crime_counts = df.groupby('STATE/UT')[crime_columns].sum()
most_common_crime = total_crime_counts.idxmax(axis=1)
most_common_crime_count = total_crime_counts.max(axis=1)

most_common_df = pd.DataFrame({
    'State': most_common_crime.index,
    'Most Common Crime': most_common_crime.values,
    'Count': most_common_crime_count.values
})

fig7 = px.bar(
    most_common_df, x='State', y='Count', color='Most Common Crime',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig7, use_container_width=True)
st.markdown(
    "<h3 style='font-size:20px;'>The bar plot reveals the which crime has been reported against SC's in each state, along with the number of occurrences.</h3>", 
    unsafe_allow_html=True
)

st.write("---")

# **9 Top 10 Districts with Highest Cases
# Allow user to select a crime type for analysis
selected_crime_type = st.selectbox('Choose a crime type for analysis', crime_columns)  # Using predefined crime columns list

# Filter out the 'TOTAL' row and calculate top districts
filtered_df = df[df["DISTRICT"].str.upper() != "TOTAL"]

# Group by district, sum cases, sort, and get the top 10 districts
top_districts = (filtered_df.groupby(["DISTRICT"])[selected_crime_type]
                 .sum()
                 .sort_values(ascending=False)
                 .head(10)).reset_index()

# Display the top 10 districts
st.subheader(f"Top 10 Districts with Highest {selected_crime_type} Cases")

# Create a bar plot using Plotly Express
fig = px.bar(
    top_districts,
    x="DISTRICT",
    y=selected_crime_type,
    color="DISTRICT",
    title=f"Top 10 Districts with Highest {selected_crime_type} Cases",
    labels={selected_crime_type: "Number of Cases", "DISTRICT": "District"},
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<h3 style='font-size:20px;'> The line chart illustrates trends of 10 districts with most crime occured over the years .</h3>", 
    unsafe_allow_html=True
)

st.write("---")


# **10. Footer Section**
st.markdown(
    """
    <footer style='text-align: center'>
    Project Code: [Recycle Ranger_029] | Data Source: [kaggle](https://www.kaggle.com/datasets/khalidative/crimeanalysis)
    
    Credits:
    This project was collaboratively developed and executed by the following team members:

    -> Suhani - Report Compilation and Final Presentation  ;
    -> Misba - Exploratory Data Analysis and Insights Generation  ;
    -> Sougata - Data Visualization and Dashboard Design  ;
    -> Arpan - Data Cleaning and Preprocessing  ;
    -> Ritika - Project Management and Quality Assurance  ;
    </footer>
    """,
    unsafe_allow_html=True
)
