## Epidemic Super Spreaders in Networks

The project allows creating complex network graph using one of the three models:
<ul>
<p>Erdos - Renyi </p>
<p>Watts - Strogatz</p>
<p>Song - Wang</p>
</ul>

<b>Main libraries:</b> <i>PyQt5, Matplotlib, Networkx, Pandas.</i>

On the generated graph the simulation is done using <b>SIR</b>(Susceptible Infected Recover) model.
Simulation can include several iteration with combined results in a single dataframe.
Model parameters:
<ul>
<li>probability of transmission to a neighbors
<li>time steps needed for an individual to heal and recover</li>
<li>time steps after recovering needed for an individual to because susceptible again.</li>
</ul>