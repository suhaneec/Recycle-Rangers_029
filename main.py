import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import PreProcessor

# Reading the data
df = pd.read_csv("crime_district.csv")
df.drop_duplicates(inplace=True)

# Convert 'Year' column to datetime format (year only)
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year

df['STATE/UT'] = df['STATE/UT'].str.strip().str.title()
df['DISTRICT'] = df['DISTRICT'].str.strip().str.title()

# Calculate total crime
crime_columns = ['Murder', 'Assault on women', 'Kidnapping and Abduction', 
                 'Dacoity', 'Robbery', 'Arson', 'Hurt', 
                 'Prevention of atrocities (POA) Act', 
                 'Protection of Civil Rights (PCR) Act', 
                 'Other Crimes Against SCs']
df["Total Crime"] = df[crime_columns].sum(axis=1)

# Main Streamlit application
st.set_page_config(page_title="Crime Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("Crime Analysis Against Schedule Caste 🚨")
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
st.markdown("### Crime Insights Overview")
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
    barmode="group",
    labels={"Total Crime": "Total Crimes", "STATE/UT": "State/UT"},
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig1.update_layout(
    xaxis_title=dict(
        text="State/UT",  # X-axis label
        font=dict(size=16)  # Bold and large font
    ),
    yaxis_title=dict(
        text="Total Crimes",  # Y-axis label
        font=dict(size=16)  # Bold and large font
    ),
    xaxis=dict(
        tickfont=dict(size=15),  # Customizing tick labels
        tickangle=90  # Rotate the x-axis labels
    ),
    yaxis=dict(
        tickfont=dict(size=15)  # Customizing tick labels
    ),
    legend=dict(
        font=dict(size=15)  # Customizing legend font
    )
)
st.plotly_chart(fig1, use_container_width=True)
st.write("---")

# **2. select column
df['Year'] = df['Year'].astype(str)
st.subheader("🔢 Filter Data by Crime ")
num_column = st.selectbox("Select a Crime", df.select_dtypes(include=np.number).columns)

# Get the min and max values for the input
min_value = int(df[num_column].min())
max_value = int(df[num_column].max())
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
    color_discrete_sequence=px.colors.sequential.Blues_r
)
fig2.update_layout(
    xaxis=dict(
        tickmode='linear'
    )
)
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

# **4.Crime Statistics in Union Territories for the Year 
st.subheader("Crime Statistics in Union Territories")

# List of Union Territories in India
union_territories = [
    "Andaman & Nicobar Islands", "Chandigarh", "Dadra & Nagar Haveli",
    "Daman & Diu", "Lakshadweep", "Delhi", "Puducherry", "Ladakh", "Jammu & Kashmir"
]

# Filter the DataFrame for Union Territories
ut_df = df[df["STATE/UT"].isin(union_territories)]

# Group by 'STATE/UT' and sum the 'Total Crime' across all years
crime_data = ut_df.groupby("STATE/UT")["Total Crime"].sum().reset_index()

# Create the bar chart
fig3 = px.bar(
    crime_data,
    x="STATE/UT",
    y="Total Crime",
    labels={"Total Crime": "Total Crimes", "STATE/UT": "Union Territory"},
    color="Total Crime",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

# Display the chart
st.plotly_chart(fig3, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This bar chart provides a visual overview of crime data across various Union Territories for the selected year. It highlights the total crime incidents, allowing for a comparison between regions and helping identify areas with higher crime rates.
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("---")

# **5. Special Acts Analysis (POA & PCR)**
st.subheader("🛡️ Trends of Crime Under Special Acts Over the Years")

# Get the range of years for the slider
min_year = df['Year'].min()
max_year = df['Year'].max()

# Streamlit slider for year selection
selected_years = st.slider(
    "Select Year Range", min_year, max_year, (min_year, max_year), step=1
)

# Filter the data based on the selected years
df_acts_filtered = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

# Group data by Year and calculate the sum for the selected range
df_acts = df_acts_filtered.groupby("Year")[["Prevention of atrocities (POA) Act", "Protection of Civil Rights (PCR) Act"]].sum().reset_index()

fig4 = px.line(
    df_acts, x="Year", y=["Prevention of atrocities (POA) Act", "Protection of Civil Rights (PCR) Act"],
    markers=True,
    labels={"value": "Crime Counts", "Year": "Year"},
    color_discrete_map={
        "Prevention of atrocities (POA) Act": "blue",
        "Protection of Civil Rights (PCR) Act": "skyblue"
    }
)
fig4.update_layout(
    xaxis=dict(
        tickmode='linear'
    )
)


# Display the plot
st.plotly_chart(fig4, use_container_width=True)

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
# **6.Crime Categories with Highest Incident KPI**
# Create a DataFrame for the pie chart
# Sum the values from the crime columns
crime_sums = df[crime_columns].sum()
crime_sums_df = pd.DataFrame({
    'Crime Category': crime_columns,
    'Total Crimes': crime_sums
})

# Create the pie chart using plotly.express
st.subheader("PieChart of Crime Categories with Highest Incident KPI ")
fig5 = px.pie(
    crime_sums_df, 
    names='Crime Category', 
    values='Total Crimes', 
    color='Crime Category',  # Differentiates each segment by color
    color_discrete_sequence=px.colors.qualitative.Vivid
)

# Display the pie chart in Streamlit
st.plotly_chart(fig5, use_container_width=True)
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


# **7. Crime Rates by State**
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
    color_discrete_map={'Highest': '#1f77b4', 'Lowest': '#87CEFA'},
    barmode='group'
)
st.plotly_chart(fig6, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The bar graph highlights the disparity in crime rates against SCs across states, focusing on the top 5 states with the highest and lowest reported cases over the years. 
        This comparison helps to identify regions with significant issues and those with relatively fewer occurrences.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# **8. Trends of Murders and Assaults on Women by Year

st.subheader("Trends of Murders and Assaults on Women by Year")
# Calculate yearly sums
yearly_data = df.groupby('Year')[['Murder', 'Assault on women']].sum().reset_index()

# Melt the data for easier plotting
melted_data = yearly_data.melt(id_vars='Year', var_name='Crime Type', value_name='Number of Cases')

# Create line plot
fig7 = px.line(
    melted_data,
    x='Year',
    y='Number of Cases',
    color='Crime Type',
    markers=True,
)
fig7.update_layout(
    xaxis=dict(
        tickmode='linear'
    )
)
st.plotly_chart(fig7, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The line graph displays the changes in the rates of murders and assaults on women over time, 
        offering a clear comparison of these two serious crimes and showing how their occurrences have evolved over the years.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# 9. Most Common Crime by State
st.subheader("Most Common Crime In Each State")
# Calculate total crime
crime_columns = ['Murder', 'Assault on women', 'Kidnapping and Abduction', 
                 'Dacoity', 'Robbery', 'Arson', 'Hurt', 
                 'Prevention of atrocities (POA) Act', 
                 'Protection of Civil Rights (PCR) Act']
total_crime_counts = df.groupby('STATE/UT')[crime_columns].sum()
most_common_crime = total_crime_counts.idxmax(axis=1)
most_common_crime_count = total_crime_counts.max(axis=1)

most_common_df = pd.DataFrame({
    'State': most_common_crime.index,
    'Most Common Crime': most_common_crime.values,
    'Count': most_common_crime_count.values
})

fig8 = px.bar(
    most_common_df, x='State', y='Count', color='Most Common Crime',
    color_discrete_sequence=px.colors.sequential.Blues
)
fig8.update_layout(xaxis=dict(tickangle=90))
st.plotly_chart(fig8, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The bar plot visualizes the distribution of crimes reported against SCs across different states, 
        highlighting the frequency of each crime type and helping to identify patterns in the data.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# **10. Top 10 Districts with Highest Cases
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
st.subheader(f"Top 10 Districts with Highest ases of {selected_crime_type} ")

# Create a bar plot using Plotly Express
fig9 = px.bar(
    top_districts,
    x="DISTRICT",
    y=selected_crime_type,
    color="DISTRICT",
    labels={selected_crime_type: "Number of Cases", "DISTRICT": "District"},
    color_discrete_sequence=px.colors.sequential.Blues_r
)

# Display the plot in Streamlit
st.plotly_chart(fig9, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        The line chart illustrates how crime rates have fluctuated in the 10 districts with the highest occurrences over time, 
        offering insights into the patterns and trends of crime across these regions.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# **11. Heatmap of Total Crimes Against SCs by State/UT Over the Years
st.subheader("Heatmap of Total Crimes Against SCs by State/UT Over the Years")

# Create a pivot table for heatmap visualization
df['STATE/UT'] = df['STATE/UT'].str.strip().str.upper()
heatmap_data = df.pivot_table(values='Total Crimes', index='STATE/UT', columns='Year', aggfunc='sum', fill_value=0)



# Plot the heatmap using Plotly Express
fig10 = px.imshow(
    heatmap_data,
    labels=dict(x="Year", y="State/UT", color="Total Crimes"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale='YlGnBu',
)

# Update layout for better readability
fig10.update_layout(
    xaxis_title="Year",
    yaxis_title="State/UT",
    width=1000,
    height=800
)

# Display the heatmap in Streamlit
st.plotly_chart(fig10, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        Summary:
        This Heatmap illustrates the crime distribution in different States/ Union Terrirtories over the Years,
        I.E the darker the shade of blue the more occurance of crime cases in that Region & Year.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# **12. Footer Section**
st.markdown(
    """
    <footer style='text-align: center'>
    Project Code: [Recycle Rangers_029] | Data Source: [kaggle](https://www.kaggle.com/datasets/khalidative/crimeanalysis)
    
    Credits:
    This project was collaboratively developed and executed by the following team members:

    -> Suhani - Report Compilation and Final Presentation |
    -> Misba - Exploratory Data Analysis and Insights Generation |
    -> Sougata - Data Visualization and Dashboard Design | 
    -> Arpan - Data Cleaning and Preprocessing.

    </footer>
    """,
    unsafe_allow_html=True
)