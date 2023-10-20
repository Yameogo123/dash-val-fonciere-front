import folium
import geopandas as gpd
import pandas as pd


def Map():
    # Charger les données géographiques des départements français
    france_geojson = gpd.read_file('./assets/departements.geojson')

    # Trouver les limites géographiques de la France
    # france_bounds = [france_geojson.bounds.minx.min(), france_geojson.bounds.miny.min(),
    #                 france_geojson.bounds.maxx.max(), france_geojson.bounds.maxy.max()]

    # Calculer les limites du graphique pour centrer la vue sur la France
    # lon_center = (france_bounds[0] + france_bounds[2]) / 2
    # lat_center = (france_bounds[1] + france_bounds[3]) / 2
    # lon_range = [france_bounds[0], france_bounds[2]]
    # lat_range = [france_bounds[1], france_bounds[3]]

    # Charger les données sur la valeur foncière moyenne par département
    df = pd.read_pickle('./assets/dataframe_avec_coord.pkl')

    max_lat = df['latitude'].max()
    min_lat = df['latitude'].min()
    max_lon = df['longitude'].max()
    min_lon = df['longitude'].min()

    ######
    codesHauteCorse = [20000]
    codesBasseCorse = [20600, 20620]
    for i in (20100, 20191):
        codesHauteCorse.append(i)
    for i in (20200, 20290):
        codesBasseCorse.append(i)
    #codesCorse_str = list(map(str, codesHauteCorse + codesBasseCorse))
    df['Code_postal'] = df['Code_postal'].astype(str)
    df['Departement'] = df['Code_postal'].apply(lambda x: '2A' if x in codesBasseCorse else (
        '2B' if x in codesHauteCorse else ('0' + x[:1] if len(x) == 4 else x[:2])))
    df['Departement'] = df['Departement'].astype(str)

    data = df.groupby('Departement')['Valeur_fonciere'].mean().reset_index()
    ######

    m = folium.Map(location=[(max_lat + min_lat) / 2, (max_lon + min_lon) / 2], zoom_start=5, control_scale=True,
               min_lat=min_lat, max_lat=max_lat,
               min_lon=min_lon, max_lon=max_lon)
    
    choropleth = folium.Choropleth(
        geo_data='./assets/departements.geojson',
        name='choropleth',
        data=data,
        columns=['Departement', 'Valeur_fonciere'],
        key_on='feature.properties.code',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Valeur foncière moyenne'
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m