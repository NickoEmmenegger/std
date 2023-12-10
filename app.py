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

def convert_season_to_year(season):
    return int(season.split('/')[0])

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
    This datastory dives deep into the financial dynamics of European football, focusing on the top five leagues, known for their competitive spirit and economic prowess. These leagues include:

    - **Premier League** (England): Renowned for its intense competition and global fanbase, the Premier League stands as a symbol of English football's rich history and financial strength.
    - **La Liga** (Spain): Home to some of the world's most famous clubs, La Liga combines technical skill with the passion of Spanish football culture.
    - **Bundesliga** (Germany): Known for its world-class player development and fan-friendly atmosphere, the Bundesliga is a cornerstone of German football.
    - **Serie A** (Italy): With a legacy of tactical innovation, Serie A has been the breeding ground for some of football's greatest legends.
    - **Ligue 1** (France): A league that has risen rapidly in profile, Ligue 1 is marked by its flair and the emergence of global football stars.
""", unsafe_allow_html=True)

# Assuming you have the logo images stored in the 'images' folder
premier_league_logo = 'images/premier_league_logo.jpg'
la_liga_logo = 'images/la_liga_logo.jpg'
bundesliga_logo = 'images/bundesliga_logo.jpg'
serie_a_logo = 'images/serie_a_logo.jpg'
ligue_1_logo = 'images/ligue_1_logo.jpg'
logos = [premier_league_logo, la_liga_logo, bundesliga_logo, serie_a_logo, ligue_1_logo]

# Logos and their descriptions
logos = [
    (premier_league_logo, "Premier League"),
    (la_liga_logo, "La Liga"),
    (bundesliga_logo, "Bundesliga"),
    (serie_a_logo, "Serie A"),
    (ligue_1_logo, "Ligue 1")
]

# Display logos with descriptions side by side
cols = st.columns(5)

# You might need to adjust these widths manually
# These are just example values; adjust them based on your images
widths = [150, 140, 130, 120, 110]  # Example widths for each logo

for col, (logo, description), width in zip(cols, logos, widths):
    col.image(logo, caption=description, width=width)

st.markdown("""
    These leagues not only represent the pinnacle of European football but also serve as significant economic entities in the global sports market. The following analysis presents a comprehensive view of their financial transactions, particularly in player transfers, from the 1992/93 to 2021/22 seasons.
""")

# League-Wise Spending Overview
st.header("League-Wise Spending Overview")
st.markdown("""
    Dive into the financial dynamics of Europe's elite football leagues, as seen through data. This comparative analysis sheds light on the diverse financial strategies employed across leagues from prioritizing youth development to splurging on marquee signings. Each league's approach tells a unique story of financial planning, club philosophies, and market-driven tactics. The data reveals how spending patterns have evolved over nearly three decades, showcasing the economic growth and strategic shifts within these leagues.
""")
# Convert 'Transfer Fee in Millions' to billions
league_spending = combined_transfers[combined_transfers['transfer_movement'] == 'in'].groupby('League Name')['Transfer Fee in Millions'].sum().reset_index().sort_values(by='Transfer Fee in Millions', ascending=False)
league_spending['Transfer Fee in Billions'] = league_spending['Transfer Fee in Millions'] / 1000
# Create the bar plot with values in billions
fig = px.bar(league_spending, x='League Name', y='Transfer Fee in Billions', title='Total Spending per League', labels={'Transfer Fee in Billions': 'Total Spending in Billion €'})
st.plotly_chart(fig, use_container_width=True)

# Top 5 Earning Clubs in Each League
st.header("Top 5 Earning Clubs in Each League")
st.markdown("""
    The top 5 earning clubs in each league are not just football entities, they are also economic models of success. This section examines how their on-field performances in domestic and European competitions translate into robust revenue streams, shaping their stature in the transfer market. It's a cycle of success. Sporting triumphs boost a club's brand value, attracting sponsorships and investments, which in turn fund future transfers, completing the financial loop.
""")
top_earning_clubs = combined_transfers[combined_transfers['transfer_movement'] == 'out'].groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_earning_clubs_per_league = top_earning_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_earning_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Earning Clubs in Each League')
st.plotly_chart(fig)

# Club-Level Spending Analysis
st.header("Club-Level Spending Analysis")
st.markdown("""
    This analysis offers a glimpse into how club-level spending correlates with success on the pitch. We look at examples of clubs that have mastered the art of building winning teams through judicious spending and those who, despite hefty investments, have yet to see proportional returns. It’s a complex balance of financial acumen and sporting insight, where every euro spent is a bet on future glory.
""")
top_clubs = combined_transfers.groupby(['League Name', 'Club Name'])['Transfer Fee in Millions'].sum().reset_index().sort_values(by=['League Name', 'Transfer Fee in Millions'], ascending=[True, False])
top_5_clubs_per_league = top_clubs.groupby('League Name').head(5)
fig = px.bar(top_5_clubs_per_league, x='Club Name', y='Transfer Fee in Millions', color='League Name', title='Top 5 Spending Clubs in Each League')
st.plotly_chart(fig)

# High-Value Player Transfer Trends
st.header("High-Value Player Transfer Trends")
st.markdown("""
    The high-value transfer segment of the market is a clear indicator of a club’s financial muscle and strategic intent. This analysis also touches upon the impact of external factors such as the COVID-19 pandemic, which has prompted a recalibration of transfer strategies, reflecting the market's resilience and adaptability in face of global economic shifts.
""")
combined_transfers['season_start_year'] = combined_transfers['season'].apply(convert_season_to_year)
sorted_transfers = combined_transfers.sort_values('season_start_year')
high_value_transfers = sorted_transfers[sorted_transfers['Transfer Fee in Millions'] > 50]
unique_sorted_seasons = sorted(high_value_transfers['season'].unique(), key=lambda x: int(x.split('/')[0]))
fig = px.scatter(high_value_transfers, x='season', y='Transfer Fee in Millions', color='League Name', 
                 hover_data=['player_name', 'Club Name'], title='High-Value Player Transfer Trends (Over 50 Million €)',
                 category_orders={"season": unique_sorted_seasons})
st.plotly_chart(fig, use_container_width=True)

# Age vs Transfer Fee Analysis for High-Value Players
st.header("Age vs Transfer Fee Analysis for High-Value Players")
st.markdown("""
    In high-value transfers the correlation between a player's age and their market value is stark. This segment focuses on how 'peak age' varies across positions and significantly influences transfer fees. Young prospects command high prices for their potential, while experienced players bring immediate prowess, each age bracket carrying its unique appeal and risk.
""")
fig = px.scatter(high_value_transfers, x='age', y='Transfer Fee in Millions', color='League Name', hover_data=['player_name', 'Club Name'], title='Age vs Transfer Fee for High-Value Players (Transfers Over 50 Million €)')
st.plotly_chart(fig)

# Spending by Player Position for High-Value Players
st.header("Spending by Player Position for High-Value Players")
st.markdown("""
    This section unravels the economic logic behind the varying transfer fees for different player positions in high-value transfers. Understanding this aspect offers insights into how clubs value skills and roles differently based on market demand, tactical trends, and the rarity of skill sets.
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

# Total Spending Across the Top Five Leagues Over the Years
st.header("Total Spending Across the Top Five Leagues Over the Years")
st.markdown("""
    In this part of our story, we're going to look at how much money the big five football leagues have spent over the years. We're not just looking at one league, but all five together. It's interesting because it shows us how the world of football likes to bring in new players. We'll see the times when these leagues spend a lot of money and times when they don't. This helps us understand how football works as a business.
""")
total_spending_per_season = combined_transfers.groupby('season')['Transfer Fee in Millions'].sum().reset_index()
fig = px.line(total_spending_per_season, x='season', y='Transfer Fee in Millions', title='Total Spending Across the Top Five Leagues Over the Years', labels={'Transfer Fee in Millions': 'Total Spending in Millions'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
When we look at the money spent by the top five football leagues over time, we can see that they have been spending more and more each year. This shows that football is getting bigger and clubs are willing to pay more to get the best players.

But then, we see the amount of money spent starts to go down. This happened when the COVID-19 pandemic hit. Because of the virus, football games were stopped or played without fans. This meant clubs didn't make as much money from tickets and couldn't spend as much on new players.

Now, the world is slowly getting better after the pandemic, and football clubs are starting to spend more money again. They are finding new ways to make money, like through the internet, and are ready to buy players again. We think that in the next few years, the clubs will probably spend even more money than they did before the pandemic.

In short, even though there was a drop in spending because of COVID-19, it looks like things are getting back on track. The love for football is strong, and clubs will always look for the best players to make their teams better.
""")

# Conclusion
st.header("Conclusion: The Economic Powerhouses of Football")
st.markdown("""
    Our journey through the financial side of European football ends here. This world, where excitement for the game meets money matters, keeps changing. Digital changes are making a big impact, with clubs using online ways to connect with fans and earn more. This isn't just about keeping fans happy, but also about making more money and reaching people all over the world. Clubs are getting better at using the internet, which helps them get more sponsors and make their brand stronger.

    New deals for showing games on the internet are also changing how money is made in football. More people watching online could mean more money from these deals. This change might help not just the big clubs, but also the smaller ones with dedicated fans. Clubs are also trying new things to keep fans engaged, like digital tokens and fun online experiences. These not only make the fan experience better but also open new ways to make money. 

    Traditional ways of making money, like selling tickets, merch, and sponsor deals, are still important. But how they mix with these new trends will change which clubs and leagues are the most powerful. Looking ahead, the story of football, both in the game and in the business, is set to get really interesting. Clubs that can handle these economic chances and challenges well will become the new leaders in the sport. The way money works in football is changing as fast as the game itself, keeping fans and experts excited and guessing. 

    To sum up, the European football transfer market is an exciting mix of money, planning, and excitement for the game. Its future, shaped by the ongoing digital changes and worldwide economic shifts, is going to change the heart of the sport. It's a thrilling time for everyone involved fans, players, and those running the show.
""", unsafe_allow_html=True)