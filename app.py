import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# Download dataset
import kagglehub
path = kagglehub.dataset_download("whisperingkahuna/premier-league-2324-team-and-player-insights")

# Load datasets
pl_table_path = os.path.join(path, 'pl_table_2023_24.csv')
xg_data_path = os.path.join(path, 'pl_table_xg_2023_24.csv')
matches_path = os.path.join(path, 'matches_23_24.csv')
top_scorers_path = os.path.join(path, 'Premleg_23_24', 'player_top_scorers.csv')
top_assists_path = os.path.join(path, 'Premleg_23_24', 'player_total_assists_in_attack.csv')
possession_path = os.path.join(path, 'Premleg_23_24', 'possession_percentage_team.csv')

# Load data
pl_table = pd.read_csv(pl_table_path)
xg_data = pd.read_csv(xg_data_path)
matches = pd.read_csv(matches_path)
top_scorers = pd.read_csv(top_scorers_path)
top_assists = pd.read_csv(top_assists_path) if os.path.exists(top_assists_path) else None
possession_data = pd.read_csv(possession_path)


# Introduction
st.title("How Did Manchester City Win the 2023/24 Premier League?")
st.markdown("---")
st.header("Setting the Stage")
st.write(
    "Manchester City entered the 2023/24 Premier League season not just as defending champions but as a team carrying the weight of expectations in one of the most competitive leagues in the world. "
    "Winning the title is a monumental challenge, and retaining it in consecutive seasons is an even greater feat. The Premier League is known for its unpredictability, where even the strongest teams can stumble against determined opponents. "
    "Yet, this season was different. City faced fierce competition from rivals like Arsenal, Liverpool, and Manchester United, endured injuries to key players, and navigated through tactical dilemmas. "
    "But what sets this campaign apart from their previous triumphs? Was it the sheer consistency that saw them amass 91 points, or the resilience to overcome challenges that would have derailed most teams? "
    "\n\n"
    "This data story delves into what made their journey so remarkable. It examines not only the tactical brilliance and individual performances that defined their season but also the adversities they overcame to make this season into history. "
    "Compared to previous campaigns, this was a season of evolution, showcasing Guardiola’s ability to adapt and innovate while the team redefined the benchmarks of football excellence."
)


# Visualization: Points Comparison
st.subheader("Points Comparison Across Teams")
st.write(
    "Historically, the average points needed to win the Premier League is 87.8, reflecting the intense competition in the league. "
    "However, since Pep Guardiola's arrival in the 2016/17 season, this average has increased significantly to 93.6 points, emphasizing the level of consistency required to compete at the top. "
    "Interestingly, over the last two seasons, this average has slightly dropped to 90.0 points, showcasing the high standards Guardiola and his team have set for the league. "
    "The Premier League table highlights Manchester City's consistency and dominance, finishing with 91 points. "
    "This achievement is even more impressive considering the competitiveness of the league, where every point must be earned through hard-fought matches. "
    "Interestingly, Arsenal's 89 points also surpass the historical league average of 87.8, highlighting the high standards of competition in the 2023/24 season."
)

# Sorting data and adding the average lines
xg_data_sorted = xg_data.sort_values(by='pts', ascending=False)

fig = px.bar(
    xg_data_sorted,
    x='name',
    y='pts',
    color='pts',
    title="Points Comparison",
    labels={"name": "Teams", "pts": "Points"},
    color_continuous_scale='Blues'
)

# Adding average lines
fig.add_hline(y=87.8, line_dash="dot", line_color="red", annotation_text="Historical Avg: 87.8", annotation_position="bottom right")
fig.add_hline(y=90.0, line_dash="dot", line_color="green", annotation_text="Recent Avg: 90.0", annotation_position="top right")

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")


# Attack and Defense
st.header("Manchester City's Attack and Defense")
st.write(
    "Manchester City's attack was led by a combination of experienced players and emerging talents. "
    "Erling Haaland, the team's star striker, continued his incredible scoring streak, while Phil Foden added creativity and versatility to the attack. "
    "City's ability to score goals consistently, both home and away, was a key factor in their success. "
    "Their attacking play was characterized by quick transitions, precise passing, and clinical finishing. "
    "Haaland's presence in the box was a constant threat to opponents, while players like Foden and De Bruyne orchestrated plays from midfield. "
    "Moreover, their tactical flexibility allowed other players like Julian Alvarez and Jack Grealish to step up and make significant contributions when needed. "
    "City’s offensive strategy also involved their fullbacks, who often overlapped and created width, making it difficult for opponents to defend. "
    "Their relentless pressing ensured they could recover possession high up the pitch, often leading to scoring opportunities."
)
fig = px.bar(
    top_scorers[top_scorers['Team'] == 'Manchester City'],
    x='Player',
    y='Goals',
    color='Goals',
    title="Top Scorers for Manchester City",
    labels={"Player": "Players", "Goals": "Goals"},
    color_continuous_scale='Viridis'
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Defensive Stability")
st.write(
    "While their attack grabbed headlines, Manchester City's defense was equally impressive. "
    "With a well-organized backline and a reliable goalkeeper, they managed to maintain one of the best defensive records in the league. "
    "City's ability to shut down opponents and control games from the back was a testament to their defensive discipline and tactical setup. "
    "Key players like Ruben Dias and Joško Gvardiol formed the backbone of the defense, providing both physicality and composure. "
    "Goalkeeper Ederson was instrumental, not only with his shot-stopping abilities but also with his distribution, which often initiated counterattacks. "
    "Additionally, City’s defensive midfielders, such as Rodri, played a pivotal role in shielding the defense and breaking up opposition attacks. "
    "Their ability to defend as a unit and adapt to various challenges made them a tough team to break down throughout the season. "
    "A key metric to evaluate defensive performance is 'Expected Goals Conceded' (xGC), which estimates the quality of chances that opponents create. "
    "Manchester City's xGC was among the lowest in the league, demonstrating their defensive organization. However, it is worth noting that Arsenal had an even better xGC, highlighting their defensive strength. "
    "Despite this, Manchester City's offensive power, spearheaded by players like Haaland, compensated for any minor defensive shortcomings. "
    "This balance between attack and defense was crucial to their overall success."
)
clean_sheets = xg_data_sorted[['name', 'xgConceded']].sort_values('xgConceded')
fig = px.bar(
    clean_sheets,
    x='name',
    y='xgConceded',
    color='xgConceded',
    title="Expected Goals Conceded Comparison",
    labels={"name": "Teams", "xgConceded": "Expected Goals Conceded"},
    color_continuous_scale='RdBu'
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")


# Challenges Faced by Manchester City
st.header("Challenges Faced by Manchester City")
st.write(
    "Manchester City's path to the 2023/24 Premier League title was anything but smooth. "
    "The season posed several significant challenges that tested the team’s resilience and ability to adapt. "
    "Despite their eventual triumph, these hurdles highlighted the effort required to maintain dominance in the world's toughest football league."
)

st.subheader("Key Injuries to Star Players")
st.write(
    "One of the most notable challenges was the absence of key players due to injuries. Kevin De Bruyne, "
    "the creative heartbeat of the midfield, missed large portions of the season due to recurring injuries. "
    "Similarly, defensive stalwarts like John Stones faced fitness issues, forcing Guardiola to reshuffle his tactical setup. "
    "Phil Foden, Rodri, and other squad members stepped up to fill these voids, but the disruption required constant adjustments to maintain performance."
)

st.subheader("Intense Competition from Arsenal")
st.write(
    "Arsenal emerged as a formidable rival during the campaign, pushing Manchester City to the limit. "
    "With their exceptional defensive record and consistent performances, Arsenal stayed neck-and-neck with City in the title race. "
    "The competition added pressure to every match, with City needing to secure critical victories to stay ahead in the standings. "
    "This rivalry injected a sense of urgency into their campaign and highlighted the importance of composure and focus in high-stakes games."
)

st.subheader("Managing Multiple Competitions")
st.write(
    "Competing on multiple fronts, including the Champions League and domestic cups, placed immense physical and mental strain on the squad. "
    "Balancing the demands of different tournaments required meticulous squad rotation and workload management. "
    "Guardiola’s tactical adjustments and the team’s depth allowed them to handle this pressure, but it often came at the cost of fatigue and occasional dips in performance."
)

st.markdown("---")


# Tactical Mastery and Guardiola's Influence
st.header("Tactical Mastery and Guardiola's Influence")
st.write(
    "Pep Guardiola's tactical philosophy is a cornerstone of Manchester City's success. His approach emphasizes control, creativity, and adaptability, allowing City to dominate games regardless of the opponent. "
    "This season, Guardiola's tactics were evident in City's high possession rates and their ability to break down defensive blocks. His emphasis on positional play ensures that every player knows their role, "
    "making City a well-oiled machine on the field. Guardiola's brilliance was further recognized when he was awarded the 'Manager of the Season' title, a testament to his outstanding leadership and tactical ingenuity."
)
pep_image = Image.open("pep_guardiola.jpg")
st.image(pep_image, caption="Pep Guardiola", use_container_width=True)
st.write(
    "Guardiola's adaptability was critical in overcoming tactical challenges posed by other top teams. For instance, his use of John Stones in a hybrid defender-midfielder role disrupted opponents' plans and added "
    "an element of surprise to City's gameplay. This tactical flexibility, combined with meticulous planning and execution, allowed City to maintain their dominance throughout the season."
)
st.markdown("---")

# Visualization: Possession Percentage
st.subheader("Control as a Strategy")
st.write(
    "Possession is a hallmark of Guardiola's teams, and Manchester City was no exception this season. "
    "By controlling the ball, City minimized the opposition's opportunities while creating numerous chances of their own. "
    "Their average possession percentage was among the highest in the league, reflecting their dominance in most matches."
    "Manchester City's ability to maintain possession allowed them to dictate the tempo of games, "
    "forcing opponents to chase the ball and limiting their attacking opportunities. "
    "This approach not only showcased City's technical superiority but also highlighted Guardiola's influence in fostering a team-first mentality."
)
fig = px.bar(
    possession_data,
    x='Team',
    y='Possession (%)',
    color='Possession (%)',
    title="Possession Percentage Across Teams",
    labels={"Team": "Teams", "Possession (%)": "Possession (%)"},
    color_continuous_scale='Plasma'
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
st.write(
    "Guardiola's philosophy is rooted in the concept of total football, where players interchange roles seamlessly to maintain fluidity and control. "
    "He places a strong emphasis on ball retention and quick, precise passing to manipulate the opposition's defensive structure. "
    "Another hallmark of Guardiola's strategy is the high press, where players aggressively win back possession in the opponent's half, preventing counterattacks. "
    "This pressing style not only disrupts the opposition but also creates immediate opportunities to attack. "
    "Guardiola is also known for his meticulous planning, analyzing every detail of the opponent to exploit their weaknesses. "
    "His use of false nines and inverted fullbacks has redefined traditional roles in football, adding layers of complexity to City's game plan. "
    "This season, Guardiola's use of wide players like Jack Grealish to stretch the field opened up spaces for midfielders and attackers to exploit. "
    "Guardiola's philosophy is not just about winning games but also about creating a style of play that is aesthetically pleasing and effective. "
    "This dual focus on results and entertainment has made Manchester City a joy to watch and a nightmare to compete against."
)
st.markdown("---")


# The Team Behind the Success
st.header("The Team Behind the Success")

## Phil Foden: Player of the Season
foden_image = Image.open("phil_foden.jpg")
st.image(foden_image, caption="Phil Foden", use_container_width=True)
st.write(
    "Phil Foden had an extraordinary season, cementing his status as one of the most important players in Manchester City's lineup. "
    "Despite being only a midfielder and not a traditional striker, Foden finished among the top contributors in the league, showcasing his incredible skill set. "
    "He ended the season ranked sixth in combined goals and assists, a remarkable achievement considering his position on the field. "
    "What sets Foden apart is his unique technical ability and vision, which allow him to execute plays that few others can. "
    "Not only is he an exceptional scorer, but he is also one of the most creative players in the league, frequently setting up his teammates with precise passes and well-timed through balls. "
    "His knack for creating chances makes him a constant threat to opposing defenses, and his performances this season earned him the well-deserved title of Player of the Season. "
    "Foden's development as a homegrown talent from Manchester City's academy is a testament to the club's emphasis on nurturing young players and integrating them into the first team."
)

# Data for Top 10 Combined Goals and Assists in the League
if top_scorers is not None and top_assists is not None:
    # Merge top scorers and top assists data
    top_scorers_assists = top_scorers.merge(
        top_assists, on="Player", suffixes=("_goals", "_assists")
    )

    # Top 10 Players by Chances Created
    top_chances_created = top_scorers_assists.nlargest(10, "Chances Created")
    fig_top_chances = px.bar(
        top_chances_created,
        x="Player",
        y="Chances Created",
        color="Chances Created",
        title="Top 10 Players: Chances Created",
        labels={"Player": "Players", "Chances Created": "Chances Created"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_top_chances, use_container_width=True)
else:
    st.write("Data for combined goals, assists, and chances created is not available.")

## Squad Evolution and Key Transfers
st.write(
    "Manchester City's success during the 2023/24 season was greatly enhanced by their strategic moves in the transfer market. "
    "One of the standout signings was Joško Gvardiol, a highly talented Croatian defender acquired from RB Leipzig. "
    "Known for his physicality, composure on the ball, and tactical intelligence, Gvardiol quickly adapted to the demands of the Premier League. "
    "His presence in defense not only provided stability but also allowed the team to play out from the back with greater confidence. "
)
transfer_image = Image.open("josko_gvardiol.jpg")
st.image(transfer_image, caption="Joško Gvardiol", use_container_width=True)
st.write(
    "Another key acquisition was Mateo Kovačić, a seasoned midfielder signed from Chelsea. His creativity, ball retention, and experience in high-pressure matches added depth to City's already formidable midfield. "
    "Jérémy Doku, the dynamic winger from Stade Rennes, brought pace and flair to the flanks, making City's attack more unpredictable. "
    "Doku's ability to beat defenders in one-on-one situations opened up space for teammates and added a new dimension to City's offensive play. "
    "These signings, coupled with the existing squad depth, ensured that Manchester City could compete across all fronts, maintaining their high standards in both domestic and international competitions. "
    "The blend of young talents like Gvardiol and Doku with experienced players like Kovačić exemplifies City's balanced approach to squad building. "
    "This calculated strategy in the transfer market highlights the club's commitment to both immediate success and sustainable growth."
)
st.markdown("---")


# Manchester City vs Top Teams
st.header("Manchester City vs Top Teams")
st.write(
    "The Premier League's competitiveness is especially evident in matches between the top teams. Manchester City's performance against Arsenal, Liverpool, Manchester United, Tottenham Hotspur, and Chelsea "
    "showcases their ability to dominate and deliver in high-stakes games. Remarkably, City only suffered one defeat against these top teams during the entire season, underscoring their consistency and tactical superiority. "
    "This success was not just a result of tactical brilliance but also the team's remarkable mental strength. In challenging situations, whether trailing in a match or playing under intense pressure, City consistently displayed composure and resilience."
)

# Filter for Opponent Teams
matches['Score'] = matches['Score'].str.replace('_', ' : ').str.strip()
top_teams = ["Arsenal", "Liverpool", "Manchester United", "Tottenham Hotspur", "Chelsea"]
selected_team = st.selectbox("Select Opponent:", options=top_teams)
filtered_matches = matches[
    ((matches["Home Team"] == "Manchester City") & (matches["Away Team"] == selected_team)) |
    ((matches["Away Team"] == "Manchester City") & (matches["Home Team"] == selected_team))
]
st.write(f"### Matches against {selected_team}")

for index, row in filtered_matches.iterrows():
    home_logo_path = f"logos/{row['Home Team'].replace(' ', '_').lower()}.png"
    away_logo_path = f"logos/{row['Away Team'].replace(' ', '_').lower()}.png"
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if os.path.exists(home_logo_path):
            home_logo = Image.open(home_logo_path)
            st.image(home_logo, width=50)
        st.markdown(f"<p style='text-align: center;'>{row['Home Team']}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<p style='text-align: center; font-size: 16px;'><b>{row['Score']}</b><br><span style='font-size: 12px;'>{row['UTC Time'][:10]}</span></p>", 
            unsafe_allow_html=True
        )
    with col3:
        if os.path.exists(away_logo_path):
            away_logo = Image.open(away_logo_path)
            st.image(away_logo, width=50)
        st.markdown(f"<p style='text-align: center;'>{row['Away Team']}</p>", unsafe_allow_html=True)

st.markdown("---")


# Conclusion
st.header("Conclusion")
st.write(
    "Manchester City’s 2023/24 Premier League campaign will be remembered as a season of resilience, brilliance, and triumph over adversity. "
    "Despite facing challenges such as injuries to star players like Kevin De Bruyne, intense competition from Arsenal, "
    "and the demands of managing multiple competitions, City adapted and overcame. "
    "The team’s depth, with players like Phil Foden stepping into critical roles, and Guardiola’s tactical ingenuity, "
    "ensured they maintained consistency. Arsenal’s defensive strength kept the title race tight, but City’s superior goal-scoring ability "
    "and mental resilience ultimately set them apart. Their dominance against top teams and ability to thrive in high-pressure moments "
    "highlighted the incredible synergy within the team and Guardiola’s exceptional leadership."
)

st.write(
    "City’s journey wasn’t just about retaining their title but about redefining dominance in the Premier League. "
    "Strategic acquisitions, like Joško Gvardiol and Mateo Kovačić, added fresh depth to the squad, ensuring long-term success. "
    "What makes this season unique isn’t just the points tally but how City overcame obstacles with determination and grit. "
    "Their balance between individual brilliance and collective effort was key to their success. "
    "This campaign proved that even in the face of adversity, tactical brilliance, mental strength, and squad depth can lead to greatness. "
    "City’s triumph is a story of persistence, innovation, and an unrelenting hunger for excellence, cementing their place as the gold standard in modern football."
)