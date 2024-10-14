
from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the predictions data
file_path = "dashboard/xgboost_predictions_2024.csv"
predictions_df = pd.read_csv(file_path)

def dashboard(request):
    # Get selected player from dropdown (default first player)
    selected_player = request.GET.get('player', predictions_df['PLAYER_NAME'].iloc[0])
    
    # Filter data for the selected player
    player_data = predictions_df[predictions_df['PLAYER_NAME'] == selected_player].iloc[0]
    
    # Pie chart
    pie_fig = px.pie(
        names=['Fastball', 'Breaking Ball', 'Off-Speed'],
        values=[player_data['PITCH_TYPE_FB'], player_data['PITCH_TYPE_BB'], player_data['PITCH_TYPE_OS']],
        title=f'Expected Pitch Mix for {selected_player}'
    )
    pie_chart = pie_fig.to_html(full_html=False)
    
    # Bar chart
    pitch_types = ['Fastball', 'Breaking Ball', 'Off-Speed']
    pitch_values = [player_data['PITCH_TYPE_FB'], player_data['PITCH_TYPE_BB'], player_data['PITCH_TYPE_OS']]
    bar_fig = go.Figure([go.Bar(x=pitch_types, y=pitch_values, text=pitch_values, textposition='auto')])
    bar_fig.update_layout(title=f'Pitch Type Probabilities for {selected_player}', xaxis_title='Pitch Type', yaxis_title='Probability')
    bar_chart = bar_fig.to_html(full_html=False)
    
    # Get the list of players for the dropdown
    player_options = predictions_df['PLAYER_NAME'].unique()
    
    context = {
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'player_options': player_options,
        'selected_player': selected_player,
    }
    
    return render(request, 'dashboard.html', context)
