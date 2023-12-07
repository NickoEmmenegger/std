import pandas as pd
import streamlit as st
import plotly.express as px

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
    bundesliga_df = pd.read_csv('data/1-bundesliga.csv')
    premier_league_df = pd.read_csv('data/premier-league.csv')
    primera_division_df = pd.read_csv('data/primera-division.csv')
    ligue_1_df = pd.read_csv('data/ligue-1.csv')
    serie_a_df = pd.read_csv('data/serie-a.csv')

    # Combine datasets into a single dataframe and rename columns
    combined_df = pd.concat([bundesliga_df, premier_league_df, primera_division_df, ligue_1_df, serie_a_df], ignore_index=True)
    combined_df.rename(columns={'fee_cleaned': 'Transfer Fee in Millions', 'league_name': 'League Name', 'club_name': 'Club Name'}, inplace=True)
    return combined_df

# Function to display images in a responsive layout
def display_images_responsive(image_paths, captions):
    if st.session_state.get('screen_width', 0) <= 640:  # Mobile devices
        for image, caption in zip(image_paths, captions):
            st.image(image, caption=caption, use_column_width=True)
    else:  # Larger screens
        cols = st.columns(3)
        for col, image, caption in zip(cols, image_paths, captions):
            col.image(image, caption=caption, width=200)

# Load data
combined_transfers = load_data()

# App title
st.title('The Financial Dynamics of European Football\'s Elite Leagues')

# Check screen width to adjust layout
screen_width = st.session_state.get('screen_width', 0)
if screen_width == 0:
    st.markdown("""
        <script>
        const updateScreenWidth = () => {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: window.innerWidth
            }, '*');
        };
        updateScreenWidth();
        window.addEventListener('resize', updateScreenWidth);
        </script>
    """, unsafe_allow_html=True)

if screen_width > 0:
    st.session_state['screen_width'] = screen_width

# Introduction to Football Transfer Market
st.header("Introduction to the Football Transfer Market")
st.markdown("""
    The European football transfer market, covering data from the 1992/93 to 2021/22 seasons, presents a dynamic and evolving financial powerhouse, reflecting the sport's competitive spirit and economic evolution. This period has witnessed groundbreaking transfers that have redefined club strategies and economic approaches. Today, it stands as a testament to the evolving financial capabilities of clubs, shaped by sponsorships, media rights, and transformative ownership models. This narrative delves into the pulsating heart of this market, exploring the spending trends, player valuations, and the strategic financial maneuvers that define the competitive landscape of Europe's top football leagues.
""", unsafe_allow_html=True)

# League-Wise Spending Overview
st.header("League-Wise Spending Overview")
st.markdown("""
    Dive into the financial dynamics of Europe's elite football leagues, as seen through data spanning from 1992/93 to 2021/22. This comparative analysis sheds light on the diverse financial strategies employed across leagues – from prioritizing youth development to splurging on marquee signings. Each league's approach tells a unique story of financial planning, club philosophies, and market-driven tactics. The data reveals how spending patterns have evolved over nearly three decades, showcasing the economic growth and strategic shifts within these leagues.
""")
league_spending = combined_transfers[combined_transfers['transfer_movement'] == 'in'].groupby('League Name')['Transfer Fee in Millions'].sum().reset_index().sort_values(by='Transfer Fee in Millions', ascending=False)
fig = px.bar(league_spending, x='League Name', y='Transfer Fee in Millions', title='Total Spending per League (in Million €)')
st.plotly_chart(fig)

# Top 5 Earning Clubs in Each League
st.header("Top 5 Earning Clubs in Each League")
st.markdown("""
    The top 5 earning clubs in each league, across seasons from 1992/93 to 2021/22, are not just football entities; they are economic models of success. This section examines how their on-field performances in domestic and European competitions translate into robust revenue streams, shaping their stature in the transfer market. It's a cycle of success – sporting triumphs boost a club's brand value, attracting sponsorships and investments, which in turn fund future transfers, completing the financial loop.
""")
top_earning_clubs = combined_transfers[combined_transfers['transfer_movement'] == 'out'].groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_earning_clubs_per_league = top_earning_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_earning_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Earning Clubs in Each League (in Million €)')
st.plotly_chart(fig)

# Club-Level Spending Analysis
st.header("Club-Level Spending Analysis")
st.markdown("""
    This analysis offers a glimpse into how club-level spending correlates with success on the pitch, drawing data from 1992/93 to 2021/22. We look at examples of clubs that have mastered the art of building winning teams through judicious spending and those who, despite hefty investments, have yet to see proportional returns. It’s a complex balance of financial acumen and sporting insight, where every euro spent is a bet on future glory.
""")
top_clubs = combined_transfers.groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_clubs_per_league = top_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Spending Clubs in Each League (in Million €)')
st.plotly_chart(fig)

# High-Value Player Transfer Trends
st.header("High-Value Player Transfer Trends")
st.markdown("""
    The high-value transfer segment of the market, from 1992/93 to 2021/22, is a clear indicator of a club’s financial muscle and strategic intent. This analysis also touches upon the impact of external factors such as the COVID-19 pandemic, which has prompted a recalibration of transfer strategies, reflecting the market's resilience and adaptability in face of global economic shifts.
""")
high_value_transfers = combined_transfers[combined_transfers['Transfer Fee in Millions'] > 50].sort_values(by='season')
fig = px.scatter(high_value_transfers, x='season', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name', 'Club Name'], title='High-Value Player Transfer Trends (Transfers Over 50 Million €)')
st.plotly_chart(fig)

# Age vs Transfer Fee Analysis for High-Value Players
st.header("Age vs Transfer Fee Analysis for High-Value Players")
st.markdown("""
    In high-value transfers, from 1992/93 to 2021/22, the correlation between a player's age and their market value is stark. This segment focuses on how 'peak age' varies across positions and significantly influences transfer fees. Young prospects command high prices for their potential, while experienced players bring immediate prowess, each age bracket carrying its unique appeal and risk.
""")
fig = px.scatter(high_value_transfers, x='age', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name', 'Club Name'], title='Age vs Transfer Fee for High-Value Players (Transfers Over 50 Million €)')
st.plotly_chart(fig)

# Spending by Player Position for High-Value Players
st.header("Spending by Player Position for High-Value Players")
st.markdown("""
    This section unravels the economic logic behind the varying transfer fees for different player positions in high-value transfers from 1992/93 to 2021/22. Understanding this aspect offers insights into how clubs value skills and roles differently based on market demand, tactical trends, and the rarity of skill sets.
""")
position_order = ['Goalkeeper', 'Defence', 'Right-Back', 'Centre-Back', 'Left-Back', 'Midfield', 'Defensive Midfield', 'Right Midfield', 'Central Midfield', 'Left Midfield', 'Attacking Midfield', 'Attack', 'Right Winger', 'Left Winger', 'Centre-Forward', 'Second Striker']
fig = px.scatter(high_value_transfers, x='position', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name'], title='Spending by Player Position for High-Value Players (Transfers Over 50 Million €)', category_orders={"position": position_order})
st.plotly_chart(fig)
st.markdown("""
    In recent headline-making transfers, players like Neymar and Kylian Mbappé of Paris Saint-Germain (PSG) have dominated the scene. PSG's ability to fund such high-profile signings stems from their substantial financial backing by Qatar Sports Investments. This investment has not only elevated PSG’s status in the transfer market but also underscores the growing influence of affluent ownership in reshaping the financial landscape of European football.
""")

# URLs or paths to the images
neymar_image = 'images/neymar_image.jpg'
psg_logo = 'images/psg_logo.jpg'
mbappe_image = 'images/mbappe_image.jpg'
image_paths = [neymar_image, psg_logo, mbappe_image]
captions = ['Neymar', 'Paris Saint-Germain', 'Kylian Mbappé']

# Create three columns
col1, col2, col3 = st.columns(3)

# Display an image in each column
with col1:
    st.image(neymar_image, caption='Neymar')

with col2:
    st.image(psg_logo, caption='Paris Saint-Germain')

with col3:
    st.image(mbappe_image, caption='Kylian Mbappé')

# Conclusion
st.header("Conclusion: The Economic Powerhouses of Football")
st.markdown("""
    Our journey through the economic underpinnings of European football, spanning from the 1992/93 to 2021/22 seasons, concludes here, but the story of this financial behemoth continues. Looking ahead, the transfer market is poised to be shaped by emerging trends like new broadcasting deals, the digital transformation of sports, and innovative fan engagement strategies. The interplay of these factors with traditional revenue streams will continue to redefine the economic hierarchy of clubs and leagues, shaping the future narrative of football both on and off the field.
""", unsafe_allow_html=True)