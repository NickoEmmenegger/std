import pandas as pd
from PIL import Image
import streamlit as st
import plotly.express as px
from streamlit.components.v1 import html

# Function to create Plotly line plot for spending trends
def plot_spending_trends(data, league):
    fig = px.line(data, x='season', y='total_spending', title=f"Spending Trend in {league.capitalize()}", labels={'total_spending': 'Total Spending (in Million €)'})
    st.plotly_chart(fig, use_container_width=True)

# Function to create interactive scatter plot for transfers over €50 million
def plot_high_value_transfers(data):
    filtered_data = data[data['fee_cleaned'] > 50]
    fig = px.scatter(filtered_data, x='season', y='fee_cleaned', color='league_name', hover_data=['player_name'], title="Player Transfers Over 50 Million €")
    st.plotly_chart(fig, use_container_width=True)

# Function to load and prepare data
def load_data():
    # Load datasets for each league
    # Adjust file paths as needed
    bundesliga_df = pd.read_csv('data/1-bundesliga.csv')
    premier_league_df = pd.read_csv('data/premier-league.csv')
    primera_division_df = pd.read_csv('data/primera-division.csv')
    ligue_1_df = pd.read_csv('data/ligue-1.csv')
    serie_a_df = pd.read_csv('data/serie-a.csv')

    # Combine datasets into a single dataframe and rename columns
    combined_df = pd.concat([bundesliga_df, premier_league_df, primera_division_df, ligue_1_df, serie_a_df], ignore_index=True)
    combined_df.rename(columns={'fee_cleaned': 'Transfer Fee in Millions', 'league_name': 'League Name', 'club_name': 'Club Name'}, inplace=True)
    return combined_df

# Load data
combined_transfers = load_data()

# App title
st.title('The Financial Dynamics of European Football\'s Elite Leagues')

# Introduction to Football Transfer Market
st.header("Introduction to the Football Transfer Market")
st.markdown("""
    The world of European football is not just a sporting arena but also a financial juggernaut. The transfer market, in particular, showcases the economic prowess of football clubs, highlighting a complex web of negotiations, strategic investments, and financial gambits. At the heart of this market are the top European leagues – the Premier League, La Liga (Primera División), Bundesliga, Serie A, and Ligue 1. These leagues are not just football competitions; they are economic ecosystems that drive the global football economy. The flow of money in the form of transfer fees reveals a landscape where clubs vie for glory, both on and off the field. This story explores the intricacies of the transfer market, delving into the spending patterns, the valuation of player skills, and how financial strategies shape the competitive landscape of European football.
""", unsafe_allow_html=True)

# Interactive Timespan Slider for Overall Analysis
st.header("Select Timespan for Overall Analysis")
overall_min_year, overall_max_year = combined_transfers['year'].min(), combined_transfers['year'].max()
overall_selected_years = st.slider("Overall Analysis Timespan", overall_min_year, overall_max_year, (overall_min_year, overall_max_year))
# Filter data based on selected timespan for overall analysis
overall_filtered_transfers = combined_transfers[(combined_transfers['year'] >= overall_selected_years[0]) & (combined_transfers['year'] <= overall_selected_years[1])]

# League-Wise Spending Overview
st.header("League-Wise Spending Overview")
st.markdown("""
    The financial might of European football leagues is evident in their spending patterns. Here we compare the total spending of different leagues within the selected timespan.
""")
league_spending = overall_filtered_transfers[overall_filtered_transfers['transfer_movement'] == 'in'].groupby('League Name')['Transfer Fee in Millions'].sum().reset_index().sort_values(by='Transfer Fee in Millions', ascending=False)
fig = px.bar(league_spending, x='League Name', y='Transfer Fee in Millions', title='Total Spending per League (in Million €)')
st.plotly_chart(fig)

# Top 5 Earning Clubs in Each League
st.header("Top 5 Earning Clubs in Each League")
st.markdown("""
    [Text about top 5 earning clubs in each league.]
""")
top_earning_clubs = overall_filtered_transfers[overall_filtered_transfers['transfer_movement'] == 'out'].groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_earning_clubs_per_league = top_earning_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_earning_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Earning Clubs in Each League (in Million €)')
st.plotly_chart(fig)

# Club-Level Spending Analysis
st.header("Club-Level Spending Analysis")
st.markdown("""
    Analyzing the spending of individual clubs offers insights into their financial strategies. Here are the top 5 spending clubs in each league.
""")
top_clubs = overall_filtered_transfers.groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_clubs_per_league = top_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Spending Clubs in Each League (in Million €)')
st.plotly_chart(fig)

# High-Value Player Transfer Trends
st.header("High-Value Player Transfer Trends")
st.markdown("""
    High-value player transfers, often exceeding 50 million euros, are key indicators of a club's financial strength and strategic ambitions.
""")
high_value_transfers = overall_filtered_transfers[overall_filtered_transfers['Transfer Fee in Millions'] > 50].sort_values(by='season')
fig = px.scatter(high_value_transfers, x='season', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name', 'Club Name'], title='High-Value Player Transfer Trends (Transfers Over 50 Million €)')
st.plotly_chart(fig)

# Age vs Transfer Fee Analysis for High-Value Players
st.header("Age vs Transfer Fee Analysis for High-Value Players")
st.markdown("""
    The correlation between a player's age and their transfer fee is particularly pronounced in high-value transfers. This plot focuses on transfers exceeding 50 million euros.
""")
fig = px.scatter(high_value_transfers, x='age', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name', 'Club Name'], title='Age vs Transfer Fee for High-Value Players (Transfers Over 50 Million €)')
st.plotly_chart(fig)

# Spending by Player Position for High-Value Players
st.header("Spending by Player Position for High-Value Players")
st.markdown("""
    Different positions command varying transfer fees. This analysis focuses on high-value transfers (over 50 million euros) and explores spending by player position.
""")
position_order = ['Goalkeeper', 'Defence', 'Right-Back', 'Centre-Back', 'Left-Back', 'Midfield', 'Defensive Midfield', 'Right Midfield', 'Central Midfield', 'Left Midfield', 'Attacking Midfield', 'Attack', 'Right Winger', 'Left Winger', 'Centre-Forward', 'Second Striker']
fig = px.scatter(high_value_transfers, x='position', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name'], title='Spending by Player Position for High-Value Players (Transfers Over 50 Million €)', category_orders={"position": position_order})
st.plotly_chart(fig)

# Conclusion
st.header("Conclusion: The Economic Powerhouses of Football")
st.markdown("""
    This exploration into the economic underpinnings of European football's elite leagues uncovers a world where financial muscle is as crucial as sporting talent. The staggering sums involved in high-value player transfers reflect the strategic importance clubs place on acquiring top talent. The correlation between investment in player transfers and on-field success is evident, yet it's also a landscape filled with financial risks and rewards. Clubs must navigate this complex market with a blend of financial acumen and sporting insight. The transfer market is a mirror to the broader economic health of football, where the interplay of revenue streams, market valuations, and strategic investments dictates the hierarchy of European football. Ultimately, the financial dynamics of player transfers are a key component of the modern football narrative, shaping the destiny of clubs and leagues alike.
""", unsafe_allow_html=True)

# End of Script