from scipy.ndimage import gaussian_filter
from mplsoccer import Pitch
import matplotlib.pyplot as plt

def draw_position_dist(df, cluster: str):
    df_cluster = df[df['cluster'] == cluster]
    
    pitch = Pitch(pitch_color='#aabb97', line_color='white', stripe_color='#c2d59d', stripe=True, line_zorder=2,)
    fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0, axis=False, title_space=0, grid_height=0.82, endnote_height=0.05)
    fig.set_facecolor('#22312b')

    bin_statistic = pitch.bin_statistic(df_cluster['x'], df_cluster['y'], statistic='count', bins=(25, 25)) 
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
    pcm = pitch.heatmap(bin_statistic, ax=axs['pitch'], cmap='hot', edgecolors='#22312b')
    cbar = fig.colorbar(pcm, ax=axs['pitch'], shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    cbar.ax.yaxis.set_tick_params(color='#efefef')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')

    axs['endnote'].text(0.4, 0, 'Attacking Direction', va='center', ha='center', color='#c7d5cc', fontsize=12)
    axs['endnote'].arrow(0.3, 0.6, 0.2, 0, head_width=0.2, head_length=0.025, ec='w', fc='w')
    axs['endnote'].set_xlim(0, 1)
    axs['endnote'].set_ylim(0, 1)
    axs['title'].text(0.5, 0.7, f'The position distribution for cluster {cluster}', color='#c7d5cc', va='center', ha='center', fontsize=30)
    axs['title'].text(0.5, 0.25, 'The Game\'s First Half', color='#c7d5cc', va='center', ha='center', fontsize=18)